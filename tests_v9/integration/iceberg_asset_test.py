# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    IcebergCatalog,
    IcebergColumn,
    IcebergNamespace,
    IcebergTable,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("ICEBERG")

CATALOG_NAME = f"cat_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.ICEBERG
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


@pytest.fixture(scope="module")
def catalog(
    client: AtlanClient, connection: Connection
) -> Generator[IcebergCatalog, None, None]:
    to_create = IcebergCatalog.creator(
        name=CATALOG_NAME, connection_qualified_name=connection.qualified_name
    )
    result = _save(client, to_create, IcebergCatalog)
    yield result
    delete_asset(client, guid=result.guid, asset_type=IcebergCatalog)


@pytest.fixture(scope="module")
def namespace(
    client: AtlanClient, catalog: IcebergCatalog
) -> Generator[IcebergNamespace, None, None]:
    to_create = IcebergNamespace.creator(
        name="sales", parent_qualified_name=catalog.qualified_name
    )
    result = _save(client, to_create, IcebergNamespace)
    yield result
    delete_asset(client, guid=result.guid, asset_type=IcebergNamespace)


@pytest.fixture(scope="module")
def sub_namespace(
    client: AtlanClient, namespace: IcebergNamespace
) -> Generator[IcebergNamespace, None, None]:
    to_create = IcebergNamespace.creator(
        name="emea", parent_qualified_name=namespace.qualified_name
    )
    result = _save(client, to_create, IcebergNamespace)
    yield result
    delete_asset(client, guid=result.guid, asset_type=IcebergNamespace)


@pytest.fixture(scope="module")
def table(
    client: AtlanClient, sub_namespace: IcebergNamespace
) -> Generator[IcebergTable, None, None]:
    to_create = IcebergTable.creator(
        name="orders", namespace_qualified_name=sub_namespace.qualified_name
    )
    result = _save(client, to_create, IcebergTable)
    yield result
    delete_asset(client, guid=result.guid, asset_type=IcebergTable)


@pytest.fixture(scope="module")
def column(
    client: AtlanClient, table: IcebergTable
) -> Generator[IcebergColumn, None, None]:
    to_create = IcebergColumn.creator(
        name="address", table_qualified_name=table.qualified_name, order=1
    )
    result = _save(client, to_create, IcebergColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=IcebergColumn)


@pytest.fixture(scope="module")
def nested_column(
    client: AtlanClient, table: IcebergTable, column: IcebergColumn
) -> Generator[IcebergColumn, None, None]:
    to_create = IcebergColumn.creator(
        name="city",
        table_qualified_name=table.qualified_name,
        order=1,
        parent_column_qualified_name=column.qualified_name,
    )
    result = _save(client, to_create, IcebergColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=IcebergColumn)


def _retrieve(client: AtlanClient, asset, asset_type, connection: Connection):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.ICEBERG
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_catalog(client: AtlanClient, connection: Connection, catalog: IcebergCatalog):
    assert catalog.guid
    assert catalog.qualified_name == f"{connection.qualified_name}/{CATALOG_NAME}"
    _retrieve(client, catalog, IcebergCatalog, connection)


def test_namespace(
    client: AtlanClient,
    connection: Connection,
    catalog: IcebergCatalog,
    namespace: IcebergNamespace,
):
    assert namespace.guid
    assert namespace.qualified_name == f"{catalog.qualified_name}/sales"
    retrieved = _retrieve(client, namespace, IcebergNamespace, connection)
    assert retrieved.database.guid == catalog.guid
    assert retrieved.database_qualified_name == catalog.qualified_name


def test_sub_namespace(
    client: AtlanClient,
    connection: Connection,
    catalog: IcebergCatalog,
    namespace: IcebergNamespace,
    sub_namespace: IcebergNamespace,
):
    # Namespace "sales.emea", as atlan-iceberg-app names it.
    assert sub_namespace.qualified_name == f"{catalog.qualified_name}/sales/emea"
    retrieved = _retrieve(client, sub_namespace, IcebergNamespace, connection)
    assert retrieved.database.guid == catalog.guid
    assert retrieved.iceberg_parent_namespace_qualified_name == namespace.qualified_name


def test_table(
    client: AtlanClient,
    connection: Connection,
    sub_namespace: IcebergNamespace,
    table: IcebergTable,
):
    assert table.guid
    assert table.qualified_name == f"{sub_namespace.qualified_name}/orders"
    retrieved = _retrieve(client, table, IcebergTable, connection)
    assert retrieved.atlan_schema.guid == sub_namespace.guid
    assert retrieved.schema_qualified_name == sub_namespace.qualified_name


def test_column(
    client: AtlanClient,
    connection: Connection,
    table: IcebergTable,
    column: IcebergColumn,
):
    assert column.guid
    assert column.qualified_name == f"{table.qualified_name}/address"
    retrieved = _retrieve(client, column, IcebergColumn, connection)
    assert retrieved.table.guid == table.guid
    assert retrieved.order == 1


def test_nested_column(
    client: AtlanClient,
    connection: Connection,
    table: IcebergTable,
    column: IcebergColumn,
    nested_column: IcebergColumn,
):
    assert nested_column.qualified_name == f"{table.qualified_name}/address/city"
    retrieved = _retrieve(client, nested_column, IcebergColumn, connection)
    assert retrieved.table.guid == table.guid
    assert retrieved.parent_column_qualified_name == column.qualified_name
    assert retrieved.column_depth_level == 2
