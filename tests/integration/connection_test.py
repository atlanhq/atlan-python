# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectionCategory, AtlanConnectorType
from tests.integration.client import TestId, delete_asset

MODULE_NAME = TestId.make_unique("CONN")


def create_connection(
    client: AtlanClient, name: str, connector_type: AtlanConnectorType
) -> Connection:
    admin_role_guid = str(client.role_cache.get_id_for_name("$admin"))
    to_create = Connection.create(
        client=client,
        name=name,
        connector_type=connector_type,
        admin_roles=[admin_role_guid],
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=Connection)[0]
    return client.asset.get_by_guid(
        result.guid, asset_type=Connection, ignore_relationships=False
    )


@pytest.fixture(scope="module")
def custom_connection(client: AtlanClient) -> Generator[Connection, None, None]:
    CUSTOM_CONNECTOR_TYPE = AtlanConnectorType.CREATE_CUSTOM(
        name=f"{MODULE_NAME}_NAME",
        value=f"{MODULE_NAME}_type",
        category=AtlanConnectionCategory.API,
    )
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CUSTOM_CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    delete_asset(client, guid=result.guid, asset_type=Connection)


def test_custom_connection(custom_connection: Connection):
    assert custom_connection.name == MODULE_NAME
    assert custom_connection.connector_name == f"{MODULE_NAME}_type"
    assert custom_connection.qualified_name
    assert f"default/{MODULE_NAME}_type" in custom_connection.qualified_name
    assert AtlanConnectorType[f"{MODULE_NAME}_NAME"].value == f"{MODULE_NAME}_type"


def test_invalid_connection(client: AtlanClient):
    with pytest.raises(
        ValueError, match="One of admin_user, admin_groups or admin_roles is required"
    ):
        Connection.create(
            client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.POSTGRES
        )


def test_invalid_connection_admin_role(
    client: AtlanClient,
):
    with pytest.raises(
        ValueError, match="Provided role ID abc123 was not found in Atlan."
    ):
        Connection.create(
            client=client,
            name=MODULE_NAME,
            connector_type=AtlanConnectorType.SAPHANA,
            admin_roles=["abc123"],
        )


def test_invalid_connection_admin_group(
    client: AtlanClient,
):
    with pytest.raises(
        ValueError, match="Provided group name abc123 was not found in Atlan."
    ):
        Connection.create(
            client=client,
            name=MODULE_NAME,
            connector_type=AtlanConnectorType.SAPHANA,
            admin_groups=["abc123"],
        )


def test_invalid_connection_admin_user(
    client: AtlanClient,
):
    with pytest.raises(
        ValueError, match="Provided username abc123 was not found in Atlan."
    ):
        Connection.create(
            client=client,
            name=MODULE_NAME,
            connector_type=AtlanConnectorType.SAPHANA,
            admin_users=["abc123"],
        )
