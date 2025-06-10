# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest
from pydantic.v1 import parse_obj_as

import pyatlan.cache.atlan_tag_cache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Purpose
from pyatlan.model.constants import DELETED_
from pyatlan.model.core import AtlanRequest, AtlanResponse, AtlanTagName

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
def good_atlan_tag(monkeypatch):
    return AtlanTagName(GOOD_ATLAN_TAG_NAME)


def test_init_with_good_name():
    sut = AtlanTagName(GOOD_ATLAN_TAG_NAME)
    assert sut._display_text == GOOD_ATLAN_TAG_NAME
    assert str(sut) == GOOD_ATLAN_TAG_NAME
    assert sut.__repr__() == f"AtlanTagName('{GOOD_ATLAN_TAG_NAME}')"
    assert sut.__hash__() == GOOD_ATLAN_TAG_NAME.__hash__()
    assert AtlanTagName(GOOD_ATLAN_TAG_NAME) == sut


def test_convert_to_display_text_when_atlan_tag_passed_returns_same_atlan_tag(
    good_atlan_tag,
):
    assert good_atlan_tag is AtlanTagName._convert_to_tag_name(good_atlan_tag)


def test_convert_to_display_text_when_bad_string():
    assert AtlanTagName._convert_to_tag_name("bad").__repr__() == "AtlanTagName('bad')"


def test_convert_to_tag_name():
    sut = AtlanTagName._convert_to_tag_name(ATLAN_TAG_ID)
    assert str(sut) == ATLAN_TAG_ID


def test_get_deleted_sentinel():
    sentinel = AtlanTagName.get_deleted_sentinel()

    assert "(DELETED)" == str(sentinel)
    assert id(sentinel) == id(AtlanTagName.get_deleted_sentinel())


def _assert_asset_tags(asset):
    assert asset and isinstance(asset, Purpose)
    # Verify that deleted tags are correctly set to `None`
    assert asset.atlan_tags and len(asset.atlan_tags) == 3
    assert asset.atlan_tags[0].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.atlan_tags[1].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.atlan_tags[2].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.purpose_atlan_tags and len(asset.purpose_atlan_tags) == 2
    assert asset.purpose_atlan_tags[0].__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.purpose_atlan_tags[1].__repr__() == f"AtlanTagName('{DELETED_}')"


def test_asset_tag_name_field_serde_with_translation(client: AtlanClient, monkeypatch):
    def get_name_for_id(_, __):
        return None

    def get_id_for_name(_, __):
        return None

    def get_source_tags_attr_id(_, __):
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

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_source_tags_attr_id",
        get_source_tags_attr_id,
    )
    # Simulate a `Purpose` asset with `purpose_atlan_tags` of type `AtlanTagName`
    raw_json = {
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
            # Source tags
            {
                "typeName": "some-deleted-source-tag-1",
                "attributes": {
                    "XzEYmFzETBrS7nuxeImNie": [
                        {
                            "sourceTagName": "CONFIDENTIAL",
                            "sourceTagQualifiedName": "default/snowflake/1747816988/ANALYTICS/WIDE_WORLD_IMPORTERS/CONFIDENTIAL",
                            "sourceTagGuid": "2a9dab90-1b86-432d-a28a-9f3d9b61192b",
                            "sourceTagConnectorName": "snowflake",
                            "sourceTagValue": [
                                {"tagAttachmentValue": "Not Restricted"}
                            ],
                        }
                    ]
                },
            },
        ],
    }
    # Build objects from 1. translated JSON and 2. raw JSON
    translated_dict = AtlanResponse(raw_json=raw_json, client=client).to_dict()
    purpose_with_translation = parse_obj_as(Purpose, translated_dict)
    purpose_without_translation = parse_obj_as(Purpose, raw_json)

    # Contruct objects dict from 1. translated JSON and 2. raw JSON
    retranslated_with_translated_dict = AtlanRequest(
        instance=purpose_with_translation, client=client
    ).translated
    retranslated_without_translated_dict = AtlanRequest(
        instance=purpose_without_translation, client=client
    ).translated

    # Re-build objects from 1. retranslated JSON and 2. retranslated raw JSON
    purpose_with_translation_and_retranslation = parse_obj_as(
        Purpose, retranslated_with_translated_dict
    )
    purpose_without_translation_and_retranslation = parse_obj_as(
        Purpose, retranslated_without_translated_dict
    )

    _assert_asset_tags(purpose_with_translation)
    _assert_asset_tags(purpose_with_translation_and_retranslation)
    _assert_asset_tags(purpose_without_translation_and_retranslation)
