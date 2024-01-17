import pytest

from pyatlan.model.assets import S3Bucket
from tests.unit.model.constants import (
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
    with pytest.raises(ValueError, match=msg):
        S3Bucket.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )


def test_create_with_required_parameters():
    attributes = S3Bucket.create(
        name=BUCKET_NAME,
        connection_qualified_name=S3_CONNECTION_QUALIFIED_NAME,
    )
    assert attributes.name == BUCKET_NAME
    assert attributes.aws_arn is None
    assert attributes.connection_qualified_name == S3_CONNECTION_QUALIFIED_NAME
    assert attributes.qualified_name == BUCKET_WITH_NAME_QUALIFIED_NAME
    assert attributes.connector_name == S3_CONNECTION_QUALIFIED_NAME.split("/")[1]


def test_create_with_aws_arn():
    attributes = S3Bucket.create(
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
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        S3Bucket.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = S3Bucket.create_for_modification(
        qualified_name=S3_OBJECT_QUALIFIED_NAME, name=BUCKET_NAME
    )

    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == BUCKET_NAME


def test_trim_to_required():
    sut = S3Bucket.create_for_modification(
        qualified_name=S3_OBJECT_QUALIFIED_NAME, name=BUCKET_NAME
    ).trim_to_required()

    assert sut.qualified_name == S3_OBJECT_QUALIFIED_NAME
    assert sut.name == BUCKET_NAME
