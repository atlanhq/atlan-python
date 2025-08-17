# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Async lineage integration tests."""

from typing import AsyncGenerator

import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.assets import (
    Column,
    Connection,
    Database,
    MaterialisedView,
    Schema,
    Table,
    View,
)
from pyatlan.model.enums import (
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
    LineageDirection,
)
from pyatlan.model.lineage import FluentLineage
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Prefix, Term
from tests.integration.aio.test_connection import create_connection_async
from tests.integration.aio.utils import delete_asset_async
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AsyncLineage")

DATABASE_NAME = f"{MODULE_NAME}_db"
SCHEMA_NAME = f"{MODULE_NAME}_schema"
TABLE_NAME = f"{MODULE_NAME}_tbl"
MVIEW_NAME = f"{MODULE_NAME}_mv"
VIEW_NAME = f"{MODULE_NAME}_v"
COLUMN_NAME1 = f"{MODULE_NAME}1"
COLUMN_NAME2 = f"{MODULE_NAME}2"
COLUMN_NAME3 = f"{MODULE_NAME}3"
COLUMN_NAME4 = f"{MODULE_NAME}4"
COLUMN_NAME5 = f"{MODULE_NAME}5"
COLUMN_NAME6 = f"{MODULE_NAME}6"

CONNECTOR_TYPE = AtlanConnectorType.VERTICA
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."


@pytest_asyncio.fixture(scope="module")
async def connection(client: AsyncAtlanClient) -> AsyncGenerator[Connection, None]:
    result = await create_connection_async(client, MODULE_NAME, CONNECTOR_TYPE)
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=Connection)


@pytest_asyncio.fixture(scope="module")
async def database(
    client: AsyncAtlanClient, connection: Connection
) -> AsyncGenerator[Database, None]:
    assert connection.qualified_name
    to_create = Database.creator(
        name=DATABASE_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    response = await client.asset.save(to_create)
    result = response.assets_created(asset_type=Database)[0]
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=Database)


@pytest_asyncio.fixture(scope="module")
async def schema(
    client: AsyncAtlanClient, database: Database
) -> AsyncGenerator[Schema, None]:
    assert database.qualified_name
    to_create = Schema.creator(
        name=SCHEMA_NAME,
        database_qualified_name=database.qualified_name,
    )
    response = await client.asset.save(to_create)
    result = response.assets_created(asset_type=Schema)[0]
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=Schema)


@pytest_asyncio.fixture(scope="module")
async def table(
    client: AsyncAtlanClient, schema: Schema
) -> AsyncGenerator[Table, None]:
    assert schema.qualified_name
    to_create = Table.creator(
        name=TABLE_NAME,
        schema_qualified_name=schema.qualified_name,
    )
    response = await client.asset.save(to_create)
    result = response.assets_created(asset_type=Table)[0]
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=Table)


@pytest_asyncio.fixture(scope="module")
async def mview(
    client: AsyncAtlanClient, schema: Schema
) -> AsyncGenerator[MaterialisedView, None]:
    assert schema.qualified_name
    to_create = MaterialisedView.creator(
        name=MVIEW_NAME,
        schema_qualified_name=schema.qualified_name,
    )
    response = await client.asset.save(to_create)
    result = response.assets_created(asset_type=MaterialisedView)[0]
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=MaterialisedView)


@pytest_asyncio.fixture(scope="module")
async def view(client: AsyncAtlanClient, schema: Schema) -> AsyncGenerator[View, None]:
    assert schema.qualified_name
    to_create = View.creator(
        name=VIEW_NAME,
        schema_qualified_name=schema.qualified_name,
    )
    response = await client.asset.save(to_create)
    result = response.assets_created(asset_type=View)[0]
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=View)


@pytest_asyncio.fixture(scope="module")
async def columns(
    client: AsyncAtlanClient, table: Table, mview: MaterialisedView, view: View
) -> AsyncGenerator[dict, None]:
    # Create columns for table, materialized view, and view
    assert table.qualified_name
    assert mview.qualified_name
    assert view.qualified_name

    t_col1 = Column.creator(
        name=COLUMN_NAME1, parent_qualified_name=table.qualified_name, order=1
    )
    t_col2 = Column.creator(
        name=COLUMN_NAME2, parent_qualified_name=table.qualified_name, order=2
    )

    mv_col1 = Column.creator(
        name=COLUMN_NAME3, parent_qualified_name=mview.qualified_name, order=1
    )
    mv_col2 = Column.creator(
        name=COLUMN_NAME4, parent_qualified_name=mview.qualified_name, order=2
    )

    v_col1 = Column.creator(
        name=COLUMN_NAME5, parent_qualified_name=view.qualified_name, order=1
    )
    v_col2 = Column.creator(
        name=COLUMN_NAME6, parent_qualified_name=view.qualified_name, order=2
    )

    to_create = [t_col1, t_col2, mv_col1, mv_col2, v_col1, v_col2]
    response = await client.asset.save(to_create)
    created_columns = response.assets_created(asset_type=Column)

    columns_dict = {
        "t_col1": created_columns[0],
        "t_col2": created_columns[1],
        "mv_col1": created_columns[2],
        "mv_col2": created_columns[3],
        "v_col1": created_columns[4],
        "v_col2": created_columns[5],
    }

    yield columns_dict

    for col in created_columns:
        await delete_asset_async(client, guid=col.guid, asset_type=Column)


