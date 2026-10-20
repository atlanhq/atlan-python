# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the TableauDatasourceField creator in pyatlan_v9.

The expected qualifiedNames are the literal strings atlan-tableau-app emits
(FND-3849 analysis) for fields of published and embedded datasources.
"""

import pytest

from pyatlan_v9.model import TableauDatasourceField
from tests_v9.unit.model.constants import (
    TABLEAU_CONNECTION_QUALIFIED_NAME,
    TABLEAU_EMBEDDED_DATASOURCE_QUALIFIED_NAME,
    TABLEAU_FIELD_ID,
    TABLEAU_NAME,
    TABLEAU_OTHER_SITE_PROJECT_QUALIFIED_NAME,
    TABLEAU_PROJECT_QUALIFIED_NAME,
    TABLEAU_PUBLISHED_DATASOURCE_QUALIFIED_NAME,
    TABLEAU_SITE_QUALIFIED_NAME,
    TABLEAU_WORKBOOK_QUALIFIED_NAME,
)

APP_PUBLISHED_QUALIFIED_NAME = (
    "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
    "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c"
    "/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a"
)
APP_EMBEDDED_QUALIFIED_NAME = (
    "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
    "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
    "/2b3c4d5e-5555-4f6a-8b7c-8d9e0f1a2b3c/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a"
)
REQUIRED = dict(
    datasource_qualified_name=TABLEAU_PUBLISHED_DATASOURCE_QUALIFIED_NAME,
    field_id=TABLEAU_FIELD_ID,
)


@pytest.mark.parametrize(
    "datasource_qn, expected_qn",
    [
        (TABLEAU_PUBLISHED_DATASOURCE_QUALIFIED_NAME, APP_PUBLISHED_QUALIFIED_NAME),
        (TABLEAU_EMBEDDED_DATASOURCE_QUALIFIED_NAME, APP_EMBEDDED_QUALIFIED_NAME),
    ],
    ids=["published", "embedded"],
)
def test_creator_matches_app_qualified_name(datasource_qn, expected_qn):
    sut = TableauDatasourceField.creator(
        name=TABLEAU_NAME,
        datasource_qualified_name=datasource_qn,
        field_id=TABLEAU_FIELD_ID,
    )

    assert sut.qualified_name == expected_qn
    assert sut.name == TABLEAU_NAME
    assert sut.connection_qualified_name == TABLEAU_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "tableau"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = TableauDatasourceField.create(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_PUBLISHED_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": TABLEAU_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        TableauDatasourceField.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        TableauDatasourceField.creator(**args)


@pytest.mark.parametrize(
    "bad_datasource_qn",
    [
        TABLEAU_PROJECT_QUALIFIED_NAME,
        f"{TABLEAU_EMBEDDED_DATASOURCE_QUALIFIED_NAME}/x",
    ],
)
def test_creator_rejects_malformed_datasource_qualified_name(bad_datasource_qn):
    with pytest.raises(ValueError, match="Invalid datasource_qualified_name"):
        TableauDatasourceField.creator(
            name=TABLEAU_NAME,
            **{**REQUIRED, "datasource_qualified_name": bad_datasource_qn},
        )


def test_published_datasource_field_sets_ancestors():
    sut = TableauDatasourceField.creator(name=TABLEAU_NAME, **REQUIRED)

    assert sut.datasource.qualified_name == TABLEAU_PUBLISHED_DATASOURCE_QUALIFIED_NAME
    assert sut.datasource_qualified_name == TABLEAU_PUBLISHED_DATASOURCE_QUALIFIED_NAME
    assert sut.project_qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert sut.top_level_project_qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert sut.site_qualified_name == TABLEAU_SITE_QUALIFIED_NAME
    assert not sut.workbook_qualified_name


def test_embedded_datasource_field_sets_workbook():
    sut = TableauDatasourceField.creator(
        name=TABLEAU_NAME,
        datasource_qualified_name=TABLEAU_EMBEDDED_DATASOURCE_QUALIFIED_NAME,
        field_id=TABLEAU_FIELD_ID,
    )

    assert sut.datasource.qualified_name == TABLEAU_EMBEDDED_DATASOURCE_QUALIFIED_NAME
    assert sut.workbook_qualified_name == TABLEAU_WORKBOOK_QUALIFIED_NAME
    assert sut.project_qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert sut.site_qualified_name == TABLEAU_SITE_QUALIFIED_NAME


def test_creator_rejects_top_level_project_from_other_site():
    with pytest.raises(ValueError, match="Invalid top_level_project_qualified_name"):
        TableauDatasourceField.creator(
            name=TABLEAU_NAME,
            **REQUIRED,
            top_level_project_qualified_name=TABLEAU_OTHER_SITE_PROJECT_QUALIFIED_NAME,
        )


def test_updater():
    sut = TableauDatasourceField.updater(
        qualified_name=APP_PUBLISHED_QUALIFIED_NAME, name=TABLEAU_NAME
    )

    assert sut.qualified_name == APP_PUBLISHED_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME


def test_trim_to_required():
    sut = TableauDatasourceField.updater(
        qualified_name=APP_PUBLISHED_QUALIFIED_NAME, name=TABLEAU_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_PUBLISHED_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
