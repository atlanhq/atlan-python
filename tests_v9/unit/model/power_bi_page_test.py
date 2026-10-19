# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the PowerBIPage creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-powerbi-app emits
(FND-3852 analysis).
"""

import pytest

from pyatlan_v9.model import PowerBIPage
from tests_v9.unit.model.constants import (
    POWERBI_CONNECTION_QUALIFIED_NAME,
    POWERBI_REPORT_QUALIFIED_NAME,
    POWERBI_WORKSPACE_QUALIFIED_NAME,
)

APP_QUALIFIED_NAME = (
    "default/powerbi/1712345678/0f1e2d3c-4b5a-4978-8a9b-0c1d2e3f4a5b"
    "/5e6f7a8b-2222-4c3d-9e4f-5a6b7c8d9e0f/ReportSection1"
)
NAME = "Overview"
REQUIRED = dict(
    report_qualified_name=POWERBI_REPORT_QUALIFIED_NAME,
    page_id="ReportSection1",
)


def test_creator_matches_app_qualified_name():
    sut = PowerBIPage.creator(name=NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == NAME
    assert sut.connection_qualified_name == POWERBI_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "powerbi"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    assert sut.workspace_qualified_name == POWERBI_WORKSPACE_QUALIFIED_NAME
    assert sut.report_qualified_name == POWERBI_REPORT_QUALIFIED_NAME
    assert sut.report.unique_attributes == {
        "qualifiedName": POWERBI_REPORT_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_create_alias():
    sut = PowerBIPage.create(name=NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        PowerBIPage.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        PowerBIPage.creator(**args)


@pytest.mark.parametrize(
    "bad_qualified_name",
    [
        POWERBI_WORKSPACE_QUALIFIED_NAME,
        f"{POWERBI_REPORT_QUALIFIED_NAME}/x",
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(bad_qualified_name):
    with pytest.raises(ValueError, match="report_qualified_name is invalid"):
        PowerBIPage.creator(
            name=NAME, **{**REQUIRED, "report_qualified_name": bad_qualified_name}
        )


def test_updater():
    sut = PowerBIPage.updater(qualified_name=APP_QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == NAME


def test_trim_to_required():
    sut = PowerBIPage.updater(
        qualified_name=APP_QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == NAME
