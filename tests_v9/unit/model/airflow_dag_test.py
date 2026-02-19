# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AirflowDag model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import AirflowDag
from tests_v9.unit.model.constants import (
    AIRFLOW_CONNECTION_QUALIFIED_NAME,
    AIRFLOW_DAG_NAME,
    AIRFLOW_DAG_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (AIRFLOW_DAG_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        AirflowDag.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test that creator properly initializes an AirflowDag with all derived fields."""
    sut = AirflowDag.creator(
        name=AIRFLOW_DAG_NAME,
        connection_qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == AIRFLOW_DAG_NAME
    assert sut.qualified_name == AIRFLOW_DAG_QUALIFIED_NAME
    assert sut.connector_name == "airflow"
    assert sut.connection_qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, AIRFLOW_DAG_QUALIFIED_NAME, "qualified_name is required"),
        (AIRFLOW_DAG_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        AirflowDag.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates an AirflowDag instance for modification."""
    sut = AirflowDag.updater(
        name=AIRFLOW_DAG_NAME, qualified_name=AIRFLOW_DAG_QUALIFIED_NAME
    )

    assert sut.name == AIRFLOW_DAG_NAME
    assert sut.qualified_name == AIRFLOW_DAG_QUALIFIED_NAME


def test_trim_to_required():
    """Test that trim_to_required returns an AirflowDag with only required fields."""
    sut = AirflowDag.updater(
        name=AIRFLOW_DAG_NAME,
        qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.name == AIRFLOW_DAG_NAME
    assert sut.qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME


def test_basic_construction():
    """Test basic AirflowDag construction with minimal parameters."""
    dag = AirflowDag(name=AIRFLOW_DAG_NAME, qualified_name=AIRFLOW_DAG_QUALIFIED_NAME)

    assert dag.name == AIRFLOW_DAG_NAME
    assert dag.qualified_name == AIRFLOW_DAG_QUALIFIED_NAME
    assert dag.type_name == "AirflowDag"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    dag = AirflowDag(name=AIRFLOW_DAG_NAME, qualified_name=AIRFLOW_DAG_QUALIFIED_NAME)

    assert dag.airflow_dag_schedule is UNSET
    assert dag.airflow_tags is UNSET
    assert dag.airflow_run_version is UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    dag = AirflowDag.creator(
        name=AIRFLOW_DAG_NAME,
        connection_qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    )

    json_str = dag.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "AirflowDag"
    assert "attributes" in data
    assert data["attributes"]["name"] == AIRFLOW_DAG_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = AirflowDag.creator(
        name=AIRFLOW_DAG_NAME,
        connection_qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = AirflowDag.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    dag = AirflowDag.creator(
        name=AIRFLOW_DAG_NAME,
        connection_qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    )

    assert dag.guid is not UNSET
    assert dag.guid is not None
    assert isinstance(dag.guid, str)
    assert dag.guid.startswith("-")
