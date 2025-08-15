# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Async utilities for integration tests."""

import logging
import math
from typing import Optional, Type

from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.aio import AsyncIndexSearchResults
from pyatlan.model.api_tokens import ApiToken
from pyatlan.model.assets import Asset, AtlasGlossary, Connection, Database
from pyatlan.model.enums import AtlanConnectorType, AtlanDeleteType, CertificateStatus
from pyatlan.model.search import DSL, IndexSearchRequest

LOGGER = logging.getLogger(__name__)


async def create_token_async(client: AsyncAtlanClient, name: str) -> ApiToken:
    """Create an API token asynchronously."""
    token = await client.token.create(name)
    return token


async def delete_token_async(
    client: AsyncAtlanClient, token: Optional[ApiToken] = None
):
    """Delete an API token asynchronously."""
    # If there is a partial failure on the server side
    # and the token is still visible in the Atlan UI,
    # in that case, the create method may not return a token.
    # We should retrieve the list of all tokens and delete them here.
    if not token:
        tokens_response = await client.token.get()
        tokens = tokens_response.records
        assert tokens
        delete_tokens = [
            token
            for token in tokens
            if token.display_name and "psdk_async" in token.display_name
        ]
        for token in delete_tokens:
            assert token and token.guid
            await client.token.purge(token.guid)
        return
    # In case of no partial failure, directly delete the token
    if token.guid:
        await client.token.purge(token.guid)


async def delete_asset_async(
    client: AsyncAtlanClient,
    guid: str,
    asset_type: Type[Asset],
    delete_type: AtlanDeleteType = AtlanDeleteType.PURGE,
) -> None:
    """Delete an asset asynchronously."""
    try:
        response = await client.asset.purge_by_guid(guid, delete_type)
        if response:
            deleted_assets = response.assets_deleted(asset_type)
            if (
                deleted_assets
                and len(deleted_assets) == 1
                and deleted_assets[0].guid == guid
            ):
                LOGGER.debug(
                    f"Successfully deleted {asset_type.__name__} with GUID {guid}"
                )
            else:
                LOGGER.warning(
                    f"Unexpected response when deleting {asset_type.__name__} with GUID {guid}"
                )
        else:
            LOGGER.warning(
                f"No response when deleting {asset_type.__name__} with GUID {guid}"
            )
    except Exception as e:
        LOGGER.error(f"Failed to remove {asset_type.__name__} with GUID {guid}: {e}")


async def create_connection_async(
    client: AsyncAtlanClient, name: str, connector_type: AtlanConnectorType
) -> Connection:
    """Create a connection asynchronously."""
    role = await client.role_cache.get_id_for_name("$admin")
    assert role
    to_create = await Connection.creator_async(
        client=client, name=name, connector_type=connector_type, admin_roles=[role]
    )
    response = await client.asset.save(to_create)
    return response.assets_created(Connection)[0]


async def create_database_async(client: AsyncAtlanClient, name: str) -> Database:
    """Create a database asynchronously."""
    connection_name = f"{name}_connection"
    connection = await create_connection_async(
        client, connection_name, AtlanConnectorType.VERTICA
    )
    database = Database.creator(
        name=name, connection_qualified_name=connection.qualified_name
    )
    response = await client.asset.save(database)
    return response.assets_created(Database)[0]


async def create_glossary_async(client: AsyncAtlanClient, name: str) -> AtlasGlossary:
    """Create a glossary asynchronously."""
    glossary = AtlasGlossary.creator(name=name)
    response = await client.asset.save(glossary)
    return response.assets_created(AtlasGlossary)[0]


