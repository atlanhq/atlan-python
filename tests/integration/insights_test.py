# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Collection, Folder, Query, Schema
from pyatlan.model.enums import AtlanConnectorType, EntityStatus
from pyatlan.model.fluent_search import FluentSearch
from tests.integration.client import TestId, delete_asset

PREFIX = TestId.make_unique("INS")

COLLECTION_NAME = PREFIX
FOLDER_NAME = PREFIX + "_folder"
SUB_FOLDER_NAME = FOLDER_NAME + "_sub"
QUERY_NAME = PREFIX + "_query"
RAW_QUERY = "SELECT * FROM DIM_CUSTOMERS;"
EXISTING_GROUP_NAME = "admins"
CONNECTION_NAME = "development"
DB_NAME = "analytics"
SCHEMA_NAME = "WIDE_WORLD_IMPORTERS"
USER_DESCRIPTION = "Automated testing of the Python SDK."


@pytest.fixture(scope="module")
def collection(client: AtlanClient) -> Generator[Collection, None, None]:
    collection = Collection.creator(client=client, name=COLLECTION_NAME)
    collection.admin_groups = [EXISTING_GROUP_NAME]
    response = client.asset.save(collection)
    result = response.assets_created(asset_type=Collection)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Collection)


@pytest.fixture(scope="module")
def folder(
    client: AtlanClient, collection: Collection
) -> Generator[Folder, None, None]:
    assert collection and collection.qualified_name
    folder = Folder.creator(
        name=FOLDER_NAME, collection_qualified_name=collection.qualified_name
    )
    response = client.asset.save(folder)
    result = response.assets_created(asset_type=Folder)[0]
    updated = response.assets_updated(asset_type=Collection)[0]
    assert (
        updated
        and updated.guid == collection.guid
        and updated.qualified_name == collection.qualified_name
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Folder)


@pytest.fixture(scope="module")
def sub_folder(client: AtlanClient, folder: Folder) -> Generator[Folder, None, None]:
    assert folder and folder.qualified_name
    sub = Folder.creator(
        name=SUB_FOLDER_NAME, parent_folder_qualified_name=folder.qualified_name
    )
    response = client.asset.save(sub)
    result = response.assets_created(asset_type=Folder)[0]
    updated = response.assets_updated(asset_type=Folder)[0]
    assert (
        updated
        and updated.guid == folder.guid
        and updated.qualified_name == folder.qualified_name
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Folder)


@pytest.fixture(scope="module")
def query(client: AtlanClient, folder: Folder) -> Generator[Query, None, None]:
    connection = client.find_connections_by_name(
        name=CONNECTION_NAME, connector_type=AtlanConnectorType.SNOWFLAKE
    )
    assert connection and len(connection) == 1 and connection[0].qualified_name
    results = (
        FluentSearch()
        .select()
        .where(Schema.CONNECTION_QUALIFIED_NAME.eq(connection[0].qualified_name))
        .where(Schema.DATABASE_NAME.eq(DB_NAME))
        .where(Schema.NAME.eq(SCHEMA_NAME))
        .execute(client=client)
    )
    assert results and len(results.current_page()) == 1
    schema = results.current_page()[0]
    assert schema and schema.qualified_name
    assert folder and folder.qualified_name
    to_create = Query.creator(
        name=QUERY_NAME, parent_folder_qualified_name=folder.qualified_name
    )
    to_create.with_raw_query(
        schema_qualified_name=schema.qualified_name, query=RAW_QUERY
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=Query)[0]
    updated = response.assets_updated(asset_type=Folder)[0]
    assert (
        updated
        and updated.guid == folder.guid
        and updated.qualified_name == folder.qualified_name
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Folder)


def test_create_collection(collection):
    assert collection
    assert collection.name == COLLECTION_NAME
    assert collection.guid and collection.qualified_name


def test_create_folder(folder, collection):
    assert folder
    assert folder.name == FOLDER_NAME
    assert folder.guid and folder.qualified_name
    assert folder.collection_qualified_name == collection.qualified_name
    assert folder.parent_qualified_name == collection.qualified_name


def test_create_sub_folder(sub_folder: Folder, folder: Folder, collection: Collection):
    assert sub_folder
    assert sub_folder.name == SUB_FOLDER_NAME
    assert sub_folder.guid and sub_folder.qualified_name
    assert sub_folder.collection_qualified_name == collection.qualified_name
    assert sub_folder.parent_qualified_name == folder.qualified_name


def test_create_query(
    client: AtlanClient, query: Query, folder: Folder, collection: Collection
):
    assert query
    assert query.name == QUERY_NAME
    assert query.guid and query.qualified_name
    assert query.collection_qualified_name == collection.qualified_name
    assert query.parent_qualified_name == folder.qualified_name


def test_update_query(
    client: AtlanClient,
    collection: Collection,
    folder: Folder,
    query: Query,
):
    query = query.updater(
        name=query.name,
        qualified_name=query.qualified_name,
        collection_qualified_name=collection.qualified_name,
        parent_qualified_name=folder.qualified_name,
    )
    query.user_description = USER_DESCRIPTION
    response = client.asset.save(query)
    updated = response.assets_updated(asset_type=Query)[0]
    assert updated and updated.qualified_name == query.qualified_name


@pytest.mark.order(after="test_update_query")
def test_retrieve_query(
    client: AtlanClient,
    query: Query,
):
    retrieved = client.asset.get_by_guid(query.guid, asset_type=Query)
    assert retrieved
    assert not retrieved.is_incomplete
    assert retrieved.guid == query.guid
    assert retrieved.qualified_name == query.qualified_name
    assert retrieved.name == query.name
    assert retrieved.user_description == USER_DESCRIPTION


@pytest.mark.order(after="test_retrieve_query")
def test_delete_query(
    client: AtlanClient,
    query: Query,
):
    response = client.asset.delete_by_guid(guid=query.guid)
    assert response
    assert not response.assets_created(asset_type=Query)
    assert not response.assets_updated(asset_type=Query)
    deleted = response.assets_deleted(asset_type=Query)

    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == query.guid
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED
    assert deleted[0].qualified_name == query.qualified_name


@pytest.mark.order(after="test_delete_query")
def test_read_deleted_query(
    client: AtlanClient,
    query: Query,
):
    deleted = client.asset.get_by_guid(guid=query.guid, asset_type=Query)
    assert deleted
    assert deleted.status == EntityStatus.DELETED
    assert deleted.guid == query.guid
    assert deleted.qualified_name == query.qualified_name
