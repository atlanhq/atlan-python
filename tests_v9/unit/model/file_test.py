# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for File model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import File
from pyatlan_v9.serde import Serde
from tests_v9.unit.model.constants import (
    FILE_CONNECTION_QUALIFIED_NAME,
    FILE_NAME,
    FILE_QUALIFIED_NAME,
)

FILE_TYPE = "PDF"


@pytest.mark.parametrize(
    "name, connection_qualified_name, file_type, msg",
    [
        (None, FILE_CONNECTION_QUALIFIED_NAME, FILE_TYPE, "name is required"),
        (FILE_NAME, None, FILE_TYPE, "connection_qualified_name is required"),
        ("", FILE_CONNECTION_QUALIFIED_NAME, FILE_TYPE, "name cannot be blank"),
        (FILE_NAME, "", FILE_TYPE, "connection_qualified_name cannot be blank"),
        (FILE_NAME, FILE_CONNECTION_QUALIFIED_NAME, None, "file_type is required"),
        (FILE_NAME, FILE_CONNECTION_QUALIFIED_NAME, "", "file_type cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name, connection_qualified_name, file_type, msg
):
    """Test that creator raises ValueError when required parameters are missing or blank."""
    with pytest.raises(ValueError, match=msg):
        File.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            file_type=file_type,
        )


def test_creator():
    """Test that creator properly initializes a File with all derived fields."""
    sut = File.creator(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )

    assert sut.name == FILE_NAME
    assert sut.connection_qualified_name == FILE_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == FILE_QUALIFIED_NAME
    assert sut.connector_name == "api"
    assert sut.file_type == FILE_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FILE_QUALIFIED_NAME, "qualified_name is required"),
        (FILE_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        File.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a File instance for modification."""
    sut = File.updater(qualified_name=FILE_QUALIFIED_NAME, name=FILE_NAME)

    assert sut.qualified_name == FILE_QUALIFIED_NAME
    assert sut.name == FILE_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a File with only required fields."""
    sut = File.updater(
        qualified_name=FILE_QUALIFIED_NAME, name=FILE_NAME
    ).trim_to_required()

    assert sut.qualified_name == FILE_QUALIFIED_NAME
    assert sut.name == FILE_NAME


def test_basic_construction():
    """Test basic File construction with minimal parameters."""
    file = File(name=FILE_NAME, qualified_name=FILE_QUALIFIED_NAME)

    assert file.name == FILE_NAME
    assert file.qualified_name == FILE_QUALIFIED_NAME
    assert file.type_name == "File"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    file = File(name=FILE_NAME, qualified_name=FILE_QUALIFIED_NAME)

    assert file.file_type is UNSET
    assert file.file_path is UNSET
    assert file.link is UNSET
    assert file.is_global is UNSET
    assert file.reference is UNSET


def test_optional_fields():
    """Test setting optional fields on File."""
    file = File(
        name=FILE_NAME,
        qualified_name=FILE_QUALIFIED_NAME,
        file_type=FILE_TYPE,
        link="https://example.com/file.pdf",
    )

    assert file.file_type == FILE_TYPE
    assert file.link == "https://example.com/file.pdf"


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    file = File(name=FILE_NAME, qualified_name=FILE_QUALIFIED_NAME)

    assert file.link is UNSET
    file.link = None
    assert file.link is None
    assert file.link is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    file = File.creator(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )

    json_str = file.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "File"
    assert "attributes" in data
    assert data["attributes"]["name"] == FILE_NAME
    assert data["attributes"]["qualifiedName"] == FILE_QUALIFIED_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    file = File.creator(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )

    json_str = file.to_json(nested=False, serde=serde)

    assert json_str
    assert FILE_NAME in json_str
    assert FILE_QUALIFIED_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = File.creator(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )
    json_str = original.to_json(nested=True, serde=serde)

    file = File.from_json(json_str, serde=serde)

    assert file.name == FILE_NAME
    assert file.qualified_name == FILE_QUALIFIED_NAME
    assert file.type_name == "File"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = File.creator(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )
    original.link = "https://example.com/file.pdf"

    json_str = original.to_json(nested=True, serde=serde)
    restored = File.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.file_type == original.file_type
    assert restored.link == original.link


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    file = File.creator(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )

    json_str = file.to_json(nested=True, serde=custom_serde)
    restored = File.from_json(json_str, serde=custom_serde)

    assert restored.name == file.name
    assert restored.qualified_name == file.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'File'."""
    file = File(name=FILE_NAME, qualified_name=FILE_QUALIFIED_NAME)
    assert file.type_name == "File"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    file = File.creator(
        name=FILE_NAME,
        connection_qualified_name=FILE_CONNECTION_QUALIFIED_NAME,
        file_type=FILE_TYPE,
    )

    assert file.guid is not UNSET
    assert file.guid is not None
    assert isinstance(file.guid, str)
    assert file.guid.startswith("-")
