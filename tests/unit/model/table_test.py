import pytest

from pyatlan.model.assets import Table
from tests.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
    TABLE_NAME,
    TABLE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, schema_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (TABLE_NAME, None, "schema_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, schema_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Table.create(name=name, schema_qualified_name=schema_qualified_name)


def test_create():
    sut = Table.create(name=TABLE_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    assert sut.name == TABLE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.qualified_name == SCHEMA_QUALIFIED_NAME


def test_overload_creator():
    sut = Table.creator(
        name=TABLE_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == TABLE_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.qualified_name == SCHEMA_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, TABLE_QUALIFIED_NAME, "qualified_name is required"),
        (TABLE_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Table.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Table.create_for_modification(
        qualified_name=TABLE_QUALIFIED_NAME, name=TABLE_NAME
    )

    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.name == TABLE_NAME


def test_trim_to_required():
    sut = Table.create_for_modification(
        qualified_name=TABLE_QUALIFIED_NAME, name=TABLE_NAME
    ).trim_to_required()

    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.name == TABLE_NAME
