# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from unittest.mock import MagicMock, patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Table
from pyatlan.model.core import AtlanTag, AtlanTagName
from pyatlan.model.enums import SaveSemantic


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture()
def mock_tag_cache(client, monkeypatch):
    mock_cache = MagicMock()
    mock_cache.get_id_for_name.return_value = "test-tag-id"
    mock_cache.get_source_tags_attr_id.return_value = "sourceTagsAttrId"
    monkeypatch.setattr(client, "atlan_tag_cache", mock_cache)
    return mock_cache


class TestAtlanTagSemantic:
    """Test suite for AtlanTag semantic field functionality."""

    def test_atlan_tag_with_semantic_field(self):
        """Test that AtlanTag can be created with semantic field."""
        tag = AtlanTag(
            type_name=AtlanTagName("TestTag"),  # type: ignore[call-arg]
            semantic=SaveSemantic.APPEND,
        )
        assert tag.semantic == SaveSemantic.APPEND
        assert str(tag.type_name) == "TestTag"

    def test_atlan_tag_semantic_default_none(self):
        """Test that semantic defaults to None."""
        tag = AtlanTag(type_name=AtlanTagName("TestTag"))  # type: ignore[call-arg]
        assert tag.semantic is None

    def test_atlan_tag_of_with_semantic_append(self, client, mock_tag_cache):
        """Test AtlanTag.of() with APPEND semantic."""
        tag = AtlanTag.of(
            atlan_tag_name=AtlanTagName("TestTag"),
            entity_guid="test-guid-123",
            semantic=SaveSemantic.APPEND,
            client=client,
        )
        assert tag.semantic == SaveSemantic.APPEND
        assert tag.entity_guid == "test-guid-123"
        assert str(tag.type_name) == "TestTag"

    def test_atlan_tag_of_with_semantic_remove(self, client, mock_tag_cache):
        """Test AtlanTag.of() with REMOVE semantic."""
        tag = AtlanTag.of(
            atlan_tag_name=AtlanTagName("TestTag"),
            entity_guid="test-guid-456",
            semantic=SaveSemantic.REMOVE,
            client=client,
        )
        assert tag.semantic == SaveSemantic.REMOVE
        assert tag.entity_guid == "test-guid-456"

    def test_atlan_tag_of_with_semantic_replace(self, client, mock_tag_cache):
        """Test AtlanTag.of() with REPLACE semantic (default behavior)."""
        tag = AtlanTag.of(
            atlan_tag_name=AtlanTagName("TestTag"),
            entity_guid="test-guid-789",
            semantic=SaveSemantic.REPLACE,
            client=client,
        )
        assert tag.semantic == SaveSemantic.REPLACE
        assert tag.entity_guid == "test-guid-789"

    def test_atlan_tag_of_without_semantic(self, client, mock_tag_cache):
        """Test AtlanTag.of() without semantic parameter (backward compatibility)."""
        tag = AtlanTag.of(
            atlan_tag_name=AtlanTagName("TestTag"),
            entity_guid="test-guid-000",
            client=client,
        )
        assert tag.semantic is None
        assert tag.entity_guid == "test-guid-000"

    @pytest.mark.asyncio
    async def test_atlan_tag_of_async_with_semantic(self, client, mock_tag_cache):
        """Test AtlanTag.of_async() with semantic parameter."""
        # Mock the async methods
        mock_tag_cache.get_id_for_name = MagicMock(return_value="test-tag-id")
        mock_tag_cache.get_source_tags_attr_id = MagicMock(
            return_value="sourceTagsAttrId"
        )

        tag = await AtlanTag.of_async(
            atlan_tag_name=AtlanTagName("TestTag"),
            entity_guid="async-guid-123",
            semantic=SaveSemantic.APPEND,
        )
        assert tag.semantic == SaveSemantic.APPEND
        assert tag.entity_guid == "async-guid-123"


