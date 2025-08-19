# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import math
from dataclasses import dataclass, field
from datetime import datetime
from time import sleep, time
from typing import AsyncGenerator, Set
from unittest.mock import patch

import httpx
import pytest
import pytest_asyncio
from httpx_retries import Retry
from pydantic.v1 import HttpUrl

from pyatlan.cache.aio.source_tag_cache import AsyncSourceTagName
from pyatlan.client.aio.asset import AsyncIndexSearchResults
from pyatlan.client.aio.atlan import client_connection
from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.client.common.asset import LOGGER
from pyatlan.model.assets import (
    Asset,
    AtlasGlossaryTerm,
    Column,
    Persona,
    Purpose,
    Table,
)
from pyatlan.model.core import AtlanTag, AtlanTagName
from pyatlan.model.enums import AtlanConnectorType, CertificateStatus, SortOrder
from pyatlan.model.fields.atlan_fields import SearchableField
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.search import (
    DSL,
    Exists,
    IndexSearchRequest,
    Match,
    Prefix,
    Range,
    Regexp,
    Term,
    Wildcard,
)
from pyatlan.model.structs import SourceTagAttachment, SourceTagAttachmentValue

from .utils import get_optimized_page_size

QUALIFIED_NAME = "qualifiedName"
ASSET_GUID = Asset.GUID.keyword_field_name
NOW_AS_TIMESTAMP = int(time() * 1000)
NOW_AS_YYYY_MM_DD = datetime.today().strftime("%Y-%m-%d")
EXISTING_TAG = "Issue"
EXISTING_SOURCE_SYNCED_TAG = "Confidential"
DB_NAME = "ANALYTICS"
TABLE_NAME = "STG_STATE_PROVINCES"
COLUMN_NAME = "LATEST_RECORDED_POPULATION"
SCHEMA_NAME = "WIDE_WORLD_IMPORTERS"

VALUES_FOR_TERM_QUERIES = {
    "with_categories": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_classification_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_classifications_text": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_connector_name": AtlanConnectorType.SNOWFLAKE,
    "with_create_time_as_timestamp": 1665727666701,
    "with_created_by": "bryan",
    "with_glossary": "mweSfpXBwfYWedQTvA3Gi",
    "with_guid": "b95eed37-fe38-48d7-8240-0c3390ef4e48",
    "with_has_lineage": True,
    "with_meanings": "2EqDFWZ6sCjbxcDNL0jFV@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_meanings_text": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_modified_by": "bryan",
    "with_name": "Schema",
    "with_owner_groups": "data_engineering",
    "with_owner_users": "ravi",
    "with_parent_category": "fWB1bJLOhEd4ik1Um1EJ8@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_qualified_name": "default/oracle/1665680872/ORCL/SCALE_TEST/TABLE_MVD_3042/PERSON_ID",
    "with_state": "ACTIVE",
    "with_super_type_names": "SQL",
    "with_type_name": "Schema",
    "with_update_time_as_timestamp": 1665723703029,
    "with_certificate_status": CertificateStatus.VERIFIED,
}

VALUES_FOR_TEXT_QUERIES = {
    "with_categories": "VBsYc9dUoEcAtDxZmjby6@mweSfpXBwfYWedQTvA3Gi",
    "with_classification_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_classifications_text": "RBmhFJqX50bl5RAeJhwt1a",
    "with_created_by": "bryan",
    "with_description": "snapshot",
    "with_glossary": "mweSfpXBwfYWedQTvA3Gi",
    "with_guid": "b95eed37-fe38-48d7-8240-0c3390ef4e48",
    "with_has_lineage": True,
    "with_meanings": "2EqDFWZ6sCjbxcDNL0jFV@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_meanings_text": "Term Test",
    "with_modification_timestamp": 1665086276846,
    "with_modified_by": "bryan",
    "with_name": "Schema",
    "with_parent_category": "fWB1bJLOhEd4ik1Um1EJ8@3Wn0W7PFCfjyKmGBZ7FLD",
    "with_propagated_classification_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_qualified_name": "default",
    "with_state": "ACTIVE",
    "with_super_type_names": "ObjectStore SQL",
    "with_timestamp": 1665727666701,
    "with_trait_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_propagated_trait_names": "RBmhFJqX50bl5RAeJhwt1a",
    "with_type_name": "Schema",
    "with_user_description": "this",
}
EXISTING_PURPOSE_NAME = "Known Issues"
EXISTING_PERSONA_NAME = "Business Definitions"


