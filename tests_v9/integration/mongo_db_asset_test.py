# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, MongoDBCollection, MongoDBDatabase
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("MONGODB")
DATABASE_NAME = f"db_{MODULE_NAME}"
COLLECTION_NAME = f"coll_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.MONGODB
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, connection: Connection
) -> Generator[MongoDBDatabase, None, None]:
    to_create = MongoDBDatabase.creator(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=MongoDBDatabase)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MongoDBDatabase)


@pytest.fixture(scope="module")
def collection(
    client: AtlanClient, database: MongoDBDatabase
) -> Generator[MongoDBCollection, None, None]:
    to_create = MongoDBCollection.creator(
        name=COLLECTION_NAME, database_qualified_name=database.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=MongoDBCollection)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MongoDBCollection)


def test_database(
    client: AtlanClient, connection: Connection, database: MongoDBDatabase
):
    assert database.guid
    assert database.qualified_name == f"{connection.qualified_name}/{DATABASE_NAME}"
    retrieved = client.asset.get_by_qualified_name(
        database.qualified_name, asset_type=MongoDBDatabase
    )
    assert retrieved.guid == database.guid
    assert retrieved.name == DATABASE_NAME
    assert retrieved.connector_name == AtlanConnectorType.MONGODB
    assert retrieved.connection_qualified_name == connection.qualified_name


def test_collection(
    client: AtlanClient,
    connection: Connection,
    database: MongoDBDatabase,
    collection: MongoDBCollection,
):
    assert collection.guid
    assert collection.qualified_name == (
        f"{connection.qualified_name}/{DATABASE_NAME}/{COLLECTION_NAME}"
    )
    retrieved = client.asset.get_by_qualified_name(
        collection.qualified_name,
        asset_type=MongoDBCollection,
        ignore_relationships=False,
    )
    assert retrieved.guid == collection.guid
    assert retrieved.name == COLLECTION_NAME
    assert retrieved.connector_name == AtlanConnectorType.MONGODB
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert retrieved.database_name == DATABASE_NAME
    assert retrieved.database_qualified_name == database.qualified_name
    assert retrieved.mongo_db_database
    assert retrieved.mongo_db_database.guid == database.guid


def test_collection_updater(client: AtlanClient, collection: MongoDBCollection):
    to_update = MongoDBCollection.updater(
        qualified_name=collection.qualified_name, name=collection.name
    )
    to_update.description = "updated by mongo_db_asset_test"
    response = client.asset.save(to_update)
    updated = response.assets_updated(asset_type=MongoDBCollection)
    assert len(updated) == 1
    assert updated[0].guid == collection.guid
