# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    DynamoDBGlobalSecondaryIndex,
    DynamoDBLocalSecondaryIndex,
    DynamoDBTable,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("DYNAMODB")

TABLE_NAME = f"table_{MODULE_NAME}"
GSI_NAME = f"gsi_{MODULE_NAME}"
LSI_NAME = f"lsi_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.DYNAMODB
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def table(
    client: AtlanClient, connection: Connection
) -> Generator[DynamoDBTable, None, None]:
    to_create = DynamoDBTable.creator(
        name=TABLE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=DynamoDBTable)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DynamoDBTable)


@pytest.fixture(scope="module")
def gsi(
    client: AtlanClient, table: DynamoDBTable
) -> Generator[DynamoDBGlobalSecondaryIndex, None, None]:
    to_create = DynamoDBGlobalSecondaryIndex.creator(
        name=GSI_NAME, table_qualified_name=table.qualified_name
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=DynamoDBGlobalSecondaryIndex
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DynamoDBGlobalSecondaryIndex)


@pytest.fixture(scope="module")
def lsi(
    client: AtlanClient, table: DynamoDBTable
) -> Generator[DynamoDBLocalSecondaryIndex, None, None]:
    to_create = DynamoDBLocalSecondaryIndex.creator(
        name=LSI_NAME, table_qualified_name=table.qualified_name
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=DynamoDBLocalSecondaryIndex
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DynamoDBLocalSecondaryIndex)


def test_table(client: AtlanClient, connection: Connection, table: DynamoDBTable):
    assert table.guid
    assert table.qualified_name == f"{connection.qualified_name}/{TABLE_NAME}"
    retrieved = client.asset.get_by_qualified_name(
        table.qualified_name, asset_type=DynamoDBTable
    )
    assert retrieved.guid == table.guid
    assert retrieved.name == TABLE_NAME
    assert retrieved.connector_name == AtlanConnectorType.DYNAMODB
    assert retrieved.connection_qualified_name == connection.qualified_name


@pytest.mark.parametrize(
    "fixture_name, asset_type, separator, index_name",
    [
        ("gsi", DynamoDBGlobalSecondaryIndex, "_gsi_", GSI_NAME),
        ("lsi", DynamoDBLocalSecondaryIndex, "_lsi_", LSI_NAME),
    ],
    ids=["gsi", "lsi"],
)
def test_secondary_index(
    request: pytest.FixtureRequest,
    client: AtlanClient,
    connection: Connection,
    table: DynamoDBTable,
    fixture_name: str,
    asset_type: type,
    separator: str,
    index_name: str,
):
    index = request.getfixturevalue(fixture_name)
    assert index.guid
    assert index.qualified_name == f"{table.qualified_name}/{separator}/{index_name}"
    retrieved = client.asset.get_by_qualified_name(
        index.qualified_name, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.guid == index.guid
    assert retrieved.name == index_name
    assert retrieved.table_name == TABLE_NAME
    assert retrieved.table_qualified_name == table.qualified_name
    assert retrieved.connector_name == AtlanConnectorType.DYNAMODB
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert retrieved.dynamo_db_table.guid == table.guid
