# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    TableauCalculatedField,
    TableauDashboard,
    TableauDashboardField,
    TableauDatasource,
    TableauDatasourceField,
    TableauProject,
    TableauSite,
    TableauWorkbook,
    TableauWorksheet,
    TableauWorksheetField,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("TABLEAU")

SITE_ID = f"site-{MODULE_NAME}"
PROJECT_ID = f"proj-{MODULE_NAME}"
SUB_PROJECT_ID = f"subproj-{MODULE_NAME}"
WORKBOOK_ID = f"wb-{MODULE_NAME}"
PUBLISHED_DS_ID = f"pds-{MODULE_NAME}"
EMBEDDED_DS_ID = f"eds-{MODULE_NAME}"
DASHBOARD_ID = f"dash-{MODULE_NAME}"
WORKSHEET_ID = f"ws-{MODULE_NAME}"
DS_FIELD_ID = f"dsf-{MODULE_NAME}"
CALC_FIELD_ID = f"cf-{MODULE_NAME}"


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.TABLEAU
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def site(
    client: AtlanClient, connection: Connection
) -> Generator[TableauSite, None, None]:
    to_create = TableauSite.creator(
        name=f"site_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        site_id=SITE_ID,
    )
    result = _save(client, to_create, TableauSite)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauSite)


@pytest.fixture(scope="module")
def project(
    client: AtlanClient, site: TableauSite
) -> Generator[TableauProject, None, None]:
    to_create = TableauProject.creator(
        name=f"project_{MODULE_NAME}",
        site_qualified_name=site.qualified_name,
        project_id=PROJECT_ID,
    )
    result = _save(client, to_create, TableauProject)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauProject)


@pytest.fixture(scope="module")
def sub_project(
    client: AtlanClient, site: TableauSite, project: TableauProject
) -> Generator[TableauProject, None, None]:
    to_create = TableauProject.creator(
        name=f"sub_project_{MODULE_NAME}",
        site_qualified_name=site.qualified_name,
        project_id=SUB_PROJECT_ID,
        parent_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauProject)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauProject)


@pytest.fixture(scope="module")
def workbook(
    client: AtlanClient, project: TableauProject, sub_project: TableauProject
) -> Generator[TableauWorkbook, None, None]:
    # Lives in the nested project, so its top-level project is the parent.
    to_create = TableauWorkbook.creator(
        name=f"workbook_{MODULE_NAME}",
        project_qualified_name=sub_project.qualified_name,
        workbook_id=WORKBOOK_ID,
        top_level_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauWorkbook)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauWorkbook)


@pytest.fixture(scope="module")
def published_datasource(
    client: AtlanClient, project: TableauProject
) -> Generator[TableauDatasource, None, None]:
    to_create = TableauDatasource.creator(
        name=f"published_ds_{MODULE_NAME}",
        project_qualified_name=project.qualified_name,
        datasource_id=PUBLISHED_DS_ID,
    )
    result = _save(client, to_create, TableauDatasource)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauDatasource)


@pytest.fixture(scope="module")
def embedded_datasource(
    client: AtlanClient,
    project: TableauProject,
    sub_project: TableauProject,
    workbook: TableauWorkbook,
) -> Generator[TableauDatasource, None, None]:
    to_create = TableauDatasource.creator(
        name=f"embedded_ds_{MODULE_NAME}",
        project_qualified_name=sub_project.qualified_name,
        datasource_id=EMBEDDED_DS_ID,
        workbook_qualified_name=workbook.qualified_name,
        top_level_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauDatasource)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauDatasource)


@pytest.fixture(scope="module")
def dashboard(
    client: AtlanClient, project: TableauProject, workbook: TableauWorkbook
) -> Generator[TableauDashboard, None, None]:
    to_create = TableauDashboard.creator(
        name=f"dashboard_{MODULE_NAME}",
        workbook_qualified_name=workbook.qualified_name,
        dashboard_id=DASHBOARD_ID,
        top_level_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauDashboard)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauDashboard)


@pytest.fixture(scope="module")
def worksheet(
    client: AtlanClient, project: TableauProject, workbook: TableauWorkbook
) -> Generator[TableauWorksheet, None, None]:
    to_create = TableauWorksheet.creator(
        name=f"worksheet_{MODULE_NAME}",
        workbook_qualified_name=workbook.qualified_name,
        worksheet_id=WORKSHEET_ID,
        top_level_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauWorksheet)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauWorksheet)


