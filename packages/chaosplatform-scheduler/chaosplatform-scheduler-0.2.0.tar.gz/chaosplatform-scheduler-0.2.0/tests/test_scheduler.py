import time
from typing import Any, Dict

from fakeredis import FakeStrictRedis

from chaosplt_scheduler.scheduler import create_scheduler_queue, \
    create_scheduler, start_scheduler, stop_scheduler

from fixtures.jobs import count_words


def test_create_scheduler_queue():
    queue = create_scheduler_queue(
        "myqueue", FakeStrictRedis(), is_async=False)
    assert queue is not None


def test_create_scheduler(config: Dict[str, Any]):
    queue = create_scheduler_queue(
        "myqueue", FakeStrictRedis(), is_async=False)
    sched = create_scheduler(queue, config)
    assert sched is not None

    job = queue.enqueue(count_words, "hello world")
    assert job.is_finished
    assert job.result == 2


def test_running_scheduler(config: Dict[str, Any]):
    queue = create_scheduler_queue(
        "myqueue", FakeStrictRedis(), is_async=False)
    sched = create_scheduler(queue, config)
    sched.interval = 1
    assert sched.running == False

    start_scheduler(sched)
    time.sleep(0.3)
    assert sched.running == True

    stop_scheduler(sched)
    time.sleep(0.3)
    assert sched.running == False
