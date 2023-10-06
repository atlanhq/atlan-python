from dataclasses import dataclass
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import NotFoundError
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryTerm,
    Connection,
    Database,
    Table,
)
from pyatlan.model.audit import AuditSearchRequest
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    WorkflowPackage,
)
from pyatlan.model.user import UserMinimalResponse
from tests.integration.client import TestId
from tests.integration.lineage_test import create_database, delete_asset

CLASSIFICATION_NAME = "Issue"


@dataclass()
class AuditInfo:
    qualified_name: str = ""
    type_name: str = ""
    guid: str = ""


@pytest.fixture(scope="module")
def audit_info():
    return AuditInfo()


@pytest.fixture()
def announcement():
    return Announcement(
        announcement_title="Important Announcement",
        announcement_message="Very important info",
        announcement_type=AnnouncementType.ISSUE,
    )


@pytest.fixture()
def database(
    client: AtlanClient, connection: Connection
) -> Generator[Database, None, None]:
    """Get a database with function scope"""
    database_name = TestId.make_unique("my_db")
    db = create_database(client, connection, database_name)
    yield db
    delete_asset(client, guid=db.guid, asset_type=Database)


@pytest.fixture()
def current_user(client: AtlanClient) -> UserMinimalResponse:
    return client.get_current_user()


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
    guid = glossary.guid
    with pytest.raises(
        NotFoundError,
        match=f"ATLAN-PYTHON-404-002 Asset with GUID {guid} is not of the type requested: Table.",
    ):
        client.get_asset_by_guid(guid, Table)


def test_get_asset_by_guid_bad_with_non_existent_guid_raises_not_found_error(
    client: AtlanClient,
):
    with pytest.raises(
        NotFoundError,
        match="ATLAN-PYTHON-404-000 Server responded with ATLAS-404-00-005: Given instance guid 76d54dd6 "
        "is invalid/not found",
    ):
        client.get_asset_by_guid("76d54dd6", AtlasGlossary)


def test_upsert_when_no_changes(client: AtlanClient, glossary: AtlasGlossary):
    response = client.save(glossary)
    assert not response.guid_assignments
    assert not response.mutated_entities


def test_get_by_qualified_name(client: AtlanClient, glossary: AtlasGlossary):
    qualified_name = glossary.qualified_name or ""
    glossary = client.get_asset_by_qualified_name(
        qualified_name=qualified_name, asset_type=AtlasGlossary
    )
    assert glossary.attributes.qualified_name == qualified_name


def test_get_by_qualified_name_when_superclass_specified_raises_not_found_error(
    client: AtlanClient, glossary: AtlasGlossary
):
    qualified_name = glossary.qualified_name or ""
    with pytest.raises(
        NotFoundError,
        match="ATLAN-PYTHON-404-014 The Asset asset could not be found by name: ",
    ):
        client.get_asset_by_qualified_name(
            qualified_name=qualified_name, asset_type=Asset
        )


def test_add_classification(client: AtlanClient, term1: AtlasGlossaryTerm):
    assert term1.qualified_name
    client.add_atlan_tags(
        AtlasGlossaryTerm, term1.qualified_name, [CLASSIFICATION_NAME]
    )
    glossary_term = client.get_asset_by_guid(term1.guid, asset_type=AtlasGlossaryTerm)
    assert glossary_term.atlan_tags
    assert len(glossary_term.atlan_tags) == 1
    classification = glossary_term.atlan_tags[0]
    assert str(classification.type_name) == CLASSIFICATION_NAME


@pytest.mark.order(after="test_add_classification")
def test_remove_classification(client: AtlanClient, term1: AtlasGlossaryTerm):
    assert term1.qualified_name
    client.remove_atlan_tag(
        AtlasGlossaryTerm, term1.qualified_name, CLASSIFICATION_NAME
    )
    glossary_term = client.get_asset_by_guid(term1.guid, asset_type=AtlasGlossaryTerm)
    assert not glossary_term.atlan_tags


