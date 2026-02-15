# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AirflowTask model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import AirflowTask
from tests_v9.unit.model.constants import (
    AIRFLOW_CONNECTION_QUALIFIED_NAME,
    AIRFLOW_DAG_QUALIFIED_NAME,
    AIRFLOW_TASK_NAME,
    AIRFLOW_TASK_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, airflow_dag_qualified_name, message",
    [
        (None, "airflow/dag", "name is required"),
        (AIRFLOW_TASK_NAME, None, "airflow_dag_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, airflow_dag_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        AirflowTask.creator(
            name=name, airflow_dag_qualified_name=airflow_dag_qualified_name
        )


def test_creator():
    """Test that creator properly initializes an AirflowTask with all derived fields."""
    sut = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME,
        airflow_dag_qualified_name=AIRFLOW_DAG_QUALIFIED_NAME,
    )

    assert sut.name == AIRFLOW_TASK_NAME
    assert sut.connector_name == "airflow"
    assert sut.airflow_dag_qualified_name == AIRFLOW_DAG_QUALIFIED_NAME
    assert sut.connection_qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == AIRFLOW_TASK_QUALIFIED_NAME


def test_overload_creator():
    """Test creator with connection_qualified_name explicitly provided."""
    sut = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME,
        airflow_dag_qualified_name=AIRFLOW_DAG_QUALIFIED_NAME,
        connection_qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == AIRFLOW_TASK_NAME
    assert sut.connector_name == "airflow"
    assert sut.airflow_dag_qualified_name == AIRFLOW_DAG_QUALIFIED_NAME
    assert sut.connection_qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == AIRFLOW_TASK_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, AIRFLOW_TASK_NAME, "qualified_name is required"),
        (AIRFLOW_TASK_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        AirflowTask.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates an AirflowTask instance for modification."""
    sut = AirflowTask.updater(
        name=AIRFLOW_TASK_NAME, qualified_name=AIRFLOW_TASK_QUALIFIED_NAME
    )

    assert sut.name == AIRFLOW_TASK_NAME
    assert sut.qualified_name == AIRFLOW_TASK_QUALIFIED_NAME


def test_trim_to_required():
    """Test that trim_to_required returns an AirflowTask with only required fields."""
    sut = AirflowTask.updater(
        name=AIRFLOW_TASK_NAME, qualified_name=AIRFLOW_TASK_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == AIRFLOW_TASK_NAME
    assert sut.qualified_name == AIRFLOW_TASK_QUALIFIED_NAME


def test_basic_construction():
    """Test basic AirflowTask construction with minimal parameters."""
    task = AirflowTask(
        name=AIRFLOW_TASK_NAME, qualified_name=AIRFLOW_TASK_QUALIFIED_NAME
    )

    assert task.name == AIRFLOW_TASK_NAME
    assert task.qualified_name == AIRFLOW_TASK_QUALIFIED_NAME
    assert task.type_name == "AirflowTask"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    task = AirflowTask(
        name=AIRFLOW_TASK_NAME, qualified_name=AIRFLOW_TASK_QUALIFIED_NAME
    )

    assert task.airflow_task_operator_class is UNSET
    assert task.airflow_dag_name is UNSET
    assert task.airflow_task_sql is UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    task = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME,
        airflow_dag_qualified_name=AIRFLOW_DAG_QUALIFIED_NAME,
    )

    json_str = task.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "AirflowTask"
    assert "attributes" in data
    assert data["attributes"]["name"] == AIRFLOW_TASK_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME,
        airflow_dag_qualified_name=AIRFLOW_DAG_QUALIFIED_NAME,
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = AirflowTask.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    task = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME,
        airflow_dag_qualified_name=AIRFLOW_DAG_QUALIFIED_NAME,
    )

    assert task.guid is not UNSET
    assert task.guid is not None
    assert isinstance(task.guid, str)
    assert task.guid.startswith("-")
