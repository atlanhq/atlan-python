# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the PowerBIColumn creator in pyatlan_v9.

The expected qualifiedName is the literal string atlan-powerbi-app emits
(FND-3852 analysis); columns and measures share one qualifiedName shape.
"""

import pytest

from pyatlan_v9.model import PowerBIColumn
from tests_v9.unit.model.constants import (
    POWERBI_CONNECTION_QUALIFIED_NAME,
    POWERBI_DATASET_QUALIFIED_NAME,
    POWERBI_TABLE_QUALIFIED_NAME,
    POWERBI_WORKSPACE_QUALIFIED_NAME,
)

APP_QUALIFIED_NAME = (
    "default/powerbi/1712345678/0f1e2d3c-4b5a-4978-8a9b-0c1d2e3f4a5b"
    "/9a8b7c6d-1111-4e2f-8a3b-4c5d6e7f8a9b/Sales/Revenue"
)
NAME = "Revenue"
REQUIRED = dict(
    power_bi_table_qualified_name=POWERBI_TABLE_QUALIFIED_NAME,
)


def test_creator_matches_app_qualified_name():
    sut = PowerBIColumn.creator(name=NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == NAME
    assert sut.connection_qualified_name == POWERBI_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "powerbi"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    assert sut.workspace_qualified_name == POWERBI_WORKSPACE_QUALIFIED_NAME
    assert sut.dataset_qualified_name == POWERBI_DATASET_QUALIFIED_NAME
    assert sut.power_bi_table_qualified_name == POWERBI_TABLE_QUALIFIED_NAME
    assert sut.table.unique_attributes == {
        "qualifiedName": POWERBI_TABLE_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_create_alias():
    sut = PowerBIColumn.create(name=NAME, **REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", ["name", *REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = {"name": NAME, **REQUIRED}
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        PowerBIColumn.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        PowerBIColumn.creator(**args)


@pytest.mark.parametrize(
    "bad_qualified_name",
    [
        POWERBI_DATASET_QUALIFIED_NAME,
        f"{POWERBI_WORKSPACE_QUALIFIED_NAME}//Sales",
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(bad_qualified_name):
    with pytest.raises(ValueError, match="power_bi_table_qualified_name is invalid"):
        PowerBIColumn.creator(
            name=NAME,
            **{**REQUIRED, "power_bi_table_qualified_name": bad_qualified_name},
        )


def test_creator_under_table_name_with_slash():
    table_qn = f"{POWERBI_DATASET_QUALIFIED_NAME}/Sales/2024"

    sut = PowerBIColumn.creator(name=NAME, power_bi_table_qualified_name=table_qn)

    assert sut.qualified_name == f"{table_qn}/Revenue"
    assert sut.dataset_qualified_name == POWERBI_DATASET_QUALIFIED_NAME
    assert sut.workspace_qualified_name == POWERBI_WORKSPACE_QUALIFIED_NAME


def test_updater():
    sut = PowerBIColumn.updater(qualified_name=APP_QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == NAME


def test_trim_to_required():
    sut = PowerBIColumn.updater(
        qualified_name=APP_QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == NAME
