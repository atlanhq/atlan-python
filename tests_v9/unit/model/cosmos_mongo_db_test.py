# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Cosmos MongoDB creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-cosmosdb-app and
atlan-cosmosnosql-app emit today (FND-3838 census), so a creator change that would
re-key existing Cosmos MongoDB assets fails here.
"""

import pytest

from pyatlan_v9.model import (
    CosmosMongoDBAccount,
    CosmosMongoDBCollection,
    CosmosMongoDBDatabase,
)

CONNECTION_QN = "default/cosmos/1712345678"
ACCOUNT_NAME = "sales-account"
DATABASE_NAME = "orders"
COLLECTION_NAME = "line_items"

# {conn}/accounts/{account}
ACCOUNT_QN = "default/cosmos/1712345678/accounts/sales-account"
# {conn}/accounts/{account}/databases/{db}
DATABASE_QN = "default/cosmos/1712345678/accounts/sales-account/databases/orders"
# {conn}/accounts/{account}/databases/{db}/collections/{collection}
COLLECTION_QN = (
    "default/cosmos/1712345678/accounts/sales-account/databases/orders"
    "/collections/line_items"
)


def test_account_creator_matches_app_qualified_name():
    sut = CosmosMongoDBAccount.creator(
        name=ACCOUNT_NAME, connection_qualified_name=CONNECTION_QN
    )

    assert sut.qualified_name == ACCOUNT_QN
    assert sut.name == ACCOUNT_NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cosmos"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


@pytest.mark.parametrize("connection_qualified_name", [None, CONNECTION_QN])
def test_database_creator_matches_app_qualified_name(connection_qualified_name):
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
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


@pytest.mark.parametrize("connection_qualified_name", [None, CONNECTION_QN])
def test_collection_creator_matches_app_qualified_name(connection_qualified_name):
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
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QN
    assert sut.cosmos_mongo_db_database.unique_attributes == {
        "qualifiedName": DATABASE_QN
    }
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_creators_chain_from_account_to_collection():
    account = CosmosMongoDBAccount.creator(
        name=ACCOUNT_NAME, connection_qualified_name=CONNECTION_QN
    )
    database = CosmosMongoDBDatabase.creator(
        name=DATABASE_NAME,
        cosmos_mongo_db_account_qualified_name=account.qualified_name,
    )
    collection = CosmosMongoDBCollection.creator(
        name=COLLECTION_NAME,
        cosmos_mongo_db_database_qualified_name=database.qualified_name,
    )

    assert collection.qualified_name == COLLECTION_QN


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QN, "name is required"),
        (ACCOUNT_NAME, None, "connection_qualified_name is required"),
        ("  ", CONNECTION_QN, "name"),
        (ACCOUNT_NAME, "", "connection_qualified_name"),
    ],
)
def test_account_creator_rejects_missing_or_blank_inputs(
    name, connection_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CosmosMongoDBAccount.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


@pytest.mark.parametrize(
    "name, account_qualified_name, message",
    [
        (None, ACCOUNT_QN, "name is required"),
        (DATABASE_NAME, None, "cosmos_mongo_db_account_qualified_name is required"),
        ("  ", ACCOUNT_QN, "name"),
        (DATABASE_NAME, "", "cosmos_mongo_db_account_qualified_name"),
        (DATABASE_NAME, "default/cosmos", "cosmos_mongo_db_account_qualified_name"),
    ],
)
def test_database_creator_rejects_missing_or_invalid_inputs(
    name, account_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CosmosMongoDBDatabase.creator(
            name=name, cosmos_mongo_db_account_qualified_name=account_qualified_name
        )


@pytest.mark.parametrize(
    "name, database_qualified_name, message",
    [
        (None, DATABASE_QN, "name is required"),
        (
            COLLECTION_NAME,
            None,
            "cosmos_mongo_db_database_qualified_name is required",
        ),
        ("  ", DATABASE_QN, "name"),
        (COLLECTION_NAME, "", "cosmos_mongo_db_database_qualified_name"),
        (COLLECTION_NAME, ACCOUNT_QN, "cosmos_mongo_db_database_qualified_name"),
    ],
)
def test_collection_creator_rejects_missing_or_invalid_inputs(
    name, database_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        CosmosMongoDBCollection.creator(
            name=name,
            cosmos_mongo_db_database_qualified_name=database_qualified_name,
        )


@pytest.mark.parametrize(
    "asset_type, kwargs, expected_qn",
    [
        (
            CosmosMongoDBAccount,
            {"name": ACCOUNT_NAME, "connection_qualified_name": CONNECTION_QN},
            ACCOUNT_QN,
        ),
        (
            CosmosMongoDBDatabase,
            {
                "name": DATABASE_NAME,
                "cosmos_mongo_db_account_qualified_name": ACCOUNT_QN,
            },
            DATABASE_QN,
        ),
        (
            CosmosMongoDBCollection,
            {
                "name": COLLECTION_NAME,
                "cosmos_mongo_db_database_qualified_name": DATABASE_QN,
            },
            COLLECTION_QN,
        ),
    ],
)
def test_create_alias(asset_type, kwargs, expected_qn):
    assert asset_type.create(**kwargs).qualified_name == expected_qn


@pytest.mark.parametrize(
    "asset_type, qualified_name, name",
    [
        (CosmosMongoDBAccount, ACCOUNT_QN, ACCOUNT_NAME),
        (CosmosMongoDBDatabase, DATABASE_QN, DATABASE_NAME),
        (CosmosMongoDBCollection, COLLECTION_QN, COLLECTION_NAME),
    ],
)
def test_create_for_modification_alias(asset_type, qualified_name, name):
    sut = asset_type.create_for_modification(qualified_name=qualified_name, name=name)

    assert isinstance(sut, asset_type)
    assert sut.qualified_name == qualified_name
    assert sut.name == name
