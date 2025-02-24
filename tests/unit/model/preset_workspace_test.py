import pytest

from pyatlan.model.assets import PresetWorkspace
from tests.unit.model.constants import (
    PRESET_CONNECTION_QUALIFIED_NAME,
    PRESET_CONNECTOR_TYPE,
    PRESET_WORKSPACE_NAME,
    PRESET_WORKSPACE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (PRESET_WORKSPACE_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        PresetWorkspace.create(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_create():
    sut = PresetWorkspace.create(
        name=PRESET_WORKSPACE_NAME,
        connection_qualified_name=PRESET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == PRESET_WORKSPACE_NAME
    assert sut.connection_qualified_name == PRESET_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.connector_name == PRESET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, PRESET_WORKSPACE_QUALIFIED_NAME, "qualified_name is required"),
        (PRESET_WORKSPACE_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        PresetWorkspace.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_create_for_modification():
    sut = PresetWorkspace.create_for_modification(
        qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME, name=PRESET_WORKSPACE_NAME
    )

    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.name == PRESET_WORKSPACE_NAME


def test_trim_to_required():
    sut = PresetWorkspace.create_for_modification(
        qualified_name=PRESET_WORKSPACE_QUALIFIED_NAME, name=PRESET_WORKSPACE_NAME
    ).trim_to_required()

    assert sut.qualified_name == PRESET_WORKSPACE_QUALIFIED_NAME
    assert sut.name == PRESET_WORKSPACE_NAME
