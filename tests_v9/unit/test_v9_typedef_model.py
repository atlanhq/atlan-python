# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import AtlanError
from pyatlan.model.enums import AtlanCustomAttributePrimitiveType
from pyatlan_v9.model.typedef import AttributeDef


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")


@pytest.fixture()
def client():
    return AtlanClient()


class TestV9AttributeDef:
    def test_string_and_rich_text_are_distinct_enum_members(self):
        """Test that STRING and RICH_TEXT are distinct enum members (not aliases)"""
        assert (
            AtlanCustomAttributePrimitiveType.STRING
            is not AtlanCustomAttributePrimitiveType.RICH_TEXT
        )
        assert (
            AtlanCustomAttributePrimitiveType.STRING
            != AtlanCustomAttributePrimitiveType.RICH_TEXT
        )
        assert (
            AtlanCustomAttributePrimitiveType.STRING.value
            != AtlanCustomAttributePrimitiveType.RICH_TEXT.value
        )

    def test_string_attribute_is_not_rich_text(self, client: AtlanClient):
        """Test that STRING attributes do NOT have is_rich_text set"""
        with patch("pyatlan_v9.model.typedef._get_all_qualified_names") as mock_get_qa:
            mock_get_qa.return_value = set()
            attr_def = AttributeDef.creator(
                client=client,
                display_name="Plain String",
                attribute_type=AtlanCustomAttributePrimitiveType.STRING,
            )

        assert attr_def.options
        assert attr_def.options.is_rich_text is False
        assert attr_def.options.primitive_type == "string"
        assert attr_def.type_name == "string"

    def test_rich_text_attribute_creation(self, client: AtlanClient):
        """Test that RICH_TEXT attributes are created with correct options"""
        with patch("pyatlan_v9.model.typedef._get_all_qualified_names") as mock_get_qa:
            mock_get_qa.return_value = set()
            attr_def = AttributeDef.creator(
                client=client,
                display_name="Rich Content",
                attribute_type=AtlanCustomAttributePrimitiveType.RICH_TEXT,
                description="Test rich text attribute",
            )

        assert attr_def.display_name == "Rich Content"
        assert attr_def.type_name == AtlanCustomAttributePrimitiveType.STRING.value
        assert attr_def.description == "Test rich text attribute"
        assert attr_def.options
        assert attr_def.options.is_rich_text is True
        assert attr_def.options.multi_value_select is False

    def test_rich_text_cannot_be_multi_valued(self, client: AtlanClient):
        """Test that RICH_TEXT attributes cannot be multi-valued"""
        with patch("pyatlan_v9.model.typedef._get_all_qualified_names") as mock_get_qa:
            mock_get_qa.return_value = set()
            with pytest.raises(AtlanError) as exc_info:
                AttributeDef.creator(
                    client=client,
                    display_name="Invalid Rich Text",
                    attribute_type=AtlanCustomAttributePrimitiveType.RICH_TEXT,
                    multi_valued=True,
                )

        error = exc_info.value
        assert "ATLAN-PYTHON-400-076" in str(error)

    def test_rich_text_options_configuration(self, client: AtlanClient):
        """Test that RICH_TEXT options are configured correctly"""
        with patch("pyatlan_v9.model.typedef._get_all_qualified_names") as mock_get_qa:
            mock_get_qa.return_value = set()
            attr_def = AttributeDef.creator(
                client=client,
                display_name="Rich Text Field",
                attribute_type=AtlanCustomAttributePrimitiveType.RICH_TEXT,
            )

        options = attr_def.options
        assert options is not None
        assert options.primitive_type == AtlanCustomAttributePrimitiveType.STRING.value
        assert options.is_rich_text is True
        assert options.multi_value_select is False
