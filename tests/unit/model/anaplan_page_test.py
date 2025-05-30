import pytest

from pyatlan.model.assets import AnaplanPage
from tests.unit.model.constants import (
    ANAPLAN_APP_QUALIFIED_NAME,
    ANAPLAN_CONNECTION_QUALIFIED_NAME,
    ANAPLAN_CONNECTOR_TYPE,
    ANAPLAN_PAGE_NAME,
    ANAPLAN_PAGE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, app_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (ANAPLAN_PAGE_NAME, None, "app_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, app_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanPage.creator(name=name, app_qualified_name=app_qualified_name)


def test_create():
    sut = AnaplanPage.creator(
        name=ANAPLAN_PAGE_NAME,
        app_qualified_name=ANAPLAN_APP_QUALIFIED_NAME,
    )

    assert sut.name == ANAPLAN_PAGE_NAME
    assert sut.connection_qualified_name == ANAPLAN_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == ANAPLAN_PAGE_QUALIFIED_NAME
    assert sut.connector_name == ANAPLAN_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ANAPLAN_APP_QUALIFIED_NAME, "qualified_name is required"),
        (ANAPLAN_PAGE_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AnaplanPage.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = AnaplanPage.create_for_modification(
        qualified_name=ANAPLAN_PAGE_QUALIFIED_NAME, name=ANAPLAN_PAGE_NAME
    )

    assert sut.qualified_name == ANAPLAN_PAGE_QUALIFIED_NAME
    assert sut.name == ANAPLAN_PAGE_NAME


def test_trim_to_required():
    sut = AnaplanPage.create_for_modification(
        name=ANAPLAN_PAGE_NAME, qualified_name=ANAPLAN_PAGE_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == ANAPLAN_PAGE_NAME
    assert sut.qualified_name == ANAPLAN_PAGE_QUALIFIED_NAME
