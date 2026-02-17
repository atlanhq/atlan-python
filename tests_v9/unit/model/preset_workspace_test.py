# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for PresetWorkspace model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import PresetWorkspace
from tests_v9.unit.model.constants import (
    PRESET_CONNECTION_QUALIFIED_NAME,
    PRESET_CONNECTOR_TYPE,
    PRESET_WORKSPACE_NAME,
    PRESET_WORKSPACE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (PRESET_WORKSPACE_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        PresetWorkspace.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test that creator properly initializes a PresetWorkspace with all derived fields."""
    sut = PresetWorkspace.creator(
        name=PRESET_WORKSPACE_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_WORKSPACE_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PRESET_WORKSPACE_QUALIFIED_NAME, "qualified_name is required"),
        (PRESET_WORKSPACE_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        PresetWorkspace.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a PresetWorkspace instance for modification."""
    sut = PresetWorkspace.updater(
        qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME, name=PRESET_WORKSPACE_NAME
    )

    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.name == PRESET_WORKSPACE_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a PresetWorkspace with only required fields."""
    sut = PresetWorkspace.updater(
        qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME, name=PRESET_WORKSPACE_NAME
    ).trim_to_required()

    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.name == PRESET_WORKSPACE_NAME


def test_basic_construction():
    """Test basic PresetWorkspace construction with minimal parameters."""
    workspace = PresetWorkspace(
        name=PRESET_WORKSPACE_NAME, qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME
    )

    assert workspace.name == PRESET_WORKSPACE_NAME
    assert workspace.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert workspace.type_name == "PresetWorkspace"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    workspace = PresetWorkspace(
        name=PRESET_WORKSPACE_NAME, qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME
    )

    assert workspace.preset_workspace_cluster_id is UNSET
    assert workspace.preset_workspace_hostname is UNSET
    assert workspace.preset_workspace_region is UNSET
    assert workspace.preset_workspace_status is UNSET


def test_type_name_defaults():
    """Test that type_name defaults to PresetWorkspace."""
    workspace = PresetWorkspace(
        name=PRESET_WORKSPACE_NAME, qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME
    )

    assert workspace.type_name == "PresetWorkspace"


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    workspace = PresetWorkspace.creator(
        name=PRESET_WORKSPACE_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    json_str = workspace.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "PresetWorkspace"
    assert "attributes" in data
    assert data["attributes"]["name"] == PRESET_WORKSPACE_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = PresetWorkspace.creator(
        name=PRESET_WORKSPACE_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = PresetWorkspace.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    workspace = PresetWorkspace.creator(
        name=PRESET_WORKSPACE_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    assert workspace.guid is not UNSET
    assert workspace.guid is not None
    assert isinstance(workspace.guid, str)
    assert workspace.guid.startswith("-")


def test_backward_compat_create():
    """Test that create is a backward-compatible alias for creator."""
    sut = PresetWorkspace.create(
        name=PRESET_WORKSPACE_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_WORKSPACE_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


def test_backward_compat_create_for_modification():
    """Test that create_for_modification is a backward-compatible alias for updater."""
    sut = PresetWorkspace.create_for_modification(
        qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME, name=PRESET_WORKSPACE_NAME
    )

    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.name == PRESET_WORKSPACE_NAME
