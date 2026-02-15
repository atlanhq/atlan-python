# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AtlasGlossaryTerm model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import AtlasGlossary, AtlasGlossaryTerm
from pyatlan_v9.serde import Serde
from tests_v9.unit.model.constants import (
    GLOSSARY_NAME,
    GLOSSARY_QUALIFIED_NAME,
    GLOSSARY_TERM_NAME,
    GLOSSARY_TERM_QUALIFIED_NAME,
)

ANCHOR = AtlasGlossary.updater(
    qualified_name=GLOSSARY_QUALIFIED_NAME, name=GLOSSARY_NAME
)
GLOSSARY_GUID = "123"


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid, categories, message",
    [
        (
            None,
            ANCHOR,
            GLOSSARY_QUALIFIED_NAME,
            GLOSSARY_GUID,
            None,
            "name is required",
        ),
        (
            GLOSSARY_TERM_NAME,
            ANCHOR,
            GLOSSARY_QUALIFIED_NAME,
            GLOSSARY_GUID,
            None,
            "Only one of the following parameters are allowed: anchor, glossary_qualified_name, glossary_guid",
        ),
        (
            GLOSSARY_TERM_NAME,
            ANCHOR,
            GLOSSARY_QUALIFIED_NAME,
            None,
            None,
            "Only one of the following parameters are allowed: anchor, glossary_qualified_name",
        ),
        (
            GLOSSARY_TERM_NAME,
            ANCHOR,
            None,
            GLOSSARY_GUID,
            None,
            "Only one of the following parameters are allowed: anchor, glossary_guid",
        ),
        (
            GLOSSARY_TERM_NAME,
            None,
            GLOSSARY_QUALIFIED_NAME,
            GLOSSARY_GUID,
            None,
            "Only one of the following parameters are allowed: glossary_qualified_name, glossary_guid",
        ),
        (
            GLOSSARY_TERM_NAME,
            None,
            None,
            None,
            None,
            "One of the following parameters are required: anchor, glossary_qualified_name, glossary_guid",
        ),
    ],
)
def test_creator_with_missing_or_invalid_parameters_raises_value_error(
    name: str,
    anchor: AtlasGlossary,
    glossary_qualified_name: str,
    glossary_guid: str,
    categories: list,
    message: str,
):
    """Test that creator raises ValueError when parameters are missing or mutually exclusive ones are provided."""
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryTerm.creator(
            name=name,
            anchor=anchor,
            glossary_qualified_name=glossary_qualified_name,
            glossary_guid=glossary_guid,
            categories=categories,
        )


@pytest.mark.parametrize(
    "anchor, glossary_qualified_name, glossary_guid, categories",
    [
        (ANCHOR, None, None, None),
        (None, GLOSSARY_QUALIFIED_NAME, None, None),
        (None, None, GLOSSARY_GUID, None),
    ],
)
def test_creator(
    anchor: AtlasGlossary,
    glossary_qualified_name: str,
    glossary_guid: str,
    categories: list,
):
    """Test that creator properly initializes a GlossaryTerm with different glossary identifier options."""
    sut = AtlasGlossaryTerm.creator(
        name=GLOSSARY_TERM_NAME,
        anchor=anchor,
        glossary_qualified_name=glossary_qualified_name,
        glossary_guid=glossary_guid,
        categories=categories,
    )

    assert sut.name == GLOSSARY_TERM_NAME
    assert sut.qualified_name
    assert sut.categories == categories

    # Verify anchor is set correctly based on which parameter was provided
    if anchor:
        assert sut.anchor is not None
        assert (
            sut.anchor.guid == anchor.guid
            or sut.anchor.unique_attributes.get("qualifiedName")
            == anchor.qualified_name
        )
    elif glossary_qualified_name:
        assert sut.anchor is not None
        assert sut.anchor.unique_attributes["qualifiedName"] == glossary_qualified_name
    elif glossary_guid:
        assert sut.anchor is not None
        assert sut.anchor.guid == glossary_guid


