# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the CassandraKeyspace creator in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-cassandra-dse-app emits today
(``app/asset_mapper.py`` ``build_keyspace_qn``), so a creator change that would re-key
existing Cassandra assets fails here.
"""

import pytest

from pyatlan_v9.model import CassandraKeyspace

CONNECTION_QN = "default/cassandra/1712345678"
NAME = "sales_ks"
QUALIFIED_NAME = "default/cassandra/1712345678/sales_ks"


def test_creator_matches_app_qualified_name():
    """Mirror build_keyspace_qn(conn_qn, keyspace)."""
    sut = CassandraKeyspace.creator(
        name="sales_ks", connection_qualified_name="default/cassandra/1712345678"
    )

    assert sut.qualified_name == "default/cassandra/1712345678/sales_ks"
    assert sut.name == "sales_ks"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cassandra"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QN, "name is required"),
        (" ", CONNECTION_QN, "name cannot be blank"),
        (NAME, None, "connection_qualified_name is required"),
        (NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_or_blank_parameters_raises_value_error(
    name, connection_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CassandraKeyspace.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_create_alias():
    sut = CassandraKeyspace.create(name=NAME, connection_qualified_name=CONNECTION_QN)

    assert sut.qualified_name == QUALIFIED_NAME


def test_updater():
    sut = CassandraKeyspace.updater(qualified_name=QUALIFIED_NAME, name=NAME)

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
        CassandraKeyspace.updater(qualified_name=qualified_name, name=name)


def test_trim_to_required():
    sut = CassandraKeyspace.updater(
        qualified_name=QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME
