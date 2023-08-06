import logging

from chaoslib.experiment import run_experiment
from chaoslib.types import Journal
import requests
import simplejson as json

__all__ = ["run"]
logger = logging.getLogger("chaosplatform")


def run(schedule_id: str, user_id: str, org_id: str, workspace_id: str,
        experiment_id: str, token_id: str, token: str, experiment: str,
        platform_url: str, settings: str = None, configuration: str = None,
        secrets: str = None) -> Journal:
    """
    Execute an experiment and return its journal

    See also:
    https://docs.chaostoolkit.org/reference/api/journal/
    """
    settings = json.loads(settings) if settings else {}
    experiment = json.loads(experiment)

    if configuration:
        if not isinstance(configuration, dict):
            configuration = json.loads(configuration)
        experiment.setdefault("configuration", {})
        experiment["configuration"].update(configuration)

    if secrets:
        if not isinstance(secrets, dict):
            secrets = json.loads(secrets)
        experiment.setdefault("secrets", {})
        experiment["secrets"].update(secrets)

    try:
        journal = run_experiment(experiment)
    except Exception as x:
        logger.error(
            "Running experiment failed due to {}".format(str(x)),
            exc_info=True
        )
    else:
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(token),
            "Connection": "close"
        }
        r = requests.post(
            "{}/api/v1/executions".format(platform_url), json={
                "experiment_id": experiment_id,
                "journal": journal
            }, headers=headers)

        if r.status_code > 399:
            logger.error(
                "Failed to push journal results for experiment {}: {}".format(
                    experiment_id, r.text
                ))

        return journal
