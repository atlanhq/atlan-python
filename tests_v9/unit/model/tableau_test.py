# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Tableau creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-tableau-app emits today
(FND-3838 census, FND-3849 analysis), so a creator change that would re-key existing
Tableau assets fails here.
"""

import pytest

from pyatlan_v9.model import (
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

CONNECTION_QN = "default/tableau/1712345678"
SITE_ID = "a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
PROJECT_ID = "5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d"
PARENT_PROJECT_ID = "0f1e2d3c-2222-4b4a-8c9d-0e1f2a3b4c5d"
TOP_PROJECT_ID = "9a8b7c6d-3333-4e4f-8a1b-2c3d4e5f6a7b"
WORKBOOK_ID = "7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
DATASOURCE_ID = "2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c"
DASHBOARD_ID = "3c4d5e6f-6666-4a7b-9c8d-9e0f1a2b3c4d"
WORKSHEET_ID = "4d5e6f7a-7777-4b8c-8d9e-0f1a2b3c4d5e"
FIELD_ID = "6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a"

SITE_QN = f"{CONNECTION_QN}/{SITE_ID}"
PROJECT_QN = f"{SITE_QN}/{PROJECT_ID}"
PARENT_PROJECT_QN = f"{SITE_QN}/{PARENT_PROJECT_ID}"
TOP_PROJECT_QN = f"{SITE_QN}/{TOP_PROJECT_ID}"
WORKBOOK_QN = f"{PROJECT_QN}/{WORKBOOK_ID}"
PUBLISHED_DS_QN = f"{PROJECT_QN}/{DATASOURCE_ID}"
EMBEDDED_DS_QN = f"{WORKBOOK_QN}/{DATASOURCE_ID}"
DASHBOARD_QN = f"{WORKBOOK_QN}/{DASHBOARD_ID}"
WORKSHEET_QN = f"{WORKBOOK_QN}/{WORKSHEET_ID}"

NAME = "Revenue"

# (type, required creator kwargs, the literal qualifiedName atlan-tableau-app emits)
ALL_TYPES = [
    (
        TableauSite,
        dict(connection_qualified_name=CONNECTION_QN, site_id=SITE_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b",
    ),
    (
        TableauProject,
        dict(site_qualified_name=SITE_QN, project_id=PROJECT_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d",
    ),
    (
        TableauWorkbook,
        dict(project_qualified_name=PROJECT_QN, workbook_id=WORKBOOK_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f",
    ),
    (
        TableauDatasource,
        dict(project_qualified_name=PROJECT_QN, datasource_id=DATASOURCE_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c",
    ),
    (
        TableauDashboard,
        dict(workbook_qualified_name=WORKBOOK_QN, dashboard_id=DASHBOARD_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
        "/3c4d5e6f-6666-4a7b-9c8d-9e0f1a2b3c4d",
    ),
    (
        TableauWorksheet,
        dict(workbook_qualified_name=WORKBOOK_QN, worksheet_id=WORKSHEET_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
        "/4d5e6f7a-7777-4b8c-8d9e-0f1a2b3c4d5e",
    ),
    (
        TableauDatasourceField,
        dict(datasource_qualified_name=PUBLISHED_DS_QN, field_id=FIELD_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c"
        "/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a",
    ),
    (
        TableauCalculatedField,
        dict(datasource_qualified_name=PUBLISHED_DS_QN, field_id=FIELD_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c"
        "/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a",
    ),
    (
        TableauWorksheetField,
        dict(worksheet_qualified_name=WORKSHEET_QN, field_id=FIELD_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
        "/4d5e6f7a-7777-4b8c-8d9e-0f1a2b3c4d5e/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a",
    ),
    (
        TableauDashboardField,
        dict(dashboard_qualified_name=DASHBOARD_QN, field_id=FIELD_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
        "/3c4d5e6f-6666-4a7b-9c8d-9e0f1a2b3c4d/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a",
    ),
]
IDS = [t[0].__name__ for t in ALL_TYPES]

# Embedded datasources (and their fields) put the workbook id between project and datasource.
EMBEDDED_VARIANTS = [
    (
        TableauDatasource,
        dict(
            project_qualified_name=PROJECT_QN,
            datasource_id=DATASOURCE_ID,
            workbook_qualified_name=WORKBOOK_QN,
        ),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
        "/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c",
    ),
    (
        TableauDatasourceField,
        dict(datasource_qualified_name=EMBEDDED_DS_QN, field_id=FIELD_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
        "/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a",
    ),
    (
        TableauCalculatedField,
        dict(datasource_qualified_name=EMBEDDED_DS_QN, field_id=FIELD_ID),
        "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
        "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
        "/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a",
    ),
]
EMBEDDED_IDS = [t[0].__name__ for t in EMBEDDED_VARIANTS]


@pytest.mark.parametrize(
    "asset_type, kwargs, expected_qn",
    ALL_TYPES + EMBEDDED_VARIANTS,
    ids=IDS + [f"{i}-embedded" for i in EMBEDDED_IDS],
)
def test_creator_matches_app_qualified_name(asset_type, kwargs, expected_qn):
    sut = asset_type.creator(name=NAME, **kwargs)

    assert sut.qualified_name == expected_qn
    assert sut.name == NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "tableau"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


@pytest.mark.parametrize("asset_type, kwargs, expected_qn", ALL_TYPES, ids=IDS)
def test_create_alias(asset_type, kwargs, expected_qn):
    assert asset_type.create(name=NAME, **kwargs).qualified_name == expected_qn


@pytest.mark.parametrize("asset_type, kwargs, _", ALL_TYPES, ids=IDS)
def test_creator_rejects_missing_or_blank_inputs(asset_type, kwargs, _):
    for param in ["name", *kwargs]:
        args = {"name": NAME, **kwargs}
        args[param] = None
        with pytest.raises(ValueError, match=f"{param} is required"):
            asset_type.creator(**args)
        args[param] = "  "
        with pytest.raises(ValueError, match=f"{param} cannot be blank"):
            asset_type.creator(**args)


def test_top_level_project_has_site_and_no_parent():
    sut = TableauProject.creator(
        name=NAME, site_qualified_name=SITE_QN, project_id=PROJECT_ID
    )

    assert sut.site.qualified_name == SITE_QN
    assert sut.site_qualified_name == SITE_QN
    assert sut.is_top_level_project is True
    assert not sut.parent_project
    assert not sut.top_level_project_qualified_name


def test_nested_project_stays_flat_and_sets_parent():
    sut = TableauProject.creator(
        name=NAME,
        site_qualified_name=SITE_QN,
        project_id=PROJECT_ID,
        parent_project_qualified_name=PARENT_PROJECT_QN,
        top_level_project_qualified_name=TOP_PROJECT_QN,
    )

    assert sut.qualified_name == PROJECT_QN
    assert sut.is_top_level_project is False
    assert sut.parent_project.qualified_name == PARENT_PROJECT_QN
    assert sut.top_level_project_qualified_name == TOP_PROJECT_QN


def test_nested_project_top_level_defaults_to_parent():
    sut = TableauProject.creator(
        name=NAME,
        site_qualified_name=SITE_QN,
        project_id=PROJECT_ID,
        parent_project_qualified_name=PARENT_PROJECT_QN,
    )

    assert sut.top_level_project_qualified_name == PARENT_PROJECT_QN


def test_project_rejects_top_level_without_parent():
    with pytest.raises(ValueError, match="requires parent_project_qualified_name"):
        TableauProject.creator(
            name=NAME,
            site_qualified_name=SITE_QN,
            project_id=PROJECT_ID,
            top_level_project_qualified_name=TOP_PROJECT_QN,
        )


def test_workbook_sets_project_ancestors():
    sut = TableauWorkbook.creator(
        name=NAME, project_qualified_name=PROJECT_QN, workbook_id=WORKBOOK_ID
    )

    assert sut.project.qualified_name == PROJECT_QN
    assert sut.site_qualified_name == SITE_QN
    assert sut.project_qualified_name == PROJECT_QN
    assert sut.top_level_project_qualified_name == PROJECT_QN


def test_top_level_project_override_is_kept():
    sut = TableauWorkbook.creator(
        name=NAME,
        project_qualified_name=PROJECT_QN,
        workbook_id=WORKBOOK_ID,
        top_level_project_qualified_name=TOP_PROJECT_QN,
    )

    assert sut.top_level_project_qualified_name == TOP_PROJECT_QN


def test_published_datasource():
    sut = TableauDatasource.creator(
        name=NAME, project_qualified_name=PROJECT_QN, datasource_id=DATASOURCE_ID
    )

    assert sut.is_published is True
    assert sut.project.qualified_name == PROJECT_QN
    assert sut.project_qualified_name == PROJECT_QN
    assert sut.site_qualified_name == SITE_QN
    assert not sut.workbook
    assert not sut.workbook_qualified_name


def test_embedded_datasource_links_project_and_workbook():
    sut = TableauDatasource.creator(
        name=NAME,
        project_qualified_name=PROJECT_QN,
        datasource_id=DATASOURCE_ID,
        workbook_qualified_name=WORKBOOK_QN,
    )

    assert sut.qualified_name == EMBEDDED_DS_QN
    assert sut.is_published is False
    assert sut.project.qualified_name == PROJECT_QN
    assert sut.workbook.qualified_name == WORKBOOK_QN
    assert sut.workbook_qualified_name == WORKBOOK_QN


def test_embedded_datasource_rejects_workbook_in_other_project():
    with pytest.raises(ValueError, match="Invalid workbook_qualified_name"):
        TableauDatasource.creator(
            name=NAME,
            project_qualified_name=PROJECT_QN,
            datasource_id=DATASOURCE_ID,
            workbook_qualified_name=f"{PARENT_PROJECT_QN}/{WORKBOOK_ID}",
        )


@pytest.mark.parametrize("asset_type", [TableauDashboard, TableauWorksheet])
def test_workbook_children_set_ancestors(asset_type):
    kwargs = next(k for t, k, _ in ALL_TYPES if t is asset_type)
    sut = asset_type.creator(name=NAME, **kwargs)

    assert sut.workbook.qualified_name == WORKBOOK_QN
    assert sut.workbook_qualified_name == WORKBOOK_QN
    assert sut.project_qualified_name == PROJECT_QN
    assert sut.top_level_project_qualified_name == PROJECT_QN
    assert sut.site_qualified_name == SITE_QN


@pytest.mark.parametrize("asset_type", [TableauDatasourceField, TableauCalculatedField])
def test_published_datasource_field_sets_ancestors(asset_type):
    sut = asset_type.creator(
        name=NAME, datasource_qualified_name=PUBLISHED_DS_QN, field_id=FIELD_ID
    )

    assert sut.datasource.qualified_name == PUBLISHED_DS_QN
    assert sut.datasource_qualified_name == PUBLISHED_DS_QN
    assert sut.project_qualified_name == PROJECT_QN
    assert sut.top_level_project_qualified_name == PROJECT_QN
    assert sut.site_qualified_name == SITE_QN
    assert not sut.workbook_qualified_name


@pytest.mark.parametrize("asset_type", [TableauDatasourceField, TableauCalculatedField])
def test_embedded_datasource_field_sets_workbook(asset_type):
    sut = asset_type.creator(
        name=NAME, datasource_qualified_name=EMBEDDED_DS_QN, field_id=FIELD_ID
    )

    assert sut.datasource.qualified_name == EMBEDDED_DS_QN
    assert sut.workbook_qualified_name == WORKBOOK_QN
    assert sut.project_qualified_name == PROJECT_QN
    assert sut.site_qualified_name == SITE_QN


def test_worksheet_field_sets_tableau_prefixed_ancestors():
    sut = TableauWorksheetField.creator(
        name=NAME, worksheet_qualified_name=WORKSHEET_QN, field_id=FIELD_ID
    )

    assert sut.tableau_worksheet.qualified_name == WORKSHEET_QN
    assert sut.tableau_worksheet_qualified_name == WORKSHEET_QN
    assert sut.tableau_workbook_qualified_name == WORKBOOK_QN
    assert sut.tableau_project_qualified_name == PROJECT_QN
    assert sut.tableau_top_level_project_qualified_name == PROJECT_QN
    assert sut.tableau_site_qualified_name == SITE_QN


def test_dashboard_field_sets_tableau_prefixed_ancestors():
    sut = TableauDashboardField.creator(
        name=NAME, dashboard_qualified_name=DASHBOARD_QN, field_id=FIELD_ID
    )

    assert sut.tableau_dashboard.qualified_name == DASHBOARD_QN
    assert sut.tableau_dashboard_qualified_name == DASHBOARD_QN
    assert sut.tableau_project_qualified_name == PROJECT_QN
    assert sut.tableau_top_level_project_qualified_name == PROJECT_QN
    assert sut.tableau_site_qualified_name == SITE_QN


@pytest.mark.parametrize(
    "asset_type, parent_param, bad_parent_qn",
    [
        (TableauSite, "connection_qualified_name", SITE_QN),
        (TableauProject, "site_qualified_name", CONNECTION_QN),
        (TableauProject, "site_qualified_name", PROJECT_QN),
        (TableauWorkbook, "project_qualified_name", SITE_QN),
        (TableauWorkbook, "project_qualified_name", WORKBOOK_QN),
        (TableauDatasource, "project_qualified_name", WORKBOOK_QN),
        (TableauDashboard, "workbook_qualified_name", PROJECT_QN),
        (TableauWorksheet, "workbook_qualified_name", WORKSHEET_QN),
        (TableauDatasourceField, "datasource_qualified_name", PROJECT_QN),
        (TableauDatasourceField, "datasource_qualified_name", f"{EMBEDDED_DS_QN}/x"),
        (TableauCalculatedField, "datasource_qualified_name", PROJECT_QN),
        (TableauWorksheetField, "worksheet_qualified_name", WORKBOOK_QN),
        (TableauDashboardField, "dashboard_qualified_name", f"{DASHBOARD_QN}/x"),
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(
    asset_type, parent_param, bad_parent_qn
):
    kwargs = next(k for t, k, _ in ALL_TYPES if t is asset_type)
    with pytest.raises(ValueError, match=f"Invalid {parent_param}"):
        asset_type.creator(name=NAME, **{**kwargs, parent_param: bad_parent_qn})


@pytest.mark.parametrize("asset_type, kwargs, _", ALL_TYPES[2:], ids=IDS[2:])
def test_creator_rejects_top_level_project_from_other_site(asset_type, kwargs, _):
    other_site_project = f"{CONNECTION_QN}/other-site/{TOP_PROJECT_ID}"
    with pytest.raises(ValueError, match="Invalid top_level_project_qualified_name"):
        asset_type.creator(
            name=NAME,
            **kwargs,
            top_level_project_qualified_name=other_site_project,
        )
