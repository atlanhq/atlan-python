# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import itertools
import logging
from time import sleep
from typing import Generator, List, Optional, Union

import pytest
from pydantic.v1 import StrictStr
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import InvalidRequestError, NotFoundError
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory, AtlasGlossaryTerm
from pyatlan.model.enums import SaveSemantic
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.search import DSL, IndexSearchRequest
from tests.integration.client import TestId, delete_asset

LOGGER = logging.getLogger(__name__)

MODULE_NAME = TestId.make_unique("GLS")

TERM_NAME1 = f"{MODULE_NAME}1"
TERM_NAME2 = f"{MODULE_NAME}2"
TERM_NAME3 = f"{MODULE_NAME}3"
TERM_NAME4 = f"{MODULE_NAME}4"


def create_glossary(client: AtlanClient, name: str) -> AtlasGlossary:
    g = AtlasGlossary.create(name=StrictStr(name))
    r = client.asset.save(g)
    return r.assets_created(AtlasGlossary)[0]


def create_category(
    client: AtlanClient,
    name: str,
    glossary: AtlasGlossary,
    parent: Optional[AtlasGlossaryCategory] = None,
) -> AtlasGlossaryCategory:
    c = AtlasGlossaryCategory.create(
        name=name, anchor=glossary, parent_category=parent or None
    )
    return client.asset.save(c).assets_created(AtlasGlossaryCategory)[0]


def create_term(
    client: AtlanClient,
    name: str,
    glossary_guid: str,
    categories: Optional[List[AtlasGlossaryCategory]] = None,
) -> AtlasGlossaryTerm:
    t = AtlasGlossaryTerm.create(
        name=StrictStr(name),
        glossary_guid=StrictStr(glossary_guid),
        categories=categories,
    )
    r = client.asset.save(t)
    return r.assets_created(AtlasGlossaryTerm)[0]


@pytest.fixture(scope="module")
def glossary(
    client: AtlanClient,
) -> Generator[AtlasGlossary, None, None]:
    g = create_glossary(client, MODULE_NAME)
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


def test_glossary(
    glossary: AtlasGlossary,
):
    assert glossary.guid
    assert glossary.name == MODULE_NAME
    assert glossary.qualified_name
    assert glossary.qualified_name != MODULE_NAME


