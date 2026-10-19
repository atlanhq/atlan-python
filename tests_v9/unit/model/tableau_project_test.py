# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the TableauProject creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-tableau-app emits (FND-3849
analysis): projects stay flat under the site even when nested.
"""

import pytest

from pyatlan_v9.model import TableauProject
from tests_v9.unit.model.constants import (
    TABLEAU_CONNECTION_QUALIFIED_NAME,
    TABLEAU_NAME,
    TABLEAU_PARENT_PROJECT_QUALIFIED_NAME,
    TABLEAU_PROJECT_ID,
    TABLEAU_PROJECT_QUALIFIED_NAME,
    TABLEAU_SITE_QUALIFIED_NAME,
    TABLEAU_TOP_PROJECT_QUALIFIED_NAME,
)

APP_QUALIFIED_NAME = (
    "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
    "/5c6d7e8f-1111-4a2b-9c3d-4e5f6a7b8c9d"
)
REQUIRED = dict(
    site_qualified_name=TABLEAU_SITE_QUALIFIED_NAME,
    project_id=TABLEAU_PROJECT_ID,
)


def test_creator_matches_app_qualified_name():
    sut = TableauProject.creator(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
    assert sut.connection_qualified_name == TABLEAU_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "tableau"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = TableauProject.create(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": TABLEAU_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        TableauProject.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        TableauProject.creator(**args)


@pytest.mark.parametrize(
    "bad_site_qn",
    [TABLEAU_CONNECTION_QUALIFIED_NAME, TABLEAU_PROJECT_QUALIFIED_NAME],
)
def test_creator_rejects_malformed_site_qualified_name(bad_site_qn):
    with pytest.raises(ValueError, match="Invalid site_qualified_name"):
        TableauProject.creator(
            name=TABLEAU_NAME, **{**REQUIRED, "site_qualified_name": bad_site_qn}
        )


def test_top_level_project_has_site_and_no_parent():
    sut = TableauProject.creator(name=TABLEAU_NAME, **REQUIRED)

    assert sut.site.qualified_name == TABLEAU_SITE_QUALIFIED_NAME
    assert sut.site_qualified_name == TABLEAU_SITE_QUALIFIED_NAME
    assert sut.is_top_level_project is True
    assert not sut.parent_project
    assert not sut.top_level_project_qualified_name


def test_nested_project_stays_flat_and_sets_parent():
    sut = TableauProject.creator(
        name=TABLEAU_NAME,
        **REQUIRED,
        parent_project_qualified_name=TABLEAU_PARENT_PROJECT_QUALIFIED_NAME,
        top_level_project_qualified_name=TABLEAU_TOP_PROJECT_QUALIFIED_NAME,
    )

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.is_top_level_project is False
    assert sut.parent_project.qualified_name == TABLEAU_PARENT_PROJECT_QUALIFIED_NAME
    assert sut.top_level_project_qualified_name == TABLEAU_TOP_PROJECT_QUALIFIED_NAME


def test_nested_project_top_level_defaults_to_parent():
    sut = TableauProject.creator(
        name=TABLEAU_NAME,
        **REQUIRED,
        parent_project_qualified_name=TABLEAU_PARENT_PROJECT_QUALIFIED_NAME,
    )

    assert sut.top_level_project_qualified_name == TABLEAU_PARENT_PROJECT_QUALIFIED_NAME


def test_creator_rejects_top_level_without_parent():
    with pytest.raises(ValueError, match="requires parent_project_qualified_name"):
        TableauProject.creator(
            name=TABLEAU_NAME,
            **REQUIRED,
            top_level_project_qualified_name=TABLEAU_TOP_PROJECT_QUALIFIED_NAME,
        )


def test_updater():
    sut = TableauProject.updater(qualified_name=APP_QUALIFIED_NAME, name=TABLEAU_NAME)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME


def test_trim_to_required():
    sut = TableauProject.updater(
        qualified_name=APP_QUALIFIED_NAME, name=TABLEAU_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
