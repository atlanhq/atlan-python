# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import pytest
from pydantic.v1 import parse_obj_as

import pyatlan.cache.aio.atlan_tag_cache
from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.aio.core import AsyncAtlanRequest, AsyncAtlanResponse
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
    return AsyncAtlanClient()


@pytest.fixture()
def good_atlan_tag(monkeypatch):
    return AtlanTagName(GOOD_ATLAN_TAG_NAME)


def test_init_with_good_name():
    """Test that AtlanTagName initialization works the same in async context"""
    sut = AtlanTagName(GOOD_ATLAN_TAG_NAME)
    assert sut._display_text == GOOD_ATLAN_TAG_NAME
    assert str(sut) == GOOD_ATLAN_TAG_NAME
    assert sut.__repr__() == f"AtlanTagName('{GOOD_ATLAN_TAG_NAME}')"
    assert sut.__hash__() == GOOD_ATLAN_TAG_NAME.__hash__()
    assert AtlanTagName(GOOD_ATLAN_TAG_NAME) == sut


def test_convert_to_display_text_when_atlan_tag_passed_returns_same_atlan_tag(
    good_atlan_tag,
):
    """Test that conversion works the same in async context"""
    assert good_atlan_tag is AtlanTagName._convert_to_tag_name(good_atlan_tag)


def test_convert_to_display_text_when_bad_string():
    """Test that bad string conversion works the same in async context"""
    assert AtlanTagName._convert_to_tag_name("bad").__repr__() == "AtlanTagName('bad')"


def test_convert_to_tag_name():
    """Test that tag name conversion works the same in async context"""
    sut = AtlanTagName._convert_to_tag_name(ATLAN_TAG_ID)
    assert str(sut) == ATLAN_TAG_ID


def test_get_deleted_sentinel():
    """Test that deleted sentinel works the same in async context"""
    sentinel = AtlanTagName.get_deleted_sentinel()

    assert "(DELETED)" == str(sentinel)
    assert id(sentinel) == id(AtlanTagName.get_deleted_sentinel())


def _assert_asset_tags(asset, is_retranslated=False):
    """Helper function to validate asset tags - same as sync version"""
    assert asset and isinstance(asset, Purpose)
    # Verify that deleted tags are correctly set to `None`
    assert asset.atlan_tags and len(asset.atlan_tags) == 5
    assert asset.atlan_tags[0].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.atlan_tags[1].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.atlan_tags[2].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    if not is_retranslated:
        assert (
            asset.atlan_tags[2].source_tag_attachments
            and len(asset.atlan_tags[2].source_tag_attachments) == 1
        )
    assert asset.atlan_tags[3].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    if not is_retranslated:
        assert asset.atlan_tags[3].source_tag_attachments == []
    assert asset.atlan_tags[4].type_name.__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.purpose_atlan_tags and len(asset.purpose_atlan_tags) == 2
    assert asset.purpose_atlan_tags[0].__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.purpose_atlan_tags[1].__repr__() == f"AtlanTagName('{DELETED_}')"


