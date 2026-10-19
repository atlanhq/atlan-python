# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the TableauDatasource creator in pyatlan_v9.

The expected qualifiedNames are the literal strings atlan-tableau-app emits
(FND-3849 analysis) for published and embedded datasources.
"""

import pytest

from pyatlan_v9.model import TableauDatasource
from tests_v9.unit.model.constants import (
    TABLEAU_CONNECTION_QUALIFIED_NAME,
    TABLEAU_DATASOURCE_ID,
    TABLEAU_EMBEDDED_DATASOURCE_QUALIFIED_NAME,
    TABLEAU_NAME,
    TABLEAU_OTHER_SITE_PROJECT_QUALIFIED_NAME,
    TABLEAU_PARENT_PROJECT_QUALIFIED_NAME,
    TABLEAU_PROJECT_QUALIFIED_NAME,
    TABLEAU_SITE_QUALIFIED_NAME,
    TABLEAU_WORKBOOK_ID,
    TABLEAU_WORKBOOK_QUALIFIED_NAME,
)

APP_PUBLISHED_QUALIFIED_NAME = (
    "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
    "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c"
)
APP_EMBEDDED_QUALIFIED_NAME = (
    "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
    "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
    "/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c"
)
REQUIRED = dict(
    project_qualified_name=TABLEAU_PROJECT_QUALIFIED_NAME,
    datasource_id=TABLEAU_DATASOURCE_ID,
)


@pytest.mark.parametrize(
    "extra, expected_qn",
    [
        ({}, APP_PUBLISHED_QUALIFIED_NAME),
        (
            {"workbook_qualified_name": TABLEAU_WORKBOOK_QUALIFIED_NAME},
            APP_EMBEDDED_QUALIFIED_NAME,
        ),
    ],
    ids=["published", "embedded"],
)
def test_creator_matches_app_qualified_name(extra, expected_qn):
    sut = TableauDatasource.creator(name=TABLEAU_NAME, **REQUIRED, **extra)

    assert sut.qualified_name == expected_qn
    assert sut.name == TABLEAU_NAME
    assert sut.connection_qualified_name == TABLEAU_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "tableau"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = TableauDatasource.create(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_PUBLISHED_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": TABLEAU_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        TableauDatasource.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        TableauDatasource.creator(**args)


def test_creator_rejects_malformed_project_qualified_name():
    with pytest.raises(ValueError, match="Invalid project_qualified_name"):
        TableauDatasource.creator(
            name=TABLEAU_NAME,
            **{**REQUIRED, "project_qualified_name": TABLEAU_WORKBOOK_QUALIFIED_NAME},
        )


def test_published_datasource():
    sut = TableauDatasource.creator(name=TABLEAU_NAME, **REQUIRED)

    assert sut.is_published is True
    assert sut.project.qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert sut.project_qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert sut.top_level_project_qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert sut.site_qualified_name == TABLEAU_SITE_QUALIFIED_NAME
    assert not sut.workbook
    assert not sut.workbook_qualified_name


def test_embedded_datasource_links_project_and_workbook():
    sut = TableauDatasource.creator(
        name=TABLEAU_NAME,
        **REQUIRED,
        workbook_qualified_name=TABLEAU_WORKBOOK_QUALIFIED_NAME,
    )

    assert sut.qualified_name == TABLEAU_EMBEDDED_DATASOURCE_QUALIFIED_NAME
    assert sut.is_published is False
    assert sut.project.qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert sut.workbook.qualified_name == TABLEAU_WORKBOOK_QUALIFIED_NAME
    assert sut.workbook_qualified_name == TABLEAU_WORKBOOK_QUALIFIED_NAME


def test_embedded_datasource_rejects_workbook_in_other_project():
    with pytest.raises(ValueError, match="Invalid workbook_qualified_name"):
        TableauDatasource.creator(
            name=TABLEAU_NAME,
            **REQUIRED,
            workbook_qualified_name=(
                f"{TABLEAU_PARENT_PROJECT_QUALIFIED_NAME}/{TABLEAU_WORKBOOK_ID}"
            ),
        )


def test_creator_rejects_top_level_project_from_other_site():
    with pytest.raises(ValueError, match="Invalid top_level_project_qualified_name"):
        TableauDatasource.creator(
            name=TABLEAU_NAME,
            **REQUIRED,
            top_level_project_qualified_name=TABLEAU_OTHER_SITE_PROJECT_QUALIFIED_NAME,
        )


def test_updater():
    sut = TableauDatasource.updater(
        qualified_name=APP_PUBLISHED_QUALIFIED_NAME, name=TABLEAU_NAME
    )

    assert sut.qualified_name == APP_PUBLISHED_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME


def test_trim_to_required():
    sut = TableauDatasource.updater(
        qualified_name=APP_PUBLISHED_QUALIFIED_NAME, name=TABLEAU_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_PUBLISHED_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
