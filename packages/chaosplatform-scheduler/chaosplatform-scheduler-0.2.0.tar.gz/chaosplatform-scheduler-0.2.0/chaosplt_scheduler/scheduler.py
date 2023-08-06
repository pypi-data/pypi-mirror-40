import logging
import threading
import time
from typing import Any, Dict

from redis import Redis
from rq import Queue
from rq.job import Job
from rq_scheduler import Scheduler
from rq_scheduler.utils import setup_loghandlers

__all__ = ["create_scheduler", "ChaosPlatformScheduler", "start_scheduler",
           "stop_scheduler", "create_scheduler_queue"]
logger = logging.getLogger("chaosplatform")


class ChaosPlatformScheduler(threading.Thread, Scheduler):
    def __init__(self, *args, **kwargs):
        """
        A scheduler based on the `rq` scheduler but in its own thread.
        """
        threading.Thread.__init__(self)
        Scheduler.__init__(self, *args, interval=10, **kwargs)

        self._lock = threading.Lock()
        self._running = False

    @property
    def running(self):
        """
        Flag indicating whether the scheduler is currently active
        """
        with self._lock:
            return self._running

    @running.setter
    def running(self, state: bool):
        """
        Mark the scheduler as active or inactive
        """
        with self._lock:
            self._running = state

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, step: int):
        self._interval = step

    def stop(self):
        """
        Terminate the scheduler

        When done, the current thread is exited.
        """
        self.log.info('Stopping scheduler...')
        self.running = False
        self.register_death()
        self.remove_lock()

    def run(self):
        """
        Scheduler thread mainloop

        Runs until the `running` flag is set to `False`.
        """
        self.log.info('Starting scheduler...')
        self.running = True
        self.register_birth()

        while self.running:
            start_time = time.time()
            if self.acquire_lock():
                self.enqueue_jobs()
                self.remove_lock()

            # from rq-scheduler run
            seconds_elapsed_since_start = time.time() - start_time
            seconds_until_next_scheduled_run = \
                self._interval - seconds_elapsed_since_start
            if self.running and seconds_until_next_scheduled_run > 0:
                time.sleep(seconds_until_next_scheduled_run)

        self.log.info('Exiting scheduler...')


def create_scheduler(queue: Queue, config: Dict[str, Any],
                     job_class: Job = Job) -> ChaosPlatformScheduler:
    """
    Create a scheduler on the given queue and job class
    """
    log_level = 'DEBUG' if config.get('debug') else 'INFO'
    setup_loghandlers(level=log_level)
    return ChaosPlatformScheduler(
        queue=queue, connection=queue.connection,
        queue_class=queue.__class__,
        job_class=job_class)


def create_scheduler_queue(name: str, connection: Redis,
                           is_async: bool = True) -> Queue:
    """
    Instanciate the scheduler queue connection
    """
    return Queue(name, connection=connection, is_async=is_async)


def start_scheduler(scheduler: ChaosPlatformScheduler):
    """
    Run the scheduler application forever
    """
    logger.info("Starting scheduler")
    scheduler.start()


def stop_scheduler(scheduler: ChaosPlatformScheduler):
    """
    Stop and release the scheduler
    """
    logger.info("Stopping scheduler")
    scheduler.stop()


def initialize_scheduler_queue(config: Dict[str, Any]) \
                               -> ChaosPlatformScheduler:
    queue_name = config["redis"].pop("queue")
    connection_params = config.get("redis")
    connection = Redis(**connection_params)
    queue = create_scheduler_queue(queue_name, connection=connection)
    return create_scheduler(queue=queue, config=config)
