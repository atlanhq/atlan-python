# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.error import AtlanError, NotFoundError
from pyatlan.model.assets import Asset, Connection, S3Bucket, S3Object
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

MODULE_NAME = TestId.make_unique("S3")

CONNECTOR_TYPE = AtlanConnectorType.S3
ARN = "arn:aws:s3:::"
BUCKET_NAME = MODULE_NAME
BUCKET_ARN = f"{ARN}{MODULE_NAME}"
OBJECT_NAME = f"myobject_{MODULE_NAME}.csv"
OBJECT_ARN = f"{ARN}{BUCKET_NAME}/prefix/{OBJECT_NAME}"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


def block(
    client: AtlanClient, response: AssetMutationResponse
) -> AssetMutationResponse:
    if response.mutated_entities and response.mutated_entities.DELETE:
        _retrieve_and_check(client, response.mutated_entities.DELETE, 0)
    return response


def _retrieve_and_check(client: AtlanClient, to_check: list[Asset], retry_count: int):
    leftovers = []
    for one in to_check:
        try:
            candidate = client.get_asset_by_guid(one.guid, asset_type=type(one))
            if candidate and candidate.status == EntityStatus.ACTIVE:
                leftovers.append(candidate)
        except NotFoundError:
            # If it is not found, it was successfully deleted (purged), so we
            # do not need to look for it any further
            print("Asset no longer exists.")
        except AtlanError:
            leftovers.append(one)
    if leftovers:
        if retry_count == 20:
            raise AtlanError(message="Overran retry limit", code="500", status_code=500)
        time.sleep(2)
        _retrieve_and_check(client, leftovers, retry_count + 1)


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def bucket(
    client: AtlanClient, connection: Connection
) -> Generator[S3Bucket, None, None]:
    assert connection.qualified_name
    to_create = S3Bucket.create(
        name=BUCKET_NAME,
        connection_qualified_name=connection.qualified_name,
        aws_arn=BUCKET_ARN,
    )
    response = client.save(to_create)
    result = response.assets_created(asset_type=S3Bucket)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Bucket)


def test_bucket(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
):
    assert bucket
    assert bucket.guid
    assert bucket.qualified_name
    assert bucket.name == BUCKET_NAME
    assert bucket.aws_arn == BUCKET_ARN
    assert bucket.connector_name == AtlanConnectorType.S3.value


@pytest.fixture(scope="module")
def s3object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
) -> Generator[S3Object, None, None]:
    assert connection.qualified_name
    assert bucket.qualified_name
    to_create = S3Object.create(
        name=OBJECT_NAME,
        connection_qualified_name=connection.qualified_name,
        aws_arn=OBJECT_ARN,
        s3_bucket_qualified_name=bucket.qualified_name,
    )
    response = client.save(to_create)
    result = response.assets_created(asset_type=S3Object)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Object)


def test_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    assert s3object
    assert s3object.guid
    assert s3object.qualified_name
    assert s3object.name == OBJECT_NAME
    assert s3object.aws_arn == OBJECT_ARN
    assert s3object.connector_name == AtlanConnectorType.S3.value


def test_update_bucket(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    assert bucket.qualified_name
    assert bucket.name
    updated = client.update_certificate(
        asset_type=S3Bucket,
        qualified_name=bucket.qualified_name,
        name=bucket.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status == CERTIFICATE_STATUS
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert bucket.qualified_name
    assert bucket.name
    updated = client.update_announcement(
        asset_type=S3Bucket,
        qualified_name=bucket.qualified_name,
        name=bucket.name,
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


@pytest.mark.order(after="test_update_bucket")
def test_retrieve_bucket(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    b = client.get_asset_by_guid(bucket.guid, asset_type=S3Bucket)
    assert b
    assert not b.is_incomplete
    assert b.guid == bucket.guid
    assert b.qualified_name == bucket.qualified_name
    assert b.name == BUCKET_NAME
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE
    assert b.objects
    assert len(b.objects) == 1
    assert isinstance(b.objects[0], S3Object)
    assert b.objects[0].guid == s3object.guid


@pytest.mark.order(after="test_retrieve_bucket")
def test_update_bucket_again(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    assert bucket.qualified_name
    assert bucket.name
    updated = client.remove_certificate(
        qualified_name=bucket.qualified_name,
        asset_type=S3Bucket,
        name=bucket.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert bucket.qualified_name
    updated = client.remove_announcement(
        qualified_name=bucket.qualified_name,
        asset_type=S3Bucket,
        name=bucket.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_bucket_again")
def test_delete_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    response = client.delete_entity_by_guid(s3object.guid)
    response = block(client, response)
    assert response
    assert not response.assets_created(asset_type=S3Object)
    assert not response.assets_updated(asset_type=S3Object)
    deleted = response.assets_deleted(asset_type=S3Object)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == s3object.guid
    assert deleted[0].qualified_name == s3object.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_object")
def test_read_deleted_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    deleted = client.get_asset_by_guid(s3object.guid, asset_type=S3Object)
    assert deleted
    assert deleted.guid == s3object.guid
    assert deleted.qualified_name == s3object.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_object")
def test_restore_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    assert s3object.qualified_name
    assert client.restore(asset_type=S3Object, qualified_name=s3object.qualified_name)
    assert s3object.qualified_name
    restored = client.get_asset_by_qualified_name(
        asset_type=S3Object, qualified_name=s3object.qualified_name
    )
    assert restored
    assert restored.guid == s3object.guid
    assert restored.qualified_name == s3object.qualified_name
    assert restored.status == EntityStatus.ACTIVE
