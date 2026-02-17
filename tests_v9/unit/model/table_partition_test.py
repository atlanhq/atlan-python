# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for TablePartition model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import TablePartition
from pyatlan_v9.model.serde import Serde
from tests_v9.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
    TABLE_NAME,
    TABLE_PARTITION_NAME,
    TABLE_QUALIFIED_NAME,
)

TABLE_PARTITION_QUALIFIED_NAME = f"{SCHEMA_QUALIFIED_NAME}/{TABLE_PARTITION_NAME}"


@pytest.mark.parametrize(
    "name, table_qualified_name, message",
    [
        (None, TABLE_QUALIFIED_NAME, "name is required"),
        (TABLE_PARTITION_NAME, None, "table_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, table_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        TablePartition.creator(name=name, table_qualified_name=table_qualified_name)


def test_creator():
    """Test that creator properly initializes a TablePartition with all derived fields."""
    sut = TablePartition.creator(
        name=TABLE_PARTITION_NAME,
        table_qualified_name=TABLE_QUALIFIED_NAME,
    )

    assert sut.name == TABLE_PARTITION_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == TABLE_PARTITION_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.table_name == TABLE_NAME
    assert sut.table_qualified_name == TABLE_QUALIFIED_NAME


def test_overload_creator():
    """Test creator with all optional parameters provided."""
    sut = TablePartition.creator(
        name=TABLE_PARTITION_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        table_name=TABLE_NAME,
        table_qualified_name=TABLE_QUALIFIED_NAME,
    )

    assert sut.name == TABLE_PARTITION_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == TABLE_PARTITION_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.table_name == TABLE_NAME
    assert sut.table_qualified_name == TABLE_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, TABLE_PARTITION_QUALIFIED_NAME, "qualified_name is required"),
        (TABLE_PARTITION_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        TablePartition.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a TablePartition instance for modification."""
    sut = TablePartition.updater(
        qualified_name=TABLE_PARTITION_QUALIFIED_NAME, name=TABLE_PARTITION_NAME
    )

    assert sut.qualified_name == TABLE_PARTITION_QUALIFIED_NAME
    assert sut.name == TABLE_PARTITION_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a TablePartition with only required fields."""
    sut = TablePartition.updater(
        qualified_name=TABLE_PARTITION_QUALIFIED_NAME, name=TABLE_PARTITION_NAME
    ).trim_to_required()

    assert sut.qualified_name == TABLE_PARTITION_QUALIFIED_NAME
    assert sut.name == TABLE_PARTITION_NAME


def test_basic_construction():
    """Test basic TablePartition construction with minimal parameters."""
    tp = TablePartition(
        name=TABLE_PARTITION_NAME, qualified_name=TABLE_PARTITION_QUALIFIED_NAME
    )

    assert tp.name == TABLE_PARTITION_NAME
    assert tp.qualified_name == TABLE_PARTITION_QUALIFIED_NAME
    assert tp.type_name == "TablePartition"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    tp = TablePartition(
        name=TABLE_PARTITION_NAME, qualified_name=TABLE_PARTITION_QUALIFIED_NAME
    )

    assert tp.column_count is UNSET
    assert tp.row_count is UNSET
    assert tp.size_bytes is UNSET
    assert tp.constraint is UNSET
    assert tp.partition_strategy is UNSET
    assert tp.external_location is UNSET


def test_optional_fields():
    """Test setting optional fields on TablePartition."""
    tp = TablePartition(
        name=TABLE_PARTITION_NAME,
        qualified_name=TABLE_PARTITION_QUALIFIED_NAME,
        column_count=5,
        row_count=100,
        partition_strategy="HASH",
        constraint="date > '2024-01-01'",
    )

    assert tp.column_count == 5
    assert tp.row_count == 100
    assert tp.partition_strategy == "HASH"
    assert tp.constraint == "date > '2024-01-01'"


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    tp = TablePartition(
        name=TABLE_PARTITION_NAME, qualified_name=TABLE_PARTITION_QUALIFIED_NAME
    )

    assert tp.alias is UNSET
    tp.alias = None
    assert tp.alias is None
    assert tp.alias is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    tp = TablePartition.creator(
        name=TABLE_PARTITION_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )

    json_str = tp.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "TablePartition"
    assert "attributes" in data
    assert data["attributes"]["name"] == TABLE_PARTITION_NAME
    assert data["attributes"]["qualifiedName"] == TABLE_PARTITION_QUALIFIED_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    tp = TablePartition.creator(
        name=TABLE_PARTITION_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )

    json_str = tp.to_json(nested=False, serde=serde)

    assert json_str
    assert TABLE_PARTITION_NAME in json_str
    assert TABLE_PARTITION_QUALIFIED_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = TablePartition.creator(
        name=TABLE_PARTITION_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )
    json_str = original.to_json(nested=True, serde=serde)

    tp = TablePartition.from_json(json_str, serde=serde)

    assert tp.name == TABLE_PARTITION_NAME
    assert tp.qualified_name == TABLE_PARTITION_QUALIFIED_NAME
    assert tp.type_name == "TablePartition"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = TablePartition.creator(
        name=TABLE_PARTITION_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )
    original.column_count = 5
    original.row_count = 100
    original.partition_strategy = "HASH"

    json_str = original.to_json(nested=True, serde=serde)
    restored = TablePartition.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.column_count == original.column_count
    assert restored.row_count == original.row_count
    assert restored.partition_strategy == original.partition_strategy


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    tp = TablePartition.creator(
        name=TABLE_PARTITION_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )

    json_str = tp.to_json(nested=True, serde=custom_serde)
    restored = TablePartition.from_json(json_str, serde=custom_serde)

    assert restored.name == tp.name
    assert restored.qualified_name == tp.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'TablePartition'."""
    tp = TablePartition(
        name=TABLE_PARTITION_NAME, qualified_name=TABLE_PARTITION_QUALIFIED_NAME
    )
    assert tp.type_name == "TablePartition"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    tp = TablePartition.creator(
        name=TABLE_PARTITION_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )

    assert tp.guid is not UNSET
    assert tp.guid is not None
    assert isinstance(tp.guid, str)
    assert tp.guid.startswith("-")


def test_parent_table_relationship():
    """Test that creator sets the parent_table relationship."""
    tp = TablePartition.creator(
        name=TABLE_PARTITION_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )

    assert tp.parent_table is not None
    assert tp.parent_table.unique_attributes["qualifiedName"] == TABLE_QUALIFIED_NAME
