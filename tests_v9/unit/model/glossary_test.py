# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AtlasGlossary model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import AtlasGlossary
from pyatlan_v9.serde import Serde
from tests_v9.unit.model.constants import GLOSSARY_NAME, GLOSSARY_QUALIFIED_NAME


def test_create_with_missing_parameters_raise_value_error():
    """Test that creator raises ValueError when name parameter is missing."""
    with pytest.raises(ValueError, match="name is required"):
        AtlasGlossary.create(name=None)


def test_create():
    """Test that creator properly initializes a Glossary with auto-generated qualified_name."""
    sut = AtlasGlossary.create(name=GLOSSARY_NAME)

    assert sut.name == GLOSSARY_NAME
    assert sut.qualified_name


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, "rJCHYGhPokx9eeXZnqt8Y", "qualified_name is required"),
        ("MyGlossary", None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        AtlasGlossary.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a Glossary instance for modification."""
    sut = AtlasGlossary.updater(
        qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
    )

    assert sut.qualified_name == GLOSSARY_QUALIFIED_NAME
    assert sut.name == GLOSSARY_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a Glossary with only required fields."""
    sut = AtlasGlossary.updater(
        qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
    ).trim_to_required()

    assert sut.qualified_name == GLOSSARY_QUALIFIED_NAME
    assert sut.name == GLOSSARY_NAME


def test_basic_construction():
    """Test basic Glossary construction with minimal parameters."""
    glossary = AtlasGlossary(name=GLOSSARY_NAME, qualified_name=GLOSSARY_QUALIFIED_NAME)

    assert glossary.name == GLOSSARY_NAME
    assert glossary.qualified_name == GLOSSARY_QUALIFIED_NAME
    assert glossary.type_name == "AtlasGlossary"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    glossary = AtlasGlossary(name=GLOSSARY_NAME, qualified_name=GLOSSARY_QUALIFIED_NAME)

    assert glossary.short_description is UNSET
    assert glossary.long_description is UNSET
    assert glossary.language is UNSET
    assert glossary.usage is UNSET


def test_optional_fields():
    """Test setting optional fields on Glossary."""
    glossary = AtlasGlossary(
        name=GLOSSARY_NAME,
        qualified_name=GLOSSARY_QUALIFIED_NAME,
        short_description="Short desc",
        long_description="Long desc",
        language="en",
        usage="Test usage",
    )

    assert glossary.short_description == "Short desc"
    assert glossary.long_description == "Long desc"
    assert glossary.language == "en"
    assert glossary.usage == "Test usage"


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    glossary_with_none = AtlasGlossary(
        name=GLOSSARY_NAME,
        qualified_name=GLOSSARY_QUALIFIED_NAME,
        short_description=None,
    )

    glossary_with_unset = AtlasGlossary(
        name=GLOSSARY_NAME, qualified_name=GLOSSARY_QUALIFIED_NAME
    )

    assert glossary_with_none.short_description is None
    assert glossary_with_unset.short_description is UNSET
    assert glossary_with_none.short_description != glossary_with_unset.short_description


def test_serialization_to_json_nested():
    """Test serialization to nested JSON format (API format)."""
    glossary = AtlasGlossary(
        name=GLOSSARY_NAME,
        qualified_name=GLOSSARY_QUALIFIED_NAME,
        short_description="Test description",
    )

    json_str = glossary.to_json(nested=True)

    assert json_str
    assert "typeName" in json_str
    assert "attributes" in json_str
    assert GLOSSARY_NAME in json_str


def test_serialization_to_json_flat():
    """Test serialization to flat JSON format."""
    glossary = AtlasGlossary(
        name=GLOSSARY_NAME,
        qualified_name=GLOSSARY_QUALIFIED_NAME,
        short_description="Test description",
    )

    json_str = glossary.to_json(nested=False)

    assert json_str
    assert GLOSSARY_NAME in json_str


def test_deserialization_from_json(glossary_json):
    """Test deserialization from nested JSON format."""
    json_str = json.dumps(glossary_json)

    glossary = AtlasGlossary.from_json(json_str)

    assert glossary.type_name == "AtlasGlossary"
    assert glossary.name == "Metrics Glossary"
    assert glossary.qualified_name == "rJCHYGhPokx9eeXZnqt8Y"
    assert glossary.guid == "76d54dd6-925b-499b-a455-6f756ae2d522"


def test_round_trip_serialization(glossary_json):
    """Test that serialization and deserialization preserve all data."""
    json_str = json.dumps(glossary_json)

    glossary = AtlasGlossary.from_json(json_str)
    serialized = glossary.to_json(nested=True)
    glossary2 = AtlasGlossary.from_json(serialized)

    assert glossary.guid == glossary2.guid
    assert glossary.name == glossary2.name
    assert glossary.qualified_name == glossary2.qualified_name
    assert glossary.type_name == glossary2.type_name


def test_relationship_attributes(glossary_json):
    """Test that relationship attributes (terms, categories) are properly deserialized."""
    json_str = json.dumps(glossary_json)

    glossary = AtlasGlossary.from_json(json_str)

    assert glossary.terms is not UNSET
    if glossary.terms:
        assert len(glossary.terms) == 1
        assert glossary.terms[0].guid == "9c9a7a04-d738-48e8-b1d3-a491eb2bccf5"
        assert glossary.terms[0].type_name == "AtlasGlossaryTerm"
        assert glossary.terms[0].display_text == "Active Subscriptions"

    assert glossary.categories is not UNSET
    if glossary.categories:
        assert len(glossary.categories) == 3
        assert glossary.categories[0].guid == "18140435-50b4-40b9-bdf0-9cd002355c6a"
        assert glossary.categories[0].display_text == "Cloud Analytics"


def test_with_custom_serde(glossary_json):
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    json_str = json.dumps(glossary_json)

    glossary = AtlasGlossary.from_json(json_str, serde=custom_serde)

    assert glossary.name == "Metrics Glossary"

    serialized = glossary.to_json(nested=True, serde=custom_serde)
    assert serialized


def test_type_name_defaults():
    """Test that type_name defaults to 'AtlasGlossary'."""
    glossary = AtlasGlossary(name=GLOSSARY_NAME, qualified_name=GLOSSARY_QUALIFIED_NAME)

    assert glossary.type_name == "AtlasGlossary"


def test_glossary_type_field():
    """Test setting the glossary_type field."""
    glossary = AtlasGlossary(
        name=GLOSSARY_NAME,
        qualified_name=GLOSSARY_QUALIFIED_NAME,
        glossary_type="BUSINESS",
    )

    assert glossary.glossary_type == "BUSINESS"


def test_additional_attributes():
    """Test setting additional_attributes dictionary field."""
    attrs = {"key1": "value1", "key2": "value2"}
    glossary = AtlasGlossary(
        name=GLOSSARY_NAME,
        qualified_name=GLOSSARY_QUALIFIED_NAME,
        additional_attributes=attrs,
    )

    assert glossary.additional_attributes == attrs
    assert glossary.additional_attributes["key1"] == "value1"
