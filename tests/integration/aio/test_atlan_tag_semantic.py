# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
import asyncio
import logging
from typing import AsyncGenerator, List, NamedTuple, Set

import pytest
import pytest_asyncio

from pyatlan.client.aio import AsyncAtlanClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.assets import Table
from pyatlan.model.core import AtlanTag, AtlanTagName
from pyatlan.model.enums import SaveSemantic
from pyatlan.model.fluent_search import FluentSearch

# Table names to search for (in production Snowflake connection)
TABLE1_NAME = "BUYINGGROUPS"
TABLE2_NAME = "CITIES_ARCHIVE"

# Tag names to use in tests
TAG_ISSUE = "Issue"
TAG_CONFIDENTIAL = "Confidential"

LOGGER = logging.getLogger(__name__)


class TableInfo(NamedTuple):
    """Container for table information."""

    name: str
    qualified_name: str


async def find_table_by_name_async(
    client: AsyncAtlanClient, table_name: str, connector_type: str = "snowflake"
) -> TableInfo:
    """
    Find a table by name using FluentSearch, filtering by connector type.

    :param client: AsyncAtlanClient instance
    :param table_name: name of the table to find
    :param connector_type: connector type to filter by (default: snowflake)
    :returns: TableInfo with name and qualified_name
    :raises ValueError: if table not found
    """
    results = await (
        FluentSearch()
        .where(FluentSearch.asset_type(Table))
        .where(Table.NAME.eq(table_name))
        .where(Table.CONNECTOR_NAME.eq(connector_type))
        .include_on_results(Table.NAME)
        .include_on_results(Table.QUALIFIED_NAME)
        .page_size(10)
    ).execute_async(client)

    tables = [asset async for asset in results]
    if not tables:
        raise ValueError(
            f"Table '{table_name}' not found in tenant "
            f"(connector_type={connector_type})"
        )

    # If multiple tables found, log them and use the first one
    if len(tables) > 1:
        LOGGER.warning(
            f"Multiple {connector_type} tables found with name '{table_name}'. "
            f"Using first one. All qualified names: "
            f"{[t.qualified_name for t in tables]}"
        )

    table = tables[0]
    if not table.qualified_name:
        raise ValueError(f"Table '{table_name}' has no qualified_name")

    LOGGER.info(
        f"Found {connector_type} table '{table_name}' "
        f"with qualified_name: {table.qualified_name}"
    )
    return TableInfo(name=table_name, qualified_name=table.qualified_name)


async def get_current_tags_async(
    client: AsyncAtlanClient, qualified_name: str
) -> Set[str]:
    """Helper to retrieve current tags on an asset."""
    asset = await client.asset.get_by_qualified_name(
        qualified_name=qualified_name,
        asset_type=Table,
    )
    return {str(t.type_name) for t in (asset.atlan_tags or [])}


async def remove_tags_from_asset_async(
    client: AsyncAtlanClient, qualified_name: str, name: str, tag_names: List[str]
) -> None:
    """Helper to remove specific tags from an asset."""
    if not tag_names:
        return
    table = Table.updater(qualified_name=qualified_name, name=name)
    table.atlan_tags = [
        AtlanTag.of(atlan_tag_name=AtlanTagName(tag), semantic=SaveSemantic.REMOVE)
        for tag in tag_names
    ]
    try:
        await client.asset.save(entity=table)
    except Exception as e:
        LOGGER.debug(f"Tag removal (may be expected if tag not present): {e}")


async def remove_all_tags_from_asset_async(
    client: AsyncAtlanClient, qualified_name: str, name: str
) -> None:
    """Helper to remove ALL tags from an asset (complete cleanup)."""
    try:
        current_tags = await get_current_tags_async(client, qualified_name)
        if current_tags:
            LOGGER.info(f"Removing all tags from {name}: {current_tags}")
            await remove_tags_from_asset_async(
                client, qualified_name, name, list(current_tags)
            )
    except Exception as e:
        LOGGER.debug(f"Complete tag removal (may be expected): {e}")


