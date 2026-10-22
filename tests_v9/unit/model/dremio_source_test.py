# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DremioSource model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-dremio-app emits today
(``{connection_qn}/{name}``, the source's Dremio path under the connection), so
a creator change that would re-key existing sources fails here.
"""

import pytest

from pyatlan_v9.model import DremioSource

CONNECTION_QUALIFIED_NAME = "default/dremio/1700000000"
SOURCE_NAME = "sales-lake"
SOURCE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{SOURCE_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-dremio-app's map_source inputs and output."""
    sut = DremioSource.creator(
        name="sales-lake", connection_qualified_name="default/dremio/1700000000"
    )

    assert sut.qualified_name == "default/dremio/1700000000/sales-lake"
    assert sut.dremio_source_qualified_name == "default/dremio/1700000000/sales-lake"
    assert sut.dremio_source_name == "sales-lake"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (SOURCE_NAME, None, "connection_qualified_name is required"),
        (SOURCE_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DremioSource.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator sets the connection and the denormalised source attributes."""
    sut = DremioSource.creator(
        name=SOURCE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == SOURCE_NAME
    assert sut.qualified_name == SOURCE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "dremio"
    assert sut.dremio_source_qualified_name == SOURCE_QUALIFIED_NAME
    assert sut.dremio_source_name == SOURCE_NAME


def test_validate_rejects_qualified_name_without_path():
    """Test validate enforces the {connection_qn}/{name} pattern."""
    sut = DremioSource.creator(
        name=SOURCE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )
    sut.qualified_name = SOURCE_NAME

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SOURCE_NAME, "qualified_name is required"),
        (SOURCE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DremioSource.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DremioSource for modification."""
    sut = DremioSource.updater(qualified_name=SOURCE_QUALIFIED_NAME, name=SOURCE_NAME)

    assert sut.qualified_name == SOURCE_QUALIFIED_NAME
    assert sut.name == SOURCE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DremioSource.updater(
        qualified_name=SOURCE_QUALIFIED_NAME, name=SOURCE_NAME
    ).trim_to_required()

    assert sut.qualified_name == SOURCE_QUALIFIED_NAME
    assert sut.name == SOURCE_NAME
