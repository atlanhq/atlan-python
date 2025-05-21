import time
from dataclasses import dataclass
from typing import Generator, List, Optional, Type
from unittest.mock import patch

import pytest
from pydantic.v1 import StrictStr

from pyatlan.client.atlan import DEFAULT_RETRY, AtlanClient
from pyatlan.client.audit import LOGGER as AUDIT_LOGGER
from pyatlan.client.search_log import LOGGER as SEARCH_LOG_LOGGER
from pyatlan.client.search_log import (
    AssetViews,
    SearchLogRequest,
    SearchLogResults,
    SearchLogViewResults,
)
from pyatlan.errors import AuthenticationError, InvalidRequestError, NotFoundError
from pyatlan.model.api_tokens import ApiToken
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    Schema,
    Table,
)
from pyatlan.model.audit import AuditSearchRequest, AuditSearchResults
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    SortOrder,
    UTMTags,
)
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, SortItem, Term
from pyatlan.model.user import UserMinimalResponse
from tests.integration.client import TestId
from tests.integration.lineage_test import create_database, delete_asset
from tests.integration.requests_test import delete_token

CLASSIFICATION_NAME = "Issue"
SL_SORT_BY_TIMESTAMP = SortItem(field="timestamp", order=SortOrder.ASCENDING)
SL_SORT_BY_GUID = SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING)
SL_SORT_BY_QUALIFIED_NAME = SortItem(
    field="entityQFNamesAll", order=SortOrder.ASCENDING
)
AUDIT_SORT_BY_GUID = SortItem(field="entityId", order=SortOrder.ASCENDING)
AUDIT_SORT_BY_LATEST = SortItem("created", order=SortOrder.DESCENDING)
MODULE_NAME = TestId.make_unique("Client")
TEST_USER_DESCRIPTION = "Automated testing of the Python SDK. (USER)"
TEST_SYSTEM_DESCRIPTION = "Automated testing of the Python SDK. (SYSTEM)"
call_count = 0


@pytest.fixture(scope="module")
def expired_token(client: AtlanClient) -> Generator[ApiToken, None, None]:
    token = None
    try:
        token = client.token.create(f"{MODULE_NAME}-expired", validity_seconds=1)
        time.sleep(5)
        yield token
    finally:
        delete_token(client, token)


@pytest.fixture(scope="module")
def argo_fake_token(client: AtlanClient) -> Generator[ApiToken, None, None]:
    token = None
    try:
        token = client.token.create(f"{MODULE_NAME}-fake-argo")
        yield token
    finally:
        delete_token(client, token)


@pytest.fixture(scope="module")
def glossary(
    client: AtlanClient,
) -> Generator[AtlasGlossary, None, None]:
    g = AtlasGlossary.creator(name=StrictStr(MODULE_NAME))
    g.description = TEST_SYSTEM_DESCRIPTION
    g.user_description = TEST_USER_DESCRIPTION
    response = client.asset.save(g)
    result = response.assets_created(AtlasGlossary)[0]
    assert result
    yield result
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


