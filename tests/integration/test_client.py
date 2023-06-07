from itertools import count
from typing import Callable, Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.error import NotFoundError
from pyatlan.model.assets import (
    AtlasGlossary,
    AtlasGlossaryTerm,
    Connection,
    Database,
    Table,
)
from pyatlan.model.enums import AtlanConnectorType
from tests.integration.lineage_test import create_database, delete_asset

iter_count = count(1)


@pytest.fixture()
def database(
    client: AtlanClient, connection: Connection, make_unique: Callable[[str], str]
) -> Generator[Database, None, None]:
    """Get a database with function scope"""
    database_name = make_unique("Func" + "_db")
    db = create_database(client, connection, make_unique, database_name)
    yield db
    delete_asset(client, guid=db.guid, asset_type=Database)


def test_append_terms_with_guid(
    client: AtlanClient, term1: AtlasGlossaryTerm, database: Database
):

    assert (
        database := client.append_terms(
            guid=database.guid, asset_type=Database, terms=[term1]
        )
    )
    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term1.guid


def test_append_terms_with_qualified_name(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
):

    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name, asset_type=Database, terms=[term1]
        )
    )
    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term1.guid


def test_append_terms_using_ref_by_guid_for_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
):

    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )
    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term1.guid


def test_replace_a_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    database: Database,
):
    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )

    assert (
        database := client.replace_terms(
            guid=database.guid, asset_type=Database, terms=[term2]
        )
    )

    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert database.assigned_terms
    assert len(database.assigned_terms) == 2
    deleted_terms = [
        t for t in database.assigned_terms if t.relationship_status == "DELETED"
    ]
    assert len(deleted_terms) == 1
    assert deleted_terms[0].guid == term1.guid
    active_terms = [
        t for t in database.assigned_terms if t.relationship_status != "DELETED"
    ]
    assert len(active_terms) == 1
    assert active_terms[0].guid == term2.guid


def test_replace_all_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
):

    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )

    assert (
        database := client.replace_terms(
            guid=database.guid, asset_type=Database, terms=[]
        )
    )

    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    deleted_terms = [
        t for t in database.assigned_terms if t.relationship_status == "DELETED"
    ]
    assert len(deleted_terms) == 1
    assert deleted_terms[0].guid == term1.guid


def test_remove_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    database: Database,
):

    assert (
        database := client.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[
                AtlasGlossaryTerm.ref_by_guid(guid=term1.guid),
                AtlasGlossaryTerm.ref_by_guid(guid=term2.guid),
            ],
        )
    )

    assert (
        database := client.remove_terms(
            guid=database.guid,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(term1.guid)],
        )
    )

    database = client.get_asset_by_guid(guid=database.guid, asset_type=Database)
    assert database.assigned_terms
    assert len(database.assigned_terms) == 2
    deleted_terms = [
        t for t in database.assigned_terms if t.relationship_status == "DELETED"
    ]
    assert len(deleted_terms) == 1
    assert deleted_terms[0].guid == term1.guid
    active_terms = [
        t for t in database.assigned_terms if t.relationship_status != "DELETED"
    ]
    assert active_terms[0].guid == term2.guid


def test_find_connections_by_name(client: AtlanClient):
    connections = client.find_connections_by_name(
        name="development",
        connector_type=AtlanConnectorType.SNOWFLAKE,
        attributes=["connectorName"],
    )
    assert len(connections) == 1
    assert connections[0].connector_name == AtlanConnectorType.SNOWFLAKE.value


def test_get_asset_by_guid_good_guid(client: AtlanClient, glossary: AtlasGlossary):
    glossary = client.get_asset_by_guid(glossary.guid, AtlasGlossary)
    assert isinstance(glossary, AtlasGlossary)


def test_get_asset_by_guid_when_table_specified_and_glossary_returned_raises_not_found_error(
    client: AtlanClient, glossary: AtlasGlossary
):
    with pytest.raises(NotFoundError) as ex_info:
        guid = glossary.guid
        client.get_asset_by_guid(guid, Table)
    assert (
        f"Asset with GUID {guid} is not of the type requested: Table."
        in ex_info.value.args[0]
    )


def test_get_asset_by_guid_bad_with_non_existent_guid_raises_not_found_error(
    client: AtlanClient,
):
    with pytest.raises(
        NotFoundError, match="Given instance guid 76d54dd6 is invalid/not found"
    ):
        client.get_asset_by_guid("76d54dd6", AtlasGlossary)


def test_upsert_when_no_changes(client: AtlanClient, glossary: AtlasGlossary):
    response = client.upsert(glossary)
    assert not response.guid_assignments
    assert not response.mutated_entities


def test_get_by_qualified_name(client: AtlanClient, glossary: AtlasGlossary):
    qualified_name = glossary.qualified_name
    glossary = client.get_asset_by_qualified_name(
        qualified_name=qualified_name, asset_type=AtlasGlossary
    )
    assert glossary.attributes.qualified_name == qualified_name
