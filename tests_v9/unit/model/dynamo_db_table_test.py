# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DynamoDBTable model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-dynamodb-app emits today
(``{connectionQN}/{tableName}``, FND-3838 census), so a creator change that
would re-key existing tables fails here.
"""

import msgspec
import pytest

from pyatlan_v9.model import DynamoDBTable

CONNECTION_QUALIFIED_NAME = "default/dynamodb/1700000000"
TABLE_NAME = "orders"
TABLE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{TABLE_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-dynamodb-app's _build_table_qualified_name inputs and output."""
    sut = DynamoDBTable.creator(
        name="orders", connection_qualified_name="default/dynamodb/1700000000"
    )

    assert sut.qualified_name == "default/dynamodb/1700000000/orders"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (TABLE_NAME, None, "connection_qualified_name is required"),
        (TABLE_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DynamoDBTable.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator sets the connection and connector."""
    sut = DynamoDBTable.creator(
        name=TABLE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == TABLE_NAME
    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "dynamodb"
    assert sut.guid


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, TABLE_NAME, "qualified_name is required"),
        (TABLE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DynamoDBTable.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DynamoDBTable for modification."""
    sut = DynamoDBTable.updater(qualified_name=TABLE_QUALIFIED_NAME, name=TABLE_NAME)

    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.name == TABLE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DynamoDBTable.creator(
        name=TABLE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.qualified_name == TABLE_QUALIFIED_NAME
    assert sut.name == TABLE_NAME
    assert sut.connection_qualified_name is msgspec.UNSET
