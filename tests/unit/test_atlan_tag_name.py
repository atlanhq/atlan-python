# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest

import pyatlan.cache.atlan_tag_cache
from pyatlan.model.core import AtlanTagName

ATLAN_TAG_ID = "yiB7RLvdC2yeryLPjaDeHM"

GOOD_ATLAN_TAG_NAME = "PII"


def test_init_with_bad_atlan_tag_name_raises_value_error(monkeypatch):
    def get_id_for_name(_):
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
def good_atlan_tag(monkeypatch):
    def get_id_for_name(value):
        return ATLAN_TAG_ID

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_id_for_name",
        get_id_for_name,
    )
    return AtlanTagName(GOOD_ATLAN_TAG_NAME)


def test_init_with_good_name(monkeypatch):
    def get_id_for_name(value):
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
    monkeypatch, good_atlan_tag
):
    assert good_atlan_tag is AtlanTagName._convert_to_display_text(good_atlan_tag)


def test_convert_to_display_text_when_bad_string_raises_value_error(monkeypatch):
    def get_name_for_id(_):
        return None

    monkeypatch.setattr(
        pyatlan.cache.atlan_tag_cache.AtlanTagCache,
        "get_name_for_id",
        get_name_for_id,
    )

    with pytest.raises(ValueError, match="bad is not a valid AtlanTag"):
        AtlanTagName._convert_to_display_text("bad")


def test_convert_to_display_text_when_id(monkeypatch):
    def get_name_for_id(value):
        return GOOD_ATLAN_TAG_NAME

    def get_id_for_name(value):
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


def test_json_encode_atlan_tag(monkeypatch, good_atlan_tag):
    assert AtlanTagName.json_encode_atlan_tag(good_atlan_tag) == ATLAN_TAG_ID
