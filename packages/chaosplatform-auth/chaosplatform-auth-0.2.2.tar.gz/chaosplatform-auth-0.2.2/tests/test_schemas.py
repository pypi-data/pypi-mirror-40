from collections import OrderedDict
from typing import Dict
from uuid import UUID

from chaosplt_auth.model import AccessToken
from chaosplt_auth.schemas import AccessTokenSchema, NewAccessTokenSchema, \
    token_schema, new_token_schema
from flask import Flask


def test_parse_access_token_request(access_token_request: Dict[str, str]):
    token = new_token_schema.load(access_token_request)
    assert token == access_token_request


def test_access_token_schema_serialization(api: Flask, user_id: UUID,
                                           access_token_id: UUID):
    info = dict(
        id=str(access_token_id),
        name="my token",
        user_id=user_id,
        access_token="access-123456",
        refresh_token="refresh-123456",
    )
    token = AccessToken(**info)

    expected_info = OrderedDict(
        id=str(access_token_id),
        user_id=str(user_id),
        name="my token",
        access_token="access-123456",
        refresh_token="refresh-123456",
        url='http://localhost/api/v1/auth/tokens/{}'.format(access_token_id),
        links={
            'self': '/api/v1/auth/tokens/{}'.format(access_token_id),
        }
    )

    with api.test_request_context():
        token = token_schema.dump(token)
        assert token == expected_info


def test_parse_access_token(api: Flask, user_id: UUID,
                            access_token_id: UUID):
    info = dict(
        name="my token",
        id=access_token_id,
        user_id=user_id,
        access_token="access-123456",
        refresh_token="refresh-123456",
    )

    with api.test_request_context():
        token = token_schema.load(info)
        assert token == AccessToken(**info)
