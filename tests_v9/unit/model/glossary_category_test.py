# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AtlasGlossaryCategory model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import AtlasGlossary, AtlasGlossaryCategory
from pyatlan_v9.model.serde import Serde
from tests_v9.unit.model.constants import (
    GLOSSARY_CATEGORY_NAME,
    GLOSSARY_CATEGORY_QUALIFIED_NAME,
    GLOSSARY_NAME,
    GLOSSARY_QUALIFIED_NAME,
)

GLOSSARY_GUID = "123"
ANCHOR = AtlasGlossary.updater(
    qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
)
# Set guid for ANCHOR to avoid serialization issues
ANCHOR.guid = GLOSSARY_GUID
PARENT_CATEGORY = AtlasGlossaryCategory.updater(
    qualified_name="123", name="Category", glossary_guid=GLOSSARY_GUID
)


@pytest.mark.parametrize(
    "name, anchor, parent_category, message",
    [
        (None, ANCHOR, None, "name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str,
    anchor: AtlasGlossary,
    parent_category: AtlasGlossaryCategory,
    message: str,
):
    """Test that creator raises ValueError when name parameter is missing."""
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryCategory.creator(
            name=name,
            anchor=anchor,
            parent_category=parent_category,
        )


@pytest.mark.parametrize(
    "anchor, parent_category",
    [
        (ANCHOR, None),
        (ANCHOR, PARENT_CATEGORY),
    ],
)
def test_creator(
    anchor: AtlasGlossary,
    parent_category: AtlasGlossaryCategory,
):
    """Test that creator properly initializes a GlossaryCategory with optional parent category."""
    sut = AtlasGlossaryCategory.creator(
        name=GLOSSARY_CATEGORY_NAME,
        anchor=anchor,
        parent_category=parent_category,
    )

    assert sut.name == GLOSSARY_CATEGORY_NAME
    assert sut.qualified_name

    # Verify parent_category is set correctly
    if parent_category:
        assert sut.parent_category is not None
    else:
        assert sut.parent_category is None

    # Verify anchor is set
    assert sut.anchor is not None


@pytest.mark.parametrize(
    "name, qualified_name, glossary_guid, message",
    [
        (None, GLOSSARY_CATEGORY_QUALIFIED_NAME, GLOSSARY_GUID, "name is required"),
        (GLOSSARY_CATEGORY_NAME, None, GLOSSARY_GUID, "qualified_name is required"),
        (
            GLOSSARY_CATEGORY_NAME,
            GLOSSARY_CATEGORY_QUALIFIED_NAME,
            None,
            "glossary_guid is required",
        ),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    name: str, qualified_name: str, glossary_guid: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryCategory.updater(
            qualified_name=qualified_name, name=name, glossary_guid=glossary_guid
        )


def test_updater():
    """Test that updater creates a GlossaryCategory instance for modification."""
    sut = AtlasGlossaryCategory.updater(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    )

    assert sut.name == GLOSSARY_CATEGORY_NAME
    assert sut.qualified_name == GLOSSARY_CATEGORY_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID


def test_updater_parent_category_removed():
    """Test that updater creates category without parent_category when not specified."""
    category = AtlasGlossaryCategory.updater(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    )

    assert category.parent_category is UNSET
    assert category.anchor.guid == GLOSSARY_GUID
    assert category.name == GLOSSARY_CATEGORY_NAME
    assert category.qualified_name == GLOSSARY_CATEGORY_QUALIFIED_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a GlossaryCategory with only required fields."""
    sut = AtlasGlossaryCategory.updater(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    ).trim_to_required()

    assert sut.name == GLOSSARY_CATEGORY_NAME
    assert sut.qualified_name == GLOSSARY_CATEGORY_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID


@pytest.mark.parametrize(
    "anchor",
    [(None), (AtlasGlossary())],
)
def test_trim_to_required_raises_value_error_when_anchor_is_invalid(anchor):
    """Test that trim_to_required raises ValueError when anchor or anchor.guid is not available."""
    sut = AtlasGlossaryCategory.updater(
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        name=GLOSSARY_CATEGORY_NAME,
        glossary_guid=GLOSSARY_GUID,
    )
    sut.anchor = anchor

    with pytest.raises(ValueError, match="anchor.guid must be available"):
        sut.trim_to_required()


def test_basic_construction():
    """Test basic GlossaryCategory construction with minimal parameters."""
    category = AtlasGlossaryCategory(
        name=GLOSSARY_CATEGORY_NAME, qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME
    )

    assert category.name == GLOSSARY_CATEGORY_NAME
    assert category.qualified_name == GLOSSARY_CATEGORY_QUALIFIED_NAME
    assert category.type_name == "AtlasGlossaryCategory"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    category = AtlasGlossaryCategory(
        name=GLOSSARY_CATEGORY_NAME, qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME
    )

    assert category.short_description is UNSET
    assert category.long_description is UNSET
    assert category.additional_attributes is UNSET
    assert category.category_type is UNSET


def test_optional_fields():
    """Test setting optional fields on GlossaryCategory."""
    category = AtlasGlossaryCategory(
        name=GLOSSARY_CATEGORY_NAME,
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        short_description="Short desc",
        category_type="BUSINESS",
    )

    assert category.short_description == "Short desc"
    assert category.category_type == "BUSINESS"


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    category = AtlasGlossaryCategory(
        name=GLOSSARY_CATEGORY_NAME, qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME
    )

    assert category.short_description is UNSET
    category.short_description = None
    assert category.short_description is None
    assert category.short_description is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    category = AtlasGlossaryCategory.creator(name=GLOSSARY_CATEGORY_NAME, anchor=ANCHOR)

    json_str = category.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "AtlasGlossaryCategory"
    assert "attributes" in data
    assert data["attributes"]["name"] == GLOSSARY_CATEGORY_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    category = AtlasGlossaryCategory.creator(name=GLOSSARY_CATEGORY_NAME, anchor=ANCHOR)

    json_str = category.to_json(nested=False, serde=serde)

    assert json_str
    assert GLOSSARY_CATEGORY_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = AtlasGlossaryCategory.creator(name=GLOSSARY_CATEGORY_NAME, anchor=ANCHOR)
    json_str = original.to_json(nested=True, serde=serde)

    category = AtlasGlossaryCategory.from_json(json_str, serde=serde)

    assert category.name == GLOSSARY_CATEGORY_NAME
    assert category.type_name == "AtlasGlossaryCategory"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = AtlasGlossaryCategory.creator(name=GLOSSARY_CATEGORY_NAME, anchor=ANCHOR)
    original.short_description = "Test description"

    json_str = original.to_json(nested=True, serde=serde)
    restored = AtlasGlossaryCategory.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.short_description == original.short_description


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    category = AtlasGlossaryCategory.creator(name=GLOSSARY_CATEGORY_NAME, anchor=ANCHOR)

    json_str = category.to_json(nested=True, serde=custom_serde)
    restored = AtlasGlossaryCategory.from_json(json_str, serde=custom_serde)

    assert restored.name == category.name
    assert restored.qualified_name == category.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'AtlasGlossaryCategory'."""
    category = AtlasGlossaryCategory(
        name=GLOSSARY_CATEGORY_NAME, qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME
    )
    assert category.type_name == "AtlasGlossaryCategory"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    category = AtlasGlossaryCategory.creator(name=GLOSSARY_CATEGORY_NAME, anchor=ANCHOR)

    assert category.guid is not UNSET
    assert category.guid is not None
    assert isinstance(category.guid, str)
    assert category.guid.startswith("-")


def test_relationship_fields():
    """Test setting relationship fields on GlossaryCategory."""
    from pyatlan_v9.model.assets.gtc_related import RelatedAtlasGlossary

    category = AtlasGlossaryCategory(
        name=GLOSSARY_CATEGORY_NAME,
        qualified_name=GLOSSARY_CATEGORY_QUALIFIED_NAME,
        anchor=RelatedAtlasGlossary(guid=GLOSSARY_GUID),
    )

    assert category.anchor is not None
    assert category.anchor.guid == GLOSSARY_GUID
