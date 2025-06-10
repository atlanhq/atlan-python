import logging
from typing import Callable, Optional

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Asset,
    Connection,
    DocumentDBCollection,
    DocumentDBDatabase,
)
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.response import AssetMutationResponse
from tests.integration.client import TestId
from tests.integration.test_sql_assets import verify_asset_updated

LOGGER = logging.getLogger(__name__)


class TestConnection:
    connection: Optional[Connection] = None

    def test_creator(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        role = client.role_cache.get_id_for_name("$admin")
        assert role
        connection_name = TestId.make_unique("DOC_Conn")
        c = Connection.creator(
            client=client,
            name=connection_name,
            connector_type=AtlanConnectorType.DOCUMENTDB,
            admin_roles=[role],
        )
        assert c.guid
        response = upsert(c)
        assert response.mutated_entities
        assert response.mutated_entities.CREATE
        assert len(response.mutated_entities.CREATE) == 1
        assert isinstance(response.mutated_entities.CREATE[0], Connection)
        assert response.guid_assignments
        assert c.guid in response.guid_assignments
        c = response.mutated_entities.CREATE[0]
        c = client.asset.get_by_guid(c.guid, Connection, ignore_relationships=False)
        assert isinstance(c, Connection)
        TestConnection.connection = c

    @pytest.mark.order(after="test_create")
    def test_trim_to_required(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestConnection.connection
        connection = TestConnection.connection.trim_to_required()
        response = upsert(connection)
        assert response.mutated_entities is None


@pytest.mark.order(after="TestConnection")
class TestDatabase:
    database: Optional[DocumentDBDatabase] = None

    def test_creator(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        assert TestConnection.connection
        connection = TestConnection.connection
        assert connection
        assert connection.qualified_name
        database_name = TestId.make_unique("DocDB")
        database = DocumentDBDatabase.creator(
            name=database_name,
            connection_qualified_name=connection.qualified_name,
        )
        assert database.guid
        response = upsert(database)
        assert response.mutated_entities
        assert response.mutated_entities.CREATE
        assert connection.qualified_name == database.connection_qualified_name
        assert len(response.mutated_entities.CREATE) == 1
        assert isinstance(response.mutated_entities.CREATE[0], DocumentDBDatabase)
        assert response.guid_assignments
        assert database.guid in response.guid_assignments
        database = response.mutated_entities.CREATE[0]
        client.asset.get_by_guid(
            database.guid, DocumentDBDatabase, ignore_relationships=False
        )
        TestDatabase.database = database

    @pytest.mark.order(after="test_creator")
    def test_updater(self, client, upsert: Callable[[Asset], AssetMutationResponse]):
        assert TestDatabase.database
        assert TestDatabase.database.qualified_name
        assert TestDatabase.database.name
        database = DocumentDBDatabase.updater(
            qualified_name=TestDatabase.database.qualified_name,
            name=TestDatabase.database.name,
        )
        description = f"{TestDatabase.database.description} more stuff"
        database.description = description
        response = upsert(database)
        verify_asset_updated(response, DocumentDBDatabase)

    @pytest.mark.order(after="test_creator")
    def test_trim_to_required(
        self, client, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestDatabase.database
        database = TestDatabase.database.trim_to_required()
        response = upsert(database)
        assert response.mutated_entities is None


@pytest.mark.order(after="TestDatabase")
class TestCollection:
    collection: Optional[DocumentDBCollection] = None

    def test_creator(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        assert TestConnection.connection
        connection = TestConnection.connection
        assert connection
        assert connection.qualified_name
        assert TestDatabase.database
        database = TestDatabase.database
        assert database
        assert database.qualified_name
        collection_name = TestId.make_unique("DocDBColl")
        collection = DocumentDBCollection.creator(
            name=collection_name,
            database_qualified_name=database.qualified_name,
            connection_qualified_name=connection.qualified_name,
        )
        assert collection.guid
        response = upsert(collection)
        assert response.mutated_entities
        assert response.mutated_entities.CREATE
        assert len(response.mutated_entities.CREATE) == 1
        assert isinstance(response.mutated_entities.CREATE[0], DocumentDBCollection)
        assert response.guid_assignments
        assert collection.guid in response.guid_assignments
        collection = response.mutated_entities.CREATE[0]
        client.asset.get_by_guid(
            collection.guid, DocumentDBCollection, ignore_relationships=False
        )
        TestCollection.collection = collection

    @pytest.mark.order(after="test_creator")
    def test_updater(self, client, upsert: Callable[[Asset], AssetMutationResponse]):
        assert TestCollection.collection
        assert TestCollection.collection.qualified_name
        assert TestCollection.collection.name
        collection = DocumentDBCollection.updater(
            qualified_name=TestCollection.collection.qualified_name,
            name=TestCollection.collection.name,
        )
        description = f"{TestCollection.collection.description} more stuff"
        collection.description = description
        response = upsert(collection)
        verify_asset_updated(response, DocumentDBCollection)

    @pytest.mark.order(after="test_creator")
    def test_trim_to_required(
        self, client, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestCollection.collection
        collection = TestCollection.collection.trim_to_required()
        response = upsert(collection)
        assert response.mutated_entities is None
