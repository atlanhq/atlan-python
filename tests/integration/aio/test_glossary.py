# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import itertools
import logging
from time import sleep
from typing import AsyncGenerator, List, Optional, Union

import pytest
import pytest_asyncio
from pydantic.v1 import StrictStr
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.errors import InvalidRequestError, NotFoundError
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory, AtlasGlossaryTerm
from pyatlan.model.assets.relations import UserDefRelationship
from pyatlan.model.enums import SaveSemantic
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.search import DSL, IndexSearchRequest
from tests.integration.aio.utils import (
    async_assert_fluent_search_count_with_retry,
    async_assert_search_count_with_retry,
    delete_asset_async,
)
from tests.integration.client import TestId

LOGGER = logging.getLogger(__name__)

MODULE_NAME = TestId.make_unique("GLS")

TERM_NAME1 = f"{MODULE_NAME}1"
TERM_NAME2 = f"{MODULE_NAME}2"
TERM_NAME3 = f"{MODULE_NAME}3"
TERM_NAME4 = f"{MODULE_NAME}4"


async def create_glossary(client: AsyncAtlanClient, name: str) -> AtlasGlossary:
    g = AtlasGlossary.create(name=StrictStr(name))
    r = await client.asset.save(g)
    return r.assets_created(AtlasGlossary)[0]


async def create_category(
    client: AsyncAtlanClient,
    name: str,
    glossary: Optional[AtlasGlossary] = None,
    glossary_guid: Optional[str] = None,
    glossary_qualified_name: Optional[str] = None,
    parent: Optional[AtlasGlossaryCategory] = None,
) -> AtlasGlossaryCategory:
    if glossary:
        c = AtlasGlossaryCategory.creator(
            name=name, anchor=glossary, parent_category=parent or None
        )
    elif glossary_guid:
        c = AtlasGlossaryCategory.creator(
            name=name, glossary_guid=glossary_guid, parent_category=parent or None
        )
    elif glossary_qualified_name:
        c = AtlasGlossaryCategory.creator(
            name=name,
            glossary_qualified_name=glossary_qualified_name,
            parent_category=parent or None,
        )
    return (await client.asset.save(c)).assets_created(AtlasGlossaryCategory)[0]


async def create_term(
    client: AsyncAtlanClient,
    name: str,
    glossary: Optional[AtlasGlossary] = None,
    glossary_guid: Optional[str] = None,
    glossary_qualified_name: Optional[str] = None,
    categories: Optional[List[AtlasGlossaryCategory]] = None,
) -> AtlasGlossaryTerm:
    if glossary:
        t = AtlasGlossaryTerm.creator(name=name, anchor=glossary, categories=categories)
    elif glossary_guid:
        t = AtlasGlossaryTerm.creator(
            name=name,
            glossary_guid=glossary_guid,
            categories=categories,
        )
    elif glossary_qualified_name:
        t = AtlasGlossaryTerm.creator(
            name=name,
            glossary_qualified_name=glossary_qualified_name,
            categories=categories,
        )
    r = await client.asset.save(t)
    return r.assets_created(AtlasGlossaryTerm)[0]


@pytest_asyncio.fixture(scope="module")
async def glossary(
    client: AsyncAtlanClient,
) -> AsyncGenerator[AtlasGlossary, None]:
    g = await create_glossary(client, MODULE_NAME)
    yield g
    await delete_asset_async(client, guid=g.guid, asset_type=AtlasGlossary)


async def test_glossary(
    glossary: AtlasGlossary,
):
    assert glossary.guid
    assert glossary.name == MODULE_NAME
    assert glossary.qualified_name
    assert glossary.qualified_name != MODULE_NAME


