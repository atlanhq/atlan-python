# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Column,
    Connection,
    Database,
    MaterialisedView,
    Process,
    Schema,
    Table,
    View,
)
from pyatlan.model.enums import AtlanConnectorType, EntityStatus, LineageDirection
from pyatlan.model.lineage import LineageListRequest, LineageRequest
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Prefix, Term
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

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


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, connection: Connection
) -> Generator[Database, None, None]:
    db = create_database(
        client=client, connection=connection, database_name=DATABASE_NAME
    )
    yield db
    delete_asset(client, guid=db.guid, asset_type=Database)


def create_database(client, connection, database_name: str):
    to_create = Database.create(
        name=database_name, connection_qualified_name=connection.qualified_name
    )
    result = client.save(to_create)
    return result.assets_created(asset_type=Database)[0]


@pytest.fixture(scope="module")
def schema(
    client: AtlanClient,
    connection: Connection,
    database: Database,
) -> Generator[Schema, None, None]:
    assert database.qualified_name
    to_create = Schema.create(
        name=SCHEMA_NAME, database_qualified_name=database.qualified_name
    )
    result = client.save(to_create)
    sch = result.assets_created(asset_type=Schema)[0]
    yield sch
    delete_asset(client, guid=sch.guid, asset_type=Schema)


@pytest.fixture(scope="module")
def table(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
) -> Generator[Table, None, None]:
    assert schema.qualified_name
    to_create = Table.create(
        name=TABLE_NAME, schema_qualified_name=schema.qualified_name
    )
    result = client.save(to_create)
    tbl = result.assets_created(asset_type=Table)[0]
    yield tbl
    delete_asset(client, guid=tbl.guid, asset_type=Table)


@pytest.fixture(scope="module")
def mview(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
) -> Generator[MaterialisedView, None, None]:
    assert schema.qualified_name
    to_create = MaterialisedView.create(
        name=MVIEW_NAME, schema_qualified_name=schema.qualified_name
    )
    result = client.save(to_create)
    mv = result.assets_created(asset_type=MaterialisedView)[0]
    yield mv
    delete_asset(client, guid=mv.guid, asset_type=MaterialisedView)


@pytest.fixture(scope="module")
def view(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
) -> Generator[View, None, None]:
    assert schema.qualified_name
    to_create = View.create(name=VIEW_NAME, schema_qualified_name=schema.qualified_name)
    result = client.save(to_create)
    v = result.assets_created(asset_type=View)[0]
    yield v
    delete_asset(client, guid=v.guid, asset_type=View)


@pytest.fixture(scope="module")
def column1(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
) -> Generator[Column, None, None]:
    assert table.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME1,
        parent_type=Table,
        parent_qualified_name=table.qualified_name,
        order=1,
    )
    result = client.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    delete_asset(client, guid=c.guid, asset_type=Column)


@pytest.fixture(scope="module")
def column2(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
) -> Generator[Column, None, None]:
    assert table.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME2,
        parent_type=Table,
        parent_qualified_name=table.qualified_name,
        order=2,
    )
    result = client.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    delete_asset(client, guid=c.guid, asset_type=Column)


@pytest.fixture(scope="module")
def column3(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    mview: MaterialisedView,
) -> Generator[Column, None, None]:
    assert mview.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME3,
        parent_type=MaterialisedView,
        parent_qualified_name=mview.qualified_name,
        order=1,
    )
    result = client.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    delete_asset(client, guid=c.guid, asset_type=Column)


@pytest.fixture(scope="module")
def column4(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    mview: MaterialisedView,
) -> Generator[Column, None, None]:
    assert mview.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME4,
        parent_type=MaterialisedView,
        parent_qualified_name=mview.qualified_name,
        order=2,
    )
    result = client.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    delete_asset(client, guid=c.guid, asset_type=Column)


@pytest.fixture(scope="module")
def column5(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    view: View,
) -> Generator[Column, None, None]:
    assert view.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME5,
        parent_type=View,
        parent_qualified_name=view.qualified_name,
        order=1,
    )
    result = client.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    delete_asset(client, guid=c.guid, asset_type=Column)


