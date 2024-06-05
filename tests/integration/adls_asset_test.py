from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import ADLSAccount, ADLSContainer, ADLSObject, Connection
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
)
from pyatlan.model.response import AssetMutationResponse
from pyatlan.utils import get_parent_qualified_name
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.utils import block

MODULE_NAME = TestId.make_unique("ADLS")

CONNECTOR_TYPE = AtlanConnectorType.ADLS
ADLS_ACCOUNT_NAME = MODULE_NAME
ADLS_CONNECTION_QUALIFIED_NAME = f"{MODULE_NAME}"
CONTAINER_NAME = f"mycontainer_{MODULE_NAME}"
CONTAINER_NAME_OVERLOAD = f"mycontainer_overload_{MODULE_NAME}"
OBJECT_NAME = f"myobject_{MODULE_NAME}.csv"
OBJECT_NAME_OVERLOAD = f"myobject_overload_{MODULE_NAME}.csv"
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
def adls_account(
    client: AtlanClient, connection: Connection
) -> Generator[ADLSAccount, None, None]:
    assert connection.qualified_name
    to_create = ADLSAccount.create(
        name=ADLS_ACCOUNT_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ADLSAccount)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ADLSAccount)


def test_adls_account(
    client: AtlanClient,
    connection: Connection,
    adls_account: ADLSAccount,
):
    assert adls_account
    assert adls_account.guid
    assert adls_account.qualified_name
    assert adls_account.connection_qualified_name == connection.qualified_name
    assert adls_account.name == ADLS_ACCOUNT_NAME
    assert adls_account.connector_name == AtlanConnectorType.ADLS.value


@pytest.fixture(scope="module")
def adls_container(
    client: AtlanClient, adls_account: ADLSAccount
) -> Generator[ADLSContainer, None, None]:
    assert adls_account.qualified_name
    to_create = ADLSContainer.create(
        name=CONTAINER_NAME, adls_account_qualified_name=adls_account.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ADLSContainer)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ADLSContainer)


def test_adls_container(
    client: AtlanClient,
    adls_account: ADLSAccount,
    adls_container: ADLSContainer,
):
    assert adls_container
    assert adls_container.guid
    assert adls_container.qualified_name
    assert adls_container.adls_account_qualified_name == adls_account.qualified_name
    assert adls_container.name == CONTAINER_NAME
    assert adls_container.connector_name == AtlanConnectorType.ADLS.value


@pytest.fixture(scope="module")
def adls_container_overload(
    client: AtlanClient, adls_account: ADLSAccount, connection: Connection
) -> Generator[ADLSContainer, None, None]:
    assert adls_account.qualified_name
    assert connection.qualified_name
    to_create = ADLSContainer.creator(
        name=CONTAINER_NAME_OVERLOAD,
        adls_account_qualified_name=adls_account.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ADLSContainer)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ADLSContainer)


def test_overload_adls_container(
    client: AtlanClient,
    adls_account: ADLSAccount,
    adls_container_overload: ADLSContainer,
):
    assert adls_container_overload
    assert adls_container_overload.guid
    assert adls_container_overload.qualified_name
    assert (
        adls_container_overload.adls_account_qualified_name
        == adls_account.qualified_name
    )
    assert adls_container_overload.name == CONTAINER_NAME_OVERLOAD
    assert adls_container_overload.connector_name == AtlanConnectorType.ADLS.value


@pytest.fixture(scope="module")
def adls_object(
    client: AtlanClient, adls_container: ADLSContainer
) -> Generator[ADLSObject, None, None]:
    assert adls_container.qualified_name
    to_create = ADLSObject.create(
        name=OBJECT_NAME,
        adls_container_qualified_name=adls_container.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ADLSObject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ADLSObject)


@pytest.fixture(scope="module")
def adls_object_overload(
    client: AtlanClient,
    adls_container_overload: ADLSContainer,
    adls_account: ADLSAccount,
    connection: Connection,
) -> Generator[ADLSObject, None, None]:
    assert adls_container_overload.qualified_name
    assert adls_account.qualified_name
    assert connection.qualified_name
    to_create = ADLSObject.creator(
        name=OBJECT_NAME_OVERLOAD,
        adls_container_qualified_name=adls_container_overload.qualified_name,
        adls_account_qualified_name=adls_account.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=ADLSObject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ADLSObject)