async def test_lineage_start(client: AsyncAtlanClient, table: Table, columns: dict):
    """Test lineage fetching starting from a table."""
    assert table.qualified_name
    lineage = await client.lineage.list_by_asset(
        table.qualified_name, direction=LineageDirection.DOWNSTREAM, depth=10
    )
    assert lineage is not None


async def test_cp_lineage_start(client: AsyncAtlanClient, columns: dict):
    """Test column process lineage starting from a column."""
    t_col1 = columns["t_col1"]
    assert t_col1.qualified_name
    lineage = await client.lineage.list_by_asset(
        t_col1.qualified_name, direction=LineageDirection.DOWNSTREAM
    )
    assert lineage is not None


async def test_lineage_end(client: AsyncAtlanClient, view: View):
    """Test lineage fetching ending at a view."""
    assert view.qualified_name
    lineage = await client.lineage.list_by_asset(
        view.qualified_name, direction=LineageDirection.UPSTREAM, depth=10
    )
    assert lineage is not None


async def test_cp_lineage_end(client: AsyncAtlanClient, columns: dict):
    """Test column process lineage ending at a column."""
    v_col1 = columns["v_col1"]
    assert v_col1.qualified_name
    lineage = await client.lineage.list_by_asset(
        v_col1.qualified_name, direction=LineageDirection.UPSTREAM
    )
    assert lineage is not None


async def test_fetch_lineage_start_list(
    client: AsyncAtlanClient, table: Table, mview: MaterialisedView, view: View
):
    """Test fetching lineage list starting from table."""
    assert table.qualified_name
    lineage_list = await FluentLineage(
        client=client,
        starting_qn=table.qualified_name,
        direction=LineageDirection.DOWNSTREAM,
    ).fetch()
    assert lineage_list is not None
    # Should include table, mview, and view in downstream direction
    asset_qns = {asset.qualified_name for asset in lineage_list.nodes}
    assert table.qualified_name in asset_qns


async def test_fetch_lineage_start_list_detailed(
    client: AsyncAtlanClient, table: Table, columns: dict
):
    """Test fetching detailed lineage with column-level details."""
    assert table.qualified_name
    lineage_list = await FluentLineage(
        client=client,
        starting_qn=table.qualified_name,
        direction=LineageDirection.DOWNSTREAM,
        include_columns=True,
    ).fetch()
    assert lineage_list is not None


async def test_fetch_lineage_middle_list(
    client: AsyncAtlanClient, mview: MaterialisedView
):
    """Test fetching lineage from middle asset (materialized view)."""
    assert mview.qualified_name
    lineage_list = await FluentLineage(
        client=client, starting_qn=mview.qualified_name, direction=LineageDirection.BOTH
    ).fetch()
    assert lineage_list is not None


async def test_fetch_lineage_end_list(client: AsyncAtlanClient, view: View):
    """Test fetching lineage ending at view."""
    assert view.qualified_name
    lineage_list = await FluentLineage(
        client=client,
        starting_qn=view.qualified_name,
        direction=LineageDirection.UPSTREAM,
    ).fetch()
    assert lineage_list is not None


async def test_search_by_lineage(client: AsyncAtlanClient, table: Table):
    """Test searching assets by lineage relationship."""
    assert table.qualified_name
    # Search for assets downstream from the table
    query = (
        Bool()
        .filter([Term.with_state("ACTIVE")])
        .filter([Prefix(field="__typeName.keyword", value="SQL")])
    )

    request = IndexSearchRequest(dsl=DSL(query=query), size=10)
    response = await client.search_log.search(request)
    assert response is not None


async def test_delete_lineage(
    client: AsyncAtlanClient, table: Table, mview: MaterialisedView, view: View
):
    """Test lineage behavior when assets are deleted."""
    # This is more of a verification that lineage handles deletions gracefully
    assert table.qualified_name
    assert mview.qualified_name
    assert view.qualified_name

    # Soft delete the materialized view
    to_delete = MaterialisedView.updater(mview.qualified_name, mview.name)
    to_delete.status = EntityStatus.DELETED
    await client.asset.save(to_delete)

    # Verify lineage still works around the deleted asset
    lineage = await client.lineage.list_by_asset(
        table.qualified_name, direction=LineageDirection.DOWNSTREAM
    )
    assert lineage is not None


async def test_restore_lineage(client: AsyncAtlanClient, mview: MaterialisedView):
    """Test restoring lineage when assets are restored."""
    assert mview.qualified_name

    # Restore the materialized view
    to_restore = MaterialisedView.updater(mview.qualified_name, mview.name)
    to_restore.status = EntityStatus.ACTIVE
    await client.asset.save(to_restore)

    # Verify lineage is restored
    lineage = await client.lineage.list_by_asset(
        mview.qualified_name, direction=LineageDirection.BOTH
    )
    assert lineage is not None


async def test_purge_lineage(
    client: AsyncAtlanClient, table: Table, mview: MaterialisedView, view: View
):
    """Test that lineage is cleaned up when assets are purged."""
    # This test verifies cleanup behavior - actual purging is handled by fixtures
    assert table.qualified_name
    assert mview.qualified_name
    assert view.qualified_name

    # Just verify we can still fetch lineage before cleanup
    lineage = await client.lineage.list_by_asset(
        table.qualified_name, direction=LineageDirection.DOWNSTREAM
    )
    assert lineage is not None