@pytest.fixture(scope="module")
def category(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(client, MODULE_NAME, glossary)
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def hierarchy_glossary(
    client: AtlanClient,
) -> Generator[AtlasGlossary, None, None]:
    g = create_glossary(client, TestId.make_unique("hierarchy"))
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


@pytest.fixture(scope="module")
def top1_category(
    client: AtlanClient, hierarchy_glossary
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(client, TestId.make_unique("top1"), hierarchy_glossary)
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def mid1a_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("mid1a"), hierarchy_glossary, parent=top1_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def mid1a_term(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1a_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryTerm, None, None]:
    assert mid1a_category.qualified_name
    t = create_term(
        client,
        name=f"mid1a_{TERM_NAME1}",
        glossary_guid=hierarchy_glossary.guid,
        categories=[
            AtlasGlossaryCategory.ref_by_qualified_name(mid1a_category.qualified_name)
        ],
    )
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


@pytest.fixture(scope="module")
def leaf1aa_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1a_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("leaf1aa"), hierarchy_glossary, parent=mid1a_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def leaf1ab_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1a_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("leaf1ab"), hierarchy_glossary, parent=mid1a_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def mid1b_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("mid1b"), hierarchy_glossary, parent=top1_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def leaf1ba_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid1b_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("leaf1ba"), hierarchy_glossary, parent=mid1b_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def top2_category(
    client: AtlanClient, hierarchy_glossary: AtlasGlossary
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(client, TestId.make_unique("top2"), hierarchy_glossary)
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def mid2a_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top2_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("mid2a"), hierarchy_glossary, parent=top2_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def leaf2aa_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid2a_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("leaf2aa"), hierarchy_glossary, parent=mid2a_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def leaf2ab_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid2a_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("leaf2ab"), hierarchy_glossary, parent=mid2a_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def mid2b_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top2_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("mid2b"), hierarchy_glossary, parent=top2_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


@pytest.fixture(scope="module")
def leaf2ba_category(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    mid2b_category: AtlasGlossaryCategory,
) -> Generator[AtlasGlossaryCategory, None, None]:
    c = create_category(
        client, TestId.make_unique("leaf2ba"), hierarchy_glossary, parent=mid2b_category
    )
    yield c
    delete_asset(client, guid=c.guid, asset_type=AtlasGlossaryCategory)


def test_category(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    assert category.guid
    assert category.name == MODULE_NAME
    assert category.qualified_name
    c = client.asset.get_by_guid(category.guid, AtlasGlossaryCategory)
    assert c
    assert c.guid == category.guid
    assert c.anchor
    assert c.anchor.guid == glossary.guid


@pytest.fixture(scope="module")
def term1(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = create_term(client, name=TERM_NAME1, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term_failure(
    client: AtlanClient,
    glossary: AtlasGlossary,
):
    with pytest.raises(
        NotFoundError,
        match="ATLAN-PYTHON-404-000 Server responded with ATLAS-404-00-009: Instance AtlasGlossaryTerm with "
        "unique attribute *",
    ):
        client.asset.update_merging_cm(
            AtlasGlossaryTerm.create(
                name=f"{TERM_NAME1} X", glossary_guid=glossary.guid
            )
        )


def test_term1(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1.guid
    assert term1.name == TERM_NAME1
    assert term1.qualified_name
    assert term1.qualified_name != TERM_NAME1
    t = client.asset.get_by_guid(term1.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term1.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest.fixture(scope="module")
def term2(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = create_term(client, name=TERM_NAME2, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term2(
    client: AtlanClient,
    term2: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term2.guid
    assert term2.name == TERM_NAME2
    assert term2.qualified_name
    assert term2.qualified_name != TERM_NAME2
    t = client.asset.get_by_guid(term2.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term2.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest.fixture(scope="module")
def term3(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = create_term(client, name=TERM_NAME3, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term3(
    client: AtlanClient,
    term3: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term3.guid
    assert term3.name == TERM_NAME3
    assert term3.qualified_name
    assert term3.qualified_name != TERM_NAME3
    t = client.asset.get_by_guid(term3.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term3.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest.fixture(scope="module")
def term4(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = create_term(client, name=TERM_NAME4, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term4(
    client: AtlanClient,
    term4: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term4.guid
    assert term4.name == TERM_NAME4
    assert term4.qualified_name
    assert term4.qualified_name != TERM_NAME4
    t = client.asset.get_by_guid(term4.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term4.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


def test_read_glossary(
    client: AtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    term3: AtlasGlossaryTerm,
    term4: AtlasGlossaryTerm,
):
    g = client.asset.get_by_guid(glossary.guid, asset_type=AtlasGlossary)
    assert g
    assert isinstance(g, AtlasGlossary)
    assert g.guid == glossary.guid
    assert g.qualified_name == glossary.qualified_name
    assert g.name == glossary.name
    terms = g.terms
    assert terms
    assert len(terms) == 4


def test_compound_queries(
    client: AtlanClient,
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
    response = client.asset.search(request)
    assert response
    assert response.count == 4
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
    response = client.asset.search(request)
    assert response
    assert response.count == 3


def test_fluent_search(
    client: AtlanClient,
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

    assert terms.count(client) == 4

    guids_chained = []
    g_sorted = []
    for asset in filter(
        lambda x: isinstance(x, AtlasGlossaryTerm),
        itertools.islice(terms.execute(client), 4),
    ):
        guids_chained.append(asset.guid)
        g_sorted.append(asset.guid)
    g_sorted.sort()
    assert guids_chained == g_sorted

    results = FluentSearch(
        _page_size=5,
        wheres=[
            CompoundQuery.active_assets(),
            CompoundQuery.asset_type(AtlasGlossaryTerm),
            AtlasGlossaryTerm.NAME.startswith(MODULE_NAME),
            AtlasGlossaryTerm.ANCHOR.startswith(glossary.qualified_name),
        ],
        _includes_on_results=[AtlasGlossaryTerm.ANCHOR.atlan_field_name],
        _includes_on_relations=[AtlasGlossary.NAME.atlan_field_name],
    ).execute(client)

    guids_alt = []
    g_sorted = []
    for asset in results:
        guids_alt.append(asset.guid)
        g_sorted.append(asset.guid)
    g_sorted.sort()
    assert g_sorted == guids_alt
    assert glossary.qualified_name

    results = FluentSearch(
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
    ).execute(client)

    names = []
    names_sorted = []
    for asset in results:
        names.append(asset.name)
        names_sorted.append(asset.name)
    names_sorted.sort()
    assert names_sorted == names


@pytest.mark.order(after="test_read_glossary")
def test_trim_to_required_glossary(
    client: AtlanClient,
    glossary: AtlasGlossary,
):
    glossary = glossary.trim_to_required()
    response = client.asset.save(glossary)
    assert response.mutated_entities is None


@pytest.mark.order(after="test_term1")
def test_term_trim_to_required(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
):
    term1 = client.asset.get_by_guid(guid=term1.guid, asset_type=AtlasGlossaryTerm)
    term1 = term1.trim_to_required()
    response = client.asset.save(term1)
    assert response.mutated_entities is None


def test_find_glossary_by_name(client: AtlanClient, glossary: AtlasGlossary):
    assert glossary.guid == client.asset.find_glossary_by_name(name=glossary.name).guid


def test_find_category_fast_by_name(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    @retry(
        wait=wait_fixed(2),
        retry=retry_if_exception_type(NotFoundError),
        stop=stop_after_attempt(3),
    )
    def check_it():
        assert (
            category.guid
            == client.asset.find_category_fast_by_name(
                name=category.name, glossary_qualified_name=glossary.qualified_name
            )[0].guid
        )

    check_it()


def test_find_category_by_name(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    assert (
        category.guid
        == client.asset.find_category_by_name(
            name=category.name, glossary_name=glossary.name
        )[0].guid
    )


def test_find_category_by_name_qn_guid_correctly_populated(
    client: AtlanClient,
    hierarchy_glossary: AtlasGlossary,
    top1_category: AtlasGlossaryCategory,
    top2_category: AtlasGlossaryCategory,
    mid1a_category: AtlasGlossaryCategory,
    mid1a_term: AtlasGlossaryTerm,
    mid2a_category: AtlasGlossaryCategory,
):
    category = client.asset.find_category_by_name(
        name=mid1a_category.name,
        glossary_name=hierarchy_glossary.name,
        attributes=["terms", "anchor", "parentCategory"],
    )[0]

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


def test_category_delete_by_guid_raises_error_invalid_request_error(
    client: AtlanClient, category: AtlasGlossaryCategory
):
    with pytest.raises(
        InvalidRequestError,
        match=f"ATLAN-PYTHON-400-052 Asset with guid: {category.guid} is an asset "
        "of type AtlasGlossaryCategory which does not support archiving. "
        "Suggestion: Please use purge if you wish to remove assets of this type.",
    ):
        client.asset.delete_by_guid(guid=category.guid)


def test_find_term_fast_by_name(
    client: AtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    @retry(
        wait=wait_fixed(2),
        retry=retry_if_exception_type(NotFoundError),
        stop=stop_after_attempt(3),
    )
    def check_it():
        assert (
            term1.guid
            == client.asset.find_term_fast_by_name(
                name=term1.name, glossary_qualified_name=glossary.qualified_name
            ).guid
        )

    check_it()


def test_find_term_by_name(
    client: AtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    assert (
        term1.guid
        == client.asset.find_term_by_name(
            name=term1.name, glossary_name=glossary.name
        ).guid
    )


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
def test_hierarchy(
    client: AtlanClient,
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
    hierarchy = client.asset.get_hierarchy(
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


def test_create_relationship(
    client: AtlanClient,
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
    response = client.asset.save(term)

    assert response
    result = client.asset.get_by_guid(guid=term1.guid, asset_type=AtlasGlossaryTerm)
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
def test_remove_relationship(
    client: AtlanClient,
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
    response = client.asset.save(term)

    assert response
    result = client.asset.get_by_guid(guid=term1.guid, asset_type=AtlasGlossaryTerm)
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
def test_append_relationship(
    client: AtlanClient,
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
    response = client.asset.save(term)

    assert response
    result = client.asset.get_by_guid(guid=term1.guid, asset_type=AtlasGlossaryTerm)
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
def test_append_relationship_again(
    client: AtlanClient,
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
    response = client.asset.save(term)

    assert response
    result = client.asset.get_by_guid(guid=term1.guid, asset_type=AtlasGlossaryTerm)
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
def test_remove_unrelated_relationship(
    client: AtlanClient,
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
        client.asset.save(term)

    EXPECTED_ERR = (
        "ATLAN-PYTHON-404-000 Server responded with ATLAS-409-00-0021: "
        "relationship AtlasGlossaryRelatedTerm does "
        f"not exist between entities {term2.guid} and {term1.guid}. "
        "Suggestion: Check the details of the server's message to correct your request."
    )
    assert EXPECTED_ERR == str(err.value)


def test_move_sub_category_to_category(
    client: AtlanClient,
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

    hierarchy = client.asset.get_hierarchy(glossary=hierarchy_glossary)
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
    response = client.asset.save(mid1a_category)

    if updated := response.assets_updated(asset_type=AtlasGlossaryCategory):
        assert updated[0].name == mid1a_category.name
        assert updated[0].qualified_name == mid1a_category.qualified_name
    else:
        pytest.fail(f"Failed to perform update on category: {mid1a_category.name}")

    # Ensure that the sub-category 'mid1a_category'
    # has been successfully moved to the root category
    sleep(10)
    hierarchy = client.asset.get_hierarchy(glossary=hierarchy_glossary)
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
