import pytest

from pyatlan.model.assets import Database
from tests.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (DATABASE_NAME, None, "connection_qualified_name is required"),
        (DATABASE_NAME, "abc", "Invalid connection_qualified_name"),
        (DATABASE_NAME, "default/snowflake", "Invalid connection_qualified_name"),
        (
            DATABASE_NAME,
            "default/snowflke/1686532494/RAW",
            "Invalid connection_qualified_name",
        ),
        (
            DATABASE_NAME,
            "default/snowflake/1686532494/RAW/",
            "Invalid connection_qualified_name",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Database.create(name=name, connection_qualified_name=connection_qualified_name)


def test_create():
    sut = Database.create(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == f"{CONNECTION_QUALIFIED_NAME}/{DATABASE_NAME}"
    assert sut.connector_name == "snowflake"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATABASE_QUALIFIED_NAME, "qualified_name is required"),
        (DATABASE_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Database.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Database.create_for_modification(
        qualified_name=DATABASE_QUALIFIED_NAME, name=DATABASE_NAME
    )

    assert sut.qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.name == DATABASE_NAME


def test_trim_to_required():
    sut = Database.create_for_modification(
        qualified_name=DATABASE_QUALIFIED_NAME, name=DATABASE_NAME
    ).trim_to_required()

    assert sut.qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.name == DATABASE_NAME
