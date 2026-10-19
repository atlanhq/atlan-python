# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the PowerBIDataflowEntityColumn creator in pyatlan_v9.

The expected qualifiedName and name are the literal strings atlan-powerbi-app
emits (FND-3852 analysis): the name defaults to "{entity} -> {column}".
"""

import pytest

from pyatlan_v9.model import PowerBIDataflowEntityColumn
from tests_v9.unit.model.constants import (
    POWERBI_CONNECTION_QUALIFIED_NAME,
    POWERBI_DATAFLOW_QUALIFIED_NAME,
    POWERBI_WORKSPACE_QUALIFIED_NAME,
)

APP_QUALIFIED_NAME = (
    "default/powerbi/1712345678/0f1e2d3c-4b5a-4978-8a9b-0c1d2e3f4a5b"
    "/3c4d5e6f-3333-4a5b-8c6d-7e8f9a0b1c2d/Customers/Region"
)
APP_NAME = "Customers -> Region"
REQUIRED = dict(
    power_bi_dataflow_qualified_name=POWERBI_DATAFLOW_QUALIFIED_NAME,
    entity_name="Customers",
    column_name="Region",
)


def test_creator_matches_app_qualified_name():
    sut = PowerBIDataflowEntityColumn.creator(**REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == APP_NAME
    assert sut.connection_qualified_name == POWERBI_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "powerbi"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    assert sut.power_bi_workspace_qualified_name == POWERBI_WORKSPACE_QUALIFIED_NAME
    assert sut.power_bi_dataflow_qualified_name == POWERBI_DATAFLOW_QUALIFIED_NAME
    assert sut.power_bi_dataflow_entity_name == "Customers"
    assert sut.power_bi_dataflow.unique_attributes == {
        "qualifiedName": POWERBI_DATAFLOW_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_creator_with_explicit_name():
    sut = PowerBIDataflowEntityColumn.creator(name="Region", **REQUIRED)

    assert sut.name == "Region"
    assert sut.qualified_name == APP_QUALIFIED_NAME


def test_create_alias():
    sut = PowerBIDataflowEntityColumn.create(**REQUIRED)

    assert sut.qualified_name == APP_QUALIFIED_NAME


@pytest.mark.parametrize("param", [*REQUIRED])
def test_creator_rejects_missing_or_blank_inputs(param):
    args = dict(REQUIRED)
    args[param] = None
    with pytest.raises(ValueError, match=f"{param} is required"):
        PowerBIDataflowEntityColumn.creator(**args)
    args[param] = "  "
    with pytest.raises(ValueError, match=f"{param} cannot be blank"):
        PowerBIDataflowEntityColumn.creator(**args)


@pytest.mark.parametrize(
    "bad_qualified_name",
    [
        POWERBI_WORKSPACE_QUALIFIED_NAME,
        f"{POWERBI_CONNECTION_QUALIFIED_NAME}//df-1",
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(bad_qualified_name):
    with pytest.raises(ValueError, match="power_bi_dataflow_qualified_name is invalid"):
        PowerBIDataflowEntityColumn.creator(
            **{**REQUIRED, "power_bi_dataflow_qualified_name": bad_qualified_name}
        )


def test_updater():
    sut = PowerBIDataflowEntityColumn.updater(
        qualified_name=APP_QUALIFIED_NAME, name=APP_NAME
    )

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == APP_NAME


def test_trim_to_required():
    sut = PowerBIDataflowEntityColumn.updater(
        qualified_name=APP_QUALIFIED_NAME, name=APP_NAME
    ).trim_to_required()

    assert sut.qualified_name == APP_QUALIFIED_NAME
    assert sut.name == APP_NAME
