# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.assets import (
    Asset,
    Column,
    ColumnProcess,
    Connection,
    Database,
    MaterialisedView,
    Process,
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

MODULE_NAME = TestId.make_unique("lineage")

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
    result = await create_connection_async(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    await delete_asset_async(client, guid=result.guid, asset_type=Connection)


@pytest_asyncio.fixture(scope="module")
async def database(
    client: AsyncAtlanClient, connection: Connection
) -> AsyncGenerator[Database, None]:
    db = await create_database_async(
        client=client, connection=connection, database_name=DATABASE_NAME
    )
    yield db
    await delete_asset_async(client, guid=db.guid, asset_type=Database)


async def create_database_async(
    client: AsyncAtlanClient, connection, database_name: str
):
    to_create = Database.create(
        name=database_name, connection_qualified_name=connection.qualified_name
    )
    to_create.certificate_status = CERTIFICATE_STATUS
    to_create.certificate_status_message = CERTIFICATE_MESSAGE
    result = await client.asset.save(to_create)
    return result.assets_created(asset_type=Database)[0]


@pytest_asyncio.fixture(scope="module")
async def schema(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
) -> AsyncGenerator[Schema, None]:
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
    assert schema.qualified_name
    to_create = Table.create(
        name=TABLE_NAME, schema_qualified_name=schema.qualified_name
    )
    result = await client.asset.save(to_create)
    tbl = result.assets_created(asset_type=Table)[0]
    yield tbl
    await delete_asset_async(client, guid=tbl.guid, asset_type=Table)


@pytest_asyncio.fixture(scope="module")
async def mview(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
) -> AsyncGenerator[MaterialisedView, None]:
    assert schema.qualified_name
    to_create = MaterialisedView.create(
        name=MVIEW_NAME, schema_qualified_name=schema.qualified_name
    )
    result = await client.asset.save(to_create)
    mv = result.assets_created(asset_type=MaterialisedView)[0]
    yield mv
    await delete_asset_async(client, guid=mv.guid, asset_type=MaterialisedView)


@pytest_asyncio.fixture(scope="module")
async def view(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
) -> AsyncGenerator[View, None]:
    assert schema.qualified_name
    to_create = View.create(name=VIEW_NAME, schema_qualified_name=schema.qualified_name)
    result = await client.asset.save(to_create)
    v = result.assets_created(asset_type=View)[0]
    yield v
    await delete_asset_async(client, guid=v.guid, asset_type=View)


@pytest_asyncio.fixture(scope="module")
async def column1(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
) -> AsyncGenerator[Column, None]:
    assert table.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME1,
        parent_type=Table,
        parent_qualified_name=table.qualified_name,
        order=1,
    )
    result = await client.asset.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=Column)


@pytest_asyncio.fixture(scope="module")
async def column2(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
) -> AsyncGenerator[Column, None]:
    assert table.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME2,
        parent_type=Table,
        parent_qualified_name=table.qualified_name,
        order=2,
    )
    result = await client.asset.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=Column)


@pytest_asyncio.fixture(scope="module")
async def column3(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    mview: MaterialisedView,
) -> AsyncGenerator[Column, None]:
    assert mview.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME3,
        parent_type=MaterialisedView,
        parent_qualified_name=mview.qualified_name,
        order=1,
    )
    result = await client.asset.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=Column)


@pytest_asyncio.fixture(scope="module")
async def column4(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    mview: MaterialisedView,
) -> AsyncGenerator[Column, None]:
    assert mview.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME4,
        parent_type=MaterialisedView,
        parent_qualified_name=mview.qualified_name,
        order=2,
    )
    result = await client.asset.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=Column)


@pytest_asyncio.fixture(scope="module")
async def column5(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    view: View,
) -> AsyncGenerator[Column, None]:
    assert view.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME5,
        parent_type=View,
        parent_qualified_name=view.qualified_name,
        order=1,
    )
    result = await client.asset.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=Column)


@pytest_asyncio.fixture(scope="module")
async def column6(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    view: View,
) -> AsyncGenerator[Column, None]:
    assert view.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME6,
        parent_type=View,
        parent_qualified_name=view.qualified_name,
        order=2,
    )
    result = await client.asset.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=Column)


