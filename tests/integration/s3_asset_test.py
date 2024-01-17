# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, S3Bucket, S3Object
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

MODULE_NAME = TestId.make_unique("S3")

CONNECTOR_TYPE = AtlanConnectorType.S3
ARN = "arn:aws:s3:::"
BUCKET_NAME = MODULE_NAME
BUCKET_ARN = f"{ARN}{MODULE_NAME}"
OBJECT_NAME = f"myobject_{MODULE_NAME}.csv"
OBJECT_ARN = f"{ARN}{BUCKET_NAME}/prefix/{OBJECT_NAME}"
OBJECT_PREFIX = "/some/folder/structure"
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
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=S3Bucket)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Bucket)


@pytest.fixture(scope="module")
def bucket_with_name(
    client: AtlanClient, connection: Connection
) -> Generator[S3Bucket, None, None]:
    assert connection.qualified_name
    to_create = S3Bucket.create(
        name=BUCKET_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=S3Bucket)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Bucket)


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
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=S3Object)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Object)


@pytest.fixture(scope="module")
def s3object_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
) -> Generator[S3Object, None, None]:
    assert connection.qualified_name
    assert bucket_with_name.qualified_name
    to_create = S3Object.create_with_prefix(
        name=OBJECT_NAME,
        connection_qualified_name=connection.qualified_name,
        prefix=OBJECT_PREFIX,
        s3_bucket_qualified_name=bucket_with_name.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=S3Object)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Object)


def _assert_bucket(bucket, with_name=False):
    assert bucket
    assert bucket.guid
    assert bucket.qualified_name
    assert bucket.name == BUCKET_NAME
    assert bucket.connector_name == AtlanConnectorType.S3.value
    if with_name:
        assert bucket.aws_arn is None
    else:
        assert bucket.aws_arn == BUCKET_ARN


def _assert_object(s3object, bucket, with_name=False):
    assert s3object
    assert s3object.guid
    assert s3object.qualified_name
    assert s3object.name == OBJECT_NAME
    assert s3object.connector_name == AtlanConnectorType.S3.value
    assert s3object.s3_bucket_qualified_name == bucket.qualified_name
    if with_name:
        assert s3object.aws_arn is None
        assert s3object.s3_object_key == f"{OBJECT_PREFIX}/{OBJECT_NAME}"
    else:
        assert s3object.aws_arn == OBJECT_ARN
        assert s3object.s3_object_key is None


def _assert_update_bucket(client, bucket, with_name=False):
    assert bucket.qualified_name
    assert bucket.name
    updated = client.asset.update_certificate(
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
    updated = client.asset.update_announcement(
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
    if with_name:
        assert bucket.aws_arn is None
    else:
        assert bucket.aws_arn == BUCKET_ARN


def _assert_retrieve_bucket(client, bucket, s3object, with_name=False):
    b = client.asset.get_by_guid(bucket.guid, asset_type=S3Bucket)
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
    if with_name:
        assert b.aws_arn is None
    else:
        assert b.aws_arn == BUCKET_ARN


def _assert_update_bucket_again(client, bucket, with_name=False):
    assert bucket.qualified_name
    assert bucket.name
    updated = client.asset.remove_certificate(
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
    updated = client.asset.remove_announcement(
        qualified_name=bucket.qualified_name,
        asset_type=S3Bucket,
        name=bucket.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message
    if with_name:
        assert bucket.aws_arn is None
    else:
        assert bucket.aws_arn == BUCKET_ARN


def _assert_delete_object(client, s3object):
    response = client.asset.delete_by_guid(s3object.guid)
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


def _assert_read_delete_object(client, s3object):
    deleted = client.asset.get_by_guid(s3object.guid, asset_type=S3Object)
    assert deleted
    assert deleted.guid == s3object.guid
    assert deleted.qualified_name == s3object.qualified_name
    assert deleted.status == EntityStatus.DELETED


def _assert_restore_object(client, s3object):
    assert s3object.qualified_name
    assert client.asset.restore(
        asset_type=S3Object, qualified_name=s3object.qualified_name
    )
    assert s3object.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=S3Object, qualified_name=s3object.qualified_name
    )
    assert restored
    assert restored.guid == s3object.guid
    assert restored.qualified_name == s3object.qualified_name
    assert restored.status == EntityStatus.ACTIVE


def test_bucket(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
):
    _assert_bucket(bucket)


def test_bucket_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
):
    _assert_bucket(bucket_with_name, True)


def test_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    _assert_object(s3object, bucket)


def test_object_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
    s3object_with_name: S3Object,
):
    _assert_object(s3object_with_name, bucket_with_name, True)


def test_update_bucket(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    _assert_update_bucket(client, bucket)


def test_update_bucket_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
    s3object_with_name: S3Object,
):
    _assert_update_bucket(client, bucket_with_name, True)


@pytest.mark.order(after="test_update_bucket")
def test_retrieve_bucket(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    _assert_retrieve_bucket(client, bucket, s3object)


@pytest.mark.order(after="test_update_bucket_with_name")
def test_retrieve_bucket_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
    s3object_with_name: S3Object,
):
    _assert_retrieve_bucket(
        client, bucket_with_name, s3object_with_name, with_name=True
    )


@pytest.mark.order(after="test_retrieve_bucket")
def test_update_bucket_again(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    _assert_update_bucket_again(client, bucket)


@pytest.mark.order(after="test_retrieve_bucket_with_name")
def test_update_bucket_with_name_again(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
    s3object_with_name: S3Object,
):
    _assert_update_bucket_again(client, bucket_with_name, True)


@pytest.mark.order(after="test_update_bucket_again")
def test_delete_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    _assert_delete_object(client, s3object)


@pytest.mark.order(after="test_update_bucket_with_name_again")
def test_delete_object_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
    s3object_with_name: S3Object,
):
    _assert_delete_object(client, s3object_with_name)


@pytest.mark.order(after="test_delete_object")
def test_read_deleted_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    _assert_read_delete_object(client, s3object)


@pytest.mark.order(after="test_delete_object_with_name")
def test_read_deleted_object_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
    s3object_with_name: S3Object,
):
    _assert_read_delete_object(client, s3object_with_name)


@pytest.mark.order(after="test_read_deleted_object")
def test_restore_object(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    s3object: S3Object,
):
    _assert_restore_object(client, s3object)


@pytest.mark.order(after="test_read_deleted_object_with_name")
def test_restore_object_with_name(
    client: AtlanClient,
    connection: Connection,
    bucket_with_name: S3Bucket,
    s3object_with_name: S3Object,
):
    _assert_restore_object(client, s3object_with_name)
