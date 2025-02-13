import pytest

from pyatlan.model.assets import CustomEntity
from tests.unit.model.constants import (
    CUSTOM_CONNECTION_QUALIFIED_NAME,
    CUSTOM_CONNECTOR_TYPE,
    CUSTOM_ENTITY_NAME,
    CUSTOM_ENTITY_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (CUSTOM_ENTITY_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        CustomEntity.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    sut = CustomEntity.creator(
        name=CUSTOM_ENTITY_NAME,
        connection_qualified_name=CUSTOM_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == CUSTOM_ENTITY_NAME
    assert sut.connection_qualified_name == CUSTOM_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == CUSTOM_ENTITY_QUALIFIED_NAME
    assert sut.connector_name == CUSTOM_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CUSTOM_CONNECTION_QUALIFIED_NAME, "qualified_name is required"),
        (CUSTOM_ENTITY_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        CustomEntity.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = CustomEntity.updater(
        qualified_name=CUSTOM_ENTITY_QUALIFIED_NAME, name=CUSTOM_ENTITY_NAME
    )

    assert sut.qualified_name == CUSTOM_ENTITY_QUALIFIED_NAME
    assert sut.name == CUSTOM_ENTITY_NAME


def test_trim_to_required():
    sut = CustomEntity.updater(
        name=CUSTOM_ENTITY_NAME, qualified_name=CUSTOM_ENTITY_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == CUSTOM_ENTITY_NAME
    assert sut.qualified_name == CUSTOM_ENTITY_QUALIFIED_NAME
