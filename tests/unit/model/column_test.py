import pytest

from pyatlan.model.assets import Column, MaterialisedView, Table, View
from tests.unit.model.constants import (
    COLUMN_NAME,
    CONNECTION_QUALIFIED_NAME,
    CONNECTOR_TYPE,
    DATABASE_NAME,
    DATABASE_QUALIFIED_NAME,
    SCHEMA_NAME,
    SCHEMA_QUALIFIED_NAME,
    TABLE_COLUMN_QUALIFIED_NAME,
    TABLE_NAME,
    TABLE_QUALIFIED_NAME,
    VIEW_COLUMN_QUALIFIED_NAME,
    VIEW_NAME,
    VIEW_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, parent_qualified_name, parent_type, order, message",
    [
        (None, TABLE_COLUMN_QUALIFIED_NAME, Table, 1, "name is required"),
        (COLUMN_NAME, None, Table, 1, "parent_qualified_name is required"),
        (COLUMN_NAME, TABLE_COLUMN_QUALIFIED_NAME, None, 1, "parent_type is required"),
        (COLUMN_NAME, TABLE_COLUMN_QUALIFIED_NAME, Table, None, "order is required"),
        (
            COLUMN_NAME,
            CONNECTION_QUALIFIED_NAME,
            Table,
            1,
            "Invalid parent_qualified_name",
        ),
        (
            COLUMN_NAME,
            DATABASE_QUALIFIED_NAME,
            Table,
            1,
            "Invalid parent_qualified_name",
        ),
        (COLUMN_NAME, SCHEMA_QUALIFIED_NAME, Table, 1, "Invalid parent_qualified_name"),
        (
            COLUMN_NAME,
            TABLE_COLUMN_QUALIFIED_NAME,
            Table,
            1,
            "Invalid parent_qualified_name",
        ),
        (
            COLUMN_NAME,
            TABLE_QUALIFIED_NAME,
            Table,
            -1,
            "Order must be be a positive integer",
        ),
        (
            COLUMN_NAME,
            TABLE_QUALIFIED_NAME,
            Column,
            1,
            "parent_type must be either Table, View, MaterializeView or TablePartition",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, parent_qualified_name: str, parent_type: type, order: int, message: str
):
    with pytest.raises(ValueError, match=message):
        Column.create(
            name=name,
            parent_qualified_name=parent_qualified_name,
            parent_type=parent_type,
            order=order,
        )


def test_create_when_parent_is_table():
    sut = Column.create(
        name=COLUMN_NAME,
        parent_qualified_name=TABLE_QUALIFIED_NAME,
        parent_type=Table,
        order=1,
    )

    assert sut.name == COLUMN_NAME
    assert sut.qualified_name == TABLE_COLUMN_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.schema_name == SCHEMA_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.order == 1
    assert sut.table_qualified_name == TABLE_QUALIFIED_NAME
    assert sut.table.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.table_name == TABLE_NAME


def test_create_when_parent_is_view():
    sut = Column.create(
        name=COLUMN_NAME,
        parent_qualified_name=VIEW_QUALIFIED_NAME,
        parent_type=View,
        order=1,
    )

    assert sut.name == COLUMN_NAME
    assert sut.qualified_name == VIEW_COLUMN_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.schema_name == SCHEMA_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.order == 1
    assert sut.view_qualified_name == VIEW_QUALIFIED_NAME
    assert sut.view_name == VIEW_NAME


def test_overload_creator():
    sut = Column.creator(
        name=COLUMN_NAME,
        parent_qualified_name=VIEW_QUALIFIED_NAME,
        parent_type=View,
        order=2,
        parent_name=VIEW_NAME,
        database_name=DATABASE_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        schema_name=SCHEMA_NAME,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        table_name=TABLE_NAME,
        table_qualified_name=TABLE_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )
    assert sut.name == COLUMN_NAME
    assert sut.qualified_name == VIEW_COLUMN_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.schema_name == SCHEMA_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.order == 2
    assert sut.view.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.view_name == VIEW_NAME


def test_create_when_parent_is_materialized_view():
    sut = Column.create(
        name=COLUMN_NAME,
        parent_qualified_name=VIEW_QUALIFIED_NAME,
        parent_type=MaterialisedView,
        order=1,
    )

    assert sut.name == COLUMN_NAME
    assert sut.qualified_name == VIEW_COLUMN_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_TYPE
    assert sut.schema_name == SCHEMA_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.order == 1
    assert sut.view_qualified_name == VIEW_QUALIFIED_NAME
    assert sut.materialised_view.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.view_name == VIEW_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, TABLE_COLUMN_QUALIFIED_NAME, "qualified_name is required"),
        (COLUMN_NAME, None, "name is required"),
    ],
)
def test_create_for_modification_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        Column.create_for_modification(qualified_name=qualified_name, name=name)


def test_create_for_modification():
    sut = Column.create_for_modification(
        qualified_name=TABLE_COLUMN_QUALIFIED_NAME, name=COLUMN_NAME
    )

    assert sut.qualified_name == TABLE_COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME


def test_trim_to_required():
    sut = Table.create_for_modification(
        qualified_name=TABLE_COLUMN_QUALIFIED_NAME, name=COLUMN_NAME
    ).trim_to_required()

    assert sut.qualified_name == TABLE_COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME
