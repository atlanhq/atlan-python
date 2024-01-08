from unittest.mock import patch

import pytest

from pyatlan.errors import ErrorCode, NotFoundError
from pyatlan.model.custom_metadata import (
    CustomMetadataDict,
    CustomMetadataProxy,
    CustomMetadataRequest,
)

ATTR_LAST_NAME = "Last Name"

ATTR_LAST_NAME_ID = "2"

ATTR_FIRST_NAME = "First Name"

ATTR_FIRST_NAME_ID = "1"

CM_ID = "123"
CM_NAME = "Something"
CM_ATTRIBUTES = {ATTR_FIRST_NAME_ID: ATTR_FIRST_NAME, ATTR_LAST_NAME_ID: ATTR_LAST_NAME}
META_DATA = {CM_ID: CM_ATTRIBUTES}


@pytest.fixture()
def mock_cache():
    with patch("pyatlan.model.custom_metadata.CustomMetadataCache") as cache:
        yield cache


def get_attr_id_for_name(*args, **kwargs):
    return ATTR_FIRST_NAME_ID if args[1] == ATTR_FIRST_NAME else ATTR_LAST_NAME_ID


def get_attr_name_for_id(*args, **kwargs):
    return ATTR_FIRST_NAME if args[1] == ATTR_FIRST_NAME_ID else ATTR_FIRST_NAME


class TestCustomMetadataDict:
    @pytest.fixture()
    def sut(self, mock_cache):
        mock_cache.get_id_for_name.return_value = CM_ID
        mock_cache.get_cache.return_value.map_attr_id_to_name = META_DATA
        mock_cache.map_attr_id_to_name = META_DATA
        mock_cache.is_attr_archived.return_value = False

        return CustomMetadataDict(CM_NAME)

    def test_init_when_invalid_name_throws_not_found_error(self, mock_cache):
        mock_cache.get_id_for_name.side_effect = (
            ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters("123")
        )
        with pytest.raises(NotFoundError):
            CustomMetadataDict(CM_NAME)
        mock_cache.get_id_for_name.assert_called_with(CM_NAME)

    def test_modified_after_init_returns_false(self, sut):
        assert sut.modified is False

    def test_init_when_called_with_valid_name_initializes_names(self, sut):
        assert sut.attribute_names == set(CM_ATTRIBUTES.values())

    def test_can_get_set_items(self, sut):
        sut[ATTR_FIRST_NAME] = "123"
        assert sut[ATTR_FIRST_NAME] == "123"
        assert sut.modified is True

    def test_get_item_with_invalid_name_raises_key_error(self, sut):
        with pytest.raises(
            KeyError, match="'garb' is not a valid property name for Something"
        ):
            sut["garb"]

    def test_set_item_with_invalid_name_raises_key_error(self, sut):
        with pytest.raises(
            KeyError, match="'garb' is not a valid property name for Something"
        ):
            sut["garb"] = ATTR_FIRST_NAME_ID

    @pytest.mark.parametrize("name", [ATTR_FIRST_NAME, ATTR_FIRST_NAME])
    def test_clear_all_set_all_attributes_to_none(self, sut, name):
        sut.clear_all()
        assert sut[name] is None
        assert sut.modified is True

    @pytest.mark.parametrize(
        "property_to_set, other_property",
        [(ATTR_FIRST_NAME, ATTR_LAST_NAME), (ATTR_LAST_NAME, ATTR_FIRST_NAME)],
    )
    def test_clear_unset_sets_unset_to_none(self, sut, property_to_set, other_property):
        sut[property_to_set] = "bob"
        sut.clear_unset()
        assert sut[property_to_set] == "bob"
        assert sut[other_property] is None

    def test_get_item_using_name_that_has_not_been_set_returns_none(self, sut):
        assert sut[ATTR_FIRST_NAME] is None

    def test_business_attributes_when_no_changes(self, sut):
        assert sut.business_attributes == {}

    def test_business_attributes_with_data(self, sut, mock_cache):
        mock_cache.get_attr_id_for_name.side_effect = get_attr_id_for_name
        alice = "alice"
        sut[ATTR_FIRST_NAME] = alice
        assert sut.business_attributes == {ATTR_FIRST_NAME_ID: alice}

    @pytest.mark.parametrize("name", [ATTR_FIRST_NAME, ATTR_FIRST_NAME])
    def test_is_unset_initially_returns_false(self, sut, name):
        assert sut.is_set(name) is False

    @pytest.mark.parametrize("name", [ATTR_FIRST_NAME, ATTR_FIRST_NAME])
    def test_unset_after_update_returns_true(self, sut, name):
        sut[name] = "bob"
        assert sut.is_set(name) is True

    def test_get_deleted_sentinel(self):
        sentinel = CustomMetadataDict.get_deleted_sentinel()

        assert sentinel is not None
        assert id(sentinel) == id(CustomMetadataDict.get_deleted_sentinel())
        assert 0 == len(sentinel)
        assert sentinel.modified is False
        assert sentinel._name == "(DELETED)"
        with pytest.raises(
            KeyError, match=r"'abc' is not a valid property name for \(DELETED\)"
        ):
            sentinel["abc"] = 1


