# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""
Unit tests for SaveSemantic feature for in-bulk asset tag management.

Tests cover:
1. AtlanTag semantic field behavior
2. Entity splitting logic based on semantic values
3. Processing of APPEND/REMOVE tags
4. Response merging
"""

from unittest.mock import MagicMock

import pytest

from pyatlan.client.common.asset import Save
from pyatlan.model.assets import Table
from pyatlan.model.core import AtlanTag, AtlanTagName
from pyatlan.model.enums import SaveSemantic


# =============================================================================
# Test 1: AtlanTag semantic field defaults to None (backward compatibility)
# =============================================================================
def test_atlan_tag_semantic_defaults_to_none():
    """Verify AtlanTag.semantic defaults to None for backward compatibility."""
    tag = AtlanTag(type_name=AtlanTagName("TestTag"))
    assert tag.semantic is None


# =============================================================================
# Test 2: AtlanTag.of() accepts semantic parameter
# =============================================================================
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


# =============================================================================
# Test 3: Semantic field is excluded from JSON serialization
# =============================================================================
def test_atlan_tag_semantic_excluded_from_json():
    """Verify semantic field is excluded from JSON (not sent to API)."""
    tag = AtlanTag(type_name=AtlanTagName("TestTag"), semantic=SaveSemantic.APPEND)
    json_dict = tag.dict(by_alias=True, exclude_none=True)
    assert "semantic" not in json_dict


# =============================================================================
# Test 4: has_tags_with_semantic() detects semantic tags
# =============================================================================
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


# =============================================================================
# Test 5: Split entities - APPEND/REMOVE goes to append_remove bucket
# =============================================================================
def test_split_entities_append_remove_bucket():
    """Verify APPEND and REMOVE semantic tags go to append_remove bucket."""
    table_append = Table()
    table_append.qualified_name = "table_append"
    table_append.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND)
    ]

    table_remove = Table()
    table_remove.qualified_name = "table_remove"
    table_remove.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REMOVE)
    ]

    append_remove, replace, no_semantic = Save.split_entities_by_tag_semantic(
        [table_append, table_remove]
    )

    assert len(append_remove) == 2
    assert len(replace) == 0
    assert len(no_semantic) == 0


# =============================================================================
# Test 6: Split entities - REPLACE goes to replace bucket (only if no APPEND/REMOVE)
# =============================================================================
def test_split_entities_replace_bucket():
    """Verify REPLACE semantic tags go to replace bucket when no APPEND/REMOVE present."""
    table_replace = Table()
    table_replace.qualified_name = "table_replace"
    table_replace.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REPLACE)
    ]

    append_remove, replace, no_semantic = Save.split_entities_by_tag_semantic(
        [table_replace]
    )

    assert len(append_remove) == 0
    assert len(replace) == 1
    assert len(no_semantic) == 0


# =============================================================================
# Test 7: Split entities - None semantic goes to no_semantic bucket
# =============================================================================
def test_split_entities_no_semantic_bucket():
    """Verify tags with None semantic (backward compatible) go to no_semantic bucket."""
    table_none = Table()
    table_none.qualified_name = "table_none"
    table_none.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"))  # semantic=None
    ]

    table_no_tags = Table()
    table_no_tags.qualified_name = "table_no_tags"
    table_no_tags.atlan_tags = None

    append_remove, replace, no_semantic = Save.split_entities_by_tag_semantic(
        [table_none, table_no_tags]
    )

    assert len(append_remove) == 0
    assert len(replace) == 0
    assert len(no_semantic) == 2


# =============================================================================
# Test 8: Split entities - Mixed semantics on same entity (APPEND takes priority)
# =============================================================================
def test_split_entities_mixed_semantics_append_priority():
    """Verify entity with both APPEND and REPLACE goes to append_remove (APPEND priority)."""
    table_mixed = Table()
    table_mixed.qualified_name = "table_mixed"
    table_mixed.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REPLACE),
    ]

    append_remove, replace, no_semantic = Save.split_entities_by_tag_semantic(
        [table_mixed]
    )

    # APPEND/REMOVE takes priority - entity goes to append_remove bucket
    assert len(append_remove) == 1
    assert len(replace) == 0
    assert len(no_semantic) == 0


# =============================================================================
# Test 9: Process APPEND/REMOVE - tags moved to correct classification fields
# =============================================================================
def test_process_asset_append_remove_semantic():
    """Verify APPEND tags go to add_or_update_classifications, REMOVE to remove_classifications."""
    table = Table()
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("AppendTag"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("RemoveTag"), semantic=SaveSemantic.REMOVE),
    ]

    Save.process_asset_for_append_remove_semantic(table)

    # atlan_tags should be cleared
    assert table.atlan_tags is None
    # APPEND tag should be in add_or_update_classifications
    assert table.add_or_update_classifications is not None
    assert len(table.add_or_update_classifications) == 1
    # REMOVE tag should be in remove_classifications
    assert table.remove_classifications is not None
    assert len(table.remove_classifications) == 1


# =============================================================================
# Test 10: Merge responses combines multiple API responses correctly
# =============================================================================
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


# =============================================================================
# API Call Count Tests - Verify correct number of API calls for different semantics
# =============================================================================


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
def mock_asset_client():
    """Create a mock AssetClient for testing API call counts."""
    from pyatlan.client.asset import AssetClient
    from pyatlan.client.common import ApiCaller

    mock_api_caller = MagicMock(spec=ApiCaller)
    mock_api_caller._call_api = MagicMock(return_value=_create_mock_response())

    # Create AssetClient with mocked api caller
    client = AssetClient.__new__(AssetClient)
    object.__setattr__(client, "_client", mock_api_caller)

    return client, mock_api_caller._call_api


# =============================================================================
# Test 11: Single APPEND semantic = 1 API call
# =============================================================================
def test_api_call_count_single_append(mock_asset_client):
    """Verify single APPEND semantic results in 1 API call."""
    client, mock_call_api = mock_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND)
    ]

    client.save(entity=table)

    assert mock_call_api.call_count == 1


# =============================================================================
# Test 12: Single REMOVE semantic = 1 API call
# =============================================================================
def test_api_call_count_single_remove(mock_asset_client):
    """Verify single REMOVE semantic results in 1 API call."""
    client, mock_call_api = mock_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REMOVE)
    ]

    client.save(entity=table)

    assert mock_call_api.call_count == 1


# =============================================================================
# Test 13: Single REPLACE semantic = 1 API call
# =============================================================================
def test_api_call_count_single_replace(mock_asset_client):
    """Verify single REPLACE semantic results in 1 API call."""
    client, mock_call_api = mock_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.REPLACE)
    ]

    client.save(entity=table)

    assert mock_call_api.call_count == 1


# =============================================================================
# Test 14: APPEND + REMOVE combined on same entity = 1 API call
# =============================================================================
def test_api_call_count_append_remove_combined(mock_asset_client):
    """Verify APPEND and REMOVE on same entity results in 1 API call."""
    client, mock_call_api = mock_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REMOVE),
    ]

    client.save(entity=table)

    # APPEND and REMOVE go in same call (append_atlan_tags=True)
    assert mock_call_api.call_count == 1


# =============================================================================
# Test 15: APPEND + REPLACE on different entities = 2 API calls
# =============================================================================
def test_api_call_count_append_replace_different_entities(mock_asset_client):
    """Verify APPEND and REPLACE on different entities = 2 API calls."""
    client, mock_call_api = mock_asset_client

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

    client.save(entity=[table1, table2])

    # APPEND and REPLACE require separate API calls
    assert mock_call_api.call_count == 2


# =============================================================================
# Test 16: No semantic (None) = 1 API call (backward compatible)
# =============================================================================
def test_api_call_count_no_semantic(mock_asset_client):
    """Verify no semantic (None) results in 1 API call via existing path."""
    client, mock_call_api = mock_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"))  # No semantic
    ]

    client.save(entity=table)

    assert mock_call_api.call_count == 1


# =============================================================================
# Test 17: APPEND + REPLACE + None semantic = 3 API calls
# =============================================================================
def test_api_call_count_all_three_semantics(mock_asset_client):
    """Verify APPEND, REPLACE, and None semantics on different entities = 3 API calls."""
    client, mock_call_api = mock_asset_client

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

    client.save(entity=[table_append, table_replace, table_none])

    # Three different semantic paths = 3 API calls
    assert mock_call_api.call_count == 3


# =============================================================================
# Test 18: Multiple APPEND entities = 1 API call (batched together)
# =============================================================================
def test_api_call_count_multiple_append_batched(mock_asset_client):
    """Verify multiple APPEND entities are batched into 1 API call."""
    client, mock_call_api = mock_asset_client

    tables = []
    for i in range(5):
        table = Table()
        table.qualified_name = f"test/table_{i}"
        table.name = f"table_{i}"
        table.atlan_tags = [
            AtlanTag(type_name=AtlanTagName(f"Tag{i}"), semantic=SaveSemantic.APPEND)
        ]
        tables.append(table)

    client.save(entity=tables)

    # All APPEND entities batched into single API call
    assert mock_call_api.call_count == 1


# =============================================================================
# Test 19: Mixed APPEND/REMOVE/REPLACE on same entity - APPEND/REMOVE prioritized
# =============================================================================
def test_api_call_count_mixed_on_same_entity(mock_asset_client):
    """Verify entity with APPEND+REPLACE goes to append_remove bucket (1 call)."""
    client, mock_call_api = mock_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = [
        AtlanTag(type_name=AtlanTagName("Tag1"), semantic=SaveSemantic.APPEND),
        AtlanTag(type_name=AtlanTagName("Tag2"), semantic=SaveSemantic.REPLACE),
        AtlanTag(type_name=AtlanTagName("Tag3"), semantic=SaveSemantic.REMOVE),
    ]

    client.save(entity=table)

    # APPEND/REMOVE takes priority, entity goes to append_remove bucket = 1 call
    assert mock_call_api.call_count == 1


# =============================================================================
# Test 20: Asset without tags = 1 API call (no semantic processing)
# =============================================================================
def test_api_call_count_asset_without_tags(mock_asset_client):
    """Verify asset without tags results in 1 API call (standard save)."""
    client, mock_call_api = mock_asset_client

    table = Table()
    table.qualified_name = "test/table"
    table.name = "test_table"
    table.atlan_tags = None  # No tags at all

    client.save(entity=table)

    # Standard save path = 1 API call
    assert mock_call_api.call_count == 1
