import pytest

from pyatlan.model.assets import View
from tests.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
    TABLE_QUALIFIED_NAME,
    VIEW_COLUMN_QUALIFIED_NAME,
    VIEW_NAME,
    VIEW_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, schema_qualified_name, message",
    [
        (None, SCHEMA_QUALIFIED_NAME, "name is required"),
        (VIEW_NAME, None, "schema_qualified_name is required"),
        (VIEW_NAME, CONNECTION_QUALIFIED_NAME, "Invalid schema_qualified_name"),
        (VIEW_NAME, DATABASE_QUALIFIED_NAME, "Invalid schema_qualified_name"),
        (VIEW_NAME, TABLE_QUALIFIED_NAME, "Invalid schema_qualified_name"),
        (VIEW_NAME, VIEW_COLUMN_QUALIFIED_NAME, "Invalid schema_qualified_name"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, schema_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        View.create(name=name, schema_qualified_name=schema_qualified_name)


def test_create():
    sut = View.create(name=VIEW_NAME, schema_qualified_name=SCHEMA_QUALIFIED_NAME)

    assert sut.name == VIEW_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.qualified_name == SCHEMA_QUALIFIED_NAME


def test_overload_creator():
    sut = View.creator(
        name=VIEW_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        database_name=DATABASE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == VIEW_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.atlan_schema.qualified_name == SCHEMA_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, VIEW_QUALIFIED_NAME, "qualified_name is required"),
        (VIEW_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        View.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = View.create_for_modification(
        qualified_name=VIEW_QUALIFIED_NAME, name=VIEW_NAME
    )

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME


def test_trim_to_required():
    sut = View.create_for_modification(
        qualified_name=VIEW_QUALIFIED_NAME, name=VIEW_NAME
    ).trim_to_required()

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME
