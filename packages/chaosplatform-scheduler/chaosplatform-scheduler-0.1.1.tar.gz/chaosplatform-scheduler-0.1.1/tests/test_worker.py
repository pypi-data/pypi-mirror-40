import tempfile
import time
from typing import Any, Dict
from unittest.mock import ANY, MagicMock, patch

from psutil import Popen
from rq import Queue

from chaosplt_scheduler.worker import initialize_worker


@patch("chaosplt_scheduler.worker.Popen", autospec=True)
def test_initialize_worker(popen: Popen, config: Dict[str, Any]):
    worker_config = config.get("worker")
    queue_name = worker_config.get("queue_name")
    worker_name = worker_config.get("worker_name")
    worker = initialize_worker(
        queue_name,
        worker_name,
        config
    )
    assert worker is not None
    assert worker.running is False
    assert worker.workers_count == 0

    try:
        worker.start()
        assert worker.running is True
        assert worker.workers_count == 1
        popen.assert_called_with(
            ANY, stdout=None, stderr=None, shell=False, cwd=tempfile.tempdir
        )
    finally:
        worker.stop()
        assert worker.running is False
        assert worker.workers_count == 0


@patch("chaosplt_scheduler.worker.Popen", autospec=True)
def test_failed_worker_is_replaced(popen: Popen, config: Dict[str, Any]):
    worker_config = config.get("worker")
    queue_name = worker_config.get("queue_name")
    worker_name = worker_config.get("worker_name")
    worker = initialize_worker(
        queue_name,
        worker_name,
        config
    )
    assert worker is not None
    assert worker.running is False
    assert worker.workers_count == 0

    proc1 = MagicMock()
    proc2 = MagicMock()

    popen.side_effect = [proc1, proc2]
    proc1.is_running.return_value = True
    proc2.is_running.return_value = True

    try:
        worker.start()
        assert worker.running is True
        assert worker.workers_count == 1
        popen.assert_called_with(
            ANY, stdout=None, stderr=None, shell=False, cwd=tempfile.tempdir
        )
        proc1.is_running.return_value = False
        time.sleep(0.2)
        assert worker.workers_count == 1
        assert worker._processes[0] == proc2
    finally:
        worker.stop()
        assert worker.running is False
        assert worker.workers_count == 0
