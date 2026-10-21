# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DynamoDBLocalSecondaryIndex model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-dynamodb-app emits today
(``{tableQN}/_lsi_/{indexName}``, FND-3838 census), so a creator change that
would re-key existing LSIs fails here.
"""

import msgspec
import pytest

from pyatlan_v9.model import DynamoDBLocalSecondaryIndex

CONNECTION_QUALIFIED_NAME = "default/dynamodb/1700000000"
TABLE_NAME = "orders"
TABLE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{TABLE_NAME}"
INDEX_NAME = "by_customer"
INDEX_QUALIFIED_NAME = f"{TABLE_QUALIFIED_NAME}/_lsi_/{INDEX_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-dynamodb-app's _build_lsi_qualified_name inputs and output."""
    sut = DynamoDBLocalSecondaryIndex.creator(
        name="by_customer",
        table_qualified_name="default/dynamodb/1700000000/orders",
        table_name="orders",
        connection_qualified_name="default/dynamodb/1700000000",
    )

    assert sut.qualified_name == "default/dynamodb/1700000000/orders/_lsi_/by_customer"
    assert sut.table_qualified_name == "default/dynamodb/1700000000/orders"
    assert sut.dynamo_db_table.unique_attributes == {
        "qualifiedName": "default/dynamodb/1700000000/orders"
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, table_qualified_name, message",
    [
        (None, TABLE_QUALIFIED_NAME, "name is required"),
        (" ", TABLE_QUALIFIED_NAME, "name cannot be blank"),
        (INDEX_NAME, None, "table_qualified_name is required"),
        (INDEX_NAME, " ", "table_qualified_name cannot be blank"),
        (INDEX_NAME, CONNECTION_QUALIFIED_NAME, "table_qualified_name is invalid"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, table_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DynamoDBLocalSecondaryIndex.creator(
            name=name, table_qualified_name=table_qualified_name
        )


def test_creator():
    """Test creator derives the table name and connection from the table."""
    sut = DynamoDBLocalSecondaryIndex.creator(
        name=INDEX_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    )

    assert sut.name == INDEX_NAME
    assert sut.qualified_name == INDEX_QUALIFIED_NAME
    assert sut.table_name == TABLE_NAME
    assert sut.table_qualified_name == TABLE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "dynamodb"
    assert sut.dynamo_db_table.type_name == "DynamoDBTable"
    assert sut.dynamo_db_table.unique_attributes == {
        "qualifiedName": TABLE_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts explicit table name and connection qualified names."""
    sut = DynamoDBLocalSecondaryIndex.creator(
        name=INDEX_NAME,
        table_qualified_name=TABLE_QUALIFIED_NAME,
        table_name="override",
        connection_qualified_name="default/dynamodb/1800000000",
    )

    assert sut.qualified_name == INDEX_QUALIFIED_NAME
    assert sut.table_name == "override"
    assert sut.connection_qualified_name == "default/dynamodb/1800000000"
    assert sut.connector_name == "dynamodb"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, INDEX_NAME, "qualified_name is required"),
        (INDEX_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DynamoDBLocalSecondaryIndex.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DynamoDBLocalSecondaryIndex for modification."""
    sut = DynamoDBLocalSecondaryIndex.updater(
        qualified_name=INDEX_QUALIFIED_NAME, name=INDEX_NAME
    )

    assert sut.qualified_name == INDEX_QUALIFIED_NAME
    assert sut.name == INDEX_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DynamoDBLocalSecondaryIndex.creator(
        name=INDEX_NAME, table_qualified_name=TABLE_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.qualified_name == INDEX_QUALIFIED_NAME
    assert sut.name == INDEX_NAME
    assert sut.dynamo_db_table is msgspec.UNSET
