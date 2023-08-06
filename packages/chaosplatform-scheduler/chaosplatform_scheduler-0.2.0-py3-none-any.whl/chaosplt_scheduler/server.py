import logging
from typing import Any, Dict, Tuple

from chaosplt_grpc import create_grpc_server, start_grpc_server, \
    stop_grpc_server
from chaosplt_grpc.scheduler.server import register_scheduler_service
import cherrypy
from grpc import Server

from .rpc import SchedulerRPC
from .scheduler import ChaosPlatformScheduler
from .service import Services, initialize_services, shutdown_services

__all__ = ["initialize_all", "release_all", "run_forever"]
logger = logging.getLogger("chaosplatform")


def initialize_all(config: Dict[str, Any], services: Services = None,
                   grpc_server: Server = None) -> Tuple[Services, Server]:
    """
    Initialize all resources for the service:

    * The gRPC application
    * The scheduler thread
    """
    logger.info("Initializing scheduler service resources")
    if not services:
        services = Services()

    initialize_services(services, config)
    grpc_server = initialize_grpc(
        services.scheduler.scheduler, config, grpc_server)

    return (services, grpc_server)


def release_all(services: Services, grpc_server: Server):
    """
    Release all resources
    """
    logger.info("Releasing scheduler service resources")
    if grpc_server:
        logger.info("gRPC server stopping")
        stop_grpc_server(grpc_server)
        logger.info("gRPC server stopped")
    shutdown_services(services)


def run_forever(config: Dict[str, Any]):
    """
    Run and block until a signal is sent to the process.

    The application, services or gRPC server are all created and initialized
    when the application starts.
    """
    def run_stuff(config: Dict[str, Any]):
        resources = initialize_all(config)
        cherrypy.engine.subscribe(
            'stop', lambda: release_all(*resources),
            priority=20)

    cherrypy.engine.subscribe(
        'start', lambda: run_stuff(config), priority=60)

    cherrypy.server.unsubscribe()
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()


###############################################################################
# Internals
###############################################################################
def initialize_grpc(scheduler: ChaosPlatformScheduler, config: Dict[str, Any],
                    grpc_server: Server = None) -> Server:
    """
    Initialize the gRPC server

    Create the server if not provided. This called by `initialize_all`.
    """
    if not grpc_server:
        srv_addr = config.get("grpc", {}).get("address")
        if srv_addr:
            grpc_server = create_grpc_server(srv_addr)
            start_grpc_server(grpc_server)
            logger.info("gRPC server started on {}".format(srv_addr))

        register_scheduler_service(
            SchedulerRPC(scheduler, config), grpc_server)

    return grpc_server
