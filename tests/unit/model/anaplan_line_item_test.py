import pytest

from pyatlan.model.assets import AnaplanLineItem
from tests.unit.model.constants import (
    ANAPLAN_CONNECTION_QUALIFIED_NAME,
    ANAPLAN_CONNECTOR_TYPE,
    ANAPLAN_LINE_ITEM_NAME,
    ANAPLAN_LINE_ITEM_QUALIFIED_NAME,
    ANAPLAN_MODULE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, module_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (ANAPLAN_LINE_ITEM_NAME, None, "module_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, module_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanLineItem.creator(name=name, module_qualified_name=module_qualified_name)


def test_create():
    sut = AnaplanLineItem.creator(
        name=ANAPLAN_LINE_ITEM_NAME,
        module_qualified_name=ANAPLAN_MODULE_QUALIFIED_NAME,
    )

    assert sut.name == ANAPLAN_LINE_ITEM_NAME
    assert sut.connection_qualified_name == ANAPLAN_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == ANAPLAN_LINE_ITEM_QUALIFIED_NAME
    assert sut.connector_name == ANAPLAN_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ANAPLAN_MODULE_QUALIFIED_NAME, "qualified_name is required"),
        (ANAPLAN_LINE_ITEM_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanLineItem.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_create_for_modification():
    sut = AnaplanLineItem.create_for_modification(
        qualified_name=ANAPLAN_LINE_ITEM_QUALIFIED_NAME, name=ANAPLAN_LINE_ITEM_NAME
    )

    assert sut.qualified_name == ANAPLAN_LINE_ITEM_QUALIFIED_NAME
    assert sut.name == ANAPLAN_LINE_ITEM_NAME


def test_trim_to_required():
    sut = AnaplanLineItem.create_for_modification(
        name=ANAPLAN_LINE_ITEM_NAME, qualified_name=ANAPLAN_LINE_ITEM_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == ANAPLAN_LINE_ITEM_NAME
    assert sut.qualified_name == ANAPLAN_LINE_ITEM_QUALIFIED_NAME