@pytest.fixture(scope="module")
def term(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = AtlasGlossaryTerm.creator(
        name=StrictStr(MODULE_NAME),
        glossary_guid=StrictStr(glossary.guid),
    )
    t.description = f"{TEST_SYSTEM_DESCRIPTION} Term"
    t.user_description = f"{TEST_USER_DESCRIPTION} Term"
    response = client.asset.save(t)
    result = response.assets_created(AtlasGlossaryTerm)[0]
    assert result
    yield result
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


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
def schema_with_db_qn(
    client: AtlanClient,
    database: Database,
) -> Generator[Schema, None, None]:
    assert database.qualified_name
    schema_name = TestId.make_unique("my_schema")
    to_create = Schema.create(
        name=schema_name, database_qualified_name=database.qualified_name
    )
    to_create.qualified_name = database.qualified_name
    result = client.asset.save(to_create)
    sch = result.assets_created(asset_type=Schema)[0]
    yield sch
    delete_asset(client, guid=sch.guid, asset_type=Schema)


@pytest.fixture()
def current_user(client: AtlanClient) -> UserMinimalResponse:
    return client.user.get_current()


def create_glossary(client: AtlanClient, name: str) -> AtlasGlossary:
    g = AtlasGlossary.create(name=StrictStr(name))
    r = client.asset.save(g)
    return r.assets_created(AtlasGlossary)[0]


@pytest.fixture(scope="module")
def audit_glossary(client: AtlanClient) -> Generator[AtlasGlossary, None, None]:
    created_glossary = create_glossary(
        client, TestId.make_unique("test-audit-glossary")
    )
    yield created_glossary
    delete_asset(client, guid=created_glossary.guid, asset_type=AtlasGlossary)


@pytest.fixture(scope="module")
def sl_glossary(
    client: AtlanClient,
) -> Generator[AtlasGlossary, None, None]:
    g = create_glossary(client, TestId.make_unique("test-sl-glossary"))
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


def _test_update_certificate(
    client: AtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    glossary_guid: Optional[str] = None,
):
    assert test_asset.qualified_name
    assert test_asset.name
    test_asset = client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.qualified_name
    assert test_asset.name
    assert test_asset.certificate_status is None
    assert test_asset.certificate_status_message is None
    message = "An important message"
    client.asset.update_certificate(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        certificate_status=CertificateStatus.DRAFT,
        message=message,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.certificate_status == CertificateStatus.DRAFT
    assert test_asset.certificate_status_message == message


def _test_remove_certificate(
    client: AtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    glossary_guid: Optional[str] = None,
):
    assert test_asset.qualified_name
    assert test_asset.name
    client.asset.remove_certificate(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.certificate_status is None
    assert test_asset.certificate_status_message is None


def _test_update_announcement(
    client: AtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    test_announcement: Announcement,
    glossary_guid: Optional[str] = None,
):
    assert test_asset.qualified_name
    assert test_asset.name
    client.asset.update_announcement(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        announcement=test_announcement,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.get_announcment() == test_announcement


def _test_remove_announcement(
    client: AtlanClient,
    test_asset: Asset,
    test_asset_type: Type[Asset],
    glossary_guid: Optional[str] = None,
):
    assert test_asset.qualified_name
    assert test_asset.name
    client.asset.remove_announcement(
        asset_type=test_asset_type,
        qualified_name=test_asset.qualified_name,
        name=test_asset.name,
        glossary_guid=glossary_guid if glossary_guid else None,
    )
    test_asset = client.asset.get_by_guid(
        guid=test_asset.guid, asset_type=test_asset_type, ignore_relationships=False
    )
    assert test_asset.get_announcment() is None


def test_append_terms_with_guid(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
):
    time.sleep(5)
    assert (
        database := client.asset.append_terms(
            guid=database.guid, asset_type=Database, terms=[term1]
        )
    )
    database = client.asset.get_by_guid(
        guid=database.guid, asset_type=Database, ignore_relationships=False
    )
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term1.guid


def test_append_terms_with_qualified_name(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
):
    time.sleep(5)
    assert (
        database := client.asset.append_terms(
            qualified_name=database.qualified_name, asset_type=Database, terms=[term1]
        )
    )
    database = client.asset.get_by_guid(
        guid=database.guid, asset_type=Database, ignore_relationships=False
    )
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term1.guid


def test_append_terms_using_ref_by_guid_for_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
):
    time.sleep(5)
    assert (
        database := client.asset.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )
    database = client.asset.get_by_guid(
        guid=database.guid, asset_type=Database, ignore_relationships=False
    )
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term1.guid


def test_append_terms_with_same_qn(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
    schema_with_db_qn: Schema,
):
    time.sleep(5)
    assert schema_with_db_qn.qualified_name == database.qualified_name
    assert (
        database := client.asset.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )
    assert (
        schema_with_db_qn := client.asset.append_terms(
            qualified_name=schema_with_db_qn.qualified_name,
            asset_type=Schema,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )


def test_replace_a_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    database: Database,
):
    time.sleep(5)
    assert (
        database := client.asset.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )

    assert (
        database := client.asset.replace_terms(
            guid=database.guid, asset_type=Database, terms=[term2]
        )
    )

    database = client.asset.get_by_guid(
        guid=database.guid, asset_type=Database, ignore_relationships=False
    )
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term2.guid


def test_replace_terms_with_same_qn(
    client: AtlanClient,
    term2: AtlasGlossaryTerm,
    database: Database,
    schema_with_db_qn: Schema,
):
    time.sleep(5)
    assert schema_with_db_qn.qualified_name == database.qualified_name
    assert (
        database := client.asset.replace_terms(
            guid=database.guid, asset_type=Database, terms=[term2]
        )
    )
    assert (
        schema_with_db_qn := client.asset.replace_terms(
            guid=schema_with_db_qn.guid, asset_type=Schema, terms=[term2]
        )
    )


def test_replace_all_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    database: Database,
):
    time.sleep(5)
    assert (
        database := client.asset.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(guid=term1.guid)],
        )
    )

    assert (
        database := client.asset.replace_terms(
            guid=database.guid, asset_type=Database, terms=[]
        )
    )

    database = client.asset.get_by_guid(
        guid=database.guid, asset_type=Database, ignore_relationships=False
    )
    assert database.assigned_terms == []
    assert len(database.assigned_terms) == 0


def test_remove_term(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    database: Database,
):
    time.sleep(5)
    assert (
        database := client.asset.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[
                AtlasGlossaryTerm.ref_by_guid(guid=term1.guid),
                AtlasGlossaryTerm.ref_by_guid(guid=term2.guid),
            ],
        )
    )

    assert (
        database := client.asset.remove_terms(
            guid=database.guid,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(term1.guid)],
        )
    )

    database = client.asset.get_by_guid(
        guid=database.guid, asset_type=Database, ignore_relationships=False
    )
    assert database.assigned_terms
    assert len(database.assigned_terms) == 1
    assert database.assigned_terms[0].guid == term2.guid


def test_remove_terms_with_same_qn(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    term2: AtlasGlossaryTerm,
    database: Database,
    schema_with_db_qn: Schema,
):
    time.sleep(5)
    assert schema_with_db_qn.qualified_name == database.qualified_name
    assert (
        database := client.asset.append_terms(
            qualified_name=database.qualified_name,
            asset_type=Database,
            terms=[
                AtlasGlossaryTerm.ref_by_guid(guid=term1.guid),
                AtlasGlossaryTerm.ref_by_guid(guid=term2.guid),
            ],
        )
    )
    assert (
        database := client.asset.remove_terms(
            guid=database.guid,
            asset_type=Database,
            terms=[AtlasGlossaryTerm.ref_by_guid(term1.guid)],
        )
    )
    assert (
        schema_with_db_qn := client.asset.append_terms(
            qualified_name=schema_with_db_qn.qualified_name,
            asset_type=Schema,
            terms=[
                AtlasGlossaryTerm.ref_by_guid(guid=term1.guid),
                AtlasGlossaryTerm.ref_by_guid(guid=term2.guid),
            ],
        )
    )
    assert (
        schema_with_db_qn := client.asset.remove_terms(
            guid=schema_with_db_qn.guid,
            asset_type=Schema,
            terms=[AtlasGlossaryTerm.ref_by_guid(term1.guid)],
        )
    )


