# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

import hashlib
from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, FivetranConnector
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("FIVETRAN")

CONNECTOR_ID = f"conn_{MODULE_NAME}"
DESTINATION_ID = f"dest_{MODULE_NAME}"
CONNECTOR_HASH = hashlib.sha1(  # noqa: S324
    f"{CONNECTOR_ID}-{DESTINATION_ID}".encode("utf-8")
).hexdigest()


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.FIVETRAN
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def fivetran_connector(
    client: AtlanClient, connection: Connection
) -> Generator[FivetranConnector, None, None]:
    to_create = FivetranConnector.creator(
        name=f"connector_{MODULE_NAME}",
        connector_id=CONNECTOR_ID,
        destination_id=DESTINATION_ID,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=FivetranConnector)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=FivetranConnector)


def test_fivetran_connector(
    client: AtlanClient,
    connection: Connection,
    fivetran_connector: FivetranConnector,
):
    assert fivetran_connector.guid
    retrieved = client.asset.get_by_guid(
        fivetran_connector.guid, asset_type=FivetranConnector
    )
    assert retrieved.qualified_name == f"{connection.qualified_name}/{CONNECTOR_HASH}"
    assert retrieved.name == fivetran_connector.name
    assert retrieved.connector_name == AtlanConnectorType.FIVETRAN
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert retrieved.fivetran_connector_destination_url == (
        f"https://fivetran.com/dashboard/warehouse?groupId={DESTINATION_ID}"
    )
    retrieved.validate(for_creation=True)


def test_fivetran_connector_by_qualified_name(
    client: AtlanClient,
    connection: Connection,
    fivetran_connector: FivetranConnector,
):
    retrieved = client.asset.get_by_qualified_name(
        f"{connection.qualified_name}/{CONNECTOR_HASH}",
        asset_type=FivetranConnector,
    )
    assert retrieved.guid == fivetran_connector.guid