def test_update_certificate(client: AtlanClient, glossary: AtlasGlossary):
    assert glossary.qualified_name
    assert glossary.name
    message = "An important message"
    client.update_certificate(
        asset_type=AtlasGlossary,
        qualified_name=glossary.qualified_name,
        name=glossary.name,
        certificate_status=CertificateStatus.DRAFT,
        message=message,
    )
    glossary = client.get_asset_by_guid(guid=glossary.guid, asset_type=AtlasGlossary)
    assert glossary.certificate_status == CertificateStatus.DRAFT
    assert glossary.certificate_status_message == message


@pytest.mark.order(after="test_update_certificate")
def test_remove_certificate(client: AtlanClient, glossary: AtlasGlossary):
    assert glossary.qualified_name
    assert glossary.name
    client.remove_certificate(
        asset_type=AtlasGlossary,
        qualified_name=glossary.qualified_name,
        name=glossary.name,
    )
    glossary = client.get_asset_by_guid(guid=glossary.guid, asset_type=AtlasGlossary)
    assert glossary.certificate_status is None
    assert glossary.certificate_status_message is None


def test_update_announcement(
    client: AtlanClient, glossary: AtlasGlossary, announcement: Announcement
):
    assert glossary.qualified_name
    assert glossary.name
    client.update_announcement(
        asset_type=AtlasGlossary,
        qualified_name=glossary.qualified_name,
        name=glossary.name,
        announcement=announcement,
    )
    glossary = client.get_asset_by_guid(guid=glossary.guid, asset_type=AtlasGlossary)
    assert glossary.get_announcment() == announcement


@pytest.mark.order(after="test_update_certificate")
def test_remove_announcement(client: AtlanClient, glossary: AtlasGlossary):
    assert glossary.qualified_name
    assert glossary.name
    client.remove_announcement(
        asset_type=AtlasGlossary,
        qualified_name=glossary.qualified_name,
        name=glossary.name,
    )
    glossary = client.get_asset_by_guid(guid=glossary.guid, asset_type=AtlasGlossary)
    assert glossary.get_announcment() is None


def test_workflow_find_by_type(client: AtlanClient):
    results = client.workflow.find_by_type(
        prefix=WorkflowPackage.FIVETRAN, max_results=10
    )
    assert results
    assert len(results) == 1


def test_audit_find_by_user(
    client: AtlanClient, current_user: UserMinimalResponse, audit_info: AuditInfo
):
    size = 10
    assert current_user.username

    results = client.audit.search(
        AuditSearchRequest.by_user(current_user.username, size=size)
    )
    assert results.total_count > 0
    assert size == len(results.current_page())
    audit_entity = results.current_page()[0]
    audit_info.qualified_name = audit_entity.entity_qualified_name
    audit_info.guid = audit_entity.entity_id
    audit_info.type_name = audit_entity.type_name


@pytest.mark.order(after="test_audit_find_by_user")
def test_audit_find_by_qualified_name(client: AtlanClient, audit_info: AuditInfo):
    assert audit_info.qualified_name
    assert audit_info.type_name
    size = 10

    results = client.audit.search(
        AuditSearchRequest.by_qualified_name(
            qualified_name=audit_info.qualified_name,
            type_name=audit_info.type_name,
            size=size,
        )
    )

    assert results.total_count > 0
    count = len(results.current_page())
    assert count > 0 and count <= size


@pytest.mark.order(after="test_audit_find_by_user")
def test_audit_find_by_guid(client: AtlanClient, audit_info: AuditInfo):
    assert audit_info.guid
    size = 10

    results = client.audit.search(
        AuditSearchRequest.by_guid(
            guid=audit_info.guid,
            size=size,
        )
    )

    assert results.total_count > 0
    count = len(results.current_page())
    assert count > 0 and count <= size
