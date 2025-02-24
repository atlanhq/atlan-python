import pytest

from pyatlan.model.assets import TablePartition
from tests.unit.model.constants import (
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
    TABLE_NAME,
    TABLE_PARTITION_NAME,
    TABLE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, table_qualified_name, message",
    [
        (None, SCHEMA_QUALIFIED_NAME, "name is required"),
        (TABLE_PARTITION_NAME, None, "table_qualified_name is required"),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, table_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        TablePartition.creator(
            name=name,
            table_qualified_name=table_qualified_name,
        )


def test_creator():
    partition = TablePartition.creator(
        name=TABLE_PARTITION_NAME,
        table_qualified_name=TABLE_QUALIFIED_NAME,
    )

    assert partition.name == TABLE_PARTITION_NAME
    assert partition.database_name == DATABASE_NAME
    assert partition.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert partition.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert partition.qualified_name == f"{SCHEMA_QUALIFIED_NAME}/{TABLE_PARTITION_NAME}"
    assert partition.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert partition.schema_name == SCHEMA_NAME
    assert partition.connector_name == CONNECTOR_TYPE
    assert partition.table_name == TABLE_NAME
    assert partition.table_qualified_name == TABLE_QUALIFIED_NAME


def test_overload_creator():
    partition = TablePartition.creator(
        name=TABLE_PARTITION_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        table_name=TABLE_NAME,
        table_qualified_name=TABLE_QUALIFIED_NAME,
    )

    assert partition.name == TABLE_PARTITION_NAME
    assert partition.database_name == DATABASE_NAME
    assert partition.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert partition.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert partition.qualified_name == f"{SCHEMA_QUALIFIED_NAME}/{TABLE_PARTITION_NAME}"
    assert partition.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert partition.schema_name == SCHEMA_NAME
    assert partition.connector_name == CONNECTOR_TYPE
    assert partition.table_name == TABLE_NAME
    assert partition.table_qualified_name == TABLE_QUALIFIED_NAME
