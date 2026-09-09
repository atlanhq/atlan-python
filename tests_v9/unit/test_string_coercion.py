# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
"""Tests for ``lenient_strings`` decoding.

Atlas's ``string`` type accepts any value and stores its stringification
(``AtlasBuiltInTypes.AtlasStringType``: ``isValidValue`` returns ``true``,
``getNormalizedValue`` returns ``obj.toString()``).  The generated models mirror
the declared Atlas type but not that leniency, so a producer that has not been
through Atlas's normalisation gets whole records rejected over one value.

Every payload shape below was observed in connector output that Atlas itself
accepted.
"""

from __future__ import annotations

import json

import msgspec
import pytest

from pyatlan_v9.model.transform import (
    from_atlas_format,
    from_atlas_json,
    get_type,
)


def _column(custom: object, *, omit: bool = False) -> dict:
    entity = {
        "typeName": "Column",
        "attributes": {"name": "c1", "qualifiedName": "default/db/sch/tbl/c1"},
    }
    if not omit:
        entity["customAttributes"] = custom
    return entity


# ---------------------------------------------------------------------------
# Dict[str, str] - the entity-header ``customAttributes`` slot
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("custom", "expected"),
    [
        pytest.param({"type_name": "int4"}, {"type_name": "int4"}, id="already-str"),
        pytest.param({"ordinal_position": 1}, {"ordinal_position": "1"}, id="int"),
        pytest.param({"len": -1.0}, {"len": "-1.0"}, id="float"),
        # JSON text, so "true" - matching what Atlas stores, not Python's repr.
        pytest.param({"is_secure": True}, {"is_secure": "true"}, id="bool"),
        # Dropped, not stringified: "null" is a value the producer never wrote.
        pytest.param({"numeric_precision": None}, {}, id="null-value"),
        pytest.param({"a": 1, "b": None, "c": "x"}, {"a": "1", "c": "x"}, id="mixed"),
        pytest.param({}, {}, id="empty"),
        # A container in a string slot: Atlas would store Java's toString();
        # this stores compact JSON.
        pytest.param({"k": {"n": "o"}}, {"k": '{"n":"o"}'}, id="nested-object"),
        pytest.param({"k": [1, 2]}, {"k": "[1,2]"}, id="nested-array"),
    ],
)
def test_string_map_values_are_coerced(custom, expected):
    asset = from_atlas_format(_column(custom), lenient_strings=True)

    assert asset.custom_attributes == expected


def test_null_map_is_dropped_because_the_slot_is_not_optional():
    """``Dict[str, str]`` with no ``None`` member cannot hold an explicit null."""
    asset = from_atlas_format(_column(None), lenient_strings=True)

    assert asset.custom_attributes is msgspec.UNSET


def test_absent_map_is_untouched():
    asset = from_atlas_format(_column(None, omit=True), lenient_strings=True)

    assert asset.custom_attributes is msgspec.UNSET


def test_non_mapping_payload_still_raises():
    """No sane coercion exists, and inventing one would hide producer drift."""
    with pytest.raises(msgspec.ValidationError):
        from_atlas_format(_column("not-a-map"), lenient_strings=True)


# ---------------------------------------------------------------------------
# List[Dict[str, str]] - a typedef attribute (``array<map<string,string>>``)
# ---------------------------------------------------------------------------


def _datasource_field(upstream: object) -> dict:
    return {
        "typeName": "TableauDatasourceField",
        "attributes": {
            "name": "f",
            "qualifiedName": "default/tableau/1/p/ds/f",
            "upstreamColumns": upstream,
        },
    }


@pytest.mark.parametrize(
    ("upstream", "expected"),
    [
        pytest.param([{"id": "7"}], [{"id": "7"}], id="already-str"),
        pytest.param([{"id": 7}], [{"id": "7"}], id="int"),
        pytest.param(
            [{"col": {"nested": "obj"}}], [{"col": '{"nested":"obj"}'}], id="object"
        ),
        pytest.param([{"a": 1}, {"b": None}], [{"a": "1"}, {}], id="ragged"),
        pytest.param([], [], id="empty"),
    ],
)
def test_list_of_string_maps_is_coerced(upstream, expected):
    asset = from_atlas_format(_datasource_field(upstream), lenient_strings=True)

    assert asset.upstream_columns == expected


# ---------------------------------------------------------------------------
# Plain ``str`` slots, and nullability
# ---------------------------------------------------------------------------


