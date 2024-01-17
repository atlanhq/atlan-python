import pytest

from pyatlan.model.assets import S3Object
from tests.unit.model.constants import (
    AWS_ARN,
    BUCKET_NAME,
    BUCKET_QUALIFIED_NAME,
    S3_CONNECTION_QUALIFIED_NAME,
    S3_OBJECT_NAME,
    S3_OBJECT_PREFIX,
    S3_OBJECT_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn, s3_bucket_qualified_name, msg",
    [
        (
            None,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_QUALIFIED_NAME,
            "name is required",
        ),
        (
            S3_OBJECT_NAME,
            None,
            "abc",
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name is required",
        ),
        (
            "",
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "/s3/",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/production/TestDb",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "s3/production",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s33/production",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3",
            None,
            BUCKET_QUALIFIED_NAME,
            "aws_arn is required",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3",
            "",
            BUCKET_QUALIFIED_NAME,
            "aws_arn cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            None,
            "s3_bucket_qualified_name is required",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            "",
            "s3_bucket_qualified_name cannot be blank",
        ),
    ],
)
def test_create_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, aws_arn, s3_bucket_qualified_name, msg
):
    with pytest.raises(ValueError, match=msg):
        S3Object.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=aws_arn,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, prefix, s3_bucket_qualified_name, msg",
    [
        (
            None,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_QUALIFIED_NAME,
            "name is required",
        ),
        (
            S3_OBJECT_NAME,
            None,
            "abc",
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name is required",
        ),
        (
            "",
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            BUCKET_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "connection_qualified_name cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "/s3/",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3/production/TestDb",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "s3/production",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s33/production",
            "abc",
            BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3",
            None,
            BUCKET_QUALIFIED_NAME,
            "prefix is required",
        ),
        (
            S3_OBJECT_NAME,
            "default/s3",
            "",
            BUCKET_QUALIFIED_NAME,
            "prefix cannot be blank",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            None,
            "s3_bucket_qualified_name is required",
        ),
        (
            S3_OBJECT_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            "abc",
            "",
            "s3_bucket_qualified_name cannot be blank",
        ),
    ],
)
def test_create_with_prefix_without_required_parameters_raises_validation_error(
    name, connection_qualified_name, prefix, s3_bucket_qualified_name, msg
):
    with pytest.raises(ValueError, match=msg):
        S3Object.create_with_prefix(
            name=name,
            connection_qualified_name=connection_qualified_name,
            prefix=prefix,
            s3_bucket_qualified_name=s3_bucket_qualified_name,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, aws_arn, s3_bucket_qualified_name",
    [
        (
            BUCKET_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            AWS_ARN,
            BUCKET_QUALIFIED_NAME,
        ),
    ],
)
def test_create_with_required_parameters(
    name, connection_qualified_name, aws_arn, s3_bucket_qualified_name
):
    attributes = S3Object.create(
        name=name,
        connection_qualified_name=connection_qualified_name,
        aws_arn=aws_arn,
        s3_bucket_qualified_name=s3_bucket_qualified_name,
    )
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.aws_arn == aws_arn
    assert attributes.qualified_name == f"{connection_qualified_name}/{aws_arn}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
    assert attributes.s3_bucket_qualified_name == s3_bucket_qualified_name


@pytest.mark.parametrize(
    "name, connection_qualified_name, prefix, s3_bucket_qualified_name",
    [
        (
            BUCKET_NAME,
            S3_CONNECTION_QUALIFIED_NAME,
            S3_OBJECT_PREFIX,
            BUCKET_QUALIFIED_NAME,
        ),
    ],
)
def test_create_with_prefix(
    name, connection_qualified_name, prefix, s3_bucket_qualified_name
):
    attributes = S3Object.create_with_prefix(
        name=name,
        connection_qualified_name=connection_qualified_name,
        prefix=prefix,
        s3_bucket_qualified_name=s3_bucket_qualified_name,
    )
    object_key = f"{prefix}/{name}"
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    assert attributes.aws_arn is None
    assert attributes.s3_object_key == object_key
    assert attributes.qualified_name == f"{connection_qualified_name}/{object_key}"
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
    assert attributes.s3_bucket_qualified_name == s3_bucket_qualified_name


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, S3_OBJECT_QUALIFIED_NAME, "qualified_name is required"),
        (S3_OBJECT_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        S3Object.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = S3Object.create_for_modification(
        qualified_name=S3_OBJECT_QUALIFIED_NAME, name=S3_OBJECT_NAME
    )

    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == S3_OBJECT_NAME


def test_trim_to_required():
    sut = S3Object.create_for_modification(
        qualified_name=S3_OBJECT_QUALIFIED_NAME, name=S3_OBJECT_NAME
    ).trim_to_required()

    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == S3_OBJECT_NAME
