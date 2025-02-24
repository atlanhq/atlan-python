import pytest

from pyatlan.model.assets import AirflowTask
from pyatlan.model.enums import AtlanConnectorType
from tests.unit.model.constants import (
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
def test_creator_with_missing_parameters_raise_value_error(
    name: str, airflow_dag_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AirflowTask.creator(
            name=name, airflow_dag_qualified_name=airflow_dag_qualified_name
        )


def test_creator():
    task = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME,
        airflow_dag_qualified_name=AIRFLOW_DAG_QUALIFIED_NAME,
    )

    assert task.name == AIRFLOW_TASK_NAME
    assert task.connector_name == AtlanConnectorType.AIRFLOW
    assert task.airflow_dag_qualified_name == AIRFLOW_DAG_QUALIFIED_NAME
    assert task.connection_qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME
    assert task.qualified_name == f"{AIRFLOW_DAG_QUALIFIED_NAME}/{AIRFLOW_TASK_NAME}"


def test_overload_creator():
    task = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME,
        airflow_dag_qualified_name=AIRFLOW_DAG_QUALIFIED_NAME,
        connection_qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    )

    assert task.name == AIRFLOW_TASK_NAME
    assert task.connector_name == AtlanConnectorType.AIRFLOW
    assert task.airflow_dag_qualified_name == AIRFLOW_DAG_QUALIFIED_NAME
    assert task.connection_qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME
    assert task.qualified_name == f"{AIRFLOW_DAG_QUALIFIED_NAME}/{AIRFLOW_TASK_NAME}"


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
    with pytest.raises(ValueError, match=message):
        AirflowTask.updater(qualified_name=qualified_name, name=name)


def test_updater():
    task = AirflowTask.updater(
        name=AIRFLOW_TASK_NAME, qualified_name=AIRFLOW_TASK_QUALIFIED_NAME
    )

    assert task.name == AIRFLOW_TASK_NAME
    assert task.qualified_name == AIRFLOW_TASK_QUALIFIED_NAME


def test_trim_to_required():
    task = AirflowTask.updater(
        name=AIRFLOW_TASK_NAME, qualified_name=AIRFLOW_TASK_QUALIFIED_NAME
    ).trim_to_required()

    assert task.name == AIRFLOW_TASK_NAME
    assert task.qualified_name == AIRFLOW_TASK_QUALIFIED_NAME
