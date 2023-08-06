import logging
import logging.config
import pkgutil
from typing import Any, Dict

import simplejson as json

__all__ = ["clean_logger", "configure_logger"]
logger = logging.getLogger("chaosplatform")


def configure_logger(log_conf_path: str, config: Dict[str, Any]):
    if log_conf_path:
        with open(log_conf_path) as f:
            log_conf = json.load(f)
    else:
        log_conf = json.loads(
            pkgutil.get_data('chaosplt_scheduler', 'logging.json'))
    logging.config.dictConfig(log_conf)
    if config["debug"]:
        [h.setLevel(logging.DEBUG) for h in logger.handlers]
        logger.setLevel(logging.DEBUG)
    logger.debug("Logger configured")


def clean_logger():
    """
    Clean all handlers attached to the logger
    """
    for h in logger.handlers[:]:
        logger.removeHandler(h)
