from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    DataverseEntity,
    DataverseAttribute,
    Connection,
)
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.response import AssetMutationResponse
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.utils import block

MODULE_NAME = TestId.make_unique("DATAVERSE")

CONNECTOR_TYPE = AtlanConnectorType.DATAVERSE
DATAVERSE_ENTITY_NAME = f"{MODULE_NAME}-dataverse-entity"
DATAVERSE_ATTRIBUTE_NAME = f"{MODULE_NAME}-dataverse-attribute"
DATAVERSE_ATTRIBUTE_NAME_OVERLOAD = f"{MODULE_NAME}-dataverse-attribute-overload"

response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def dataverse_entity(
    client: AtlanClient, connection: Connection
) -> Generator[DataverseEntity, None, None]:
    assert connection.qualified_name
    to_create = DataverseEntity.creator(
        name=DATAVERSE_ENTITY_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataverseEntity)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataverseEntity)


def test_dataverse_entity(
    client: AtlanClient, connection: Connection, dataverse_entity: DataverseEntity
):
    assert dataverse_entity
    assert dataverse_entity.guid
    assert dataverse_entity.qualified_name
    assert dataverse_entity.name == DATAVERSE_ENTITY_NAME
    assert dataverse_entity.connection_qualified_name == connection.qualified_name
    assert dataverse_entity.connector_name == AtlanConnectorType.DATAVERSE.value


@pytest.fixture(scope="module")
def dataverse_attribute(
    client: AtlanClient, dataverse_entity: DataverseEntity
) -> Generator[DataverseAttribute, None, None]:
    assert dataverse_entity.qualified_name
    to_create = DataverseAttribute.creator(
        name=DATAVERSE_ATTRIBUTE_NAME,
        dataverse_entity_qualified_name=dataverse_entity.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataverseAttribute)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataverseAttribute)


def test_dataverse_attribute(
    client: AtlanClient,
    dataverse_entity: DataverseEntity,
    dataverse_attribute: DataverseAttribute,
):
    assert dataverse_attribute
    assert dataverse_attribute.guid
    assert dataverse_attribute.qualified_name
    assert dataverse_attribute.name == DATAVERSE_ATTRIBUTE_NAME
    assert (
        dataverse_attribute.connection_qualified_name
        == dataverse_entity.connection_qualified_name
    )
    assert dataverse_attribute.connector_name == AtlanConnectorType.DATAVERSE.value


@pytest.fixture(scope="module")
def dataverse_attribute_overload(
    client: AtlanClient, connection: Connection, dataverse_entity: DataverseEntity
) -> Generator[DataverseAttribute, None, None]:
    assert connection.qualified_name
    assert dataverse_entity.qualified_name
    to_create = DataverseAttribute.creator(
        name=DATAVERSE_ATTRIBUTE_NAME_OVERLOAD,
        dataverse_entity_qualified_name=dataverse_entity.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataverseAttribute)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataverseAttribute)


def test_overload_dataverse_attribute(
    client: AtlanClient,
    dataverse_entity: DataverseEntity,
    dataverse_attribute_overload: DataverseAttribute,
):
    assert dataverse_attribute_overload
    assert dataverse_attribute_overload.guid
    assert dataverse_attribute_overload.qualified_name
    assert dataverse_attribute_overload.name == DATAVERSE_ATTRIBUTE_NAME_OVERLOAD
    assert (
        dataverse_attribute_overload.connection_qualified_name
        == dataverse_entity.connection_qualified_name
    )
    assert (
        dataverse_attribute_overload.connector_name
        == AtlanConnectorType.DATAVERSE.value
    )
