# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm

PREFIX = "psdk-Glossary"

GLOSSARY_NAME = PREFIX + " Traversable"
TERM_NAME1 = PREFIX + " Term1"
TERM_NAME2 = PREFIX + " Term2"


class GlossaryTest:
    @staticmethod
    def create_glossary(client: AtlanClient, name: str) -> AtlasGlossary:
        glossary = AtlasGlossary.create(name=name)
        response = client.upsert(glossary)
        assert response
        assert len(response.assets_deleted(asset_type=AtlasGlossary)) == 0
        assert len(response.assets_updated(asset_type=AtlasGlossary)) == 0
        assert len(response.assets_created(asset_type=AtlasGlossary)) == 1
        one = response.assets_created(asset_type=AtlasGlossary)[0]
        assert isinstance(one, AtlasGlossary)
        g = one
        assert g.guid
        assert g.qualified_name
        assert g.name == name
        assert g.qualified_name != name
        return g

    @staticmethod
    def create_term(
        client: AtlanClient, name: str, glossary_guid: str
    ) -> AtlasGlossaryTerm:
        term = AtlasGlossaryTerm.create(name=name, glossary_guid=glossary_guid)
        response = client.upsert(term)
        assert response
        assert len(response.assets_deleted(asset_type=AtlasGlossary)) == 0
        assert len(response.assets_updated(asset_type=AtlasGlossary)) == 1
        g = response.assets_updated(asset_type=AtlasGlossary)[0]
        assert isinstance(g, AtlasGlossary)
        assert g.guid == glossary_guid
        assert len(response.assets_created(asset_type=AtlasGlossaryTerm)) == 1
        t = response.assets_created(asset_type=AtlasGlossaryTerm)[0]
        assert isinstance(t, AtlasGlossaryTerm)
        assert t.guid
        assert t.qualified_name
        assert t.name == name
        assert t.qualified_name != name
        return t


@pytest.fixture(scope="session")
def client() -> AtlanClient:
    return AtlanClient()


@pytest.fixture(scope="module")
def glossary(client: AtlanClient) -> Generator[AtlasGlossary, None, None]:
    g = GlossaryTest.create_glossary(client, GLOSSARY_NAME)
    assert g
    assert g.guid
    assert g.name == GLOSSARY_NAME
    yield g
    client.purge_entity_by_guid(g.guid)


@pytest.fixture(scope="module")
def term1(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = GlossaryTest.create_term(client, name=TERM_NAME1, glossary_guid=glossary.guid)
    assert t
    assert t.guid
    assert t.name == TERM_NAME1
    yield t
    client.purge_entity_by_guid(t.guid)


@pytest.fixture(scope="module")
def term2(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = GlossaryTest.create_term(client, name=TERM_NAME2, glossary_guid=glossary.guid)
    assert t
    assert t.guid
    assert t.name == TERM_NAME2
    yield t
    client.purge_entity_by_guid(t.guid)


@pytest.mark.usefixtures("term1", "term2")
def test_read_glossary(client: AtlanClient, glossary: AtlasGlossary):
    g = client.get_asset_by_guid(glossary.guid, asset_type=AtlasGlossary)
    assert g
    assert isinstance(g, AtlasGlossary)
    assert g.guid == glossary.guid
    assert g.qualified_name == glossary.qualified_name
    assert g.name == glossary.name
    # TODO: should we be able to flatten this to g.terms (?)
    terms = g.attributes.terms
    assert terms
    assert len(terms) == 2
