# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for CosmosMongoDBAccount.creator in pyatlan_v9.

The expected qualifiedName is the exact string atlan-cosmosdb-app and
atlan-cosmosnosql-app emit today (FND-3838 census): {conn}/accounts/{account}.
"""

import pytest

from pyatlan_v9.model import CosmosMongoDBAccount

CONNECTION_QN = "default/cosmos/1712345678"
ACCOUNT_NAME = "sales-account"
ACCOUNT_QN = "default/cosmos/1712345678/accounts/sales-account"


def test_creator_matches_app_qualified_name():
    sut = CosmosMongoDBAccount.creator(
        name=ACCOUNT_NAME, connection_qualified_name=CONNECTION_QN
    )

    assert sut.qualified_name == ACCOUNT_QN
    assert sut.name == ACCOUNT_NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cosmos"
    sut.validate(for_creation=True)


def test_creator_matches_cosmosnosql_qualified_name():
    sut = CosmosMongoDBAccount.creator(
        name=ACCOUNT_NAME,
        connection_qualified_name="default/cosmosnosql/1712345678",
    )

    assert sut.qualified_name == (
        "default/cosmosnosql/1712345678/accounts/sales-account"
    )
    assert sut.connector_name == "cosmosnosql"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QN, "name is required"),
        (" ", CONNECTION_QN, "name cannot be blank"),
        (ACCOUNT_NAME, None, "connection_qualified_name is required"),
        (ACCOUNT_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_rejects_missing_or_blank_inputs(
    name, connection_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CosmosMongoDBAccount.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_create_alias():
    sut = CosmosMongoDBAccount.create(
        name=ACCOUNT_NAME, connection_qualified_name=CONNECTION_QN
    )

    assert sut.qualified_name == ACCOUNT_QN


def test_updater_and_trim_to_required():
    sut = CosmosMongoDBAccount.creator(
        name=ACCOUNT_NAME, connection_qualified_name=CONNECTION_QN
    ).trim_to_required()

    assert isinstance(sut, CosmosMongoDBAccount)
    assert sut.qualified_name == ACCOUNT_QN
    assert sut.name == ACCOUNT_NAME

    updated = CosmosMongoDBAccount.create_for_modification(
        qualified_name=ACCOUNT_QN, name=ACCOUNT_NAME
    )
    assert isinstance(updated, CosmosMongoDBAccount)
    assert updated.qualified_name == ACCOUNT_QN
