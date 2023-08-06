import logging
from typing import Any, Dict, NoReturn

import attr
from dateparser import parse

from .runner import run as run_toolkit
from .scheduler import initialize_scheduler_queue, start_scheduler, \
    stop_scheduler, ChaosPlatformScheduler
from .worker import ChaosPlatformWorker, initialize_worker, start_worker, \
    stop_worker

__all__ = ["SchedulerService", "initialize_services", "shutdown_services"]
logger = logging.getLogger("chaosplatform")


@attr.s
class Services:
    scheduler: ChaosPlatformScheduler = attr.ib(default=None)
    worker: ChaosPlatformWorker = attr.ib(default=None)


class SchedulerService:
    def __init__(self, scheduler: ChaosPlatformScheduler,
                 config: Dict[str, Any]):
        self.scheduler = scheduler
        self.job_config = config.get("job")

    def release(self):
        self.scheduler = None
        self.job_config = None

    def schedule(self, schedule_id: str, user_id: str, org_id: str,
                 workspace_id: str, experiment_id: str, token_id: str,
                 token: str, scheduled: str, experiment: str, interval: int,
                 repeat: int, cron: str, settings: str, configuration: str,
                 secrets: str, timezone: str = 'UTC') -> str:
        """
        Queue a job for execution

        Various scenarios can happen:

        * When `cron` is set to a Cron string, the job will be queued to
          run periodically.
        * When `interval` is set to an integer, the job is queued to run
          periodically
        * Otherwise, the job is scheduled to run once

        However, when `repeat` is also set, the job is ran only that number of
        times, when `cron` or `interval` were also set.

        The job is first queued when `scheduled` is reached. It must be a
        datestring in the given `timezone`, which defaults to `"UTC"`.

        The method returns the job identifier provided by the underlying
        scheduler.
        """
        # None means infinity
        repeat = repeat or None
        scheduled = parse(scheduled, settings={'TO_TIMEZONE': timezone})
        platform_url = self.job_config["platform_url"]
        if cron:
            job = self.scheduler.cron(
                cron,
                func=run_toolkit,
                args=[
                    schedule_id, user_id, org_id,
                    workspace_id, experiment_id, token_id, token,
                    experiment, platform_url, settings, configuration, secrets
                ],
                repeat=repeat
            )
        elif interval:
            job = self.scheduler.schedule(
                scheduled,
                func=run_toolkit,
                args=[
                    schedule_id, user_id, org_id,
                    workspace_id, experiment_id, token_id, token,
                    experiment, platform_url, settings, configuration, secrets
                ],
                interval=interval,
                repeat=repeat
            )
        else:
            job = self.scheduler.enqueue_at(
                scheduled,
                run_toolkit,
                schedule_id, user_id, org_id, workspace_id, experiment_id,
                token_id, token, experiment, platform_url, settings,
                configuration, secrets
            )
        logger.info("Scheduled job {} at '{}Z'".format(
            job.id, scheduled.isoformat()))
        return job.id

    def cancel(self, job_id: str) -> NoReturn:
        """
        Cancel a job.

        If the job never started, it is cancelled beforehand. Or its next
        iteration, if one was planned.
        """
        logger.info("Cancel job {}".format(job_id))
        self.scheduler.cancel(job_id)


def initialize_services(services: Services, config: Dict[str, Any]):
    """
    Initialize the scheduler and worker resources
    """
    if not services.scheduler:
        scheduler = initialize_scheduler_queue(config)
        start_scheduler(scheduler)
        services.scheduler = SchedulerService(scheduler, config)

    if not services.worker:
        worker_config = config["worker"]
        services.worker = initialize_worker(
            worker_config["queue_name"], worker_config["worker_name"], config)
        start_worker(services.worker)


def shutdown_services(services: Services):
    """
    Shutdown the scheduler and worker services, releasing their resources
    """
    if services.scheduler:
        sched = services.scheduler.scheduler
        stop_scheduler(sched)
        services.scheduler.release()
    if services.worker:
        stop_worker(services.worker)
