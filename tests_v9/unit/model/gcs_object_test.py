# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for GCSObject model in pyatlan_v9."""

import pytest

from pyatlan.model.utils import construct_object_key
from pyatlan_v9.models import GCSObject
from tests_v9.unit.model.constants import (
    GCS_BUCKET_NAME,
    GCS_BUCKET_QUALIFIED_NAME,
    GCS_CONNECTION_QUALIFIED_NAME,
    GCS_OBJECT_NAME,
    GCS_OBJECT_PREFIX,
    GCS_OBJECT_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, gcs_bucket_name, gcs_bucket_qualified_name, message",
    [
        (None, GCS_BUCKET_NAME, "object/name/qn", "name is required"),
        (GCS_OBJECT_NAME, None, "object/name/qn", "gcs_bucket_name is required"),
        (
            GCS_OBJECT_NAME,
            GCS_BUCKET_NAME,
            None,
            "gcs_bucket_qualified_name is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, gcs_bucket_name: str, gcs_bucket_qualified_name: str, message: str
):
    """Test creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        GCSObject.creator(
            name=name,
            gcs_bucket_name=gcs_bucket_name,
            gcs_bucket_qualified_name=gcs_bucket_qualified_name,
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, prefix, gcs_bucket_name, gcs_bucket_qualified_name, msg",
    [
        (
            None,
            GCS_CONNECTION_QUALIFIED_NAME,
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "name is required",
        ),
        (
            GCS_OBJECT_NAME,
            None,
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "connection_qualified_name is required",
        ),
        (
            "",
            GCS_CONNECTION_QUALIFIED_NAME,
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            GCS_OBJECT_NAME,
            "",
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "connection_qualified_name cannot be blank",
        ),
        (
            GCS_OBJECT_NAME,
            "default/gcs/",
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            GCS_OBJECT_NAME,
            "/gcs/",
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            GCS_OBJECT_NAME,
            "default/gcs/production/TestDb",
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            GCS_OBJECT_NAME,
            "gcs/production",
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            GCS_OBJECT_NAME,
            "default/gcs-invalid/production",
            "abc",
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
            "Invalid connection_qualified_name",
        ),
        (
            GCS_OBJECT_NAME,
            GCS_CONNECTION_QUALIFIED_NAME,
            "abc",
            None,
            GCS_BUCKET_QUALIFIED_NAME,
            "gcs_bucket_name is required",
        ),
        (
            GCS_OBJECT_NAME,
            GCS_CONNECTION_QUALIFIED_NAME,
            "abc",
            "",
            GCS_BUCKET_QUALIFIED_NAME,
            "gcs_bucket_name cannot be blank",
        ),
        (
            GCS_OBJECT_NAME,
            GCS_CONNECTION_QUALIFIED_NAME,
            "abc",
            GCS_BUCKET_NAME,
            None,
            "gcs_bucket_qualified_name is required",
        ),
        (
            GCS_OBJECT_NAME,
            GCS_CONNECTION_QUALIFIED_NAME,
            "abc",
            GCS_BUCKET_NAME,
            "",
            "gcs_bucket_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_with_prefix_without_required_parameters_raises_validation_error(
    name,
    connection_qualified_name,
    prefix,
    gcs_bucket_name,
    gcs_bucket_qualified_name,
    msg,
):
    """Test creator_with_prefix validation for missing or invalid parameters."""
    with pytest.raises(ValueError, match=msg):
        GCSObject.creator_with_prefix(
            name=name,
            connection_qualified_name=connection_qualified_name,
            gcs_bucket_name=gcs_bucket_name,
            gcs_bucket_qualified_name=gcs_bucket_qualified_name,
            prefix=prefix,
        )


def test_creator():
    """Test creator derives qualified name and connection values."""
    sut = GCSObject.creator(
        name=GCS_OBJECT_NAME,
        gcs_bucket_name=GCS_BUCKET_NAME,
        gcs_bucket_qualified_name=GCS_BUCKET_QUALIFIED_NAME,
    )

    assert sut.name == GCS_OBJECT_NAME
    assert sut.gcs_bucket_qualified_name == GCS_BUCKET_QUALIFIED_NAME
    assert sut.qualified_name == GCS_OBJECT_QUALIFIED_NAME
    assert sut.connection_qualified_name == GCS_CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "name, connection_qualified_name, prefix, gcs_bucket_name, gcs_bucket_qualified_name",
    [
        (
            GCS_OBJECT_NAME,
            GCS_CONNECTION_QUALIFIED_NAME,
            GCS_OBJECT_PREFIX,
            GCS_BUCKET_NAME,
            GCS_BUCKET_QUALIFIED_NAME,
        ),
    ],
)
def test_creator_with_prefix(
    name, connection_qualified_name, prefix, gcs_bucket_name, gcs_bucket_qualified_name
):
    """Test creator_with_prefix computes object key and qualified name."""
    attributes = GCSObject.creator_with_prefix(
        name=name,
        connection_qualified_name=connection_qualified_name,
        gcs_bucket_name=gcs_bucket_name,
        gcs_bucket_qualified_name=gcs_bucket_qualified_name,
        prefix=prefix,
    )
    assert attributes.name == name
    assert attributes.connection_qualified_name == connection_qualified_name
    object_key = construct_object_key(prefix, name)
    assert attributes.gcs_object_key == object_key
    assert (
        attributes.qualified_name
        == f"{connection_qualified_name}/{attributes.gcs_bucket_name}/{object_key}"
    )
    assert attributes.connector_name == connection_qualified_name.split("/")[1]
    assert attributes.gcs_bucket_qualified_name == gcs_bucket_qualified_name


def test_overload_creator():
    """Test creator accepts explicit connection_qualified_name override."""
    sut = GCSObject.creator(
        name=GCS_OBJECT_NAME,
        gcs_bucket_name=GCS_BUCKET_NAME,
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
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        GCSObject.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater returns minimal update payload."""
    sut = GCSObject.updater(
        qualified_name=GCS_OBJECT_QUALIFIED_NAME, name=GCS_OBJECT_NAME
    )

    assert sut.qualified_name == GCS_OBJECT_QUALIFIED_NAME
    assert sut.name == GCS_OBJECT_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only required fields for updates."""
    sut = GCSObject.creator(
        name=GCS_OBJECT_NAME,
        gcs_bucket_name=GCS_BUCKET_NAME,
        gcs_bucket_qualified_name=GCS_BUCKET_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.name == GCS_OBJECT_NAME
    assert sut.qualified_name == GCS_OBJECT_QUALIFIED_NAME
