# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DremioSpace model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-dremio-app emits today
(``{connection_qn}/{name}``, the space's Dremio path under the connection), so
a creator change that would re-key existing spaces fails here.
"""

import pytest

from pyatlan_v9.model import DremioSpace

CONNECTION_QUALIFIED_NAME = "default/dremio/1700000000"
SPACE_NAME = "analytics"
SPACE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{SPACE_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-dremio-app's map_space inputs and output."""
    sut = DremioSpace.creator(
        name="analytics", connection_qualified_name="default/dremio/1700000000"
    )

    assert sut.qualified_name == "default/dremio/1700000000/analytics"
    assert sut.dremio_space_qualified_name == "default/dremio/1700000000/analytics"
    assert sut.dremio_space_name == "analytics"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (SPACE_NAME, None, "connection_qualified_name is required"),
        (SPACE_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DremioSpace.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator sets the connection and the denormalised space attributes."""
    sut = DremioSpace.creator(
        name=SPACE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == SPACE_NAME
    assert sut.qualified_name == SPACE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "dremio"
    assert sut.dremio_space_qualified_name == SPACE_QUALIFIED_NAME
    assert sut.dremio_space_name == SPACE_NAME


def test_validate_rejects_qualified_name_without_path():
    """Test validate enforces the {connection_qn}/{name} pattern."""
    sut = DremioSpace.creator(
        name=SPACE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )
    sut.qualified_name = SPACE_NAME

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SPACE_NAME, "qualified_name is required"),
        (SPACE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DremioSpace.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DremioSpace for modification."""
    sut = DremioSpace.updater(qualified_name=SPACE_QUALIFIED_NAME, name=SPACE_NAME)

    assert sut.qualified_name == SPACE_QUALIFIED_NAME
    assert sut.name == SPACE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DremioSpace.updater(
        qualified_name=SPACE_QUALIFIED_NAME, name=SPACE_NAME
    ).trim_to_required()

    assert sut.qualified_name == SPACE_QUALIFIED_NAME
    assert sut.name == SPACE_NAME
