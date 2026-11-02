# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import AnomaloCheck, Connection
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("ANOMALO")

WAREHOUSE_ID = 7
TABLE_ID = "4521"
CHECK_ID = f"check-{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.ANOMALO
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def anomalo_check(
    client: AtlanClient, connection: Connection
) -> Generator[AnomaloCheck, None, None]:
    # The check may run on any asset; the connection stands in for a real table.
    to_create = AnomaloCheck.creator(
        name=f"check_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        warehouse_id=WAREHOUSE_ID,
        table_id=TABLE_ID,
        check_id=CHECK_ID,
        linked_asset_qualified_name=connection.qualified_name,
        linked_asset_type_name="Connection",
    )
    result = client.asset.save(to_create).assets_created(asset_type=AnomaloCheck)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnomaloCheck)


def _check_qualified_name(connection: Connection) -> str:
    return f"{connection.qualified_name}/{WAREHOUSE_ID}/{TABLE_ID}/check/{CHECK_ID}"


def test_anomalo_check(
    client: AtlanClient, connection: Connection, anomalo_check: AnomaloCheck
):
    assert anomalo_check.guid
    retrieved = client.asset.get_by_guid(
        anomalo_check.guid, asset_type=AnomaloCheck, ignore_relationships=False
    )
    assert retrieved.qualified_name == _check_qualified_name(connection)
    assert retrieved.name == anomalo_check.name
    assert retrieved.connector_name == AtlanConnectorType.ANOMALO
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert (
        retrieved.anomalo_check_linked_asset_qualified_name == connection.qualified_name
    )
    assert retrieved.anomalo_check_asset
    assert retrieved.anomalo_check_asset.guid == connection.guid
    retrieved.validate(for_creation=True)


def test_anomalo_check_by_qualified_name(
    client: AtlanClient, connection: Connection, anomalo_check: AnomaloCheck
):
    retrieved = client.asset.get_by_qualified_name(
        _check_qualified_name(connection), asset_type=AnomaloCheck
    )
    assert retrieved.guid == anomalo_check.guid
