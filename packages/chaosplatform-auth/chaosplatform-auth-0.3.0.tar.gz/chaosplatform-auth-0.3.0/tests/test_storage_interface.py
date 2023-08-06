import pytest

from chaosplt_auth.storage.interface import BaseAccessTokenService, \
    BaseOAuthTokenService


def test_cannot_instanciate_acess_token_interface():
    try:
        BaseAccessTokenService()
    except TypeError as e:
        return
    else:
        pytest.fail("BaseAccessTokenService should remain abstract")


def test_cannot_instanciate_acess_token_interface():
    try:
        BaseOAuthTokenService()
    except TypeError as e:
        return
    else:
        pytest.fail("BaseOAuthTokenService should remain abstract")
