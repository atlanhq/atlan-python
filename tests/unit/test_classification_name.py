# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest

import pyatlan.cache.classification_cache
from pyatlan.model.core import ClassificationName

CLASSIFICATION_ID = "yiB7RLvdC2yeryLPjaDeHM"

GOOD_CLASSIFICATION_NAME = "PII"


def test_init_with_bad_classification_name_raises_value_error(monkeypatch):
    def get_id_for_name(_):
        return None

    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_id_for_name",
        get_id_for_name,
    )
    with pytest.raises(
        ValueError, match=f"{GOOD_CLASSIFICATION_NAME} is not a valid Classification"
    ):
        ClassificationName(GOOD_CLASSIFICATION_NAME)


@pytest.fixture()
def good_classification(monkeypatch):
    def get_id_for_name(value):
        return CLASSIFICATION_ID

    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_id_for_name",
        get_id_for_name,
    )
    return ClassificationName(GOOD_CLASSIFICATION_NAME)


def test_init_with_good_name(monkeypatch):
    def get_id_for_name(value):
        assert value == GOOD_CLASSIFICATION_NAME
        return GOOD_CLASSIFICATION_NAME

    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_id_for_name",
        get_id_for_name,
    )
    sut = ClassificationName(GOOD_CLASSIFICATION_NAME)
    assert sut._display_text == GOOD_CLASSIFICATION_NAME
    assert str(sut) == GOOD_CLASSIFICATION_NAME
    assert sut.__repr__() == f"ClassificationName('{GOOD_CLASSIFICATION_NAME}')"
    assert sut.__hash__() == GOOD_CLASSIFICATION_NAME.__hash__()
    assert ClassificationName(GOOD_CLASSIFICATION_NAME) == sut


def test_convert_to_display_text_when_classification_passed_returns_same_classification(
    monkeypatch, good_classification
):
    assert good_classification is ClassificationName._convert_to_display_text(
        good_classification
    )


def test_convert_to_display_text_when_bad_string_raises_value_error(monkeypatch):
    def get_name_for_id(_):
        return None

    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_name_for_id",
        get_name_for_id,
    )

    with pytest.raises(ValueError, match="bad is not a valid Classification"):
        ClassificationName._convert_to_display_text("bad")


def test_convert_to_display_text_when_id(monkeypatch):
    def get_name_for_id(value):
        return GOOD_CLASSIFICATION_NAME

    def get_id_for_name(value):
        assert value == GOOD_CLASSIFICATION_NAME
        return GOOD_CLASSIFICATION_NAME

    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_id_for_name",
        get_id_for_name,
    )
    monkeypatch.setattr(
        pyatlan.cache.classification_cache.ClassificationCache,
        "get_name_for_id",
        get_name_for_id,
    )

    sut = ClassificationName._convert_to_display_text(CLASSIFICATION_ID)

    assert str(sut) == GOOD_CLASSIFICATION_NAME


def test_json_encode_classification(monkeypatch, good_classification):

    assert (
        ClassificationName.json_encode_classification(good_classification)
        == CLASSIFICATION_ID
    )
