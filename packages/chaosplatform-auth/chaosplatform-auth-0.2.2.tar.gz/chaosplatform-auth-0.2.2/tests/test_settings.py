import os.path

import cherrypy
from flask import Flask

from chaosplt_auth.settings import load_settings

cur_dir = os.path.abspath(os.path.dirname(__file__))
fixtures_dir = os.path.join(cur_dir, "fixtures")
env_path = os.path.join(fixtures_dir, '.env')


def test_load_single_dot_env():
    config = load_settings(env_path)
    assert config.get('debug') == True


def test_load_from_directory():
    config = load_settings(fixtures_dir)
    assert config.get('debug') == True
    assert cherrypy.server.socket_port == 8080


def test_configuring_app(app: Flask):
    assert app.config["SECRET_KEY"] == "whatever"
    assert app.secret_key == "whatever"
    assert app.config["JWT_SECRET_KEY"] == "jwt_whatever"
    assert app.config["GRPC_LISTEN_ADDR"] == "127.0.0.1:50051"
    assert app.config["CACHE_TYPE"] == "simple"
