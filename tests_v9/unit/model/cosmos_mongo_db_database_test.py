# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for CosmosMongoDBDatabase.creator in pyatlan_v9.

The expected qualifiedName is the exact string atlan-cosmosdb-app and
atlan-cosmosnosql-app emit today (FND-3838 census):
{conn}/accounts/{account}/databases/{db}.
"""

import pytest

from pyatlan_v9.model import CosmosMongoDBDatabase

CONNECTION_QN = "default/cosmos/1712345678"
ACCOUNT_QN = "default/cosmos/1712345678/accounts/sales-account"
DATABASE_NAME = "orders"
DATABASE_QN = "default/cosmos/1712345678/accounts/sales-account/databases/orders"


@pytest.mark.parametrize("connection_qualified_name", [None, CONNECTION_QN])
def test_creator_matches_app_qualified_name(connection_qualified_name):
    sut = CosmosMongoDBDatabase.creator(
        name=DATABASE_NAME,
        cosmos_mongo_db_account_qualified_name=ACCOUNT_QN,
        connection_qualified_name=connection_qualified_name,
    )

    assert sut.qualified_name == DATABASE_QN
    assert sut.name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cosmos"
    assert sut.cosmos_mongo_db_account_qualified_name == ACCOUNT_QN
    assert sut.cosmos_mongo_db_account.unique_attributes == {
        "qualifiedName": ACCOUNT_QN
    }
    sut.validate(for_creation=True)


def test_creator_uses_explicit_connection_qualified_name():
    sut = CosmosMongoDBDatabase.creator(
        name=DATABASE_NAME,
        cosmos_mongo_db_account_qualified_name=ACCOUNT_QN,
        connection_qualified_name="default/cosmosnosql/1700000000",
    )

    assert sut.qualified_name == DATABASE_QN
    assert sut.connection_qualified_name == "default/cosmosnosql/1700000000"
    assert sut.connector_name == "cosmosnosql"


@pytest.mark.parametrize(
    "name, account_qualified_name, message",
    [
        (None, ACCOUNT_QN, "name is required"),
        (" ", ACCOUNT_QN, "name cannot be blank"),
        (DATABASE_NAME, None, "cosmos_mongo_db_account_qualified_name is required"),
        (
            DATABASE_NAME,
            " ",
            "cosmos_mongo_db_account_qualified_name cannot be blank",
        ),
        (
            DATABASE_NAME,
            "default/cosmos/1712345678",
            "cosmos_mongo_db_account_qualified_name is invalid",
        ),
    ],
)
def test_creator_rejects_missing_blank_or_invalid_inputs(
    name, account_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CosmosMongoDBDatabase.creator(
            name=name, cosmos_mongo_db_account_qualified_name=account_qualified_name
        )


def test_create_alias():
    sut = CosmosMongoDBDatabase.create(
        name=DATABASE_NAME, cosmos_mongo_db_account_qualified_name=ACCOUNT_QN
    )

    assert sut.qualified_name == DATABASE_QN


def test_updater_and_trim_to_required():
    sut = CosmosMongoDBDatabase.creator(
        name=DATABASE_NAME, cosmos_mongo_db_account_qualified_name=ACCOUNT_QN
    ).trim_to_required()

    assert isinstance(sut, CosmosMongoDBDatabase)
    assert sut.qualified_name == DATABASE_QN
    assert sut.name == DATABASE_NAME

    updated = CosmosMongoDBDatabase.create_for_modification(
        qualified_name=DATABASE_QN, name=DATABASE_NAME
    )
    assert isinstance(updated, CosmosMongoDBDatabase)
    assert updated.qualified_name == DATABASE_QN
