# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Table model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import Table
from pyatlan_v9.model.serde import Serde
from tests_v9.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
    TABLE_NAME,
    TABLE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, schema_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (TABLE_NAME, None, "schema_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, schema_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Table.create(name=name, schema_qualified_name=schema_qualified_name)


def test_create():
    """Test that creator properly initializes a Table with all derived fields."""
    sut = Table.create(name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    assert sut.name == TABLE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.unique_attributes["qualifiedName"] == SCHEMA_QUALIFIED_NAME


def test_overload_creator():
    """Test creator with all optional parameters provided."""
    sut = Table.creator(
        name=TABLE_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == TABLE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.unique_attributes["qualifiedName"] == SCHEMA_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, TABLE_QUALIFIED_NAME, "qualified_name is required"),
        (TABLE_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Table.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a Table instance for modification."""
    sut = Table.updater(qualified_name=TABLE_QUALIFIED_NAME, name=TABLE_NAME)

    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.name == TABLE_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a Table with only required fields."""
    sut = Table.updater(
        qualified_name=TABLE_QUALIFIED_NAME, name=TABLE_NAME
    ).trim_to_required()

    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.name == TABLE_NAME


def test_basic_construction():
    """Test basic Table construction with minimal parameters."""
    table = Table(name=TABLE_NAME, qualified_name=TABLE_QUALIFIED_NAME)

    assert table.name == TABLE_NAME
    assert table.qualified_name == TABLE_QUALIFIED_NAME
    assert table.type_name == "Table"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    table = Table(name=TABLE_NAME, qualified_name=TABLE_QUALIFIED_NAME)

    assert table.column_count is UNSET
    assert table.row_count is UNSET
    assert table.size_bytes is UNSET
    assert table.is_temporary is UNSET
    assert table.is_partitioned is UNSET


def test_optional_fields():
    """Test setting optional fields on Table."""
    table = Table(
        name=TABLE_NAME,
        qualified_name=TABLE_QUALIFIED_NAME,
        column_count=10,
        row_count=1000,
        size_bytes=5000,
    )

    assert table.column_count == 10
    assert table.row_count == 1000
    assert table.size_bytes == 5000


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    table = Table(name=TABLE_NAME, qualified_name=TABLE_QUALIFIED_NAME)

    assert table.alias is UNSET
    table.alias = None
    assert table.alias is None
    assert table.alias is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    table = Table.create(name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    json_str = table.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "Table"
    assert "attributes" in data
    assert data["attributes"]["name"] == TABLE_NAME
    assert data["attributes"]["qualifiedName"] == TABLE_QUALIFIED_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    table = Table.create(name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    json_str = table.to_json(nested=False, serde=serde)

    assert json_str
    assert TABLE_NAME in json_str
    assert TABLE_QUALIFIED_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = Table.create(
        name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )
    json_str = original.to_json(nested=True, serde=serde)

    table = Table.from_json(json_str, serde=serde)

    assert table.name == TABLE_NAME
    assert table.qualified_name == TABLE_QUALIFIED_NAME
    assert table.type_name == "Table"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = Table.create(
        name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME
    )
    original.column_count = 5
    original.row_count = 100

    json_str = original.to_json(nested=True, serde=serde)
    restored = Table.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.column_count == original.column_count
    assert restored.row_count == original.row_count


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    table = Table.create(name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    json_str = table.to_json(nested=True, serde=custom_serde)
    restored = Table.from_json(json_str, serde=custom_serde)

    assert restored.name == table.name
    assert restored.qualified_name == table.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'Table'."""
    table = Table(name=TABLE_NAME, qualified_name=TABLE_QUALIFIED_NAME)
    assert table.type_name == "Table"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    table = Table.creator(name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    assert table.guid is not UNSET
    assert table.guid is not None
    assert isinstance(table.guid, str)
    assert table.guid.startswith("-")


def test_sql_fields():
    """Test setting SQL-specific fields (database, schema names)."""
    table = Table(
        name=TABLE_NAME,
        qualified_name=TABLE_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert table.database_name == DATABASE_NAME
    assert table.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert table.schema_name == SCHEMA_NAME
    assert table.schema_qualified_name == SCHEMA_QUALIFIED_NAME
