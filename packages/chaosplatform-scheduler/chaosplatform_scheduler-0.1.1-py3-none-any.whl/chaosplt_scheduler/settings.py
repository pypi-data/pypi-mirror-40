# -*- coding: utf-8 -*-
import glob
import os

import cherrypy
from dotenv import load_dotenv

__all__ = ["load_settings"]


def load_settings(env_path: str):
    """
    Load settings from the environment:

    * if `env_path` is a file, read it
    * if `env_path` is a directory, load, all its `*.env` files
    """
    if os.path.isdir(env_path):
        pattern = os.path.join(env_path, '**', '.env')
        for env_file in glob.iglob(pattern, recursive=True):
            load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv(dotenv_path=env_path)

    debug = True if os.getenv('CHAOSPLATFORM_DEBUG') else False
    cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)
    cherrypy.config.update({
        'engine.autoreload.on': False,
        'log.screen': debug,
        'log.access_file': '',
        'log.error_file': '',
        'environment': '' if debug else 'production'
    })

    config = {
        "debug": debug,
        "grpc": {
            "address": os.getenv("GRPC_LISTEN_ADDR"),
        },
        "queue_name": os.getenv("QUEUE_NAME"),
        "worker_name": os.getenv("WORKER_NAME"),
        "add_random_suffix_to_worker_name": True,
        "redis": {
            "host": os.getenv("REDIS_HOST", "127.0.0.1"),
            "port": os.getenv("REDIS_PORT", 6379)
        },
        "job": {
            "platform_url": os.getenv("PLATFORM_URL")
        }
    }

    return config
