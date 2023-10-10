from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.api_tokens import ApiToken
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("Requests")
API_TOKEN_NAME = f"{MODULE_NAME}"


def create_token(client: AtlanClient, name: str) -> ApiToken:
    t = client.token.create(name)
    return t


def delete_token(client: AtlanClient, guid: str) -> None:
    client.token.purge(guid)


@pytest.fixture(scope="module")
def token(client: AtlanClient) -> Generator[ApiToken, None, None]:
    t = create_token(client, API_TOKEN_NAME)
    yield t
    delete_token(client, str(t.guid))


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
