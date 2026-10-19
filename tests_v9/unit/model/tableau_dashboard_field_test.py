# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the TableauDashboardField creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-tableau-app emits (FND-3849
analysis), so a creator change that would re-key existing fields fails here.
"""

import pytest

from pyatlan_v9.model import TableauDashboardField
from tests_v9.unit.model.constants import (
    TABLEAU_CONNECTION_QUALIFIED_NAME,
    TABLEAU_DASHBOARD_QUALIFIED_NAME,
    TABLEAU_FIELD_ID,
    TABLEAU_NAME,
    TABLEAU_OTHER_SITE_PROJECT_QUALIFIED_NAME,
    TABLEAU_PROJECT_QUALIFIED_NAME,
    TABLEAU_SITE_QUALIFIED_NAME,
)

APP_QUALIFIED_NAME = (
    "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
    "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d/7e8f9a0b-4444-4c1d-8e2f-3a4b5c6d7e8f"
    "/3c4d5e6f-6666-4a7b-9c8d-9e0f1a2b3c4d/6f7a8b9c-8888-4d0e-9f1a-2b3c4d5e6f7a"
)
REQUIRED = dict(
    dashboard_qualified_name=TABLEAU_DASHBOARD_QUALIFIED_NAME,
    field_id=TABLEAU_FIELD_ID,
)


def test_creator_matches_app_qualified_name():
    sut = TableauDashboardField.creator(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
    assert sut.connection_qualified_name == TABLEAU_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "tableau"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = TableauDashboardField.create(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": TABLEAU_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        TableauDashboardField.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        TableauDashboardField.creator(**args)


def test_creator_rejects_malformed_dashboard_qualified_name():
    with pytest.raises(ValueError, match="Invalid dashboard_qualified_name"):
        TableauDashboardField.creator(
            name=TABLEAU_NAME,
            **{
                **REQUIRED,
                "dashboard_qualified_name": f"{TABLEAU_DASHBOARD_QUALIFIED_NAME}/x",
            },
        )


def test_creator_sets_tableau_prefixed_ancestors():
    sut = TableauDashboardField.creator(name=TABLEAU_NAME, **REQUIRED)

    assert sut.tableau_dashboard.qualified_name == TABLEAU_DASHBOARD_QUALIFIED_NAME
    assert sut.tableau_dashboard_qualified_name == TABLEAU_DASHBOARD_QUALIFIED_NAME
    assert sut.tableau_project_qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    assert (
        sut.tableau_top_level_project_qualified_name == TABLEAU_PROJECT_QUALIFIED_NAME
    )
    assert sut.tableau_site_qualified_name == TABLEAU_SITE_QUALIFIED_NAME


def test_creator_rejects_top_level_project_from_other_site():
    with pytest.raises(ValueError, match="Invalid top_level_project_qualified_name"):
        TableauDashboardField.creator(
            name=TABLEAU_NAME,
            **REQUIRED,
            top_level_project_qualified_name=TABLEAU_OTHER_SITE_PROJECT_QUALIFIED_NAME,
        )


def test_updater():
    sut = TableauDashboardField.updater(
        qualified_name=APP_QUALIFIED_NAME, name=TABLEAU_NAME
    )

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME


def test_trim_to_required():
    sut = TableauDashboardField.updater(
        qualified_name=APP_QUALIFIED_NAME, name=TABLEAU_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