def test_find_connections_by_name(client: AtlanClient):
    connections = client.asset.find_connections_by_name(
        name="development",
        connector_type=AtlanConnectorType.SNOWFLAKE,
        attributes=["connectorName"],
    )
    assert len(connections) == 1
    assert connections[0].connector_name == AtlanConnectorType.SNOWFLAKE.value


def test_get_asset_by_guid_good_guid(client: AtlanClient, glossary: AtlasGlossary):
    glossary = client.asset.get_by_guid(
        glossary.guid, AtlasGlossary, ignore_relationships=False
    )
    assert isinstance(glossary, AtlasGlossary)


def test_get_asset_by_guid_without_asset_type(
    client: AtlanClient, glossary: AtlasGlossary
):
    glossary = client.asset.get_by_guid(glossary.guid, ignore_relationships=False)
    assert isinstance(glossary, AtlasGlossary)


def test_get_minimal_asset_without_asset_type(
    client: AtlanClient, glossary: AtlasGlossary
):
    glossary = client.asset.retrieve_minimal(glossary.guid)
    assert isinstance(glossary, AtlasGlossary)


def test_get_asset_by_guid_when_table_specified_and_glossary_returned_raises_not_found_error(
    client: AtlanClient, glossary: AtlasGlossary
):
    guid = glossary.guid
    with pytest.raises(
        NotFoundError,
        match=f"ATLAN-PYTHON-404-002 Asset with GUID {guid} is not of the type requested: Table.",
    ):
        client.asset.get_by_guid(guid, Table, ignore_relationships=False)


