# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for PresetDashboard model in pyatlan_v9."""

import pytest

from pyatlan_v9.model import PresetDashboard
from tests_v9.unit.model.constants import (
    PRESET_CONNECTION_QUALIFIED_NAME,
    PRESET_CONNECTOR_TYPE,
    PRESET_DASHBOARD_NAME,
    PRESET_DASHBOARD_QUALIFIED_NAME,
    PRESET_WORKSPACE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, preset_workspace_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (PRESET_DASHBOARD_NAME, None, "preset_workspace_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, preset_workspace_qualified_name: str, message: str
):
    """Test creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        PresetDashboard.creator(
            name=name, preset_workspace_qualified_name=preset_workspace_qualified_name
        )


def test_creator():
    """Test creator builds derived names and connector metadata."""
    sut = PresetDashboard.creator(
        name=PRESET_DASHBOARD_NAME,
        preset_workspace_qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_DASHBOARD_NAME
    assert sut.preset_workspace_qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{PRESET_WORKSPACE_QUALIFIED_NAME}/{PRESET_DASHBOARD_NAME}"
    )
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


def test_overload_creator():
    """Test creator accepts explicit connection_qualified_name override."""
    sut = PresetDashboard.creator(
        name=PRESET_DASHBOARD_NAME,
        preset_workspace_qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_DASHBOARD_NAME
    assert sut.preset_workspace_qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{PRESET_WORKSPACE_QUALIFIED_NAME}/{PRESET_DASHBOARD_NAME}"
    )
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PRESET_DASHBOARD_QUALIFIED_NAME, "qualified_name is required"),
        (PRESET_DASHBOARD_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        PresetDashboard.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater returns minimal update payload."""
    sut = PresetDashboard.updater(
        qualified_name=PRESET_DASHBOARD_QUALIFIED_NAME, name=PRESET_DASHBOARD_NAME
    )

    assert sut.qualified_name == PRESET_DASHBOARD_QUALIFIED_NAME
    assert sut.name == PRESET_DASHBOARD_NAME


def test_trim_to_required():
    """Test trim_to_required preserves required update fields."""
    sut = PresetDashboard.updater(
        qualified_name=PRESET_DASHBOARD_QUALIFIED_NAME, name=PRESET_DASHBOARD_NAME
    ).trim_to_required()

    assert sut.qualified_name == PRESET_DASHBOARD_QUALIFIED_NAME
    assert sut.name == PRESET_DASHBOARD_NAME
