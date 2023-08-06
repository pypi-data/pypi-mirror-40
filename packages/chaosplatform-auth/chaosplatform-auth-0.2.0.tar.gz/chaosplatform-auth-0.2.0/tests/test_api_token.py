from typing import Dict
import uuid
from uuid import UUID

import cherrypy
from flask import Flask
from werkzeug.test import Client

from chaosplt_auth.model import AccessToken, User
from chaosplt_auth.schemas import AccessTokenSchema, NewAccessTokenSchema, \
    token_schema, new_token_schema


def test_new_invalid_request_payload(api: Flask, api_client: Client,
                                     access_token_request: Dict[str, str],
                                     request_token: str):
    r = api_client.post(
        "/api/v1/auth/tokens",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(request_token),
            "Content-Type": "application/json"
        },
        json={}
    )
    assert r.status_code == 422

    msg = r.json
    assert "name" in msg
    assert "user_id" in msg


def test_new_valid_request_payload(api: Flask, api_client: Client,
                                   access_token_request: Dict[str, str],
                                   request_token: str, account_service,
                                   user: User):
    account_service.registration.get.return_value = user
    r = api_client.post(
        "/api/v1/auth/tokens",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        },
        json=access_token_request
    )
    assert r.status_code == 201


def test_cannot_create_for_other_user(api: Flask, api_client: Client,
                                   access_token_request: Dict[str, str],
                                   request_token: str, account_service,
                                   user: User):
    account_service.registration.get.return_value = user
    
    data = access_token_request.copy()
    data["user_id"] = str(uuid.uuid4())

    r = api_client.post(
        "/api/v1/auth/tokens",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        },
        json=data
    )
    assert r.status_code == 422
    assert r.json["message"] == "Cannot create a token for another user"


def test_get_access_token(api: Flask, api_client: Client,
                          access_token_request: Dict[str, str],
                          request_token: str, account_service,
                          user: User):
    account_service.registration.get.return_value = user
    r = api_client.post(
        "/api/v1/auth/tokens",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        },
        json=access_token_request
    )
    assert r.status_code == 201
    token = r.json

    r = api_client.get(
        "/api/v1/auth/tokens/{}".format(token["id"]),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        }
    )
    assert r.status_code == 200


def test_delete_access_token(api: Flask, api_client: Client,
                          access_token_request: Dict[str, str],
                          request_token: str, account_service,
                          user: User):
    account_service.registration.get.return_value = user
    r = api_client.post(
        "/api/v1/auth/tokens",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        },
        json=access_token_request
    )
    assert r.status_code == 201
    token = r.json

    r = api_client.get(
        "/api/v1/auth/tokens/{}".format(token["id"]),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        }
    )
    assert r.status_code == 200

    r = api_client.delete(
        "/api/v1/auth/tokens/{}".format(token["id"]),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        }
    )
    assert r.status_code == 204

    r = api_client.get(
        "/api/v1/auth/tokens/{}".format(token["id"]),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(request_token),
        }
    )
    assert r.status_code == 404
