# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""SQL creators at non-standard depths (FND-3887): schema-less tables (Workday Prism,
NetSuite), schemas without a database (db2 z/OS) and nested columns."""

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Column,
    Connection,
    Procedure,
    Schema,
    Table,
    View,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SQLDEPTH")


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.NETSUITE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def table(client: AtlanClient, connection: Connection) -> Generator[Table, None, None]:
    to_create = Table.creator(
        name=f"table_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=Table)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Table)


@pytest.fixture(scope="module")
def column(client: AtlanClient, table: Table) -> Generator[Column, None, None]:
    to_create = Column.creator(
        name=f"column_{MODULE_NAME}",
        parent_qualified_name=table.qualified_name,
        parent_type=Table,
        order=1,
        connection_qualified_name=table.connection_qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=Column)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Column)


@pytest.fixture(scope="module")
def nested_column(
    client: AtlanClient, table: Table, column: Column
) -> Generator[Column, None, None]:
    parent = Column.creator(
        name=column.name,
        parent_qualified_name=table.qualified_name,
        parent_type=Table,
        order=1,
        connection_qualified_name=table.connection_qualified_name,
    )
    to_create = Column.creator(
        name=f"nested_{MODULE_NAME}",
        parent_qualified_name=column.qualified_name,
        parent_type=Column,
        order=2,
        parent_column=parent,
    )
    result = client.asset.save(to_create).assets_created(asset_type=Column)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Column)


@pytest.fixture(scope="module")
def schema(
    client: AtlanClient, connection: Connection
) -> Generator[Schema, None, None]:
    to_create = Schema.creator(
        name=f"schema_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=Schema)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Schema)


@pytest.fixture(scope="module")
def view(client: AtlanClient, schema: Schema) -> Generator[View, None, None]:
    to_create = View.creator(
        name=f"view_{MODULE_NAME}",
        schema_qualified_name=schema.qualified_name,
        connection_qualified_name=schema.connection_qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=View)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=View)


@pytest.fixture(scope="module")
def procedure(client: AtlanClient, schema: Schema) -> Generator[Procedure, None, None]:
    to_create = Procedure.creator(
        name=f"procedure_{MODULE_NAME}",
        definition="CREATE PROCEDURE p() BEGIN END",
        schema_qualified_name=schema.qualified_name,
        connection_qualified_name=schema.connection_qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=Procedure)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Procedure)


def _retrieve(client: AtlanClient, asset, asset_type):
    retrieved = client.asset.get_by_qualified_name(
        asset.qualified_name, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.guid == asset.guid
    assert retrieved.connector_name == AtlanConnectorType.NETSUITE
    return retrieved


def test_schema_less_table(client: AtlanClient, connection: Connection, table: Table):
    assert table.qualified_name == f"{connection.qualified_name}/table_{MODULE_NAME}"
    retrieved = _retrieve(client, table, Table)
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert not retrieved.schema_qualified_name


def test_column_under_schema_less_table(
    client: AtlanClient, table: Table, column: Column
):
    assert column.qualified_name == f"{table.qualified_name}/column_{MODULE_NAME}"
    retrieved = _retrieve(client, column, Column)
    assert retrieved.table.guid == table.guid
    assert retrieved.table_qualified_name == table.qualified_name


def test_nested_column(
    client: AtlanClient, table: Table, column: Column, nested_column: Column
):
    assert nested_column.qualified_name == (
        f"{column.qualified_name}/nested_{MODULE_NAME}"
    )
    retrieved = _retrieve(client, nested_column, Column)
    assert retrieved.parent_column.guid == column.guid
    assert retrieved.table.guid == table.guid
    assert retrieved.column_depth_level == 2
    assert retrieved.parent_column_qualified_name == column.qualified_name


def test_schema_without_database(
    client: AtlanClient, connection: Connection, schema: Schema
):
    assert schema.qualified_name == f"{connection.qualified_name}/schema_{MODULE_NAME}"
    retrieved = _retrieve(client, schema, Schema)
    assert not retrieved.database_qualified_name


def test_view_under_schema_without_database(
    client: AtlanClient, schema: Schema, view: View
):
    assert view.qualified_name == f"{schema.qualified_name}/view_{MODULE_NAME}"
    retrieved = _retrieve(client, view, View)
    assert retrieved.atlan_schema.guid == schema.guid


def test_procedure_under_schema_without_database(
    client: AtlanClient, schema: Schema, procedure: Procedure
):
    assert procedure.qualified_name == (
        f"{schema.qualified_name}/_procedures_/procedure_{MODULE_NAME}"
    )
    retrieved = _retrieve(client, procedure, Procedure)
    assert retrieved.atlan_schema.guid == schema.guid
