from datetime import datetime
import os
import random
import string
from typing import Any, Dict
from unittest.mock import MagicMock
import uuid
from uuid import UUID

import cherrypy
from flask import  Flask, request
from flask_caching import Cache
from flask_login import login_required, login_user, logout_user
import logging
from logging import StreamHandler
import pytest
from sqlalchemy.sql import text as sa_text

from chaosplt_relational_storage.db import RelationalStorage
from chaosplt_scheduling.cache import setup_cache
from chaosplt_scheduling.log import http_requests_logger
from chaosplt_scheduling.views.api import create_api, cleanup_api, serve_api, \
    register_api
from chaosplt_scheduling.views.web import create_app, cleanup_app, serve_app, \
    register_views
from chaosplt_scheduling.service import Services, initialize_services
from chaosplt_scheduling.settings import load_settings
from chaosplt_scheduling.storage import initialize_storage, shutdown_storage, \
    SchedulingStorage

cur_dir = os.path.abspath(os.path.dirname(__file__))
fixtures_dir = os.path.join(cur_dir, "fixtures")
config_path = os.path.join(fixtures_dir, 'config.toml')


@pytest.fixture
def config():
    return load_settings(config_path)


@pytest.fixture(autouse=True)
def storage(config: Dict[str, Any]) -> SchedulingStorage:
    s = initialize_storage(config)
    yield s
    # clear out the table from all data
    # dropping seems to cause issues
    s.driver.engine.execute(
        sa_text("DELETE FROM schedule;").execution_options(
            autocommit=True))


@pytest.fixture
def stream_handler() -> StreamHandler:
    return StreamHandler()


@pytest.fixture
def scheduler_service():
    return MagicMock()


@pytest.fixture
def services(config: Dict[str, Any], scheduler_service) -> Services:
    svc = Services()
    svc.scheduler = scheduler_service
    initialize_services(svc, config)
    return svc


@pytest.fixture
def app(config: Dict[str, Any], services: Services, storage: SchedulingStorage,
        stream_handler: StreamHandler) -> Flask:
    application = create_app(config)
    cache = setup_cache(application)
    serve_app(
        application, cache, services, storage, config, "/scheduling",
        log_handler=stream_handler)
    return application


@pytest.fixture
def api(app: Flask, config: Dict[str, Any], services: Services,
        storage: SchedulingStorage, stream_handler: StreamHandler) -> Flask:
    application = create_api(config)
    cache = setup_cache(application)
    wsgiapp = http_requests_logger(application, stream_handler)
    cherrypy.tree.graft(wsgiapp, "/api/v1")
    serve_api(
        application, cache, services, storage, config, "/api/v1/scheduling",
        log_handler=stream_handler)
    return application


@pytest.fixture
def app_cache(app: Flask) -> Cache:
    return Cache(app, config=app.config)


@pytest.fixture
def api_cache(api: Flask) -> Cache:
    return Cache(api, config=api.config)


@pytest.fixture
def user_id() -> UUID:
    return uuid.uuid4() #UUID("1d77476b-f11d-433b-b7ee-bcbf25862051")


@pytest.fixture
def org_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def workspace_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def experiment_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def token_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def scheduled() -> str:
    return "{}Z".format(datetime.utcnow().isoformat())


@pytest.fixture
def app_client(app: Flask, services: Services, username: str, name: str,
               email: str):
    app.config['TESTING'] = True
    app.testing = True

    with app.test_request_context():
        user = services.account.registration.create(
            username, name, email)
        login_user(user, remember=True)
        services.account.registration.get(user_id)

    with app.test_client() as client:
        yield client


@pytest.fixture
def api_client(api: Flask, services: Services, username: str, name: str,
               email: str):
    api.config['TESTING'] = True
    api.testing = True

    with api.test_request_context():
        user = services.account.registration.create(
            username, name, email)
        login_user(user, remember=True)
        services.account.registration.get(user_id)

    with api.test_client() as client:
        yield client


@pytest.fixture
def scheduling(org_id: UUID, workspace_id: UUID, experiment_id: UUID,
               token_id: UUID, scheduled: str) -> Dict[str, str]:
    return {
        "org": str(org_id),
        "workspace": str(workspace_id),
        "experiment": str(experiment_id),
        "token": str(token_id),
        "scheduled": scheduled
    }
