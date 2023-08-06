#!/usr/bin/env python
import sys

import click
from redis import Redis
from redis.exceptions import ConnectionError
from rq import Queue, Worker
from rq.cli.helpers import setup_loghandlers_from_args
from rq.contrib.legacy import cleanup_ghosts
from rq.job import Job

from . import __version__


@click.group()
@click.version_option(version=__version__)
def runner():
    pass


@runner.command()
@click.option('--name', help='Worker name.', required=True)
@click.option('--queue', help='Queue name.', required=True)
@click.option('--verbose', is_flag=True, help='Enable more traces.')
@click.option('--connection-host', help='Connection host', default='localhost',
              show_default=True)
@click.option('--connection-port', help='Connection port', default=6379,
              show_default=True, type=int)
@click.option('--connection-password', help='Connection password')
@click.option('--connection-db', help='Connection database to use', default=0,
              show_default=True)
@click.option('--connection-over-tls', is_flag=True,
              help='Connection over TLS')
def run(name: str, queue: str, connection_host: str,
        connection_port: int = 6379, connection_password: str = None,
        connection_over_tls: bool = False, connection_db: int = 0,
        verbose: bool = False):
    date_format = "%Y-%m-%dT%H:%M:%S"
    log_format = "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s"
    setup_loghandlers_from_args(verbose, False, date_format, log_format)

    params = {
        "ssl": connection_over_tls,
        "password": connection_password,
        "host": connection_host,
        "port": connection_port,
        "db": connection_db
    }

    try:
        c = Redis(**params)
        cleanup_ghosts(c)
        worker = Worker(
            [queue],
            name=name,
            connection=c,
            default_worker_ttl=420,
            default_result_ttl=500,
            job_monitoring_interval=30,
            job_class=Job,
            queue_class=Queue,
            exception_handlers=None
        )

        worker.work(
            burst=False, logging_level="DEBUG" if verbose else "INFO",
            date_format=date_format, log_format=log_format)
    except ConnectionError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    run()
