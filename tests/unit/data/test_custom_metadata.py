from unittest.mock import patch

import pytest

from pyatlan.error import NotFoundError
from pyatlan.model.custom_metadata import CustomMetadataDict

CM_ID = "123"
CM_NAME = "Something"
CM_ATTRIBUTES = {"1": "First Name", "2": "Last Name"}
META_DATA = {CM_ID: CM_ATTRIBUTES}


class Test_CustomMetadataDict:
    @pytest.fixture()
    @patch("pyatlan.model.custom_metadata.CustomMetadataCache")
    def custom_metadata_dict(self, mock_cache):
        mock_cache.get_id_for_name.return_value = CM_ID
        mock_cache.map_attr_id_to_name = META_DATA

        return CustomMetadataDict(CM_NAME)

    @patch("pyatlan.model.custom_metadata.CustomMetadataCache")
    def test_init_when_invalid_name_throws_not_found_error(self, mock_cache):
        mock_cache.get_id_for_name.side_effect = NotFoundError(message="", code="123")
        with pytest.raises(NotFoundError):
            CustomMetadataDict(CM_NAME)
        mock_cache.get_id_for_name.assert_called_with(CM_NAME)

    def test_init_when_called_with_valid_name_initializes_names(
        self, custom_metadata_dict
    ):
        assert custom_metadata_dict.attribute_names == set(CM_ATTRIBUTES.values())

    def test_can_get_set_items(self, custom_metadata_dict):
        custom_metadata_dict["First Name"] = "Bob"
        assert custom_metadata_dict["First Name"] == "Bob"

    def test_get_item_with_invalid_name_raises_key_error(self, custom_metadata_dict):
        with pytest.raises(
            KeyError, match="'garb' is not a valid property name for Something"
        ):
            custom_metadata_dict["garb"]

    def test_set_item_with_invalid_name_raises_key_error(self, custom_metadata_dict):
        with pytest.raises(
            KeyError, match="'garb' is not a valid property name for Something"
        ):
            custom_metadata_dict["garb"] = "1"

    def test_clear_set_all_attributes_to_none(self, custom_metadata_dict):
        custom_metadata_dict["First Name"] = "Bob"
        custom_metadata_dict.clear()
        for name in custom_metadata_dict.attribute_names:
            assert custom_metadata_dict[name] is None

    def test_get_item_using_name_that_has_not_been_set_raises_key_err(
        self, custom_metadata_dict
    ):
        with pytest.raises(
            KeyError,
            match="'First Name' must be set before trying to retrieve the value",
        ):
            custom_metadata_dict["First Name"]
