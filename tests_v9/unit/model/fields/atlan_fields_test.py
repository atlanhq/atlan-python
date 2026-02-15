# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Parity tests for searchable field types."""

import pytest

from pyatlan.model.enums import SortOrder
from pyatlan.model.fields.atlan_fields import (
    AtlanSearchableFieldType,
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
    """Tests for SearchableField behavior."""

    @pytest.fixture()
    def sut(self) -> SearchableField:
        """Build a SearchableField instance."""
        return SearchableField(
            atlan_field_name=ATLAN_FIELD_NAME, elastic_field_name=ELASTIC_FIELD_NAME
        )

    def test_internal_field_name(self, sut: SearchableField):
        """Test internal field name."""
        assert sut.internal_field_name == ATLAN_FIELD_NAME

    def test_atlan_field_name(self, sut: SearchableField):
        """Test Atlan field name."""
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_elastic_field_name(self, sut: SearchableField):
        """Test Elasticsearch field name."""
        assert sut.elastic_field_name == ELASTIC_FIELD_NAME

    def test_has_any_value(self, sut: SearchableField):
        """Test has_any_value returns Exists query."""
        exists = sut.has_any_value()

        assert isinstance(exists, Exists)
        assert exists.field == sut.elastic_field_name

    def test_order(self, sut: SearchableField):
        """Test order returns sort item using field and order."""
        order = SortOrder.DESCENDING

        sort_item = sut.order(order=order)

        assert sort_item.order == order
        assert sort_item.field == sut.elastic_field_name


class TestKeywordField:
    """Tests for KeywordField behavior."""

    @pytest.fixture()
    def sut(self) -> KeywordField:
        """Build a KeywordField instance."""
        return KeywordField(
            atlan_field_name=ATLAN_FIELD_NAME, keyword_field_name=KEYWORD_FIELD_NAME
        )

    def test_internal_field_name(self, sut: KeywordField):
        """Test internal field name."""
        assert sut.internal_field_name == ATLAN_FIELD_NAME

    def test_atlan_field_name(self, sut: KeywordField):
        """Test Atlan field name."""
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_keyword_field_name(self, sut: KeywordField):
        """Test keyword field name."""
        assert sut.keyword_field_name == KEYWORD_FIELD_NAME

    def test_elastic_field_name(self, sut: SearchableField):
        """Test Elasticsearch field name maps to keyword field."""
        assert sut.elastic_field_name == KEYWORD_FIELD_NAME


class TestKeywordTextField:
    """Tests for KeywordTextField behavior."""

    @pytest.fixture()
    def sut(self) -> KeywordTextField:
        """Build a KeywordTextField instance."""
        return KeywordTextField(
            atlan_field_name=ATLAN_FIELD_NAME,
            keyword_field_name=KEYWORD_FIELD_NAME,
            text_field_name=TEXT_FIELD_NAME,
        )

    def test_internal_field_name(self, sut: KeywordTextField):
        """Test internal field name."""
        assert sut.internal_field_name == ATLAN_FIELD_NAME

    def test_text_field_name(self, sut: KeywordTextField):
        """Test text field name."""
        assert sut.text_field_name == TEXT_FIELD_NAME

    def test_atlan_field_name(self, sut: KeywordTextField):
        """Test Atlan field name."""
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_keyword_field_name(self, sut: KeywordTextField):
        """Test keyword field name."""
        assert sut.keyword_field_name == KEYWORD_FIELD_NAME

    def test_has_any_value_default_uses_keyword_field(self, sut: KeywordTextField):
        """Test default has_any_value uses keyword field."""
        exists = sut.has_any_value()

        assert isinstance(exists, Exists)
        assert exists.field == KEYWORD_FIELD_NAME

    def test_has_any_value_with_keyword_field_type(self, sut: KeywordTextField):
        """Test has_any_value with KEYWORD type uses keyword field."""
        exists = sut.has_any_value(field_type=AtlanSearchableFieldType.KEYWORD)

        assert isinstance(exists, Exists)
        assert exists.field == KEYWORD_FIELD_NAME

    def test_has_any_value_with_text_field_type(self, sut: KeywordTextField):
        """Test has_any_value with TEXT type uses text field."""
        exists = sut.has_any_value(field_type=AtlanSearchableFieldType.TEXT)

        assert isinstance(exists, Exists)
        assert exists.field == TEXT_FIELD_NAME


class TestInternalKeywordTextField:
    """Tests for InternalKeywordTextField behavior."""

    @pytest.fixture()
    def sut(self) -> InternalKeywordTextField:
        """Build an InternalKeywordTextField instance."""
        return InternalKeywordTextField(
            atlan_field_name=ATLAN_FIELD_NAME,
            keyword_field_name=KEYWORD_FIELD_NAME,
            text_field_name=TEXT_FIELD_NAME,
            internal_field_name=INTERNAL_FIELD_NAME,
        )

    def test_internal_field_name(self, sut: InternalKeywordTextField):
        """Test explicit internal field name."""
        assert sut.internal_field_name == INTERNAL_FIELD_NAME

    def test_text_field_name(self, sut: InternalKeywordTextField):
        """Test text field name."""
        assert sut.text_field_name == TEXT_FIELD_NAME

    def test_atlan_field_name(self, sut: InternalKeywordTextField):
        """Test Atlan field name."""
        assert sut.atlan_field_name == ATLAN_FIELD_NAME

    def test_keyword_field_name(self, sut: InternalKeywordTextField):
        """Test keyword field name."""
        assert sut.keyword_field_name == KEYWORD_FIELD_NAME
