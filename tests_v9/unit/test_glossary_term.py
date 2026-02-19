# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""
Unit tests for v9 AtlasGlossaryTerm — ported from tests/unit/test_glossary_term.py.

The v9 model is flat (no nested Attributes class), so:
- `Attributes.create()` tests are adapted to use `AtlasGlossaryTerm.create()` directly.
- Assertions on `sut.attributes.anchor` become `sut.anchor`.
- Anchor `unique_attributes` becomes `anchor.qualified_name`.
"""

import pytest

from pyatlan_v9.model.assets import AtlasGlossary, AtlasGlossaryTerm


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid, message",
    [
        (None, None, None, "1234", "name is required"),
        (
            "Glossary",
            None,
            None,
            None,
            "One of the following parameters are required: anchor, glossary_qualified_name, glossary_guid",
        ),
        (
            "Glossary",
            AtlasGlossary(name="g"),
            "qname",
            None,
            "Only one of the following parameters are allowed: anchor, glossary_qualified_name",
        ),
        (
            "Glossary",
            AtlasGlossary(name="g"),
            None,
            "123",
            "Only one of the following parameters are allowed: anchor, glossary_guid",
        ),
        (
            "Glossary",
            None,
            "qname",
            "123",
            "Only one of the following parameters are allowed: glossary_qualified_name, glossary_guid",
        ),
    ],
)
def test_create_without_required_parameters_raises_value_error(
    name, anchor, glossary_qualified_name, glossary_guid, message
):
    """
    Test that AtlasGlossaryTerm.create() raises ValueError for invalid parameter
    combinations. Replaces both `Attributes.create` and `create` legacy tests.
    """
    with pytest.raises(ValueError, match=message):
        AtlasGlossaryTerm.create(
            name=name,
            anchor=anchor,
            glossary_qualified_name=glossary_qualified_name,
            glossary_guid=glossary_guid,
        )


@pytest.mark.parametrize(
    "name, anchor, glossary_qualified_name, glossary_guid",
    [
        ("Glossary", AtlasGlossary.ref_by_guid(guid="123"), None, None),
        (
            "Glossary",
            AtlasGlossary.ref_by_qualified_name(
                qualified_name="glossary/qualifiedName"
            ),
            None,
            None,
        ),
        ("Glossary", None, "glossary/qualifiedName", None),
        ("Glossary", None, None, "123"),
    ],
)
def test_create_with_required_parameters(
    name, anchor, glossary_qualified_name, glossary_guid
):
    """
    Test that AtlasGlossaryTerm.create() works with valid parameter combinations.
    Replaces both `Attributes.create` and `create` legacy tests.
    """
    sut = AtlasGlossaryTerm.create(
        name=name,
        anchor=anchor,
        glossary_qualified_name=glossary_qualified_name,
        glossary_guid=glossary_guid,
    )

    # In the v9 flat model, anchor is directly on the term (not nested in attributes)
    if anchor:
        # The creator trims the anchor to a reference; check guid/qn match
        if hasattr(anchor, "guid") and anchor.guid is not None:
            from msgspec import UNSET

            if anchor.guid is not UNSET:
                assert sut.anchor.guid == anchor.guid
        if hasattr(anchor, "qualified_name") and anchor.qualified_name is not None:
            from msgspec import UNSET

            if anchor.qualified_name is not UNSET:
                assert sut.anchor.qualified_name == anchor.qualified_name
    if glossary_qualified_name:
        assert sut.anchor.qualified_name == glossary_qualified_name
    if glossary_guid:
        assert sut.anchor.guid == glossary_guid
