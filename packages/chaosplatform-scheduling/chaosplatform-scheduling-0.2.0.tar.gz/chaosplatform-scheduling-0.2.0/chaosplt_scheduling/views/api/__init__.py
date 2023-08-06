# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
from typing import Any, Dict

from flask import Blueprint, Flask, after_this_request, request, Response
from flask_caching import Cache

from chaosplt_scheduling.auth import setup_jwt, setup_login
from chaosplt_scheduling.schemas import setup_schemas
from chaosplt_scheduling.service import Services
from chaosplt_scheduling.storage import SchedulingStorage

from .scheduling import api as scheduling_api

__all__ = ["create_api", "cleanup_api", "register_api"]


def create_api(config: Dict[str, Any]) -> Flask:
    """
    Create the API application for the scheduling API endpoint.
    """
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

    setup_jwt(app)
    setup_schemas(app)
    setup_login(app, from_jwt=True)

    return app


def cleanup_api(app: Flask):
    pass


def serve_api(app: Flask, cache: Cache, services: Services,
              storage: SchedulingStorage, config: Dict[str, Any],
              mount_point: str = '/api/v1/scheduling',
              log_handler: StreamHandler = None):
    """
    Serve the scheduling API application over HTTP.
    """
    register_api(app, cache, services, storage, mount_point)


###############################################################################
# Internals
###############################################################################
def register_api(app: Flask, cache: Cache, services: Services,
                 storage: SchedulingStorage, mount_point: str):
    patch_request(scheduling_api, services, storage)
    app.register_blueprint(scheduling_api, url_prefix=mount_point)


def patch_request(bp: Blueprint, services, storage: SchedulingStorage):
    @bp.before_request
    def prepare_request():
        request.services = services
        request.storage = storage

        @after_this_request
        def clean_request(response: Response):
            request.services = None
            request.storage = None
            return response
