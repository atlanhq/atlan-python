from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, DataverseAttribute, DataverseEntity
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
)
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("DATAVERSE")

CONNECTOR_TYPE = AtlanConnectorType.DATAVERSE
DATAVERSE_ENTITY_NAME = f"{MODULE_NAME}-dataverse-entity"
DATAVERSE_ATTRIBUTE_NAME = f"{MODULE_NAME}-dataverse-attribute"
DATAVERSE_ATTRIBUTE_NAME_OVERLOAD = f"{MODULE_NAME}-dataverse-attribute-overload"

CERTIFICATE_STATUS = CertificateStatus.VERIFIED

ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


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


def _update_cert_and_annoucement(client, asset, asset_type):
    assert asset.name
    assert asset.qualified_name

    updated = client.asset.update_certificate(
        name=asset.name,
        asset_type=asset_type,
        qualified_name=asset.qualified_name,
        message=CERTIFICATE_MESSAGE,
        certificate_status=CERTIFICATE_STATUS,
    )
    assert updated
    assert updated.certificate_status == CERTIFICATE_STATUS
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE

    updated = client.asset.update_announcement(
        name=asset.name,
        asset_type=asset_type,
        qualified_name=asset.qualified_name,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.announcement_type == ANNOUNCEMENT_TYPE
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE


def test_update_dataverse_assets(
    client: AtlanClient,
    dataverse_entity: DataverseEntity,
    dataverse_attribute: DataverseAttribute,
):
    _update_cert_and_annoucement(client, dataverse_entity, DataverseEntity)
    _update_cert_and_annoucement(client, dataverse_attribute, DataverseAttribute)


def _retrieve_dataverse_assets(client, asset, asset_type):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved
    assert not retrieved.is_incomplete
    assert retrieved.guid == asset.guid
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.DATAVERSE
    assert retrieved.certificate_status == CERTIFICATE_STATUS
    assert retrieved.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_update_dataverse_assets")
def test_retrieve_dataverse_assets(
    client: AtlanClient,
    dataverse_entity: DataverseEntity,
    dataverse_attribute: DataverseAttribute,
):
    _retrieve_dataverse_assets(client, dataverse_entity, DataverseEntity)
    _retrieve_dataverse_assets(client, dataverse_attribute, DataverseAttribute)


@pytest.mark.order(after="test_retrieve_dataverse_assets")
def test_delete_dataverse_attribute(
    client: AtlanClient,
    dataverse_attribute: DataverseAttribute,
):
    response = client.asset.delete_by_guid(guid=dataverse_attribute.guid)
    assert response
    assert not response.assets_created(asset_type=DataverseAttribute)
    assert not response.assets_updated(asset_type=DataverseAttribute)
    deleted = response.assets_deleted(asset_type=DataverseAttribute)

    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == dataverse_attribute.guid
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED
    assert deleted[0].qualified_name == dataverse_attribute.qualified_name


@pytest.mark.order(after="test_delete_dataverse_attribute")
def test_read_deleted_dataverse_attribute(
    client: AtlanClient,
    dataverse_attribute: DataverseAttribute,
):
    deleted = client.asset.get_by_guid(
        dataverse_attribute.guid,
        asset_type=DataverseAttribute,
        ignore_relationships=False,
    )
    assert deleted
    assert deleted.status == EntityStatus.DELETED
    assert deleted.guid == dataverse_attribute.guid
    assert deleted.qualified_name == dataverse_attribute.qualified_name


@pytest.mark.order(after="test_read_deleted_dataverse_attribute")
def test_restore_dataverse_attribute(
    client: AtlanClient,
    dataverse_attribute: DataverseAttribute,
):
    assert dataverse_attribute.qualified_name
    assert client.asset.restore(
        asset_type=DataverseAttribute, qualified_name=dataverse_attribute.qualified_name
    )
    assert dataverse_attribute.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=DataverseAttribute,
        qualified_name=dataverse_attribute.qualified_name,
        ignore_relationships=False,
    )
    assert restored
    assert restored.guid == dataverse_attribute.guid
    assert restored.status == EntityStatus.ACTIVE
    assert restored.qualified_name == dataverse_attribute.qualified_name
