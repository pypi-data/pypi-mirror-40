# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
from typing import Any, Dict

from flask import Blueprint, Flask, request, after_this_request, Response
from flask_caching import Cache

from chaosplt_scheduling.service import Services
from chaosplt_scheduling.storage import SchedulingStorage

__all__ = ["create_app", "cleanup_app", "serve_app"]


def create_app(config: Dict[str, Any]) -> Flask:
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.debug = config.get("debug", False)

    logger = logging.getLogger('flask.app')
    logger.propagate = False

    app.config["SECRET_KEY"] = config["http"]["secret_key"]
    app.secret_key = config["http"]["secret_key"]
    app.config["JWT_SECRET_KEY"] = config["jwt"]["secret_key"]
    app.config["SQLALCHEMY_DATABASE_URI"] = config["db"]["uri"]

    app.config["CACHE_TYPE"] = config["cache"].get("type", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        redis_config = config["cache"]["redis"]
        app.config["CACHE_REDIS_HOST"] = redis_config.get("host")
        app.config["CACHE_REDIS_PORT"] = redis_config.get("port", 6379)
        app.config["CACHE_REDIS_DB"] = redis_config.get("db", 0)
        app.config["CACHE_REDIS_PASSWORD"] = redis_config.get("password")

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
