# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, S3Bucket
from pyatlan.model.enums import AtlanConnectorType
from tests.integration.client import delete_asset
from tests.integration.connection_test import create_connection

PREFIX = "psdk"
S3_PREFIX = f"{PREFIX}-S3"

CONNECTOR_TYPE = AtlanConnectorType.S3
CONNECTION_NAME = S3_PREFIX

BUCKET_NAME = "mybucket"
BUCKET_ARN = f"{PREFIX}arn:aws:s3:::mybucket"
OBJECT_NAME = "myobject.csv"
OBJECT_ARN = f"{PREFIX}arn:aws:s3:::mybucket/prefix/myobject.csv"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=CONNECTION_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def bucket(
    client: AtlanClient, connection: Connection
) -> Generator[S3Bucket, None, None]:
    to_create = S3Bucket.create(
        name=BUCKET_NAME,
        connection_qualified_name=connection.qualified_name,
        aws_arn=BUCKET_ARN,
    )
    response = client.upsert(to_create)
    result = response.assets_created(asset_type=S3Bucket)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Bucket)


def test_bucket(client: AtlanClient, connection: Connection, bucket: S3Bucket):
    assert bucket
    assert bucket.guid
    assert bucket.qualified_name
    assert bucket.name == BUCKET_NAME
    assert bucket.aws_arn == BUCKET_ARN
    assert bucket.connector_name == AtlanConnectorType.S3.value
