# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Column model in pyatlan_v9 - exact parity with tests/unit/model/column_test.py."""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import (
    Column,
    DocumentDBCollection,
    MaterialisedView,
    MongoDBCollection,
    Schema,
    SnowflakeDynamicTable,
    Table,
    View,
)
from tests_v9.unit.model.constants import (
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
            "parent_column is required when parent_type is Column",
        ),
        (
            COLUMN_NAME,
            TABLE_QUALIFIED_NAME,
            Schema,
            1,
            "parent_type must be either Table",
        ),
    ],
)
def test_create_with_missing_parameters_raise_value_error(
    name: str, parent_qualified_name: str, parent_type: type, order: int, message: str
):
    """Test that creator raises ValueError when required parameters are missing or invalid."""
    with pytest.raises(ValueError, match=message):
        Column.creator(
            name=name,
            parent_qualified_name=parent_qualified_name,
            parent_type=parent_type,
            order=order,
        )


def test_create_when_parent_is_table():
    """Test creating Column when parent is Table."""
    sut = Column.creator(
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
    assert sut.table_name == TABLE_NAME


def test_create_when_parent_is_snowflake_dynamic_table():
    """Test creating Column when parent is SnowflakeDynamicTable."""
    sut = Column.creator(
        name=COLUMN_NAME,
        parent_qualified_name=TABLE_QUALIFIED_NAME,
        parent_type=SnowflakeDynamicTable,
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
    assert sut.snowflake_dynamic_table.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.table_name == TABLE_NAME


def test_create_when_parent_is_view():
    """Test creating Column when parent is View."""
    sut = Column.creator(
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
    """Test creator with all optional parameters provided."""
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
    assert sut.view_name == VIEW_NAME


def test_create_when_parent_is_materialized_view():
    """Test creating Column when parent is MaterialisedView."""
    sut = Column.creator(
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
    assert sut.view_name == VIEW_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, TABLE_COLUMN_QUALIFIED_NAME, "qualified_name is required"),
        (COLUMN_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Column.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a Column instance for modification."""
    sut = Column.updater(qualified_name=TABLE_COLUMN_QUALIFIED_NAME, name=COLUMN_NAME)

    assert sut.qualified_name == TABLE_COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME


def test_trim_to_required():
    """Test that trim_to_required returns Column with only required fields."""
    sut = Column.updater(
        qualified_name=TABLE_COLUMN_QUALIFIED_NAME, name=COLUMN_NAME
    ).trim_to_required()

    assert sut.qualified_name == TABLE_COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME


# Non-standard depths and nested columns (FND-3887). Each qualifiedName is the literal
# string the connector app emits today.

FABRIC_CONNECTION_QN = "default/fabric/1700000000"
FABRIC_TABLE_QN = "default/fabric/1700000000/ws-1234/lh-5678/dbo/sales"
WORKDAY_CONNECTION_QN = "default/workdayprismanalytics/1700000000"
GLUE_TABLE_QN = "default/glue/1700000000/AwsDataCatalog/sales_db/orders"
DOCUMENTDB_COLLECTION_QN = "default/documentdb/1700000000/sample_db/orders"
MONGODB_COLLECTION_QN = "default/mongodb/1700000000/sample_db/orders"


def test_creator_fabric_six_segment_parent():
    sut = Column.creator(
        name="amount",
        parent_qualified_name=FABRIC_TABLE_QN,
        parent_type=Table,
        order=3,
        database_name="Lakehouse",
        database_qualified_name="default/fabric/1700000000/ws-1234/lh-5678",
        connection_qualified_name=FABRIC_CONNECTION_QN,
    )

    assert (
        sut.qualified_name
        == "default/fabric/1700000000/ws-1234/lh-5678/dbo/sales/amount"
    )
    assert sut.connector_name == "fabric"
    assert sut.connection_qualified_name == FABRIC_CONNECTION_QN
    assert sut.database_name == "Lakehouse"
    assert sut.database_qualified_name == "default/fabric/1700000000/ws-1234/lh-5678"
    assert sut.table_name == "sales"
    assert sut.table_qualified_name == FABRIC_TABLE_QN
    assert sut.table.unique_attributes["qualifiedName"] == FABRIC_TABLE_QN
    sut.validate(for_creation=True)


def test_creator_schema_less_table_parent():
    sut = Column.creator(
        name="Employee_ID",
        parent_qualified_name=f"{WORKDAY_CONNECTION_QN}/Workers",
        parent_type=Table,
        order=1,
        connection_qualified_name=WORKDAY_CONNECTION_QN,
    )

    assert (
        sut.qualified_name
        == "default/workdayprismanalytics/1700000000/Workers/Employee_ID"
    )
    assert sut.table_name == "Workers"
    assert sut.database_name is UNSET
    assert sut.schema_name is UNSET
    sut.validate(for_creation=True)


def test_creator_explicit_connection_on_standard_depth_derives_parents():
    sut = Column.creator(
        name=COLUMN_NAME,
        parent_qualified_name=TABLE_QUALIFIED_NAME,
        parent_type=Table,
        order=1,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == TABLE_COLUMN_QUALIFIED_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.table_name == TABLE_NAME


@pytest.mark.parametrize(
    "kwargs, message",
    [
        (
            {"connection_qualified_name": "default/fabric/1700000001"},
            "parent_qualified_name is invalid",
        ),
        (
            {"connection_qualified_name": FABRIC_CONNECTION_QN, "database_name": " "},
            "database_name cannot be blank",
        ),
        (
            {"connection_qualified_name": FABRIC_CONNECTION_QN, "parent_name": ""},
            "parent_name cannot be blank",
        ),
        (
            {"connection_qualified_name": ""},
            "connection_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_explicit_parents_invalid(kwargs: dict, message: str):
    with pytest.raises(ValueError, match=message):
        Column.creator(
            name="amount",
            parent_qualified_name=FABRIC_TABLE_QN,
            parent_type=Table,
            order=1,
            **kwargs,
        )


def test_creator_mongodb_collection_parent():
    sut = Column.creator(
        name="address",
        parent_qualified_name=MONGODB_COLLECTION_QN,
        parent_type=MongoDBCollection,
        order=1,
    )

    assert sut.qualified_name == "default/mongodb/1700000000/sample_db/orders/address"
    assert sut.connector_name == "mongodb"
    assert sut.connection_qualified_name == "default/mongodb/1700000000"
    assert sut.database_name == "sample_db"
    assert sut.database_qualified_name == "default/mongodb/1700000000/sample_db"
    assert sut.schema_name is UNSET
    assert sut.nosql_collection_name == "orders"
    assert sut.nosql_collection_qualified_name == MONGODB_COLLECTION_QN
    assert (
        sut.mongo_db_collection.unique_attributes["qualifiedName"]
        == MONGODB_COLLECTION_QN
    )
    assert sut.table is UNSET


def test_creator_documentdb_collection_parent():
    sut = Column.creator(
        name="address",
        parent_qualified_name=DOCUMENTDB_COLLECTION_QN,
        parent_type=DocumentDBCollection,
        order=0,
    )

    assert (
        sut.qualified_name == "default/documentdb/1700000000/sample_db/orders/address"
    )
    assert sut.table.type_name == "DocumentDBCollection"
    assert sut.table_name == "orders"
    assert sut.table_qualified_name == DOCUMENTDB_COLLECTION_QN
    assert sut.nosql_collection_qualified_name == DOCUMENTDB_COLLECTION_QN
    sut.validate(for_creation=True)


def test_creator_collection_parent_wrong_depth():
    with pytest.raises(ValueError, match="Invalid parent_qualified_name"):
        Column.creator(
            name="address",
            parent_qualified_name=f"{MONGODB_COLLECTION_QN}/extra",
            parent_type=MongoDBCollection,
            order=1,
        )


def test_creator_nested_columns_documentdb():
    top = Column.creator(
        name="address",
        parent_qualified_name=DOCUMENTDB_COLLECTION_QN,
        parent_type=DocumentDBCollection,
        order=1,
    )
    child = Column.creator(
        name="geo",
        parent_qualified_name=top.qualified_name,
        parent_type=Column,
        order=2,
        parent_column=top,
    )
    grandchild = Column.creator(
        name="lat",
        parent_qualified_name=child.qualified_name,
        parent_type=Column,
        order=3,
        parent_column=child,
    )

    assert (
        child.qualified_name
        == "default/documentdb/1700000000/sample_db/orders/address/geo"
    )
    assert child.parent_column.unique_attributes["qualifiedName"] == top.qualified_name
    assert child.parent_column_qualified_name == top.qualified_name
    assert child.parent_column_name == "address"
    assert child.column_depth_level == 2
    assert child.column_hierarchy == [
        {"depth": "1", "name": "address", "qualifiedName": top.qualified_name}
    ]
    assert child.table_qualified_name == DOCUMENTDB_COLLECTION_QN
    assert child.table.type_name == "DocumentDBCollection"
    assert child.database_qualified_name == "default/documentdb/1700000000/sample_db"

    assert grandchild.qualified_name == (
        "default/documentdb/1700000000/sample_db/orders/address/geo/lat"
    )
    assert grandchild.column_depth_level == 3
    assert grandchild.column_hierarchy == [
        {"depth": "1", "name": "address", "qualifiedName": top.qualified_name},
        {"depth": "2", "name": "geo", "qualifiedName": child.qualified_name},
    ]
    grandchild.validate(for_creation=True)


def test_creator_nested_column_glue_keeps_parent_depth_convention():
    top = Column.creator(
        name="items",
        parent_qualified_name=GLUE_TABLE_QN,
        parent_type=Table,
        order=1,
    )
    top.column_depth_level = 0  # glue numbers top-level columns from 0
    child = Column.creator(
        name="sku",
        parent_qualified_name=top.qualified_name,
        parent_type=Column,
        order=1,
        parent_column=top,
    )

    assert (
        child.qualified_name
        == "default/glue/1700000000/AwsDataCatalog/sales_db/orders/items/sku"
    )
    assert child.column_depth_level == 1
    assert (
        child.schema_qualified_name == "default/glue/1700000000/AwsDataCatalog/sales_db"
    )
    assert child.table.unique_attributes["qualifiedName"] == GLUE_TABLE_QN
    child.validate(for_creation=True)


def test_creator_nested_column_parent_mismatch():
    top = Column.creator(
        name="items", parent_qualified_name=GLUE_TABLE_QN, parent_type=Table, order=1
    )
    with pytest.raises(ValueError, match="parent_column does not match"):
        Column.creator(
            name="sku",
            parent_qualified_name=f"{GLUE_TABLE_QN}/other",
            parent_type=Column,
            order=1,
            parent_column=top,
        )
