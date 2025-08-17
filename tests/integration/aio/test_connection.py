# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Async connection integration tests."""

from typing import AsyncGenerator

import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectionCategory, AtlanConnectorType
from tests.integration.aio.utils import delete_asset_async
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AsyncCONN")


async def create_connection_async(
    client: AsyncAtlanClient, name: str, connector_type: AtlanConnectorType
) -> Connection:
    admin_role_guid = str(await client.role_cache.get_id_for_name("$admin"))
    to_create = await Connection.creator_async(
        client=client,
        name=name,
        connector_type=connector_type,
        admin_roles=[admin_role_guid],
    )
    response = await client.asset.save(to_create)
    result = response.assets_created(asset_type=Connection)[0]
    return await client.asset.get_by_guid(
        result.guid, asset_type=Connection, ignore_relationships=False
    )


@pytest_asyncio.fixture(scope="module")
async def custom_connection(
    client: AsyncAtlanClient,
) -> AsyncGenerator[Connection, None]:
    CUSTOM_CONNECTOR_TYPE = AtlanConnectorType.CREATE_CUSTOM(
        name=f"{MODULE_NAME}_NAME",
        value=f"{MODULE_NAME}_type",
        category=AtlanConnectionCategory.API,
    )
    result = await create_connection_async(
        client=client, name=MODULE_NAME, connector_type=CUSTOM_CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    await delete_asset_async(client, guid=result.guid, asset_type=Connection)


async def test_custom_connection(custom_connection: Connection):
    assert custom_connection.name == MODULE_NAME
    assert custom_connection.connector_name == f"{MODULE_NAME}_type"
    assert custom_connection.qualified_name
    assert custom_connection.category == AtlanConnectionCategory.API


async def test_custom_connection_qualified_name(
    client: AsyncAtlanClient, custom_connection: Connection
):
    found = await client.asset.get_by_qualified_name(
        qualified_name=custom_connection.qualified_name,
        asset_type=Connection,
        ignore_relationships=False,
    )
    assert found
    assert found.name == MODULE_NAME
    assert found.connector_name == f"{MODULE_NAME}_type"