def test_get_by_guid_with_fs(client: AtlanClient, term: AtlasGlossaryTerm):
    time.sleep(5)
    # Default - should call `GET_ENTITY_BY_GUID` API
    result = client.asset.get_by_guid(guid=term.guid, asset_type=AtlasGlossaryTerm)
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    # Ensure no relationship attributes are present
    assert result.anchor is None

    # Should call `GET_ENTITY_BY_GUID` API with `ignore_relationships=False`
    result = client.asset.get_by_guid(
        guid=term.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    assert result.anchor
    # These are not returned by the `GET_ENTITY_BY_GUID` API
    assert result.anchor.description is None
    assert result.anchor.user_description is None

    # Should call IndexSearch API without any relationship attributes
    result = client.asset.get_by_guid(
        guid=term.guid,
        asset_type=AtlasGlossaryTerm,
        ignore_relationships=False,
        attributes=[AtlasGlossaryTerm.DESCRIPTION, AtlasGlossaryTerm.USER_DESCRIPTION],  # type: ignore[arg-type]
    )
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    # Ensure no relationship attributes are present
    assert result.anchor is None

    # Should call IndexSearch API
    result = client.asset.get_by_guid(
        guid=term.guid,
        asset_type=AtlasGlossaryTerm,
        ignore_relationships=False,
        attributes=["description", "userDescription", "anchor"],
        related_attributes=[  # type: ignore[arg-type]
            AtlasGlossary.DESCRIPTION,
            AtlasGlossary.USER_DESCRIPTION,
        ],
    )
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    assert result.anchor
    assert result.anchor.description == f"{TEST_SYSTEM_DESCRIPTION}"
    assert result.anchor.user_description == f"{TEST_USER_DESCRIPTION}"


def test_get_by_qualified_name_with_fs(client: AtlanClient, term: AtlasGlossaryTerm):
    time.sleep(5)
    # Default - should call `GET_ENTITY_BY_GUID` API
    assert term and term.qualified_name
    result = client.asset.get_by_qualified_name(
        qualified_name=term.qualified_name, asset_type=AtlasGlossaryTerm
    )
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    # Ensure no relationship attributes are present
    assert result.anchor is None

    # Should call `GET_ENTITY_BY_GUID` API with `ignore_relationships=False`
    result = client.asset.get_by_qualified_name(
        qualified_name=term.qualified_name,
        asset_type=AtlasGlossaryTerm,
        ignore_relationships=False,
    )
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    assert result.anchor
    # These are not returned by the `GET_ENTITY_BY_GUID` API
    assert result.anchor.description is None
    assert result.anchor.user_description is None

    # Should call IndexSearch API without any relationship attributes
    result = client.asset.get_by_qualified_name(
        qualified_name=term.qualified_name,
        asset_type=AtlasGlossaryTerm,
        ignore_relationships=False,
        attributes=[AtlasGlossaryTerm.DESCRIPTION, AtlasGlossaryTerm.USER_DESCRIPTION],  # type: ignore[arg-type]
    )
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    # Ensure no relationship attributes are present
    assert result.anchor is None

    # Should call IndexSearch API
    result = client.asset.get_by_qualified_name(
        qualified_name=term.qualified_name,
        asset_type=AtlasGlossaryTerm,
        ignore_relationships=False,
        attributes=["description", "userDescription", "anchor"],
        related_attributes=[  # type: ignore[arg-type]
            AtlasGlossary.DESCRIPTION,
            AtlasGlossary.USER_DESCRIPTION,
        ],
    )
    assert isinstance(result, AtlasGlossaryTerm)
    assert result.guid == term.guid
    assert hasattr(result, "attributes")
    assert result.attributes.name == term.name
    assert result.attributes.qualified_name == term.qualified_name
    assert result.description == f"{TEST_SYSTEM_DESCRIPTION} Term"
    assert result.user_description == f"{TEST_USER_DESCRIPTION} Term"
    assert result.anchor
    assert result.anchor.description == f"{TEST_SYSTEM_DESCRIPTION}"
    assert result.anchor.user_description == f"{TEST_USER_DESCRIPTION}"


def test_get_asset_by_guid_bad_with_non_existent_guid_raises_not_found_error(
    client: AtlanClient,
):
    with pytest.raises(
        NotFoundError,
        match="ATLAN-PYTHON-404-000 Server responded with a not found "
        "error ATLAS-404-00-005: Given instance guid 76d54dd6 is invalid/not found",
    ):
        client.asset.get_by_guid("76d54dd6", AtlasGlossary, ignore_relationships=False)


def test_upsert_when_no_changes(client: AtlanClient, glossary: AtlasGlossary):
    response = client.asset.save(glossary)
    assert not response.guid_assignments
    assert not response.mutated_entities


def test_get_by_qualified_name(client: AtlanClient, glossary: AtlasGlossary):
    qualified_name = glossary.qualified_name or ""
    glossary = client.asset.get_by_qualified_name(
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
        client.asset.get_by_qualified_name(
            qualified_name=qualified_name, asset_type=Asset
        )


def test_add_classification(client: AtlanClient, term1: AtlasGlossaryTerm):
    assert term1.qualified_name
    client.asset.add_atlan_tags(
        AtlasGlossaryTerm, term1.qualified_name, [CLASSIFICATION_NAME]
    )
    glossary_term = client.asset.get_by_guid(
        term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert glossary_term.atlan_tags
    assert len(glossary_term.atlan_tags) == 1
    classification = glossary_term.atlan_tags[0]
    assert str(classification.type_name) == CLASSIFICATION_NAME


@pytest.mark.order(after="test_add_classification")
def test_include_atlan_tag_names(client: AtlanClient, term1: AtlasGlossaryTerm):
    assert term1 and term1.qualified_name
    query = Term.with_type_name(term1.type_name) + Term.with_name(term1.name)
    request = IndexSearchRequest(
        dsl=DSL(query=query), exclude_atlan_tags=True, include_atlan_tag_names=False
    )
    response = client.asset.search(criteria=request)

    # Ensure classification names are not present
    assert response
    assert response.current_page() and len(response.current_page()) == 1
    assert response.current_page()[0].guid == term1.guid
    assert response.current_page()[0].classification_names is None

    request = IndexSearchRequest(
        dsl=DSL(query=query), exclude_atlan_tags=True, include_atlan_tag_names=True
    )
    response = client.asset.search(criteria=request)

    # Ensure classification names are present
    assert response
    assert response.current_page() and len(response.current_page()) == 1
    assert response.current_page()[0].guid == term1.guid
    classification_names = response.current_page()[0].classification_names
    assert classification_names and len(classification_names) == 1


@pytest.mark.order(after="test_add_classification")
def test_remove_classification(client: AtlanClient, term1: AtlasGlossaryTerm):
    assert term1.qualified_name
    client.asset.remove_atlan_tag(
        AtlasGlossaryTerm, term1.qualified_name, CLASSIFICATION_NAME
    )
    glossary_term = client.asset.get_by_guid(
        term1.guid, asset_type=AtlasGlossaryTerm, ignore_relationships=False
    )
    assert not glossary_term.atlan_tags


def test_glossary_update_certificate(client: AtlanClient, glossary: AtlasGlossary):
    _test_update_certificate(client, glossary, AtlasGlossary)


def test_glossary_term_update_certificate(
    client: AtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    _test_update_certificate(client, term1, AtlasGlossaryTerm, glossary.guid)


def test_glossary_category_update_certificate(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    _test_update_certificate(client, category, AtlasGlossaryCategory, glossary.guid)


@pytest.mark.order(after="test_glossary_update_certificate")
def test_glossary_remove_certificate(client: AtlanClient, glossary: AtlasGlossary):
    _test_remove_certificate(client, glossary, AtlasGlossary)


@pytest.mark.order(after="test_glossary_term_update_certificate")
def test_glossary_term_remove_certificate(
    client: AtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    _test_remove_certificate(client, term1, AtlasGlossaryTerm, glossary.guid)


@pytest.mark.order(after="test_glossary_category_update_certificate")
def test_glossary_category_remove_certificate(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    _test_remove_certificate(client, category, AtlasGlossaryCategory, glossary.guid)


def test_glossary_update_announcement(
    client: AtlanClient, glossary: AtlasGlossary, announcement: Announcement
):
    _test_update_announcement(client, glossary, AtlasGlossary, announcement)


def test_asset_remove_certificate_by_setting_none(
    client: AtlanClient,
    database: Database,
):
    assert database
    assert database.guid
    assert database.certificate_status
    assert database.certificate_status_message
    database.certificate_status = None
    database.certificate_status_message = None
    response = client.asset.save(entity=[database])
    db_updated = response.assets_updated(asset_type=Database)

    assert db_updated
    assert len(db_updated) == 1
    assert db_updated[0].name == database.name
    assert db_updated[0].guid == database.guid
    assert db_updated[0].certificate_status is None
    assert db_updated[0].certificate_status_message is None


def test_glossary_term_update_announcement(
    client: AtlanClient,
    term1: AtlasGlossaryTerm,
    glossary: AtlasGlossary,
    announcement: Announcement,
):
    _test_update_announcement(
        client, term1, AtlasGlossaryTerm, announcement, glossary.guid
    )


def test_glossary_category_update_announcement(
    client: AtlanClient,
    category: AtlasGlossaryCategory,
    glossary: AtlasGlossary,
    announcement: Announcement,
):
    _test_update_announcement(
        client, category, AtlasGlossaryCategory, announcement, glossary.guid
    )


@pytest.mark.order(after="test_glossary_update_announcement")
def test_glossary_remove_announcement(client: AtlanClient, glossary: AtlasGlossary):
    _test_remove_announcement(client, glossary, AtlasGlossary)


@pytest.mark.order(after="test_glossary_term_update_announcement")
def test_glossary_term_remove_announcement(
    client: AtlanClient, term1: AtlasGlossaryTerm, glossary: AtlasGlossary
):
    _test_remove_announcement(client, term1, AtlasGlossaryTerm, glossary.guid)


@pytest.mark.order(after="test_glossary_category_update_announcement")
def test_glossary_category_remove_announcement(
    client: AtlanClient, category: AtlasGlossaryCategory, glossary: AtlasGlossary
):
    _test_remove_announcement(client, category, AtlasGlossaryCategory, glossary.guid)


def test_audit_find_by_user(
    client: AtlanClient,
    current_user: UserMinimalResponse,
    audit_info: AuditInfo,
):
    size = 10
    assert current_user.username

    results = client.audit.search(
        AuditSearchRequest.by_user(current_user.username, size=size, sort=[])
    )
    assert results.total_count > 0
    assert size == len(results.current_page())
    audit_entity = results.current_page()[0]
    audit_info.qualified_name = audit_entity.entity_qualified_name
    audit_info.guid = audit_entity.entity_id
    audit_info.type_name = audit_entity.type_name

    # Fetch next page and make sure pagination works
    results.next_page()
    audit_entity_next_page = results._entity_audits[0]
    assert audit_entity != audit_entity_next_page


@pytest.fixture(scope="module")
def generate_audit_entries(client: AtlanClient, audit_glossary: AtlasGlossary):
    log_count = 5
    for i in range(log_count):
        updater = AtlasGlossary.updater(
            qualified_name=audit_glossary.qualified_name,
            name=audit_glossary.name,
        )
        updater.description = f"Updated description {i + 1}"
        client.asset.save(updater)
        time.sleep(1)

    request = AuditSearchRequest.by_guid(guid=audit_glossary.guid, size=log_count)
    response = client.audit.search(request)
    assert response.total_count >= log_count, (
        f"Expected at least {log_count} logs, but got {response.total_count}."
    )


def _assert_audit_search_results(
    results, expected_sorts, size, TOTAL_AUDIT_ENTRIES, bulk=False
):
    assert results.total_count > size
    assert len(results.current_page()) == size
    counter = 0
    for audit in results:
        assert audit
        counter += 1
    assert counter == TOTAL_AUDIT_ENTRIES
    assert results
    assert results._bulk is bulk
    assert results._criteria.dsl.sort == expected_sorts


@pytest.mark.order(after="test_audit_find_by_user")
@patch.object(AUDIT_LOGGER, "debug")
def test_audit_search_pagination(
    mock_logger,
    audit_glossary: AtlasGlossary,
    generate_audit_entries,
    client: AtlanClient,
):
    size = 2

    # Test audit search by GUID with default offset-based pagination
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value=audit_glossary.guid)]),
        sort=[],
        size=size,
    )
    request = AuditSearchRequest(dsl=dsl)
    results = client.audit.search(criteria=request, bulk=False)
    TOTAL_AUDIT_ENTRIES = results.total_count
    expected_sorts = [SortItem(field="entityId", order=SortOrder.ASCENDING)]
    _assert_audit_search_results(
        results, expected_sorts, size, TOTAL_AUDIT_ENTRIES, False
    )

    # Test audit search by guid with `bulk` option using timestamp-based pagination
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value=audit_glossary.guid)]),
        sort=[],
        size=size,
    )
    request = AuditSearchRequest(dsl=dsl)
    results = client.audit.search(criteria=request, bulk=True)
    expected_sorts = [
        SortItem("created", order=SortOrder.ASCENDING),
        SortItem(field="entityId", order=SortOrder.ASCENDING),
    ]
    _assert_audit_search_results(
        results, expected_sorts, size, TOTAL_AUDIT_ENTRIES, True
    )
    assert mock_logger.call_count == 1
    assert "Audit bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()

    # When the number of results exceeds the predefined
    # threshold and bulk is true and no pre-defined sort.
    with patch.object(AuditSearchResults, "_MASS_EXTRACT_THRESHOLD", -1):
        dsl = DSL(
            query=Bool(filter=[Term(field="entityId", value=audit_glossary.guid)]),
            sort=[],
            size=size,
        )
        request = AuditSearchRequest(dsl=dsl)
        results = client.audit.search(criteria=request, bulk=True)
        expected_sorts = [
            SortItem("created", order=SortOrder.ASCENDING),
            SortItem(field="entityId", order=SortOrder.ASCENDING),
        ]
        _assert_audit_search_results(
            results, expected_sorts, size, TOTAL_AUDIT_ENTRIES, True
        )
        assert mock_logger.call_count < TOTAL_AUDIT_ENTRIES
        assert (
            "Audit bulk search option is enabled."
            in mock_logger.call_args_list[0][0][0]
        )
        mock_logger.reset_mock()

    # When the number of results exceeds the predefined threshold and bulk is `False` and no pre-defined sort.
    # Then SDK automatically switches to a `bulk` search option using timestamp-based pagination
    with patch.object(AuditSearchResults, "_MASS_EXTRACT_THRESHOLD", -1):
        dsl = DSL(
            query=Bool(filter=[Term(field="entityId", value=audit_glossary.guid)]),
            sort=[],
            size=size,
        )
        request = AuditSearchRequest(dsl=dsl)
        results = client.audit.search(criteria=request, bulk=False)
        results.total_count
        expected_sorts = [
            SortItem("created", order=SortOrder.ASCENDING),
            SortItem(field="entityId", order=SortOrder.ASCENDING),
        ]
        _assert_audit_search_results(
            results, expected_sorts, size, TOTAL_AUDIT_ENTRIES, False
        )
        assert mock_logger.call_count < TOTAL_AUDIT_ENTRIES
        assert (
            "Result size (%s) exceeds threshold (%s)."
            in mock_logger.call_args_list[0][0][0]
        )
        mock_logger.reset_mock()


