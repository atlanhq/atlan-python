# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""
Async unit tests for AtlanTag semantic functionality.
Mirrors tests/unit/test_atlan_tag_semantic.py for the async client.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from pyatlan.client.aio.asset import AsyncAssetClient
from pyatlan.client.common import AsyncApiCaller
from pyatlan.client.common.asset import Save
from pyatlan.model.assets import Table
from pyatlan.model.core import AtlanTag, AtlanTagName
from pyatlan.model.enums import SaveSemantic


def test_atlan_tag_semantic_defaults_to_none():
    """Verify AtlanTag.semantic defaults to None for backward compatibility."""
    tag = AtlanTag(type_name=AtlanTagName("TestTag"))
    assert tag.semantic is None


def test_atlan_tag_of_with_semantic():
    """Verify AtlanTag.of() factory method accepts semantic parameter."""
    tag_append = AtlanTag.of(
        atlan_tag_name=AtlanTagName("Tag1"),
        semantic=SaveSemantic.APPEND,
    )
    tag_remove = AtlanTag.of(
        atlan_tag_name=AtlanTagName("Tag2"),
        semantic=SaveSemantic.REMOVE,
    )
    tag_replace = AtlanTag.of(
        atlan_tag_name=AtlanTagName("Tag3"),
        semantic=SaveSemantic.REPLACE,
    )

    assert tag_append.semantic == SaveSemantic.APPEND
    assert tag_remove.semantic == SaveSemantic.REMOVE
    assert tag_replace.semantic == SaveSemantic.REPLACE


def test_atlan_tag_semantic_excluded_from_json():
    """Verify semantic field is excluded from JSON (not sent to API)."""
    tag = AtlanTag(type_name=AtlanTagName("TestTag"), semantic=SaveSemantic.APPEND)
    json_dict = tag.dict(by_alias=True, exclude_none=True)
    assert "semantic" not in json_dict


def test_has_tags_with_semantic_detection():
    """Verify has_tags_with_semantic correctly detects semantic vs non-semantic tags."""
    # Entity with APPEND semantic - should return True
    table_append = Table()
    table_append.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND)
    ]
    assert Save.has_tags_with_semantic([table_append]) is True

    # Entity with no semantic (None) - should return False
    table_none = Table()
    table_none.atlan_tags = [AtlanTag(type_name=AtlanTagName("Tag2"))]
    assert Save.has_tags_with_semantic([table_none]) is False

    # Entity with no tags - should return False
    table_empty = Table()
    table_empty.atlan_tags = None
    assert Save.has_tags_with_semantic([table_empty]) is False


def test_get_semantic_flags():
    """Verify get_semantic_flags correctly identifies APPEND/REMOVE and REPLACE semantics."""
    # APPEND only
    table_append = Table()
    table_append.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND)
    ]
    has_append_remove, has_replace = Save.get_semantic_flags([table_append])
    assert has_append_remove is True
    assert has_replace is False

    # REPLACE only
    table_replace = Table()
    table_replace.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REPLACE)
    ]
    has_append_remove, has_replace = Save.get_semantic_flags([table_replace])
    assert has_append_remove is False
    assert has_replace is True

    # Both APPEND and REPLACE
    table_mixed = Table()
    table_mixed.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REPLACE),
    ]
    has_append_remove, has_replace = Save.get_semantic_flags([table_mixed])
    assert has_append_remove is True
    assert has_replace is True

    # No semantic
    table_none = Table()
    table_none.atlan_tags = [AtlanTag(type_name=AtlanTagName("Tag1"))]
    has_append_remove, has_replace = Save.get_semantic_flags([table_none])
    assert has_append_remove is False
    assert has_replace is False


def test_process_asset_append_remove_semantic():
    """Verify APPEND tags go to add_or_update_classifications, REMOVE to remove_classifications."""
    table = Table()
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("AppendTag"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("RemoveTag"), semantic=SaveSemantic.REMOVE),
    ]

    Save.process_asset_for_append_remove_semantic(table)

    # atlan_tags should be cleared (no REPLACE or None semantic tags to keep)
    assert table.atlan_tags is None
    # APPEND tag should be in add_or_update_classifications
    assert table.add_or_update_classifications is not None
    assert len(table.add_or_update_classifications) == 1
    # REMOVE tag should be in remove_classifications
    assert table.remove_classifications is not None
    assert len(table.remove_classifications) == 1


