# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the CassandraColumn creator in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-cassandra-dse-app emits today
(``app/asset_mapper.py`` ``build_column_qn``), so a creator change that would re-key
existing Cassandra assets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import (
    CassandraColumn,
    CassandraIndex,
    CassandraTable,
    CassandraView,
)

CONNECTION_QN = "default/cassandra/1712345678"
TABLE_QN = "default/cassandra/1712345678/sales_ks/orders"
VIEW_QN = "default/cassandra/1712345678/sales_ks/orders_by_customer"
NAME = "order_id"
QUALIFIED_NAME = "default/cassandra/1712345678/sales_ks/orders/order_id"


def test_table_column_matches_app_qualified_name():
    """Mirror build_column_qn(conn_qn, keyspace, table_name, column) for a table."""
    sut = CassandraColumn.creator(
        name="order_id",
        parent_qualified_name="default/cassandra/1712345678/sales_ks/orders",
        parent_type=CassandraTable,
    )

    assert sut.qualified_name == "default/cassandra/1712345678/sales_ks/orders/order_id"
    assert sut.name == "order_id"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cassandra"
    assert sut.cassandra_keyspace_name == "sales_ks"
    assert sut.cassandra_table_name == "orders"
    assert sut.cassandra_table_qualified_name == TABLE_QN
    assert sut.cassandra_table.qualified_name == TABLE_QN
    assert sut.cassandra_view is UNSET
    sut.validate(for_creation=True)


def test_view_column_matches_app_qualified_name():
    """Mirror build_column_qn for a view column (table_name is the view name)."""
    sut = CassandraColumn.creator(
        name="order_id",
        parent_qualified_name="default/cassandra/1712345678/sales_ks/orders_by_customer",
        parent_type=CassandraView,
    )

    assert (
        sut.qualified_name
        == "default/cassandra/1712345678/sales_ks/orders_by_customer/order_id"
    )
    assert sut.cassandra_keyspace_name == "sales_ks"
    assert sut.cassandra_view_name == "orders_by_customer"
    assert sut.cassandra_view_qualified_name == VIEW_QN
    assert sut.cassandra_view.qualified_name == VIEW_QN
    assert sut.cassandra_table is UNSET
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection_qualified_name():
    sut = CassandraColumn.creator(
        name=NAME,
        parent_qualified_name=TABLE_QN,
        parent_type=CassandraTable,
        connection_qualified_name=CONNECTION_QN,
    )

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QN


@pytest.mark.parametrize(
    "name, parent_qualified_name, parent_type, message",
    [
        (None, TABLE_QN, CassandraTable, "name is required"),
        (" ", TABLE_QN, CassandraTable, "name cannot be blank"),
        (NAME, None, CassandraTable, "parent_qualified_name is required"),
        (NAME, " ", CassandraTable, "parent_qualified_name cannot be blank"),
        (NAME, TABLE_QN, None, "parent_type is required"),
        (NAME, TABLE_QN, CassandraIndex, "CassandraTable or CassandraView"),
        (
            NAME,
            "default/cassandra/1712345678/sales_ks",
            CassandraTable,
            "parent_qualified_name must be",
        ),
    ],
)
def test_creator_with_invalid_parameters_raises_value_error(
    name, parent_qualified_name, parent_type, message
):
    with pytest.raises(ValueError, match=message):
        CassandraColumn.creator(
            name=name,
            parent_qualified_name=parent_qualified_name,
            parent_type=parent_type,
        )


def test_validate_for_creation_requires_a_parent():
    sut = CassandraColumn.creator(
        name=NAME, parent_qualified_name=TABLE_QN, parent_type=CassandraTable
    )
    sut.cassandra_table = UNSET

    with pytest.raises(ValueError, match="one of cassandra_table, cassandra_view"):
        sut.validate(for_creation=True)


def test_create_alias():
    sut = CassandraColumn.create(
        name=NAME, parent_qualified_name=TABLE_QN, parent_type=CassandraTable
    )

    assert sut.qualified_name == QUALIFIED_NAME


def test_updater():
    sut = CassandraColumn.updater(qualified_name=QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        ("", NAME, "qualified_name is required"),
        (QUALIFIED_NAME, "", "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        CassandraColumn.updater(qualified_name=qualified_name, name=name)


def test_trim_to_required():
    sut = CassandraColumn.updater(
        qualified_name=QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME
