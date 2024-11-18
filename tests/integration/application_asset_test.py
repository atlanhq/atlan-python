from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import ApplicationContainer, Connection
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
APPLICATION_CONTAINER_NAME = f"{MODULE_NAME}-application-container"
APPLICATION_CONTAINER_ID = "1234"
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
def application_container(
    client: AtlanClient, connection: Connection
) -> Generator[ApplicationContainer, None, None]:
    assert connection.qualified_name
    to_create = ApplicationContainer.creator(
        name=APPLICATION_CONTAINER_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ApplicationContainer)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ApplicationContainer)


def test_application_container(
    client: AtlanClient,
    connection: Connection,
    application_container: ApplicationContainer,
):
    assert application_container
    assert application_container.guid
    assert application_container.qualified_name
    assert application_container.name == APPLICATION_CONTAINER_NAME
    assert application_container.connection_qualified_name == connection.qualified_name
    assert application_container.connector_name == AtlanConnectorType.APPLICATION.value


# here
def test_update_application_container(
    client: AtlanClient,
    connection: Connection,
    application_container: ApplicationContainer,
):
    assert application_container.qualified_name
    assert application_container.name
    updated = client.asset.update_certificate(
        asset_type=ApplicationContainer,
        qualified_name=application_container.qualified_name,
        name=application_container.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert application_container.qualified_name
    assert application_container.name
    updated = client.asset.update_announcement(
        asset_type=ApplicationContainer,
        qualified_name=application_container.qualified_name,
        name=application_container.name,
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


@pytest.mark.order(after="test_update_application_container")
def test_retrieve_application_container(
    client: AtlanClient,
    connection: Connection,
    application_container: ApplicationContainer,
):
    b = client.asset.get_by_guid(
        application_container.guid, asset_type=ApplicationContainer
    )
    assert b
    assert not b.is_incomplete
    assert b.guid == application_container.guid
    assert b.qualified_name == application_container.qualified_name
    assert b.name == application_container.name
    assert b.connector_name == application_container.connector_name
    assert (
        b.connection_qualified_name == application_container.connection_qualified_name
    )
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_application_container")
def test_update_application_container_again(
    client: AtlanClient,
    connection: Connection,
    application_container: ApplicationContainer,
):
    assert application_container.qualified_name
    assert application_container.name
    updated = client.asset.remove_certificate(
        asset_type=ApplicationContainer,
        qualified_name=application_container.qualified_name,
        name=application_container.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert application_container.qualified_name
    updated = client.asset.remove_announcement(
        asset_type=ApplicationContainer,
        qualified_name=application_container.qualified_name,
        name=application_container.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_application_container_again")
def test_delete_application_container(
    client: AtlanClient,
    connection: Connection,
    application_container: ApplicationContainer,
):
    response = client.asset.delete_by_guid(application_container.guid)
    assert response
    assert not response.assets_created(asset_type=ApplicationContainer)
    assert not response.assets_updated(asset_type=ApplicationContainer)
    deleted = response.assets_deleted(asset_type=ApplicationContainer)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == application_container.guid
    assert deleted[0].qualified_name == application_container.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_application_container")
def test_read_deleted_application_container(
    client: AtlanClient,
    connection: Connection,
    application_container: ApplicationContainer,
):
    deleted = client.asset.get_by_guid(
        application_container.guid, asset_type=ApplicationContainer
    )
    assert deleted
    assert deleted.guid == application_container.guid
    assert deleted.qualified_name == application_container.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_application_container")
def test_restore_application_container(
    client: AtlanClient,
    connection: Connection,
    application_container: ApplicationContainer,
):
    assert application_container.qualified_name
    assert client.asset.restore(
        asset_type=ApplicationContainer,
        qualified_name=application_container.qualified_name,
    )
    assert application_container.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=ApplicationContainer,
        qualified_name=application_container.qualified_name,
    )
    assert restored
    assert restored.guid == application_container.guid
    assert restored.qualified_name == application_container.qualified_name
    assert restored.status == EntityStatus.ACTIVE