@pytest_asyncio.fixture(scope="module")
async def business_definitions_persona(client: AsyncAtlanClient):
    personas = await client.asset.find_personas_by_name(EXISTING_PERSONA_NAME)
    return personas[0]


@pytest_asyncio.fixture(scope="module")
async def known_issues_purpose(client: AsyncAtlanClient):
    purposes = await client.asset.find_purposes_by_name(EXISTING_PURPOSE_NAME)
    return purposes[0]


@pytest_asyncio.fixture(scope="module")
async def snowflake_conn(client: AsyncAtlanClient):
    connections = await client.asset.find_connections_by_name(
        "development", AtlanConnectorType.SNOWFLAKE
    )
    return connections[0]


@pytest_asyncio.fixture(scope="module")
async def snowflake_column_qn(snowflake_conn):
    return f"{snowflake_conn.qualified_name}/{DB_NAME}/{SCHEMA_NAME}/{TABLE_NAME}/{COLUMN_NAME}"


@dataclass()
class AssetTracker:
    missing_types: Set[str] = field(default_factory=set)
    found_types: Set[str] = field(default_factory=set)


@pytest_asyncio.fixture(scope="module")
async def asset_tracker() -> AsyncGenerator[AssetTracker, None]:
    tracker = AssetTracker()
    yield tracker
    print("Total number of asset types found: ", len(tracker.found_types))
    print("Total number of asset types missing: ", len(tracker.missing_types))
    print("Assets were not found for the following types:")
    for name in sorted(tracker.missing_types):
        print("\t", name)
    print("Assets were found for the following types:")
    for name in sorted(tracker.found_types):
        print("\t", name)


def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


@pytest.mark.parametrize("cls", [(cls) for cls in get_all_subclasses(Asset)])
async def test_search(client: AsyncAtlanClient, asset_tracker, cls):
    name = cls.__name__
    query = Term.with_state("ACTIVE")
    post_filter = Term.with_type_name(name)
    dsl = DSL(query=query, post_filter=post_filter)
    request = IndexSearchRequest(dsl=dsl, attributes=["name"])
    results = await client.asset.search(criteria=request)
    if results.count > 0:
        asset_tracker.found_types.add(name)
        counter = 0
        async for asset in results:
            assert isinstance(asset, cls)
            counter += 1
            if counter > 3:
                break
    else:
        asset_tracker.missing_types.add(name)


def _assert_source_tag(tables, source_tag, source_tag_value):
    assert tables and len(tables) > 0
    for table in tables:
        tags = table.atlan_tags
        assert tags and len(tags) > 0
        synced_tags = [tag for tag in tags if str(tag.type_name) == source_tag]
        assert synced_tags and len(synced_tags) > 0
        for st in synced_tags:
            attachments = st.source_tag_attachments
            assert attachments and len(attachments) > 0
            for sta in attachments:
                values = sta.source_tag_value
                assert values and len(values) > 0
                for value in values:
                    attached_value = value.tag_attachment_value
                    assert attached_value and attached_value == source_tag_value


async def test_search_source_synced_assets(client: AsyncAtlanClient):
    search_results = await (
        FluentSearch()
        .select()
        .where(CompoundQuery.asset_type(Table))
        .where(
            await CompoundQuery.tagged_with_value_async(
                client=client,
                atlan_tag_name=EXISTING_SOURCE_SYNCED_TAG,
                value="Highly Restricted",
            )
        )
        .aexecute(client=client)
    )
    tables = [table async for table in search_results if isinstance(table, Table)]
    _assert_source_tag(tables, EXISTING_SOURCE_SYNCED_TAG, "Highly Restricted")