@pytest.mark.order(after="test_audit_search_pagination")
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


def test_audit_search_default_sorting(client: AtlanClient, audit_info: AuditInfo):
    # Test empty sorting
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value=audit_info.guid)]),
        sort=[],
        size=10,
        from_=0,
    )
    request = AuditSearchRequest(dsl=dsl)
    response = client.audit.search(criteria=request)
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 1
    assert sort_options[0].field == AUDIT_SORT_BY_GUID.field

    # Sort without GUID
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value=audit_info.guid)]),
        sort=[AUDIT_SORT_BY_LATEST],
        size=10,
        from_=0,
    )
    request = AuditSearchRequest(dsl=dsl)
    response = client.audit.search(criteria=request)
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 2
    assert sort_options[0].field == AUDIT_SORT_BY_LATEST.field
    assert sort_options[1].field == AUDIT_SORT_BY_GUID.field

    # Sort with only GUID
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value=audit_info.guid)]),
        sort=[AUDIT_SORT_BY_GUID],
        size=10,
        from_=0,
    )
    request = AuditSearchRequest(dsl=dsl)
    response = client.audit.search(criteria=request)
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 1
    assert sort_options[0].field == AUDIT_SORT_BY_GUID.field

    # Sort with GUID and others
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value=audit_info.guid)]),
        sort=[AUDIT_SORT_BY_GUID, AUDIT_SORT_BY_LATEST],
        size=10,
        from_=0,
    )
    request = AuditSearchRequest(dsl=dsl)
    response = client.audit.search(criteria=request)
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 2
    assert sort_options[0].field == AUDIT_SORT_BY_GUID.field
    assert sort_options[1].field == AUDIT_SORT_BY_LATEST.field


