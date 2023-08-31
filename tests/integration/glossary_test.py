# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import itertools
import logging
from typing import Generator

import pytest
from pydantic import StrictStr
from retry import retry

from pyatlan.client.atlan import AtlanClient
from pyatlan.error import NotFoundError
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory, AtlasGlossaryTerm
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.search import DSL, IndexSearchRequest
from tests.integration.client import TestId, delete_asset

LOGGER = logging.getLogger(__name__)

MODULE_NAME = TestId.make_unique("GLS")

TERM_NAME1 = f"{MODULE_NAME}1"
TERM_NAME2 = f"{MODULE_NAME}2"


def create_glossary(client: AtlanClient, name: str) -> AtlasGlossary:
    g = AtlasGlossary.create(name=StrictStr(name))
    r = client.save(g)
    return r.assets_created(AtlasGlossary)[0]


def create_category(
    client: AtlanClient, name: str, glossary: AtlasGlossary
) -> AtlasGlossaryCategory:
    c = AtlasGlossaryCategory.create(name=name, anchor=glossary)
    return client.save(c).assets_created(AtlasGlossaryCategory)[0]


def create_term(
    client: AtlanClient, name: str, glossary_guid: str
) -> AtlasGlossaryTerm:
    t = AtlasGlossaryTerm.create(
        name=StrictStr(name), glossary_guid=StrictStr(glossary_guid)
    )
    r = client.save(t)
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


def test_category(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    assert category.guid
    assert category.name == MODULE_NAME
    assert category.qualified_name
    c = client.get_asset_by_guid(category.guid, AtlasGlossaryCategory)
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
        match="Instance AtlasGlossaryTerm with unique attribute .* does not exist",
    ):
        client.update_merging_cm(
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
    t = client.get_asset_by_guid(term1.guid, asset_type=AtlasGlossaryTerm)
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
    t = client.get_asset_by_guid(term2.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term2.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


def test_read_glossary(
    client: AtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
):
    g = client.get_asset_by_guid(glossary.guid, asset_type=AtlasGlossary)
    assert g
    assert isinstance(g, AtlasGlossary)
    assert g.guid == glossary.guid
    assert g.qualified_name == glossary.qualified_name
    assert g.name == glossary.name
    terms = g.terms
    assert terms
    assert len(terms) == 2


def test_compound_queries(
    client: AtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
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
    response = client.search(request)
    assert response
    assert response.count == 2
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
    response = client.search(request)
    assert response
    assert response.count == 1


def test_fluent_search(
    client: AtlanClient,
    glossary: AtlasGlossary,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
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

    assert terms.count(client) == 2

    guids_chained = []
    g_sorted = []
    for asset in filter(
        lambda x: isinstance(x, AtlasGlossaryTerm),
        itertools.islice(terms.execute(client), 2),
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
    response = client.save(glossary)
    assert response.mutated_entities is None


@pytest.mark.order(after="test_term1")
def test_term_trim_to_required(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
):
    term1 = client.get_asset_by_guid(guid=term1.guid, asset_type=AtlasGlossaryTerm)
    term1 = term1.trim_to_required()
    response = client.save(term1)
    assert response.mutated_entities is None


def test_find_glossary_by_name(client: AtlanClient, glossary: AtlasGlossary):
    assert glossary.guid == client.find_glossary_by_name(name=glossary.name).guid


def test_find_category_fast_by_name(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    @retry(NotFoundError, tries=3, delay=2, logger=LOGGER)
    def check_it():
        assert (
            category.guid
            == client.find_category_fast_by_name(
                name=category.name, glossary_qualified_name=glossary.qualified_name
            )[0].guid
        )

    check_it()


def test_find_category_by_name(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    assert (
        category.guid
        == client.find_category_by_name(
            name=category.name, glossary_name=glossary.name
        )[0].guid
    )


def test_find_term_fast_by_name(
    client: AtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    @retry(NotFoundError, tries=3, delay=2, logger=LOGGER)
    def check_it():
        assert (
            term1.guid
            == client.find_term_fast_by_name(
                name=term1.name, glossary_qualified_name=glossary.qualified_name
            ).guid
        )

    check_it()


def test_find_term_by_name(
    client: AtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    assert (
        term1.guid
        == client.find_term_by_name(name=term1.name, glossary_name=glossary.name).guid
    )
