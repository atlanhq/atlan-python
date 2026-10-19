# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for CosmosMongoDBCollection.creator in pyatlan_v9.

The expected qualifiedName is the exact string atlan-cosmosdb-app and
atlan-cosmosnosql-app emit today (FND-3838 census):
{conn}/accounts/{account}/databases/{db}/collections/{collection}
(cosmosnosql calls the last segment {container}; same shape).
"""

import pytest

from pyatlan_v9.model import (
    CosmosMongoDBAccount,
    CosmosMongoDBCollection,
    CosmosMongoDBDatabase,
)

CONNECTION_QN = "default/cosmos/1712345678"
ACCOUNT_QN = "default/cosmos/1712345678/accounts/sales-account"
DATABASE_QN = "default/cosmos/1712345678/accounts/sales-account/databases/orders"
COLLECTION_NAME = "line_items"
COLLECTION_QN = (
    "default/cosmos/1712345678/accounts/sales-account/databases/orders"
    "/collections/line_items"
)


@pytest.mark.parametrize("connection_qualified_name", [None, CONNECTION_QN])
def test_creator_matches_app_qualified_name(connection_qualified_name):
    sut = CosmosMongoDBCollection.creator(
        name=COLLECTION_NAME,
        cosmos_mongo_db_database_qualified_name=DATABASE_QN,
        connection_qualified_name=connection_qualified_name,
    )

    assert sut.qualified_name == COLLECTION_QN
    assert sut.name == COLLECTION_NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cosmos"
    assert sut.cosmos_mongo_db_database_qualified_name == DATABASE_QN
    assert sut.database_name == "orders"
    assert sut.database_qualified_name == DATABASE_QN
    assert sut.cosmos_mongo_db_database.unique_attributes == {
        "qualifiedName": DATABASE_QN
    }
    sut.validate(for_creation=True)


def test_creator_uses_explicit_connection_qualified_name():
    sut = CosmosMongoDBCollection.creator(
        name=COLLECTION_NAME,
        cosmos_mongo_db_database_qualified_name=DATABASE_QN,
        connection_qualified_name="default/cosmosnosql/1700000000",
    )

    assert sut.qualified_name == COLLECTION_QN
    assert sut.connection_qualified_name == "default/cosmosnosql/1700000000"
    assert sut.connector_name == "cosmosnosql"


def test_creators_chain_from_account_to_collection():
    account = CosmosMongoDBAccount.creator(
        name="sales-account", connection_qualified_name=CONNECTION_QN
    )
    database = CosmosMongoDBDatabase.creator(
        name="orders", cosmos_mongo_db_account_qualified_name=account.qualified_name
    )
    collection = CosmosMongoDBCollection.creator(
        name=COLLECTION_NAME,
        cosmos_mongo_db_database_qualified_name=database.qualified_name,
    )

    assert collection.qualified_name == COLLECTION_QN


@pytest.mark.parametrize(
    "name, database_qualified_name, message",
    [
        (None, DATABASE_QN, "name is required"),
        (" ", DATABASE_QN, "name cannot be blank"),
        (
            COLLECTION_NAME,
            None,
            "cosmos_mongo_db_database_qualified_name is required",
        ),
        (
            COLLECTION_NAME,
            " ",
            "cosmos_mongo_db_database_qualified_name cannot be blank",
        ),
        (
            COLLECTION_NAME,
            ACCOUNT_QN,
            "cosmos_mongo_db_database_qualified_name is invalid",
        ),
    ],
)
def test_creator_rejects_missing_blank_or_invalid_inputs(
    name, database_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CosmosMongoDBCollection.creator(
            name=name,
            cosmos_mongo_db_database_qualified_name=database_qualified_name,
        )


def test_create_alias():
    sut = CosmosMongoDBCollection.create(
        name=COLLECTION_NAME, cosmos_mongo_db_database_qualified_name=DATABASE_QN
    )

    assert sut.qualified_name == COLLECTION_QN


def test_updater_and_trim_to_required():
    sut = CosmosMongoDBCollection.creator(
        name=COLLECTION_NAME, cosmos_mongo_db_database_qualified_name=DATABASE_QN
    ).trim_to_required()

    assert isinstance(sut, CosmosMongoDBCollection)
    assert sut.qualified_name == COLLECTION_QN
    assert sut.name == COLLECTION_NAME

    updated = CosmosMongoDBCollection.create_for_modification(
        qualified_name=COLLECTION_QN, name=COLLECTION_NAME
    )
    assert isinstance(updated, CosmosMongoDBCollection)
    assert updated.qualified_name == COLLECTION_QN
