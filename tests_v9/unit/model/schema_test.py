# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Schema model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import Schema
from pyatlan_v9.serde import Serde
from tests_v9.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, database_qualified_name, message",
    [
        (None, DATABASE_QUALIFIED_NAME, "name is required"),
        (SCHEMA_NAME, None, "database_qualified_name is required"),
        (SCHEMA_NAME, "abc", "Invalid database_qualified_name"),
        (SCHEMA_NAME, CONNECTION_QUALIFIED_NAME, "Invalid database_qualified_name"),
        (
            SCHEMA_NAME,
            SCHEMA_QUALIFIED_NAME,
            "Invalid database_qualified_name",
        ),
    ],
)
def test_creator_with_missing_or_invalid_parameters_raises_value_error(
    name: str, database_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing or invalid."""
    with pytest.raises(ValueError, match=message):
        Schema.creator(name=name, database_qualified_name=database_qualified_name)


def test_creator():
    """Test that creator properly initializes a Schema with all derived fields."""
    sut = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )

    assert sut.name == SCHEMA_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.database.unique_attributes["qualifiedName"] == DATABASE_QUALIFIED_NAME


def test_overload_creator():
    """Test creator with all optional parameters provided."""
    sut = Schema.creator(
        name=SCHEMA_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == SCHEMA_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.database.unique_attributes["qualifiedName"] == DATABASE_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SCHEMA_QUALIFIED_NAME, "qualified_name is required"),
        (SCHEMA_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Schema.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a Schema instance for modification."""
    sut = Schema.updater(qualified_name=SCHEMA_QUALIFIED_NAME, name=SCHEMA_NAME)

    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.name == SCHEMA_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a Schema with only required fields."""
    sut = Schema.updater(
        qualified_name=SCHEMA_QUALIFIED_NAME, name=SCHEMA_NAME
    ).trim_to_required()

    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.name == SCHEMA_NAME


def test_basic_construction():
    """Test basic Schema construction with minimal parameters."""
    schema = Schema(name=SCHEMA_NAME, qualified_name=SCHEMA_QUALIFIED_NAME)

    assert schema.name == SCHEMA_NAME
    assert schema.qualified_name == SCHEMA_QUALIFIED_NAME
    assert schema.type_name == "Schema"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    schema = Schema(name=SCHEMA_NAME, qualified_name=SCHEMA_QUALIFIED_NAME)

    assert schema.table_count is UNSET
    assert schema.views_count is UNSET
    assert schema.sql_external_location is UNSET
    assert schema.query_count is UNSET
    assert schema.sql_is_secure is UNSET


def test_optional_fields():
    """Test setting optional fields on Schema."""
    schema = Schema(
        name=SCHEMA_NAME,
        qualified_name=SCHEMA_QUALIFIED_NAME,
        table_count=10,
        views_count=5,
        query_count=100,
    )

    assert schema.table_count == 10
    assert schema.views_count == 5
    assert schema.query_count == 100


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    schema = Schema(name=SCHEMA_NAME, qualified_name=SCHEMA_QUALIFIED_NAME)

    assert schema.sql_is_secure is UNSET
    schema.sql_is_secure = None
    assert schema.sql_is_secure is None
    assert schema.sql_is_secure is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    schema = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )

    json_str = schema.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "Schema"
    assert "attributes" in data
    assert data["attributes"]["name"] == SCHEMA_NAME
    assert data["attributes"]["qualifiedName"] == SCHEMA_QUALIFIED_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    schema = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )

    json_str = schema.to_json(nested=False, serde=serde)

    assert json_str
    assert SCHEMA_NAME in json_str
    assert SCHEMA_QUALIFIED_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )
    json_str = original.to_json(nested=True, serde=serde)

    schema = Schema.from_json(json_str, serde=serde)

    assert schema.name == SCHEMA_NAME
    assert schema.qualified_name == SCHEMA_QUALIFIED_NAME
    assert schema.type_name == "Schema"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )
    original.table_count = 5
    original.views_count = 3

    json_str = original.to_json(nested=True, serde=serde)
    restored = Schema.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.table_count == original.table_count
    assert restored.views_count == original.views_count


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    schema = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )

    json_str = schema.to_json(nested=True, serde=custom_serde)
    restored = Schema.from_json(json_str, serde=custom_serde)

    assert restored.name == schema.name
    assert restored.qualified_name == schema.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'Schema'."""
    schema = Schema(name=SCHEMA_NAME, qualified_name=SCHEMA_QUALIFIED_NAME)
    assert schema.type_name == "Schema"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    schema = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )

    assert schema.guid is not UNSET
    assert schema.guid is not None
    assert isinstance(schema.guid, str)
    assert schema.guid.startswith("-")


def test_sql_fields():
    """Test setting SQL-specific fields (database names)."""
    schema = Schema(
        name=SCHEMA_NAME,
        qualified_name=SCHEMA_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
    )

    assert schema.database_name == DATABASE_NAME
    assert schema.database_qualified_name == DATABASE_QUALIFIED_NAME
