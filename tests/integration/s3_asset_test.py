# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Callable, Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, S3Bucket
from pyatlan.model.enums import AtlanConnectorType
from tests.integration.client import delete_asset
from tests.integration.connection_test import create_connection

MODULE_NAME = "S3"
CONNECTOR_TYPE = AtlanConnectorType.S3
ARN = "arn:aws:s3:::"


@pytest.fixture(scope="module")
def connection(
    client: AtlanClient, make_unique: Callable[[str], str]
) -> Generator[Connection, None, None]:
    connection_name = make_unique(MODULE_NAME)
    result = create_connection(
        client=client, name=connection_name, connector_type=CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def bucket(
    client: AtlanClient, connection: Connection, make_unique: Callable[[str], str]
) -> Generator[S3Bucket, None, None]:
    bucket_name = make_unique(MODULE_NAME)
    bucket_arn = make_unique(ARN + MODULE_NAME)
    to_create = S3Bucket.create(
        name=bucket_name,
        connection_qualified_name=connection.qualified_name,
        aws_arn=bucket_arn,
    )
    response = client.upsert(to_create)
    result = response.assets_created(asset_type=S3Bucket)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=S3Bucket)


def test_bucket(
    client: AtlanClient,
    connection: Connection,
    bucket: S3Bucket,
    make_unique: Callable[[str], str],
):
    assert bucket
    assert bucket.guid
    assert bucket.qualified_name
    assert bucket.name == make_unique(MODULE_NAME)
    assert bucket.aws_arn == make_unique(ARN + MODULE_NAME)
    assert bucket.connector_name == AtlanConnectorType.S3.value
