import pytest

from pyatlan.model.assets import Table

DEFAULT = "default"
CONNECTOR_TYPE = "snowflake"
TIME_STAMP = "1686532494/"
DATABASE_NAME = "MyDB"
SCHEMA_NAME = "MySchema"
TABLE_NAME = "MyTable"
CONNECTION_QUALIFIED_NAME = f"{DEFAULT}/{CONNECTOR_TYPE}/{TIME_STAMP}"
DATABASE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{DATABASE_NAME}"
SCHEMA_QUALIFIED_NAME = f"{DATABASE_QUALIFIED_NAME}/{SCHEMA_NAME}"
TABLE_QUALIFIED_NAME = f"{SCHEMA_QUALIFIED_NAME}/{TABLE_NAME}"


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
    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.sch
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
