# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for AtlanTagName plus AtlanResponse/AtlanRequest tag translation."""

from __future__ import annotations

import msgspec
import pytest

from pyatlan.model.constants import DELETED_
from pyatlan_v9.model import Purpose
from pyatlan_v9.model.core import AtlanRequest, AtlanResponse, AtlanTagName

ATLAN_TAG_ID = "yiB7RLvdC2yeryLPjaDeHM"
GOOD_ATLAN_TAG_NAME = "PII"


class _MockTagCache:
    def get_name_for_id(self, _tag_id: str):
        return None

    def get_id_for_name(self, _tag_name: str):
        return None

    def get_source_tags_attr_id(self, tag_id: str):
        source_tag_ids = {
            "source-tag-with-attributes": "ZLVyaOlGWDrkLFZgmZCjLa",
            "source-tag-without-attributes": "BLVyaOlGWDrkLFZgmZCjLa",
            "deleted-source-tag": None,
        }
        return source_tag_ids.get(tag_id, None)


class _MockClient:
    atlan_tag_cache = _MockTagCache()


@pytest.fixture()
def client():
    """Provide a mock client with Atlan tag-cache methods used in translation."""
    return _MockClient()


@pytest.fixture()
def good_atlan_tag():
    """Provide a valid AtlanTagName object for conversion tests."""
    return AtlanTagName(GOOD_ATLAN_TAG_NAME)


def test_init_with_good_name():
    """Verify AtlanTagName stores and exposes the input display text."""
    sut = AtlanTagName(GOOD_ATLAN_TAG_NAME)
    assert sut._display_text == GOOD_ATLAN_TAG_NAME
    assert str(sut) == GOOD_ATLAN_TAG_NAME
    assert sut.__repr__() == f"AtlanTagName('{GOOD_ATLAN_TAG_NAME}')"
    assert sut.__hash__() == GOOD_ATLAN_TAG_NAME.__hash__()
    assert AtlanTagName(GOOD_ATLAN_TAG_NAME) == sut


def test_convert_to_display_text_when_atlan_tag_passed_returns_same_atlan_tag(
    good_atlan_tag,
):
    """Verify conversion keeps existing AtlanTagName objects untouched."""
    assert good_atlan_tag is AtlanTagName._convert_to_tag_name(good_atlan_tag)


def test_convert_to_display_text_when_bad_string():
    """Verify conversion of a plain string creates an AtlanTagName value."""
    assert AtlanTagName._convert_to_tag_name("bad").__repr__() == "AtlanTagName('bad')"


def test_convert_to_tag_name():
    """Verify conversion of a string ID to AtlanTagName preserves its text."""
    sut = AtlanTagName._convert_to_tag_name(ATLAN_TAG_ID)
    assert str(sut) == ATLAN_TAG_ID


def test_get_deleted_sentinel():
    """Verify deleted sentinel is stable and maps to '(DELETED)' text."""
    sentinel = AtlanTagName.get_deleted_sentinel()
    assert "(DELETED)" == str(sentinel)
    assert id(sentinel) == id(AtlanTagName.get_deleted_sentinel())


def _assert_asset_tags(asset: Purpose, is_retranslated: bool = False):
    assert asset and isinstance(asset, Purpose)
    assert asset.classifications and len(asset.classifications) == 5
    assert str(asset.classifications[0].type_name) == DELETED_
    assert str(asset.classifications[1].type_name) == DELETED_
    assert str(asset.classifications[2].type_name) == DELETED_
    if not is_retranslated:
        assert asset.classifications[2].source_tag_attachments
        assert len(asset.classifications[2].source_tag_attachments) == 1
    assert str(asset.classifications[3].type_name) == DELETED_
    if not is_retranslated:
        assert asset.classifications[3].source_tag_attachments == []
    assert str(asset.classifications[4].type_name) == DELETED_
    assert asset.purpose_atlan_tags and len(asset.purpose_atlan_tags) == 2
    assert asset.purpose_atlan_tags[0].__repr__() == f"AtlanTagName('{DELETED_}')"
    assert asset.purpose_atlan_tags[1].__repr__() == f"AtlanTagName('{DELETED_}')"


def test_asset_tag_name_field_serde_with_translation(client):
    """Verify translation and retranslation behavior for deleted and source tags."""
    raw_json = {
        "typeName": "Purpose",
        "attributes": {
            "purposeClassifications": [
                "some-deleted-purpose-tag-1",
                "some-deleted-purpose-tag-2",
            ],
        },
        "guid": "9f7a35f4-8d37-4273-81ec-c497a83a2472",
        "status": "ACTIVE",
        "classifications": [
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
            {
                "typeName": "source-tag-without-attributes",
                "entityGuid": "46be9b92-170b-4c74-bf28-f9dc99021a2a",
                "entityStatus": "ACTIVE",
                "propagate": True,
                "removePropagationsOnEntityDelete": True,
                "restrictPropagationThroughLineage": False,
                "restrictPropagationThroughHierarchy": False,
            },
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

    translated_dict = AtlanResponse(raw_json=raw_json, client=client).to_dict()
    purpose_with_translation = Purpose.from_json(msgspec.json.encode(translated_dict))
    purpose_without_translation = Purpose.from_json(msgspec.json.encode(raw_json))

    retranslated_with_translated_dict = AtlanRequest(
        instance=purpose_with_translation, client=client
    ).translated
    retranslated_without_translated_dict = AtlanRequest(
        instance=purpose_without_translation, client=client
    ).translated

    purpose_with_translation_and_retranslation = Purpose.from_json(
        msgspec.json.encode(retranslated_with_translated_dict)
    )
    purpose_without_translation_and_retranslation = Purpose.from_json(
        msgspec.json.encode(retranslated_without_translated_dict)
    )

    _assert_asset_tags(purpose_with_translation)
    _assert_asset_tags(purpose_with_translation_and_retranslation, is_retranslated=True)
    _assert_asset_tags(
        purpose_without_translation_and_retranslation, is_retranslated=True
    )
