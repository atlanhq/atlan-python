# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for CustomEntity model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import CustomEntity
from tests_v9.unit.model.constants import (
    CUSTOM_CONNECTION_QUALIFIED_NAME,
    CUSTOM_CONNECTOR_TYPE,
    CUSTOM_ENTITY_NAME,
    CUSTOM_ENTITY_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (CUSTOM_ENTITY_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        CustomEntity.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test that creator properly initializes a CustomEntity with all derived fields."""
    sut = CustomEntity.creator(
        name=CUSTOM_ENTITY_NAME,
        connection_qualified_name=CUSTOM_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == CUSTOM_ENTITY_NAME
    assert sut.connection_qualified_name == CUSTOM_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == CUSTOM_ENTITY_QUALIFIED_NAME
    assert sut.connector_name == CUSTOM_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CUSTOM_CONNECTION_QUALIFIED_NAME, "qualified_name is required"),
        (CUSTOM_ENTITY_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        CustomEntity.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a CustomEntity instance for modification."""
    sut = CustomEntity.updater(
        qualified_name=CUSTOM_ENTITY_QUALIFIED_NAME, name=CUSTOM_ENTITY_NAME
    )

    assert sut.qualified_name == CUSTOM_ENTITY_QUALIFIED_NAME
    assert sut.name == CUSTOM_ENTITY_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a CustomEntity with only required fields."""
    sut = CustomEntity.updater(
        name=CUSTOM_ENTITY_NAME, qualified_name=CUSTOM_ENTITY_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == CUSTOM_ENTITY_NAME
    assert sut.qualified_name == CUSTOM_ENTITY_QUALIFIED_NAME


def test_basic_construction():
    """Test basic CustomEntity construction with minimal parameters."""
    entity = CustomEntity(
        name=CUSTOM_ENTITY_NAME, qualified_name=CUSTOM_ENTITY_QUALIFIED_NAME
    )

    assert entity.name == CUSTOM_ENTITY_NAME
    assert entity.qualified_name == CUSTOM_ENTITY_QUALIFIED_NAME
    assert entity.type_name == "CustomEntity"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    entity = CustomEntity(
        name=CUSTOM_ENTITY_NAME, qualified_name=CUSTOM_ENTITY_QUALIFIED_NAME
    )

    assert entity.custom_children_subtype is UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    entity = CustomEntity.creator(
        name=CUSTOM_ENTITY_NAME,
        connection_qualified_name=CUSTOM_CONNECTION_QUALIFIED_NAME,
    )

    json_str = entity.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "CustomEntity"
    assert "attributes" in data
    assert data["attributes"]["name"] == CUSTOM_ENTITY_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = CustomEntity.creator(
        name=CUSTOM_ENTITY_NAME,
        connection_qualified_name=CUSTOM_CONNECTION_QUALIFIED_NAME,
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = CustomEntity.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    entity = CustomEntity.creator(
        name=CUSTOM_ENTITY_NAME,
        connection_qualified_name=CUSTOM_CONNECTION_QUALIFIED_NAME,
    )

    assert entity.guid is not UNSET
    assert entity.guid is not None
    assert isinstance(entity.guid, str)
    assert entity.guid.startswith("-")