def test_scalar_in_a_plain_string_slot_is_coerced():
    entity = {
        "typeName": "Column",
        "attributes": {"name": 12345, "qualifiedName": "default/db/sch/tbl/c1"},
    }

    asset = from_atlas_format(entity, lenient_strings=True)

    assert asset.name == "12345"


def test_null_is_preserved_in_an_optional_string_slot():
    """``name`` is ``Union[str, None]``; a declared null is a real value there."""
    entity = {
        "typeName": "Column",
        "attributes": {"name": None, "qualifiedName": "default/db/sch/tbl/c1"},
    }

    asset = from_atlas_format(entity, lenient_strings=True)

    assert asset.name is None


# ---------------------------------------------------------------------------
# Nested related structs - the shape a name-keyed fixup would miss
# ---------------------------------------------------------------------------


def test_nested_related_struct_is_coerced():
    """``RelatedTableauDatasourceField.upstream_columns`` is a typed slot too.

    It is reached through a relationship attribute, not the top level, so the
    coercion has to follow the model's own nesting.
    """
    entity = {
        "typeName": "TableauWorksheet",
        "attributes": {"name": "w", "qualifiedName": "default/tableau/1/p/wb/w"},
        "relationshipAttributes": {
            "datasourceFields": [
                {
                    "typeName": "TableauDatasourceField",
                    "guid": "abc",
                    "attributes": {
                        "name": "f",
                        "upstreamColumns": [{"id": 7}],
                    },
                }
            ]
        },
    }

    asset = from_atlas_format(entity, lenient_strings=True)

    assert asset.datasource_fields[0].upstream_columns == [{"id": "7"}]


# ---------------------------------------------------------------------------
# The flag is off by default, and genuine breakage still raises
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "entity",
    [
        pytest.param(_column({"ordinal_position": 1}), id="int-in-map"),
        pytest.param(_datasource_field([{"col": {"n": "o"}}]), id="object-in-list-map"),
    ],
)
def test_default_is_unchanged(entity):
    """Decoding an Atlas API response must behave exactly as before."""
    with pytest.raises(msgspec.ValidationError):
        from_atlas_format(entity)

    with pytest.raises(msgspec.ValidationError):
        from_atlas_json(json.dumps(entity).encode())


@pytest.mark.parametrize(
    "entity",
    [
        pytest.param(
            {
                "typeName": "Column",
                "attributes": {"name": "c1", "order": {"not": "an int"}},
            },
            id="wrong-typed-non-string-field",
        ),
        pytest.param(
            {
                "typeName": "Column",
                "attributes": {"name": "c1"},
                "createTime": {"not": "an int"},
            },
            id="wrong-typed-top-level-field",
        ),
    ],
)
def test_non_string_slots_are_left_strict(entity):
    """Leniency is confined to ``str`` slots; everything else still raises."""
    with pytest.raises(msgspec.ValidationError):
        from_atlas_format(entity, lenient_strings=True)


def test_malformed_json_still_raises():
    with pytest.raises(msgspec.DecodeError):
        from_atlas_json(b"{not json", lenient_strings=True)


def test_json_entry_point_applies_the_flag():
    asset = from_atlas_json(
        json.dumps(_column({"ordinal_position": 1})).encode(), lenient_strings=True
    )

    assert asset.custom_attributes == {"ordinal_position": "1"}


def test_wrapped_entity_shape_applies_the_flag():
    payload = {"entity": _column({"ordinal_position": 1})}

    asset = from_atlas_json(json.dumps(payload).encode(), lenient_strings=True)

    assert asset.custom_attributes == {"ordinal_position": "1"}


# ---------------------------------------------------------------------------
# The plan is derived from the model, not a hand-maintained field list
# ---------------------------------------------------------------------------


def test_plan_covers_every_string_map_field_of_a_type():
    """A new ``map<string,string>`` typedef attribute is covered on regeneration.

    Guards the property that matters: the plan comes from the model, so nothing
    has to be added here when the models are regenerated.
    """
    from pyatlan_v9.model.string_coercion import _plan_for

    plan = _plan_for(get_type("TableauDatasourceField"))

    assert "upstreamColumns" in plan
    assert "upstreamFields" in plan
    assert "customAttributes" in plan
    assert "qualifiedName" in plan


def test_plan_is_cached_per_class():
    from pyatlan_v9.model.string_coercion import _plan_for

    cls = get_type("Column")

    assert _plan_for(cls) is _plan_for(cls)
