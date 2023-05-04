from itertools import count
from typing import Callable, Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm, Connection, Database

iter_count = count(1)


@pytest.fixture(scope="module")
def client() -> AtlanClient:
    return AtlanClient()


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Connection:
    return client.get_asset_by_guid("b3a5c49a-0c7c-4e66-8453-f4da8d9ce222", Connection)


@pytest.fixture(scope="module")
def glossary(client: AtlanClient) -> Generator[AtlasGlossary, None, None]:
    glossary = AtlasGlossary.create(name="Integration Test Glossary")
    glossary = client.upsert(glossary).assets_created(asset_type=AtlasGlossary)[0]
    yield glossary
    client.purge_entity_by_guid(guid=glossary.guid)


@pytest.fixture()
def database(
    client: AtlanClient, connection: Connection
) -> Generator[Database, None, None]:

    database = Database.create(
        name=f"Integration_Test_Entity_DB{next(iter_count)}",
        connection_qualified_name=connection.attributes.qualified_name,
    )
    database = client.upsert(database).assets_created(Database)[0]

    yield database

    client.purge_entity_by_guid(guid=database.guid)


@pytest.fixture()
def make_term(
    client: AtlanClient, glossary
) -> Generator[Callable[[str], AtlasGlossaryTerm], None, None]:
    created_term_guids = []

    def _make_term(name: str) -> AtlasGlossaryTerm:
        term = AtlasGlossaryTerm.create(
            name=f"Integration Test Glossary Term {name}", anchor=glossary
        )
        term = client.upsert(term).assets_created(AtlasGlossaryTerm)[0]
        created_term_guids.append(term.guid)
        return term

    yield _make_term

    for guid in created_term_guids:
        client.purge_entity_by_guid(guid=guid)


def test_register_client_with_bad_parameter_raises_valueerror():
    with pytest.raises(ValueError, match="client must be an instance of AtlanClient"):
        AtlanClient.register_client("")
    assert AtlanClient.get_default_client() is None


def test_register_client():
    client = AtlanClient(base_url="http://mark.atlan.com", api_key="123")
    AtlanClient.register_client(client)
    assert AtlanClient.get_default_client() == client


def test_append_terms_with_guid(
    client: AtlanClient,
    make_term: Callable[[str], AtlasGlossaryTerm],
    database: Database,
):
    term = make_term("Term1")

    assert (
        database := client.append_terms(
            guid=database.guid, asset_type=Database, terms=[term]
        )
    )
    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert len(database.terms) == 1
    assert database.terms[0].guid == term.guid


def test_append_terms_with_qualified_name(
    client: AtlanClient,
    make_term: Callable[[str], AtlasGlossaryTerm],
    database: Database,
):
    term = make_term("Term1")

    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name, asset_type=Database, terms=[term]
        )
    )
    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert len(database.terms) == 1
    assert database.terms[0].guid == term.guid


def test_append_terms_using_ref_by_guid_for_term(
    client: AtlanClient,
    make_term: Callable[[str], AtlasGlossaryTerm],
    database: Database,
):
    term = make_term("Term1")

    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term.guid)],
        )
    )
    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert len(database.terms) == 1
    assert database.terms[0].guid == term.guid


def test_replace_a_term(
    client: AtlanClient,
    make_term: Callable[[str], AtlasGlossaryTerm],
    database: Database,
):
    original_term = make_term("Term1")
    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=original_term.guid)],
        )
    )

    replacemant_term = make_term("Term2")
    assert (
        database := client.replace_terms(
            guid=database.guid, asset_type=Database, terms=[replacemant_term]
        )
    )

    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert len(database.terms) == 2
    deleted_terms = [t for t in database.terms if t.relationship_status == "DELETED"]
    assert len(deleted_terms) == 1
    assert deleted_terms[0].guid == original_term.guid
    active_terms = [t for t in database.terms if t.relationship_status != "DELETED"]
    assert len(active_terms) == 1
    assert active_terms[0].guid == replacemant_term.guid


def test_replace_all_term(
    client: AtlanClient,
    make_term: Callable[[str], AtlasGlossaryTerm],
    database: Database,
):
    original_term = make_term("Term1")
    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=original_term.guid)],
        )
    )

    assert (
        database := client.replace_terms(
            guid=database.guid, asset_type=Database, terms=[]
        )
    )

    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert len(database.terms) == 1
    deleted_terms = [t for t in database.terms if t.relationship_status == "DELETED"]
    assert len(deleted_terms) == 1
    assert deleted_terms[0].guid == original_term.guid


def test_remove_term(
    client: AtlanClient,
    make_term: Callable[[str], AtlasGlossaryTerm],
    database: Database,
):
    original_term = make_term("Term1")
    another_term = make_term("Term2")
    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[
                AtlasGlossaryTerm.ref_by_guid(guid=original_term.guid),
                AtlasGlossaryTerm.ref_by_guid(guid=another_term.guid),
            ],
        )
    )

    assert (
        database := client.remove_terms(
            guid=database.guid,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(original_term.guid)],
        )
    )

    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert len(database.terms) == 2
    deleted_terms = [t for t in database.terms if t.relationship_status == "DELETED"]
    assert len(deleted_terms) == 1
    assert deleted_terms[0].guid == original_term.guid
    active_terms = [t for t in database.terms if t.relationship_status != "DELETED"]
    assert active_terms[0].guid == another_term.guid
