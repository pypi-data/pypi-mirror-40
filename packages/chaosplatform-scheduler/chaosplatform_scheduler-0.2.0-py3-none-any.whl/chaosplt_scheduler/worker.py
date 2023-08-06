import logging
import shutil
import threading
import time
from typing import Any, Dict
import uuid

import psutil
from psutil import Popen

__all__ = ["initialize_worker", "ChaosPlatformWorker", "start_worker",
           "stop_worker"]
logger = logging.getLogger("chaosplatform")


class ChaosPlatformWorker:
    def __init__(self, queue: str, worker_name: str, worker_directory: str,
                 log_level: str = "INFO", count_worker: int = 1,
                 add_suffix: bool = False, supervising_interval: int = 2):
        # worker params
        self.queue_name = queue
        self.worker_name = worker_name
        self.worker_directory = worker_directory
        self.log_level = log_level
        self.count_worker = count_worker
        self.add_suffix = add_suffix

        # internal machinery
        self._lock = threading.Lock()
        self._running = False
        self._processes = []
        self.supervising_interval = supervising_interval
        self.supervisor = threading.Thread(None, self.supervise)

    @property
    def running(self) -> bool:
        with self._lock:
            return self._running

    @running.setter
    def running(self, value: bool):
        with self._lock:
            self._running = value

    @property
    def workers_count(self):
        return len(self._processes)

    def start(self):
        """
        Start the worker and starts supervising its processes
        """
        logger.info('Starting {} workers...'.format(self.count_worker))
        self.running = True
        list(map(self._start_worker, range(self.count_worker)))
        self.supervisor.start()

    def stop(self):
        """
        Terminate all the process workers
        """
        logger.info('Stopping all workers...')
        self.running = False
        for p in self._processes:
            logger.info("Terminating worker (PID {})".format(p.pid))
            p.terminate()
            ret = p.wait()
            logger.info(
                "Worker (PID {}) terminated with return code {}".format(
                    p.pid, ret))
        self.supervisor.join(timeout=0.5)
        self._processes = []

    def supervise(self):
        """
        Supervise all workers and restart any instance that has died
        """
        logger.info("Starting worker supervisors...")
        while self.running:
            for i, p in enumerate(self._processes[:]):
                # exit fast
                if not self.running:
                    return

                if not p.is_running() or p.status() == psutil.STATUS_ZOMBIE:
                    self._processes.remove(p)
                    logger.warning(
                        "Worker (PID {}) gone, starting a new one...".format(
                            p.pid))
                    self._start_worker(i)

            time.sleep(self.supervising_interval)
        logger.info("Worker supervisor is now terminated")

    def _start_worker(self, index: int):
        """
        Start a new worker child process
        """
        logger.info("Creating a new worker")

        path = shutil.which("chaosplatform-worker")
        name = self.worker_name
        if self.add_suffix:
            name = "{}-{}".format(name, uuid.uuid4().hex)

        args = [
            path,
            "--name", name,
            "--queue", self.queue_name
        ]

        if self.log_level == "DEBUG":
            args.append("--verbose")

        # notice, the current's process environment variables will be passed
        # down to the child worker process
        logger.debug("Executing: {}".format(" ".join(args)))
        p = Popen(
            args, stdout=None,
            stderr=None, shell=False, cwd=self.worker_directory)
        self._processes.append(p)
        logger.info("Worker '{}' started (PID {})".format(name, p.pid))


def initialize_worker(queue_name: str, worker_name: str,
                      config: Dict[str, Any]) -> ChaosPlatformWorker:
    """
    Create a worker instance and attach a connection to a redis server
    """
    worker_config = config["worker"]
    worker = ChaosPlatformWorker(
        queue=queue_name, worker_name=worker_name,
        add_suffix=worker_config.get("add_random_suffix_to_worker_name"),
        worker_directory=worker_config["worker_directory"],
        log_level="DEBUG" if worker_config["debug"] else "INFO",
        count_worker=int(worker_config.get("count", 1)),
        supervising_interval=float(worker_config.get(
            "supervising_interval", 2))
    )
    return worker


def start_worker(worker: ChaosPlatformWorker):
    """
    Run the worker
    """
    logger.info("Starting worker")
    worker.start()


def stop_worker(worker: ChaosPlatformWorker):
    """
    Stop and release the worker
    """
    logger.info("Stopping worker")
    worker.stop()
