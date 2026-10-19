# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the PowerBIWorkspace creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-powerbi-app emits
(FND-3852 analysis).
"""

import pytest

from pyatlan_v9.model import PowerBIWorkspace
from tests_v9.unit.model.constants import (
    POWERBI_CONNECTION_QUALIFIED_NAME,
    POWERBI_NAME,
)

APP_QUALIFIED_NAME = "default/powerbi/1712345678/0f1e2d3c-4b5a-4978-8a9b-0c1d2e3f4a5b"
REQUIRED = dict(
    connection_qualified_name=POWERBI_CONNECTION_QUALIFIED_NAME,
    workspace_id="0f1e2d3c-4b5a-4978-8a9b-0c1d2e3f4a5b",
)


def test_creator_matches_app_qualified_name():
    sut = PowerBIWorkspace.creator(name=POWERBI_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME
    assert sut.connection_qualified_name == POWERBI_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "powerbi"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = PowerBIWorkspace.create(name=POWERBI_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": POWERBI_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        PowerBIWorkspace.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        PowerBIWorkspace.creator(**args)


def test_updater():
    sut = PowerBIWorkspace.updater(qualified_name=APP_QUALIFIED_NAME, name=POWERBI_NAME)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME


def test_trim_to_required():
    sut = PowerBIWorkspace.updater(
        qualified_name=APP_QUALIFIED_NAME, name=POWERBI_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME
