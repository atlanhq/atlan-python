from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Application, Connection
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

MODULE_NAME = TestId.make_unique("APP")

CONNECTOR_TYPE = AtlanConnectorType.APP
APPLICATION_NAME = f"{MODULE_NAME}-application"
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
def application(
    client: AtlanClient, connection: Connection
) -> Generator[Application, None, None]:
    assert connection.qualified_name
    to_create = Application.create(
        name=APPLICATION_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=Application)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Application)


def test_application(
    client: AtlanClient,
    connection: Connection,
    application: Application,
):
    assert application
    assert application.guid
    assert application.qualified_name
    assert application.name == APPLICATION_NAME
    assert application.connection_qualified_name == connection.qualified_name
    assert application.connector_name == AtlanConnectorType.APP.value


# here
def test_update_application(
    client: AtlanClient,
    connection: Connection,
    application: Application,
):
    assert application.qualified_name
    assert application.name
    updated = client.asset.update_certificate(
        asset_type=Application,
        qualified_name=application.qualified_name,
        name=application.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert application.qualified_name
    assert application.name
    updated = client.asset.update_announcement(
        asset_type=Application,
        qualified_name=application.qualified_name,
        name=application.name,
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


@pytest.mark.order(after="test_update_application")
def test_retrieve_application(
    client: AtlanClient,
    connection: Connection,
    application: Application,
):
    b = client.asset.get_by_guid(application.guid, asset_type=Application)
    assert b
    assert not b.is_incomplete
    assert b.guid == application.guid
    assert b.qualified_name == application.qualified_name
    assert b.name == application.name
    assert b.connector_name == application.connector_name
    assert b.connection_qualified_name == application.connection_qualified_name
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_application")
def test_update_application_again(
    client: AtlanClient,
    connection: Connection,
    application: Application,
):
    assert application.qualified_name
    assert application.name
    updated = client.asset.remove_certificate(
        asset_type=Application,
        qualified_name=application.qualified_name,
        name=application.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert application.qualified_name
    updated = client.asset.remove_announcement(
        asset_type=Application,
        qualified_name=application.qualified_name,
        name=application.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_application_again")
def test_delete_application(
    client: AtlanClient,
    connection: Connection,
    application: Application,
):
    response = client.asset.delete_by_guid(application.guid)
    assert response
    assert not response.assets_created(asset_type=Application)
    assert not response.assets_updated(asset_type=Application)
    deleted = response.assets_deleted(asset_type=Application)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == application.guid
    assert deleted[0].qualified_name == application.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_application")
def test_read_deleted_application(
    client: AtlanClient,
    connection: Connection,
    application: Application,
):
    deleted = client.asset.get_by_guid(application.guid, asset_type=Application)
    assert deleted
    assert deleted.guid == application.guid
    assert deleted.qualified_name == application.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_application")
def test_restore_application(
    client: AtlanClient,
    connection: Connection,
    application: Application,
):
    assert application.qualified_name
    assert client.asset.restore(
        asset_type=Application,
        qualified_name=application.qualified_name,
    )
    assert application.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=Application,
        qualified_name=application.qualified_name,
    )
    assert restored
    assert restored.guid == application.guid
    assert restored.qualified_name == application.qualified_name
    assert restored.status == EntityStatus.ACTIVE