@pytest_asyncio.fixture(scope="module")
async def table1(client: AsyncAtlanClient) -> TableInfo:
    """Fixture to find TABLE1 (BUYINGGROUPS) dynamically."""
    return await find_table_by_name_async(client, TABLE1_NAME)


@pytest_asyncio.fixture(scope="module")
async def table2(client: AsyncAtlanClient) -> TableInfo:
    """Fixture to find TABLE2 (CITIES_ARCHIVE) dynamically."""
    return await find_table_by_name_async(client, TABLE2_NAME)


@pytest_asyncio.fixture(scope="module", autouse=True)
async def complete_cleanup_before_tests(
    client: AsyncAtlanClient, table1: TableInfo, table2: TableInfo
) -> AsyncGenerator[None, None]:
    """
    Module-scoped fixture to do a COMPLETE cleanup of ALL tags before any tests run.
    This ensures a clean slate at the start of the test module.
    """
    LOGGER.info("Performing complete cleanup of ALL tags before tests...")

    # Remove ALL tags from both tables
    for table_info in [table1, table2]:
        await remove_all_tags_from_asset_async(
            client,
            table_info.qualified_name,
            table_info.name,
        )
    await asyncio.sleep(3)

    # Verify cleanup was successful
    for table_info in [table1, table2]:
        tags = await get_current_tags_async(client, table_info.qualified_name)
        LOGGER.info(f"After complete cleanup - {table_info.name} tags: {tags}")

    yield

    # Final cleanup after all tests
    LOGGER.info("Final cleanup after all tests...")
    for table_info in [table1, table2]:
        await remove_all_tags_from_asset_async(
            client,
            table_info.qualified_name,
            table_info.name,
        )


@pytest_asyncio.fixture(autouse=True)
async def cleanup_tags(
    client: AsyncAtlanClient, table1: TableInfo, table2: TableInfo
) -> AsyncGenerator[None, None]:
    """
    Fixture to ensure test tags are removed before and after each test.
    This maintains a clean state for testing.
    """
    # Cleanup before test - remove our test tags
    for table_info in [table1, table2]:
        await remove_tags_from_asset_async(
            client,
            table_info.qualified_name,
            table_info.name,
            [TAG_ISSUE, TAG_CONFIDENTIAL],
        )
    await asyncio.sleep(2)

    yield

    # Cleanup after test - remove our test tags
    for table_info in [table1, table2]:
        await remove_tags_from_asset_async(
            client,
            table_info.qualified_name,
            table_info.name,
            [TAG_ISSUE, TAG_CONFIDENTIAL],
        )


@pytest.mark.order(1)
async def test_append_single_tag(
    client: AsyncAtlanClient,
    table1: TableInfo,
) -> None:
    """
    Test APPEND semantic - Add a single tag.
    Expected: Tag is added to the asset.
    """
    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
    ]

    response = await client.asset.save(entity=table)
    await asyncio.sleep(3)

    # Verify response and tags
    assert response is not None
    assert response.mutated_entities is not None
    tags = await get_current_tags_async(client, table1.qualified_name)
    assert TAG_ISSUE in tags
    LOGGER.info(f"APPEND single tag test passed. Tags: {tags}")


@pytest.mark.order(after="test_append_single_tag")
async def test_append_multiple_tags(
    client: AsyncAtlanClient,
    table1: TableInfo,
) -> None:
    """
    Test APPEND semantic - Add multiple tags in one request.
    Expected: All tags are added to the asset.
    """
    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_CONFIDENTIAL),
            semantic=SaveSemantic.APPEND,
        ),
    ]

    response = await client.asset.save(entity=table)
    await asyncio.sleep(3)

    # Verify response and tags
    assert response is not None
    tags = await get_current_tags_async(client, table1.qualified_name)
    assert TAG_ISSUE in tags
    assert TAG_CONFIDENTIAL in tags
    LOGGER.info(f"APPEND multiple tags test passed. Tags: {tags}")


