# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, SnowflakeShare
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SNOWFLAKE")

SHARE_NAME = f"share_{MODULE_NAME}"
OWNER_ACCOUNT = f"acct_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SNOWFLAKE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def snowflake_share(
    client: AtlanClient, connection: Connection
) -> Generator[SnowflakeShare, None, None]:
    to_create = SnowflakeShare.creator(
        name=SHARE_NAME,
        owner_account=OWNER_ACCOUNT,
        connection_qualified_name=connection.qualified_name,
        kind="INBOUND",
    )
    result = client.asset.save(to_create).assets_created(asset_type=SnowflakeShare)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SnowflakeShare)


def test_snowflake_share(
    client: AtlanClient, connection: Connection, snowflake_share: SnowflakeShare
):
    assert snowflake_share.guid
    retrieved = client.asset.get_by_guid(
        snowflake_share.guid, asset_type=SnowflakeShare
    )
    assert (
        retrieved.qualified_name
        == f"{connection.qualified_name}/share/{OWNER_ACCOUNT}/{SHARE_NAME}"
    )
    assert retrieved.name == SHARE_NAME
    assert retrieved.snowflake_share_owner_account == OWNER_ACCOUNT
    assert retrieved.snowflake_share_kind == "INBOUND"
    assert retrieved.connector_name == AtlanConnectorType.SNOWFLAKE
    assert retrieved.connection_qualified_name == connection.qualified_name
    retrieved.validate(for_creation=True)


def test_snowflake_share_by_qualified_name(
    client: AtlanClient, connection: Connection, snowflake_share: SnowflakeShare
):
    retrieved = client.asset.get_by_qualified_name(
        f"{connection.qualified_name}/share/{OWNER_ACCOUNT}/{SHARE_NAME}",
        asset_type=SnowflakeShare,
    )
    assert retrieved.guid == snowflake_share.guid
