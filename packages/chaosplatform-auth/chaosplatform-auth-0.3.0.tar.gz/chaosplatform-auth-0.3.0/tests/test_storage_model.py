import uuid

from chaosplt_auth.storage import AuthStorage
from chaosplt_auth.storage.model import AccessToken, OAuthToken
from chaosplt_relational_storage.db import orm_session


def test_save_access_token(storage: AuthStorage):
    with orm_session() as session:
        token = AccessToken.save(
            name=uuid.uuid4().hex,
            user_id=uuid.uuid4(),
            access_token="at-123456",
            refresh_token="rt-123456",
            session=session
        )
        session.commit()
        assert uuid.UUID(hex=token.id.hex) == token.id


def test_get_access_token(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = AccessToken.save(
            name=uuid.uuid4().hex,
            user_id=user_id,
            access_token="at-123456",
            refresh_token="rt-123456",
            session=session
        )
        session.commit()

        fetched_token = AccessToken.load(user_id, token.id, session)
        assert token == fetched_token


def test_get_access_token_for_user(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = AccessToken.save(
            name=uuid.uuid4().hex,
            user_id=user_id,
            access_token="at-123456",
            refresh_token="rt-123456",
            session=session
        )
        session.commit()

        fetched_tokens = AccessToken.load_by_user(user_id, session)
        assert fetched_tokens == [token]

        fetched_tokens = AccessToken.load_by_user(uuid.uuid4(), session)
        assert fetched_tokens == []


def test_delete_access_token(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = AccessToken.save(
            name=uuid.uuid4().hex,
            user_id=user_id,
            access_token="at-123456",
            refresh_token="rt-123456",
            session=session
        )
        session.commit()

        fetched_token = AccessToken.load(user_id, token.id, session)
        assert token == fetched_token

        AccessToken.delete(user_id, token.id, session)
        fetched_token = AccessToken.load(user_id, token.id, session)
        assert fetched_token == None


def test_save_oauth2_token(storage: AuthStorage):
    with orm_session() as session:
        token = OAuthToken.save(
            user_id=uuid.uuid4(),
            provider="github",
            provider_id=uuid.uuid4().hex,
            token={"token": "a-token"},
            session=session
        )
        session.commit()
        assert token.token == {"token": "a-token"}


def test_get_oauth2_token(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = OAuthToken.save(
            user_id=user_id,
            provider="github",
            provider_id=uuid.uuid4().hex,
            token={"token": "a-token"},
            session=session
        )
        session.commit()

        fetched_token = OAuthToken.load(user_id, token.id, session)
        assert token == fetched_token


def test_cannot_get_oauth2_token_for_different_user(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = OAuthToken.save(
            user_id=user_id,
            provider="github",
            provider_id=uuid.uuid4().hex,
            token={"token": "a-token"},
            session=session
        )
        session.commit()

        fetched_token = OAuthToken.load(user_id, token.id, session)
        assert fetched_token == token

        fetched_token = OAuthToken.load(uuid.uuid4(), token.id, session)
        assert fetched_token == None


def test_get_oauth2_token_for_user(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = OAuthToken.save(
            user_id=user_id,
            provider="github",
            provider_id=uuid.uuid4().hex,
            token={"token": "a-token"},
            session=session
        )
        session.commit()

        fetched_token = OAuthToken.load_by_user(user_id, session)
        assert fetched_token == token

        fetched_token = OAuthToken.load_by_user(uuid.uuid4(), session)
        assert fetched_token == None


def test_get_oauth2_token_by_provider(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()
        provider_id = uuid.uuid4().hex

        token = OAuthToken.save(
            user_id=user_id,
            provider="github",
            provider_id=provider_id,
            token={"token": "a-token"},
            session=session
        )
        session.commit()

        fetched_token = OAuthToken.load_by_provider(
            "github", provider_id, session)
        assert fetched_token == token

        fetched_token = OAuthToken.load_by_provider(
            "bitbucket", provider_id, session)
        assert fetched_token == None


def test_delete_oauth2_token(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = OAuthToken.save(
            user_id=user_id,
            provider="github",
            provider_id=uuid.uuid4().hex,
            token={"token": "a-token"},
            session=session
        )
        session.commit()

        fetched_token = OAuthToken.load(user_id, token.id, session)
        assert token == fetched_token

        OAuthToken.delete(user_id, token.id, session)
        fetched_token = OAuthToken.load(user_id, token.id, session)
        assert fetched_token == None


def test_delete_oauth2_token_by_user(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = OAuthToken.save(
            user_id=user_id,
            provider="github",
            provider_id=uuid.uuid4().hex,
            token={"token": "a-token"},
            session=session
        )
        session.commit()

        fetched_token = OAuthToken.load(user_id, token.id, session)
        assert token == fetched_token

        OAuthToken.delete_by_user(user_id, session)
        fetched_token = OAuthToken.load(user_id, token.id, session)
        assert fetched_token == None


def test_update_oauth2_token(storage: AuthStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        token = OAuthToken.save(
            user_id=user_id,
            provider="github",
            provider_id=uuid.uuid4().hex,
            token={"token": "a-token"},
            session=session
        )
        session.commit()

        OAuthToken.update_by_user(user_id, {"token": "b-token"}, session)

        fetched_token = OAuthToken.load(user_id, token.id, session)
        assert {"token": "a-token"} != fetched_token.token
        assert {"token": "b-token"} == fetched_token.token