class TestCustomMetadataProxy:
    @pytest.fixture()
    def sut(self, mock_cache):
        yield CustomMetadataProxy(business_attributes=None)

    def test_when_intialialized_with_no_business_attributes_then_modified_is_false(
        self, sut
    ):
        assert sut.modified is False
        assert sut.business_attributes is None

    def test_when_intialialized_with_no_business_attributes_then_business_attributes_returns_none(
        self, sut
    ):
        assert sut.business_attributes is None

    def test_set_custom_metadata(self, sut):
        cm = CustomMetadataDict(name=CM_NAME)
        sut.set_custom_metadata(cm)
        assert sut.modified is True
        assert sut.get_custom_metadata(name=CM_NAME) is cm

    def test_after_modifying_metadata_modified_is_true(self, sut, mock_cache):
        mock_cache.get_id_for_name.return_value = CM_ID
        mock_cache.get_cache.return_value.map_attr_id_to_name = META_DATA
        mock_cache.is_attr_archived.return_value = False

        cm = sut.get_custom_metadata(name=CM_NAME)
        cm[ATTR_FIRST_NAME] = "James"

        assert sut.modified is True

    def test_when_not_modified_returns_business_attributes(self, mock_cache):
        mock_cache.get_name_for_id.return_value = CM_NAME
        mock_cache.get_attr_name_for_id.return_value = ATTR_FIRST_NAME
        mock_cache.get_id_for_name.return_value = CM_ID
        mock_cache.get_cache.return_value.map_attr_id_to_name = META_DATA
        mock_cache.is_attr_archived.return_value = False
        ba = {CM_ID: {ATTR_FIRST_NAME_ID: ATTR_FIRST_NAME}}

        sut = CustomMetadataProxy(business_attributes=ba)

        assert sut.business_attributes is ba

    def test_when_modified_returns_updated_business_attributes(self, mock_cache):
        mock_cache.get_name_for_id.return_value = CM_NAME
        mock_cache.get_attr_name_for_id.side_effect = get_attr_name_for_id
        mock_cache.get_id_for_name.return_value = CM_ID
        mock_cache.get_cache.return_value.map_attr_id_to_name = META_DATA
        mock_cache.is_attr_archived.return_value = False
        mock_cache.get_attr_id_for_name.side_effect = get_attr_id_for_name
        ba = {CM_ID: {ATTR_FIRST_NAME_ID: "Dave"}}

        sut = CustomMetadataProxy(business_attributes=ba)
        cm = sut.get_custom_metadata(name=CM_NAME)
        joey = "Joey"
        donna = "Donna"
        cm[ATTR_FIRST_NAME] = donna
        cm[ATTR_LAST_NAME] = joey
        ba = sut.business_attributes

        assert ba == {CM_ID: {ATTR_FIRST_NAME_ID: donna, ATTR_LAST_NAME_ID: joey}}

    def test_when_invalid_metadata_set_then_delete_sentinel_is_used(self, mock_cache):
        mock_cache.get_name_for_id.side_effect = (
            ErrorCode.CM_NOT_FOUND_BY_ID.exception_with_parameters(CM_ID)
        )
        ba = {CM_ID: {ATTR_FIRST_NAME_ID: "Dave"}}

        sut = CustomMetadataProxy(business_attributes=ba)

        assert len(sut.get_custom_metadata("(DELETED)")) == 0

    def test_when_property_is_archived(self, mock_cache):
        mock_cache.get_name_for_id.return_value = CM_NAME
        mock_cache.get_attr_name_for_id.return_value = ATTR_FIRST_NAME
        mock_cache.get_id_for_name.return_value = CM_ID
        mock_cache.get_cache.return_value.map_attr_id_to_name = META_DATA
        mock_cache.is_attr_archived.return_value = True
        ba = {CM_ID: {ATTR_FIRST_NAME_ID: ATTR_FIRST_NAME}}
        sut = CustomMetadataProxy(business_attributes=ba)
        assert sut.business_attributes is ba
        assert sut.get_custom_metadata(CM_NAME) == {}


class TestCustomMetadataRequest:
    def test_create(self, mock_cache):
        mock_cache.get_id_for_name.return_value = CM_ID
        mock_cache.map_attr_id_to_name = META_DATA

        cm = CustomMetadataDict(CM_NAME)
        request = CustomMetadataRequest.create(custom_metadata_dict=cm)
        assert request.__root__ == {}