@pytest.fixture(scope="module")
def datasource_field(
    client: AtlanClient, published_datasource: TableauDatasource
) -> Generator[TableauDatasourceField, None, None]:
    to_create = TableauDatasourceField.creator(
        name=f"ds_field_{MODULE_NAME}",
        datasource_qualified_name=published_datasource.qualified_name,
        field_id=DS_FIELD_ID,
    )
    result = _save(client, to_create, TableauDatasourceField)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauDatasourceField)


@pytest.fixture(scope="module")
def calculated_field(
    client: AtlanClient,
    project: TableauProject,
    embedded_datasource: TableauDatasource,
) -> Generator[TableauCalculatedField, None, None]:
    to_create = TableauCalculatedField.creator(
        name=f"calc_field_{MODULE_NAME}",
        datasource_qualified_name=embedded_datasource.qualified_name,
        field_id=CALC_FIELD_ID,
        top_level_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauCalculatedField)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauCalculatedField)


@pytest.fixture(scope="module")
def worksheet_field(
    client: AtlanClient,
    project: TableauProject,
    worksheet: TableauWorksheet,
    datasource_field: TableauDatasourceField,
) -> Generator[TableauWorksheetField, None, None]:
    # The app keys worksheet fields by the id of the datasource field they use.
    to_create = TableauWorksheetField.creator(
        name=f"ws_field_{MODULE_NAME}",
        worksheet_qualified_name=worksheet.qualified_name,
        field_id=DS_FIELD_ID,
        top_level_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauWorksheetField)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauWorksheetField)


@pytest.fixture(scope="module")
def dashboard_field(
    client: AtlanClient,
    project: TableauProject,
    dashboard: TableauDashboard,
    datasource_field: TableauDatasourceField,
) -> Generator[TableauDashboardField, None, None]:
    to_create = TableauDashboardField.creator(
        name=f"dash_field_{MODULE_NAME}",
        dashboard_qualified_name=dashboard.qualified_name,
        field_id=DS_FIELD_ID,
        top_level_project_qualified_name=project.qualified_name,
    )
    result = _save(client, to_create, TableauDashboardField)
    yield result
    delete_asset(client, guid=result.guid, asset_type=TableauDashboardField)


def _assert_retrieved(client, asset, asset_type, connection, expected_suffix):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == f"{connection.qualified_name}/{expected_suffix}"
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.TABLEAU
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_site(client: AtlanClient, connection: Connection, site):
    _assert_retrieved(client, site, TableauSite, connection, SITE_ID)


def test_project(client: AtlanClient, connection: Connection, site, project):
    retrieved = _assert_retrieved(
        client, project, TableauProject, connection, f"{SITE_ID}/{PROJECT_ID}"
    )
    assert retrieved.site.guid == site.guid
    assert retrieved.site_qualified_name == site.qualified_name
    assert retrieved.is_top_level_project is True


def test_sub_project_is_flat(
    client: AtlanClient, connection: Connection, site, project, sub_project
):
    retrieved = _assert_retrieved(
        client, sub_project, TableauProject, connection, f"{SITE_ID}/{SUB_PROJECT_ID}"
    )
    assert retrieved.site.guid == site.guid
    assert retrieved.parent_project.guid == project.guid
    assert retrieved.is_top_level_project is False
    assert retrieved.top_level_project_qualified_name == project.qualified_name


def test_workbook(
    client: AtlanClient, connection: Connection, site, project, sub_project, workbook
):
    retrieved = _assert_retrieved(
        client,
        workbook,
        TableauWorkbook,
        connection,
        f"{SITE_ID}/{SUB_PROJECT_ID}/{WORKBOOK_ID}",
    )
    assert retrieved.project.guid == sub_project.guid
    assert retrieved.site_qualified_name == site.qualified_name
    assert retrieved.project_qualified_name == sub_project.qualified_name
    assert retrieved.top_level_project_qualified_name == project.qualified_name


def test_published_datasource(
    client: AtlanClient, connection: Connection, project, published_datasource
):
    retrieved = _assert_retrieved(
        client,
        published_datasource,
        TableauDatasource,
        connection,
        f"{SITE_ID}/{PROJECT_ID}/{PUBLISHED_DS_ID}",
    )
    assert retrieved.is_published is True
    assert retrieved.project.guid == project.guid
    assert not retrieved.workbook


