import pytest

from pyatlan.model.assets import AnaplanView
from tests.unit.model.constants import (
    ANAPLAN_CONNECTION_QUALIFIED_NAME,
    ANAPLAN_CONNECTOR_TYPE,
    ANAPLAN_MODULE_QUALIFIED_NAME,
    ANAPLAN_VIEW_NAME,
    ANAPLAN_VIEW_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, module_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (ANAPLAN_VIEW_NAME, None, "module_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, module_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanView.creator(name=name, module_qualified_name=module_qualified_name)


def test_create():
    sut = AnaplanView.creator(
        name=ANAPLAN_VIEW_NAME,
        module_qualified_name=ANAPLAN_MODULE_QUALIFIED_NAME,
    )

    assert sut.name == ANAPLAN_VIEW_NAME
    assert sut.connection_qualified_name == ANAPLAN_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == ANAPLAN_VIEW_QUALIFIED_NAME
    assert sut.connector_name == ANAPLAN_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ANAPLAN_MODULE_QUALIFIED_NAME, "qualified_name is required"),
        (ANAPLAN_VIEW_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanView.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = AnaplanView.create_for_modification(
        qualified_name=ANAPLAN_VIEW_QUALIFIED_NAME, name=ANAPLAN_VIEW_NAME
    )

    assert sut.qualified_name == ANAPLAN_VIEW_QUALIFIED_NAME
    assert sut.name == ANAPLAN_VIEW_NAME


def test_trim_to_required():
    sut = AnaplanView.create_for_modification(
        name=ANAPLAN_VIEW_NAME, qualified_name=ANAPLAN_VIEW_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == ANAPLAN_VIEW_NAME
    assert sut.qualified_name == ANAPLAN_VIEW_QUALIFIED_NAME
