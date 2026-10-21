# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    CassandraColumn,
    CassandraIndex,
    CassandraKeyspace,
    CassandraTable,
    CassandraView,
    Connection,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("CASSANDRA")

KEYSPACE_NAME = f"ks_{MODULE_NAME}"
TABLE_NAME = f"table_{MODULE_NAME}"
VIEW_NAME = f"view_{MODULE_NAME}"
COLUMN_NAME = f"column_{MODULE_NAME}"
INDEX_NAME = f"index_{MODULE_NAME}"


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


def _retrieve(client: AtlanClient, asset, asset_type, connection: Connection):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.CASSANDRA
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.CASSANDRA
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def keyspace(
    client: AtlanClient, connection: Connection
) -> Generator[CassandraKeyspace, None, None]:
    to_create = CassandraKeyspace.creator(
        name=KEYSPACE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = _save(client, to_create, CassandraKeyspace)
    yield result
    delete_asset(client, guid=result.guid, asset_type=CassandraKeyspace)


@pytest.fixture(scope="module")
def table(
    client: AtlanClient, keyspace: CassandraKeyspace
) -> Generator[CassandraTable, None, None]:
    to_create = CassandraTable.creator(
        name=TABLE_NAME, keyspace_qualified_name=keyspace.qualified_name
    )
    result = _save(client, to_create, CassandraTable)
    yield result
    delete_asset(client, guid=result.guid, asset_type=CassandraTable)


@pytest.fixture(scope="module")
def view(
    client: AtlanClient, keyspace: CassandraKeyspace
) -> Generator[CassandraView, None, None]:
    to_create = CassandraView.creator(
        name=VIEW_NAME, keyspace_qualified_name=keyspace.qualified_name
    )
    result = _save(client, to_create, CassandraView)
    yield result
    delete_asset(client, guid=result.guid, asset_type=CassandraView)


@pytest.fixture(scope="module")
def table_column(
    client: AtlanClient, table: CassandraTable
) -> Generator[CassandraColumn, None, None]:
    to_create = CassandraColumn.creator(
        name=COLUMN_NAME,
        parent_qualified_name=table.qualified_name,
        parent_type=CassandraTable,
    )
    result = _save(client, to_create, CassandraColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=CassandraColumn)


@pytest.fixture(scope="module")
def view_column(
    client: AtlanClient, view: CassandraView
) -> Generator[CassandraColumn, None, None]:
    to_create = CassandraColumn.creator(
        name=COLUMN_NAME,
        parent_qualified_name=view.qualified_name,
        parent_type=CassandraView,
    )
    result = _save(client, to_create, CassandraColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=CassandraColumn)


@pytest.fixture(scope="module")
def index(
    client: AtlanClient, table: CassandraTable
) -> Generator[CassandraIndex, None, None]:
    to_create = CassandraIndex.creator(
        name=INDEX_NAME, table_qualified_name=table.qualified_name
    )
    result = _save(client, to_create, CassandraIndex)
    yield result
    delete_asset(client, guid=result.guid, asset_type=CassandraIndex)


def test_keyspace(
    client: AtlanClient, connection: Connection, keyspace: CassandraKeyspace
):
    _retrieve(client, keyspace, CassandraKeyspace, connection)
    assert keyspace.qualified_name == f"{connection.qualified_name}/{KEYSPACE_NAME}"


@pytest.mark.parametrize("fixture_name", ["table", "view"])
def test_table_and_view(
    client: AtlanClient,
    connection: Connection,
    keyspace: CassandraKeyspace,
    fixture_name: str,
    request: pytest.FixtureRequest,
):
    asset = request.getfixturevalue(fixture_name)
    retrieved = _retrieve(client, asset, type(asset), connection)
    assert retrieved.qualified_name == f"{keyspace.qualified_name}/{asset.name}"
    assert retrieved.cassandra_keyspace_name == KEYSPACE_NAME
    assert retrieved.cassandra_keyspace.guid == keyspace.guid


def test_table_column(
    client: AtlanClient,
    connection: Connection,
    table: CassandraTable,
    table_column: CassandraColumn,
):
    retrieved = _retrieve(client, table_column, CassandraColumn, connection)
    assert retrieved.qualified_name == f"{table.qualified_name}/{COLUMN_NAME}"
    assert retrieved.cassandra_keyspace_name == KEYSPACE_NAME
    assert retrieved.cassandra_table_name == TABLE_NAME
    assert retrieved.cassandra_table_qualified_name == table.qualified_name
    assert retrieved.cassandra_table.guid == table.guid


def test_view_column(
    client: AtlanClient,
    connection: Connection,
    view: CassandraView,
    view_column: CassandraColumn,
):
    retrieved = _retrieve(client, view_column, CassandraColumn, connection)
    assert retrieved.qualified_name == f"{view.qualified_name}/{COLUMN_NAME}"
    assert retrieved.cassandra_keyspace_name == KEYSPACE_NAME
    assert retrieved.cassandra_view_name == VIEW_NAME
    assert retrieved.cassandra_view_qualified_name == view.qualified_name
    assert retrieved.cassandra_view.guid == view.guid


def test_index(
    client: AtlanClient,
    connection: Connection,
    table: CassandraTable,
    index: CassandraIndex,
):
    retrieved = _retrieve(client, index, CassandraIndex, connection)
    assert retrieved.qualified_name == f"{table.qualified_name}/{INDEX_NAME}"
    assert retrieved.cassandra_keyspace_name == KEYSPACE_NAME
    assert retrieved.cassandra_table_name == TABLE_NAME
    assert retrieved.cassandra_table_qualified_name == table.qualified_name
    assert retrieved.cassandra_table.guid == table.guid
