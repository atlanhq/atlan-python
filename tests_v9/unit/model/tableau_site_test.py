# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the TableauSite creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-tableau-app emits (FND-3849
analysis), so a creator change that would re-key existing sites fails here.
"""

import pytest

from pyatlan_v9.model import TableauSite
from tests_v9.unit.model.constants import (
    TABLEAU_CONNECTION_QUALIFIED_NAME,
    TABLEAU_NAME,
    TABLEAU_SITE_ID,
    TABLEAU_SITE_QUALIFIED_NAME,
)

APP_QUALIFIED_NAME = "default/tableau/1712345678/a1b2c3d4-0000-4e5f-8a9b-0c1d2e3f4a5b"
REQUIRED = dict(
    connection_qualified_name=TABLEAU_CONNECTION_QUALIFIED_NAME,
    site_id=TABLEAU_SITE_ID,
)


def test_creator_matches_app_qualified_name():
    sut = TableauSite.creator(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
    assert sut.connection_qualified_name == TABLEAU_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "tableau"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = TableauSite.create(name=TABLEAU_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": TABLEAU_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        TableauSite.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        TableauSite.creator(**args)


def test_creator_rejects_malformed_connection_qualified_name():
    with pytest.raises(ValueError, match="Invalid connection_qualified_name"):
        TableauSite.creator(
            name=TABLEAU_NAME,
            **{**REQUIRED, "connection_qualified_name": TABLEAU_SITE_QUALIFIED_NAME},
        )


def test_updater():
    sut = TableauSite.updater(qualified_name=APP_QUALIFIED_NAME, name=TABLEAU_NAME)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME


def test_trim_to_required():
    sut = TableauSite.updater(
        qualified_name=APP_QUALIFIED_NAME, name=TABLEAU_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == TABLEAU_NAME
