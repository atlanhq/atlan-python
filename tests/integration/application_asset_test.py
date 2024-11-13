from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import ApplicationAsset, Connection
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
)
from pyatlan.model.response import AssetMutationResponse
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.utils import block

MODULE_NAME = TestId.make_unique("APPLICATION")

CONNECTOR_TYPE = AtlanConnectorType.APPLICATION
APPLICATION_ASSET_NAME = f"{MODULE_NAME}-application-asset"
APPLICATION_ASSET_NAME_OVERLOAD_1 = f"{MODULE_NAME}-application-asset-overload-1"
APPLICATION_ASSET_NAME_OVERLOAD_2 = f"{MODULE_NAME}-application-asset-overload-2"
APPLICATION_ASSET_ID = "1234"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def application_asset(
    client: AtlanClient, connection: Connection
) -> Generator[ApplicationAsset, None, None]:
    assert connection.qualified_name
    to_create = ApplicationAsset.create(
        name=APPLICATION_ASSET_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ApplicationAsset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ApplicationAsset)


def test_application_asset(
    client: AtlanClient, connection: Connection, application_asset: ApplicationAsset
):
    assert application_asset
    assert application_asset.guid
    assert application_asset.qualified_name
    assert application_asset.name == APPLICATION_ASSET_NAME
    assert application_asset.connection_qualified_name == connection.qualified_name
    assert application_asset.connector_name == AtlanConnectorType.APPLICATION.value


@pytest.fixture(scope="module")
def application_asset_overload_1(
    client: AtlanClient, connection: Connection
) -> Generator[ApplicationAsset, None, None]:
    assert connection.qualified_name
    to_create = ApplicationAsset.create(
        name=APPLICATION_ASSET_NAME,
        connection_qualified_name=connection.qualified_name,
        application_id=APPLICATION_ASSET_ID,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ApplicationAsset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ApplicationAsset)


def test_application_asset_overload_1(
    client: AtlanClient,
    connection: Connection,
    application_asset_overload_1: ApplicationAsset,
):
    assert application_asset_overload_1
    assert application_asset_overload_1.guid
    assert application_asset_overload_1.qualified_name
    assert application_asset_overload_1.name == APPLICATION_ASSET_NAME
    assert (
        application_asset_overload_1.connection_qualified_name
        == connection.qualified_name
    )
    assert (
        application_asset_overload_1.connector_name
        == AtlanConnectorType.APPLICATION.value
    )
    assert application_asset_overload_1.application_id == APPLICATION_ASSET_ID


# here
def test_update_application_asset(
    client: AtlanClient, connection: Connection, application_asset: ApplicationAsset
):
    assert application_asset.qualified_name
    assert application_asset.name
    updated = client.asset.update_certificate(
        asset_type=ApplicationAsset,
        qualified_name=application_asset.qualified_name,
        name=application_asset.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert application_asset.qualified_name
    assert application_asset.name
    updated = client.asset.update_announcement(
        asset_type=ApplicationAsset,
        qualified_name=application_asset.qualified_name,
        name=application_asset.name,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE


@pytest.mark.order(after="test_update_application_asset")
def test_retrieve_application_asset(
    client: AtlanClient, connection: Connection, application_asset: ApplicationAsset
):
    b = client.asset.get_by_guid(application_asset.guid, asset_type=ApplicationAsset)
    assert b
    assert not b.is_incomplete
    assert b.guid == application_asset.guid
    assert b.qualified_name == application_asset.qualified_name
    assert b.name == application_asset.name
    assert b.connector_name == application_asset.connector_name
    assert b.connection_qualified_name == application_asset.connection_qualified_name
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_application_asset")
def test_update_application_asset_again(
    client: AtlanClient, connection: Connection, application_asset: ApplicationAsset
):
    assert application_asset.qualified_name
    assert application_asset.name
    updated = client.asset.remove_certificate(
        asset_type=ApplicationAsset,
        qualified_name=application_asset.qualified_name,
        name=application_asset.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert application_asset.qualified_name
    updated = client.asset.remove_announcement(
        asset_type=ApplicationAsset,
        qualified_name=application_asset.qualified_name,
        name=application_asset.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_application_asset_again")
def test_delete_application_asset(
    client: AtlanClient, connection: Connection, application_asset: ApplicationAsset
):
    response = client.asset.delete_by_guid(application_asset.guid)
    assert response
    assert not response.assets_created(asset_type=ApplicationAsset)
    assert not response.assets_updated(asset_type=ApplicationAsset)
    deleted = response.assets_deleted(asset_type=ApplicationAsset)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == application_asset.guid
    assert deleted[0].qualified_name == application_asset.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_application_asset")
def test_read_deleted_application_asset(
    client: AtlanClient, connection: Connection, application_asset: ApplicationAsset
):
    deleted = client.asset.get_by_guid(
        application_asset.guid, asset_type=ApplicationAsset
    )
    assert deleted
    assert deleted.guid == application_asset.guid
    assert deleted.qualified_name == application_asset.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_application_asset")
def test_restore_application_asset(
    client: AtlanClient, connection: Connection, application_asset: ApplicationAsset
):
    assert application_asset.qualified_name
    assert client.asset.restore(
        asset_type=ApplicationAsset, qualified_name=application_asset.qualified_name
    )
    assert application_asset.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=ApplicationAsset, qualified_name=application_asset.qualified_name
    )
    assert restored
    assert restored.guid == application_asset.guid
    assert restored.qualified_name == application_asset.qualified_name
    assert restored.status == EntityStatus.ACTIVE