@pytest.mark.parametrize(
    "name, qualified_name, glossary_guid, message",
    [
        (None, GLOSSARY_TERM_QUALIFIED_NAME, GLOSSARY_GUID, "name is required"),
        (GLOSSARY_TERM_NAME, None, GLOSSARY_GUID, "qualified_name is required"),
        (
            GLOSSARY_TERM_NAME,
            GLOSSARY_TERM_QUALIFIED_NAME,
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
        AtlasGlossaryTerm.updater(
            qualified_name=qualified_name, name=name, glossary_guid=glossary_guid
        )


def test_updater():
    """Test that updater creates a GlossaryTerm instance for modification."""
    sut = AtlasGlossaryTerm.updater(
        qualified_name=GLOSSARY_TERM_QUALIFIED_NAME,
        name=GLOSSARY_TERM_NAME,
        glossary_guid=GLOSSARY_GUID,
    )

    assert sut.name == GLOSSARY_TERM_NAME
    assert sut.qualified_name == GLOSSARY_TERM_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID


def test_trim_to_required():
    """Test that trim_to_required returns a GlossaryTerm with only required fields."""
    sut = AtlasGlossaryTerm.updater(
        qualified_name=GLOSSARY_TERM_QUALIFIED_NAME,
        name=GLOSSARY_TERM_NAME,
        glossary_guid=GLOSSARY_GUID,
    ).trim_to_required()

    assert sut.name == GLOSSARY_TERM_NAME
    assert sut.qualified_name == GLOSSARY_TERM_QUALIFIED_NAME
    assert sut.anchor.guid == GLOSSARY_GUID


@pytest.mark.parametrize(
    "anchor",
    [(None), (AtlasGlossary())],
)
def test_trim_to_required_raises_value_error_when_anchor_is_invalid(anchor):
    """Test that trim_to_required raises ValueError when anchor or anchor.guid is not available."""
    sut = AtlasGlossaryTerm.updater(
        qualified_name=GLOSSARY_TERM_QUALIFIED_NAME,
        name=GLOSSARY_TERM_NAME,
        glossary_guid=GLOSSARY_GUID,
    )
    sut.anchor = anchor

    with pytest.raises(ValueError, match="anchor.guid must be available"):
        sut.trim_to_required()


def test_basic_construction():
    """Test basic GlossaryTerm construction with minimal parameters."""
    term = AtlasGlossaryTerm(
        name=GLOSSARY_TERM_NAME, qualified_name=GLOSSARY_TERM_QUALIFIED_NAME
    )

    assert term.name == GLOSSARY_TERM_NAME
    assert term.qualified_name == GLOSSARY_TERM_QUALIFIED_NAME
    assert term.type_name == "AtlasGlossaryTerm"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    term = AtlasGlossaryTerm(
        name=GLOSSARY_TERM_NAME, qualified_name=GLOSSARY_TERM_QUALIFIED_NAME
    )

    assert term.short_description is UNSET
    assert term.long_description is UNSET
    assert term.examples is UNSET
    assert term.abbreviation is UNSET
    assert term.usage is UNSET


def test_optional_fields():
    """Test setting optional fields on GlossaryTerm."""
    term = AtlasGlossaryTerm(
        name=GLOSSARY_TERM_NAME,
        qualified_name=GLOSSARY_TERM_QUALIFIED_NAME,
        short_description="Short desc",
        abbreviation="MT",
        usage="Test usage",
    )

    assert term.short_description == "Short desc"
    assert term.abbreviation == "MT"
    assert term.usage == "Test usage"


def test_none_vs_unset():
    """Test the distinction between None and UNSET values."""
    term = AtlasGlossaryTerm(
        name=GLOSSARY_TERM_NAME, qualified_name=GLOSSARY_TERM_QUALIFIED_NAME
    )

    assert term.abbreviation is UNSET
    term.abbreviation = None
    assert term.abbreviation is None
    assert term.abbreviation is not UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    term = AtlasGlossaryTerm.creator(
        name=GLOSSARY_TERM_NAME, glossary_guid=GLOSSARY_GUID
    )

    json_str = term.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "AtlasGlossaryTerm"
    assert "attributes" in data
    assert data["attributes"]["name"] == GLOSSARY_TERM_NAME


def test_serialization_to_json_flat(serde):
    """Test serialization to flat JSON format."""
    term = AtlasGlossaryTerm.creator(
        name=GLOSSARY_TERM_NAME, glossary_guid=GLOSSARY_GUID
    )

    json_str = term.to_json(nested=False, serde=serde)

    assert json_str
    assert GLOSSARY_TERM_NAME in json_str


def test_deserialization_from_json(serde):
    """Test deserialization from nested JSON format."""
    original = AtlasGlossaryTerm.creator(
        name=GLOSSARY_TERM_NAME, glossary_guid=GLOSSARY_GUID
    )
    json_str = original.to_json(nested=True, serde=serde)

    term = AtlasGlossaryTerm.from_json(json_str, serde=serde)

    assert term.name == GLOSSARY_TERM_NAME
    assert term.type_name == "AtlasGlossaryTerm"


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = AtlasGlossaryTerm.creator(
        name=GLOSSARY_TERM_NAME, glossary_guid=GLOSSARY_GUID
    )
    original.abbreviation = "MT"
    original.usage = "Test"

    json_str = original.to_json(nested=True, serde=serde)
    restored = AtlasGlossaryTerm.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.abbreviation == original.abbreviation
    assert restored.usage == original.usage


def test_with_custom_serde():
    """Test that a custom Serde instance can be used for serialization."""
    custom_serde = Serde()
    term = AtlasGlossaryTerm.creator(
        name=GLOSSARY_TERM_NAME, glossary_guid=GLOSSARY_GUID
    )

    json_str = term.to_json(nested=True, serde=custom_serde)
    restored = AtlasGlossaryTerm.from_json(json_str, serde=custom_serde)

    assert restored.name == term.name
    assert restored.qualified_name == term.qualified_name


def test_type_name_defaults():
    """Test that type_name defaults to 'AtlasGlossaryTerm'."""
    term = AtlasGlossaryTerm(
        name=GLOSSARY_TERM_NAME, qualified_name=GLOSSARY_TERM_QUALIFIED_NAME
    )
    assert term.type_name == "AtlasGlossaryTerm"


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    term = AtlasGlossaryTerm.creator(
        name=GLOSSARY_TERM_NAME, glossary_guid=GLOSSARY_GUID
    )

    assert term.guid is not UNSET
    assert term.guid is not None
    assert isinstance(term.guid, str)
    assert term.guid.startswith("-")


def test_relationship_fields():
    """Test setting relationship fields on GlossaryTerm."""
    from pyatlan_v9.models.gtc_related import RelatedAtlasGlossary

    term = AtlasGlossaryTerm(
        name=GLOSSARY_TERM_NAME,
        qualified_name=GLOSSARY_TERM_QUALIFIED_NAME,
        anchor=RelatedAtlasGlossary(guid=GLOSSARY_GUID),
    )

    assert term.anchor is not None
    assert term.anchor.guid == GLOSSARY_GUID
