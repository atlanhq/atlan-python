# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the CassandraView creator in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-cassandra-dse-app emits today
(``app/asset_mapper.py`` ``build_view_qn``), so a creator change that would re-key
existing Cassandra assets fails here.
"""

import pytest

from pyatlan_v9.model import CassandraView

CONNECTION_QN = "default/cassandra/1712345678"
KEYSPACE_QN = "default/cassandra/1712345678/sales_ks"
NAME = "orders_by_customer"
QUALIFIED_NAME = "default/cassandra/1712345678/sales_ks/orders_by_customer"


def test_creator_matches_app_qualified_name():
    """Mirror build_view_qn(conn_qn, keyspace, view)."""
    sut = CassandraView.creator(
        name="orders_by_customer",
        keyspace_qualified_name="default/cassandra/1712345678/sales_ks",
    )

    assert (
        sut.qualified_name == "default/cassandra/1712345678/sales_ks/orders_by_customer"
    )
    assert sut.name == "orders_by_customer"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cassandra"
    assert sut.cassandra_keyspace_name == "sales_ks"
    assert sut.cassandra_keyspace.qualified_name == KEYSPACE_QN
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection_qualified_name():
    sut = CassandraView.creator(
        name=NAME,
        keyspace_qualified_name=KEYSPACE_QN,
        connection_qualified_name=CONNECTION_QN,
    )

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QN


@pytest.mark.parametrize(
    "name, keyspace_qualified_name, message",
    [
        (None, KEYSPACE_QN, "name is required"),
        (" ", KEYSPACE_QN, "name cannot be blank"),
        (NAME, None, "keyspace_qualified_name is required"),
        (NAME, " ", "keyspace_qualified_name cannot be blank"),
        (NAME, CONNECTION_QN, "keyspace_qualified_name must be"),
    ],
)
def test_creator_with_invalid_parameters_raises_value_error(
    name, keyspace_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CassandraView.creator(
            name=name, keyspace_qualified_name=keyspace_qualified_name
        )


def test_create_alias():
    sut = CassandraView.create(name=NAME, keyspace_qualified_name=KEYSPACE_QN)

    assert sut.qualified_name == QUALIFIED_NAME


def test_updater():
    sut = CassandraView.updater(qualified_name=QUALIFIED_NAME, name=NAME)

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
        CassandraView.updater(qualified_name=qualified_name, name=name)


def test_trim_to_required():
    sut = CassandraView.updater(
        qualified_name=QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME
