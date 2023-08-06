from typing import Any, Dict
from uuid import UUID

import jwt

from chaosplt_auth.rpc import AuthRPC
from chaosplt_auth.storage import AuthStorage


def test_create_auth_rpc_service(config: Dict[str, Any], storage: AuthStorage,
                                 user_id: UUID, name: str):
    rpc = AuthRPC(storage, config)
    token = rpc.create_access_token(user_id, name)

    assert token.name == name
    assert token.user_id == str(user_id)
    assert token.id is not None
    assert token.access_token is not None
    assert token.refresh_token is not None

    access_token_claim = jwt.decode(
        token.access_token, config["jwt"]["secret_key"],
        algorithms=[config["jwt"]["algorithm"]])
    assert access_token_claim[config["jwt"]["identity_claim_key"]] == str(user_id)

    refresh_token_claim = jwt.decode(
        token.access_token, config["jwt"]["secret_key"],
        algorithms=[config["jwt"]["algorithm"]])
    assert refresh_token_claim[config["jwt"]["identity_claim_key"]] == str(user_id)


def test_delete_auth_rpc_service(config: Dict[str, Any], storage: AuthStorage,
                                 user_id: UUID, name: str):
    rpc = AuthRPC(storage, config)
    token = rpc.create_access_token(user_id, name)
    assert token.name == name
    assert token.user_id == str(user_id)
    assert token.id is not None

    access_token = storage.access_token.get(user_id, token.id)
    assert access_token is not None

    rpc.delete_access_token(user_id, token.id)
    access_token = storage.access_token.get(user_id, token.id)
    assert access_token is None