@pytest.mark.order(after="test_append_multiple_tags")
async def test_remove_tag_after_append(
    client: AsyncAtlanClient,
    table1: TableInfo,
) -> None:
    """
    Test REMOVE semantic - Add a tag, then remove it.
    Expected: Tag is removed from the asset.
    """
    # First add a tag
    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
    ]
    await client.asset.save(entity=table)
    await asyncio.sleep(3)

    # Verify tag was added
    tags_after_add = await get_current_tags_async(client, table1.qualified_name)
    assert TAG_ISSUE in tags_after_add, "Setup failed: tag not added"

    # Remove the tag
    table_remove = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table_remove.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.REMOVE,
        ),
    ]
    response = await client.asset.save(entity=table_remove)
    await asyncio.sleep(3)

    # Verify response and tags
    assert response is not None
    tags = await get_current_tags_async(client, table1.qualified_name)
    assert TAG_ISSUE not in tags
    LOGGER.info(f"REMOVE tag test passed. Tags: {tags}")


@pytest.mark.order(after="test_remove_tag_after_append")
async def test_replace_all_tags(
    client: AsyncAtlanClient,
    table2: TableInfo,
) -> None:
    """
    Test REPLACE semantic - Replace all tags with a new one.
    Expected: Only the new tag remains on the asset.
    """
    # First add Issue tag
    table = Table.updater(qualified_name=table2.qualified_name, name=table2.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
    ]
    await client.asset.save(entity=table)
    await asyncio.sleep(3)

    # Verify tag was added
    tags_after_add = await get_current_tags_async(client, table2.qualified_name)
    assert TAG_ISSUE in tags_after_add, "Setup failed: tag not added"

    # Replace with Confidential
    table_replace = Table.updater(
        qualified_name=table2.qualified_name, name=table2.name
    )
    table_replace.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_CONFIDENTIAL),
            semantic=SaveSemantic.REPLACE,
        ),
    ]
    response = await client.asset.save(entity=table_replace)
    await asyncio.sleep(3)

    # Verify response and tags
    assert response is not None
    tags = await get_current_tags_async(client, table2.qualified_name)
    assert TAG_CONFIDENTIAL in tags
    assert TAG_ISSUE not in tags
    LOGGER.info(f"REPLACE tags test passed. Tags: {tags}")


@pytest.mark.order(after="test_replace_all_tags")
async def test_append_and_remove_combined(
    client: AsyncAtlanClient,
    table1: TableInfo,
) -> None:
    """
    Test mixed semantics - APPEND and REMOVE in same request.
    Expected: Issue is added, Confidential is removed.
    """
    # First add Confidential tag
    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_CONFIDENTIAL),
            semantic=SaveSemantic.APPEND,
        ),
    ]
    await client.asset.save(entity=table)
    await asyncio.sleep(3)

    # Verify setup
    tags_after_add = await get_current_tags_async(client, table1.qualified_name)
    assert TAG_CONFIDENTIAL in tags_after_add, (
        "Setup failed: Confidential tag not added"
    )

    # APPEND Issue and REMOVE Confidential in same request
    table_mixed = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table_mixed.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_CONFIDENTIAL),
            semantic=SaveSemantic.REMOVE,
        ),
    ]
    response = await client.asset.save(entity=table_mixed)
    await asyncio.sleep(3)

    # Verify response and tags
    assert response is not None
    tags = await get_current_tags_async(client, table1.qualified_name)
    assert TAG_ISSUE in tags
    assert TAG_CONFIDENTIAL not in tags
    LOGGER.info(f"Mixed APPEND/REMOVE test passed. Tags: {tags}")


