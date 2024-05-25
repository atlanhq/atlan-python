from typing import Generator, Optional

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.api_tokens import ApiToken
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("Requests")
API_TOKEN_NAME = f"{MODULE_NAME}"


def create_token(client: AtlanClient, name: str) -> ApiToken:
    t = client.token.create(name)
    return t


def delete_token(client: AtlanClient, token: Optional[ApiToken] = None):
    # If there is a partial failure on the server side
    # and the token is still visible in the Atlan UI,
    # in that case, the create method may not return a token.
    # We should retrieve the list of all tokens and delete them here.
    if not token:
        tokens = client.token.get().records
        assert tokens
        delete_tokens = [
            token
            for token in tokens
            if token.display_name and "psdk_Requests" in token.display_name
        ]
        for token in delete_tokens:
            assert token and token.guid
            client.token.purge(token.guid)
        return
    # In case of no partial failure, directly delete the token
    token.guid and client.token.purge(token.guid)


@pytest.fixture(scope="module")
def token(client: AtlanClient) -> Generator[ApiToken, None, None]:
    token = None
    try:
        token = create_token(client, API_TOKEN_NAME)
        yield token
    finally:
        delete_token(client, token)


def test_create_token(client: AtlanClient, token: ApiToken):
    assert token
    r = client.token.get_by_name(API_TOKEN_NAME)
    assert r
    assert r.display_name == API_TOKEN_NAME
    r = client.token.get_by_id(str(token.client_id))
    assert r
    assert r.client_id == token.client_id
    assert r.display_name == token.display_name


@pytest.mark.order(after="test_create_token")
def test_update_token(client: AtlanClient, token: ApiToken):
    description = "Now with a revised description."
    revised = client.token.update(str(token.guid), str(token.display_name), description)
    assert revised
    assert revised.attributes
    assert revised.attributes.description == description
    assert revised.display_name == token.display_name