async def test_source_tag_assign_with_value(client: AsyncAtlanClient, table: Table):
    """
    Test source tag assignment with values using async SourceTagAttachment.by_name_async().

    Note: This test demonstrates that the async implementation is correct, but may be skipped
    due to environmental differences between sync and async source tag cache behavior.
    """
    # Make sure no tags are assigned initially
    assert table.guid
    table = await client.asset.get_by_guid(
        guid=table.guid, asset_type=Table, ignore_relationships=False
    )
    assert not table.atlan_tags
    assert table.name and table.qualified_name

    # Test with the exact same approach as the sync test
    source_tag_name = await AsyncSourceTagName.creator(
        client=client,
        tag="snowflake/development@@ANALYTICS/WIDE_WORLD_IMPORTERS/CONFIDENTIAL",
    )

    # Test our async implementation
    source_tag_attachment = await SourceTagAttachment.by_name_async(
        client=client,
        name=source_tag_name,
        source_tag_values=[
            SourceTagAttachmentValue(tag_attachment_value="Not Restricted")
        ],
    )

    to_update = table.updater(table.qualified_name, table.name)
    to_update.atlan_tags = [
        AtlanTag.of(atlan_tag_name=AtlanTagName(EXISTING_TAG)),
        await AtlanTag.of_async(
            atlan_tag_name=AtlanTagName(EXISTING_SOURCE_SYNCED_TAG),
            source_tag_attachment=source_tag_attachment,
            client=client,
        ),
    ]
    response = await client.asset.save(to_update, replace_atlan_tags=True)

    assert (tables := response.assets_updated(asset_type=Table)) and len(tables) == 1
    assert (
        tables
        and len(tables) == 1
        and tables[0].atlan_tags
        and len(tables[0].atlan_tags) == 2
    )
    for tag in tables[0].atlan_tags:
        assert str(tag.type_name) in (EXISTING_TAG, EXISTING_SOURCE_SYNCED_TAG)

    # Make sure source tag is now attached
    # to the table with the provided value
    sleep(5)
    search_results = await (
        FluentSearch()
        .select()
        .where(CompoundQuery.asset_type(Table))
        .where(Table.QUALIFIED_NAME.eq(table.qualified_name))
        .where(
            await CompoundQuery.tagged_with_value_async(
                client=client,
                atlan_tag_name=EXISTING_SOURCE_SYNCED_TAG,
                value="Not Restricted",
            )
        )
        .aexecute(client=client)
    )
    tables = [table async for table in search_results if isinstance(table, Table)]

    assert (
        tables
        and len(tables) == 1
        and tables[0].atlan_tags
        and len(tables[0].atlan_tags) == 2
    )
    for tag in tables[0].atlan_tags:
        assert str(tag.type_name) in (EXISTING_TAG, EXISTING_SOURCE_SYNCED_TAG)
    _assert_source_tag(tables, EXISTING_SOURCE_SYNCED_TAG, "Not Restricted")


async def test_search_source_specific_custom_attributes(
    client: AsyncAtlanClient, snowflake_column_qn: str
):
    # Test with get_by_qualified_name()
    asset = await client.asset.get_by_qualified_name(
        asset_type=Column,
        qualified_name=snowflake_column_qn,
        min_ext_info=True,
        ignore_relationships=True,
    )
    assert asset and asset.custom_attributes

    # Test with FluentSearch()
    results = await (
        FluentSearch()
        .where(CompoundQuery.active_assets())
        .where(Column.QUALIFIED_NAME.eq(snowflake_column_qn))
        .include_on_results(Column.CUSTOM_ATTRIBUTES)
        .aexecute(client=client)
    )
    assert results and results.count == 1
    assert results.current_page() and len(results.current_page()) == 1
    column = results.current_page()[0]
    assert isinstance(column, Column) and column and column.custom_attributes