@pytest.mark.order(after="test_append_and_remove_combined")
async def test_bulk_save_with_mixed_semantics_raises_error(
    client: AsyncAtlanClient,
    table1: TableInfo,
    table2: TableInfo,
) -> None:
    """
    Test bulk save with APPEND/REMOVE and REPLACE semantics across different assets raises error.
    - Table1: APPEND/REMOVE semantics
    - Table2: REPLACE semantic
    Expected: InvalidRequestError because SDK sets both appendTags and replaceTags to True.

    Note: To save entities with different semantics, use separate save() calls.
    """
    t1 = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    t1.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
    ]

    t2 = Table.updater(qualified_name=table2.qualified_name, name=table2.name)
    t2.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.REPLACE,
        ),
    ]

    # This should raise an error because mixing APPEND/REMOVE and REPLACE
    # in the same save() call sets both appendTags=True and replaceTags=True
    with pytest.raises(InvalidRequestError) as exc_info:
        await client.asset.save(entity=[t1, t2])

    assert "Only one of" in str(exc_info.value) or "replaceTags" in str(exc_info.value)
    LOGGER.info(
        f"Expected error raised for bulk save with mixed semantics: {exc_info.value}"
    )


@pytest.mark.order(after="test_bulk_save_with_mixed_semantics_raises_error")
async def test_mixed_semantics_on_same_asset_raises_error(
    client: AsyncAtlanClient,
    table1: TableInfo,
) -> None:
    """
    Test APPEND and REPLACE semantics on the same asset raises an error.
    SDK sets both appendTags=True and replaceTags=True which backend rejects.
    Expected: InvalidRequestError from server.
    """
    # Apply both APPEND and REPLACE on the same asset
    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_CONFIDENTIAL),
            semantic=SaveSemantic.REPLACE,
        ),
    ]

    # This WILL raise "Only one of [replaceClassifications, replaceTags, appendTags]" error
    # because SDK sets both appendTags=True and replaceTags=True
    with pytest.raises(InvalidRequestError) as exc_info:
        await client.asset.save(entity=table)

    assert "Only one of" in str(exc_info.value) or "replaceTags" in str(exc_info.value)
    LOGGER.info(
        f"Expected error raised for mixed APPEND+REPLACE on same asset: {exc_info.value}"
    )


@pytest.mark.order(after="test_mixed_semantics_on_same_asset_raises_error")
async def test_all_three_semantics_raises_error(
    client: AsyncAtlanClient,
    table1: TableInfo,
) -> None:
    """
    Test that mixing all three semantics (APPEND, REPLACE, None) raises an error.
    SDK sets both appendTags=True and replaceTags=True which backend rejects.
    """
    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            semantic=SaveSemantic.APPEND,
        ),
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_CONFIDENTIAL),
            semantic=SaveSemantic.REPLACE,
        ),
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE),
            # No semantic
        ),
    ]

    # This should raise an error because both appendTags and replaceTags will be True
    with pytest.raises(InvalidRequestError) as exc_info:
        await client.asset.save(entity=table)

    assert "Only one of" in str(exc_info.value) or "replaceTags" in str(exc_info.value)
    LOGGER.info(f"Expected error raised for mixed semantics: {exc_info.value}")


@pytest.mark.order(after="test_all_three_semantics_raises_error")
async def test_backward_compatibility_no_semantic(
    client: AsyncAtlanClient,
    table1: TableInfo,
) -> None:
    """
    Test backward compatibility - tags with no semantic (None) work as before.
    Expected: Tag is added using existing behavior.
    """
    # Use AtlanTag directly without semantic (backward compatible)
    table = Table.updater(qualified_name=table1.qualified_name, name=table1.name)
    table.atlan_tags = [
        AtlanTag.of(
            atlan_tag_name=AtlanTagName(TAG_ISSUE)
        ),  # No semantic - backward compatible
    ]

    response = await client.asset.save(entity=table, replace_atlan_tags=True)
    await asyncio.sleep(3)

    # Verify response and tags
    assert response is not None
    tags = await get_current_tags_async(client, table1.qualified_name)
    assert TAG_ISSUE in tags
    LOGGER.info(f"Backward compatibility test passed. Tags: {tags}")
