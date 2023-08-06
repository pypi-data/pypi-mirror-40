# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
import os
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
    app.debug = True if os.getenv('CHAOSPLATFORM_DEBUG') else False

    logger = logging.getLogger('flask.app')
    logger.propagate = False

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.secret_key = app.config["SECRET_KEY"]

    app.config["GRPC_ADDR"] = "{}:{}".format(
        os.getenv("GRPC_LISTEN_ADDR"), os.getenv("GRPC_LISTEN_PORT"))

    app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        app.config["CACHE_REDIS_HOST"] = os.getenv("CACHE_REDIS_HOST")
        app.config["CACHE_REDIS_PORT"] = os.getenv("CACHE_REDIS_PORT", 6379)

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
