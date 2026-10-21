# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the CassandraIndex creator in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-cassandra-dse-app emits today
(``app/asset_mapper.py`` ``build_index_qn``), so a creator change that would re-key
existing Cassandra assets fails here.
"""

import pytest

from pyatlan_v9.model import CassandraIndex

CONNECTION_QN = "default/cassandra/1712345678"
TABLE_QN = "default/cassandra/1712345678/sales_ks/orders"
NAME = "orders_status_idx"
QUALIFIED_NAME = "default/cassandra/1712345678/sales_ks/orders/orders_status_idx"


def test_creator_matches_app_qualified_name():
    """Mirror build_index_qn(conn_qn, keyspace, table, index)."""
    sut = CassandraIndex.creator(
        name="orders_status_idx",
        table_qualified_name="default/cassandra/1712345678/sales_ks/orders",
    )

    assert (
        sut.qualified_name
        == "default/cassandra/1712345678/sales_ks/orders/orders_status_idx"
    )
    assert sut.name == "orders_status_idx"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cassandra"
    assert sut.cassandra_keyspace_name == "sales_ks"
    assert sut.cassandra_table_name == "orders"
    # The app omits this; the typedef requires it, so the creator sets it.
    assert sut.cassandra_table_qualified_name == TABLE_QN
    assert sut.cassandra_table.qualified_name == TABLE_QN
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection_qualified_name():
    sut = CassandraIndex.creator(
        name=NAME,
        table_qualified_name=TABLE_QN,
        connection_qualified_name=CONNECTION_QN,
    )

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QN


@pytest.mark.parametrize(
    "name, table_qualified_name, message",
    [
        (None, TABLE_QN, "name is required"),
        (" ", TABLE_QN, "name cannot be blank"),
        (NAME, None, "table_qualified_name is required"),
        (NAME, " ", "table_qualified_name cannot be blank"),
        (NAME, "default/cassandra/1712345678/sales_ks", "table_qualified_name must be"),
    ],
)
def test_creator_with_invalid_parameters_raises_value_error(
    name, table_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CassandraIndex.creator(name=name, table_qualified_name=table_qualified_name)


def test_create_alias():
    sut = CassandraIndex.create(name=NAME, table_qualified_name=TABLE_QN)

    assert sut.qualified_name == QUALIFIED_NAME


def test_updater():
    sut = CassandraIndex.updater(qualified_name=QUALIFIED_NAME, name=NAME)

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
        CassandraIndex.updater(qualified_name=qualified_name, name=name)


def test_trim_to_required():
    sut = CassandraIndex.updater(
        qualified_name=QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME
