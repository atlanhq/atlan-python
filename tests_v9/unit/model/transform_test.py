# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Unit tests for to_atlas_format null handling in pyatlan_v9 (AICHAT-1884).

to_atlas_format must agree with to_nested_bytes across the three field states:
UNSET stays absent, an explicit None is kept as a JSON null, and a real value is
preserved. Before the fix, to_atlas_format silently dropped explicit nulls, so a
caller clearing a value (asset.description = None) had that instruction discarded.
"""

import json

import pytest

from pyatlan_v9.model.assets import Column, Table, View
from pyatlan_v9.model.transform import to_atlas_format

SCHEMA_QN = "default/mysql/1/db/sch"
TABLE_QN = f"{SCHEMA_QN}/tbl"

# (python attr, atlas wire key, sample value) spanning str / int / bool.
TABLE_FIELDS = [
    ("description", "description", "a description"),
    ("row_count", "rowCount", 42),
    ("is_partitioned", "isPartitioned", True),
]


def _table(state=None):
    asset = Table.creator(name="T1", schema_qualified_name=SCHEMA_QN)
    if state == "none":
        for attr, _wire, _value in TABLE_FIELDS:
            setattr(asset, attr, None)
    elif state == "value":
        for attr, _wire, value in TABLE_FIELDS:
            setattr(asset, attr, value)
    return asset


def _view():
    return View.creator(name="V1", schema_qualified_name=SCHEMA_QN)


def _column():
    return Column.creator(
        name="C1", parent_qualified_name=TABLE_QN, parent_type=Table, order=1
    )


def _nested_attrs(asset):
    return json.loads(asset.to_nested_bytes()).get("attributes", {})


def _atlas_attrs(asset):
    return to_atlas_format(asset).get("attributes", {})


# ---------------------------------------------------------------------------
# Core: the three states agree across both encoders (Table, all field types)
# ---------------------------------------------------------------------------


def test_unset_fields_absent_in_both_encoders():
    """UNSET fields never reach either encoder's output."""
    asset = _table()
    nested, atlas = _nested_attrs(asset), _atlas_attrs(asset)
    for _attr, wire, _value in TABLE_FIELDS:
        assert wire not in nested
        assert wire not in atlas


def test_explicit_null_preserved_in_both_encoders():
    """Explicitly-set None is kept as a JSON null — the AICHAT-1884 fix."""
    asset = _table("none")
    nested, atlas = _nested_attrs(asset), _atlas_attrs(asset)
    for _attr, wire, _value in TABLE_FIELDS:
        assert nested[wire] is None
        assert atlas[wire] is None  # silently dropped before the fix


def test_real_values_preserved_in_both_encoders():
    """Real values agree across both encoders."""
    asset = _table("value")
    nested, atlas = _nested_attrs(asset), _atlas_attrs(asset)
    for _attr, wire, value in TABLE_FIELDS:
        assert nested[wire] == value
        assert atlas[wire] == value


# ---------------------------------------------------------------------------
# Cross-type: the fix is not Table-specific
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("builder", [_view, _column], ids=["View", "Column"])
def test_explicit_null_preserved_across_asset_types(builder):
    """A cleared description survives to_atlas_format for other asset types too."""
    asset = builder()
    asset.description = None
    assert _nested_attrs(asset)["description"] is None
    assert _atlas_attrs(asset)["description"] is None


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_falsy_but_not_null_values_are_kept():
    """False / 0 / "" are values, not nulls — they must not be dropped."""
    asset = Table.creator(name="T1", schema_qualified_name=SCHEMA_QN)
    asset.is_partitioned = False
    asset.row_count = 0
    asset.description = ""
    atlas = _atlas_attrs(asset)
    assert atlas["isPartitioned"] is False
    assert atlas["rowCount"] == 0
    assert atlas["description"] == ""


def test_mixed_states_on_one_asset():
    """UNSET absent, None kept as null, value kept — all on the same asset."""
    asset = Table.creator(name="T1", schema_qualified_name=SCHEMA_QN)
    asset.description = None  # explicit null
    asset.row_count = 42  # value
    # is_partitioned left UNSET
    atlas = _atlas_attrs(asset)
    assert atlas["description"] is None
    assert atlas["rowCount"] == 42
    assert "isPartitioned" not in atlas


def test_attributes_block_present_when_only_an_explicit_null_is_set():
    """An asset whose only set attribute is a cleared one still emits attributes.

    Before the fix the null was dropped, leaving attributes empty and omitted —
    so the clear vanished entirely from the payload.
    """
    asset = Table.creator(name="T1", schema_qualified_name=SCHEMA_QN)
    asset.description = None
    result = to_atlas_format(asset)
    assert "attributes" in result
    assert result["attributes"]["description"] is None


@pytest.mark.parametrize("state", ["unset", "none", "value"])
def test_encoders_agree_per_field_in_every_state(state):
    """For each tested field, to_atlas_format matches to_nested_bytes in all
    three states (scoped to the fields under test; relationship attributes set by
    the creator are encoded differently by the two and are out of scope here)."""
    asset = _table(None if state == "unset" else state)
    nested, atlas = _nested_attrs(asset), _atlas_attrs(asset)
    for _attr, wire, _value in TABLE_FIELDS:
        assert (wire in nested) == (wire in atlas)
        assert nested.get(wire) == atlas.get(wire)


def test_unset_asset_has_no_attributes_block():
    """A freshly-created asset with no touched attributes emits no null noise."""
    asset = Table.creator(name="T1", schema_qualified_name=SCHEMA_QN)
    result = to_atlas_format(asset)
    # name/qualifiedName from the creator are real values, so attributes exists,
    # but it must carry no null entries.
    assert None not in result.get("attributes", {}).values()
