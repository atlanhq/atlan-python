import pytest

from pyatlan.model.assets import APIObject
from tests.unit.model.constants import (
    API_CONNECTION_QUALIFIED_NAME,
    API_CONNECTOR_TYPE,
    API_OBJECT_QUALIFIED_NAME,
    API_OBJECT_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (API_OBJECT_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APIObject.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_create():
    sut = APIObject.creator(
        name=API_OBJECT_NAME, connection_qualified_name=API_CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == API_OBJECT_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_OBJECT_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE


def test_overload_creator():
    sut = APIObject.creator(
        name=API_OBJECT_NAME,
        connection_qualified_name=API_CONNECTION_QUALIFIED_NAME,
        api_field_count=2,
    )

    assert sut.name == API_OBJECT_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_OBJECT_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE
    assert sut.api_field_count == 2


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, API_OBJECT_QUALIFIED_NAME, "qualified_name is required"),
        (API_OBJECT_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        APIObject.updater(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = APIObject.updater(
        qualified_name=API_OBJECT_QUALIFIED_NAME, name=API_OBJECT_NAME
    )

    assert sut.qualified_name == API_OBJECT_QUALIFIED_NAME
    assert sut.name == API_OBJECT_NAME


def test_trim_to_required():
    sut = APIObject.updater(
        name=API_OBJECT_NAME, qualified_name=API_OBJECT_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == API_OBJECT_NAME
    assert sut.qualified_name == API_OBJECT_QUALIFIED_NAME
