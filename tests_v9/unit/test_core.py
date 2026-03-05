# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Unit tests for pyatlan_v9 core types.

Ported from tests/unit/test_core.py. Key differences from the original:

- TestAtlanTag: Uses direct keyword construction with AtlanTagName instead of
  dict-based Pydantic construction. No mock_tag_cache or client fixtures needed
  since msgspec does not trigger cache lookups during validation.
- TestMsgspecExtraFields: Replaces TestAtlanObjectExtraFields. Tests msgspec
  behavior of ignoring unknown fields during deserialization (vs Pydantic's
  Extra.ignore + __atlan_extra__ pattern).
- TestPyatlanVersion: Unchanged — tests pyatlan.__version__ which is shared.
"""

from __future__ import annotations

from typing import Union

import msgspec

from pyatlan_v9.model.core import AtlanTag, AtlanTagName


class _Inner(msgspec.Struct, kw_only=True, rename="camel"):
    old_attr: str


class _Outer(msgspec.Struct, kw_only=True, rename="camel"):
    old: str
    attributes: Union[_Inner, None] = None


class _AtlanFieldModel(msgspec.Struct, kw_only=True, rename="camel"):
    name: str
    atlan_field: str


class _AttrInner(msgspec.Struct, kw_only=True, rename="camel"):
    old_attr: str


class _AttrOuter(msgspec.Struct, kw_only=True, rename="camel"):
    old: str
    attributes: _AttrInner


# ---------------------------------------------------------------------------
# TestAtlanTag
# ---------------------------------------------------------------------------


class TestAtlanTag:
    """Tests for AtlanTag creation and AtlanTagName sentinel handling."""

    def test_atlan_tag_when_tag_name_is_found(self):
        sut = AtlanTag(type_name=AtlanTagName("123"))
        assert str(sut.type_name) == "123"

    def test_atlan_tag_when_tag_name_is_empty_then_sentinel_is_returned(self):
        # Empty string should map to deleted sentinel
        sut = AtlanTag(type_name=AtlanTagName.get_deleted_sentinel())
        assert sut.type_name == AtlanTagName.get_deleted_sentinel()


# ---------------------------------------------------------------------------
# TestAtlanObjectExtraFields
# ---------------------------------------------------------------------------


class TestAtlanObjectExtraFields:
    """
    Tests that msgspec structs properly handle unknown/extra fields during
    deserialization. In msgspec, extra fields are simply ignored by default
    (there is no __atlan_extra__ dict equivalent).
    """

    def test_msgspec_struct_ignores_unknown_fields(self):
        class TestModel(msgspec.Struct, kw_only=True, rename="camel"):
            name: str

        # Decode with extra fields - should work fine (ignored)
        data = b'{"name": "test", "unknownField": 123}'
        result = msgspec.json.decode(data, type=TestModel)
        assert result.name == "test"

    def test_msgspec_struct_known_fields(self):
        class TestModel(msgspec.Struct, kw_only=True, rename="camel"):
            name: str
            value: Union[int, None] = None

        data = b'{"name": "test", "value": 42}'
        result = msgspec.json.decode(data, type=TestModel)
        assert result.name == "test"
        assert result.value == 42

    def test_msgspec_struct_known_fields_with_none_default(self):
        class TestModel(msgspec.Struct, kw_only=True, rename="camel"):
            name: str
            value: Union[int, None] = None

        data = b'{"name": "test"}'
        result = msgspec.json.decode(data, type=TestModel)
        assert result.name == "test"
        assert result.value is None

    def test_msgspec_struct_ignores_extra_nested_fields(self):
        data = b'{"old": "oldValue", "new": "newValue", "attributes": {"oldAttr": "oldValueAttr", "newAttr": "newValueAttr"}}'
        result = msgspec.json.decode(data, type=_Outer)

        # Known fields are properly deserialized
        assert result.old == "oldValue"
        assert result.attributes is not None
        assert result.attributes.old_attr == "oldValueAttr"

    def test_msgspec_struct_camel_case_rename(self):
        class TestModel(msgspec.Struct, kw_only=True, rename="camel"):
            my_field: str
            another_value: Union[int, None] = None

        # JSON uses camelCase, Python uses snake_case
        data = b'{"myField": "hello", "anotherValue": 99}'
        result = msgspec.json.decode(data, type=TestModel)
        assert result.my_field == "hello"
        assert result.another_value == 99

    def test_msgspec_struct_serialization_excludes_unknown_fields(self):
        class TestModel(msgspec.Struct, kw_only=True, rename="camel"):
            name: str

        # Decode with extra fields
        data = b'{"name": "test", "unknownField": 123, "anotherUnknown": "abc"}'
        result = msgspec.json.decode(data, type=TestModel)

        # Serialization only includes known fields
        encoded = msgspec.json.decode(msgspec.json.encode(result))
        assert encoded == {"name": "test"}

    def test_atlan_api_response(self):
        """Parity check for legacy AtlanObject extra-field behavior under msgspec."""

        class TestResponse(msgspec.Struct, kw_only=True, rename="camel"):
            name: str

        test_data = {"name": "test"}
        response = msgspec.convert(test_data, type=TestResponse)
        assert msgspec.to_builtins(response) == test_data

        test_data_extra = {"name": "test", "new1": 123, "new2": 456}
        response = msgspec.convert(test_data_extra, type=TestResponse)
        assert msgspec.to_builtins(response) == test_data

        test_data_extra_nested = {
            "name": "test",
            "new1": {"new2": [1, 2, 3]},
            "new3": "abc",
        }
        response = msgspec.convert(test_data_extra_nested, type=TestResponse)
        assert msgspec.to_builtins(response) == test_data

        test_data_contains_atlan_field = {
            "name": "test",
            "atlanField": "test_value",
            "__atlan_extra__": "ignored",
        }
        response = msgspec.convert(
            test_data_contains_atlan_field, type=_AtlanFieldModel
        )
        assert response.name == test_data_contains_atlan_field["name"]
        assert response.atlan_field == "test_value"

        test_attr_raw_data = {
            "old": "oldValue",
            "new": "newValue",
            "attributes": {"oldAttr": "oldValueAttr", "newAttr": "newValueAttr"},
        }
        response = msgspec.convert(test_attr_raw_data, type=_AttrOuter)
        assert msgspec.to_builtins(response) == {
            "old": "oldValue",
            "attributes": {"oldAttr": "oldValueAttr"},
        }
        assert response.old == "oldValue"
        assert response.attributes.old_attr == "oldValueAttr"


# ---------------------------------------------------------------------------
# TestPyatlanVersion
# ---------------------------------------------------------------------------


class TestPyatlanVersion:
    """Tests for pyatlan.__version__ attribute."""

    def test_pyatlan_has_version_attribute(self):
        """Test that pyatlan module has __version__ attribute"""
        import pyatlan

        assert hasattr(pyatlan, "__version__")
        assert pyatlan.__version__ is not None
        assert isinstance(pyatlan.__version__, str)
        assert pyatlan.__version__ != "unknown"

    def test_pyatlan_version_format(self):
        """Test that the version follows semantic versioning format"""
        import re

        import pyatlan

        # Check if version matches semantic versioning pattern (x.y.z)
        version_pattern = r"^\d+\.\d+\.\d+.*$"
        assert re.match(version_pattern, pyatlan.__version__)

    def test_pyatlan_version_accessibility(self):
        """Test that version can be accessed after import"""
        import pyatlan

        # Version should be accessible immediately after import
        version = pyatlan.__version__
        assert version is not None
        assert len(version) > 0
