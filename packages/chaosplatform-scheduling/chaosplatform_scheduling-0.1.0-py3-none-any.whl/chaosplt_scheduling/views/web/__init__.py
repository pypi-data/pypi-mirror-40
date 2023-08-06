# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
import os
from typing import Any, Dict

from flask import Blueprint, Flask, request, after_this_request, Response
from flask_caching import Cache

from chaosplt_scheduling.service import Services
from chaosplt_scheduling.storage import SchedulingStorage

__all__ = ["create_app", "cleanup_app", "serve_app"]


def create_app(config: Dict[str, Any]) -> Flask:
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.debug = True if os.getenv('CHAOSPLATFORM_DEBUG') else False

    logger = logging.getLogger('flask.app')
    logger.propagate = False

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.secret_key = app.config["SECRET_KEY"]

    app.config["GRPC_LISTEN_ADDR"] = os.getenv("GRPC_LISTEN_ADDR")

    app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        app.config["CACHE_REDIS_HOST"] = os.getenv("CACHE_REDIS_HOST")
        app.config["CACHE_REDIS_PORT"] = os.getenv("CACHE_REDIS_PORT", 6379)

    return app


def cleanup_app(app: Flask):
    pass


def serve_app(app: Flask, cache: Cache, services: Services,
              storage: SchedulingStorage, config: Dict[str, Any],
              mount_point: str = '/scheduling',
              log_handler: StreamHandler = None):
    register_views(app, cache, services, storage)


###############################################################################
# Internals
###############################################################################
def register_views(app: Flask, cache: Cache, services,
                   storage: SchedulingStorage):
    pass


def patch_request(bp: Blueprint, services, storage: SchedulingStorage):
    """
    Configure each request by attaching the services and storage
    and detach both once when the request is finished
    """
    @bp.before_request
    def prepare_request():
        request.services = services
        request.storage = storage

        @after_this_request
        def clean_request(response: Response):
            request.services = None
            request.storage = None
            return response