def test_process_asset_keeps_replace_tags():
    """Verify REPLACE tags remain in atlan_tags after processing."""
    table = Table()
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("AppendTag"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("ReplaceTag"), semantic=SaveSemantic.REPLACE),
    ]

    Save.process_asset_for_append_remove_semantic(table)

    # REPLACE tag should remain in atlan_tags
    assert table.atlan_tags is not None
    assert len(table.atlan_tags) == 1
    assert table.atlan_tags[0].semantic == SaveSemantic.REPLACE
    # APPEND tag should be in add_or_update_classifications
    assert table.add_or_update_classifications is not None
    assert len(table.add_or_update_classifications) == 1


def test_process_asset_keeps_none_semantic_tags():
    """Verify None semantic tags remain in atlan_tags after processing."""
    table = Table()
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("AppendTag"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("NoneTag")),  # None semantic
    ]

    Save.process_asset_for_append_remove_semantic(table)

    # None semantic tag should remain in atlan_tags
    assert table.atlan_tags is not None
    assert len(table.atlan_tags) == 1
    assert table.atlan_tags[0].semantic is None
    # APPEND tag should be in add_or_update_classifications
    assert table.add_or_update_classifications is not None
    assert len(table.add_or_update_classifications) == 1


def test_process_asset_only_replace_tags_unchanged():
    """Verify entity with only REPLACE tags keeps all tags in atlan_tags."""
    table = Table()
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("ReplaceTag"), semantic=SaveSemantic.REPLACE),
    ]

    Save.process_asset_for_append_remove_semantic(table)

    # REPLACE tag should remain in atlan_tags
    assert table.atlan_tags is not None
    assert len(table.atlan_tags) == 1
    # No classification fields should be set
    assert table.add_or_update_classifications is None
    assert table.remove_classifications is None


def test_merge_responses():
    """Verify merge_responses correctly combines multiple AssetMutationResponse objects."""
    from pyatlan.model.response import AssetMutationResponse, MutatedEntities

    table1 = Table()
    table1.guid = "guid1"
    table2 = Table()
    table2.guid = "guid2"

    response1 = AssetMutationResponse(
        guid_assignments={"temp1": "real1"},
        mutated_entities=MutatedEntities(CREATE=[table1]),
    )
    response2 = AssetMutationResponse(
        guid_assignments={"temp2": "real2"},
        mutated_entities=MutatedEntities(UPDATE=[table2]),
    )

    result = Save.merge_responses([response1, response2])

    assert result is not None
    assert result.guid_assignments == {"temp1": "real1", "temp2": "real2"}
    assert result.mutated_entities is not None
    assert result.mutated_entities.CREATE is not None
    assert result.mutated_entities.UPDATE is not None
    assert len(result.mutated_entities.CREATE) == 1
    assert len(result.mutated_entities.UPDATE) == 1


def _create_mock_response():
    """Helper to create a mock API response JSON."""
    return {
        "guidAssignments": {"temp": "real"},
        "mutatedEntities": {
            "CREATE": [],
            "UPDATE": [{"typeName": "Table", "guid": "test-guid"}],
        },
    }


@pytest.fixture
def mock_async_asset_client():
    """Create a mock AsyncAssetClient for testing API call counts."""
    mock_api_caller = MagicMock(spec=AsyncApiCaller)
    mock_api_caller._call_api = AsyncMock(return_value=_create_mock_response())

    # Create AsyncAssetClient with mocked api caller
    client = AsyncAssetClient.__new__(AsyncAssetClient)
    object.__setattr__(client, "_client", mock_api_caller)

    return client, mock_api_caller._call_api


async def test_api_call_count_single_append(mock_async_asset_client):
    """Verify single APPEND semantic results in 1 API call."""
    client, mock_call_api = mock_async_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND)
    ]

    await client.save(entity=table)

    assert mock_call_api.call_count == 1


