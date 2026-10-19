# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the PowerBIDatasource creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-powerbi-app emits
(FND-3852 analysis); datasources need no dataset, since the app emits ones used only by dataflows.
"""

import pytest

from pyatlan_v9.model import PowerBIDatasource
from tests_v9.unit.model.constants import (
    POWERBI_CONNECTION_QUALIFIED_NAME,
    POWERBI_NAME,
)

APP_QUALIFIED_NAME = "default/powerbi/1712345678/7b8c9d0e-4444-4f1a-8b2c-3d4e5f6a7b8c"
REQUIRED = dict(
    connection_qualified_name=POWERBI_CONNECTION_QUALIFIED_NAME,
    datasource_id="7b8c9d0e-4444-4f1a-8b2c-3d4e5f6a7b8c",
)


def test_creator_matches_app_qualified_name():
    sut = PowerBIDatasource.creator(name=POWERBI_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME
    assert sut.connection_qualified_name == POWERBI_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "powerbi"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    assert not sut.datasets
    sut.validate(for_creation=True)


def test_create_alias():
    sut = PowerBIDatasource.create(name=POWERBI_NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": POWERBI_NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        PowerBIDatasource.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        PowerBIDatasource.creator(**args)


def test_updater():
    sut = PowerBIDatasource.updater(
        qualified_name=APP_QUALIFIED_NAME, name=POWERBI_NAME
    )

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME


def test_trim_to_required():
    sut = PowerBIDatasource.updater(
        qualified_name=APP_QUALIFIED_NAME, name=POWERBI_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == POWERBI_NAME
