# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    SalesforceDashboard,
    SalesforceField,
    SalesforceObject,
    SalesforceOrganization,
    SalesforceReport,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SALESFORCE")

ORG_ID = f"00D{MODULE_NAME}"
OBJECT_API_NAME = f"Obj_{MODULE_NAME}__c"
FIELD_API_NAME = f"Fld_{MODULE_NAME}__c"
REPORT_ID = f"00O{MODULE_NAME}"
DASHBOARD_ID = f"01Z{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SALESFORCE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def organization(
    client: AtlanClient, connection: Connection
) -> Generator[SalesforceOrganization, None, None]:
    to_create = SalesforceOrganization.creator(
        name=f"org_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        source_id=ORG_ID,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SalesforceOrganization
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SalesforceOrganization)


@pytest.fixture(scope="module")
def sf_object(
    client: AtlanClient, organization: SalesforceOrganization
) -> Generator[SalesforceObject, None, None]:
    to_create = SalesforceObject.creator(
        name=f"object_{MODULE_NAME}",
        api_name=OBJECT_API_NAME,
        organization_qualified_name=organization.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SalesforceObject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SalesforceObject)


@pytest.fixture(scope="module")
def sf_field(
    client: AtlanClient, sf_object: SalesforceObject
) -> Generator[SalesforceField, None, None]:
    to_create = SalesforceField.creator(
        name=f"field_{MODULE_NAME}",
        api_name=FIELD_API_NAME,
        object_qualified_name=sf_object.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SalesforceField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SalesforceField)


@pytest.fixture(scope="module")
def report(
    client: AtlanClient, organization: SalesforceOrganization
) -> Generator[SalesforceReport, None, None]:
    to_create = SalesforceReport.creator(
        name=f"report_{MODULE_NAME}",
        source_id=REPORT_ID,
        organization_qualified_name=organization.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SalesforceReport)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SalesforceReport)


@pytest.fixture(scope="module")
def dashboard(
    client: AtlanClient, organization: SalesforceOrganization
) -> Generator[SalesforceDashboard, None, None]:
    to_create = SalesforceDashboard.creator(
        name=f"dashboard_{MODULE_NAME}",
        source_id=DASHBOARD_ID,
        organization_qualified_name=organization.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SalesforceDashboard
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SalesforceDashboard)


def _retrieve(client, asset, asset_type, connection, expected_qn):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == expected_qn
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.SALESFORCE
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def _org_qn(connection: Connection) -> str:
    return f"{connection.qualified_name}/{ORG_ID}"


def test_organization(
    client: AtlanClient,
    connection: Connection,
    organization: SalesforceOrganization,
):
    retrieved = _retrieve(
        client, organization, SalesforceOrganization, connection, _org_qn(connection)
    )
    assert retrieved.source_id == ORG_ID


def test_object(
    client: AtlanClient,
    connection: Connection,
    organization: SalesforceOrganization,
    sf_object: SalesforceObject,
):
    retrieved = _retrieve(
        client,
        sf_object,
        SalesforceObject,
        connection,
        f"{_org_qn(connection)}/{OBJECT_API_NAME}",
    )
    assert retrieved.api_name == OBJECT_API_NAME
    assert retrieved.organization_qualified_name == _org_qn(connection)
    assert retrieved.organization.guid == organization.guid


def test_field(
    client: AtlanClient,
    connection: Connection,
    sf_object: SalesforceObject,
    sf_field: SalesforceField,
):
    retrieved = _retrieve(
        client,
        sf_field,
        SalesforceField,
        connection,
        f"{_org_qn(connection)}/{OBJECT_API_NAME}/{FIELD_API_NAME}",
    )
    assert retrieved.api_name == FIELD_API_NAME
    assert retrieved.object_qualified_name == sf_object.qualified_name
    assert retrieved.organization_qualified_name == _org_qn(connection)
    assert retrieved.object.guid == sf_object.guid


@pytest.mark.parametrize(
    "fixture_name, asset_type, source_id",
    [
        ("report", SalesforceReport, REPORT_ID),
        ("dashboard", SalesforceDashboard, DASHBOARD_ID),
    ],
)
def test_report_and_dashboard(
    request,
    client: AtlanClient,
    connection: Connection,
    organization: SalesforceOrganization,
    fixture_name,
    asset_type,
    source_id,
):
    asset = request.getfixturevalue(fixture_name)
    retrieved = _retrieve(
        client, asset, asset_type, connection, f"{_org_qn(connection)}/{source_id}"
    )
    assert retrieved.source_id == source_id
    assert retrieved.organization_qualified_name == _org_qn(connection)
    assert retrieved.organization.guid == organization.guid