@pytest.fixture(scope="module")
def column6(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    view: View,
) -> Generator[Column, None, None]:
    assert view.qualified_name
    to_create = Column.create(
        name=COLUMN_NAME6,
        parent_type=View,
        parent_qualified_name=view.qualified_name,
        order=2,
    )
    result = client.save(to_create)
    c = result.assets_created(asset_type=Column)[0]
    yield c
    delete_asset(client, guid=c.guid, asset_type=Column)


@pytest.fixture(scope="module")
def lineage_start(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
) -> Generator[Process, None, None]:
    process_name = f"{table.name} >> {mview.name}"
    assert connection.qualified_name
    to_create = Process.create(
        name=process_name,
        connection_qualified_name=connection.qualified_name,
        inputs=[Table.ref_by_guid(table.guid)],
        outputs=[MaterialisedView.ref_by_guid(mview.guid)],
    )
    response = client.save(to_create)
    ls = response.assets_created(asset_type=Process)[0]
    yield ls
    delete_asset(client, guid=ls.guid, asset_type=Process)


def test_lineage_start(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
):
    assert lineage_start
    assert lineage_start.guid
    assert lineage_start.qualified_name
    assert lineage_start.name == f"{table.name} >> {mview.name}"
    assert lineage_start.inputs
    assert len(lineage_start.inputs) == 1
    assert lineage_start.inputs[0]
    assert lineage_start.inputs[0].type_name == "Table"
    assert lineage_start.inputs[0].guid == table.guid
    assert lineage_start.outputs
    assert len(lineage_start.outputs) == 1
    assert lineage_start.outputs[0]
    assert lineage_start.outputs[0].type_name == "MaterialisedView"
    assert lineage_start.outputs[0].guid == mview.guid


@pytest.fixture(scope="module")
def lineage_end(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
) -> Generator[Process, None, None]:
    process_name = f"{mview.name} >> {view.name}"
    assert connection.qualified_name
    to_create = Process.create(
        name=process_name,
        connection_qualified_name=connection.qualified_name,
        inputs=[MaterialisedView.ref_by_guid(mview.guid)],
        outputs=[View.ref_by_guid(view.guid)],
    )
    response = client.save(to_create)
    ls = response.assets_created(asset_type=Process)[0]
    yield ls
    delete_asset(client, guid=ls.guid, asset_type=Process)


def test_lineage_end(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_end: Process,
):
    assert lineage_end
    assert lineage_end.guid
    assert lineage_end.qualified_name
    assert lineage_end.name == f"{mview.name} >> {view.name}"
    assert lineage_end.inputs
    assert len(lineage_end.inputs) == 1
    assert lineage_end.inputs[0]
    assert lineage_end.inputs[0].type_name == "MaterialisedView"
    assert lineage_end.inputs[0].guid == mview.guid
    assert lineage_end.outputs
    assert len(lineage_end.outputs) == 1
    assert lineage_end.outputs[0]
    assert lineage_end.outputs[0].type_name == "View"
    assert lineage_end.outputs[0].guid == view.guid


