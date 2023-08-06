from datetime import datetime, timedelta
from unittest.mock import MagicMock, ANY

from dateparser import parse

from chaosplt_scheduler.rpc import SchedulerRPC


def test_schedule_experiment_execution_at():
    scheduler = MagicMock()
    job = MagicMock()
    job.id = "myjob"
    scheduler.enqueue_at.return_value = job

    dt = (datetime.utcnow() + timedelta(seconds=1)).isoformat()
    scheduled = parse(dt, settings={'TO_TIMEZONE': 'UTC'})

    rpc = SchedulerRPC(scheduler, {"job": {"platform_url": "http://a:80"}})
    job_id = rpc.schedule(
        schedule_id="1",
        user_id="2",
        org_id="3",
        workspace_id="4",
        experiment_id="5",
        token_id="6",
        token="7",
        scheduled=dt,
        experiment="8",
        interval=None,
        repeat=None,
        cron=None,
        settings=None,
        configuration=None,
        secrets=None)
    scheduler.enqueue_at.assert_called_with(
        scheduled, ANY, "1", "2", "3", "4", "5", "6", "7", "8", 
        "http://a:80", None, None, None
    )
    assert job_id == "myjob"


def test_schedule_experiment_execution_cron_no_repeat():
    scheduler = MagicMock()
    job = MagicMock()
    job.id = "myjob"
    scheduler.cron.return_value = job

    dt = (datetime.utcnow() + timedelta(seconds=1)).isoformat()

    rpc = SchedulerRPC(scheduler, {"job": {"platform_url": "http://a:80"}})
    job_id = rpc.schedule(
        schedule_id="1",
        user_id="2",
        org_id="3",
        workspace_id="4",
        experiment_id="5",
        token_id="6",
        token="7",
        scheduled=dt,
        experiment="8",
        interval=None,
        repeat=None,
        cron="1 * * * *",
        settings=None,
        configuration=None,
        secrets=None)
    scheduler.cron.assert_called_with(
        "1 * * * *", func=ANY,
        args=[
            "1", "2", "3", "4", "5", "6", "7", "8", "http://a:80", None, None,
            None
        ],
        repeat=None
    )


def test_schedule_experiment_execution_cron_with_repeat():
    scheduler = MagicMock()
    job = MagicMock()
    job.id = "myjob"
    scheduler.cron.return_value = job

    dt = (datetime.utcnow() + timedelta(seconds=1)).isoformat()

    rpc = SchedulerRPC(scheduler, {"job": {"platform_url": "http://a:80"}})
    job_id = rpc.schedule(
        schedule_id="1",
        user_id="2",
        org_id="3",
        workspace_id="4",
        experiment_id="5",
        token_id="6",
        token="7",
        scheduled=dt,
        experiment="8",
        interval=None,
        repeat=10,
        cron="1 * * * *",
        settings=None,
        configuration=None,
        secrets=None)
    scheduler.cron.assert_called_with(
        "1 * * * *", func=ANY,
        args=[
            "1", "2", "3", "4", "5", "6", "7", "8", "http://a:80", None, None,
            None
        ],
        repeat=10
    )


def test_schedule_experiment_execution_interval_no_repeat():
    scheduler = MagicMock()
    job = MagicMock()
    job.id = "myjob"
    scheduler.schedule.return_value = job

    dt = (datetime.utcnow() + timedelta(seconds=1)).isoformat()
    scheduled = parse(dt, settings={'TO_TIMEZONE': 'UTC'})

    rpc = SchedulerRPC(scheduler, {"job": {"platform_url": "http://a:80"}})
    job_id = rpc.schedule(
        schedule_id="1",
        user_id="2",
        org_id="3",
        workspace_id="4",
        experiment_id="5",
        token_id="6",
        token="7",
        scheduled=dt,
        experiment="8",
        interval=30,
        repeat=None,
        cron=None,
        settings=None,
        configuration=None,
        secrets=None)
    scheduler.schedule.assert_called_with(
        scheduled, func=ANY,
        args=[
            "1", "2", "3", "4", "5", "6", "7", "8", "http://a:80", None, None,
            None
        ],
        interval=30, repeat=None
    )


def test_schedule_experiment_execution_interval_no_repeat():
    scheduler = MagicMock()
    job = MagicMock()
    job.id = "myjob"
    scheduler.schedule.return_value = job

    dt = (datetime.utcnow() + timedelta(seconds=1)).isoformat()
    scheduled = parse(dt, settings={'TO_TIMEZONE': 'UTC'})

    rpc = SchedulerRPC(scheduler, {"job": {"platform_url": "http://a:80"}})
    job_id = rpc.schedule(
        schedule_id="1",
        user_id="2",
        org_id="3",
        workspace_id="4",
        experiment_id="5",
        token_id="6",
        token="7",
        scheduled=dt,
        experiment="8",
        interval=30,
        repeat=10,
        cron=None,
        settings=None,
        configuration=None,
        secrets=None)
    scheduler.schedule.assert_called_with(
        scheduled, func=ANY,
        args=[
            "1", "2", "3", "4", "5", "6", "7", "8", "http://a:80", None, None,
            None
        ],
        interval=30, repeat=10
    )


def test_cancel_schedule():
    scheduler = MagicMock()
    job = MagicMock()
    job.id = "myjob"
    scheduler.enqueue_at.return_value = job

    dt = (datetime.utcnow() + timedelta(seconds=1)).isoformat()
    scheduled = parse(dt, settings={'TO_TIMEZONE': 'UTC'})

    rpc = SchedulerRPC(scheduler, {"job": {"platform_url": "http://a:80"}})
    job_id = rpc.schedule(
        schedule_id="1",
        user_id="2",
        org_id="3",
        workspace_id="4",
        experiment_id="5",
        token_id="6",
        token="7",
        scheduled=dt,
        experiment="8",
        interval=None,
        repeat=None,
        cron=None,
        settings=None,
        configuration=None,
        secrets=None)
    scheduler.enqueue_at.assert_called_with(
        scheduled, ANY, "1", "2", "3", "4", "5", "6", "7", "8", "http://a:80",
        None, None, None
    )
    assert job_id == "myjob"

    rpc.cancel(job_id)
    scheduler.cancel.assert_called_with(job_id)
