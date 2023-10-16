# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection
from pyatlan.model.enums import AtlanConnectorType
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("CONN")


def create_connection(
    client: AtlanClient, name: str, connector_type: AtlanConnectorType
) -> Connection:
    admin_role_guid = str(RoleCache.get_id_for_name("$admin"))
    to_create = Connection.create(
        name=name, connector_type=connector_type, admin_roles=[admin_role_guid]
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=Connection)[0]
    return client.asset.get_by_guid(result.guid, asset_type=Connection)


def test_invalid_connection(client: AtlanClient):
    with pytest.raises(
        ValueError, match="One of admin_user, admin_groups or admin_roles is required"
    ):
        Connection.create(name=MODULE_NAME, connector_type=AtlanConnectorType.POSTGRES)


def test_invalid_connection_admin_role(
    client: AtlanClient,
):
    with pytest.raises(
        ValueError, match="Provided role ID abc123 was not found in Atlan."
    ):
        Connection.create(
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
            name=MODULE_NAME,
            connector_type=AtlanConnectorType.SAPHANA,
            admin_users=["abc123"],
        )
