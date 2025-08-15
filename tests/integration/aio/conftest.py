# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Conftest for async integration tests."""

from typing import AsyncGenerator

import pytest_asyncio

from pyatlan.client.aio import AsyncAtlanClient
from pyatlan.model.assets import Connection, Database, Schema, Table
from pyatlan.model.enums import AtlanConnectorType, CertificateStatus
from tests.integration.aio.utils import create_connection_async, delete_asset_async
from tests.integration.client import TestId

# Constants for lineage test fixtures
MODULE_NAME = TestId.make_unique("aio-lineage")
DATABASE_NAME = f"{MODULE_NAME}_db"
SCHEMA_NAME = f"{MODULE_NAME}_schema"
TABLE_NAME = f"{MODULE_NAME}_tbl"
CONNECTOR_TYPE = AtlanConnectorType.SNOWFLAKE
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."


@pytest_asyncio.fixture(scope="module")
async def client():
    """Async Atlan client fixture for integration tests."""
    client = AsyncAtlanClient()
    yield client


@pytest_asyncio.fixture(scope="module")
async def connection(client: AsyncAtlanClient) -> AsyncGenerator[Connection, None]:
    """Async connection fixture."""
    result = await create_connection_async(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=Connection)


@pytest_asyncio.fixture(scope="module")
async def database(
    client: AsyncAtlanClient, connection: Connection
) -> AsyncGenerator[Database, None]:
    """Async database fixture."""
    to_create = Database.create(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
    )
    to_create.certificate_status = CERTIFICATE_STATUS
    to_create.certificate_status_message = CERTIFICATE_MESSAGE
    result = await client.asset.save(to_create)
    db = result.assets_created(asset_type=Database)[0]
    yield db
    await delete_asset_async(client, guid=db.guid, asset_type=Database)


@pytest_asyncio.fixture(scope="module")
async def schema(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
) -> AsyncGenerator[Schema, None]:
    """Async schema fixture."""
    assert database.qualified_name
    to_create = Schema.create(
        name=SCHEMA_NAME, database_qualified_name=database.qualified_name
    )
    result = await client.asset.save(to_create)
    sch = result.assets_created(asset_type=Schema)[0]
    yield sch
    await delete_asset_async(client, guid=sch.guid, asset_type=Schema)


@pytest_asyncio.fixture(scope="module")
async def table(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
) -> AsyncGenerator[Table, None]:
    """Async table fixture."""
    assert schema.qualified_name
    to_create = Table.create(
        name=TABLE_NAME, schema_qualified_name=schema.qualified_name
    )
    result = await client.asset.save(to_create)
    tbl = result.assets_created(asset_type=Table)[0]
    yield tbl
    await delete_asset_async(client, guid=tbl.guid, asset_type=Table)
