# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import pytest

from pyatlan.model.enums import SortOrder
from pyatlan.model.fields.atlan_fields import (
    InternalKeywordTextField,
    KeywordField,
    KeywordTextField,
    SearchableField,
)
from pyatlan.model.search import Exists

ATLAN_FIELD_NAME = "atlan_field_name"
ELASTIC_FIELD_NAME = "elastic_field_name"
INTERNAL_FIELD_NAME = "internal_field_name"
KEYWORD_FIELD_NAME = "keyword_field_name"
TEXT_FIELD_NAME = "text_field_name"


class TestSearchableField:
    @pytest.fixture()
    def sut(self) -> SearchableField:
        return SearchableField(
            atlan_field_name=ATLAN_FIELD_NAME, elastic_field_name=ELASTIC_FIELD_NAME
        )

    def test_internal_field_name(self, sut: SearchableField):
        assert sut.internal_field_name == ATLAN_FIELD_NAME

    def test_atlan_field_name(self, sut: SearchableField):
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_elastic_field_name(self, sut: SearchableField):
        assert sut.elastic_field_name == ELASTIC_FIELD_NAME

    def test_has_any_value(self, sut: SearchableField):
        exists = sut.has_any_value()

        assert isinstance(exists, Exists)
        assert exists.field == sut.elastic_field_name

    def test_order(self, sut: SearchableField):
        order = SortOrder.DESCENDING

        sort_item = sut.order(order=order)

        assert sort_item.order == order
        assert sort_item.field == sut.elastic_field_name


class TestKeywordField:
    @pytest.fixture()
    def sut(self) -> KeywordField:
        return KeywordField(
            atlan_field_name=ATLAN_FIELD_NAME, keyword_field_name=KEYWORD_FIELD_NAME
        )

    def test_internal_field_name(self, sut: KeywordField):
        assert sut.internal_field_name == ATLAN_FIELD_NAME

    def test_atlan_field_name(self, sut: KeywordField):
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_keyword_field_name(self, sut: KeywordField):
        assert sut.keyword_field_name == KEYWORD_FIELD_NAME

    def test_elastic_field_name(self, sut: SearchableField):
        assert sut.elastic_field_name == KEYWORD_FIELD_NAME


class TestKeywordTextField:
    @pytest.fixture()
    def sut(self) -> KeywordTextField:
        return KeywordTextField(
            atlan_field_name=ATLAN_FIELD_NAME,
            keyword_field_name=KEYWORD_FIELD_NAME,
            text_field_name=TEXT_FIELD_NAME,
        )

    def test_internal_field_name(self, sut: KeywordTextField):
        assert sut.internal_field_name == ATLAN_FIELD_NAME

    def test_text_field_name(self, sut: KeywordTextField):
        assert sut.text_field_name == TEXT_FIELD_NAME

    def test_atlan_field_name(self, sut: KeywordTextField):
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_keyword_field_name(self, sut: KeywordTextField):
        assert sut.keyword_field_name == KEYWORD_FIELD_NAME


class TestInternalKeywordTextField:
    @pytest.fixture()
    def sut(self) -> InternalKeywordTextField:
        return InternalKeywordTextField(
            atlan_field_name=ATLAN_FIELD_NAME,
            keyword_field_name=KEYWORD_FIELD_NAME,
            text_field_name=TEXT_FIELD_NAME,
            internal_field_name=INTERNAL_FIELD_NAME,
        )

    def test_internal_field_name(self, sut: InternalKeywordTextField):
        assert sut.internal_field_name == INTERNAL_FIELD_NAME

    def test_text_field_name(self, sut: InternalKeywordTextField):
        assert sut.text_field_name == TEXT_FIELD_NAME

    def test_atlan_field_name(self, sut: InternalKeywordTextField):
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_keyword_field_name(self, sut: InternalKeywordTextField):
        assert sut.keyword_field_name == KEYWORD_FIELD_NAME