def test_overload_adls_object(
    client: AtlanClient,
    adls_container_overload: ADLSContainer,
    adls_object_overload: ADLSObject,
):
    assert adls_object_overload
    assert adls_object_overload.guid
    assert adls_object_overload.qualified_name
    assert (
        adls_object_overload.adls_container_qualified_name
        == adls_container_overload.qualified_name
    )
    assert adls_object_overload.name == OBJECT_NAME_OVERLOAD
    assert adls_object_overload.connector_name == AtlanConnectorType.ADLS.value
    assert adls_container_overload.qualified_name
    assert (
        adls_object_overload.adls_account_qualified_name
        == get_parent_qualified_name(adls_container_overload.qualified_name)
    )


def test_adls_object(
    client: AtlanClient,
    adls_container: ADLSContainer,
    adls_object: ADLSObject,
):
    assert adls_object
    assert adls_object.guid
    assert adls_object.qualified_name
    assert adls_object.adls_container_qualified_name == adls_container.qualified_name
    assert adls_object.name == OBJECT_NAME
    assert adls_object.connector_name == AtlanConnectorType.ADLS.value
    assert adls_container.qualified_name
    assert adls_object.adls_account_qualified_name == get_parent_qualified_name(
        adls_container.qualified_name
    )


def test_update_adls_object(
    client: AtlanClient,
    connection: Connection,
    adls_container: ADLSContainer,
    adls_object: ADLSObject,
):
    assert adls_object.qualified_name
    assert adls_object.name
    updated = client.asset.update_certificate(
        asset_type=ADLSObject,
        qualified_name=adls_object.qualified_name,
        name=OBJECT_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert adls_object.qualified_name
    assert adls_object.name
    updated = client.asset.update_announcement(
        asset_type=ADLSObject,
        qualified_name=adls_object.qualified_name,
        name=OBJECT_NAME,
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


@pytest.mark.order(after="test_update_adls_object")
def test_retrieve_adls_object(
    client: AtlanClient,
    connection: Connection,
    adls_container: ADLSContainer,
    adls_object: ADLSObject,
):
    b = client.asset.get_by_guid(adls_object.guid, asset_type=ADLSObject)
    assert b
    assert not b.is_incomplete
    assert b.guid == adls_object.guid
    assert b.qualified_name == adls_object.qualified_name
    assert b.name == OBJECT_NAME
    assert b.connector_name == AtlanConnectorType.ADLS.value
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_adls_object")
def test_update_adls_object_again(
    client: AtlanClient,
    connection: Connection,
    adls_container: ADLSContainer,
    adls_object: ADLSObject,
):
    assert adls_object.qualified_name
    assert adls_object.name
    updated = client.asset.remove_certificate(
        asset_type=ADLSObject,
        qualified_name=adls_object.qualified_name,
        name=adls_object.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert adls_object.qualified_name
    updated = client.asset.remove_announcement(
        qualified_name=adls_object.qualified_name,
        asset_type=ADLSObject,
        name=adls_object.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_adls_object_again")
def test_delete_adls_object(
    client: AtlanClient,
    connection: Connection,
    adls_container: ADLSContainer,
    adls_object: ADLSObject,
):
    response = client.asset.delete_by_guid(adls_object.guid)
    assert response
    assert not response.assets_created(asset_type=ADLSObject)
    assert not response.assets_updated(asset_type=ADLSObject)
    deleted = response.assets_deleted(asset_type=ADLSObject)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == adls_object.guid
    assert deleted[0].qualified_name == adls_object.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_adls_object")
def test_read_deleted_adls_object(
    client: AtlanClient,
    connection: Connection,
    adls_container: ADLSContainer,
    adls_object: ADLSObject,
):
    deleted = client.asset.get_by_guid(adls_object.guid, asset_type=ADLSObject)
    assert deleted
    assert deleted.guid == adls_object.guid
    assert deleted.qualified_name == adls_object.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_adls_object")
def test_restore_object(
    client: AtlanClient,
    connection: Connection,
    adls_container: ADLSContainer,
    adls_object: ADLSObject,
):
    assert adls_object.qualified_name
    assert client.asset.restore(
        asset_type=ADLSObject, qualified_name=adls_object.qualified_name
    )
    assert adls_object.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=ADLSObject, qualified_name=adls_object.qualified_name
    )
    assert restored
    assert restored.guid == adls_object.guid
    assert restored.qualified_name == adls_object.qualified_name
    assert restored.status == EntityStatus.ACTIVE