async def test_search_next_page(client: AsyncAtlanClient):
    # Get optimized page size for better performance
    total_assets, size = await get_optimized_page_size(
        client=client,
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name(value="AtlasGlossaryTerm"),
        target_api_calls=10,
    )

    # Run the test with optimized page size
    dsl = DSL(
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name(value="AtlasGlossaryTerm"),
        size=size,
    )
    request = IndexSearchRequest(dsl=dsl)
    results = await client.asset.search(criteria=request)
    assert results.count > size
    assert len(results.current_page()) == size
    counter = 0
    while True:
        for _ in results.current_page():
            counter += 1
        if await results.next_page() is not True:
            break
    assert counter == results.count


async def _assert_search_results(
    results, expected_sorts, size, TOTAL_ASSETS, bulk=False
):
    assert results.count > size
    assert len(results.current_page()) == size
    counter = 0
    async for term in results:
        assert term
        counter += 1
    assert counter == TOTAL_ASSETS
    assert results
    assert results._bulk is bulk
    assert results.aggregations is None
    assert results._criteria.dsl.sort == expected_sorts


@patch.object(LOGGER, "debug")
async def test_search_pagination(mock_logger, client: AsyncAtlanClient):
    # Avoid testing on integration tests objects
    exclude_sdk_terms = [
        Asset.NAME.wildcard("psdk_*"),
        Asset.NAME.wildcard("jsdk_*"),
        Asset.NAME.wildcard("gsdk_*"),
    ]
    query = CompoundQuery(
        where_nots=exclude_sdk_terms, where_somes=[CompoundQuery.active_assets()]
    ).to_query()

    # Test search() with DSL: using default offset-based pagination
    # when results are less than the predefined threshold (i.e: 100,000 assets)
    dsl = DSL(
        query=query,
        post_filter=Term.with_type_name(value="AtlasGlossaryTerm"),
        size=0,  # to get the total count
    )

    request = IndexSearchRequest(dsl=dsl)
    results = await client.asset.search(criteria=request)
    # Assigning this here to ensure the total assets
    # remain constant across different test cases
    TOTAL_ASSETS = results.count

    # set page_size to divide into ~5 API calls
    size = max(1, math.ceil(TOTAL_ASSETS / 5))
    request.dsl.size = size

    # Now, we can test different test scenarios for search() with the dynamic page size
    results = await client.asset.search(criteria=request)

    expected_sorts = [Asset.GUID.order(SortOrder.ASCENDING)]
    await _assert_search_results(results, expected_sorts, size, TOTAL_ASSETS)

    # Test search() DSL: with `bulk` option using timestamp-based pagination
    dsl = DSL(
        query=query,
        post_filter=Term.with_type_name(value="AtlasGlossaryTerm"),
        size=size,
    )
    request = IndexSearchRequest(dsl=dsl)
    results = await client.asset.search(criteria=request, bulk=True)
    expected_sorts = [
        Asset.CREATE_TIME.order(SortOrder.ASCENDING),
        Asset.GUID.order(SortOrder.ASCENDING),
    ]
    await _assert_search_results(results, expected_sorts, size, TOTAL_ASSETS, True)
    assert mock_logger.call_count == 1
    assert "Bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()

    # Test search(): using default offset-based pagination
    # when results are less than the predefined threshold (i.e: 100,000 assets)
    request = (
        FluentSearch(where_nots=exclude_sdk_terms)
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .page_size(size)
    ).to_request()
    results = await client.asset.search(criteria=request)
    expected_sorts = [Asset.GUID.order(SortOrder.ASCENDING)]
    await _assert_search_results(results, expected_sorts, size, TOTAL_ASSETS)

    # Test search(): with `bulk` option using timestamp-based pagination
    request = (
        FluentSearch(where_nots=exclude_sdk_terms)
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .page_size(size)
    ).to_request()
    results = await client.asset.search(criteria=request, bulk=True)
    expected_sorts = [
        Asset.CREATE_TIME.order(SortOrder.ASCENDING),
        Asset.GUID.order(SortOrder.ASCENDING),
    ]
    await _assert_search_results(results, expected_sorts, size, TOTAL_ASSETS, True)
    assert mock_logger.call_count == 1
    assert "Bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()

    # Test search() execute(): with `bulk` option using timestamp-based pagination
    results = (
        FluentSearch(where_nots=exclude_sdk_terms)
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .page_size(size)
    ).aexecute(client, bulk=True)
    results = await results
    expected_sorts = [
        Asset.CREATE_TIME.order(SortOrder.ASCENDING),
        Asset.GUID.order(SortOrder.ASCENDING),
    ]
    await _assert_search_results(results, expected_sorts, size, TOTAL_ASSETS, True)
    assert mock_logger.call_count == 1
    assert "Bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()

    # Test search(): when the number of results exceeds the predefined threshold,
    # the SDK automatically switches to a `bulk` search option using timestamp-based pagination.
    with patch.object(AsyncIndexSearchResults, "_MASS_EXTRACT_THRESHOLD", 1):
        request = (
            FluentSearch(where_nots=exclude_sdk_terms)
            .where(CompoundQuery.active_assets())
            .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
            .page_size(size)
        ).to_request()
        results = await client.asset.search(criteria=request)
        expected_sorts = [
            Asset.CREATE_TIME.order(SortOrder.ASCENDING),
            Asset.GUID.order(SortOrder.ASCENDING),
        ]
        await _assert_search_results(results, expected_sorts, size, TOTAL_ASSETS)
        assert mock_logger.call_count < TOTAL_ASSETS
        assert (
            "Result size (%s) exceeds threshold (%s)."
            in mock_logger.call_args_list[0][0][0]
        )
        mock_logger.reset_mock()


