import pytest

from pyatlan.model.assets import Application
from tests.unit.model.constants import (
    APP_CONNECTION_QUALIFIED_NAME,
    APP_CONNECTOR_TYPE,
    APPLICATION_NAME,
    APPLICATION_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (APPLICATION_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Application.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_create():
    sut = Application.creator(
        name=APPLICATION_NAME,
        connection_qualified_name=APP_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == APPLICATION_NAME
    assert sut.connection_qualified_name == APP_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == APPLICATION_QUALIFIED_NAME
    assert sut.connector_name == APP_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, APPLICATION_QUALIFIED_NAME, "qualified_name is required"),
        (APPLICATION_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Application.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Application.create_for_modification(
        qualified_name=APPLICATION_QUALIFIED_NAME,
        name=APPLICATION_NAME,
    )

    assert sut.qualified_name == APPLICATION_QUALIFIED_NAME
    assert sut.name == APPLICATION_NAME


def test_trim_to_required():
    sut = Application.create_for_modification(
        name=APPLICATION_NAME,
        qualified_name=APPLICATION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.name == APPLICATION_NAME
    assert sut.qualified_name == APPLICATION_QUALIFIED_NAME