@pytest_asyncio.fixture(scope="module")
async def lineage_start(
    client: AsyncAtlanClient,
    connection: Connection,
    table: Table,
    mview: MaterialisedView,
) -> AsyncGenerator[Process, None]:
    process_name = f"{table.name} >> {mview.name}"
    assert connection.qualified_name
    to_create = Process.create(
        name=process_name,
        connection_qualified_name=connection.qualified_name,
        inputs=[Table.ref_by_guid(table.guid)],
        outputs=[MaterialisedView.ref_by_guid(mview.guid)],
    )
    response = await client.asset.save(to_create)
    lineage = response.assets_created(asset_type=Process)[0]
    yield lineage
    await delete_asset_async(client, guid=lineage.guid, asset_type=Process)


@pytest_asyncio.fixture(scope="module")
async def cp_lineage_start(
    client: AsyncAtlanClient,
    connection: Connection,
    column1: Column,
    column3: Column,
    lineage_start: Process,
) -> AsyncGenerator[ColumnProcess, None]:
    col_process_name = f"{column1.name} >> {column3.name}"
    assert connection.qualified_name
    to_create = ColumnProcess.create(
        name=col_process_name,
        connection_qualified_name=connection.qualified_name,
        inputs=[Column.ref_by_guid(column1.guid)],
        outputs=[Column.ref_by_guid(column3.guid)],
        parent=Process.ref_by_guid(lineage_start.guid),
    )
    try:
        response = await client.asset.save(to_create)
        cp_ls = response.assets_created(asset_type=ColumnProcess)[0]
        assert len(response.assets_updated(asset_type=Process)) == 1

        yield cp_ls
    finally:
        await delete_asset_async(client, guid=cp_ls.guid, asset_type=ColumnProcess)


@pytest_asyncio.fixture(scope="module")
async def lineage_end(
    client: AsyncAtlanClient,
    connection: Connection,
    mview: MaterialisedView,
    view: View,
) -> AsyncGenerator[Process, None]:
    process_name = f"{mview.name} >> {view.name}"
    assert connection.qualified_name
    to_create = Process.create(
        name=process_name,
        connection_qualified_name=connection.qualified_name,
        inputs=[MaterialisedView.ref_by_guid(mview.guid)],
        outputs=[View.ref_by_guid(view.guid)],
    )
    response = await client.asset.save(to_create)
    lineage = response.assets_created(asset_type=Process)[0]
    yield lineage
    await delete_asset_async(client, guid=lineage.guid, asset_type=Process)


@pytest_asyncio.fixture(scope="module")
async def cp_lineage_end(
    client: AsyncAtlanClient,
    connection: Connection,
    column3: Column,
    column5: Column,
    lineage_end: Process,
) -> AsyncGenerator[ColumnProcess, None]:
    col_process_name = f"{column3.name} >> {column5.name}"
    assert connection.qualified_name
    to_create = ColumnProcess.create(
        name=col_process_name,
        connection_qualified_name=connection.qualified_name,
        inputs=[Column.ref_by_guid(column3.guid)],
        outputs=[Column.ref_by_guid(column5.guid)],
        parent=Process.ref_by_guid(lineage_end.guid),
    )
    try:
        response = await client.asset.save(to_create)
        cp_le = response.assets_created(asset_type=ColumnProcess)[0]
        assert len(response.assets_updated(asset_type=Process)) == 1
        assert response.assets_updated(asset_type=Process)[0].guid == lineage_end.guid
        yield cp_le
    finally:
        await delete_asset_async(client, guid=cp_le.guid, asset_type=ColumnProcess)


def _assert_lineage(asset_1, asset_2, lineage):
    assert lineage
    assert lineage.guid
    assert lineage.qualified_name
    assert lineage.name == f"{asset_1.name} >> {asset_2.name}"
    assert lineage.inputs
    assert len(lineage.inputs) == 1
    assert lineage.inputs[0]
    assert lineage.inputs[0].type_name == asset_1.__class__.__name__
    assert lineage.inputs[0].guid == asset_1.guid
    assert lineage.outputs
    assert len(lineage.outputs) == 1
    assert lineage.outputs[0]
    assert lineage.outputs[0].type_name == asset_2.__class__.__name__
    assert lineage.outputs[0].guid == asset_2.guid


