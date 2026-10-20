# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    CosmosMongoDBAccount,
    CosmosMongoDBCollection,
    CosmosMongoDBDatabase,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("COSMOS")

ACCOUNT_NAME = f"account_{MODULE_NAME}"
DATABASE_NAME = f"database_{MODULE_NAME}"
COLLECTION_NAME = f"collection_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.COSMOS
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def account(
    client: AtlanClient, connection: Connection
) -> Generator[CosmosMongoDBAccount, None, None]:
    to_create = CosmosMongoDBAccount.creator(
        name=ACCOUNT_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=CosmosMongoDBAccount
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=CosmosMongoDBAccount)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, account: CosmosMongoDBAccount
) -> Generator[CosmosMongoDBDatabase, None, None]:
    to_create = CosmosMongoDBDatabase.creator(
        name=DATABASE_NAME,
        cosmos_mongo_db_account_qualified_name=account.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=CosmosMongoDBDatabase
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=CosmosMongoDBDatabase)


@pytest.fixture(scope="module")
def collection(
    client: AtlanClient, database: CosmosMongoDBDatabase
) -> Generator[CosmosMongoDBCollection, None, None]:
    to_create = CosmosMongoDBCollection.creator(
        name=COLLECTION_NAME,
        cosmos_mongo_db_database_qualified_name=database.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=CosmosMongoDBCollection
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=CosmosMongoDBCollection)


def _assert_retrieved(client, asset, asset_type, connection, expected_qn):
    assert asset.guid
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == expected_qn
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.COSMOS
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_account(
    client: AtlanClient, connection: Connection, account: CosmosMongoDBAccount
):
    _assert_retrieved(
        client,
        account,
        CosmosMongoDBAccount,
        connection,
        f"{connection.qualified_name}/accounts/{ACCOUNT_NAME}",
    )


def test_database(
    client: AtlanClient,
    connection: Connection,
    account: CosmosMongoDBAccount,
    database: CosmosMongoDBDatabase,
):
    retrieved = _assert_retrieved(
        client,
        database,
        CosmosMongoDBDatabase,
        connection,
        f"{connection.qualified_name}/accounts/{ACCOUNT_NAME}"
        f"/databases/{DATABASE_NAME}",
    )
    assert retrieved.cosmos_mongo_db_account_qualified_name == account.qualified_name
    assert retrieved.cosmos_mongo_db_account.guid == account.guid


def test_collection(
    client: AtlanClient,
    connection: Connection,
    database: CosmosMongoDBDatabase,
    collection: CosmosMongoDBCollection,
):
    retrieved = _assert_retrieved(
        client,
        collection,
        CosmosMongoDBCollection,
        connection,
        f"{connection.qualified_name}/accounts/{ACCOUNT_NAME}"
        f"/databases/{DATABASE_NAME}/collections/{COLLECTION_NAME}",
    )
    assert retrieved.cosmos_mongo_db_database_qualified_name == database.qualified_name
    assert retrieved.database_name == DATABASE_NAME
    assert retrieved.database_qualified_name == database.qualified_name
    assert retrieved.cosmos_mongo_db_database.guid == database.guid