@pytest.mark.asyncio
async def test_asset_tag_name_field_serde_with_translation_async(
    client: AsyncAtlanClient, monkeypatch
):
    """Test async version of asset tag name field serialization/deserialization with translation"""

    # Mock async methods
    async def get_name_for_id(_, __):
        return None

    async def get_id_for_name(_, __):
        return None

    async def get_source_tags_attr_id(_, tag_id):
        # Return different values based on tag_id to test different scenarios
        source_tag_ids = {
            "source-tag-with-attributes": "ZLVyaOlGWDrkLFZgmZCjLa",  # source tag with attributes
            "source-tag-without-attributes": "BLVyaOlGWDrkLFZgmZCjLa",
            "deleted-source-tag": None,  # deleted source tag with attributes
        }
        return source_tag_ids.get(tag_id, None)  # Return None for non-source tags

    # Patch async cache methods
    monkeypatch.setattr(
        pyatlan.cache.aio.atlan_tag_cache.AsyncAtlanTagCache,
        "get_id_for_name",
        get_id_for_name,
    )

    monkeypatch.setattr(
        pyatlan.cache.aio.atlan_tag_cache.AsyncAtlanTagCache,
        "get_name_for_id",
        get_name_for_id,
    )

    monkeypatch.setattr(
        pyatlan.cache.aio.atlan_tag_cache.AsyncAtlanTagCache,
        "get_source_tags_attr_id",
        get_source_tags_attr_id,
    )

    # Same raw JSON structure as sync test
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
            # Source tags with attributes
            {
                "typeName": "source-tag-with-attributes",
                "attributes": {
                    "ZLVyaOlGWDrkLFZgmZCjLa": [
                        {
                            "typeName": "SourceTagAttachment",
                            "attributes": {
                                "sourceTagName": "CONFIDENTIAL",
                                "sourceTagQualifiedName": "default/snowflake/1747816988/ANALYTICS/WIDE_WORLD_IMPORTERS/CONFIDENTIAL",
                                "sourceTagGuid": "2a9dab90-1b86-432d-a28a-9f3d9b61192b",
                                "sourceTagConnectorName": "snowflake",
                                "sourceTagValue": [
                                    {"tagAttachmentValue": "Not Restricted"}
                                ],
                            },
                        }
                    ]
                },
                "entityGuid": "46be9b92-170b-4c74-bf28-f9dc99021a2a",
                "entityStatus": "ACTIVE",
                "propagate": True,
                "removePropagationsOnEntityDelete": True,
                "restrictPropagationThroughLineage": False,
                "restrictPropagationThroughHierarchy": False,
            },
            # Source tags (without attributes)
            {
                "typeName": "source-tag-without-attributes",
                "entityGuid": "46be9b92-170b-4c74-bf28-f9dc99021a2a",
                "entityStatus": "ACTIVE",
                "propagate": True,
                "removePropagationsOnEntityDelete": True,
                "restrictPropagationThroughLineage": False,
                "restrictPropagationThroughHierarchy": False,
            },
            # Deleted source tags (with attributes)
            {
                "typeName": "deleted-source-tag",
                "attributes": {
                    "XzEYmFzETBrS7nuxeImNie": [
                        {
                            "typeName": "SourceTagAttachment",
                            "attributes": {
                                "sourceTagName": "CONFIDENTIAL",
                                "sourceTagQualifiedName": "default/snowflake/1747816988/ANALYTICS/WIDE_WORLD_IMPORTERS/CONFIDENTIAL",
                                "sourceTagGuid": "2a9dab90-1b86-432d-a28a-9f3d9b61192b",
                                "sourceTagConnectorName": "snowflake",
                                "sourceTagValue": [
                                    {"tagAttachmentValue": "Not Restricted"}
                                ],
                            },
                        }
                    ]
                },
                "entityGuid": "46be9b92-170b-4c74-bf28-f9dc99021a2a",
                "entityStatus": "DELETED",
                "propagate": True,
                "removePropagationsOnEntityDelete": True,
                "restrictPropagationThroughLineage": False,
                "restrictPropagationThroughHierarchy": False,
            },
        ],
    }

    # Build objects from 1. translated JSON and 2. raw JSON (async version)
    async_response = AsyncAtlanResponse(raw_json=raw_json, client=client)
    translated_dict = await async_response.translate()
    purpose_with_translation = parse_obj_as(Purpose, translated_dict)
    purpose_without_translation = parse_obj_as(Purpose, raw_json)

    # Construct objects dict from 1. translated JSON and 2. raw JSON (async version)
    async_request_with_translation = AsyncAtlanRequest(
        instance=purpose_with_translation, client=client
    )
    retranslated_with_translated_dict = (
        await async_request_with_translation.retranslate()
    )

    async_request_without_translation = AsyncAtlanRequest(
        instance=purpose_without_translation, client=client
    )
    retranslated_without_translated_dict = (
        await async_request_without_translation.retranslate()
    )

    # Re-build objects from 1. retranslated JSON and 2. retranslated raw JSON
    purpose_with_translation_and_retranslation = parse_obj_as(
        Purpose, retranslated_with_translated_dict
    )
    purpose_without_translation_and_retranslation = parse_obj_as(
        Purpose, retranslated_without_translated_dict
    )

    # Validate results using the same assertion helper
    _assert_asset_tags(purpose_with_translation)
    _assert_asset_tags(purpose_with_translation_and_retranslation, is_retranslated=True)
    _assert_asset_tags(
        purpose_without_translation_and_retranslation, is_retranslated=True
    )
