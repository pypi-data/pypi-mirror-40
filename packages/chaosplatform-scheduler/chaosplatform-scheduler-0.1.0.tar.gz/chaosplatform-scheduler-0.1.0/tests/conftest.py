import os
import sys
import tempfile
from typing import Any, Dict

from fakeredis import FakeStrictRedis
import pytest

from chaosplt_scheduler.service import Services
from chaosplt_scheduler.scheduler import create_scheduler_queue, \
    create_scheduler, start_scheduler, stop_scheduler, ChaosPlatformScheduler


sys.path.insert(
    0, os.path.join(
        os.path.dirname(__file__)))


@pytest.fixture
def config() -> Dict[str, Any]:
    return {
        "debug": False,
        "grpc": {
            "address": "127.0.0.1:50980"
        },
        "redis": {
            "host": "127.0.0.1",
            "port": 6379,
            "queue": "chaosplatform"
        },
        "worker": {
            "debug": False,
            "queue_name": "fakequeue",
            "worker_name": "worker-test",
            "worker_directory": tempfile.tempdir,
            "add_random_suffix_to_worker_name": True,
            "supervising_interval": 0.1,
            "redis": {
                "host": "127.0.0.1",
                "port": 6379
            }
        }
    }


@pytest.fixture
def scheduler(config: Dict[str, Any]) -> ChaosPlatformScheduler:
    queue = create_scheduler_queue(
        "myqueue", FakeStrictRedis(singleton=False), is_async=False)
    sched = create_scheduler(queue, config)
    sched.interval = 1
    return sched


@pytest.fixture
def services() -> Services:
    return Services()
