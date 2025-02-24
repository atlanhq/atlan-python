import pytest

from pyatlan.model.assets import SupersetChart
from tests.unit.model.constants import (
    SUPERSET_CHART_NAME,
    SUPERSET_CHART_QUALIFIED_NAME,
    SUPERSET_CONNECTION_QUALIFIED_NAME,
    SUPERSET_CONNECTOR_TYPE,
    SUPERSET_DASHBOARD_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, superset_dashboard_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (SUPERSET_CHART_NAME, None, "superset_dashboard_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, superset_dashboard_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        SupersetChart.create(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
        )


def test_create():
    sut = SupersetChart.create(
        name=SUPERSET_CHART_NAME,
        superset_dashboard_qualified_name=SUPERSET_DASHBOARD_QUALIFIED_NAME,
    )

    assert sut.name == SUPERSET_CHART_NAME
    assert sut.superset_dashboard_qualified_name == SUPERSET_DASHBOARD_QUALIFIED_NAME
    assert sut.connection_qualified_name == SUPERSET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{SUPERSET_DASHBOARD_QUALIFIED_NAME}/{SUPERSET_CHART_NAME}"
    )
    assert sut.connector_name == SUPERSET_CONNECTOR_TYPE


def test_overload_creator():
    sut = SupersetChart.creator(
        name=SUPERSET_CHART_NAME,
        superset_dashboard_qualified_name=SUPERSET_DASHBOARD_QUALIFIED_NAME,
        connection_qualified_name=SUPERSET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == SUPERSET_CHART_NAME
    assert sut.superset_dashboard_qualified_name == SUPERSET_DASHBOARD_QUALIFIED_NAME
    assert sut.connection_qualified_name == SUPERSET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{SUPERSET_DASHBOARD_QUALIFIED_NAME}/{SUPERSET_CHART_NAME}"
    )
    assert sut.connector_name == SUPERSET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SUPERSET_CHART_QUALIFIED_NAME, "qualified_name is required"),
        (SUPERSET_CHART_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        SupersetChart.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = SupersetChart.create_for_modification(
        qualified_name=SUPERSET_CHART_QUALIFIED_NAME, name=SUPERSET_CHART_NAME
    )

    assert sut.qualified_name == SUPERSET_CHART_QUALIFIED_NAME
    assert sut.name == SUPERSET_CHART_NAME


def test_trim_to_required():
    sut = SupersetChart.create_for_modification(
        name=SUPERSET_CHART_NAME, qualified_name=SUPERSET_CHART_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == SUPERSET_CHART_NAME
    assert sut.qualified_name == SUPERSET_CHART_QUALIFIED_NAME
