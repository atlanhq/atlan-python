# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest
from pydantic.v1 import parse_obj_as

import pyatlan.cache.atlan_tag_cache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Purpose
from pyatlan.model.constants import DELETED_
from pyatlan.model.core import AtlanTagName

ATLAN_TAG_ID = "yiB7RLvdC2yeryLPjaDeHM"

GOOD_ATLAN_TAG_NAME = "PII"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture()
def current_client(client, monkeypatch):
    monkeypatch.setattr(
        AtlanClient,
        "get_current_client",
        lambda: client,
    )


def test_init_with_bad_atlan_tag_name_raises_value_error(
    current_client: AtlanClient, monkeypatch
):
    def get_id_for_name(_, __):
        return None

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_id_for_name",
        get_id_for_name,
    )
    with pytest.raises(
        ValueError, match=f"{GOOD_ATLAN_TAG_NAME} is not a valid Classification"
    ):
        AtlanTagName(GOOD_ATLAN_TAG_NAME)


@pytest.fixture()
def good_atlan_tag(current_client: AtlanClient, monkeypatch):
    def get_id_for_name(_, value):
        return ATLAN_TAG_ID

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_id_for_name",
        get_id_for_name,
    )
    return AtlanTagName(GOOD_ATLAN_TAG_NAME)


def test_init_with_good_name(current_client: AtlanClient, monkeypatch):
    def get_id_for_name(_, value):
        assert value == GOOD_ATLAN_TAG_NAME
        return GOOD_ATLAN_TAG_NAME

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_id_for_name",
        get_id_for_name,
    )
    sut = AtlanTagName(GOOD_ATLAN_TAG_NAME)
    assert sut._display_text == GOOD_ATLAN_TAG_NAME
    assert str(sut) == GOOD_ATLAN_TAG_NAME
    assert sut.__repr__() == f"AtlanTagName('{GOOD_ATLAN_TAG_NAME}')"
    assert sut.__hash__() == GOOD_ATLAN_TAG_NAME.__hash__()
    assert AtlanTagName(GOOD_ATLAN_TAG_NAME) == sut


def test_convert_to_display_text_when_atlan_tag_passed_returns_same_atlan_tag(
    good_atlan_tag,
):
    assert good_atlan_tag is AtlanTagName._convert_to_display_text(good_atlan_tag)


def test_convert_to_display_text_when_bad_string(
    current_client: AtlanClient, monkeypatch
):
    def get_name_for_id(_, __):
        return None

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_name_for_id",
        get_name_for_id,
    )

    assert (
        AtlanTagName._convert_to_display_text("bad").__repr__()
        == f"AtlanTagName('{DELETED_}')"
    )


def test_convert_to_display_text_when_id(current_client: AtlanClient, monkeypatch):
    def get_name_for_id(_, __):
        return GOOD_ATLAN_TAG_NAME

    def get_id_for_name(_, value):
        assert value == GOOD_ATLAN_TAG_NAME
        return GOOD_ATLAN_TAG_NAME

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_id_for_name",
        get_id_for_name,
    )
    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_name_for_id",
        get_name_for_id,
    )

    sut = AtlanTagName._convert_to_display_text(ATLAN_TAG_ID)

    assert str(sut) == GOOD_ATLAN_TAG_NAME


def test_json_encode_atlan_tag(good_atlan_tag):
    assert AtlanTagName.json_encode_atlan_tag(good_atlan_tag) == ATLAN_TAG_ID


def test_asset_tag_name_field_deserialization(current_client: AtlanClient, monkeypatch):
    def get_name_for_id(_, __):
        return None

    def get_id_for_name(_, __):
        return None

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_id_for_name",
        get_id_for_name,
    )

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_name_for_id",
        get_name_for_id,
    )
    # Simulate a `Purpose` asset with `purpose_atlan_tags` of type `AtlanTagName`
    purpose_asset = {
        "typeName": "Purpose",
        "attributes": {
            # AtlanTagName
            "purposeClassifications": [
                "some-deleted-purpose-tag-1",
                "some-deleted-purpose-tag-2",
            ],
        },
        "guid": "9f7a35f4-8d37-4273-81ec-c497a83a2472",
        "status": "ACTIVE",
        "classifications": [
            # AtlanTag
            {
                "typeName": "some-deleted-purpose-tag-1",
                "entityGuid": "82683fb9-1501-4627-a5d0-0da9be64c0d5",
                "entityStatus": "DELETED",
                "propagate": False,
                "removePropagationsOnEntityDelete": True,
                "restrictPropagationThroughLineage": True,
                "restrictPropagationThroughHierarchy": False,
            },
            {
                "typeName": "some-deleted-purpose-tag-2",
                "entityGuid": "82683fb9-1501-4627-a5d0-0da9be64c0d5",
                "entityStatus": "DELETED",
                "propagate": False,
                "removePropagationsOnEntityDelete": True,
                "restrictPropagationThroughLineage": True,
                "restrictPropagationThroughHierarchy": False,
            },
        ],
    }
    purpose = parse_obj_as(Purpose, purpose_asset)
    assert purpose and isinstance(purpose, Purpose)

    # Verify that deleted tags are correctly set to `None`
    # assert purpose.atlan_tags == [AtlanTagName('(DELETED)')]
    assert purpose.atlan_tags and len(purpose.atlan_tags) == 2
    assert purpose.atlan_tags[0].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert purpose.atlan_tags[1].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert purpose.purpose_atlan_tags and len(purpose.purpose_atlan_tags) == 2
    assert purpose.purpose_atlan_tags[0].__repr__() == f"AtlanTagName('{DELETED_}')"
    assert purpose.purpose_atlan_tags[1].__repr__() == f"AtlanTagName('{DELETED_}')"
