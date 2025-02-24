import pytest

from pyatlan.model.assets import Schema
from tests.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, database_qualified_name, message",
    [
        (None, DATABASE_QUALIFIED_NAME, "name is required"),
        (SCHEMA_NAME, None, "database_qualified_name is required"),
        (SCHEMA_NAME, "abc", "Invalid database_qualified_name"),
        (SCHEMA_NAME, CONNECTION_QUALIFIED_NAME, "Invalid database_qualified_name"),
        (
            SCHEMA_NAME,
            SCHEMA_QUALIFIED_NAME,
            "Invalid database_qualified_name",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, database_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Schema.create(name=name, database_qualified_name=database_qualified_name)


def test_create():
    sut = Schema.create(
        name=SCHEMA_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    )

    assert sut.name == SCHEMA_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.database.qualified_name == DATABASE_QUALIFIED_NAME


def test_overload_creator():
    sut = Schema.creator(
        name=SCHEMA_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == SCHEMA_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.database.qualified_name == DATABASE_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SCHEMA_QUALIFIED_NAME, "qualified_name is required"),
        (SCHEMA_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Schema.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Schema.create_for_modification(
        qualified_name=SCHEMA_QUALIFIED_NAME, name=SCHEMA_NAME
    )

    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.name == SCHEMA_NAME


def test_trim_to_required():
    sut = Schema.create_for_modification(
        qualified_name=SCHEMA_QUALIFIED_NAME, name=SCHEMA_NAME
    ).trim_to_required()

    assert sut.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.name == SCHEMA_NAME
