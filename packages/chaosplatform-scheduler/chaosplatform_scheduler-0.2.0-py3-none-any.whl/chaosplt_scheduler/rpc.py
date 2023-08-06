import logging
from typing import Any, Dict

from chaosplt_grpc.scheduler.server import \
    SchedulerService as GRPCSchedulerService

from .service import SchedulerService
from .scheduler import ChaosPlatformScheduler

__all__ = ["SchedulerRPC"]
logger = logging.getLogger("chaosplatform")


class SchedulerRPC(SchedulerService, GRPCSchedulerService):
    def __init__(self, scheduler: ChaosPlatformScheduler,
                 config: Dict[str, Any]):
        SchedulerService.__init__(self, scheduler, config)
        GRPCSchedulerService.__init__(self)
