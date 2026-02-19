# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for S3Object model in pyatlan_v9."""

import pytest
from msgspec import UNSET

from pyatlan.model.utils import construct_object_key
from pyatlan_v9.model import S3Object
from tests_v9.unit.model.constants import (
    AWS_ARN,
    BUCKET_NAME,
    BUCKET_QUALIFIED_NAME,
    S3_CONNECTION_QUALIFIED_NAME,
    S3_OBJECT_NAME,
    S3_OBJECT_PREFIX,
    S3_OBJECT_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn, s3_bucket_name, s3_bucket_qualified_name, msg",
    [
        (
            None,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "name is required",
        ),
        (
            S3_OBJECT_NAME,
            None,
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name is required",
        ),
        (
            "",
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "/s3/",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/production/TestDb",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "s3/production",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s33/production",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3",
            None,
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "aws_arn is required",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3",
            "",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "aws_arn cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            None,
            BUCKET_QUALIFIED_NAME,
            "s3_bucket_name is required",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            "",
            BUCKET_QUALIFIED_NAME,
            "s3_bucket_name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            None,
            "s3_bucket_qualified_name is required",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            "",
            "s3_bucket_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_without_required_parameters_raises_validation_error(
    name,
    connection_qualified_name,
    aws_arn,
    s3_bucket_name,
    s3_bucket_qualified_name,
    msg,
):
    """Test creator validation for missing and malformed parameters."""
    with pytest.raises(ValueError, match=msg):
        S3Object.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
            s3_bucket_name=s3_bucket_name,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, prefix, s3_bucket_name, s3_bucket_qualified_name, msg",
    [
        (
            None,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "name is required",
        ),
        (
            S3_OBJECT_NAME,
            None,
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name is required",
        ),
        (
            "",
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "/s3/",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/production/TestDb",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "s3/production",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s33/production",
            "abc",
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            None,
            BUCKET_QUALIFIED_NAME,
            "s3_bucket_name is required",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            "",
            BUCKET_QUALIFIED_NAME,
            "s3_bucket_name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            None,
            "s3_bucket_qualified_name is required",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_NAME,
            "",
            "s3_bucket_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_with_prefix_without_required_parameters_raises_validation_error(
    name,
    connection_qualified_name,
    prefix,
    s3_bucket_name,
    s3_bucket_qualified_name,
    msg,
):
    """Test creator_with_prefix validation for missing and malformed parameters."""
    with pytest.raises(ValueError, match=msg):
        S3Object.creator_with_prefix(
            name=name,
            connection_qualified_name=connection_qualified_name,
            prefix=prefix,
            s3_bucket_name=s3_bucket_name,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn, s3_bucket_name, s3_bucket_qualified_name",
    [
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            AWS_ARN,
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
        ),
    ],
)
def test_creator_with_required_parameters(
    name, connection_qualified_name, aws_arn, s3_bucket_name, s3_bucket_qualified_name
):
    """Test creator builds expected qualified name and connector metadata."""
    attributes = S3Object.creator(
        name=name,
        connection_qualified_name=connection_qualified_name,
        aws_arn=aws_arn,
        s3_bucket_name=s3_bucket_name,
        s3_bucket_qualified_name=s3_bucket_qualified_name,
    )
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.aws_arn == aws_arn
    assert attributes.qualified_name == f"{connection_qualified_name}/{aws_arn}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
    assert attributes.s3_bucket_name == s3_bucket_name
    assert attributes.s3_bucket_qualified_name == s3_bucket_qualified_name


@pytest.mark.parametrize(
    "name, connection_qualified_name, prefix, s3_bucket_name, s3_bucket_qualified_name",
    [
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            S3_OBJECT_PREFIX,
            BUCKET_NAME,
            BUCKET_QUALIFIED_NAME,
        ),
    ],
)
def test_creator_with_prefix(
    name, connection_qualified_name, prefix, s3_bucket_name, s3_bucket_qualified_name
):
    """Test creator_with_prefix derives object-key based qualified name."""
    attributes = S3Object.creator_with_prefix(
        name=name,
        connection_qualified_name=connection_qualified_name,
        prefix=prefix,
        s3_bucket_name=s3_bucket_name,
        s3_bucket_qualified_name=s3_bucket_qualified_name,
    )
    object_key = f"{prefix}/{name}"
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.aws_arn is UNSET
    assert attributes.s3_object_key == construct_object_key(prefix, name)
    assert (
        attributes.qualified_name
        == f"{connection_qualified_name}/{attributes.s3_bucket_name}/{object_key}"
    )
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
    assert attributes.s3_bucket_qualified_name == s3_bucket_qualified_name


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, S3_OBJECT_QUALIFIED_NAME, "qualified_name is required"),
        (S3_OBJECT_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validation for required parameters."""
    with pytest.raises(ValueError, match=message):
        S3Object.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater returns minimal update instance."""
    sut = S3Object.updater(qualified_name=S3_OBJECT_QUALIFIED_NAME, name=S3_OBJECT_NAME)
    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == S3_OBJECT_NAME


def test_trim_to_required():
    """Test trim_to_required keeps qualified_name and name."""
    sut = S3Object.updater(
        qualified_name=S3_OBJECT_QUALIFIED_NAME, name=S3_OBJECT_NAME
    ).trim_to_required()
    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == S3_OBJECT_NAME
