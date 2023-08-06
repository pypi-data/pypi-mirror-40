import uuid
from uuid import UUID

from chaosplt_auth.views.web.backend import OAuthBackend


def test_get_oauth_token_before_create(oauth_backend: OAuthBackend,
                                       user_id: UUID):
    token = oauth_backend.get_oauth_token(user_id)
    assert token == None


def test_get_oauth_token_after_create(oauth_backend: OAuthBackend,
                                      user_id: UUID):
    token = oauth_backend.get_oauth_token(user_id)
    assert token == None

    new_token = oauth_backend.create_oauth_token(
        user_id, "github", "12345", {"token": "12335"})

    token = oauth_backend.get_oauth_token(user_id)
    assert token == new_token


def test_delete_oauth_token_after_create(oauth_backend: OAuthBackend,
                                         user_id: UUID):
    token = oauth_backend.get_oauth_token(user_id)
    assert token == None

    new_token = oauth_backend.create_oauth_token(
        user_id, "github", uuid.uuid4().hex, {"token": "12335"})

    token = oauth_backend.get_oauth_token(user_id)
    assert token == new_token

    oauth_backend.delete_oauth_token(user_id)

    token = oauth_backend.get_oauth_token(user_id)
    assert token == None


def test_get_oauth_token_by_provider(oauth_backend: OAuthBackend,
                                     user_id: UUID):
    token = oauth_backend.get_oauth_token(user_id)
    assert token == None

    provider_id = uuid.uuid4().hex
    new_token = oauth_backend.create_oauth_token(
        user_id, "github", provider_id, {"token": "12335"})

    token = oauth_backend.get_oauth_token_by_provider("github", provider_id)
    assert token == new_token



def test_update_oauth_token(oauth_backend: OAuthBackend, user_id: UUID):
    token = oauth_backend.get_oauth_token(user_id)
    assert token == None

    token = oauth_backend.create_oauth_token(
        user_id, "github", uuid.uuid4().hex, {"token": "12335"})
    oauth_backend.set_oauth_token(user_id, {"token": "456789"})

    token = oauth_backend.get_oauth_token(user_id)
    assert token.token == {"token": "456789"}
