from unittest.mock import call

import pytest

from pyatlan.model.core import AtlanTag, AtlanTagName

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