async def test_lineage_start(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
):
    _assert_lineage(table, mview, lineage_start)


async def test_cp_lineage_start(
    column1: Column,
    column3: Column,
    cp_lineage_start: ColumnProcess,
):
    _assert_lineage(column1, column3, cp_lineage_start)


async def test_lineage_end(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_end: Process,
):
    _assert_lineage(mview, view, lineage_end)


async def test_cp_lineage_end(
    column3: Column,
    column5: Column,
    cp_lineage_end: ColumnProcess,
):
    _assert_lineage(column3, column5, cp_lineage_end)


async def test_fetch_lineage_start_list(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = FluentLineage(
        starting_guid=table.guid, includes_on_results=Asset.NAME, size=1
    ).request
    response = await client.asset.get_lineage_list(lineage)
    assert response
    results = []
    async for a in response:
        results.append(a)
    assert len(results) == 4
    assert isinstance(results[0], Process)
    assert results[0].depth == 1
    assert isinstance(results[1], MaterialisedView)
    assert results[1].depth == 1
    assert results[1].guid == mview.guid
    assert isinstance(results[2], Process)
    assert results[2].depth == 2
    assert isinstance(results[3], View)
    assert results[3].depth == 2
    assert results[3].guid == view.guid
    lineage = FluentLineage(
        starting_guid=table.guid, direction=LineageDirection.UPSTREAM
    ).request
    response = await client.asset.get_lineage_list(lineage)
    assert response
    assert not response.has_more


async def test_fetch_lineage_start_list_detailed(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    column1: Column,
    column2: Column,
    column3: Column,
    column4: Column,
    column5: Column,
    column6: Column,
    lineage_start: Process,
    lineage_end: Process,
    cp_lineage_start: ColumnProcess,
    cp_lineage_end: ColumnProcess,
):
    lineage = FluentLineage(
        starting_guid=table.guid,
        includes_on_results=Asset.NAME,
        immediate_neighbors=True,
    ).request
    response = await client.asset.get_lineage_list(lineage)
    assert response
    results = []
    async for a in response:
        results.append(a)
    assert len(results) == 5
    assert isinstance(results[0], Table)
    assert results[0].depth == 0
    assert results[0].guid == table.guid
    assert results[0].immediate_upstream is None
    assert results[0].immediate_downstream and len(results[0].immediate_downstream) == 1
    assert results[0].immediate_downstream[0].guid == mview.guid
    assert isinstance(results[1], Process)
    assert results[1].depth == 1
    assert results[1].immediate_upstream == []
    assert results[1].immediate_downstream and len(results[1].immediate_downstream) == 1
    assert results[1].immediate_downstream[0].guid == lineage_end.guid
    assert isinstance(results[2], MaterialisedView)
    assert results[2].depth == 1
    assert results[2].guid == mview.guid
    assert results[2].immediate_upstream and len(results[2].immediate_upstream) == 1
    assert results[2].immediate_upstream[0].guid == table.guid
    assert results[2].immediate_downstream and len(results[2].immediate_downstream) == 1
    assert results[2].immediate_downstream[0].guid == view.guid
    assert isinstance(results[3], Process)
    assert results[3].depth == 2
    assert results[3].immediate_upstream and len(results[3].immediate_upstream) == 1
    assert results[3].immediate_upstream[0].guid == lineage_start.guid
    assert results[3].immediate_downstream == []
    assert isinstance(results[4], View)
    assert results[4].depth == 2
    assert results[4].guid == view.guid
    assert results[4].immediate_upstream and len(results[4].immediate_upstream) == 1
    assert results[4].immediate_upstream[0].guid == mview.guid
    assert results[4].immediate_downstream is None


async def test_fetch_lineage_middle_list(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = FluentLineage(
        starting_guid=mview.guid, includes_on_results=Asset.NAME, size=5
    ).request
    response = await client.asset.get_lineage_list(lineage)
    assert response
    results = []
    async for a in response:
        results.append(a)
    assert len(results) == 2
    assert isinstance(results[0], Process)
    assert isinstance(results[1], View)
    assert results[1].guid == view.guid
    lineage = FluentLineage(
        starting_guid=mview.guid, direction=LineageDirection.UPSTREAM, size=5
    ).request
    response = await client.asset.get_lineage_list(lineage)
    assert response
    results = []
    async for a in response:
        results.append(a)
    assert len(results) == 2

    assert isinstance(results[1], Table)
    assert results[1].guid == table.guid


async def test_fetch_lineage_end_list(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = FluentLineage(
        starting_guid=view.guid, includes_on_results=Asset.NAME, size=10
    ).request
    response = await client.asset.get_lineage_list(lineage)
    assert response
    assert not response.has_more
    lineage = FluentLineage(
        starting_guid=view.guid, direction=LineageDirection.UPSTREAM
    ).request
    response = await client.asset.get_lineage_list(lineage)
    assert response
    results = []
    async for a in response:
        results.append(a)
    assert len(results) == 4
    assert isinstance(results[0], Process)
    assert isinstance(results[1], MaterialisedView)
    assert isinstance(results[2], Process)
    assert isinstance(results[3], Table)
    one = results[3]
    assert one.guid == table.guid


async def test_search_by_lineage(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    be_active = Term.with_state("ACTIVE")
    have_lineage = Term.with_has_lineage(True)
    be_a_sql_type = Term.with_super_type_names("SQL")
    assert connection.qualified_name
    with_qn_prefix = Prefix.with_qualified_name(connection.qualified_name)
    query = Bool(must=[be_active, have_lineage, be_a_sql_type, with_qn_prefix])
    dsl = DSL(query=query)
    index = IndexSearchRequest(
        dsl=dsl,
        attributes=["name", "__hasLineage"],
    )
    response = await client.asset.search(index)
    assert response
    count = 0
    # TODO: replace with exponential back-off and jitter
    while response.count < 3 and count < 10:
        await asyncio.sleep(2)
        response = await client.asset.search(index)
        count += 1
    assert response
    assert response.count == 6
    assets = []
    asset_types = []
    async for t in response:
        assets.append(t)
        asset_types.append(t.type_name)
        assert t.has_lineage
    assert len(assets) == 6
    assert "Table" in asset_types
    assert "MaterialisedView" in asset_types
    assert "View" in asset_types
    assert "Column" in asset_types


@pytest.mark.order(
    after=[
        "test_lineage_start",
        "test_lineage_end",
        "test_fetch_lineage_start_list",
        "test_fetch_lineage_middle_list",
        "test_fetch_lineage_end_list",
        "test_search_by_lineage",
    ]
)
async def test_delete_lineage(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    response = await client.asset.delete_by_guid(lineage_start.guid)
    assert response
    deleted = response.assets_deleted(asset_type=Process)
    assert len(deleted) == 1
    one = deleted[0]
    assert one
    assert isinstance(one, Process)
    assert one.guid == lineage_start.guid
    assert one.qualified_name == lineage_start.qualified_name
    assert one.status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_lineage")
async def test_restore_lineage(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    assert lineage_start.qualified_name
    assert lineage_start.name
    to_restore = Process.create_for_modification(
        lineage_start.qualified_name, lineage_start.name
    )
    to_restore.status = EntityStatus.ACTIVE
    await client.asset.save(to_restore)
    restored = await client.asset.get_by_guid(
        lineage_start.guid, asset_type=Process, ignore_relationships=False
    )
    assert restored
    count = 0
    # TODO: replace with exponential back-off and jitter
    while restored.status == EntityStatus.DELETED:
        await asyncio.sleep(2)
        restored = await client.asset.get_by_guid(
            lineage_start.guid, asset_type=Process, ignore_relationships=False
        )
        count += 1
    assert restored.guid == lineage_start.guid
    assert restored.qualified_name == lineage_start.qualified_name
    assert restored.status == EntityStatus.ACTIVE


@pytest.mark.order(after="test_restore_lineage")
async def test_purge_lineage(
    client: AsyncAtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    response = await client.asset.purge_by_guid(lineage_start.guid)
    assert response
    purged = response.assets_deleted(asset_type=Process)
    assert len(purged) == 1
    one = purged[0]
    assert one
    assert isinstance(one, Process)
    assert one.guid == lineage_start.guid
    assert one.qualified_name == lineage_start.qualified_name
    assert one.status == EntityStatus.DELETED
