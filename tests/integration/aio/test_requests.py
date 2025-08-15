# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Async requests integration tests."""

from typing import AsyncGenerator

import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.api_tokens import ApiToken
from tests.integration.aio.utils import create_token_async, delete_token_async
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AsyncRequests")
API_TOKEN_NAME = f"{MODULE_NAME}"


@pytest_asyncio.fixture(scope="module")
async def token(client: AsyncAtlanClient) -> AsyncGenerator[ApiToken, None]:
    token = None
    try:
        token = await create_token_async(client, API_TOKEN_NAME)
        yield token
    finally:
        await delete_token_async(client, token)


async def test_create_token(client: AsyncAtlanClient, token: ApiToken):
    assert token
    r = await client.token.get_by_name(API_TOKEN_NAME)
    assert r
    assert r.display_name == API_TOKEN_NAME
    r = await client.token.get_by_id(str(token.client_id))
    assert r
    assert r.client_id == token.client_id
    assert r.display_name == token.display_name


async def test_update_token(client: AsyncAtlanClient, token: ApiToken):
    description = "Now with a revised description."
    revised = await client.token.update(
        str(token.guid), str(token.display_name), description
    )
    assert revised
    assert revised.attributes
    assert revised.attributes.description == description
    assert revised.display_name == token.display_name
