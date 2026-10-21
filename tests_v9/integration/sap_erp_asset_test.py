# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

import re
from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, SapErpColumn, SapErpTable, SapErpView
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SAPERP")

# Raw SAP names with a namespace prefix, as atlan-saperp-app sees them. The
# qualifiedName uses them cleaned (every non-word character replaced by "_").
TABLE_NAME = f"/BIC/T{MODULE_NAME}"
VIEW_NAME = f"/BIC/V{MODULE_NAME}"
COLUMN_NAME = "/BIC/ZFIELD"


def _clean(name: str) -> str:
    return re.sub(r"\W", "_", name, flags=re.ASCII)


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SAP_ECC
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def table(
    client: AtlanClient, connection: Connection
) -> Generator[SapErpTable, None, None]:
    to_create = SapErpTable.creator(
        name=TABLE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=SapErpTable)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapErpTable)


@pytest.fixture(scope="module")
def view(
    client: AtlanClient, connection: Connection
) -> Generator[SapErpView, None, None]:
    to_create = SapErpView.creator(
        name=VIEW_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=SapErpView)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapErpView)


@pytest.fixture(scope="module")
def table_column(
    client: AtlanClient, table: SapErpTable
) -> Generator[SapErpColumn, None, None]:
    to_create = SapErpColumn.creator(
        name=COLUMN_NAME,
        parent_qualified_name=table.qualified_name,
        parent_name=TABLE_NAME,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SapErpColumn)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapErpColumn)


@pytest.fixture(scope="module")
def view_column(
    client: AtlanClient, view: SapErpView
) -> Generator[SapErpColumn, None, None]:
    to_create = SapErpColumn.creator(
        name=COLUMN_NAME,
        parent_qualified_name=view.qualified_name,
        parent_name=VIEW_NAME,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SapErpColumn)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapErpColumn)


def _assert_retrieved(client, asset, asset_type, connection, qualified_name):
    assert asset.guid
    assert asset.qualified_name == qualified_name
    retrieved = client.asset.get_by_qualified_name(
        qualified_name, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.guid == asset.guid
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.SAP_ECC
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_table(client: AtlanClient, connection: Connection, table: SapErpTable):
    _assert_retrieved(
        client,
        table,
        SapErpTable,
        connection,
        f"{connection.qualified_name}/table/{_clean(TABLE_NAME)}",
    )
    assert table.name == TABLE_NAME


def test_view(client: AtlanClient, connection: Connection, view: SapErpView):
    _assert_retrieved(
        client,
        view,
        SapErpView,
        connection,
        f"{connection.qualified_name}/view/{_clean(VIEW_NAME)}",
    )
    assert view.name == VIEW_NAME


def test_table_column(
    client: AtlanClient,
    connection: Connection,
    table: SapErpTable,
    table_column: SapErpColumn,
):
    retrieved = _assert_retrieved(
        client,
        table_column,
        SapErpColumn,
        connection,
        f"{connection.qualified_name}/column/{_clean(TABLE_NAME)}/{_clean(COLUMN_NAME)}",
    )
    assert retrieved.sap_erp_table.guid == table.guid
    assert retrieved.sap_erp_table_name == TABLE_NAME
    assert retrieved.sap_erp_table_qualified_name == table.qualified_name


def test_view_column(
    client: AtlanClient,
    connection: Connection,
    view: SapErpView,
    view_column: SapErpColumn,
):
    retrieved = _assert_retrieved(
        client,
        view_column,
        SapErpColumn,
        connection,
        f"{connection.qualified_name}/column/{_clean(VIEW_NAME)}/{_clean(COLUMN_NAME)}",
    )
    assert retrieved.sap_erp_view.guid == view.guid
    assert retrieved.sap_erp_view_name == VIEW_NAME
    assert retrieved.sap_erp_view_qualified_name == view.qualified_name