def _view_test_glossary_by_search(
    client: AtlanClient, sl_glossary: AtlasGlossary
) -> None:
    time.sleep(2)
    index = (
        FluentSearch().where(Asset.GUID.eq(sl_glossary.guid, case_insensitive=True))
    ).to_request()
    index.request_metadata = IndexSearchRequest.Metadata(
        utm_tags=[
            UTMTags.ACTION_ASSET_VIEWED,
            UTMTags.UI_PROFILE,
            UTMTags.UI_SIDEBAR,
            UTMTags.PROJECT_SDK_PYTHON,
        ],
        save_search_log=True,
    )
    response = client.asset.search(index)
    assert response.count == 1
    assert response.current_page()[0].name == sl_glossary.name
    time.sleep(2)


def test_search_log_most_recent_viewers(
    client: AtlanClient, current_user: UserMinimalResponse, sl_glossary: AtlasGlossary
):
    _view_test_glossary_by_search(client, sl_glossary)
    request = SearchLogRequest.most_recent_viewers(guid=sl_glossary.guid)
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogViewResults):
        pytest.fail(f"Failed to retrieve most recent viewers of : {sl_glossary.name}")
    viewers = response.user_views
    assert response.asset_views is None
    if viewers is not None:
        assert len(viewers) == 1
        for viewer in viewers:
            assert viewer.username
            assert viewer.view_count
            assert viewer.most_recent_view

    # Test exclude users
    assert current_user.username
    request = SearchLogRequest.most_recent_viewers(
        guid=sl_glossary.guid, exclude_users=[current_user.username]
    )
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogViewResults):
        pytest.fail(f"Failed to retrieve most recent viewers of : {sl_glossary.name}")
    assert response.count == 0
    assert response.user_views is not None
    assert len(response.user_views) == 0
    assert response.asset_views is None


@pytest.mark.order(after="test_search_log_most_recent_viewers")
def test_search_log_most_viewed_assets(
    client: AtlanClient,
    current_user: UserMinimalResponse,
    sl_glossary: AtlasGlossary,
):
    def _assert_most_viewed_assets(
        details: Optional[List[AssetViews]],
    ):
        if details is not None:
            assert len(details) > 0
            for detail in details:
                assert detail.guid
                assert detail.total_views
                assert detail.distinct_users

    request = SearchLogRequest.most_viewed_assets(max_assets=10)
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogViewResults):
        pytest.fail("Failed to retrieve most viewed assets")
    assert response.user_views is None
    _assert_most_viewed_assets(response.asset_views)

    request = SearchLogRequest.most_viewed_assets(max_assets=10, by_different_user=True)
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogViewResults):
        pytest.fail("Failed to retrieve most viewed assets (by_different_user)")
    assert response.user_views is None
    _assert_most_viewed_assets(response.asset_views)

    # Test exclude users
    prev_count = response.count
    assert prev_count
    assert current_user.username
    request = SearchLogRequest.most_viewed_assets(
        max_assets=10, exclude_users=[current_user.username]
    )
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogViewResults):
        pytest.fail("Failed to retrieve most viewed assets")
    assert response.count < prev_count
    assert response.user_views is None
    _assert_most_viewed_assets(response.asset_views)


