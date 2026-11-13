# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""
BLDX-1678: a response that holds ``classifications`` as plain strings (for
example inside a workflow's DAG filter, as returned by ``client.app.get_all()``)
must not crash the tag translators.

Every response the SDK reads is walked by ``_deep_translate``, and any dict with
a ``classifications`` key is handed to the tag translator. The translator
expected each entry to be a classification object (a dict with ``typeName``),
so a ``list[str]`` raised ``AttributeError: 'str' object has no attribute 'get'``.

There are four copies of the translator: sync and async, in ``pyatlan`` and in
``pyatlan_v9``. All four sit on a live response path, so all four are covered.

No tenant calls: the tag cache is a small in-memory fake.
"""

from types import SimpleNamespace

import pytest

from pyatlan.model.aio.translators import AsyncAtlanTagTranslator
from pyatlan.model.constants import DELETED_
from pyatlan.model.core import AtlanResponse
from pyatlan.model.translators import AtlanTagTranslator
from pyatlan_v9.model.aio.translators import (
    AsyncAtlanTagTranslator as V9AsyncAtlanTagTranslator,
)
from pyatlan_v9.model.translators import AtlanTagTranslator as V9AtlanTagTranslator

TAG_ID = "yiB7RLvdC2yeryLPjaDeHM"
TAG_NAME = "PII"
UNKNOWN_TAG_ID = "zzUnknownTagIdzz"
# The key that keeps the original hashed ID differs by copy: "tag_id" in pyatlan,
# "tagId" in pyatlan_v9. Tests read it from the class (translator_cls._TAG_ID).


class _FakeTagCache:
    """Knows exactly one tag: TAG_ID <-> TAG_NAME."""

    def get_name_for_id(self, tag_id):
        return {TAG_ID: TAG_NAME}.get(tag_id)

    def get_source_tags_attr_id(self, tag_id):
        return None


class _AsyncFakeTagCache:
    async def get_name_for_id(self, tag_id):
        return {TAG_ID: TAG_NAME}.get(tag_id)

    async def get_source_tags_attr_id(self, tag_id):
        return None


def _sync_client():
    return SimpleNamespace(atlan_tag_cache=_FakeTagCache())


def _async_client():
    return SimpleNamespace(atlan_tag_cache=_AsyncFakeTagCache())


# (translator class, is_async), one entry per copy of the translator
TRANSLATORS = [
    pytest.param(AtlanTagTranslator, False, id="pyatlan-sync"),
    pytest.param(AsyncAtlanTagTranslator, True, id="pyatlan-async"),
    pytest.param(V9AtlanTagTranslator, False, id="pyatlan_v9-sync"),
    pytest.param(V9AsyncAtlanTagTranslator, True, id="pyatlan_v9-async"),
]


async def _translate(translator_cls, is_async, data):
    if is_async:
        return await translator_cls(_async_client()).translate(data)
    return translator_cls(_sync_client()).translate(data)


# ---------------------------------------------------------------------------
# The issue: string entries must not crash, and must come back unchanged.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("translator_cls, is_async", TRANSLATORS)
async def test_string_classifications_are_left_unchanged(translator_cls, is_async):
    # "PII" is a tag NAME here, not a hashed tag ID. A string entry is not a
    # classification object, so the translator must leave it exactly as it is.
    data = {"classifications": ["PII", "Confidential"]}

    result = await _translate(translator_cls, is_async, data)

    assert result["classifications"] == ["PII", "Confidential"]


@pytest.mark.parametrize("translator_cls, is_async", TRANSLATORS)
async def test_mixed_list_keeps_strings_and_still_translates_objects(
    translator_cls, is_async
):
    # The string comes FIRST: a guard must skip just that entry and keep going,
    # so the classification object after it is still translated.
    data = {"classifications": ["PII", {"typeName": TAG_ID}]}

    result = await _translate(translator_cls, is_async, data)

    assert result["classifications"][0] == "PII"
    assert str(result["classifications"][1]["typeName"]) == TAG_NAME
    assert result["classifications"][1][translator_cls._TAG_ID] == TAG_ID


def test_app_list_payload_with_string_classifications_translates():
    # Shape of a workflow list page: the strings sit deep inside a DAG filter.
    raw_json = {
        "items": [
            {
                "name": "example-workflow-a1b2",
                "dag": {
                    "extract": {
                        "inputs": {
                            "args": {
                                "rules": [
                                    {
                                        "filterSchema": {
                                            "rules": [
                                                {
                                                    "value": {
                                                        "classifications": [
                                                            "PII",
                                                            "Confidential",
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    }
                },
            }
        ],
        "has_more": False,
    }

    translated = AtlanResponse(raw_json=raw_json, client=_sync_client()).to_dict()

    value = translated["items"][0]["dag"]["extract"]["inputs"]["args"]["rules"][0][
        "filterSchema"
    ]["rules"][0]["value"]
    assert value["classifications"] == ["PII", "Confidential"]


# ---------------------------------------------------------------------------
# Guards: behaviour that already works and must stay green after the fix.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("translator_cls, is_async", TRANSLATORS)
async def test_guard_classification_objects_still_resolve(translator_cls, is_async):
    data = {"classifications": [{"typeName": TAG_ID}, {"typeName": UNKNOWN_TAG_ID}]}

    result = await _translate(translator_cls, is_async, data)

    assert str(result["classifications"][0]["typeName"]) == TAG_NAME
    assert result["classifications"][0][translator_cls._TAG_ID] == TAG_ID
    # An ID the cache does not know still becomes the deleted sentinel.
    assert str(result["classifications"][1]["typeName"]) == DELETED_


@pytest.mark.parametrize("translator_cls, is_async", TRANSLATORS)
async def test_guard_classification_names_still_translate(translator_cls, is_async):
    # classificationNames is a list of hashed IDs by design: unchanged behaviour.
    data = {"classificationNames": [TAG_ID]}

    result = await _translate(translator_cls, is_async, data)

    assert result["classificationNames"] == [TAG_NAME]
