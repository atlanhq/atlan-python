import pytest

from pyatlan.model.assets import AnaplanModel
from tests.unit.model.constants import (
    ANAPLAN_CONNECTION_QUALIFIED_NAME,
    ANAPLAN_CONNECTOR_TYPE,
    ANAPLAN_MODEL_NAME,
    ANAPLAN_MODEL_QUALIFIED_NAME,
    ANAPLAN_WORKSPACE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, workspace_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (ANAPLAN_MODEL_NAME, None, "workspace_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, workspace_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanModel.creator(
            name=name, workspace_qualified_name=workspace_qualified_name
        )


def test_create():
    sut = AnaplanModel.creator(
        name=ANAPLAN_MODEL_NAME,
        workspace_qualified_name=ANAPLAN_WORKSPACE_QUALIFIED_NAME,
    )

    assert sut.name == ANAPLAN_MODEL_NAME
    assert sut.connection_qualified_name == ANAPLAN_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == ANAPLAN_MODEL_QUALIFIED_NAME
    assert sut.connector_name == ANAPLAN_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ANAPLAN_WORKSPACE_QUALIFIED_NAME, "qualified_name is required"),
        (ANAPLAN_MODEL_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanModel.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = AnaplanModel.create_for_modification(
        qualified_name=ANAPLAN_MODEL_QUALIFIED_NAME, name=ANAPLAN_MODEL_NAME
    )

    assert sut.qualified_name == ANAPLAN_MODEL_QUALIFIED_NAME
    assert sut.name == ANAPLAN_MODEL_NAME


def test_trim_to_required():
    sut = AnaplanModel.create_for_modification(
        name=ANAPLAN_MODEL_NAME, qualified_name=ANAPLAN_MODEL_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == ANAPLAN_MODEL_NAME
    assert sut.qualified_name == ANAPLAN_MODEL_QUALIFIED_NAME
