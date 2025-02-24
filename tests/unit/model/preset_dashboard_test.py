import pytest

from pyatlan.model.assets import PresetDashboard
from tests.unit.model.constants import (
    PRESET_CONNECTION_QUALIFIED_NAME,
    PRESET_CONNECTOR_TYPE,
    PRESET_DASHBOARD_NAME,
    PRESET_DASHBOARD_QUALIFIED_NAME,
    PRESET_WORKSPACE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, preset_workspace_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (PRESET_DASHBOARD_NAME, None, "preset_workspace_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, preset_workspace_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        PresetDashboard.create(
            name=name, preset_workspace_qualified_name=preset_workspace_qualified_name
        )


def test_create():
    sut = PresetDashboard.create(
        name=PRESET_DASHBOARD_NAME,
        preset_workspace_qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_DASHBOARD_NAME
    assert sut.preset_workspace_qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{PRESET_WORKSPACE_QUALIFIED_NAME}/{PRESET_DASHBOARD_NAME}"
    )
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


def test_overload_creator():
    sut = PresetDashboard.creator(
        name=PRESET_DASHBOARD_NAME,
        preset_workspace_qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_DASHBOARD_NAME
    assert sut.preset_workspace_qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{PRESET_WORKSPACE_QUALIFIED_NAME}/{PRESET_DASHBOARD_NAME}"
    )
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PRESET_DASHBOARD_QUALIFIED_NAME, "qualified_name is required"),
        (PRESET_DASHBOARD_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        PresetDashboard.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_create_for_modification():
    sut = PresetDashboard.create_for_modification(
        qualified_name=PRESET_DASHBOARD_QUALIFIED_NAME, name=PRESET_DASHBOARD_NAME
    )

    assert sut.qualified_name == PRESET_DASHBOARD_QUALIFIED_NAME
    assert sut.name == PRESET_DASHBOARD_NAME


def test_trim_to_required():
    sut = PresetDashboard.create_for_modification(
        qualified_name=PRESET_DASHBOARD_QUALIFIED_NAME, name=PRESET_DASHBOARD_NAME
    ).trim_to_required()

    assert sut.qualified_name == PRESET_DASHBOARD_QUALIFIED_NAME
    assert sut.name == PRESET_DASHBOARD_NAME
