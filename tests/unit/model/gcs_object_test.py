import pytest

from pyatlan.model.assets import GCSObject
from tests.unit.model.constants import (
    GCS_BUCKET_QUALIFIED_NAME,
    GCS_CONNECTION_QUALIFIED_NAME,
    GCS_OBJECT_NAME,
    GCS_OBJECT_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, gcs_bucket_qualified_name, message",
    [
        (None, "bucket/name", "name is required"),
        (GCS_OBJECT_NAME, None, "gcs_bucket_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, gcs_bucket_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        GCSObject.create(name=name, gcs_bucket_qualified_name=gcs_bucket_qualified_name)


def test_create():
    sut = GCSObject.create(
        name=GCS_OBJECT_NAME, gcs_bucket_qualified_name=GCS_BUCKET_QUALIFIED_NAME
    )

    assert sut.name == GCS_OBJECT_NAME
    assert sut.gcs_bucket_qualified_name == GCS_BUCKET_QUALIFIED_NAME
    assert sut.qualified_name == GCS_OBJECT_QUALIFIED_NAME
    assert sut.connection_qualified_name == GCS_CONNECTION_QUALIFIED_NAME


def test_overload_creator():
    sut = GCSObject.creator(
        name=GCS_OBJECT_NAME,
        gcs_bucket_qualified_name=GCS_BUCKET_QUALIFIED_NAME,
        connection_qualified_name=GCS_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == GCS_OBJECT_NAME
    assert sut.gcs_bucket_qualified_name == GCS_BUCKET_QUALIFIED_NAME
    assert sut.qualified_name == GCS_OBJECT_QUALIFIED_NAME
    assert sut.connection_qualified_name == GCS_CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, GCS_OBJECT_QUALIFIED_NAME, "qualified_name is required"),
        (GCS_OBJECT_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        GCSObject.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = GCSObject.create_for_modification(
        qualified_name=GCS_OBJECT_QUALIFIED_NAME, name=GCS_OBJECT_NAME
    )

    assert sut.qualified_name == GCS_OBJECT_QUALIFIED_NAME
    assert sut.name == GCS_OBJECT_NAME


def test_trim_to_required():
    sut = GCSObject.create(
        name=GCS_OBJECT_NAME, gcs_bucket_qualified_name=GCS_BUCKET_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == GCS_OBJECT_NAME
    assert sut.qualified_name == GCS_OBJECT_QUALIFIED_NAME