@pytest.mark.order(after="test_search_log_most_viewed_assets")
def test_search_log_views_by_guid(
    client: AtlanClient, current_user: UserMinimalResponse, sl_glossary: AtlasGlossary
):
    request = SearchLogRequest.views_by_guid(guid=sl_glossary.guid, size=10)
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogResults):
        pytest.fail("Failed to retrieve asset detailed log entries")
    log_entries = response.current_page()
    assert len(response.current_page()) == 1
    assert "Atlan-PythonSDK" in log_entries[0].user_agent
    assert "service-account-apikey" in log_entries[0].user_name
    assert log_entries[0].entity_guids_all[0] == sl_glossary.guid
    assert log_entries[0].ip_address
    assert log_entries[0].host
    assert log_entries[0].utm_tags
    assert log_entries[0].entity_guids_allowed
    assert log_entries[0].entity_qf_names_all
    assert log_entries[0].entity_qf_names_allowed
    assert log_entries[0].entity_type_names_all
    assert log_entries[0].entity_type_names_allowed
    assert log_entries[0].has_result
    assert log_entries[0].results_count
    assert log_entries[0].response_time
    assert log_entries[0].created_at
    assert log_entries[0].timestamp
    assert log_entries[0].failed is False
    assert log_entries[0].request_dsl
    assert log_entries[0].request_dsl_text
    assert log_entries[0].request_attributes is None
    assert log_entries[0].request_relation_attributes is None

    # Test exclude users
    assert current_user.username
    request = SearchLogRequest.views_by_guid(
        guid=sl_glossary.guid, size=10, exclude_users=[current_user.username]
    )
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogResults):
        pytest.fail("Failed to retrieve asset detailed log entries")
    assert response.count == 0
    assert len(response.current_page()) == 0


@pytest.fixture(scope="module")
def generate_search_logs(client: AtlanClient, sl_glossary: AtlasGlossary):
    log_count = 5

    for _ in range(log_count):
        _view_test_glossary_by_search(client, sl_glossary)
        time.sleep(1)

    request = SearchLogRequest.views_by_guid(guid=sl_glossary.guid, size=20)
    response = client.search_log.search(request)
    assert response.count >= log_count, (
        f"Expected at least {log_count} logs, but got {response.count}."
    )


def _assert_search_log_results(
    results, expected_sorts, size, TOTAL_LOG_ENTRIES, bulk=False
):
    assert results.count > size
    assert len(results.current_page()) == size
    counter = 0
    for log in results:
        assert log
        counter += 1
    assert counter == TOTAL_LOG_ENTRIES
    assert results
    assert results._bulk is bulk
    assert results._criteria.dsl.sort == expected_sorts


@patch.object(SEARCH_LOG_LOGGER, "debug")
def test_search_log_pagination(
    mock_logger, generate_search_logs, sl_glossary: AtlasGlossary, client: AtlanClient
):
    size = 2
    # Test search logs by GUID with default offset-based pagination
    search_log_request = SearchLogRequest.views_by_guid(
        guid=sl_glossary.guid,
        size=size,
        exclude_users=[],
    )

    results = client.search_log.search(criteria=search_log_request, bulk=False)
    TOTAL_LOG_ENTRIES = results.count

    expected_sorts = [
        SortItem(field="timestamp", order=SortOrder.ASCENDING),
        SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING),
    ]
    _assert_search_log_results(results, expected_sorts, size, TOTAL_LOG_ENTRIES)

    # Test search logs by GUID with `bulk` option using timestamp-based pagination
    search_log_request = SearchLogRequest.views_by_guid(
        guid=sl_glossary.guid,
        size=size,
        exclude_users=[],
    )
    results = client.search_log.search(criteria=search_log_request, bulk=True)
    expected_sorts = [
        SortItem(field="createdAt", order=SortOrder.ASCENDING),
        SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING),
    ]
    _assert_search_log_results(results, expected_sorts, size, TOTAL_LOG_ENTRIES, True)
    assert mock_logger.call_count == 1
    assert (
        "Search log bulk search option is enabled."
        in mock_logger.call_args_list[0][0][0]
    )
    mock_logger.reset_mock()

    # When the number of results exceeds the predefined threshold and bulk=True
    with patch.object(SearchLogResults, "_MASS_EXTRACT_THRESHOLD", -1):
        search_log_request = SearchLogRequest.views_by_guid(
            guid=sl_glossary.guid,
            size=size,
            exclude_users=[],
        )
        results = client.search_log.search(criteria=search_log_request, bulk=True)
        expected_sorts = [
            SortItem(field="createdAt", order=SortOrder.ASCENDING),
            SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING),
        ]
        _assert_search_log_results(
            results, expected_sorts, size, TOTAL_LOG_ENTRIES, True
        )
        assert mock_logger.call_count < TOTAL_LOG_ENTRIES
        assert (
            "Search log bulk search option is enabled."
            in mock_logger.call_args_list[0][0][0]
        )
        mock_logger.reset_mock()

    # When results exceed threshold and bulk=False, SDK auto-switches to bulk search
    with patch.object(SearchLogResults, "_MASS_EXTRACT_THRESHOLD", -1):
        search_log_request = SearchLogRequest.views_by_guid(
            guid=sl_glossary.guid,
            size=size,
            exclude_users=[],
        )
        results = client.search_log.search(criteria=search_log_request, bulk=False)
        expected_sorts = [
            SortItem(field="createdAt", order=SortOrder.ASCENDING),
            SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING),
        ]
        _assert_search_log_results(results, expected_sorts, size, TOTAL_LOG_ENTRIES)
        assert mock_logger.call_count < TOTAL_LOG_ENTRIES
        assert (
            "Result size (%s) exceeds threshold (%s)."
            in mock_logger.call_args_list[0][0][0]
        )
        mock_logger.reset_mock()


