# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
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
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."


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


def create_database(client: AtlanClient, connection, database_name: str):
    to_create = Database.create(
        name=database_name, connection_qualified_name=connection.qualified_name
    )
    to_create.certificate_status = CERTIFICATE_STATUS
    to_create.certificate_status_message = CERTIFICATE_MESSAGE
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    result = client.asset.save(to_create)
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
    response = client.asset.save(to_create)
    ls = response.assets_created(asset_type=Process)[0]
    yield ls
    delete_asset(client, guid=ls.guid, asset_type=Process)


@pytest.fixture(scope="module")
def cp_lineage_start(
    client: AtlanClient,
    connection: Connection,
    column1: Column,
    column3: Column,
    lineage_start: Process,
) -> Generator[ColumnProcess, None, None]:
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
        response = client.asset.save(to_create)
        cp_ls = response.assets_created(asset_type=ColumnProcess)[0]
        assert len(response.assets_updated(asset_type=Process)) == 1
        assert response.assets_updated(asset_type=Process)[0].guid == lineage_start.guid
        yield cp_ls
    finally:
        delete_asset(client, guid=cp_ls.guid, asset_type=ColumnProcess)


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
    response = client.asset.save(to_create)
    ls = response.assets_created(asset_type=Process)[0]
    yield ls
    delete_asset(client, guid=ls.guid, asset_type=Process)


@pytest.fixture(scope="module")
def cp_lineage_end(
    client: AtlanClient,
    connection: Connection,
    column3: Column,
    column5: Column,
    lineage_end: Process,
) -> Generator[ColumnProcess, None, None]:
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
        response = client.asset.save(to_create)
        cp_le = response.assets_created(asset_type=ColumnProcess)[0]
        assert len(response.assets_updated(asset_type=Process)) == 1
        assert response.assets_updated(asset_type=Process)[0].guid == lineage_end.guid
        yield cp_le
    finally:
        delete_asset(client, guid=cp_le.guid, asset_type=ColumnProcess)


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
    _assert_lineage(table, mview, lineage_start)


def test_cp_lineage_start(
    column1: Column,
    column3: Column,
    cp_lineage_start: ColumnProcess,
):
    _assert_lineage(column1, column3, cp_lineage_start)


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
    _assert_lineage(mview, view, lineage_end)


def test_cp_lineage_end(
    column3: Column,
    column5: Column,
    cp_lineage_end: ColumnProcess,
):
    _assert_lineage(column3, column5, cp_lineage_end)


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
    lineage = FluentLineage(
        starting_guid=table.guid, includes_on_results=Asset.NAME, size=1
    ).request
    response = client.asset.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
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
    response = client.asset.get_lineage_list(lineage)
    assert response
    assert not response.has_more


def test_fetch_lineage_start_list_detailed(
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
    lineage = FluentLineage(
        starting_guid=table.guid,
        includes_on_results=Asset.NAME,
        immediate_neighbors=True,
    ).request
    response = client.asset.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
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
    lineage = FluentLineage(
        starting_guid=table.guid,
        direction=LineageDirection.UPSTREAM,
        immediate_neighbors=True,
    ).request
    response = client.asset.get_lineage_list(lineage)
    assert response
    assert not response.has_more
    assets = response.current_page()
    assert assets[0].immediate_upstream is None
    assert assets[0].immediate_downstream is None


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
    lineage = FluentLineage(
        starting_guid=mview.guid, includes_on_results=Asset.NAME, size=5
    ).request
    response = client.asset.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
        results.append(a)
    assert len(results) == 2
    assert isinstance(results[0], Process)
    assert isinstance(results[1], View)
    assert results[1].guid == view.guid
    lineage = FluentLineage(
        starting_guid=mview.guid, direction=LineageDirection.UPSTREAM, size=5
    ).request
    response = client.asset.get_lineage_list(lineage)
    assert response
    results = []
    for a in response:
        results.append(a)
    assert len(results) == 2
    assert isinstance(results[0], Process)
    assert isinstance(results[1], Table)
    assert results[1].guid == table.guid


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
    lineage = FluentLineage(
        starting_guid=view.guid, includes_on_results=Asset.NAME, size=10
    ).request
    response = client.asset.get_lineage_list(lineage)
    assert response
    assert not response.has_more
    lineage = FluentLineage(
        starting_guid=view.guid, direction=LineageDirection.UPSTREAM
    ).request
    response = client.asset.get_lineage_list(lineage)
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
    response = client.asset.search(index)
    assert response
    count = 0
    # TODO: replace with exponential back-off and jitter
    while response.count < 3 and count < 10:
        time.sleep(2)
        response = client.asset.search(index)
        count += 1
    assert response
    assert response.count == 6
    assets = []
    asset_types = []
    for t in response:
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
    response = client.asset.delete_by_guid(lineage_start.guid)
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
    client.asset.save(to_restore)
    restored = client.asset.get_by_guid(
        lineage_start.guid, asset_type=Process, ignore_relationships=False
    )
    assert restored
    count = 0
    # TODO: replace with exponential back-off and jitter
    while restored.status == EntityStatus.DELETED:
        time.sleep(2)
        restored = client.asset.get_by_guid(
            lineage_start.guid, asset_type=Process, ignore_relationships=False
        )
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
    response = client.asset.purge_by_guid(lineage_start.guid)
    assert response
    purged = response.assets_deleted(asset_type=Process)
    assert len(purged) == 1
    one = purged[0]
    assert one
    assert isinstance(one, Process)
    assert one.guid == lineage_start.guid
    assert one.qualified_name == lineage_start.qualified_name
    assert one.status == EntityStatus.DELETED