async def update_certificate_async(
    client: AsyncAtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    glossary_guid: Optional[str] = None,
):
    """Update certificate status for an asset asynchronously."""
    assert test_asset.qualified_name
    assert test_asset.name
    test_asset = await client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.qualified_name
    assert test_asset.name
    assert test_asset.certificate_status is None
    assert test_asset.certificate_status_message is None
    message = "An important message"
    await client.asset.update_certificate(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        certificate_status=CertificateStatus.DRAFT,
        message=message,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = await client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.certificate_status == CertificateStatus.DRAFT
    assert test_asset.certificate_status_message == message


async def remove_certificate_async(
    client: AsyncAtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    glossary_guid: Optional[str] = None,
):
    """Remove certificate status from an asset asynchronously."""
    assert test_asset.qualified_name
    assert test_asset.name
    await client.asset.remove_certificate(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = await client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.certificate_status is None
    assert test_asset.certificate_status_message is None


async def update_announcement_async(
    client: AsyncAtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    test_announcement,
    glossary_guid: Optional[str] = None,
):
    """Update announcement for an asset asynchronously."""
    assert test_asset.qualified_name
    assert test_asset.name
    await client.asset.update_announcement(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        announcement=test_announcement,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = await client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.get_announcment() == test_announcement


async def remove_announcement_async(
    client: AsyncAtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    glossary_guid: Optional[str] = None,
):
    """Remove announcement from an asset asynchronously."""
    assert test_asset.qualified_name
    assert test_asset.name
    await client.asset.remove_announcement(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = await client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.get_announcment() is None


async def async_search_request_count_with_retry(
    client: AsyncAtlanClient, request: IndexSearchRequest, expected_count: int
) -> int:
    """
    Execute IndexSearchRequest with retry until expected count is reached (async version).

    :param client: AsyncAtlanClient instance
    :param request: IndexSearchRequest to execute
    :param expected_count: expected count to reach
    :returns: actual count found
    """
    from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

    @retry(
        reraise=True,
        retry=retry_if_result(lambda x: x != expected_count),
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def _retry_search():
        response = await client.asset.search(criteria=request)
        return len(response.current_page())

    return await _retry_search()


async def async_assert_search_count_with_retry(
    client: AsyncAtlanClient, request: IndexSearchRequest, expected_count: int
) -> None:
    """
    Assert search count with retry - convenience method for async test assertions.

    :param client: AsyncAtlanClient instance
    :param request: IndexSearchRequest to execute
    :param expected_count: expected count to assert
    :raises AssertionError: if count doesn't match after retries
    """
    actual_count = await async_search_request_count_with_retry(
        client, request, expected_count
    )
    assert actual_count == expected_count, (
        f"Expected {expected_count} results, got {actual_count}"
    )


async def async_search_with_retry(
    client: AsyncAtlanClient, request: IndexSearchRequest, expected_count: int
) -> AsyncIndexSearchResults:
    """
    Execute search with retry until expected count is reached, then return the results.

    :param client: AsyncAtlanClient instance
    :param request: IndexSearchRequest to execute
    :param expected_count: expected count to reach
    :returns: AsyncIndexSearchResults with the expected count
    """

    @retry(
        reraise=True,
        retry=retry_if_result(
            lambda response: len(response.current_page()) != expected_count
        ),
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def _retry_search():
        return await client.asset.search(criteria=request)

    return await _retry_search()


async def get_optimized_page_size(
    client: AsyncAtlanClient,
    query,
    post_filter=None,
    target_api_calls: int = 10,
    min_size: int = 2,
    attributes=None,
):
    """
    Utility to get optimized page size for search tests by calculating total count first.
    This prevents slow tests by avoiding too many small API calls.

    :param client: AsyncAtlanClient instance
    :param query: Query to use for the search
    :param post_filter: Optional post filter
    :param target_api_calls: Target number of API calls (default 10)
    :param min_size: Minimum page size (default 2)
    :param attributes: Optional attributes for the request
    :returns: tuple of (total_assets_count, optimized_page_size)
    """
    # Get total count
    count_dsl = DSL(
        query=query,
        post_filter=post_filter,
        size=0,  # get total count only
    )
    count_request = IndexSearchRequest(dsl=count_dsl)
    if attributes:
        count_request.attributes = attributes

    count_results = await client.asset.search(criteria=count_request)
    total_assets = count_results.count

    # Calculate optimal page size
    optimal_size = max(min_size, math.ceil(total_assets / target_api_calls))

    return total_assets, optimal_size
