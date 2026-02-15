# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for View model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import View
from pyatlan_v9.serde import Serde
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
        View.creator(name=name, schema_qualified_name=schema_qualified_name)


def test_creator():
    """Test that creator properly initializes a View with all derived fields."""
    sut = View.creator(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

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
    sut = View.creator(
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
        View.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a View instance for modification."""
    sut = View.updater(qualified_name=VIEW_QUALIFIED_NAME, name=VIEW_NAME)

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a View with only required fields."""
    sut = View.updater(
        qualified_name=VIEW_QUALIFIED_NAME, name=VIEW_NAME
    ).trim_to_required()

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME


def test_basic_construction():
    """Test basic View construction with minimal parameters."""
    view = View(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)

    assert view.name == VIEW_NAME
    assert view.qualified_name == VIEW_QUALIFIED_NAME
    assert view.type_name == "View"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    view = View(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)

    assert view.column_count is UNSET
    assert view.row_count is UNSET
    assert view.size_bytes is UNSET
    assert view.is_temporary is UNSET
    assert view.definition is UNSET


def test_optional_fields():
    """Test setting optional fields on View."""
    view = View(
        name=VIEW_NAME,
        qualified_name=VIEW_QUALIFIED_NAME,
        column_count=5,
        row_count=100,
        size_bytes=1024,
    )

    assert view.column_count == 5
    assert view.row_count == 100
    assert view.size_bytes == 1024


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    view = View(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)

    assert view.alias is UNSET
    view.alias = None
    assert view.alias is None
    assert view.alias is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    view = View.creator(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    json_str = view.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "View"
    assert "attributes" in data
    assert data["attributes"]["name"] == VIEW_NAME
    assert data["attributes"]["qualifiedName"] == VIEW_QUALIFIED_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    view = View.creator(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    json_str = view.to_json(nested=False, serde=serde)

    assert json_str
    assert VIEW_NAME in json_str
    assert VIEW_QUALIFIED_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = View.creator(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)
    json_str = original.to_json(nested=True, serde=serde)

    view = View.from_json(json_str, serde=serde)

    assert view.name == VIEW_NAME
    assert view.qualified_name == VIEW_QUALIFIED_NAME
    assert view.type_name == "View"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = View.creator(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)
    original.column_count = 5
    original.row_count = 100

    json_str = original.to_json(nested=True, serde=serde)
    restored = View.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.column_count == original.column_count
    assert restored.row_count == original.row_count


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    view = View.creator(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    json_str = view.to_json(nested=True, serde=custom_serde)
    restored = View.from_json(json_str, serde=custom_serde)

    assert restored.name == view.name
    assert restored.qualified_name == view.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'View'."""
    view = View(name=VIEW_NAME, qualified_name=VIEW_QUALIFIED_NAME)
    assert view.type_name == "View"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    view = View.creator(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    assert view.guid is not UNSET
    assert view.guid is not None
    assert isinstance(view.guid, str)
    assert view.guid.startswith("-")


def test_sql_fields():
    """Test setting SQL-specific fields (database, schema names)."""
    view = View(
        name=VIEW_NAME,
        qualified_name=VIEW_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert view.database_name == DATABASE_NAME
    assert view.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert view.schema_name == SCHEMA_NAME
    assert view.schema_qualified_name == SCHEMA_QUALIFIED_NAME