async def test_api_call_count_single_remove(mock_async_asset_client):
    """Verify single REMOVE semantic results in 1 API call."""
    client, mock_call_api = mock_async_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REMOVE)
    ]

    await client.save(entity=table)

    assert mock_call_api.call_count == 1


async def test_api_call_count_single_replace(mock_async_asset_client):
    """Verify single REPLACE semantic results in 1 API call."""
    client, mock_call_api = mock_async_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REPLACE)
    ]

    await client.save(entity=table)

    assert mock_call_api.call_count == 1


async def test_api_call_count_append_remove_combined(mock_async_asset_client):
    """Verify APPEND and REMOVE on same entity results in 1 API call."""
    client, mock_call_api = mock_async_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REMOVE),
    ]

    await client.save(entity=table)

    # APPEND and REMOVE go in same call (appendTags=True)
    assert mock_call_api.call_count == 1


async def test_api_call_count_append_replace_different_entities(
    mock_async_asset_client,
):
    """Verify APPEND and REPLACE on different entities results in 1 API call (both flags set)."""
    client, mock_call_api = mock_async_asset_client

    table1 = Table()
    table1.qualified_name = "test/table1"
    table1.name = "test_table1"
    table1.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND)
    ]

    table2 = Table()
    table2.qualified_name = "test/table2"
    table2.name = "test_table2"
    table2.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REPLACE)
    ]

    await client.save(entity=[table1, table2])

    # SDK makes single API call with both flags set (backend may return error)
    assert mock_call_api.call_count == 1


async def test_api_call_count_no_semantic(mock_async_asset_client):
    """Verify no semantic (None) results in 1 API call via existing path."""
    client, mock_call_api = mock_async_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"))  # No semantic
    ]

    await client.save(entity=table)

    assert mock_call_api.call_count == 1


async def test_api_call_count_all_three_semantics(mock_async_asset_client):
    """Verify APPEND, REPLACE, and None semantics results in 1 API call."""
    client, mock_call_api = mock_async_asset_client

    table_append = Table()
    table_append.qualified_name = "test/table_append"
    table_append.name = "table_append"
    table_append.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND)
    ]

    table_replace = Table()
    table_replace.qualified_name = "test/table_replace"
    table_replace.name = "table_replace"
    table_replace.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REPLACE)
    ]

    table_none = Table()
    table_none.qualified_name = "test/table_none"
    table_none.name = "table_none"
    table_none.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag3"))  # No semantic
    ]

    await client.save(entity=[table_append, table_replace, table_none])

    # SDK makes single API call (backend may return error if conflicting flags)
    assert mock_call_api.call_count == 1


async def test_api_call_count_multiple_append_batched(mock_async_asset_client):
    """Verify multiple APPEND entities are batched into 1 API call."""
    client, mock_call_api = mock_async_asset_client

    tables = []
    for i in range(5):
        table = Table()
        table.qualified_name = f"test/table_{i}"
        table.name = f"table_{i}"
        table.atlan_tags = [
            AtlanTag(type_name=AtlanTagName(f"Tag{i}"), semantic=SaveSemantic.APPEND)
        ]
        tables.append(table)

    await client.save(entity=tables)

    # All APPEND entities batched into single API call
    assert mock_call_api.call_count == 1


async def test_api_call_count_mixed_on_same_entity(mock_async_asset_client):
    """Verify entity with APPEND+REPLACE+REMOVE results in 1 API call (both flags set)."""
    client, mock_call_api = mock_async_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REPLACE),
        AtlanTag(type_name=AtlanTagName("Tag3"), semantic=SaveSemantic.REMOVE),
    ]

    await client.save(entity=table)

    # SDK makes single API call with both appendTags and replaceTags set
    assert mock_call_api.call_count == 1


async def test_api_call_count_asset_without_tags(mock_async_asset_client):
    """Verify asset without tags results in 1 API call (standard save)."""
    client, mock_call_api = mock_async_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = None  # No tags at all

    await client.save(entity=table)

    # Standard save path = 1 API call
    assert mock_call_api.call_count == 1
