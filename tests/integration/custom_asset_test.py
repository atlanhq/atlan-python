from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Connection, CustomEntity
)
from pyatlan.model.enums import (
    AtlanConnectorType,
    EntityStatus,
)
from pyatlan.model.response import AssetMutationResponse
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.utils import block

MODULE_NAME = TestId.make_unique("CUSTOM")

CONNECTOR_TYPE = AtlanConnectorType.CUSTOM
CUSTOM_ENTITY_NAME = f"{MODULE_NAME}-custom-entity"

response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def custom_entity(
    client: AtlanClient, connection: Connection
) -> Generator[CustomEntity, None, None]:
    assert connection.qualified_name
    to_create = CustomEntity.creator(
        name=CUSTOM_ENTITY_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=CustomEntity)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=CustomEntity)


def test_custom_entity(
    client: AtlanClient, connection: Connection, custom_entity: CustomEntity
):
    assert custom_entity
    assert custom_entity.guid
    assert custom_entity.qualified_name
    assert custom_entity.name == CUSTOM_ENTITY_NAME
    assert custom_entity.connection_qualified_name == connection.qualified_name
    assert custom_entity.connector_name == AtlanConnectorType.CUSTOM.value


@pytest.mark.order(after="test_custom_entity")
def test_delete_custom_entity(
    client: AtlanClient,
    connection: Connection,
    custom_entity: CustomEntity,
):
    response = client.asset.delete_by_guid(custom_entity.guid)
    assert response
    assert not response.assets_created(asset_type=CustomEntity)
    assert not response.assets_updated(asset_type=CustomEntity)
    deleted = response.assets_deleted(asset_type=CustomEntity)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == custom_entity.guid
    assert deleted[0].qualified_name == custom_entity.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_custom_entity")
def test_restore_custom_entity(
    client: AtlanClient,
    connection: Connection,
    custom_entity: CustomEntity,
):
    assert custom_entity.qualified_name
    assert client.asset.restore(
        asset_type=CustomEntity, qualified_name=custom_entity.qualified_name
    )
    assert custom_entity.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=CustomEntity, qualified_name=custom_entity.qualified_name
    )
    assert restored
    assert restored.guid == custom_entity.guid
    assert restored.qualified_name == custom_entity.qualified_name
    assert restored.status == EntityStatus.ACTIVE
