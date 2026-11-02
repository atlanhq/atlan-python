# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Procedure model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import Procedure
from tests_v9.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    PROCEDURE_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
)

DEFINITION = """
BEGIN
insert into `atlanhq.testing_lineage.INSTACART_ALCOHOL_ORDER_TIME_copy`
select * from `atlanhq.testing_lineage.INSTACART_ALCOHOL_ORDER_TIME`;
END
"""

PROCEDURE_QUALIFIED_NAME = f"{SCHEMA_QUALIFIED_NAME}/_procedures_/{PROCEDURE_NAME}"


@pytest.mark.parametrize(
    "name, definition, schema_qualified_name, message",
    [
        (None, DEFINITION, SCHEMA_QUALIFIED_NAME, "name is required"),
        (PROCEDURE_NAME, None, SCHEMA_QUALIFIED_NAME, "definition is required"),
        (PROCEDURE_NAME, DEFINITION, None, "schema_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, definition: str, schema_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Procedure.creator(
            name=name,
            definition=definition,
            schema_qualified_name=schema_qualified_name,
        )


def test_creator():
    """Test that creator properly initializes a Procedure with all derived fields."""
    sut = Procedure.creator(
        name=PROCEDURE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert sut.name == PROCEDURE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == PROCEDURE_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.unique_attributes["qualifiedName"] == SCHEMA_QUALIFIED_NAME


def test_overload_creator():
    """Test creator with all optional parameters provided."""
    sut = Procedure.creator(
        name=PROCEDURE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PROCEDURE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == PROCEDURE_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.unique_attributes["qualifiedName"] == SCHEMA_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PROCEDURE_QUALIFIED_NAME, "qualified_name is required"),
        (PROCEDURE_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Procedure.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a Procedure instance for modification."""
    sut = Procedure.updater(
        qualified_name=PROCEDURE_QUALIFIED_NAME, name=PROCEDURE_NAME
    )

    assert sut.qualified_name == PROCEDURE_QUALIFIED_NAME
    assert sut.name == PROCEDURE_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a Procedure with only required fields."""
    sut = Procedure.updater(
        qualified_name=PROCEDURE_QUALIFIED_NAME, name=PROCEDURE_NAME
    ).trim_to_required()

    assert sut.qualified_name == PROCEDURE_QUALIFIED_NAME
    assert sut.name == PROCEDURE_NAME


def test_basic_construction():
    """Test basic Procedure construction with minimal parameters."""
    proc = Procedure(name=PROCEDURE_NAME, qualified_name=PROCEDURE_QUALIFIED_NAME)

    assert proc.name == PROCEDURE_NAME
    assert proc.qualified_name == PROCEDURE_QUALIFIED_NAME
    assert proc.type_name == "Procedure"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    proc = Procedure(name=PROCEDURE_NAME, qualified_name=PROCEDURE_QUALIFIED_NAME)

    assert proc.definition is UNSET
    assert proc.sql_language is UNSET
    assert proc.database_name is UNSET
    assert proc.schema_name is UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    proc = Procedure.creator(
        name=PROCEDURE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    json_str = proc.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "Procedure"
    assert "attributes" in data
    assert data["attributes"]["name"] == PROCEDURE_NAME
    assert data["attributes"]["qualifiedName"] == PROCEDURE_QUALIFIED_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = Procedure.creator(
        name=PROCEDURE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = Procedure.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name
    assert restored.definition == original.definition


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    proc = Procedure.creator(
        name=PROCEDURE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert proc.guid is not UNSET
    assert proc.guid is not None
    assert isinstance(proc.guid, str)
    assert proc.guid.startswith("-")


# Non-standard depths (FND-3887). Each qualifiedName is the literal string the
# connector app emits today.

FABRIC_CONNECTION_QN = "default/fabric/1700000000"
FABRIC_DATABASE_QN = "default/fabric/1700000000/ws-1234/lh-5678"
FABRIC_SCHEMA_QN = "default/fabric/1700000000/ws-1234/lh-5678/dbo"


def test_creator_fabric_six_segment_parents():
    sut = Procedure.creator(
        name="sales",
        definition="CREATE PROCEDURE sales() BEGIN END",
        schema_qualified_name=FABRIC_SCHEMA_QN,
        database_name="Lakehouse",
        database_qualified_name=FABRIC_DATABASE_QN,
        connection_qualified_name=FABRIC_CONNECTION_QN,
    )

    assert (
        sut.qualified_name
        == "default/fabric/1700000000/ws-1234/lh-5678/dbo/_procedures_/sales"
    )
    assert sut.connector_name == "fabric"
    assert sut.connection_qualified_name == FABRIC_CONNECTION_QN
    assert sut.database_name == "Lakehouse"
    assert sut.database_qualified_name == FABRIC_DATABASE_QN
    assert sut.schema_name == "dbo"
    assert sut.schema_qualified_name == FABRIC_SCHEMA_QN
    assert sut.atlan_schema.unique_attributes["qualifiedName"] == FABRIC_SCHEMA_QN
    sut.validate(for_creation=True)


def test_creator_explicit_connection_on_standard_depth_derives_parents():
    sut = Procedure.creator(
        name="sales",
        definition="CREATE PROCEDURE sales() BEGIN END",
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME


def test_creator_explicit_schema_without_database():
    sut = Procedure.creator(
        name="sales",
        definition="CREATE PROCEDURE sales() BEGIN END",
        schema_qualified_name="default/db2zos/1700000000/PAYROLL",
        connection_qualified_name="default/db2zos/1700000000",
    )

    assert sut.qualified_name == "default/db2zos/1700000000/PAYROLL/_procedures_/sales"
    assert sut.schema_name == "PAYROLL"
    assert sut.database_name is UNSET
    assert sut.database_qualified_name is UNSET
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "kwargs, message",
    [
        (
            {"connection_qualified_name": "default/fabric/1700000001"},
            "schema_qualified_name is invalid",
        ),
        (
            {
                "connection_qualified_name": FABRIC_CONNECTION_QN,
                "database_qualified_name": "default/fabric/1700000000/ws-9999/lh-5678",
            },
            "schema_qualified_name is invalid",
        ),
        (
            {"connection_qualified_name": FABRIC_CONNECTION_QN, "schema_name": " "},
            "schema_name cannot be blank",
        ),
        (
            {"connection_qualified_name": "default/fabric"},
            "connection_qualified_name is invalid",
        ),
        ({}, "Invalid schema_qualified_name"),
    ],
)
def test_creator_explicit_parents_invalid(kwargs: dict, message: str):
    with pytest.raises(ValueError, match=message):
        Procedure.creator(
            name="sales",
            definition="CREATE PROCEDURE sales() BEGIN END",
            schema_qualified_name=FABRIC_SCHEMA_QN,
            **kwargs,
        )
