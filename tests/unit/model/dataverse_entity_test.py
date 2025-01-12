import pytest

from pyatlan.model.assets import DataverseEntity
from tests.unit.model.constants import (
    DATAVERSE_CONNECTION_QUALIFIED_NAME,
    DATAVERSE_CONNECTOR_TYPE,
    DATAVERSE_ENTITY_NAME,
    DATAVERSE_ENTITY_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (DATAVERSE_ENTITY_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DataverseEntity.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    sut = DataverseEntity.creator(
        name=DATAVERSE_ENTITY_NAME,
        connection_qualified_name=DATAVERSE_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == DATAVERSE_ENTITY_NAME
    assert sut.connection_qualified_name == DATAVERSE_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == DATAVERSE_ENTITY_QUALIFIED_NAME
    assert sut.connector_name == DATAVERSE_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATAVERSE_CONNECTION_QUALIFIED_NAME, "qualified_name is required"),
        (DATAVERSE_ENTITY_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DataverseEntity.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = DataverseEntity.updater(
        qualified_name=DATAVERSE_ENTITY_QUALIFIED_NAME, name=DATAVERSE_ENTITY_NAME
    )

    assert sut.qualified_name == DATAVERSE_ENTITY_QUALIFIED_NAME
    assert sut.name == DATAVERSE_ENTITY_NAME


def test_trim_to_required():
    sut = DataverseEntity.updater(
        name=DATAVERSE_ENTITY_NAME, qualified_name=DATAVERSE_ENTITY_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == DATAVERSE_ENTITY_NAME
    assert sut.qualified_name == DATAVERSE_ENTITY_QUALIFIED_NAME
