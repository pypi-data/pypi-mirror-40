# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
from typing import Any, Dict

from flask import Blueprint, Flask, request, after_this_request, Response
from flask_caching import Cache

from chaosplt_auth.auth import setup_login
from chaosplt_auth.service import Services
from chaosplt_auth.storage import AuthStorage

from .backend import setup_oauth_provider
from .oauth2 import view as oauth2_view, github_view

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

    # OAUTH2
    oauth2_config = config["oauth2"]
    for backend in oauth2_config:
        provider = backend.upper()
        provider_config = oauth2_config[backend]

        app.config["_OAUTH_CLIENT_ID".format(provider)] = \
            provider_config["client_id"]
        app.config["_OAUTH_CLIENT_SECRET".format(provider)] = \
            provider_config["client_secret"]

    setup_login(app, from_session=True)

    return app


def cleanup_app(app: Flask):
    pass


def serve_app(app: Flask, cache: Cache, services: Services,
              storage: AuthStorage, config: Dict[str, Any],
              mount_point: str = '/oauth2', log_handler: StreamHandler = None):
    register_views(app, cache, services, storage)


###############################################################################
# Internals
###############################################################################
def register_views(app: Flask, cache: Cache, services, storage: AuthStorage):
    patch_request(oauth2_view, services, storage)
    patch_request(github_view, services, storage)

    app.register_blueprint(github_view, url_prefix="/auth/oauth2/via")
    app.register_blueprint(oauth2_view, url_prefix="/auth/oauth2")

    setup_oauth_provider(github_view, services, storage, cache)


def patch_request(bp: Blueprint, services, storage: AuthStorage):
    @bp.before_request
    def prepare_request():
        request.services = services
        request.storage = storage

        @after_this_request
        def clean_request(response: Response):
            request.services = None
            request.storage = None
            return response
