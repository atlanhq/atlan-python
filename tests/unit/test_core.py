from __future__ import annotations

from typing import no_type_check
from unittest.mock import MagicMock

import pytest
from pydantic.v1 import Field

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.core import AtlanObject, AtlanTag, AtlanTagName

DISPLAY_TEXT = "Something"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture()
def mock_tag_cache(client, monkeypatch):
    mock_cache = MagicMock(client)
    monkeypatch.setattr(AtlanClient, "atlan_tag_cache", mock_cache)
    return mock_cache


class TestAtlanTag:
    def test_atlan_tag_when_tag_name_is_found(self, mock_tag_cache):
        sut = AtlanTag(**{"typeName": "123"})
        assert str(sut.type_name) == "123"

    def test_atlan_tag_when_tag_name_is_empty_then_sentinel_is_returned(
        self, mock_tag_cache
    ):
        sut = AtlanTag(**{"typeName": ""})

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
