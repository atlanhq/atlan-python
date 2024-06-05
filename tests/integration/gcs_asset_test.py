from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, GCSBucket, GCSObject
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

MODULE_NAME = TestId.make_unique("GCS")

CONNECTOR_TYPE = AtlanConnectorType.GCS
GCS_BUCKET_NAME = MODULE_NAME
GCS_OBJECT_NAME = f"{MODULE_NAME}.csv"
GCS_OBJECT_NAME_OVERLOAD = f"{MODULE_NAME}_overload.csv"
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
def gcs_bucket(
    client: AtlanClient, connection: Connection
) -> Generator[GCSBucket, None, None]:
    assert connection.qualified_name
    to_create = GCSBucket.create(
        name=GCS_BUCKET_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=GCSBucket)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=GCSBucket)


def test_gcs_bucket(client: AtlanClient, connection: Connection, gcs_bucket: GCSBucket):
    assert gcs_bucket
    assert gcs_bucket.guid
    assert gcs_bucket.qualified_name
    assert gcs_bucket.connection_qualified_name == connection.qualified_name
    assert gcs_bucket.name == GCS_BUCKET_NAME
    assert gcs_bucket.connector_name == AtlanConnectorType.GCS.value


@pytest.fixture(scope="module")
def gcs_object(
    client: AtlanClient, connection: Connection, gcs_bucket: GCSBucket
) -> Generator[GCSObject, None, None]:
    assert gcs_bucket.qualified_name
    to_create = GCSObject.create(
        name=GCS_OBJECT_NAME, gcs_bucket_qualified_name=gcs_bucket.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=GCSObject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=GCSObject)


def test_gcs_object(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object: GCSObject,
):
    assert gcs_object
    assert gcs_object.guid
    assert gcs_object.qualified_name
    assert gcs_object.gcs_bucket_qualified_name == gcs_bucket.qualified_name
    assert gcs_object.name == GCS_OBJECT_NAME
    assert gcs_object.connector_name == AtlanConnectorType.GCS.value


@pytest.fixture(scope="module")
def gcs_object_overload(
    client: AtlanClient, connection: Connection, gcs_bucket: GCSBucket
) -> Generator[GCSObject, None, None]:
    assert gcs_bucket.qualified_name
    assert connection.qualified_name
    to_create = GCSObject.creator(
        name=GCS_OBJECT_NAME_OVERLOAD,
        gcs_bucket_qualified_name=gcs_bucket.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=GCSObject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=GCSObject)


def test_overload_gcs_object(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object_overload: GCSObject,
):
    assert gcs_object_overload
    assert gcs_object_overload.guid
    assert gcs_object_overload.qualified_name
    assert gcs_object_overload.gcs_bucket_qualified_name == gcs_bucket.qualified_name
    assert gcs_object_overload.name == GCS_OBJECT_NAME_OVERLOAD
    assert gcs_object_overload.connector_name == AtlanConnectorType.GCS.value


def test_update_gcs_object(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object: GCSObject,
):
    assert gcs_object.qualified_name
    assert gcs_object.name
    updated = client.asset.update_certificate(
        asset_type=GCSObject,
        qualified_name=gcs_object.qualified_name,
        name=GCS_OBJECT_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert gcs_object.qualified_name
    assert gcs_object.name
    updated = client.asset.update_announcement(
        asset_type=GCSObject,
        qualified_name=gcs_object.qualified_name,
        name=GCS_OBJECT_NAME,
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


@pytest.mark.order(after="test_update_gcs_object")
def test_retrieve_gcs_object(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object: GCSObject,
):
    b = client.asset.get_by_guid(gcs_object.guid, asset_type=GCSObject)
    assert b
    assert not b.is_incomplete
    assert b.guid == gcs_object.guid
    assert b.qualified_name == gcs_object.qualified_name
    assert b.name == GCS_OBJECT_NAME
    assert b.connector_name == AtlanConnectorType.GCS.value
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_gcs_object")
def test_update_gcs_object_again(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object: GCSObject,
):
    assert gcs_object.qualified_name
    assert gcs_object.name
    updated = client.asset.remove_certificate(
        asset_type=GCSObject,
        qualified_name=gcs_object.qualified_name,
        name=gcs_object.name,
    )
    assert updated
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert gcs_object.qualified_name
    updated = client.asset.remove_announcement(
        qualified_name=gcs_object.qualified_name,
        asset_type=GCSObject,
        name=gcs_object.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_gcs_object_again")
def test_delete_gcs_object(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object: GCSObject,
):
    response = client.asset.delete_by_guid(gcs_object.guid)
    assert response
    assert not response.assets_created(asset_type=GCSObject)
    assert not response.assets_updated(asset_type=GCSObject)
    deleted = response.assets_deleted(asset_type=GCSObject)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == gcs_object.guid
    assert deleted[0].qualified_name == gcs_object.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_gcs_object")
def test_read_deleted_gcs_object(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object: GCSObject,
):
    deleted = client.asset.get_by_guid(gcs_object.guid, asset_type=GCSObject)
    assert deleted
    assert deleted.guid == gcs_object.guid
    assert deleted.qualified_name == gcs_object.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_gcs_object")
def test_restore_object(
    client: AtlanClient,
    connection: Connection,
    gcs_bucket: GCSBucket,
    gcs_object: GCSObject,
):
    assert gcs_object.qualified_name
    assert client.asset.restore(
        asset_type=GCSObject, qualified_name=gcs_object.qualified_name
    )
    assert gcs_object.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=GCSObject, qualified_name=gcs_object.qualified_name
    )
    assert restored
    assert restored.guid == gcs_object.guid
    assert restored.qualified_name == gcs_object.qualified_name
    assert restored.status == EntityStatus.ACTIVE
