from typing import Any, Dict
from unittest.mock import ANY, MagicMock, patch

from chaosplt_scheduler.service import Services
from chaosplt_scheduler.server import initialize_all, release_all


@patch('chaosplt_scheduler.service.initialize_scheduler_queue', autospec=True)
@patch('chaosplt_scheduler.server.create_grpc_server', autospec=True)
def test_initialize_all(create_grpc_server, initialize_scheduler_queue,
                        config: Dict[str, Any], services: Services):

    scheduler = MagicMock()
    initialize_scheduler_queue.return_value = scheduler

    grpc_server = MagicMock()
    create_grpc_server.return_value = grpc_server

    try:
        services, grpc_s = initialize_all(config, services, None)

        assert services.scheduler is not None
        assert services.worker is not None
        assert grpc_s is not None
        assert grpc_s == grpc_server
        grpc_s.start.assert_called()
        scheduler.start.assert_called()
    finally:
        release_all(services, grpc_server)
        grpc_s.stop.assert_called_with(grace=1)
        scheduler.stop.assert_called()
