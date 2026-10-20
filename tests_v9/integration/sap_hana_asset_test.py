# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import CalculationView, Connection, Database, Schema
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SAPHANA")

# atlan-saphana-app always names the catalog DEFAULT (extract_calc_view.sql).
DATABASE_NAME = "DEFAULT"
SCHEMA_NAME = f"sch_{MODULE_NAME}"
PACKAGE_ID = "sales.reporting"
VIEW_NAME = f"CV_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SAPHANA
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, connection: Connection
) -> Generator[Database, None, None]:
    to_create = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = _save(client, to_create, Database)
    yield result
    delete_asset(client, guid=result.guid, asset_type=Database)


@pytest.fixture(scope="module")
def schema(client: AtlanClient, database: Database) -> Generator[Schema, None, None]:
    to_create = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=database.qualified_name
    )
    result = _save(client, to_create, Schema)
    yield result
    delete_asset(client, guid=result.guid, asset_type=Schema)


@pytest.fixture(scope="module")
def calculation_view(
    client: AtlanClient, schema: Schema
) -> Generator[CalculationView, None, None]:
    to_create = CalculationView.creator(
        name=VIEW_NAME,
        package_id=PACKAGE_ID,
        schema_qualified_name=schema.qualified_name,
    )
    result = _save(client, to_create, CalculationView)
    yield result
    delete_asset(client, guid=result.guid, asset_type=CalculationView)


def test_calculation_view(
    client: AtlanClient,
    connection: Connection,
    database: Database,
    schema: Schema,
    calculation_view: CalculationView,
):
    assert calculation_view.guid
    # {conn}/DEFAULT/{schema}/{package}/{view}, as atlan-saphana-app names it.
    assert (
        calculation_view.qualified_name
        == f"{connection.qualified_name}/DEFAULT/{SCHEMA_NAME}/{PACKAGE_ID}/{VIEW_NAME}"
    )

    retrieved = client.asset.get_by_guid(
        calculation_view.guid,
        asset_type=CalculationView,
        ignore_relationships=False,
    )
    assert retrieved.qualified_name == calculation_view.qualified_name
    assert retrieved.name == VIEW_NAME
    assert retrieved.connector_name == AtlanConnectorType.SAPHANA
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert retrieved.database_qualified_name == database.qualified_name
    assert retrieved.schema_qualified_name == schema.qualified_name
    assert retrieved.calculation_view_package_id == PACKAGE_ID
    assert retrieved.atlan_schema.guid == schema.guid
