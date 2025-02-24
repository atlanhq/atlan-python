import pytest

from pyatlan.model.assets import PresetChart
from tests.unit.model.constants import (
    PRESET_CHART_NAME,
    PRESET_CHART_QUALIFIED_NAME,
    PRESET_CONNECTION_QUALIFIED_NAME,
    PRESET_CONNECTOR_TYPE,
    PRESET_DASHBOARD_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, preset_dashboard_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (PRESET_CHART_NAME, None, "preset_dashboard_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, preset_dashboard_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        PresetChart.create(name=name, preset_dashboard_qualified_name=preset_dashboard_qualified_name)


def test_create():
    sut = PresetChart.create(
        name=PRESET_CHART_NAME,
        preset_dashboard_qualified_name=PRESET_DASHBOARD_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_CHART_NAME
    assert sut.preset_dashboard_qualified_name == PRESET_DASHBOARD_QUALIFIED_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == f"{PRESET_DASHBOARD_QUALIFIED_NAME}/{PRESET_CHART_NAME}"
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


def test_overload_creator():
    sut = PresetChart.creator(
        name=PRESET_CHART_NAME,
        preset_dashboard_qualified_name=PRESET_DASHBOARD_QUALIFIED_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_CHART_NAME
    assert sut.preset_dashboard_qualified_name == PRESET_DASHBOARD_QUALIFIED_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == f"{PRESET_DASHBOARD_QUALIFIED_NAME}/{PRESET_CHART_NAME}"
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PRESET_CHART_QUALIFIED_NAME, "qualified_name is required"),
        (PRESET_CHART_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        PresetChart.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = PresetChart.create_for_modification(qualified_name=PRESET_CHART_QUALIFIED_NAME, name=PRESET_CHART_NAME)

    assert sut.qualified_name == PRESET_CHART_QUALIFIED_NAME
    assert sut.name == PRESET_CHART_NAME


def test_trim_to_required():
    sut = PresetChart.create_for_modification(
        name=PRESET_CHART_NAME, qualified_name=PRESET_CHART_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == PRESET_CHART_NAME
    assert sut.qualified_name == PRESET_CHART_QUALIFIED_NAME
