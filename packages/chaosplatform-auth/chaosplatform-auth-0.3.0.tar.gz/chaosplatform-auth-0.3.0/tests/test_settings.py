import os.path

import cherrypy
from flask import Flask

from chaosplt_auth.settings import load_settings

cur_dir = os.path.abspath(os.path.dirname(__file__))
fixtures_dir = os.path.join(cur_dir, "fixtures")
config_path = os.path.join(fixtures_dir, 'config.toml')


def test_load_single_dot_env():
    config = load_settings(config_path)
    assert config.get('debug') == True


def test_configuring_app(app: Flask):
    assert app.config["SECRET_KEY"] == "whatever"
    assert app.secret_key == "whatever"
    assert app.config["JWT_SECRET_KEY"] == "jwt_whatever"
    assert app.config["CACHE_TYPE"] == "simple"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"