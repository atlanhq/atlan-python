from __future__ import annotations

from typing import no_type_check
from unittest.mock import call

import pytest
from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject, AtlanTag, AtlanTagName

DISPLAY_TEXT = "Something"


class TestAtlanTagName:
    def test_get_deleted_sentinel(self):
        sentinel = AtlanTagName.get_deleted_sentinel()

        assert "(DELETED)" == str(sentinel)
        assert id(sentinel) == id(AtlanTagName.get_deleted_sentinel())

    def test_atlan_tag_name_when_name_found_returns_atlan_tag_name(
        self, mock_tag_cache
    ):
        mock_tag_cache.get_id_for_name.return_value = "123"

        sut = AtlanTagName(DISPLAY_TEXT)

        assert DISPLAY_TEXT == str(sut)
        mock_tag_cache.get_id_for_name.assert_called_once_with(DISPLAY_TEXT)

    def test_atlan_tag_name_when_name_not_found_raise_value_error(self, mock_tag_cache):
        mock_tag_cache.get_id_for_name.return_value = None

        with pytest.raises(
            ValueError, match=f"{DISPLAY_TEXT} is not a valid Classification"
        ):
            AtlanTagName(DISPLAY_TEXT)

    def test_json_encode_atlan_tag_returns_internal_code(self, mock_tag_cache):
        internal_value = "123"
        mock_tag_cache.get_id_for_name.return_value = internal_value
        sut = AtlanTagName(DISPLAY_TEXT)

        assert internal_value == AtlanTagName.json_encode_atlan_tag(sut)
        mock_tag_cache.get_id_for_name.assert_has_calls(
            [call(DISPLAY_TEXT), call(DISPLAY_TEXT)]
        )


class TestAtlanTag:
    def test_atlan_tag_when_tag_name_is_found(self, mock_tag_cache):
        mock_tag_cache.get_name_for_id.return_value = DISPLAY_TEXT

        sut = AtlanTag(**{"typeName": "123"})

        assert str(sut.type_name) == DISPLAY_TEXT

    def test_atlan_tag_when_tag_name_is_not_found_then_sentinel_is_returned(
        self, mock_tag_cache
    ):
        mock_tag_cache.get_name_for_id.return_value = None

        sut = AtlanTag(**{"typeName": "123"})

        assert sut.type_name == AtlanTagName.get_deleted_sentinel()


class TestAtlanObjectExtraFields:
    @no_type_check
    def test_atlan_api_response(self):
        class TestResponse(AtlanObject):
            """
            Test class inheriting from `AtlanAPIResponse`
            """

            name: str

        test_data = {"name": "test"}
        response = TestResponse(**test_data)

        # Model serialization never includes
        # new fields due to `Extra.ignore`
        assert response.dict() == test_data
        assert response.__atlan_extra__ == {}

        test_data_extra = {"name": "test", "new1": 123, "new2": 456}
        response = TestResponse(**test_data_extra)

        # Model serialization never includes
        # new fields due to `Extra.ignore`
        assert response.dict() == test_data
        assert response.__atlan_extra__ == {"new1": 123, "new2": 456}

        test_data_extra_nested = {
            "name": "test",
            "new1": {"new2": [1, 2, 3]},
            "new3": "abc",
        }
        response = TestResponse(**test_data_extra_nested)

        # Model serialization never includes
        # new fields due to `Extra.ignore`
        assert response.dict() == test_data
        assert response.__atlan_extra__ == {"new1": {"new2": [1, 2, 3]}, "new3": "abc"}

        class TestResponseWithAtlanField(AtlanObject):
            """
            To test when API response contains
            property similar name as `__atlan_extra__`
            """

            name: str
            atlan_field: str = Field(alias="__atlan_extra__")

        test_data_contains_atlan_field = {
            "name": "test",
            "__atlan_extra__": "test_value",
        }
        response = TestResponseWithAtlanField(**test_data_contains_atlan_field)

        # Make sure in this case it shouldn't be populated
        assert response.__atlan_extra__ == {}
        assert response.name == test_data_contains_atlan_field["name"]
        assert response.atlan_field == test_data_contains_atlan_field["__atlan_extra__"]

        class TestResponseWithAttributes(AtlanObject):
            """
            To test when API response contains
            property similar name as `__atlan_extra__`
            """

            old: str
            attributes: TestResponseWithAttributes.Attributes = Field(
                default_factory=lambda: TestResponseWithAttributes.Attributes()
            )

            class Attributes(AtlanObject):
                old_attr: str

        test_attr_raw_data = {
            "old": "oldValue",
            "new": "newValue",
            "attributes": {"oldAttr": "oldValueAttr", "newAttr": "newValueAttr"},
        }
        response = TestResponseWithAttributes(**test_attr_raw_data)

        # Model serialization never includes
        # new fields due to `Extra.ignore`
        assert response.dict() == {
            "old": "oldValue",
            "attributes": {"old_attr": "oldValueAttr"},
        }
        assert response.old == "oldValue"
        assert response.attributes.old_attr == "oldValueAttr"
        assert response.__atlan_extra__ == {"new": "newValue"}
        assert response.attributes.__atlan_extra__ == {"newAttr": "newValueAttr"}

        test_attr_instance_data = {
            "old": "oldValue",
            "new": "newValue",
            "attributes": TestResponseWithAttributes.Attributes(
                **{"oldAttr": "oldValueAttr", "newAttr": "newValueAttr"}
            ),
        }
        response = TestResponseWithAttributes(**test_attr_instance_data)

        # Model serialization never includes
        # new fields due to `Extra.ignore`
        assert response.dict() == {
            "old": "oldValue",
            "attributes": {"old_attr": "oldValueAttr"},
        }
        assert response.old == "oldValue"
        assert response.attributes.old_attr == "oldValueAttr"
        assert response.__atlan_extra__ == {"new": "newValue"}
        assert response.attributes.__atlan_extra__ == {"newAttr": "newValueAttr"}
