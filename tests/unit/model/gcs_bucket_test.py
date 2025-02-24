import pytest

from pyatlan.model.assets import GCSBucket
from tests.unit.model.constants import (
    GCS_BUCKET_NAME,
    GCS_CONNECTION_QUALIFIED_NAME,
    GCS_CONNECTOR_TYPE,
    GCS_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (GCS_BUCKET_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        GCSBucket.create(name=name, connection_qualified_name=connection_qualified_name)


def test_create():
    sut = GCSBucket.create(
        name=GCS_BUCKET_NAME, connection_qualified_name=GCS_CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == GCS_BUCKET_NAME
    assert sut.connection_qualified_name == GCS_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == GCS_QUALIFIED_NAME
    assert sut.connector_name == GCS_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, GCS_QUALIFIED_NAME, "qualified_name is required"),
        (GCS_BUCKET_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        GCSBucket.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = GCSBucket.create_for_modification(
        qualified_name=GCS_QUALIFIED_NAME, name=GCS_BUCKET_NAME
    )

    assert sut.qualified_name == GCS_QUALIFIED_NAME
    assert sut.name == GCS_BUCKET_NAME


def test_trim_to_required():
    sut = GCSBucket.create(
        name=GCS_BUCKET_NAME, connection_qualified_name=GCS_CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == GCS_BUCKET_NAME
    assert sut.qualified_name == GCS_QUALIFIED_NAME
