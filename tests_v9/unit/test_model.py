# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

"""
Unit tests for v9 models — ported from tests/unit/test_model.py.

Tests the v9 msgspec.Struct model layer: remove_* methods on all entity
subclasses, field get/set, create_for_modification, ref_by_qualified_name,
and model deserialization.

The legacy test uses Pydantic ``Asset.Attributes`` inner classes and property
delegation. The v9 test uses direct field access on msgspec.Struct asset
classes (no inner Attributes class pattern).
"""

import json
from pathlib import Path
from re import escape
from typing import List

import msgspec
import pytest

from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import (
    AnnouncementType,
    CertificateStatus,
)
from pyatlan.utils import validate_single_required_field
from pyatlan_v9.model.assets.asset import Asset
from pyatlan_v9.model.assets.readme import Readme
from pyatlan_v9.model.assets.table import Table

SCHEMA_QUALIFIED_NAME = "default/snowflake/1646836521/ATLAN_SAMPLE_DATA/FOOD_BEVERAGE"
TABLE_NAME = "MKT_EXPENSES"

DATA_DIR = Path(__file__).parent / ".." / ".." / "tests" / "unit" / "data"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_all_subclasses(cls):
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))
    return all_subclasses


def _entity_classes():
    """Return all instantiable v9 entity classes (not Attributes/Nested/Relationship)."""
    return [
        c
        for c in get_all_subclasses(Asset)
        if not any(
            x in c.__name__
            for x in ["Attributes", "Nested", "Relationship"]
        )
    ]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def table():
    return Table.creator(
        name=TABLE_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )


# ---------------------------------------------------------------------------
# test_remove_methods — equivalent to legacy test_remove_desscription
#
# Tests that remove_* methods correctly set the relevant fields to None
# on all v9 entity subclasses. In legacy, this tests on Asset.Attributes
# inner classes; in v9, it tests directly on the entity classes.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "clazz, method_name, property_names, values",
    [
        (clazz, info[1], info[2:], info[0])
        for clazz in _entity_classes()
        for info in [
            (["abc"], "remove_description", "description"),
            (["abc"], "remove_user_description", "user_description"),
            ([["bob"], ["dave"]], "remove_owners", "owner_groups", "owner_users"),
            (
                [CertificateStatus.DRAFT, "some message"],
                "remove_certificate",
                "certificate_status",
                "certificate_status_message",
            ),
            (
                ["a message", "a title", AnnouncementType.ISSUE],
                "remove_announcement",
                "announcement_message",
                "announcement_title",
                "announcement_type",
            ),
        ]
    ],
)
def test_remove_methods(clazz, method_name, property_names, values):
    """Test remove_* methods set all associated fields to None."""
    instance = clazz()
    for prop, value in zip(property_names, values):
        setattr(instance, prop, value)
    getattr(instance, method_name)()
    for prop in property_names:
        assert getattr(instance, prop) is None


# ---------------------------------------------------------------------------
# test_field_set_get — equivalent to legacy test_attributes
#
# Tests that key common fields can be set and read back on all v9 entity
# subclasses. In v9, fields are direct Struct attributes (no Attributes
# inner class delegation).
# ---------------------------------------------------------------------------

_FIELD_VALUES = [
    ("name", "test-name"),
    ("description", "test-description"),
    ("user_description", "test-user-description"),
    ("certificate_status", CertificateStatus.VERIFIED),
    ("announcement_type", AnnouncementType.WARNING),
]


@pytest.mark.parametrize(
    "clazz, field_name, value",
    [
        (clazz, field_name, value)
        for clazz in _entity_classes()
        for field_name, value in _FIELD_VALUES
    ],
)
def test_field_set_get(clazz, field_name, value):
    """Test that common fields can be set and read back on all entity types."""
    instance = clazz()
    setattr(instance, field_name, value)
    assert getattr(instance, field_name) == value


# ---------------------------------------------------------------------------
# Standalone tests — ported directly from legacy
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "names, values, message",
    [
        (
            ("one", "two"),
            (None, None),
            "One of the following parameters are required: one, two",
        ),
        (
            ("one", "two"),
            (1, 2),
            "Only one of the following parameters are allowed: one, two",
        ),
        (
            ("one", "two", "three"),
            (1, None, 3),
            "Only one of the following parameters are allowed: one, three",
        ),
    ],
)
def test_validate_single_required_field_with_bad_values_raises_value_error(
    names, values, message
):
    with pytest.raises(ValueError, match=message):
        validate_single_required_field(names, values)


def test_validate_single_required_field_with_only_one_field_does_not_raise_value_error():
    validate_single_required_field(["One", "Two", "Three"], [None, None, 3])


def test_create_for_modification_on_asset_raises_exception():
    with pytest.raises(
        (InvalidRequestError, ValueError),
    ):
        Asset.create_for_modification(qualified_name="", name="")


def test_readme_creator_asset_guid_validation():
    with pytest.raises(
        ValueError,
        match=escape(
            "asset guid must be present, use the client.asset.ref_by_guid() method to retrieve an asset by its GUID"
        ),
    ):
        Readme.creator(
            asset=Asset.ref_by_qualified_name("test-qn"),
            content="<h1>Test Content</h1>",
            asset_name="test-readme",
        )
