import uuid

from chaosplt_auth.storage.concrete import AccessTokenService, OAuthTokenService
from chaosplt_auth.storage.model import AccessToken, OAuthToken
from chaosplt_relational_storage.db import orm_session, RelationalStorage


def test_save_access_token(storage: RelationalStorage):
    svc = AccessTokenService(storage)
    token = svc.create(
        name=uuid.uuid4().hex,
        user_id=uuid.uuid4(),
        access_token="at-123456",
        refresh_token="rt-123456",
    )
    assert uuid.UUID(hex=token.id.hex) == token.id


def test_get_access_token(storage: RelationalStorage):
    svc = AccessTokenService(storage)
    user_id = uuid.uuid4()

    token = svc.create(
        name=uuid.uuid4().hex,
        user_id=user_id,
        access_token="at-123456",
        refresh_token="rt-123456",
    )

    fetched_token = svc.get(user_id, token.id)
    assert token == fetched_token


def test_get_access_token_for_user(storage: RelationalStorage):
    svc = AccessTokenService(storage)
    user_id = uuid.uuid4()

    token = svc.create(
        name=uuid.uuid4().hex,
        user_id=user_id,
        access_token="at-123456",
        refresh_token="rt-123456",
    )

    fetched_token = svc.get_by_user(user_id)
    assert {token.name: token} == fetched_token


def test_delete_access_token(storage: RelationalStorage):
    svc = AccessTokenService(storage)
    user_id = uuid.uuid4()

    token = svc.create(
        name=uuid.uuid4().hex,
        user_id=user_id,
        access_token="at-123456",
        refresh_token="rt-123456",
    )

    fetched_token = svc.get_by_user(user_id)
    assert {token.name: token} == fetched_token

    svc.delete(user_id, token.id)
    
    fetched_token = svc.get_by_user(user_id)
    assert fetched_token == {}


def test_save_oauth2_token(storage: RelationalStorage):
    svc = OAuthTokenService(storage)

    token = svc.create(
        user_id=uuid.uuid4(),
        provider="github",
        provider_id=uuid.uuid4().hex,
        token={"token": "a-token"}
    )
    assert token.token == {"token": "a-token"}


def test_get_oauth2_token(storage: RelationalStorage):
    svc = OAuthTokenService(storage)
    user_id = uuid.uuid4()

    token = svc.create(
        user_id=user_id,
        provider="github",
        provider_id=uuid.uuid4().hex,
        token={"token": "a-token"}
    )
    fetched_token = svc.get(user_id, token.id)
    assert token == fetched_token


def test_cannot_get_oauth2_token_for_different_user(storage: RelationalStorage):
    svc = OAuthTokenService(storage)
    user_id = uuid.uuid4()

    token = svc.create(
        user_id=user_id,
        provider="github",
        provider_id=uuid.uuid4().hex,
        token={"token": "a-token"}
    )

    fetched_token = svc.get(user_id, token.id)
    assert fetched_token == token

    fetched_token = svc.get(uuid.uuid4(), token.id)
    assert fetched_token == None


def test_cannot_get_for_different_user(storage: RelationalStorage):
    svc = OAuthTokenService(storage)
    user_id = uuid.uuid4()

    token = svc.create(
        user_id=user_id,
        provider="github",
        provider_id=uuid.uuid4().hex,
        token={"token": "a-token"}
    )

    fetched_token = svc.get_by_user(user_id)
    assert fetched_token == token

    fetched_token = svc.get_by_user(uuid.uuid4())
    assert fetched_token == None


def test_get_oauth2_token_by_provider(storage: RelationalStorage):
    svc = OAuthTokenService(storage)
    user_id = uuid.uuid4()
    provider_id= uuid.uuid4().hex

    token = svc.create(
        user_id=user_id,
        provider="github",
        provider_id=provider_id,
        token={"token": "a-token"}
    )

    fetched_token = svc.get_by_provider("github", provider_id)
    assert fetched_token == token

    fetched_token = svc.get_by_provider("bitbucket", provider_id)
    assert fetched_token == None


def test_delete_oauth2_token(storage: RelationalStorage):
    svc = OAuthTokenService(storage)
    user_id = uuid.uuid4()
    provider_id= uuid.uuid4().hex

    token = svc.create(
        user_id=user_id,
        provider="github",
        provider_id=provider_id,
        token={"token": "a-token"}
    )

    fetched_token = svc.get(user_id, token.id)
    assert token == fetched_token

    svc.delete(user_id, token.id)
    fetched_token = svc.get(user_id, token.id)
    assert fetched_token == None


def test_delete_oauth2_token_by_user(storage: RelationalStorage):
    svc = OAuthTokenService(storage)
    user_id = uuid.uuid4()
    provider_id= uuid.uuid4().hex

    token = svc.create(
        user_id=user_id,
        provider="github",
        provider_id=provider_id,
        token={"token": "a-token"}
    )

    fetched_token = svc.get(user_id, token.id)
    assert token == fetched_token

    svc.delete_by_user(user_id)
    fetched_token = svc.get(user_id, token.id)
    assert fetched_token == None


def test_update_oauth2_token(storage: RelationalStorage):
    svc = OAuthTokenService(storage)
    user_id = uuid.uuid4()
    provider_id= uuid.uuid4().hex

    token = svc.create(
        user_id=user_id,
        provider="github",
        provider_id=provider_id,
        token={"token": "a-token"}
    )

    svc.set_for_user(user_id, {"token": "b-token"})

    fetched_token = svc.get(user_id, token.id)
    assert {"token": "a-token"} != fetched_token.token
    assert {"token": "b-token"} == fetched_token.token
