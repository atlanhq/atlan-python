# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, SodaCheck
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SODA")

CHECK_ID = f"check-{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SODA
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def soda_check(
    client: AtlanClient, connection: Connection
) -> Generator[SodaCheck, None, None]:
    to_create = SodaCheck.creator(
        name=f"check_{MODULE_NAME}",
        soda_check_id=CHECK_ID,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SodaCheck)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SodaCheck)


def test_soda_check(client: AtlanClient, connection: Connection, soda_check: SodaCheck):
    assert soda_check.guid
    retrieved = client.asset.get_by_guid(soda_check.guid, asset_type=SodaCheck)
    assert retrieved.qualified_name == f"{connection.qualified_name}/check/{CHECK_ID}"
    assert retrieved.name == soda_check.name
    assert retrieved.soda_check_id == CHECK_ID
    assert retrieved.connector_name == AtlanConnectorType.SODA
    assert retrieved.connection_qualified_name == connection.qualified_name
    retrieved.validate(for_creation=True)


def test_soda_check_by_qualified_name(
    client: AtlanClient, connection: Connection, soda_check: SodaCheck
):
    retrieved = client.asset.get_by_qualified_name(
        f"{connection.qualified_name}/check/{CHECK_ID}", asset_type=SodaCheck
    )
    assert retrieved.guid == soda_check.guid
