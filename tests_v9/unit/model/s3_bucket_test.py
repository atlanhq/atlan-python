# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for S3Bucket model in pyatlan_v9 - exact parity with tests/unit/model/s3_bucket_test.py."""

import pytest

from pyatlan_v9.model import S3Bucket
from tests_v9.unit.model.constants import (
    AWS_ARN,
    BUCKET_NAME,
    BUCKET_QUALIFIED_NAME,
    BUCKET_WITH_NAME_QUALIFIED_NAME,
    S3_CONNECTION_QUALIFIED_NAME,
    S3_OBJECT_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, msg",
    [
        (None, S3_CONNECTION_QUALIFIED_NAME, "name is required"),
        (BUCKET_NAME, None, "connection_qualified_name is required"),
        ("", S3_CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (BUCKET_NAME, "", "connection_qualified_name cannot be blank"),
        (BUCKET_NAME, "default/s3/", "Invalid connection_qualified_name"),
        (BUCKET_NAME, "/s3/", "Invalid connection_qualified_name"),
        (
            BUCKET_NAME,
            "default/s3/production/TestDb",
            "Invalid connection_qualified_name",
        ),
        (BUCKET_NAME, "s3/production", "Invalid connection_qualified_name"),
        (
            BUCKET_NAME,
            "default/s33/production",
            "Invalid connection_qualified_name",
        ),
    ],
)
def test_create_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, msg
):
    """Test that creator raises ValueError when required parameters are missing or invalid."""
    with pytest.raises(ValueError, match=msg):
        S3Bucket.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )


def test_create_with_required_parameters():
    """Test creating S3Bucket with required parameters."""
    attributes = S3Bucket.creator(
        name=BUCKET_NAME,
        connection_qualified_name=S3_CONNECTION_QUALIFIED_NAME,
    )
    assert attributes.name == BUCKET_NAME
    assert attributes.aws_arn is None
    assert attributes.connection_qualified_name == S3_CONNECTION_QUALIFIED_NAME
    assert attributes.qualified_name == BUCKET_WITH_NAME_QUALIFIED_NAME
    assert attributes.connector_name == S3_CONNECTION_QUALIFIED_NAME.split("/")[1]


def test_create_with_aws_arn():
    """Test creating S3Bucket with AWS ARN."""
    attributes = S3Bucket.creator(
        name=BUCKET_NAME,
        connection_qualified_name=S3_CONNECTION_QUALIFIED_NAME,
        aws_arn=AWS_ARN,
    )
    assert attributes.name == BUCKET_NAME
    assert attributes.aws_arn == AWS_ARN
    assert attributes.connection_qualified_name == S3_CONNECTION_QUALIFIED_NAME
    assert attributes.qualified_name == BUCKET_QUALIFIED_NAME
    assert attributes.connector_name == S3_CONNECTION_QUALIFIED_NAME.split("/")[1]


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, S3_OBJECT_QUALIFIED_NAME, "qualified_name is required"),
        (BUCKET_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        S3Bucket.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates an S3Bucket instance for modification."""
    sut = S3Bucket.updater(qualified_name=S3_OBJECT_QUALIFIED_NAME, name=BUCKET_NAME)

    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == BUCKET_NAME


def test_trim_to_required():
    """Test that trim_to_required returns S3Bucket with only required fields."""
    sut = S3Bucket.updater(
        qualified_name=S3_OBJECT_QUALIFIED_NAME, name=BUCKET_NAME
    ).trim_to_required()

    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == BUCKET_NAME
