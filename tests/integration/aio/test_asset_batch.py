import logging
from time import sleep
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from pyatlan.client.aio.batch import AsyncBatch
from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.assets import (
    Connection,
    Database,
    MaterialisedView,
    Schema,
    Table,
    View,
)
from pyatlan.model.enums import AssetCreationHandling
from pyatlan.test_utils import get_random_connector
from tests.integration.aio.utils import delete_asset_async
from tests.integration.client import TestId

LOGGER = logging.getLogger(__name__)
PREFIX = TestId.make_unique("AsyncBatch")

CONNECTION_NAME = PREFIX
DATABASE_NAME = PREFIX + "_db"
SCHEMA_NAME = PREFIX + "_schema"
TABLE_NAME = PREFIX + "_table"
VIEW_NAME = PREFIX + "_view"
MVIEW_NAME = PREFIX + "_mview"
BATCH_MAX_SIZE = 10
CONNECTOR_TYPE = get_random_connector()
DESCRIPTION = "Automated testing of the Python SDK."


@pytest_asyncio.fixture(scope="module")
async def wait_for_consistency():
    """Wait for eventual consistency."""
    sleep(5)


@pytest_asyncio.fixture(scope="module")
async def connection(client: AsyncAtlanClient) -> AsyncGenerator[Connection, None]:
    admin_role_guid = str(await client.role_cache.get_id_for_name("$admin"))
    c = await Connection.creator_async(
        client=client,
        name=CONNECTION_NAME,
        connector_type=CONNECTOR_TYPE,
        admin_roles=[admin_role_guid],
    )
    response = await client.asset.save(c)
    connection_created = response.assets_created(asset_type=Connection)
    assert connection_created
    c = connection_created[0]
    yield c
    await delete_asset_async(client=client, guid=c.guid, asset_type=Connection)


@pytest_asyncio.fixture(scope="module")
async def database(
    client: AsyncAtlanClient, connection: Connection
) -> AsyncGenerator[Database, None]:
    assert connection.qualified_name
    d = Database.create(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
    )
    response = await client.asset.save(d)
    database_created = response.assets_created(asset_type=Database)
    assert database_created
    d = database_created[0]
    yield d
    await delete_asset_async(client=client, guid=d.guid, asset_type=Database)


@pytest_asyncio.fixture(scope="module")
async def schema(
    client: AsyncAtlanClient, database: Database
) -> AsyncGenerator[Schema, None]:
    assert database.qualified_name
    s = Schema.create(name=SCHEMA_NAME, database_qualified_name=database.qualified_name)
    response = await client.asset.save(s)
    schema_created = response.assets_created(asset_type=Schema)
    assert schema_created
    s = schema_created[0]
    yield s
    await delete_asset_async(client=client, guid=s.guid, asset_type=Schema)


@pytest_asyncio.fixture(scope="module")
async def batch_table_create(
    client: AsyncAtlanClient, schema: Schema
) -> AsyncGenerator[AsyncBatch, None]:
    assert schema and schema.qualified_name

    batch = AsyncBatch(
        client=client,
        creation_handling=AssetCreationHandling.PARTIAL,
        max_size=BATCH_MAX_SIZE,
        table_view_agnostic=True,
        update_only=False,
    )

    # Build tables
    for i in range(1, 4):
        table = Table.create(
            name=f"{TABLE_NAME}{i}", schema_qualified_name=schema.qualified_name
        )
        table.description = DESCRIPTION
        await batch.add(table)

    # Build view
    view = View.create(name=VIEW_NAME, schema_qualified_name=schema.qualified_name)
    view.description = DESCRIPTION
    await batch.add(view)

    # Build materialized view
    mview = MaterialisedView.create(
        name=MVIEW_NAME, schema_qualified_name=schema.qualified_name
    )
    mview.description = DESCRIPTION
    await batch.add(mview)

    # Execute batch
    result = await batch.flush()
    yield result


async def test_batch_create(batch_table_create: AsyncBatch, schema: Schema):
    response = batch_table_create

    # Ensure the response exists
    assert response

    # Verify assets were successfully created (expect 5: 3 tables, 1 view, 1 materialized view)
    tables_created = response.assets_created(asset_type=Table)
    views_created = response.assets_created(asset_type=View)
    mviews_created = response.assets_created(asset_type=MaterialisedView)

    total_created = len(tables_created) + len(views_created) + len(mviews_created)
    assert total_created >= 5

    # Ensure the schema was updated
    schemas_updated = response.assets_updated(asset_type=Schema)
    assert len(schemas_updated) == 1
    assert schemas_updated[0].qualified_name == schema.qualified_name


@pytest.mark.order(after="test_batch_create")
async def test_batch_update(
    wait_for_consistency,
    client: AsyncAtlanClient,
    batch_table_create: AsyncBatch,
    schema: Schema,
):
    create_batch = batch_table_create
    table1 = None
    view = None
    mview = None

    # Get all created assets from the response
    all_tables = create_batch.assets_created(asset_type=Table)
    all_views = create_batch.assets_created(asset_type=View)
    all_mviews = create_batch.assets_created(asset_type=MaterialisedView)

    all_created_assets = all_tables + all_views + all_mviews

    for asset in all_created_assets:
        if asset.name == f"{TABLE_NAME}1":
            table1 = asset
        elif asset.name == VIEW_NAME:
            view = asset
        elif asset.name == MVIEW_NAME:
            mview = asset

    assert table1 and view and mview

    # Create an update batch
    update_batch = AsyncBatch(
        client=client,
        creation_handling=AssetCreationHandling.PARTIAL,
        max_size=BATCH_MAX_SIZE,
        table_view_agnostic=True,
        update_only=True,
    )

    # Update the table with new description
    updated_table = Table.create(
        name=table1.name, schema_qualified_name=schema.qualified_name
    )
    updated_table.description = "Updated description for table"
    await update_batch.add(updated_table)

    # Execute update batch
    result = await update_batch.flush()

    # Verify the update
    assert result
    updated_tables = result.assets_updated(asset_type=Table)
    assert len(updated_tables) == 1
    assert updated_tables[0].name == table1.name