async def test_search_iter(client: AsyncAtlanClient):
    # Get optimized page size for better performance
    total_assets, size = await get_optimized_page_size(
        client=client,
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name("AtlasGlossaryTerm"),
        target_api_calls=10,
    )

    # Run the test with optimized page size
    dsl = DSL(
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name("AtlasGlossaryTerm"),
        size=size,
    )
    request = IndexSearchRequest(dsl=dsl)
    results = await client.asset.search(criteria=request)
    assert results.count > size
    assets = [a async for a in results]
    assert len(assets) == results.count


async def test_search_next_when_start_changed_returns_remaining(
    client: AsyncAtlanClient,
):
    # This test specifically tests pagination near the end, so keep size small
    size = 2

    # Get total count to ensure we have enough data for this edge case test
    total_assets, _ = await get_optimized_page_size(
        client=client,
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name("Table"),
        attributes=["databaseName"],
        min_size=size,
    )

    # Ensure we have enough assets for this test
    assert total_assets >= size, f"Need at least {size} assets, got {total_assets}"

    # Run the test with small page size (this test specifically needs small pages)
    dsl = DSL(
        query=Term.with_state("ACTIVE"),
        post_filter=Term.with_type_name("Table"),
        size=size,
    )
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["databaseName"],
    )
    results = await client.asset.search(criteria=request)
    assert await results.next_page(start=results.count - size) is True
    results_list = [item async for item in results]
    assert len(results_list) == size


@pytest.fixture()
def term_query_value(request):
    return VALUES_FOR_TERM_QUERIES[request.param]


@pytest.fixture()
def text_query_value(request):
    return VALUES_FOR_TEXT_QUERIES[request.param]


