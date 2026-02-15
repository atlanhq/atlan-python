# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for GCSBucket model in pyatlan_v9."""

import pytest

from pyatlan_v9.models import GCSBucket
from tests_v9.unit.model.constants import (
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
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        GCSBucket.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator populates derived fields for a GCSBucket."""
    sut = GCSBucket.creator(
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
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        GCSBucket.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a GCSBucket instance for modification."""
    sut = GCSBucket.updater(qualified_name=GCS_QUALIFIED_NAME, name=GCS_BUCKET_NAME)

    assert sut.qualified_name == GCS_QUALIFIED_NAME
    assert sut.name == GCS_BUCKET_NAME


def test_trim_to_required():
    """Test trim_to_required returns a GCSBucket with only required fields."""
    sut = GCSBucket.creator(
        name=GCS_BUCKET_NAME, connection_qualified_name=GCS_CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == GCS_BUCKET_NAME
    assert sut.qualified_name == GCS_QUALIFIED_NAME