@pytest_asyncio.fixture(scope="module")
async def category(
    client: AsyncAtlanClient, glossary: AtlasGlossary
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(client, MODULE_NAME, glossary)
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def hierarchy_glossary(
    client: AsyncAtlanClient,
) -> AsyncGenerator[AtlasGlossary, None]:
    g = await create_glossary(client, TestId.make_unique("hierarchy"))
    yield g
    await delete_asset_async(client, guid=g.guid, asset_type=AtlasGlossary)


@pytest_asyncio.fixture(scope="module")
async def top1_category(
    client: AsyncAtlanClient, hierarchy_glossary
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(client, TestId.make_unique("top1"), hierarchy_glossary)
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def mid1a_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("mid1a"), hierarchy_glossary, parent=top1_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def mid1a_term(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1a_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryTerm, None]:
    assert mid1a_category.qualified_name
    t = await create_term(
        client,
        name=f"mid1a_{TERM_NAME1}",
        glossary_guid=hierarchy_glossary.guid,
        categories=[
            AtlasGlossaryCategory.ref_by_qualified_name(mid1a_category.qualified_name)
        ],
    )
    yield t
    await delete_asset_async(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


@pytest_asyncio.fixture(scope="module")
async def leaf1aa_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1a_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    assert hierarchy_glossary and hierarchy_glossary.guid
    c = await create_category(
        client,
        TestId.make_unique("leaf1aa"),
        glossary_guid=hierarchy_glossary.guid,
        parent=mid1a_category,
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def leaf1ab_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1a_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client,
        TestId.make_unique("leaf1ab"),
        glossary_qualified_name=hierarchy_glossary.qualified_name,
        parent=mid1a_category,
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def mid1b_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("mid1b"), hierarchy_glossary, parent=top1_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def leaf1ba_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1b_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("leaf1ba"), hierarchy_glossary, parent=mid1b_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def top2_category(
    client: AsyncAtlanClient, hierarchy_glossary: AtlasGlossary
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(client, TestId.make_unique("top2"), hierarchy_glossary)
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def mid2a_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top2_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("mid2a"), hierarchy_glossary, parent=top2_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def leaf2aa_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid2a_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("leaf2aa"), hierarchy_glossary, parent=mid2a_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def leaf2ab_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid2a_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("leaf2ab"), hierarchy_glossary, parent=mid2a_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def mid2b_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top2_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("mid2b"), hierarchy_glossary, parent=top2_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def leaf2ba_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid2b_category: AtlasGlossaryCategory,
) -> AsyncGenerator[AtlasGlossaryCategory, None]:
    c = await create_category(
        client, TestId.make_unique("leaf2ba"), hierarchy_glossary, parent=mid2b_category
    )
    yield c
    await delete_asset_async(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest_asyncio.fixture(scope="module")
async def term_user_def_relationship() -> UserDefRelationship:
    test_id = MODULE_NAME.lower()
    return UserDefRelationship(
        from_type_label=f"Testing from label ({test_id})",
        to_type_label=f"Testing to label ({test_id})",
    )


async def test_category(
    client: AsyncAtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    assert category.guid
    assert category.name == MODULE_NAME
    assert category.qualified_name
    c = await client.asset.get_by_guid(
        category.guid, AtlasGlossaryCategory, ignore_relationships=False
    )
    assert c
    assert c.guid == category.guid
    assert c.anchor
    assert c.anchor.guid == glossary.guid


@pytest_asyncio.fixture(scope="module")
async def term1(
    client: AsyncAtlanClient, glossary: AtlasGlossary
) -> AsyncGenerator[AtlasGlossaryTerm, None]:
    t = await create_term(client, name=TERM_NAME1, glossary=glossary)
    yield t
    await delete_asset_async(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


async def test_term_failure(
    client: AsyncAtlanClient,
    glossary: AtlasGlossary,
):
    with pytest.raises(
        NotFoundError,
        match="ATLAN-PYTHON-404-000 Server responded with a not found "
        "error ATLAS-404-00-009: Instance AtlasGlossaryTerm with unique attribute *",
    ):
        await client.asset.update_merging_cm(
            AtlasGlossaryTerm.create(
                name=f"{TERM_NAME1} X", glossary_guid=glossary.guid
            )
        )


async def test_term1(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1.guid
    assert term1.name == TERM_NAME1
    assert term1.qualified_name
    assert term1.qualified_name != TERM_NAME1
    t = await client.asset.get_by_guid(
        term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert t
    assert t.guid == term1.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest_asyncio.fixture(scope="module")
async def term2(
    client: AsyncAtlanClient, glossary: AtlasGlossary
) -> AsyncGenerator[AtlasGlossaryTerm, None]:
    t = await create_term(client, name=TERM_NAME2, glossary_guid=glossary.guid)
    yield t
    await delete_asset_async(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


async def test_term2(
    client: AsyncAtlanClient,
    term2: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term2.guid
    assert term2.name == TERM_NAME2
    assert term2.qualified_name
    assert term2.qualified_name != TERM_NAME2
    t = await client.asset.get_by_guid(
        term2.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert t
    assert t.guid == term2.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest_asyncio.fixture(scope="module")
async def term3(
    client: AsyncAtlanClient, glossary: AtlasGlossary
) -> AsyncGenerator[AtlasGlossaryTerm, None]:
    t = await create_term(
        client, name=TERM_NAME3, glossary_qualified_name=glossary.qualified_name
    )
    yield t
    await delete_asset_async(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


async def test_term3(
    client: AsyncAtlanClient,
    term3: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term3.guid
    assert term3.name == TERM_NAME3
    assert term3.qualified_name
    assert term3.qualified_name != TERM_NAME3
    t = await client.asset.get_by_guid(
        term3.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert t
    assert t.guid == term3.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest_asyncio.fixture(scope="module")
async def term4(
    client: AsyncAtlanClient, glossary: AtlasGlossary
) -> AsyncGenerator[AtlasGlossaryTerm, None]:
    t = await create_term(client, name=TERM_NAME4, glossary_guid=glossary.guid)
    yield t
    await delete_asset_async(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


async def test_term4(
    client: AsyncAtlanClient,
    term4: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term4.guid
    assert term4.name == TERM_NAME4
    assert term4.qualified_name
    assert term4.qualified_name != TERM_NAME4
    t = await client.asset.get_by_guid(
        term4.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert t
    assert t.guid == term4.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


async def test_read_glossary(
    client: AsyncAtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    term4: AtlasGlossaryTerm,
):
    g = await client.asset.get_by_guid(
        glossary.guid, asset_type=AtlasGlossary, ignore_relationships=False
    )
    assert g
    assert isinstance(g, AtlasGlossary)
    assert g.guid == glossary.guid
    assert g.qualified_name == glossary.qualified_name
    assert g.name == glossary.name
    terms = g.terms
    assert terms
    assert len(terms) == 4


async def test_compound_queries(
    client: AsyncAtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    term4: AtlasGlossaryTerm,
):
    assert glossary.qualified_name
    cq = (
        CompoundQuery()
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .where(AtlasGlossaryTerm.NAME.startswith(MODULE_NAME))
        .where(AtlasGlossaryTerm.ANCHOR.eq(glossary.qualified_name))
    ).to_query()
    request = IndexSearchRequest(dsl=DSL(query=cq))
    # Use centralized retry utility for eventual consistency
    await async_assert_search_count_with_retry(client, request, expected_count=4)
    assert glossary.qualified_name
    assert term2.name

    cq = (
        CompoundQuery()
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .where(AtlasGlossaryTerm.NAME.startswith(MODULE_NAME))
        .where(AtlasGlossaryTerm.ANCHOR.eq(glossary.qualified_name))
        .where_not(AtlasGlossaryTerm.NAME.eq(term2.name))
    ).to_query()
    request = IndexSearchRequest(dsl=DSL(query=cq))
    # Use centralized retry utility for eventual consistency
    await async_assert_search_count_with_retry(client, request, expected_count=3)


async def test_fluent_search(
    client: AsyncAtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    term4: AtlasGlossaryTerm,
):
    assert glossary.qualified_name
    terms = (
        FluentSearch()
        .page_size(1)
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossaryTerm))
        .where(AtlasGlossaryTerm.NAME.startswith(MODULE_NAME))
        .where(AtlasGlossaryTerm.ANCHOR.eq(glossary.qualified_name))
        .include_on_results(AtlasGlossaryTerm.ANCHOR)
        .include_on_relations(AtlasGlossary.NAME)
    )

    # Use centralized retry utility to handle search index eventual consistency
    await async_assert_fluent_search_count_with_retry(terms, client, expected_count=4)

    guids_chained = []
    g_sorted = []

    # Execute the async search and collect results into a list first
    search_results = await terms.aexecute(client)
    all_results = []
    async for asset in search_results:
        all_results.append(asset)

    # Now use itertools.islice like sync version
    for asset in filter(
        lambda x: isinstance(x, AtlasGlossaryTerm),
        itertools.islice(all_results, 4),
    ):
        guids_chained.append(asset.guid)
        g_sorted.append(asset.guid)
    g_sorted.sort()
    assert guids_chained == g_sorted

    results = await FluentSearch(
        _page_size=5,
        wheres=[
            CompoundQuery.active_assets(),
            CompoundQuery.asset_type(AtlasGlossaryTerm),
            AtlasGlossaryTerm.NAME.startswith(MODULE_NAME),
            AtlasGlossaryTerm.ANCHOR.startswith(glossary.qualified_name),
        ],
        _includes_on_results=[AtlasGlossaryTerm.ANCHOR.atlan_field_name],
        _includes_on_relations=[AtlasGlossary.NAME.atlan_field_name],
    ).aexecute(client)

    guids_alt = []
    g_sorted = []
    async for asset in results:
        guids_alt.append(asset.guid)
        g_sorted.append(asset.guid)
    g_sorted.sort()
    assert g_sorted == guids_alt
    assert glossary.qualified_name

    async_results = await FluentSearch(
        _page_size=5,
        wheres=[
            CompoundQuery.active_assets(),
            CompoundQuery.asset_type(AtlasGlossaryTerm),
            AtlasGlossaryTerm.NAME.startswith(MODULE_NAME),
            AtlasGlossaryTerm.ANCHOR.startswith(glossary.qualified_name),
        ],
        _includes_on_results=["anchor"],
        _includes_on_relations=["name"],
        sorts=[AtlasGlossaryTerm.NAME.order()],
    ).aexecute(client)

    names = []
    names_sorted = []
    async for asset in async_results:
        names.append(asset.name)
        names_sorted.append(asset.name)
    names_sorted.sort()
    assert names_sorted == names


@pytest.mark.order(after="test_read_glossary")
async def test_trim_to_required_glossary(
    client: AsyncAtlanClient,
    glossary: AtlasGlossary,
):
    glossary = glossary.trim_to_required()
    response = await client.asset.save(glossary)
    assert response.mutated_entities is None


@pytest.mark.order(after="test_term1")
async def test_term_trim_to_required(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
):
    term1 = await client.asset.get_by_guid(
        guid=term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    term1 = term1.trim_to_required()
    response = await client.asset.save(term1)
    assert response.mutated_entities is None


async def test_find_glossary_by_name(client: AsyncAtlanClient, glossary: AtlasGlossary):
    found_glossary = await client.asset.find_glossary_by_name(name=glossary.name)
    assert glossary.guid == found_glossary.guid


async def test_find_category_fast_by_name(
    client: AsyncAtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    @retry(
        wait=wait_fixed(2),
        retry=retry_if_exception_type(NotFoundError),
        stop=stop_after_attempt(3),
    )
    async def check_it():
        result = await client.asset.find_category_fast_by_name(
            name=category.name, glossary_qualified_name=glossary.qualified_name
        )
        assert category.guid == result[0].guid

    await check_it()


async def test_find_category_by_name(
    client: AsyncAtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    result = await client.asset.find_category_by_name(
        name=category.name, glossary_name=glossary.name
    )
    assert category.guid == result[0].guid


async def test_find_category_by_name_qn_guid_correctly_populated(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
    top2_category: AtlasGlossaryCategory,
    mid1a_category: AtlasGlossaryCategory,
    mid1a_term: AtlasGlossaryTerm,
    mid2a_category: AtlasGlossaryCategory,
):
    categories = await client.asset.find_category_by_name(
        name=mid1a_category.name,
        glossary_name=hierarchy_glossary.name,
        attributes=["terms", "anchor", "parentCategory"],
    )
    category = categories[0]

    # Glossary
    assert category.anchor
    assert category.anchor.guid == hierarchy_glossary.guid
    assert category.anchor.name == hierarchy_glossary.name
    assert category.anchor.qualified_name == hierarchy_glossary.qualified_name

    # Glossary category
    assert category.parent_category
    assert category.parent_category.guid == top1_category.guid
    assert category.parent_category.name == top1_category.name
    assert category.parent_category.qualified_name == top1_category.qualified_name

    # Glossary term
    assert category.terms and category.terms[0]
    assert category.terms[0].guid == mid1a_term.guid
    assert category.terms[0].name == mid1a_term.name
    assert category.terms[0].qualified_name == mid1a_term.qualified_name


async def test_category_delete_by_guid_raises_error_invalid_request_error(
    client: AsyncAtlanClient, category: AtlasGlossaryCategory
):
    with pytest.raises(
        InvalidRequestError,
        match=f"ATLAN-PYTHON-400-052 Asset with guid: {category.guid} is an asset "
        "of type AtlasGlossaryCategory which does not support archiving. "
        "Suggestion: Please use purge if you wish to remove assets of this type.",
    ):
        await client.asset.delete_by_guid(guid=category.guid)


async def test_find_term_fast_by_name(
    client: AsyncAtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    @retry(
        wait=wait_fixed(2),
        retry=retry_if_exception_type(NotFoundError),
        stop=stop_after_attempt(3),
    )
    async def check_it():
        result = await client.asset.find_term_fast_by_name(
            name=term1.name, glossary_qualified_name=glossary.qualified_name
        )
        assert term1.guid == result.guid

    await check_it()


async def test_find_term_by_name(
    client: AsyncAtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    result = await client.asset.find_term_by_name(
        name=term1.name, glossary_name=glossary.name
    )
    assert term1.guid == result.guid


@pytest.mark.parametrize(
    "attributes, related_attributes",
    [
        (AtlasGlossaryCategory.TERMS, AtlasGlossaryTerm.NAME),
        (
            AtlasGlossaryCategory.TERMS.atlan_field_name,
            AtlasGlossaryTerm.NAME.atlan_field_name,
        ),
    ],
)
async def test_hierarchy(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
    mid1a_category: AtlasGlossaryCategory,
    leaf1aa_category: AtlasGlossaryCategory,
    leaf1ab_category: AtlasGlossaryCategory,
    mid1b_category: AtlasGlossaryCategory,
    leaf1ba_category: AtlasGlossaryCategory,
    top2_category: AtlasGlossaryCategory,
    mid2a_category: AtlasGlossaryCategory,
    leaf2aa_category: AtlasGlossaryCategory,
    leaf2ab_category: AtlasGlossaryCategory,
    mid2b_category: AtlasGlossaryCategory,
    leaf2ba_category: AtlasGlossaryCategory,
    attributes: Union[AtlanField, str],
    related_attributes: Union[AtlanField, str],
):
    sleep(10)
    hierarchy = await client.asset.get_hierarchy(
        glossary=hierarchy_glossary,
        attributes=[attributes],
        related_attributes=[related_attributes],
    )

    root_categories = hierarchy.root_categories

    assert root_categories
    assert len(root_categories) == 2
    assert root_categories[0].name
    assert root_categories[1].name
    assert "top" in root_categories[0].name
    assert "top" in root_categories[1].name
    assert hierarchy.get_category(top1_category.guid)
    category_without_terms = hierarchy.get_category(top1_category.guid)
    assert category_without_terms.terms is not None
    assert 0 == len(category_without_terms.terms)
    assert hierarchy.get_category(mid1a_category.guid)
    category_with_term = hierarchy.get_category(mid1a_category.guid)
    assert category_with_term.terms
    assert 1 == len(category_with_term.terms)
    assert f"mid1a_{TERM_NAME1}" == category_with_term.terms[0].name
    assert hierarchy.get_category(leaf1aa_category.guid)
    assert hierarchy.get_category(leaf1ab_category.guid)
    assert hierarchy.get_category(mid1b_category.guid)
    assert hierarchy.get_category(leaf1ba_category.guid)
    assert hierarchy.get_category(top2_category.guid)
    assert hierarchy.get_category(mid2a_category.guid)
    assert hierarchy.get_category(leaf2aa_category.guid)
    assert hierarchy.get_category(leaf2ab_category.guid)
    assert hierarchy.get_category(mid2b_category.guid)
    assert hierarchy.get_category(leaf2ba_category.guid)

    category_names = [category.name for category in hierarchy.breadth_first]

    assert len(category_names) == 12
    assert category_names
    assert category_names[0]
    assert category_names[1]
    assert category_names[2]
    assert category_names[3]
    assert category_names[4]
    assert category_names[5]
    assert category_names[6]
    assert category_names[7]
    assert category_names[8]
    assert category_names[9]
    assert category_names[10]
    assert category_names[11]
    assert "top" in category_names[0]
    assert "top" in category_names[1]
    assert "mid" in category_names[2]
    assert "mid" in category_names[3]
    assert "mid" in category_names[4]
    assert "mid" in category_names[5]
    assert "leaf" in category_names[6]
    assert "leaf" in category_names[7]
    assert "leaf" in category_names[8]
    assert "leaf" in category_names[9]
    assert "leaf" in category_names[10]
    assert "leaf" in category_names[11]

    category_names = [category.name for category in hierarchy.depth_first]

    assert len(category_names) == 12
    assert category_names
    assert category_names[0]
    assert category_names[1]
    assert category_names[2]
    assert category_names[3]
    assert category_names[4]
    assert category_names[5]
    assert category_names[6]
    assert category_names[7]
    assert category_names[8]
    assert category_names[9]
    assert category_names[10]
    assert category_names[11]
    assert "top" in category_names[0]
    assert "mid" in category_names[1]
    assert "leaf" in category_names[2]
    assert "leaf" in category_names[3]
    assert "mid" in category_names[4]
    assert "leaf" in category_names[5]
    assert "top" in category_names[6]
    assert "mid" in category_names[7]
    assert "leaf" in category_names[8]
    assert "leaf" in category_names[9]
    assert "mid" in category_names[10]
    assert "leaf" in category_names[11]


async def test_create_relationship(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1
    assert term1.name
    assert term1.qualified_name

    term = AtlasGlossaryTerm.create_for_modification(
        qualified_name=term1.qualified_name,
        name=term1.name,
        glossary_guid=glossary.guid,
    )
    term.see_also = [
        AtlasGlossaryTerm.ref_by_guid(guid=term2.guid),
        AtlasGlossaryTerm.ref_by_guid(guid=term3.guid),
    ]
    response = await client.asset.save(term)

    assert response
    result = await client.asset.get_by_guid(
        guid=term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert result
    assert result.see_also
    assert len(result.see_also) == 2
    related_guids = []
    for term in result.see_also:
        assert term.guid
        related_guids.append(term.guid)
    assert term2.guid in related_guids
    assert term3.guid in related_guids


@pytest.mark.order(after="test_create_relationship")
async def test_remove_relationship(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1
    assert term1.name
    assert term1.qualified_name

    term = AtlasGlossaryTerm.create_for_modification(
        qualified_name=term1.qualified_name,
        name=term1.name,
        glossary_guid=glossary.guid,
    )
    term.see_also = [
        AtlasGlossaryTerm.ref_by_guid(guid=term2.guid, semantic=SaveSemantic.REMOVE),
    ]
    response = await client.asset.save(term)

    assert response
    result = await client.asset.get_by_guid(
        guid=term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert result
    assert result.see_also
    active_relationships = []
    for term in result.see_also:
        assert term.guid
        if term.relationship_status == "ACTIVE":
            active_relationships.append(term)
    assert len(active_relationships) == 1
    assert term3.guid == active_relationships[0].guid


@pytest.mark.order(after="test_remove_relationship")
async def test_append_relationship(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    term4: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1
    assert term1.name
    assert term1.qualified_name

    term = AtlasGlossaryTerm.create_for_modification(
        qualified_name=term1.qualified_name,
        name=term1.name,
        glossary_guid=glossary.guid,
    )
    term.see_also = [
        AtlasGlossaryTerm.ref_by_guid(guid=term4.guid, semantic=SaveSemantic.APPEND),
    ]
    response = await client.asset.save(term)

    assert response
    result = await client.asset.get_by_guid(
        guid=term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert result
    assert result.see_also
    active_relationships = []
    for term in result.see_also:
        assert term.guid
        if term.relationship_status == "ACTIVE":
            active_relationships.append(term.guid)
    assert len(active_relationships) == 2
    assert term3.guid in active_relationships
    assert term4.guid in active_relationships


@pytest.mark.order(after="test_append_relationship")
async def test_append_relationship_again(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    term4: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1
    assert term1.name
    assert term1.qualified_name

    term = AtlasGlossaryTerm.create_for_modification(
        qualified_name=term1.qualified_name,
        name=term1.name,
        glossary_guid=glossary.guid,
    )
    term.see_also = [
        AtlasGlossaryTerm.ref_by_guid(guid=term4.guid, semantic=SaveSemantic.APPEND),
    ]
    response = await client.asset.save(term)

    assert response
    result = await client.asset.get_by_guid(
        guid=term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert result
    assert result.see_also
    active_relationships = []
    for term in result.see_also:
        assert term.guid
        if term.relationship_status == "ACTIVE":
            active_relationships.append(term.guid)
    assert len(active_relationships) == 2
    assert term3.guid in active_relationships
    assert term4.guid in active_relationships


@pytest.mark.order(after="test_append_relationship_again")
async def test_remove_unrelated_relationship(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1
    assert term1.name
    assert term1.qualified_name

    term = AtlasGlossaryTerm.create_for_modification(
        qualified_name=term1.qualified_name,
        name=term1.name,
        glossary_guid=glossary.guid,
    )
    term.see_also = [
        AtlasGlossaryTerm.ref_by_guid(guid=term2.guid, semantic=SaveSemantic.REMOVE),
    ]
    with pytest.raises(NotFoundError) as err:
        await client.asset.save(term)

    EXPECTED_ERR = (
        "ATLAN-PYTHON-404-000 Server responded with a not found error ATLAS-409-00-0021: "
        "relationship AtlasGlossaryRelatedTerm does "
        f"not exist between entities {term2.guid} and {term1.guid}. "
        "Suggestion: Check the details of the server's message to correct your request."
    )
    assert EXPECTED_ERR == str(err.value)


async def test_move_sub_category_to_category(
    client: AsyncAtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
    top2_category: AtlasGlossaryCategory,
    mid1a_category: AtlasGlossaryCategory,
    mid2a_category: AtlasGlossaryCategory,
):
    sleep(10)
    assert mid1a_category.name
    assert hierarchy_glossary.guid
    assert top1_category.qualified_name
    assert top2_category.qualified_name
    assert mid1a_category.qualified_name

    hierarchy = await client.asset.get_hierarchy(glossary=hierarchy_glossary)
    root_categories = hierarchy.root_categories

    assert len(root_categories) == 2
    root_category_qns = (
        root_categories[0].qualified_name,
        root_categories[1].qualified_name,
    )
    assert top1_category.qualified_name in root_category_qns
    assert top2_category.qualified_name in root_category_qns

    mid1a_category = AtlasGlossaryCategory.updater(
        name=mid1a_category.name,
        qualified_name=mid1a_category.qualified_name,
        glossary_guid=hierarchy_glossary.guid,
    )
    mid1a_category.parent_category = None
    response = await client.asset.save(mid1a_category)

    if updated := response.assets_updated(asset_type=AtlasGlossaryCategory):
        assert updated[0].name == mid1a_category.name
        assert updated[0].qualified_name == mid1a_category.qualified_name
    else:
        pytest.fail(f"Failed to perform update on category: {mid1a_category.name}")

    # Ensure that the sub-category 'mid1a_category'
    # has been successfully moved to the root category
    sleep(10)
    hierarchy = await client.asset.get_hierarchy(glossary=hierarchy_glossary)
    root_categories = hierarchy.root_categories

    assert len(root_categories) == 3
    root_category_qns_updated = (
        root_categories[0].qualified_name,
        root_categories[1].qualified_name,
        root_categories[2].qualified_name,
    )
    assert top1_category.qualified_name in root_category_qns_updated
    assert top2_category.qualified_name in root_category_qns_updated
    assert mid1a_category.qualified_name in root_category_qns_updated


async def test_user_def_relationship_on_terms(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
    term_user_def_relationship: UserDefRelationship,
):
    term1_to_update = AtlasGlossaryTerm.updater(
        qualified_name=term1.qualified_name,
        name=term1.name,
        glossary_guid=glossary.guid,
    )
    term2 = AtlasGlossaryTerm.ref_by_guid(term2.guid)
    term1_to_update.user_def_relationship_to = [
        term_user_def_relationship.user_def_relationship_to(term2)
    ]

    response = await client.asset.save(term1_to_update)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE is None
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 2
    assets = response.assets_updated(asset_type=AtlasGlossaryTerm)
    assert len(assets) == 2


def _assert_relationship(relationship, expected_type_name, udr):
    assert relationship
    assert relationship.guid
    assert relationship.type_name
    assert relationship.attributes
    assert relationship.attributes.relationship_attributes
    assert relationship.attributes.relationship_attributes.attributes
    assert (
        relationship.attributes.relationship_attributes.type_name == expected_type_name
    )
    assert relationship.attributes.relationship_attributes == udr


@pytest.mark.order(after="test_user_def_relationship_on_terms")
async def test_search_user_def_relationship_on_terms(
    client: AsyncAtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    term_user_def_relationship: UserDefRelationship,
):
    # Wait for assets to be indexed
    sleep(5)
    assert term1 and term1.guid
    assert term2 and term2.guid
    results = await (
        FluentSearch()
        .select()
        .where_some(AtlasGlossaryTerm.GUID.eq(term1.guid))
        .where_some(AtlasGlossaryTerm.GUID.eq(term2.guid))
        .include_on_results(AtlasGlossaryTerm.USER_DEF_RELATIONSHIP_TO)
        .include_on_results(AtlasGlossaryTerm.USER_DEF_RELATIONSHIP_FROM)
        .include_relationship_attributes(True)
        .aexecute(client=client)
    )
    assert results and results.count == 2
    async for asset in results:
        assert asset and asset.guid
        if asset.guid == term1.guid:
            assert (
                asset.user_def_relationship_to
                and len(asset.user_def_relationship_to) == 1
            )
            _assert_relationship(
                asset.user_def_relationship_to[0],
                UserDefRelationship.__name__,
                term_user_def_relationship,
            )
        else:
            assert (
                asset.user_def_relationship_from
                and len(asset.user_def_relationship_from) == 1
            )
            _assert_relationship(
                asset.user_def_relationship_from[0],
                UserDefRelationship.__name__,
                term_user_def_relationship,
            )
