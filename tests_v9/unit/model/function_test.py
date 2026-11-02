# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Function model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import Function

CONNECTION_QN = "default/databricks/1700000000"
DATABASE_QN = f"{CONNECTION_QN}/main"
SCHEMA_QN = f"{DATABASE_QN}/analytics"
FUNCTION_NAME = "mask_email"
FUNCTION_QN = f"{SCHEMA_QN}/{FUNCTION_NAME}"


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        pytest.param(
            # atlan-databricks-app transform/duckdb/function_transformer.py:37
            # and transform/templates/function.yaml
            dict(
                name="mask_email",
                schema_qualified_name="default/databricks/1700000000/main/analytics",
            ),
            dict(
                qualified_name="default/databricks/1700000000/main/analytics/mask_email",
                connection_qualified_name="default/databricks/1700000000",
                connector_name="databricks",
                database_name="main",
                database_qualified_name="default/databricks/1700000000/main",
                schema_name="analytics",
            ),
            id="databricks",
        ),
        pytest.param(
            # atlan-db2-app flavors/luw (and db2i) qualified_name.build_function_qn
            dict(
                name="CALC_TAX",
                schema_qualified_name="default/db2luw/1700000000/SAMPLE/DB2INST1",
            ),
            dict(
                qualified_name="default/db2luw/1700000000/SAMPLE/DB2INST1/CALC_TAX",
                connection_qualified_name="default/db2luw/1700000000",
                connector_name="db2luw",
                database_name="SAMPLE",
                database_qualified_name="default/db2luw/1700000000/SAMPLE",
                schema_name="DB2INST1",
            ),
            id="db2-luw",
        ),
        pytest.param(
            # atlan-db2-app flavors/zos: schema has no database segment
            dict(
                name="CALC_TAX",
                schema_qualified_name="default/db2zos/1700000000/PAYROLL",
                connection_qualified_name="default/db2zos/1700000000",
            ),
            dict(
                qualified_name="default/db2zos/1700000000/PAYROLL/CALC_TAX",
                connection_qualified_name="default/db2zos/1700000000",
                connector_name="db2zos",
                database_name=UNSET,
                database_qualified_name=UNSET,
                schema_name="PAYROLL",
            ),
            id="db2-zos",
        ),
        pytest.param(
            # atlan-sapase-app sapase_app.py map_function: {db_qn}/{owner}/{name}
            dict(
                name="fn_rate",
                schema_qualified_name="default/sap-ase/1700000000/salesdb/dbo",
            ),
            dict(
                qualified_name="default/sap-ase/1700000000/salesdb/dbo/fn_rate",
                connection_qualified_name="default/sap-ase/1700000000",
                connector_name="sap-ase",
                database_name="salesdb",
                database_qualified_name="default/sap-ase/1700000000/salesdb",
                schema_name="dbo",
            ),
            id="sapase",
        ),
        pytest.param(
            # atlan-saphana-app extras-function.yaml (conn qn uses /sap-hana/)
            dict(
                name="GET_RATE",
                schema_qualified_name="default/sap-hana/1700000000/HXE/SALES",
            ),
            dict(
                qualified_name="default/sap-hana/1700000000/HXE/SALES/GET_RATE",
                connection_qualified_name="default/sap-hana/1700000000",
                connector_name="sap-hana",
                database_name="HXE",
                database_qualified_name="default/sap-hana/1700000000/HXE",
                schema_name="SALES",
            ),
            id="saphana",
        ),
    ],
)
def test_creator_matches_app_qualified_name(kwargs, expected):
    """Mirror each connector app's Function builder inputs and output."""
    sut = Function.creator(**kwargs)

    for attr, value in expected.items():
        assert getattr(sut, attr) == value, attr
    assert sut.schema_qualified_name == kwargs["schema_qualified_name"]
    assert sut.function_schema.unique_attributes == {
        "qualifiedName": kwargs["schema_qualified_name"]
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, schema_qualified_name, message",
    [
        (None, SCHEMA_QN, "name is required"),
        (" ", SCHEMA_QN, "name cannot be blank"),
        (FUNCTION_NAME, None, "schema_qualified_name is required"),
        (FUNCTION_NAME, " ", "schema_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name, schema_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        Function.creator(name=name, schema_qualified_name=schema_qualified_name)


@pytest.mark.parametrize(
    "arg",
    [
        "schema_name",
        "database_name",
        "database_qualified_name",
        "connection_qualified_name",
    ],
)
def test_creator_with_blank_optional_parent_raises_value_error(arg):
    kwargs = {"connection_qualified_name": CONNECTION_QN, arg: " "}
    with pytest.raises(ValueError, match=f"{arg} cannot be blank"):
        Function.creator(
            name=FUNCTION_NAME,
            schema_qualified_name=SCHEMA_QN,
            **kwargs,
        )


def test_creator_with_non_standard_depth_and_no_connection_raises_value_error():
    with pytest.raises(ValueError, match="Invalid schema_qualified_name"):
        Function.creator(
            name=FUNCTION_NAME,
            schema_qualified_name="default/db2zos/1700000000/PAYROLL",
        )


@pytest.mark.parametrize(
    "kwargs, message",
    [
        (
            dict(connection_qualified_name="default/databricks/999"),
            "schema_qualified_name is invalid",
        ),
        (
            dict(
                connection_qualified_name=CONNECTION_QN,
                database_qualified_name=f"{CONNECTION_QN}/other",
            ),
            "schema_qualified_name is invalid",
        ),
        (
            dict(connection_qualified_name=CONNECTION_QN, database_name="other"),
            "schema_qualified_name is invalid",
        ),
        (
            dict(connection_qualified_name="default/databricks"),
            "connection_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_mismatched_parents_raises_value_error(kwargs, message):
    with pytest.raises(ValueError, match=message):
        Function.creator(name=FUNCTION_NAME, schema_qualified_name=SCHEMA_QN, **kwargs)


def test_creator_with_explicit_parents():
    sut = Function.creator(
        name=FUNCTION_NAME,
        schema_qualified_name=SCHEMA_QN,
        schema_name="Analytics",
        database_name="Main",
        database_qualified_name=DATABASE_QN,
        connection_qualified_name=CONNECTION_QN,
        function_definition="RETURN regexp_replace(email, '.+@', '***@')",
        function_language="SQL",
    )

    assert sut.qualified_name == FUNCTION_QN
    assert sut.schema_name == "Analytics"
    assert sut.database_name == "Main"
    assert sut.database_qualified_name == DATABASE_QN
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.function_definition == "RETURN regexp_replace(email, '.+@', '***@')"
    assert sut.function_language == "SQL"


def test_creator_leaves_optional_attributes_unset():
    sut = Function.creator(name=FUNCTION_NAME, schema_qualified_name=SCHEMA_QN)

    assert sut.function_definition is UNSET
    assert sut.function_language is UNSET


def test_creator_with_guid():
    sut = Function.creator(name=FUNCTION_NAME, schema_qualified_name=SCHEMA_QN)

    assert isinstance(sut.guid, str)
    assert sut.guid.startswith("-")


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FUNCTION_NAME, "qualified_name is required"),
        (FUNCTION_QN, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name, name, message
):
    with pytest.raises(ValueError, match=message):
        Function.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = Function.updater(qualified_name=FUNCTION_QN, name=FUNCTION_NAME)

    assert sut.qualified_name == FUNCTION_QN
    assert sut.name == FUNCTION_NAME


def test_trim_to_required():
    sut = Function.creator(
        name=FUNCTION_NAME, schema_qualified_name=SCHEMA_QN
    ).trim_to_required()

    assert sut.qualified_name == FUNCTION_QN
    assert sut.name == FUNCTION_NAME
    assert sut.schema_qualified_name is UNSET


def test_round_trip_serialization(serde):
    original = Function.creator(name=FUNCTION_NAME, schema_qualified_name=SCHEMA_QN)

    json_str = original.to_json(nested=True, serde=serde)
    data = json.loads(json_str)
    assert data["typeName"] == "Function"
    assert data["attributes"]["qualifiedName"] == FUNCTION_QN

    restored = Function.from_json(json_str, serde=serde)
    assert restored.qualified_name == FUNCTION_QN
    assert restored.schema_qualified_name == SCHEMA_QN