@pytest.mark.parametrize(
    "term_query_value, method, clazz",
    [
        (method, method, query)
        for query in [Term, Prefix, Regexp, Wildcard]
        for method in sorted(dir(query))
        if method.startswith("with_") and method != "with_custom_metadata"
    ],
    indirect=["term_query_value"],
)
async def test_term_queries_factory(
    client: AsyncAtlanClient, term_query_value, method, clazz
):
    assert hasattr(clazz, method)
    query = getattr(clazz, method)(term_query_value)
    filter = ~Term.with_type_name("__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = await client.asset.search(criteria=request)
    assert results.count >= 0


@pytest.mark.parametrize(
    "with_name",
    [
        (method)
        for method in dir(Exists)
        # if method.startswith("with_") and method != "with_custom_metadata"
        if method == "with_create_time_as_timestamp"
    ],
)
async def test_exists_query_factory(client: AsyncAtlanClient, with_name):
    assert hasattr(Exists, with_name)
    query = getattr(Exists, with_name)()
    filter = ~Term(field="__typeName.keyword", value="__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = await client.asset.search(criteria=request)
    assert results.count >= 0


@pytest.mark.parametrize(
    "text_query_value, method, clazz",
    [
        (method, method, query)
        for query in [Match]
        for method in sorted(dir(query))
        if method.startswith("with_")
    ],
    indirect=["text_query_value"],
)
async def test_text_queries_factory(
    client: AsyncAtlanClient, text_query_value, method, clazz
):
    assert hasattr(clazz, method)
    query = getattr(clazz, method)(text_query_value)
    filter = ~Term.with_type_name("__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = await client.asset.search(criteria=request)
    assert results.count >= 0


@pytest.mark.parametrize(
    "value, method, format",
    [
        (0, "with_popularity_score", None),
        (NOW_AS_TIMESTAMP, "with_create_time_as_timestamp", None),
        (NOW_AS_YYYY_MM_DD, "with_create_time_as_date", "yyyy-MM-dd"),
        (NOW_AS_TIMESTAMP, "with_update_time_as_timestamp", None),
        (NOW_AS_YYYY_MM_DD, "with_update_time_as_date", "yyyy-MM-dd"),
    ],
)
async def test_range_factory(client: AsyncAtlanClient, value, method, format):
    assert hasattr(Range, method)
    query = getattr(Range, method)(lt=value, format=format)
    filter = ~Term(field="__typeName.keyword", value="__AtlasAuditEntry")
    dsl = DSL(query=query, post_filter=filter, size=1)
    request = IndexSearchRequest(
        dsl=dsl,
        attributes=["name"],
    )
    results = await client.asset.search(criteria=request)
    assert results.count >= 0


async def test_bucket_aggregation(client: AsyncAtlanClient):
    request = (
        FluentSearch.select()
        .aggregate("type", Asset.TYPE_NAME.bucket_by())
        .sort(Asset.CREATE_TIME.order())
        .page_size(0)  # only interested in checking aggregation results
    ).to_request()
    results = await client.asset.search(criteria=request)
    assert results.aggregations
    result = results.aggregations["type"]
    assert result
    assert result.buckets
    assert len(result.buckets) > 0
    for bucket in result.buckets:
        assert bucket.key
        assert bucket.doc_count


async def test_nested_bucket_aggregation(client: AsyncAtlanClient):
    nested_aggs_level_2 = Asset.TYPE_NAME.bucket_by(
        nested={"asset_guid": Asset.GUID.bucket_by()}
    )
    nested_aggs = Asset.TYPE_NAME.bucket_by(nested={"asset_name": nested_aggs_level_2})
    request = (
        FluentSearch.select()
        .aggregate("asset_type", nested_aggs)
        .sort(Asset.CREATE_TIME.order())
        .page_size(0)  # only interested in checking aggregation results
        .to_request()
    )
    results = await client.asset.search(criteria=request)

    assert results.aggregations
    result = results.aggregations["asset_type"]
    assert result
    assert result.buckets
    assert len(result.buckets) > 0
    for bucket in result.buckets:
        assert bucket.key
        assert bucket.doc_count
        assert bucket.nested_results
        nested_results = bucket.nested_results["asset_name"]
        assert nested_results
        # Nested results level 1
        for bucket in nested_results.buckets:
            assert bucket.key
            assert bucket.doc_count
            assert bucket.nested_results
            nested_results = bucket.nested_results["asset_guid"]
            assert nested_results
            # Nested results level 2
            for bucket in nested_results.buckets:
                assert bucket.key
                assert bucket.doc_count
                # Make sure it's not nested further
                assert bucket.nested_results is None


async def test_aggregation_source_value(client: AsyncAtlanClient):
    request = (
        FluentSearch.select()
        .aggregate(
            "asset_type",
            Asset.TYPE_NAME.bucket_by(
                nested={
                    "asset_description": Asset.DESCRIPTION.bucket_by(
                        include_source_value=True
                    )
                },
            ),
        )
        .sort(Asset.CREATE_TIME.order())
        .page_size(0)  # only interested in checking aggregation results
        .to_request()
    )
    results = await client.asset.search(criteria=request)

    source_value_found = False
    assert results.aggregations
    result = results.aggregations["asset_type"]
    assert result
    assert result.buckets
    assert len(result.buckets) > 0
    for bucket in result.buckets:
        assert bucket.key
        assert bucket.doc_count
        assert bucket.nested_results
        nested_results = bucket.nested_results["asset_description"]
        assert nested_results
        # Nested results level 1
        for bucket in nested_results.buckets:
            if not bucket.key:
                continue
            assert bucket.key
            assert bucket.doc_count
            assert bucket.nested_results
            if SearchableField.EMBEDDED_SOURCE_VALUE in bucket.nested_results:
                nested_results = bucket.nested_results[
                    SearchableField.EMBEDDED_SOURCE_VALUE
                ]
                assert (
                    nested_results
                    and nested_results.hits
                    and nested_results.hits.hits
                    and nested_results.hits.hits[0]
                )
                assert bucket.get_source_value(Asset.DESCRIPTION)
                source_value_found = True

    if not source_value_found:
        pytest.fail(
            "Failed to retrieve the source value for asset description in the aggregation"
        )


async def test_metric_aggregation(client: AsyncAtlanClient):
    request = (
        FluentSearch()
        .where(Term.with_type_name("Table"))
        .aggregate("avg_columns", Table.COLUMN_COUNT.avg())
        .aggregate("min_columns", Table.COLUMN_COUNT.min())
        .aggregate("max_columns", Table.COLUMN_COUNT.max())
        .aggregate("sum_columns", Table.COLUMN_COUNT.sum())
        .sort(Asset.CREATE_TIME.order())
    ).to_request()
    results = await client.asset.search(criteria=request)
    assert results
    assert results.aggregations
    assert results.aggregations["avg_columns"]
    assert results.aggregations["min_columns"]
    assert results.aggregations["max_columns"]
    assert results.aggregations["sum_columns"]


async def test_index_search_with_no_aggregation_results(client: AsyncAtlanClient):
    test_aggs = {"max_update_time": {"max": {"field": "__modificationTimestamp"}}}
    request = (
        FluentSearch(aggregations=test_aggs).where(  # type:ignore[arg-type]
            Column.QUALIFIED_NAME.startswith("some-non-existent-column-qn")
        )
    ).to_request()
    response = await client.search(criteria=request)

    assert response
    assert response.count == 0
    assert response.aggregations is None


async def test_default_sorting(client: AsyncAtlanClient):
    # Empty sorting
    request = (
        FluentSearch().where(Asset.QUALIFIED_NAME.eq("test-qn", case_insensitive=True))
    ).to_request()
    response = await client.asset.search(criteria=request)
    sort_options = response._criteria.dsl.sort  # type: ignore
    assert response
    assert len(sort_options) == 1
    assert sort_options[0].field == ASSET_GUID

    # Sort without GUID
    request = (
        FluentSearch()
        .where(Asset.QUALIFIED_NAME.eq("test-qn", case_insensitive=True))
        .sort(Asset.QUALIFIED_NAME.order(SortOrder.ASCENDING))
    ).to_request()
    response = await client.asset.search(criteria=request)
    sort_options = response._criteria.dsl.sort  # type: ignore
    assert response
    assert len(sort_options) == 2
    assert sort_options[0].field == QUALIFIED_NAME
    assert sort_options[1].field == ASSET_GUID

    # Sort with only GUID
    request = (
        FluentSearch()
        .where(Asset.QUALIFIED_NAME.eq("test-qn", case_insensitive=True))
        .sort(Asset.GUID.order(SortOrder.ASCENDING))
    ).to_request()
    response = await client.asset.search(criteria=request)
    sort_options = response._criteria.dsl.sort  # type: ignore
    assert response
    assert len(sort_options) == 1
    assert sort_options[0].field == ASSET_GUID

    # Sort with GUID and others
    request = (
        FluentSearch()
        .where(Asset.QUALIFIED_NAME.eq("test-qn", case_insensitive=True))
        .sort(Asset.QUALIFIED_NAME.order(SortOrder.ASCENDING))
        .sort(Asset.GUID.order(SortOrder.ASCENDING))
    ).to_request()
    response = await client.asset.search(criteria=request)
    sort_options = response._criteria.dsl.sort  # type: ignore
    assert response
    assert len(sort_options) == 2
    assert sort_options[0].field == QUALIFIED_NAME
    assert sort_options[1].field == ASSET_GUID


async def test_persona_search(
    client: AsyncAtlanClient,
    business_definitions_persona: Persona,
    known_issues_purpose: Purpose,
):
    request1 = (
        FluentSearch.select()
        .aggregate("type", Asset.TYPE_NAME.bucket_by())
        .sort(Asset.CREATE_TIME.order())
        .page_size(0)  # only interested in checking aggregation results
    ).to_request()

    request2 = (
        FluentSearch.select()
        .aggregate("type", Asset.TYPE_NAME.bucket_by())
        .sort(Asset.CREATE_TIME.order())
        .page_size(0)  # only interested in checking aggregation results
    ).to_request()
    request2.persona = business_definitions_persona.qualified_name

    results_without_persona = await client.asset.search(request1)
    results_with_persona = await client.asset.search(request2)

    # Make sure the results are different (total assets count != glossary assets count)
    assert results_without_persona.count != results_with_persona.count


async def test_purpose_search(client: AsyncAtlanClient, known_issues_purpose: Purpose):
    request1 = (
        FluentSearch.select()
        .aggregate("type", Asset.TYPE_NAME.bucket_by())
        .sort(Asset.CREATE_TIME.order())
        .page_size(0)  # only interested in checking aggregation results
    ).to_request()

    request2 = (
        FluentSearch.select()
        .aggregate("type", Asset.TYPE_NAME.bucket_by())
        .sort(Asset.CREATE_TIME.order())
        .page_size(0)  # only interested in checking aggregation results
    ).to_request()
    request2.purpose = known_issues_purpose.qualified_name

    results_without_purpose = await client.asset.search(request1)
    results_with_purpose = await client.asset.search(request2)

    # Make sure the results are different (total assets count != assets tagged with "Known issues" count)
    assert results_without_purpose.count != results_with_purpose.count


async def test_read_timeout(client: AsyncAtlanClient):
    request = (FluentSearch().select()).to_request()
    async with client_connection(
        client=client, read_timeout=0.1, retry=Retry(total=0)
    ) as timed_client:
        with pytest.raises(httpx.ReadTimeout):
            await timed_client.asset.search(criteria=request)


async def test_connect_timeout(client: AsyncAtlanClient):
    request = FluentSearch().select().to_request()

    # Use a non-routable IP that will definitely timeout
    # 192.0.2.1 is reserved for documentation/testing
    async with client_connection(
        client=client,
        base_url=HttpUrl("http://192.0.2.1:80", scheme="http"),  # Non-routable test IP
        connect_timeout=0.001,
        retry=Retry(total=0),  # No retries to get the raw ConnectTimeout
    ) as timed_client:
        with pytest.raises((httpx.ConnectTimeout)):
            await timed_client.asset.search(criteria=request)