def test_embedded_datasource(
    client: AtlanClient,
    connection: Connection,
    sub_project,
    workbook,
    embedded_datasource,
):
    retrieved = _assert_retrieved(
        client,
        embedded_datasource,
        TableauDatasource,
        connection,
        f"{SITE_ID}/{SUB_PROJECT_ID}/{WORKBOOK_ID}/{EMBEDDED_DS_ID}",
    )
    assert retrieved.is_published is False
    assert retrieved.project.guid == sub_project.guid
    assert retrieved.workbook.guid == workbook.guid
    assert retrieved.workbook_qualified_name == workbook.qualified_name


def test_dashboard(
    client: AtlanClient, connection: Connection, project, workbook, dashboard
):
    retrieved = _assert_retrieved(
        client,
        dashboard,
        TableauDashboard,
        connection,
        f"{SITE_ID}/{SUB_PROJECT_ID}/{WORKBOOK_ID}/{DASHBOARD_ID}",
    )
    assert retrieved.workbook.guid == workbook.guid
    assert retrieved.workbook_qualified_name == workbook.qualified_name
    assert retrieved.top_level_project_qualified_name == project.qualified_name


def test_worksheet(
    client: AtlanClient, connection: Connection, project, workbook, worksheet
):
    retrieved = _assert_retrieved(
        client,
        worksheet,
        TableauWorksheet,
        connection,
        f"{SITE_ID}/{SUB_PROJECT_ID}/{WORKBOOK_ID}/{WORKSHEET_ID}",
    )
    assert retrieved.workbook.guid == workbook.guid
    assert retrieved.workbook_qualified_name == workbook.qualified_name
    assert retrieved.top_level_project_qualified_name == project.qualified_name


def test_datasource_field(
    client: AtlanClient,
    connection: Connection,
    published_datasource,
    datasource_field,
):
    retrieved = _assert_retrieved(
        client,
        datasource_field,
        TableauDatasourceField,
        connection,
        f"{SITE_ID}/{PROJECT_ID}/{PUBLISHED_DS_ID}/{DS_FIELD_ID}",
    )
    assert retrieved.datasource.guid == published_datasource.guid
    assert retrieved.datasource_qualified_name == published_datasource.qualified_name
    assert not retrieved.workbook_qualified_name


def test_calculated_field(
    client: AtlanClient,
    connection: Connection,
    workbook,
    embedded_datasource,
    calculated_field,
):
    retrieved = _assert_retrieved(
        client,
        calculated_field,
        TableauCalculatedField,
        connection,
        f"{SITE_ID}/{SUB_PROJECT_ID}/{WORKBOOK_ID}/{EMBEDDED_DS_ID}/{CALC_FIELD_ID}",
    )
    assert retrieved.datasource.guid == embedded_datasource.guid
    assert retrieved.datasource_qualified_name == embedded_datasource.qualified_name
    assert retrieved.workbook_qualified_name == workbook.qualified_name


def test_worksheet_field(
    client: AtlanClient,
    connection: Connection,
    workbook,
    worksheet,
    worksheet_field,
):
    retrieved = _assert_retrieved(
        client,
        worksheet_field,
        TableauWorksheetField,
        connection,
        f"{SITE_ID}/{SUB_PROJECT_ID}/{WORKBOOK_ID}/{WORKSHEET_ID}/{DS_FIELD_ID}",
    )
    assert retrieved.tableau_worksheet.guid == worksheet.guid
    assert retrieved.tableau_worksheet_qualified_name == worksheet.qualified_name
    assert retrieved.tableau_workbook_qualified_name == workbook.qualified_name


def test_dashboard_field(
    client: AtlanClient,
    connection: Connection,
    dashboard,
    dashboard_field,
):
    retrieved = _assert_retrieved(
        client,
        dashboard_field,
        TableauDashboardField,
        connection,
        f"{SITE_ID}/{SUB_PROJECT_ID}/{WORKBOOK_ID}/{DASHBOARD_ID}/{DS_FIELD_ID}",
    )
    assert retrieved.tableau_dashboard.guid == dashboard.guid
    assert retrieved.tableau_dashboard_qualified_name == dashboard.qualified_name
