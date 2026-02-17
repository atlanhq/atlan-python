# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for MaterialisedView model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import MaterialisedView
from pyatlan_v9.model.serde import Serde
from tests_v9.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
    TABLE_QUALIFIED_NAME,
    VIEW_COLUMN_QUALIFIED_NAME,
    VIEW_NAME,
    VIEW_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, schema_qualified_name, message",
    [
        (None, SCHEMA_QUALIFIED_NAME, "name is required"),
        (VIEW_NAME, None, "schema_qualified_name is required"),
        (VIEW_NAME, CONNECTION_QUALIFIED_NAME, "Invalid schema_qualified_name"),
        (VIEW_NAME, DATABASE_QUALIFIED_NAME, "Invalid schema_qualified_name"),
        (VIEW_NAME, TABLE_QUALIFIED_NAME, "Invalid schema_qualified_name"),
        (VIEW_NAME, VIEW_COLUMN_QUALIFIED_NAME, "Invalid schema_qualified_name"),
    ],
)
def test_creator_with_missing_or_invalid_parameters_raises_value_error(
    name: str, schema_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing or invalid."""
    with pytest.raises(ValueError, match=message):
        MaterialisedView.creator(name=name, schema_qualified_name=schema_qualified_name)


def test_creator():
    """Test that creator properly initializes a MaterialisedView with all derived fields."""
    sut = MaterialisedView.creator(
        name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )

    assert sut.name == VIEW_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.unique_attributes["qualifiedName"] == SCHEMA_QUALIFIED_NAME


def test_overload_creator():
    """Test creator with all optional parameters provided."""
    sut = MaterialisedView.creator(
        name=VIEW_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        database_name=DATABASE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == VIEW_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.unique_attributes["qualifiedName"] == SCHEMA_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, VIEW_QUALIFIED_NAME, "qualified_name is required"),
        (VIEW_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        MaterialisedView.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a MaterialisedView instance for modification."""
    sut = MaterialisedView.updater(qualified_name=VIEW_QUALIFIED_NAME, name=VIEW_NAME)

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a MaterialisedView with only required fields."""
    sut = MaterialisedView.updater(
        qualified_name=VIEW_QUALIFIED_NAME, name=VIEW_NAME
    ).trim_to_required()

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME


def test_basic_construction():
    """Test basic MaterialisedView construction with minimal parameters."""
    mv = MaterialisedView(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)

    assert mv.name == VIEW_NAME
    assert mv.qualified_name == VIEW_QUALIFIED_NAME
    assert mv.type_name == "MaterialisedView"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    mv = MaterialisedView(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)

    assert mv.column_count is UNSET
    assert mv.row_count is UNSET
    assert mv.size_bytes is UNSET
    assert mv.is_temporary is UNSET
    assert mv.definition is UNSET
    assert mv.refresh_mode is UNSET
    assert mv.refresh_method is UNSET
    assert mv.staleness is UNSET


def test_optional_fields():
    """Test setting optional fields on MaterialisedView."""
    mv = MaterialisedView(
        name=VIEW_NAME,
        qualified_name=VIEW_QUALIFIED_NAME,
        column_count=5,
        row_count=100,
        size_bytes=1024,
        refresh_mode="COMPLETE",
    )

    assert mv.column_count == 5
    assert mv.row_count == 100
    assert mv.size_bytes == 1024
    assert mv.refresh_mode == "COMPLETE"


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    mv = MaterialisedView(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)

    assert mv.alias is UNSET
    mv.alias = None
    assert mv.alias is None
    assert mv.alias is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    mv = MaterialisedView.creator(
        name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )

    json_str = mv.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "MaterialisedView"
    assert "attributes" in data
    assert data["attributes"]["name"] == VIEW_NAME
    assert data["attributes"]["qualifiedName"] == VIEW_QUALIFIED_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    mv = MaterialisedView.creator(
        name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )

    json_str = mv.to_json(nested=False, serde=serde)

    assert json_str
    assert VIEW_NAME in json_str
    assert VIEW_QUALIFIED_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = MaterialisedView.creator(
        name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )
    json_str = original.to_json(nested=True, serde=serde)

    mv = MaterialisedView.from_json(json_str, serde=serde)

    assert mv.name == VIEW_NAME
    assert mv.qualified_name == VIEW_QUALIFIED_NAME
    assert mv.type_name == "MaterialisedView"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = MaterialisedView.creator(
        name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )
    original.column_count = 5
    original.row_count = 100
    original.refresh_mode = "COMPLETE"

    json_str = original.to_json(nested=True, serde=serde)
    restored = MaterialisedView.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.column_count == original.column_count
    assert restored.row_count == original.row_count
    assert restored.refresh_mode == original.refresh_mode


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    mv = MaterialisedView.creator(
        name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )

    json_str = mv.to_json(nested=True, serde=custom_serde)
    restored = MaterialisedView.from_json(json_str, serde=custom_serde)

    assert restored.name == mv.name
    assert restored.qualified_name == mv.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'MaterialisedView'."""
    mv = MaterialisedView(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)
    assert mv.type_name == "MaterialisedView"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    mv = MaterialisedView.creator(
        name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )

    assert mv.guid is not UNSET
    assert mv.guid is not None
    assert isinstance(mv.guid, str)
    assert mv.guid.startswith("-")


def test_sql_fields():
    """Test setting SQL-specific fields (database, schema names)."""
    mv = MaterialisedView(
        name=VIEW_NAME,
        qualified_name=VIEW_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert mv.database_name == DATABASE_NAME
    assert mv.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert mv.schema_name == SCHEMA_NAME
    assert mv.schema_qualified_name == SCHEMA_QUALIFIED_NAME


def test_materialised_view_specific_fields():
    """Test MaterialisedView-specific fields like refresh_mode and staleness."""
    mv = MaterialisedView(
        name=VIEW_NAME,
        qualified_name=VIEW_QUALIFIED_NAME,
        refresh_mode="COMPLETE",
        refresh_method="FORCE",
        staleness="STALE",
        stale_since_date=1686532494000,
    )

    assert mv.refresh_mode == "COMPLETE"
    assert mv.refresh_method == "FORCE"
    assert mv.staleness == "STALE"
    assert mv.stale_since_date == 1686532494000
