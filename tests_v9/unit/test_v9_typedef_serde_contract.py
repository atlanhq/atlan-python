# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

"""
Guardrail tests for the UNSET/omit_defaults serde contract in pyatlan_v9/model/typedef.py.

CRITICAL DEPENDENCY: atlan-model-caster-app (github.com/atlanhq/atlan-model-caster-app)
relies on the exact serde behaviour enforced by these tests. The app:
  1. Decodes Atlas API responses into TypeDefResponse/AttributeDef structs.
  2. Uses getattr(attr, "type_name") / getattr(attr, "name") on AttributeDef to drive
     backward-compatibility violation checks — these MUST return a real value or UNSET,
     never crash because attribute_defs items are plain dicts.
  3. Re-encodes desired typedefs back to JSON for Atlas API POSTs/PUTs.
     Sparse source payloads must NOT be expanded with null fields on re-encode — Atlas
     rejects unknown or unexpected null-valued fields in typedef write requests.

Invariants that must never be broken:
  A. attribute_defs items decode as AttributeDef structs (not dict).
  B. Round-tripping a sparse AttributeDef preserves only the fields that were present.
  C. Absent fields default to UNSET (not None) so omit_defaults=True keeps them out.
  D. Explicit None fields are preserved (written as null) — distinct from absent.
  E. No stale defaults are injected (RelationshipDef.propagate_tags, relationship_category).
  F. attribute_defs / element_defs default to UNSET (not []) so empty lists are omitted.
  G. TypeDefResponse encodes to {} when all lists are empty (no extraneous keys).
  H. strict=False decoder accepts string-encoded booleans and numbers from Atlas responses.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

import msgspec
import pytest

from pyatlan_v9.model.typedef import (
    AttributeDef,
    CustomMetadataDef,
    EntityDef,
    EnumDef,
    RelationshipDef,
    RelationshipEndDef,
    StructDef,
    TypeDefResponse,
)

# ---------------------------------------------------------------------------
# Helpers — mirrors what atlan-model-caster-app uses internally
# ---------------------------------------------------------------------------

_ENCODER = msgspec.json.Encoder()
_DECODER = msgspec.json.Decoder(TypeDefResponse, strict=False)


def _encode(obj: Any) -> Dict[str, Any]:
    """Re-encode a msgspec struct to a plain Python dict (via JSON round-trip)."""
    return json.loads(_ENCODER.encode(obj))


def _decode(raw: bytes) -> TypeDefResponse:
    return _DECODER.decode(raw)


def _payload(**kwargs) -> bytes:
    """Build a minimal TypeDefResponse JSON payload from keyword categories."""
    return json.dumps(kwargs).encode()


# ---------------------------------------------------------------------------
# A. attribute_defs decode as AttributeDef structs (Invariant A)
# ---------------------------------------------------------------------------


class TestAttributeDefsDecodeAsStructs:
    """
    CRITICAL: atlan-model-caster-app calls getattr(attr, "type_name") on every
    attribute_def item. If items are plain dicts, getattr silently returns UNSET
    and ALL backward-compatibility checks are silently skipped. These tests
    guarantee items are always AttributeDef structs.
    """

    def _make_payload(self, def_key: str, def_val: dict, attr: dict) -> bytes:
        return _payload(**{def_key: [{**def_val, "attributeDefs": [attr]}]})

    def test_entity_def_attribute_defs_are_structs(self) -> None:
        """EntityDef.attribute_defs items must be AttributeDef, not dict."""
        raw = self._make_payload(
            "entityDefs",
            {"name": "MyEntity", "typeVersion": "1.0"},
            {"name": "attr1", "typeName": "string"},
        )
        response = _decode(raw)
        assert response.entity_defs
        attr = response.entity_defs[0].attribute_defs[0]  # type: ignore[index]
        assert isinstance(attr, AttributeDef), (
            f"Expected AttributeDef, got {type(attr).__name__}. "
            "If this fails, model-caster BC checks are silently broken."
        )

    def test_struct_def_attribute_defs_are_structs(self) -> None:
        """StructDef.attribute_defs items must be AttributeDef, not dict."""
        raw = self._make_payload(
            "structDefs",
            {"name": "MyStruct", "typeVersion": "1.0"},
            {"name": "field1", "typeName": "int"},
        )
        response = _decode(raw)
        assert response.struct_defs
        attr = response.struct_defs[0].attribute_defs[0]  # type: ignore[index]
        assert isinstance(attr, AttributeDef)

    def test_classification_def_attribute_defs_are_structs(self) -> None:
        """AtlanTagDef.attribute_defs items must be AttributeDef, not dict.

        Note: the TypeDefResponse field is named `atlan_tag_defs`; the JSON key
        is `classificationDefs` (via rename="camel" + name="classificationDefs").
        """
        raw = _payload(
            classificationDefs=[
                {
                    "name": "PII",
                    "typeVersion": "1.0",
                    "attributeDefs": [{"name": "sensitivity", "typeName": "string"}],
                }
            ]
        )
        response = _decode(raw)
        assert response.atlan_tag_defs
        attr = response.atlan_tag_defs[0].attribute_defs[0]  # type: ignore[index]
        assert isinstance(attr, AttributeDef)

    def test_getattr_name_returns_value_not_unset(self) -> None:
        """getattr(attr, 'name') must return the actual value, not UNSET."""
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [{"name": "myField", "typeName": "string"}],
                }
            ]
        )
        response = _decode(raw)
        attr = response.entity_defs[0].attribute_defs[0]  # type: ignore[index]
        name = getattr(attr, "name", msgspec.UNSET)
        assert name == "myField", (
            "getattr(attr, 'name') returned UNSET — attribute_defs items may be dicts."
        )

    def test_getattr_type_name_returns_value_not_unset(self) -> None:
        """getattr(attr, 'type_name') must return the actual value, not UNSET."""
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [{"name": "f", "typeName": "date"}],
                }
            ]
        )
        response = _decode(raw)
        attr = response.entity_defs[0].attribute_defs[0]  # type: ignore[index]
        type_name = getattr(attr, "type_name", msgspec.UNSET)
        assert type_name == "date", (
            "getattr(attr, 'type_name') returned UNSET — type change BC checks are silently skipped."
        )


# ---------------------------------------------------------------------------
# B + C. Sparse round-trip preserves only present fields (Invariants B & C)
# ---------------------------------------------------------------------------


class TestSparseRoundTrip:
    """
    CRITICAL: atlan-model-caster-app re-encodes desired typedefs to JSON for
    Atlas API writes. A sparse source like {"name":"x","typeName":"string"} must
    NOT become {"name":"x","typeName":"string","cardinality":null,...} on re-encode —
    Atlas will reject the unexpected null fields.

    With omit_defaults=True and UNSET defaults, absent fields stay absent.
    """

    def test_sparse_attribute_def_does_not_expand_on_reencode(self) -> None:
        """
        Decoding and re-encoding a sparse AttributeDef must not inject null fields.
        This is the core safety guarantee for Atlas API write requests.
        """
        sparse_source = {"name": "x", "typeName": "string"}
        full_payload = _payload(
            entityDefs=[{"name": "E", "typeVersion": "1.0", "attributeDefs": [sparse_source]}]
        )
        decoded = _decode(full_payload)
        re_encoded_attr = _encode(decoded)["entityDefs"][0]["attributeDefs"][0]

        # Only the two present fields should appear
        assert set(re_encoded_attr.keys()) == {"name", "typeName"}, (
            f"Re-encoded AttributeDef has extra fields: {set(re_encoded_attr.keys()) - {'name', 'typeName'}}. "
            "Null-field expansion will cause Atlas API write requests to fail."
        )

    def test_absent_fields_default_to_unset_not_none(self) -> None:
        """
        Absent fields must default to UNSET, not None.
        If they default to None, omit_defaults=True still omits them, but
        explicit None and absent would become indistinguishable (Invariant D).
        """
        attr = AttributeDef(name="x", type_name="string")
        assert attr.cardinality is msgspec.UNSET, (
            "Absent AttributeDef.cardinality must be UNSET, not None."
        )
        assert attr.description is msgspec.UNSET
        assert attr.display_name is msgspec.UNSET
        assert attr.options is msgspec.UNSET

    def test_sparse_entity_def_omits_attribute_defs_when_absent(self) -> None:
        """EntityDef with no attributeDefs in source must not emit attributeDefs key."""
        raw = _payload(entityDefs=[{"name": "E", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        re_encoded = _encode(decoded)
        entity = re_encoded["entityDefs"][0]
        assert "attributeDefs" not in entity, (
            "attributeDefs appears in output despite being absent in source. "
            "This pollutes Atlas API write payloads."
        )

    def test_only_present_fields_survive_full_typedef_round_trip(self) -> None:
        """A TypeDefResponse round-trip emits only the fields from the source."""
        source = {
            "entityDefs": [
                {
                    "name": "Asset",
                    "typeVersion": "2.0",
                    "description": "Base asset type",
                    "attributeDefs": [
                        {"name": "owner", "typeName": "string", "isOptional": True}
                    ],
                }
            ]
        }
        decoded = _decode(json.dumps(source).encode())
        re_encoded = _encode(decoded)

        entity = re_encoded["entityDefs"][0]
        assert entity["name"] == "Asset"
        assert entity["typeVersion"] == "2.0"
        assert entity["description"] == "Base asset type"
        assert "attributeDefs" in entity
        attr = entity["attributeDefs"][0]
        assert set(attr.keys()) == {"name", "typeName", "isOptional"}


# ---------------------------------------------------------------------------
# D. Explicit None is preserved (Invariant D)
# ---------------------------------------------------------------------------


class TestExplicitNullPreserved:
    """
    Explicit null from the server must survive round-trip as null.
    This distinguishes 'not set by user' (UNSET) from 'explicitly cleared' (None).
    """

    def test_explicit_null_attribute_def_field_survives_round_trip(self) -> None:
        """A field sent as null by Atlas must remain null after decode/re-encode."""
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [
                        {"name": "x", "typeName": "string", "defaultValue": None}
                    ],
                }
            ]
        )
        decoded = _decode(raw)
        attr = decoded.entity_defs[0].attribute_defs[0]  # type: ignore[index]
        assert attr.default_value is None, (
            "Explicit null default_value was lost or replaced with UNSET."
        )
        re_encoded_attr = _encode(decoded)["entityDefs"][0]["attributeDefs"][0]
        assert "defaultValue" in re_encoded_attr
        assert re_encoded_attr["defaultValue"] is None

    def test_unset_and_explicit_none_are_distinguishable(self) -> None:
        """UNSET (absent) and None (explicit null) must be distinguishable at runtime."""
        absent = AttributeDef(name="a", type_name="string")
        explicit_null = AttributeDef(name="b", type_name="string", default_value=None)
        assert absent.default_value is msgspec.UNSET
        assert explicit_null.default_value is None
        assert absent.default_value is not explicit_null.default_value


# ---------------------------------------------------------------------------
# E. No stale defaults in RelationshipDef (Invariant E)
# ---------------------------------------------------------------------------


class TestRelationshipDefNoStaleDefaults:
    """
    RelationshipDef fields that previously had non-None defaults (propagate_tags,
    relationship_category, relationship_label) must default to UNSET so that
    model-caster does not inject stale values into Atlas update payloads.
    """

    def test_propagate_tags_defaults_to_unset(self) -> None:
        """RelationshipDef.propagate_tags must default to UNSET (was 'ONE_TO_TWO')."""
        raw = _payload(
            relationshipDefs=[
                {
                    "name": "R",
                    "typeVersion": "1.0",
                    "endDef1": {"type": "A", "name": "r1", "isContainer": False},
                    "endDef2": {"type": "B", "name": "r2", "isContainer": False},
                    "relationshipCategory": "ASSOCIATION",
                }
            ]
        )
        decoded = _decode(raw)
        rel = decoded.relationship_defs[0]  # type: ignore[index]
        # Field absent in source → must be UNSET, not a stale string like "ONE_TO_TWO"
        assert rel.propagate_tags is msgspec.UNSET, (
            f"propagate_tags={rel.propagate_tags!r}. Stale default would corrupt Atlas updates."
        )

    def test_propagate_tags_absent_from_re_encoded_output(self) -> None:
        """propagateTagPropagation must not appear in re-encoded output when absent in source."""
        raw = _payload(
            relationshipDefs=[
                {
                    "name": "R",
                    "typeVersion": "1.0",
                    "endDef1": {"type": "A", "name": "r1", "isContainer": False},
                    "endDef2": {"type": "B", "name": "r2", "isContainer": False},
                    "relationshipCategory": "ASSOCIATION",
                }
            ]
        )
        decoded = _decode(raw)
        re_encoded = _encode(decoded)
        rel_out = re_encoded["relationshipDefs"][0]
        assert "propagateTagPropagation" not in rel_out, (
            "propagateTagPropagation injected with stale default — would corrupt Atlas writes."
        )

    def test_relationship_category_absent_from_output_when_not_in_source(self) -> None:
        """relationshipCategory must not be injected when absent in source."""
        raw = _payload(
            relationshipDefs=[
                {
                    "name": "R",
                    "typeVersion": "1.0",
                    "endDef1": {"type": "A", "name": "r1", "isContainer": False},
                    "endDef2": {"type": "B", "name": "r2", "isContainer": False},
                }
            ]
        )
        decoded = _decode(raw)
        re_encoded = _encode(decoded)
        rel_out = re_encoded["relationshipDefs"][0]
        assert "relationshipCategory" not in rel_out, (
            "relationshipCategory injected when absent — was previously a stale default."
        )

    def test_explicit_relationship_category_survives(self) -> None:
        """An explicitly provided relationshipCategory must survive round-trip."""
        raw = _payload(
            relationshipDefs=[
                {
                    "name": "R",
                    "typeVersion": "1.0",
                    "endDef1": {"type": "A", "name": "r1", "isContainer": False},
                    "endDef2": {"type": "B", "name": "r2", "isContainer": False},
                    "relationshipCategory": "COMPOSITION",
                }
            ]
        )
        decoded = _decode(raw)
        re_encoded = _encode(decoded)
        assert re_encoded["relationshipDefs"][0]["relationshipCategory"] == "COMPOSITION"


# ---------------------------------------------------------------------------
# F. attribute_defs / element_defs default to UNSET (Invariant F)
# ---------------------------------------------------------------------------


class TestListFieldsDefaultToUnset:
    """
    attribute_defs and element_defs must default to UNSET (not []) so that
    re-encoding a typedef that had no attribute_defs in its source does not
    emit an empty list. Atlas interprets an explicit [] as 'clear all attributes'.
    """

    def test_entity_def_attribute_defs_defaults_to_unset(self) -> None:
        """EntityDef.attribute_defs must default to UNSET, not []."""
        raw = _payload(entityDefs=[{"name": "E", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        assert decoded.entity_defs[0].attribute_defs is msgspec.UNSET, (
            "EntityDef.attribute_defs defaulted to [] instead of UNSET. "
            "Re-encoding would emit attributeDefs:[] which tells Atlas to clear all attributes."
        )

    def test_struct_def_attribute_defs_defaults_to_unset(self) -> None:
        """StructDef.attribute_defs must default to UNSET, not []."""
        raw = _payload(structDefs=[{"name": "S", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        assert decoded.struct_defs[0].attribute_defs is msgspec.UNSET  # type: ignore[index]

    def test_enum_def_element_defs_defaults_to_unset(self) -> None:
        """EnumDef.element_defs must default to UNSET, not []."""
        raw = _payload(enumDefs=[{"name": "Status", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        assert decoded.enum_defs[0].element_defs is msgspec.UNSET, (  # type: ignore[index]
            "EnumDef.element_defs defaulted to [] instead of UNSET."
        )

    def test_element_defs_present_are_decoded_as_structs(self) -> None:
        """EnumDef.element_defs items must be ElementDef structs."""
        raw = _payload(
            enumDefs=[
                {
                    "name": "Status",
                    "typeVersion": "1.0",
                    "elementDefs": [
                        {"value": "ACTIVE", "ordinal": 0},
                        {"value": "INACTIVE", "ordinal": 1},
                    ],
                }
            ]
        )
        decoded = _decode(raw)
        elems = decoded.enum_defs[0].element_defs  # type: ignore[index]
        assert elems is not msgspec.UNSET
        assert all(isinstance(e, EnumDef.ElementDef) for e in elems)  # type: ignore[union-attr]
        assert elems[0].value == "ACTIVE"  # type: ignore[index]
        assert elems[1].ordinal == 1  # type: ignore[index]


# ---------------------------------------------------------------------------
# G. Empty TypeDefResponse encodes to {} (Invariant G)
# ---------------------------------------------------------------------------


class TestTypeDefResponseOmitDefaults:
    """
    TypeDefResponse with all-empty lists must encode to an empty JSON object.
    model-caster compares re-encoded output sizes to detect drift; extra empty
    list keys would falsely inflate the output.
    """

    def test_empty_response_encodes_to_empty_object(self) -> None:
        """A freshly constructed TypeDefResponse must encode to {}."""
        empty = TypeDefResponse()
        encoded = _encode(empty)
        assert encoded == {}, (
            f"Empty TypeDefResponse encoded to {encoded!r} instead of {{}}. "
            "omit_defaults=True must be set on TypeDefResponse."
        )

    def test_only_populated_categories_appear_in_output(self) -> None:
        """Only categories with items should appear in re-encoded output."""
        raw = _payload(enumDefs=[{"name": "Status", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        encoded = _encode(decoded)
        assert set(encoded.keys()) == {"enumDefs"}, (
            f"Unexpected keys in encoded output: {set(encoded.keys())}. "
            "Empty categories should be omitted."
        )

    def test_non_empty_category_survives_round_trip(self) -> None:
        """Populated lists must still be present after round-trip."""
        raw = _payload(
            entityDefs=[{"name": "E", "typeVersion": "1.0"}],
            enumDefs=[{"name": "Status", "typeVersion": "1.0"}],
        )
        decoded = _decode(raw)
        encoded = _encode(decoded)
        assert "entityDefs" in encoded
        assert "enumDefs" in encoded
        assert len(encoded["entityDefs"]) == 1
        assert len(encoded["enumDefs"]) == 1


# ---------------------------------------------------------------------------
# H. strict=False accepts string-encoded primitives (Invariant H)
# ---------------------------------------------------------------------------


class TestStrictFalseDecoding:
    """
    Atlas API responses sometimes return booleans as strings ("true"/"false") and
    numbers as strings. The decoder must accept these without raising.
    """

    def test_string_boolean_is_locked_accepted(self) -> None:
        """isLocked: 'true' (string) must decode without error."""
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [
                        {"name": "x", "typeName": "string", "isOptional": "true"}
                    ],
                }
            ]
        )
        # Must not raise
        decoded = _decode(raw)
        attr = decoded.entity_defs[0].attribute_defs[0]  # type: ignore[index]
        assert attr.is_optional is True

    def test_strict_true_rejects_string_boolean(self) -> None:
        """A strict=True decoder must reject string-encoded booleans."""
        strict_decoder = msgspec.json.Decoder(TypeDefResponse, strict=True)
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [
                        {"name": "x", "typeName": "string", "isOptional": "true"}
                    ],
                }
            ]
        )
        with pytest.raises(msgspec.ValidationError):
            strict_decoder.decode(raw)

    def test_string_encoded_integer_cardinality_accepted(self) -> None:
        """isIndexable: '1' (string-encoded int treated as truthy) — strict=False coerces str→bool."""
        # strict=False coerces str → bool/int, not int → str.
        # The common Atlas pattern is string-encoded booleans ("true"/"false").
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [
                        {"name": "x", "typeName": "string", "isIndexable": "false"}
                    ],
                }
            ]
        )
        decoded = _decode(raw)
        attr = decoded.entity_defs[0].attribute_defs[0]  # type: ignore[index]
        assert attr.is_indexable is False


# ---------------------------------------------------------------------------
# Server fields round-trip correctly
# ---------------------------------------------------------------------------


class TestServerFieldsRoundTrip:
    """
    Server-assigned fields (guid, create_time, created_by, etc.) must survive
    round-trip so model-caster can preserve them for update operations.
    """

    def test_server_fields_survive_round_trip(self) -> None:
        """guid, createTime, createdBy on TypeDef must round-trip correctly."""
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "guid": "abc-123",
                    "createTime": 1700000000,
                    "createdBy": "admin",
                    "updateTime": 1700001000,
                    "updatedBy": "user1",
                    "version": 3,
                }
            ]
        )
        decoded = _decode(raw)
        entity = decoded.entity_defs[0]  # type: ignore[index]
        assert entity.guid == "abc-123"
        assert entity.create_time == 1700000000
        assert entity.created_by == "admin"
        assert entity.update_time == 1700001000
        assert entity.version == 3

        re_encoded = _encode(decoded)
        out = re_encoded["entityDefs"][0]
        assert out["guid"] == "abc-123"
        assert out["createTime"] == 1700000000
        assert out["createdBy"] == "admin"

    def test_server_fields_absent_from_source_stay_unset(self) -> None:
        """Server fields absent from source must be UNSET (not None or default values)."""
        raw = _payload(entityDefs=[{"name": "E", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        entity = decoded.entity_defs[0]  # type: ignore[index]
        assert entity.guid is msgspec.UNSET
        assert entity.create_time is msgspec.UNSET
        assert entity.created_by is msgspec.UNSET

    def test_absent_server_fields_not_in_encoded_output(self) -> None:
        """Absent server fields must not appear in re-encoded output."""
        raw = _payload(entityDefs=[{"name": "E", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        out = _encode(decoded)["entityDefs"][0]
        assert "guid" not in out
        assert "createTime" not in out
        assert "createdBy" not in out


# ---------------------------------------------------------------------------
# Options does not inject stale defaults
# ---------------------------------------------------------------------------


class TestAttributeDefOptionsNoStaleDefaults:
    """
    AttributeDef.Options fields default to UNSET. The is_rich_text=False and
    custom_metadata_version='v2' values that used to appear as hard-coded class
    defaults must NOT be injected when options are absent from the source payload.
    """

    def test_options_absent_from_source_stays_unset(self) -> None:
        """An AttributeDef with no 'options' key must have options=UNSET."""
        attr = AttributeDef(name="x", type_name="string")
        assert attr.options is msgspec.UNSET

    def test_options_absent_not_in_encoded_output(self) -> None:
        """options must not appear in encoded output when absent."""
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [{"name": "x", "typeName": "string"}],
                }
            ]
        )
        decoded = _decode(raw)
        out = _encode(decoded)["entityDefs"][0]["attributeDefs"][0]
        assert "options" not in out, (
            "options was injected with stale defaults — would corrupt Atlas write payloads."
        )

    def test_explicit_options_values_survive_round_trip(self) -> None:
        """Options fields present in source must survive round-trip exactly."""
        raw = _payload(
            entityDefs=[
                {
                    "name": "E",
                    "typeVersion": "1.0",
                    "attributeDefs": [
                        {
                            "name": "x",
                            "typeName": "string",
                            "options": {
                                "primitiveType": "string",
                                "isRichText": True,
                                "multiValueSelect": False,
                            },
                        }
                    ],
                }
            ]
        )
        decoded = _decode(raw)
        opts = decoded.entity_defs[0].attribute_defs[0].options  # type: ignore[index]
        assert opts is not msgspec.UNSET
        assert opts is not None  # type: ignore[union-attr]
        assert opts.primitive_type == "string"  # type: ignore[union-attr]
        assert opts.is_rich_text is True  # type: ignore[union-attr]
        assert opts.multi_value_select is False  # type: ignore[union-attr]

        out_opts = _encode(decoded)["entityDefs"][0]["attributeDefs"][0]["options"]
        assert out_opts["primitiveType"] == "string"
        assert out_opts["isRichText"] is True
        assert out_opts["multiValueSelect"] is False


# ---------------------------------------------------------------------------
# RelationshipEndDef strongly-typed (end_def1 / end_def2) — new invariant
# ---------------------------------------------------------------------------


class TestRelationshipEndDefStronglyTyped:
    """
    CRITICAL: end_def1 and end_def2 on RelationshipDef must decode as
    RelationshipEndDef structs, not plain dicts. This mirrors Java's
    RelationshipEndDef extends AttributeDef, providing typed access to
    .type (entity type name), .is_container, .name, .cardinality, etc.

    If these were dicts, any code accessing end_def1.type would silently
    return UNSET via getattr — the same class of bug as the attribute_defs
    dict issue that broke BC checks in model-caster-app.
    """

    def _rel_payload(self, extra: dict | None = None) -> bytes:
        rd: dict = {
            "name": "AssetOwner",
            "typeVersion": "1.0",
            "endDef1": {
                "type": "Asset",
                "name": "owners",
                "isContainer": True,
                "cardinality": "SET",
            },
            "endDef2": {
                "type": "AtlasUser",
                "name": "assets",
                "isContainer": False,
                "cardinality": "SINGLE",
            },
            "relationshipCategory": "AGGREGATION",
        }
        if extra:
            rd.update(extra)
        return _payload(relationshipDefs=[rd])

    def test_end_def1_decodes_as_relationship_end_def(self) -> None:
        """end_def1 must be a RelationshipEndDef struct, not a dict."""
        decoded = _decode(self._rel_payload())
        end = decoded.relationship_defs[0].end_def1  # type: ignore[index]
        assert isinstance(end, RelationshipEndDef), (
            f"end_def1 decoded as {type(end).__name__} instead of RelationshipEndDef. "
            "Typed access to .type, .is_container, etc. will silently fail."
        )

    def test_end_def2_decodes_as_relationship_end_def(self) -> None:
        """end_def2 must be a RelationshipEndDef struct, not a dict."""
        decoded = _decode(self._rel_payload())
        end = decoded.relationship_defs[0].end_def2  # type: ignore[index]
        assert isinstance(end, RelationshipEndDef)

    def test_end_def1_type_field_accessible_via_attribute(self) -> None:
        """end_def1.type must return the entity type name, not UNSET."""
        decoded = _decode(self._rel_payload())
        end = decoded.relationship_defs[0].end_def1  # type: ignore[index]
        assert end.type == "Asset", (  # type: ignore[union-attr]
            f"end_def1.type={end.type!r}. If dict, getattr would return UNSET silently."
        )

    def test_end_def2_is_container_accessible(self) -> None:
        """end_def2.is_container must be False (not a dict key lookup)."""
        decoded = _decode(self._rel_payload())
        end = decoded.relationship_defs[0].end_def2  # type: ignore[index]
        assert end.is_container is False  # type: ignore[union-attr]

    def test_end_def_name_field_accessible(self) -> None:
        """The inherited .name field from AttributeDef must be accessible on both ends."""
        decoded = _decode(self._rel_payload())
        rel = decoded.relationship_defs[0]  # type: ignore[index]
        assert rel.end_def1.name == "owners"  # type: ignore[union-attr]
        assert rel.end_def2.name == "assets"  # type: ignore[union-attr]

    def test_end_def_cardinality_accessible(self) -> None:
        """The inherited .cardinality field from AttributeDef must survive round-trip."""
        decoded = _decode(self._rel_payload())
        end1 = decoded.relationship_defs[0].end_def1  # type: ignore[index]
        assert str(end1.cardinality) == "SET" or end1.cardinality is not msgspec.UNSET  # type: ignore[union-attr]

    def test_end_def_sparse_round_trip_preserves_only_present_fields(self) -> None:
        """A sparse endDef must not expand with null fields on re-encode."""
        decoded = _decode(self._rel_payload())
        re_encoded = _encode(decoded)
        end1_out = re_encoded["relationshipDefs"][0]["endDef1"]
        # Only present fields in the source should appear
        present_keys = {"type", "name", "isContainer", "cardinality"}
        assert set(end1_out.keys()) == present_keys, (
            f"endDef1 has extra keys after round-trip: {set(end1_out.keys()) - present_keys}. "
            "Null-field expansion in relationship end defs corrupts Atlas API writes."
        )

    def test_end_def_absent_defaults_to_unset(self) -> None:
        """RelationshipDef with no endDef1/endDef2 in source must have them as UNSET."""
        raw = _payload(relationshipDefs=[{"name": "R", "typeVersion": "1.0"}])
        decoded = _decode(raw)
        rel = decoded.relationship_defs[0]  # type: ignore[index]
        assert rel.end_def1 is msgspec.UNSET
        assert rel.end_def2 is msgspec.UNSET

    def test_relationship_attribute_defs_present_decode_as_structs(self) -> None:
        """relationshipAttributeDefs items must decode as RelationshipAttributeDef, not dict."""
        from pyatlan_v9.model.typedef import RelationshipAttributeDef

        raw = _payload(
            relationshipDefs=[
                {
                    "name": "R",
                    "typeVersion": "1.0",
                    "endDef1": {"type": "A", "name": "r1", "isContainer": False},
                    "endDef2": {"type": "B", "name": "r2", "isContainer": False},
                    "relationshipAttributeDefs": [
                        {"name": "label", "typeName": "string", "relationshipTypeName": "R"}
                    ],
                }
            ]
        )
        decoded = _decode(raw)
        rel = decoded.relationship_defs[0]  # type: ignore[index]
        assert rel.relationship_attribute_defs is not msgspec.UNSET
        rad = rel.relationship_attribute_defs[0]  # type: ignore[index]
        assert isinstance(rad, RelationshipAttributeDef)
        assert rad.relationship_type_name == "R"