def test_search_log_default_sorting(client: AtlanClient, sl_glossary: AtlasGlossary):
    # Empty sorting
    request = SearchLogRequest.views_by_guid(guid=sl_glossary.guid, size=10, sort=[])
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogResults):
        pytest.fail("Failed to retrieve asset detailed log entries")
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 2
    assert sort_options[0].field == SL_SORT_BY_TIMESTAMP.field
    assert sort_options[1].field == SL_SORT_BY_GUID.field

    # Sort without GUID
    request = SearchLogRequest.views_by_guid(
        guid=sl_glossary.guid,
        size=10,
        sort=[SL_SORT_BY_QUALIFIED_NAME],
    )
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogResults):
        pytest.fail("Failed to retrieve asset detailed log entries")
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 3
    assert sort_options[0].field == SL_SORT_BY_QUALIFIED_NAME.field
    assert sort_options[1].field == SL_SORT_BY_TIMESTAMP.field
    assert sort_options[2].field == SL_SORT_BY_GUID.field

    # Sort with only GUID
    request = SearchLogRequest.views_by_guid(
        guid=sl_glossary.guid,
        size=10,
        sort=[SL_SORT_BY_GUID],
    )
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogResults):
        pytest.fail("Failed to retrieve asset detailed log entries")
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 2
    assert sort_options[0].field == SL_SORT_BY_GUID.field
    assert sort_options[1].field == SL_SORT_BY_TIMESTAMP.field

    # Sort with GUID and others
    request = SearchLogRequest.views_by_guid(
        guid=sl_glossary.guid,
        size=10,
        sort=[SL_SORT_BY_GUID, SL_SORT_BY_QUALIFIED_NAME],
    )
    response = client.search_log.search(request)
    if not isinstance(response, SearchLogResults):
        pytest.fail("Failed to retrieve asset detailed log entries")
    assert response
    sort_options = response._criteria.dsl.sort
    assert len(sort_options) == 3
    assert sort_options[0].field == SL_SORT_BY_GUID.field
    assert sort_options[1].field == SL_SORT_BY_QUALIFIED_NAME.field
    assert sort_options[2].field == SL_SORT_BY_TIMESTAMP.field


def test_client_401_token_refresh(
    client: AtlanClient, expired_token: ApiToken, argo_fake_token: ApiToken, monkeypatch
):
    # Use a smaller retry count to speed up test execution
    DEFAULT_RETRY.total = 1

    # Retrieve required client information before updating the client with invalid API tokens
    assert argo_fake_token and argo_fake_token.guid
    argo_client_secret = client.impersonate.get_client_secret(
        client_guid=argo_fake_token.guid
    )

    # Retrieve the user ID associated with the expired token's username
    # Since user credentials for API tokens cannot be retrieved directly, use the existing username
    expired_token_user_id = client.impersonate.get_user_id(
        username=expired_token.username
    )

    # Initialize the client with an expired/invalid token (results in 401 Unauthorized errors)
    assert (
        expired_token
        and expired_token.attributes
        and expired_token.attributes.access_token
    )
    client = AtlanClient(
        api_key=expired_token.attributes.access_token, retry=DEFAULT_RETRY
    )
    expired_api_token = expired_token.attributes.access_token

    # Case 1: No user_id (default)
    # Verify that the client raises an authentication error when no user ID is provided
    assert client._user_client is None
    with pytest.raises(
        AuthenticationError,
        match="Server responded with an authentication error 401",
    ):
        FluentSearch().where(CompoundQuery.active_assets()).where(
            CompoundQuery.asset_type(AtlasGlossary)
        ).page_size(100).execute(client=client)

    # Case 2: Invalid user_id
    # Test that providing an invalid user ID results in the same authentication error
    client._user_id = "invalid-user-id"
    with pytest.raises(
        InvalidRequestError,
        match="Missing privileged credentials to impersonate users",
    ):
        FluentSearch().where(CompoundQuery.active_assets()).where(
            CompoundQuery.asset_type(AtlasGlossary)
        ).page_size(100).execute(client=client)

    # Case 3: Valid user_id associated with the expired token
    # This should trigger a retry, refresh the token
    # and use the new bearer token for subsequent requests
    # Set up a fake Argo client ID and client secret for impersonation
    monkeypatch.setenv("CLIENT_ID", argo_fake_token.client_id)
    monkeypatch.setenv("CLIENT_SECRET", argo_client_secret)

    # Configure the client with the user ID
    # of the expired token to ensure token refresh is possible
    client._user_id = expired_token_user_id

    # Verify that the API key is updated after the retry and the request succeeds
    results = (
        FluentSearch()
        .where(CompoundQuery.active_assets())
        .where(CompoundQuery.asset_type(AtlasGlossary))
        .page_size(100)
        .execute(client=client)
    )

    # Confirm the API key has been updated and results are returned
    assert client.api_key != expired_api_token
    assert results and results.count >= 1


def test_process_assets_when_no_assets_found(client: AtlanClient):
    def should_never_be_called(_: Asset):
        pytest.fail("Should not be called")

    search = (
        FluentSearch()
        .where(Term.with_state("ACTIVE"))
        .where(Asset.NAME.startswith("zXZ"))
    )

    processed_count = client.asset.process_assets(
        search=search, func=should_never_be_called
    )
    assert processed_count == 0


def test_process_assets_when_assets_found(client: AtlanClient):
    def doit(asset: Asset):
        global call_count
        call_count += 1

    search = (
        FluentSearch()
        .where(Term.with_state("ACTIVE"))
        .where(Asset.TYPE_NAME.eq("Table"))
        .where(Asset.NAME.startswith("B"))
    )
    expected_count = client.asset.search(search.to_request()).count

    processed_count = client.asset.process_assets(search=search, func=doit)

    assert call_count == expected_count
    assert processed_count == expected_count
