# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the PowerBIReport creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-powerbi-app emits
(FND-3852 analysis).
"""

import pytest

from pyatlan_v9.model import PowerBIReport
from tests_v9.unit.model.constants import (
    POWERBI_CONNECTION_QUALIFIED_NAME,
    POWERBI_NAME,
    POWERBI_WORKSPACE_QUALIFIED_NAME,
)

APP_QUALIFIED_NAME = (
    "default/powerbi/1712345678/0f1e2d3c-4b5a-4978-8a9b-0c1d2e3f4a5b"
    "/5e6f7a8b-2222-4c3d-9e4f-5a6b7c8d9e0f"
)
REQUIRED = dict(
    workspace_qualified_name=POWERBI_WORKSPACE_QUALIFIED_NAME,
    report_id="5e6f7a8b-2222-4c3d-9e4f-5a6b7c8d9e0f",
)


def test_creator_matches_app_qualified_name():
    sut = PowerBIReport.creator(name=POWERBI_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME
    assert sut.connection_qualified_name == POWERBI_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "powerbi"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    assert sut.workspace_qualified_name == POWERBI_WORKSPACE_QUALIFIED_NAME
    assert sut.workspace.unique_attributes == {
        "qualifiedName": POWERBI_WORKSPACE_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_create_alias():
    sut = PowerBIReport.create(name=POWERBI_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": POWERBI_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        PowerBIReport.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        PowerBIReport.creator(**args)


@pytest.mark.parametrize(
    "bad_qualified_name",
    [
        POWERBI_CONNECTION_QUALIFIED_NAME,
        f"{POWERBI_CONNECTION_QUALIFIED_NAME}/",
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(bad_qualified_name):
    with pytest.raises(ValueError, match="workspace_qualified_name is invalid"):
        PowerBIReport.creator(
            name=POWERBI_NAME,
            **{**REQUIRED, "workspace_qualified_name": bad_qualified_name},
        )


def test_updater():
    sut = PowerBIReport.updater(qualified_name=APP_QUALIFIED_NAME, name=POWERBI_NAME)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME


def test_trim_to_required():
    sut = PowerBIReport.updater(
        qualified_name=APP_QUALIFIED_NAME, name=POWERBI_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME
