import pytest

from pyatlan.model.assets import AirflowDag
from pyatlan.model.enums import AtlanConnectorType
from tests.unit.model.constants import (
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
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AirflowDag.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    dag = AirflowDag.create(
        name=AIRFLOW_DAG_NAME,
        connection_qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    )

    assert dag.name == AIRFLOW_DAG_NAME
    assert dag.qualified_name == AIRFLOW_DAG_QUALIFIED_NAME
    assert dag.connector_name == AtlanConnectorType.AIRFLOW
    assert dag.connection_qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME


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
    with pytest.raises(ValueError, match=message):
        AirflowDag.updater(qualified_name=qualified_name, name=name)


def test_updater():
    dag = AirflowDag.updater(
        name=AIRFLOW_DAG_NAME, qualified_name=AIRFLOW_DAG_QUALIFIED_NAME
    )
    assert dag.name == AIRFLOW_DAG_NAME
    assert dag.qualified_name == AIRFLOW_DAG_QUALIFIED_NAME


def test_trim_to_required():
    dag = AirflowDag.updater(
        name=AIRFLOW_DAG_NAME,
        qualified_name=AIRFLOW_CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert dag.name == AIRFLOW_DAG_NAME
    assert dag.qualified_name == AIRFLOW_CONNECTION_QUALIFIED_NAME
