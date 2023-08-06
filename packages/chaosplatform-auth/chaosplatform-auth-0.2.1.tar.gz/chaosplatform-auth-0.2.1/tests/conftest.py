import logging
from logging import StreamHandler
import os
import random
import string
from typing import Any, Dict
from unittest.mock import MagicMock
import uuid
from uuid import UUID

import cherrypy
from flask import Flask, request
from flask_caching import Cache
from flask_login import login_required, login_user, logout_user

import pytest

from chaosplt_auth.cache import setup_cache
from chaosplt_auth.log import http_requests_logger
from chaosplt_auth.views.api import create_api, cleanup_api, serve_api, \
    register_api
from chaosplt_auth.views.web.backend import OAuthBackend
from chaosplt_auth.views.web import create_app, cleanup_app, serve_app, \
    register_views
from chaosplt_auth.model import User
from chaosplt_relational_storage.db import RelationalStorage
from chaosplt_auth.service import Services, initialize_services
from chaosplt_auth.settings import load_settings
from chaosplt_auth.storage import initialize_storage, AuthStorage
from flask_jwt_extended import create_access_token, create_refresh_token

cur_dir = os.path.abspath(os.path.dirname(__file__))
fixtures_dir = os.path.join(cur_dir, "fixtures")
env_path = os.path.join(fixtures_dir, '.env')


@pytest.fixture
def config():
    return load_settings(env_path)


@pytest.fixture
def storage(config: Dict[str, Any]) -> AuthStorage:
    return initialize_storage(config)


@pytest.fixture
def stream_handler() -> StreamHandler:
    return StreamHandler()


@pytest.fixture
def account_service():
    return MagicMock()


@pytest.fixture
def services(config: Dict[str, Any], account_service) -> Services:
    svc = Services()
    svc.account = account_service
    initialize_services(svc, config)
    return svc


@pytest.fixture
def app(config: Dict[str, Any], services: Services, storage: AuthStorage,
        stream_handler: StreamHandler) -> Flask:
    application = create_app(config)
    cache = setup_cache(application)
    serve_app(
        application, cache, services, storage, config, "/auth",
        log_handler=stream_handler)
    return application


@pytest.fixture
def api(app: Flask, config: Dict[str, Any], services: Services,
        storage: AuthStorage, stream_handler: StreamHandler) -> Flask:
    application = create_api(config)
    cache = setup_cache(application)
    wsgiapp = http_requests_logger(application, stream_handler)
    cherrypy.tree.graft(wsgiapp, "/api/v1")
    serve_api(
        application, cache, services, storage, config, "/api/v1/auth",
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
def username() -> str:
    return "jane"


@pytest.fixture
def name() -> str:
    return "jane martin"


@pytest.fixture
def email() -> str:
    return "jane@world.com"


@pytest.fixture
def user(user_id: UUID, username: str, name: str, email: str):
    return User(user_id, username, name, email, True, True, False)


@pytest.fixture
def access_token_id() -> UUID:
    return UUID("86693512-82e9-4dec-8d54-53c312272300")


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
def access_token_name() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def access_token_request(user_id: UUID,
                         access_token_name: str) -> Dict[str, str]:
    return {
        "name": access_token_name,
        "user_id": str(user_id),
        "scopes": "read"
    }


@pytest.fixture
def request_token(app: Flask, api: Flask, user_id: UUID) -> str:
    with api.app_context():
        return create_access_token(str(user_id))


@pytest.fixture
def oauth_backend(services: Services, storage: AuthStorage, app_cache: Cache):
    return OAuthBackend(services, storage, app_cache)
