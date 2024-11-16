import pytest

from pyatlan.model.assets import ApplicationAsset
from tests.unit.model.constants import (
    APPLICATION_CONTAINER_NAME,
    APPLICATION_CONTAINER_QUALIFIED_NAME,
    APPLICATION_CONNECTION_QUALIFIED_NAME,
    APPLICATION_CONNECTOR_TYPE,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (APPLICATION_CONTAINER_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        ApplicationAsset.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_create():
    sut = ApplicationAsset.creator(
        name=APPLICATION_CONTAINER_NAME,
        connection_qualified_name=APPLICATION_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == APPLICATION_CONTAINER_NAME
    assert sut.connection_qualified_name == APPLICATION_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == APPLICATION_CONTAINER_QUALIFIED_NAME
    assert sut.connector_name == APPLICATION_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, APPLICATION_CONTAINER_QUALIFIED_NAME, "qualified_name is required"),
        (APPLICATION_CONTAINER_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        ApplicationAsset.create_for_modification(
            qualified_name=qualified_name, name=name
        )


def test_create_for_modification():
    sut = ApplicationAsset.create_for_modification(
        qualified_name=APPLICATION_CONTAINER_QUALIFIED_NAME, name=APPLICATION_CONTAINER_NAME
    )

    assert sut.qualified_name == APPLICATION_CONTAINER_QUALIFIED_NAME
    assert sut.name == APPLICATION_CONTAINER_NAME


def test_trim_to_required():
    sut = ApplicationAsset.create_for_modification(
        name=APPLICATION_CONTAINER_NAME, qualified_name=APPLICATION_CONTAINER_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == APPLICATION_CONTAINER_NAME
    assert sut.qualified_name == APPLICATION_CONTAINER_QUALIFIED_NAME