def test_fetch_lineage_start(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = LineageRequest(guid=table.guid, hide_process=True)
    response = client.get_lineage(lineage)
    assert response
    assert response.base_entity_guid == table.guid
    assert not response.get_upstream_asset_guids()
    downstream_guids = response.get_downstream_asset_guids()
    assert downstream_guids
    assert len(downstream_guids) == 1
    assert mview.guid in downstream_guids
    assert len(response.get_downstream_assets()) == 1
    downstream_guids = response.get_downstream_process_guids()
    assert downstream_guids
    assert len(downstream_guids) == 1
    downstream_dfs = response.get_all_downstream_asset_guids_dfs()
    assert len(downstream_dfs) == 3
    assert downstream_dfs[0] == table.guid
    assert downstream_dfs[1] == mview.guid
    assert downstream_dfs[2] == view.guid
    downstream_dfs_assets = response.get_all_downstream_assets_dfs()
    assert len(downstream_dfs_assets) == 3
    assert downstream_dfs_assets[0].guid == table.guid
    assert downstream_dfs_assets[1].guid == mview.guid
    assert downstream_dfs_assets[2].guid == view.guid
    upstream_dfs = response.get_all_upstream_asset_guids_dfs()
    assert len(upstream_dfs) == 1
    assert upstream_dfs[0] == table.guid


def test_fetch_lineage_start_list(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = LineageListRequest.create(guid=table.guid)
    lineage.attributes = ["name"]
    lineage.size = 1
    response = client.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
        results.append(a)
    assert len(results) == 4
    assert isinstance(results[0], Process)
    assert isinstance(results[1], MaterialisedView)
    assert isinstance(results[2], Process)
    assert isinstance(results[3], View)
    one = results[3]
    assert one.guid == view.guid
    lineage = LineageListRequest.create(guid=table.guid)
    lineage.direction = LineageDirection.UPSTREAM
    response = client.get_lineage_list(lineage)
    assert response
    assert not response.has_more


def test_fetch_lineage_middle(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = LineageRequest(guid=mview.guid, hide_process=True)
    response = client.get_lineage(lineage)
    assert response
    assert response.base_entity_guid == mview.guid
    upstream_guids = response.get_upstream_asset_guids()
    assert upstream_guids
    assert len(upstream_guids) == 1
    assert table.guid in upstream_guids
    upstream_assets = response.get_upstream_assets()
    assert upstream_assets
    assert len(upstream_assets) == 1
    one = upstream_assets[0]
    assert isinstance(one, Table)
    assert one.qualified_name == table.qualified_name
    upstream_guids = response.get_upstream_process_guids()
    assert len(upstream_guids) == 1
    assert lineage_start.guid in upstream_guids
    downstream_guids = response.get_downstream_asset_guids()
    assert downstream_guids
    assert len(downstream_guids) == 1
    assert view.guid in downstream_guids
    downstream_assets = response.get_downstream_assets()
    assert len(downstream_assets) == 1
    one = downstream_assets[0]
    assert isinstance(one, View)
    assert one.qualified_name == view.qualified_name
    downstream_guids = response.get_downstream_process_guids()
    assert downstream_guids
    assert len(downstream_guids) == 1
    assert lineage_end.guid in downstream_guids
    downstream_dfs = response.get_all_downstream_asset_guids_dfs()
    assert len(downstream_dfs) == 2
    assert downstream_dfs[0] == mview.guid
    assert downstream_dfs[1] == view.guid
    downstream_dfs_assets = response.get_all_downstream_assets_dfs()
    assert len(downstream_dfs_assets) == 2
    assert downstream_dfs_assets[0].guid == mview.guid
    assert downstream_dfs_assets[1].guid == view.guid
    upstream_dfs = response.get_all_upstream_asset_guids_dfs()
    assert len(upstream_dfs) == 2
    assert upstream_dfs[0] == mview.guid
    assert upstream_dfs[1] == table.guid
    upstream_dfs_assets = response.get_all_upstream_assets_dfs()
    assert len(upstream_dfs_assets) == 2
    assert upstream_dfs_assets[0].guid == mview.guid
    assert upstream_dfs_assets[1].guid == table.guid


def test_fetch_lineage_middle_list(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = LineageListRequest.create(guid=mview.guid)
    lineage.attributes = ["name"]
    lineage.size = 5
    response = client.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
        results.append(a)
    assert len(results) == 2
    assert isinstance(results[0], Process)
    assert isinstance(results[1], View)
    assert results[1].guid == view.guid
    lineage = LineageListRequest.create(guid=mview.guid)
    lineage.direction = LineageDirection.UPSTREAM
    lineage.size = 5
    response = client.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
        results.append(a)
    assert len(results) == 2
    assert isinstance(results[0], Process)
    assert isinstance(results[1], Table)
    assert results[1].guid == table.guid


def test_fetch_lineage_end(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = LineageRequest(guid=view.guid, hide_process=True)
    response = client.get_lineage(lineage)
    assert response
    assert response.base_entity_guid == view.guid
    upstream_guids = response.get_upstream_asset_guids()
    assert upstream_guids
    assert len(upstream_guids) == 1
    assert mview.guid in upstream_guids
    upstream_guids = response.get_upstream_process_guids()
    assert upstream_guids
    assert len(upstream_guids) == 1
    assert lineage_end.guid in upstream_guids
    downstream_guids = response.get_downstream_asset_guids()
    assert not downstream_guids
    downstream_dfs = response.get_all_downstream_asset_guids_dfs()
    assert len(downstream_dfs) == 1
    assert downstream_dfs[0] == view.guid
    downstream_dfs_assets = response.get_all_downstream_assets_dfs()
    assert len(downstream_dfs_assets) == 1
    assert downstream_dfs_assets[0].guid == view.guid
    upstream_dfs = response.get_all_upstream_asset_guids_dfs()
    assert len(upstream_dfs) == 3
    assert upstream_dfs[0] == view.guid
    assert upstream_dfs[1] == mview.guid
    assert upstream_dfs[2] == table.guid
    upstream_dfs_assets = response.get_all_upstream_assets_dfs()
    assert len(upstream_dfs_assets) == 3
    assert upstream_dfs_assets[0].guid == view.guid
    assert upstream_dfs_assets[1].guid == mview.guid
    assert upstream_dfs_assets[2].guid == table.guid


def test_fetch_lineage_end_list(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    lineage = LineageListRequest.create(guid=view.guid)
    lineage.attributes = ["name"]
    lineage.size = 10
    response = client.get_lineage_list(lineage)
    assert response
    assert not response.has_more
    lineage = LineageListRequest.create(guid=view.guid)
    lineage.direction = LineageDirection.UPSTREAM
    response = client.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
        results.append(a)
    assert len(results) == 4
    assert isinstance(results[0], Process)
    assert isinstance(results[1], MaterialisedView)
    assert isinstance(results[2], Process)
    assert isinstance(results[3], Table)
    one = results[3]
    assert one.guid == table.guid


def test_search_by_lineage(
    client: AtlanClient,
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
    response = client.search(index)
    assert response
    count = 0
    # TODO: replace with exponential back-off and jitter
    while response.count < 3 and count < 10:
        time.sleep(2)
        response = client.search(index)
        count += 1
    assert response
    assert response.count == 3
    assets = []
    asset_types = []
    for t in response:
        assets.append(t)
        asset_types.append(t.type_name)
        assert t.has_lineage
    assert len(assets) == 3
    assert "Table" in asset_types
    assert "MaterialisedView" in asset_types
    assert "View" in asset_types


@pytest.mark.order(
    after=[
        "test_lineage_start",
        "test_lineage_end",
        "test_fetch_lineage_start",
        "test_fetch_lineage_start_list",
        "test_fetch_lineage_middle",
        "test_fetch_lineage_middle_list",
        "test_fetch_lineage_end",
        "test_fetch_lineage_end_list",
        "test_search_by_lineage",
    ]
)
def test_delete_lineage(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    response = client.delete_entity_by_guid(lineage_start.guid)
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
def test_restore_lineage(
    client: AtlanClient,
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
    client.save(to_restore)
    restored = client.get_asset_by_guid(lineage_start.guid, asset_type=Process)
    assert restored
    count = 0
    # TODO: replace with exponential back-off and jitter
    while restored.status == EntityStatus.DELETED:
        time.sleep(2)
        restored = client.get_asset_by_guid(lineage_start.guid, asset_type=Process)
        count += 1
    assert restored.guid == lineage_start.guid
    assert restored.qualified_name == lineage_start.qualified_name
    assert restored.status == EntityStatus.ACTIVE


@pytest.mark.order(after="test_restore_lineage")
def test_purge_lineage(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    table: Table,
    mview: MaterialisedView,
    view: View,
    lineage_start: Process,
    lineage_end: Process,
):
    response = client.purge_entity_by_guid(lineage_start.guid)
    assert response
    purged = response.assets_deleted(asset_type=Process)
    assert len(purged) == 1
    one = purged[0]
    assert one
    assert isinstance(one, Process)
    assert one.guid == lineage_start.guid
    assert one.qualified_name == lineage_start.qualified_name
    assert one.status == EntityStatus.DELETED