class TestSaveTagSemanticProcessing:
    """Test suite for Save._process_tags_by_semantic functionality."""

    def test_process_tags_append_semantic(self):
        """Test processing tags with APPEND semantic."""
        from pyatlan.client.common.asset import Save

        # Create an asset with tags having APPEND semantic
        asset = Table()
        asset.classifications = [
            AtlanTag(
                type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND  # type: ignore[call-arg]
            ),
            AtlanTag(
                type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.APPEND  # type: ignore[call-arg]
            ),
        ]

        processed_asset = Save._process_tags_by_semantic(asset)

        # Tags with APPEND semantic should be in add_or_update_classifications
        assert processed_asset.add_or_update_classifications is not None
        assert len(processed_asset.add_or_update_classifications) == 2
        assert processed_asset.classifications is None
        assert processed_asset.remove_classifications is None

    def test_process_tags_remove_semantic(self):
        """Test processing tags with REMOVE semantic."""
        from pyatlan.client.common.asset import Save

        asset = Table()
        asset.classifications = [
            AtlanTag(
                type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REMOVE  # type: ignore[call-arg]
            ),
        ]

        processed_asset = Save._process_tags_by_semantic(asset)

        # Tags with REMOVE semantic should be in remove_classifications
        assert processed_asset.remove_classifications is not None
        assert len(processed_asset.remove_classifications) == 1
        assert processed_asset.classifications is None
        assert processed_asset.add_or_update_classifications is None

    def test_process_tags_replace_semantic(self):
        """Test processing tags with REPLACE semantic."""
        from pyatlan.client.common.asset import Save

        asset = Table()
        asset.classifications = [
            AtlanTag(
                type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REPLACE  # type: ignore[call-arg]
            ),
        ]

        processed_asset = Save._process_tags_by_semantic(asset)

        # Tags with REPLACE or None semantic should stay in classifications
        assert processed_asset.classifications is not None
        assert len(processed_asset.classifications) == 1
        assert processed_asset.add_or_update_classifications is None
        assert processed_asset.remove_classifications is None

    def test_process_tags_mixed_semantics(self):
        """Test processing tags with mixed semantics."""
        from pyatlan.client.common.asset import Save

        asset = Table()
        asset.classifications = [
            AtlanTag(
                type_name=AtlanTagName("AppendTag"), semantic=SaveSemantic.APPEND  # type: ignore[call-arg]
            ),
            AtlanTag(
                type_name=AtlanTagName("RemoveTag"), semantic=SaveSemantic.REMOVE  # type: ignore[call-arg]
            ),
            AtlanTag(
                type_name=AtlanTagName("ReplaceTag"), semantic=SaveSemantic.REPLACE  # type: ignore[call-arg]
            ),
        ]

        processed_asset = Save._process_tags_by_semantic(asset)

        # Each semantic should be in its own list
        assert processed_asset.add_or_update_classifications is not None
        assert len(processed_asset.add_or_update_classifications) == 1
        assert (
            str(processed_asset.add_or_update_classifications[0].type_name)
            == "AppendTag"
        )

        assert processed_asset.remove_classifications is not None
        assert len(processed_asset.remove_classifications) == 1
        assert str(processed_asset.remove_classifications[0].type_name) == "RemoveTag"

        assert processed_asset.classifications is not None
        assert len(processed_asset.classifications) == 1
        assert str(processed_asset.classifications[0].type_name) == "ReplaceTag"

    def test_process_tags_none_semantic(self):
        """Test processing tags with None semantic (backward compatibility)."""
        from pyatlan.client.common.asset import Save

        asset = Table()
        asset.classifications = [
            AtlanTag(type_name=AtlanTagName("Tag1"), semantic=None),  # type: ignore[call-arg]
        ]

        processed_asset = Save._process_tags_by_semantic(asset)

        # Tags with None semantic should be treated as REPLACE
        assert processed_asset.classifications is not None
        assert len(processed_asset.classifications) == 1
        assert processed_asset.add_or_update_classifications is None
        assert processed_asset.remove_classifications is None

    def test_process_tags_from_add_or_update_classifications(self):
        """Test processing tags from add_or_update_classifications field."""
        from pyatlan.client.common.asset import Save

        asset = Table()
        asset.add_or_update_classifications = [
            AtlanTag(
                type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND  # type: ignore[call-arg]
            ),
        ]

        processed_asset = Save._process_tags_by_semantic(asset)

        # Should stay in add_or_update_classifications
        assert processed_asset.add_or_update_classifications is not None
        assert len(processed_asset.add_or_update_classifications) == 1

    def test_process_tags_from_remove_classifications(self):
        """Test processing tags from remove_classifications field."""
        from pyatlan.client.common.asset import Save

        asset = Table()
        asset.remove_classifications = [
            AtlanTag(type_name=AtlanTagName("Tag1")),  # type: ignore[call-arg]
        ]

        processed_asset = Save._process_tags_by_semantic(asset)

        # Should stay in remove_classifications
        assert processed_asset.remove_classifications is not None
        assert len(processed_asset.remove_classifications) == 1

    def test_process_tags_no_tags(self):
        """Test processing asset with no tags."""
        from pyatlan.client.common.asset import Save

        asset = Table()
        processed_asset = Save._process_tags_by_semantic(asset)

        # All tag fields should be None
        assert processed_asset.classifications is None
        assert processed_asset.add_or_update_classifications is None
        assert processed_asset.remove_classifications is None

    @patch("pyatlan.client.common.asset.Save.validate_and_flush_entities")
    def test_save_prepare_request_processes_tag_semantics(
        self, mock_validate, client, mock_tag_cache
    ):
        """Test that Save.prepare_request processes tag semantics."""
        from pyatlan.client.common.asset import Save

        # Create assets with different tag semantics
        asset = Table.creator(
            name="test_table", connection_qualified_name="test/connection"
        )
        asset.classifications = [
            AtlanTag(
                type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND  # type: ignore[call-arg]
            ),
            AtlanTag(
                type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REMOVE  # type: ignore[call-arg]
            ),
        ]

        query_params, bulk_request = Save.prepare_request(
            entity=asset, client=client, append_atlan_tags=True
        )

        # Check that tags were processed
        processed_asset = bulk_request.entities[0]
        assert processed_asset.add_or_update_classifications is not None
        assert len(processed_asset.add_or_update_classifications) == 1
        assert processed_asset.remove_classifications is not None
        assert len(processed_asset.remove_classifications) == 1
        assert processed_asset.classifications is None
