from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, CustomEntity
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
)
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("CUSTOM")

CONNECTOR_TYPE = AtlanConnectorType.CUSTOM
CUSTOM_ENTITY_NAME = f"{MODULE_NAME}-custom-entity"

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


def test_update_custom_assets(
    client: AtlanClient,
    custom_entity: CustomEntity,
):
    _update_cert_and_annoucement(client, custom_entity, CustomEntity)


def _retrieve_custom_assets(client, asset, asset_type):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved
    assert not retrieved.is_incomplete
    assert retrieved.guid == asset.guid
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.CUSTOM
    assert retrieved.certificate_status == CERTIFICATE_STATUS
    assert retrieved.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_update_custom_assets")
def test_retrieve_custom_assets(
    client: AtlanClient,
    custom_entity: CustomEntity,
):
    _retrieve_custom_assets(client, custom_entity, CustomEntity)
