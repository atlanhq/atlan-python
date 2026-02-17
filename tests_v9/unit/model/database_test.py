# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Database model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import Database
from pyatlan_v9.model.serde import Serde
from tests_v9.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (DATABASE_NAME, None, "connection_qualified_name is required"),
        (DATABASE_NAME, "abc", "Invalid connection_qualified_name"),
        (DATABASE_NAME, "default/snowflake", "Invalid connection_qualified_name"),
        (
            DATABASE_NAME,
            "default/snowflke/1686532494/RAW",
            "Invalid connection_qualified_name",
        ),
        (
            DATABASE_NAME,
            "default/snowflake/1686532494/RAW/",
            "Invalid connection_qualified_name",
        ),
    ],
)
def test_creator_with_missing_or_invalid_parameters_raises_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing or invalid."""
    with pytest.raises(ValueError, match=message):
        Database.creator(name=name, connection_qualified_name=connection_qualified_name)


def test_creator():
    """Test that creator properly initializes a Database with all derived fields."""
    sut = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == f"{CONNECTION_QUALIFIED_NAME}/{DATABASE_NAME}"
    assert sut.connector_name == "snowflake"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATABASE_QUALIFIED_NAME, "qualified_name is required"),
        (DATABASE_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Database.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a Database instance for modification."""
    sut = Database.updater(qualified_name=DATABASE_QUALIFIED_NAME, name=DATABASE_NAME)

    assert sut.qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.name == DATABASE_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a Database with only required fields."""
    sut = Database.updater(
        qualified_name=DATABASE_QUALIFIED_NAME, name=DATABASE_NAME
    ).trim_to_required()

    assert sut.qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.name == DATABASE_NAME


def test_basic_construction():
    """Test basic Database construction with minimal parameters."""
    database = Database(name=DATABASE_NAME, qualified_name=DATABASE_QUALIFIED_NAME)

    assert database.name == DATABASE_NAME
    assert database.qualified_name == DATABASE_QUALIFIED_NAME
    assert database.type_name == "Database"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    database = Database(name=DATABASE_NAME, qualified_name=DATABASE_QUALIFIED_NAME)

    assert database.schema_count is UNSET
    assert database.query_count is UNSET
    assert database.query_user_count is UNSET


def test_optional_fields():
    """Test setting optional fields on Database."""
    database = Database(
        name=DATABASE_NAME,
        qualified_name=DATABASE_QUALIFIED_NAME,
        schema_count=5,
        query_count=100,
    )

    assert database.schema_count == 5
    assert database.query_count == 100


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    database = Database(name=DATABASE_NAME, qualified_name=DATABASE_QUALIFIED_NAME)

    assert database.sql_is_secure is UNSET
    database.sql_is_secure = None
    assert database.sql_is_secure is None
    assert database.sql_is_secure is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    database = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    json_str = database.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "Database"
    assert "attributes" in data
    assert data["attributes"]["name"] == DATABASE_NAME
    assert data["attributes"]["qualifiedName"] == DATABASE_QUALIFIED_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    database = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    json_str = database.to_json(nested=False, serde=serde)

    assert json_str
    assert DATABASE_NAME in json_str
    assert DATABASE_QUALIFIED_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )
    json_str = original.to_json(nested=True, serde=serde)

    database = Database.from_json(json_str, serde=serde)

    assert database.name == DATABASE_NAME
    assert database.qualified_name == DATABASE_QUALIFIED_NAME
    assert database.type_name == "Database"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )
    original.schema_count = 10
    original.query_count = 500

    json_str = original.to_json(nested=True, serde=serde)
    restored = Database.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.schema_count == original.schema_count
    assert restored.query_count == original.query_count


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    database = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    json_str = database.to_json(nested=True, serde=custom_serde)
    restored = Database.from_json(json_str, serde=custom_serde)

    assert restored.name == database.name
    assert restored.qualified_name == database.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'Database'."""
    database = Database(name=DATABASE_NAME, qualified_name=DATABASE_QUALIFIED_NAME)
    assert database.type_name == "Database"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    database = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert database.guid is not UNSET
    assert database.guid is not None
    assert isinstance(database.guid, str)
    assert database.guid.startswith("-")
