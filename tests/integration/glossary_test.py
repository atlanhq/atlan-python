# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Callable, Generator

import pytest
from pydantic import StrictStr

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm
from tests.integration.client import delete_asset

MODULE_NAME = "GLS"


def create_glossary(client: AtlanClient, name: str) -> AtlasGlossary:
    g = AtlasGlossary.create(name=StrictStr(name))
    r = client.upsert(g)
    return r.assets_created(AtlasGlossary)[0]


def create_term(
    client: AtlanClient, name: str, glossary_guid: str
) -> AtlasGlossaryTerm:
    t = AtlasGlossaryTerm.create(
        name=StrictStr(name), glossary_guid=StrictStr(glossary_guid)
    )
    r = client.upsert(t)
    return r.assets_created(AtlasGlossaryTerm)[0]


@pytest.fixture(scope="module")
def glossary(
    client: AtlanClient,
    make_unique: Callable[[str], str],
) -> Generator[AtlasGlossary, None, None]:
    glossary_name = make_unique(f"{MODULE_NAME}")
    g = create_glossary(client, glossary_name)
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


def test_glossary(
    glossary: AtlasGlossary,
    make_unique: Callable[[str], str],
):
    assert glossary.guid
    assert glossary.name == make_unique(f"{MODULE_NAME}")
    assert glossary.qualified_name
    assert glossary.qualified_name != make_unique(f"{MODULE_NAME}")


@pytest.fixture(scope="module")
def term1(
    client: AtlanClient, make_unique: Callable[[str], str], glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    term_name1 = make_unique(f"{MODULE_NAME}1")
    t = create_term(client, name=term_name1, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term1(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    term1: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term1.guid
    assert term1.name == make_unique(f"{MODULE_NAME}1")
    assert term1.qualified_name
    assert term1.qualified_name != make_unique(f"{MODULE_NAME}1")
    t = client.get_asset_by_guid(term1.guid, asset_type=AtlasGlossaryTerm)
    assert t
    assert t.guid == term1.guid
    assert t.attributes.anchor
    assert t.attributes.anchor.guid == glossary.guid


@pytest.fixture(scope="module")
def term2(
    client: AtlanClient, make_unique: Callable[[str], str], glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    term_name2 = make_unique(f"{MODULE_NAME}2")
    t = create_term(client, name=term_name2, glossary_guid=glossary.guid)
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def test_term2(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    term2: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
):
    assert term2.guid
    assert term2.name == make_unique(f"{MODULE_NAME}2")
    assert term2.qualified_name
    assert term2.qualified_name != make_unique(f"{MODULE_NAME}2")
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
