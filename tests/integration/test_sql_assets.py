import datetime
import logging
from typing import Callable, List, Optional, Type

import pytest

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Asset,
    Column,
    Connection,
    Database,
    Readme,
    Schema,
    Table,
    View,
)
from pyatlan.model.enums import AtlanConnectorType, SourceCostUnitType
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.response import A, AssetMutationResponse
from pyatlan.model.structs import PopularityInsights
from tests.integration.client import TestId

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def upsert(client: AtlanClient):
    guids: List[str] = []

    def _upsert(asset: Asset) -> AssetMutationResponse:
        _response = client.asset.save(asset)
        if (
            _response
            and _response.mutated_entities
            and _response.mutated_entities.CREATE
        ):
            guids.append(_response.mutated_entities.CREATE[0].guid)
        return _response

    yield _upsert

    for guid in reversed(guids):
        response = client.asset.purge_by_guid(guid)
        if (
            not response
            or not response.mutated_entities
            or not response.mutated_entities.DELETE
        ):
            LOGGER.error(f"Failed to remove asset with GUID {guid}.")


def verify_asset_created(response, asset_type: Type[A]):
    assert response.mutated_entities


def verify_asset_updated(response, asset_type: Type[A]):
    assert response.mutated_entities
    assert response.mutated_entities.CREATE is None
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 1
    assets = response.assets_updated(asset_type=asset_type)
    assert len(assets) == 1


class TestConnection:
    connection: Optional[Connection] = None

    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        role = RoleCache.get_id_for_name("$admin")
        assert role
        connection_name = TestId.make_unique("INT")
        c = Connection.create(
            name=connection_name,
            connector_type=AtlanConnectorType.SNOWFLAKE,
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
        c = client.asset.get_by_guid(c.guid, Connection)
        assert isinstance(c, Connection)
        TestConnection.connection = c

    @pytest.mark.order(after="test_create")
    def test_create_for_modification(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestConnection.connection
        assert TestConnection.connection.name
        connection = TestConnection.connection
        description = f"{connection.description} more stuff"
        connection = Connection.create_for_modification(
            qualified_name=TestConnection.connection.qualified_name or "",
            name=TestConnection.connection.name,
        )
        connection.description = description
        response = upsert(connection)
        verify_asset_updated(response, Connection)

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
    database: Optional[Database] = None

    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        assert TestConnection.connection
        connection = TestConnection.connection
        assert connection
        assert connection.qualified_name
        database_name = TestId.make_unique("My_Db")
        database = Database.create(
            name=database_name,
            connection_qualified_name=connection.qualified_name,
        )
        assert database.guid
        response = upsert(database)
        assert response.mutated_entities
        assert response.mutated_entities.CREATE
        assert len(response.mutated_entities.CREATE) == 1
        assert isinstance(response.mutated_entities.CREATE[0], Database)
        assert response.guid_assignments
        assert database.guid in response.guid_assignments
        database = response.mutated_entities.CREATE[0]
        client.asset.get_by_guid(database.guid, Database)
        TestDatabase.database = database

    @pytest.mark.order(after="test_create")
    def test_create_for_modification(
        self, client, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestDatabase.database
        assert TestDatabase.database.qualified_name
        assert TestDatabase.database.name
        database = Database.create_for_modification(
            qualified_name=TestDatabase.database.qualified_name,
            name=TestDatabase.database.name,
        )
        description = f"{TestDatabase.database.description} more stuff"
        database.description = description
        response = upsert(database)
        verify_asset_updated(response, Database)

    @pytest.mark.order(after="test_create")
    def test_trim_to_required(
        self, client, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestDatabase.database
        database = TestDatabase.database.trim_to_required()
        response = upsert(database)
        assert response.mutated_entities is None


@pytest.mark.order(after="TestDatabase")
class TestSchema:
    schema: Optional[Schema] = None

    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        schema_name = TestId.make_unique("My_Schema")
        assert TestDatabase.database is not None
        assert TestDatabase.database.qualified_name
        schema = Schema.create(
            name=schema_name,
            database_qualified_name=TestDatabase.database.qualified_name,
        )
        response = upsert(schema)
        assert (schemas := response.assets_created(asset_type=Schema))
        assert len(schemas) == 1
        schema = client.asset.get_by_guid(schemas[0].guid, Schema)
        assert (databases := response.assets_updated(asset_type=Database))
        assert len(databases) == 1
        database = client.asset.get_by_guid(databases[0].guid, Database)
        assert database.attributes.schemas
        schemas = database.attributes.schemas
        assert len(schemas) == 1
        assert schemas[0].guid == schema.guid
        TestSchema.schema = schema

    def test_overload_creator(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        schema_name = TestId.make_unique("My_Overload_Schema")
        assert TestDatabase.database is not None
        assert TestDatabase.database.name
        assert TestDatabase.database.qualified_name
        assert TestConnection.connection is not None
        assert TestConnection.connection.qualified_name

        schema = Schema.creator(
            name=schema_name,
            database_qualified_name=TestDatabase.database.qualified_name,
            database_name=TestDatabase.database.name,
            connection_qualified_name=TestConnection.connection.qualified_name,
        )
        response = upsert(schema)
        assert (schemas := response.assets_created(asset_type=Schema))
        assert len(schemas) == 1
        overload_schema = client.asset.get_by_guid(schemas[0].guid, Schema)
        assert (databases := response.assets_updated(asset_type=Database))
        assert len(databases) == 1
        database = client.asset.get_by_guid(databases[0].guid, Database)
        assert database.attributes.schemas
        schemas = database.attributes.schemas
        assert len(schemas) == 2
        # `database.attributes.schemas` ordering can differ,
        # so it's better to use "in" operator
        schema_guids = [schema.guid for schema in schemas]
        assert TestSchema.schema and TestSchema.schema.guid in schema_guids
        assert overload_schema.guid and overload_schema.guid in schema_guids

    @pytest.mark.order(after="test_create")
    def test_create_for_modification(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestSchema.schema
        schema = TestSchema.schema
        assert schema.qualified_name
        assert schema.name
        description = f"{schema.description} more stuff"
        schema = Schema.create_for_modification(
            qualified_name=schema.qualified_name, name=schema.name
        )
        schema.description = description
        response = upsert(schema)
        verify_asset_updated(response, Schema)

    @pytest.mark.order(after="test_create")
    def test_trim_to_required(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestSchema.schema
        schema = TestSchema.schema.trim_to_required()
        response = upsert(schema)
        assert response.mutated_entities is None


@pytest.mark.order(after="TestSchema")
class TestTable:
    table: Optional[Table] = None

    @pytest.fixture(scope="module")
    def popularity_insight(self):
        popularity = PopularityInsights()
        popularity.record_user = "ernest"
        popularity.record_query_count = 1
        popularity.record_compute_cost = 1.00
        popularity.record_query_count = 2
        popularity.record_total_user_count = 3
        popularity.record_compute_cost_unit = SourceCostUnitType.BYTES
        popularity.record_last_timestamp = datetime.datetime.now()
        popularity.record_query_duration = 4
        popularity.record_warehouse = "there"
        return popularity

    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        table_name = TestId.make_unique("My_Table")
        assert TestSchema.schema is not None
        assert TestSchema.schema.qualified_name
        table = Table.create(
            name=table_name,
            schema_qualified_name=TestSchema.schema.qualified_name,
        )
        response = upsert(table)
        assert (tables := response.assets_created(asset_type=Table))
        assert len(tables) == 1
        table = client.asset.get_by_guid(guid=tables[0].guid, asset_type=Table)
        assert (schemas := response.assets_updated(asset_type=Schema))
        assert len(schemas) == 1
        schema = client.asset.get_by_guid(guid=schemas[0].guid, asset_type=Schema)
        assert schema.attributes.tables
        tables = schema.attributes.tables
        assert len(tables) == 1
        assert tables[0].guid == table.guid
        TestTable.table = table

    def test_overload_creator(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        table_name = TestId.make_unique("My_Overload_Table")
        assert TestSchema.schema is not None
        assert TestSchema.schema.name
        assert TestSchema.schema.qualified_name
        assert TestDatabase.database is not None
        assert TestDatabase.database.name
        assert TestDatabase.database.qualified_name
        assert TestConnection.connection is not None
        assert TestConnection.connection.qualified_name

        table = Table.creator(
            name=table_name,
            schema_qualified_name=TestSchema.schema.qualified_name,
            schema_name=TestSchema.schema.name,
            database_name=TestDatabase.database.name,
            database_qualified_name=TestDatabase.database.qualified_name,
            connection_qualified_name=TestConnection.connection.qualified_name,
        )
        response = upsert(table)
        assert (tables := response.assets_created(asset_type=Table))
        assert len(tables) == 1
        overload_table = client.asset.get_by_guid(guid=tables[0].guid, asset_type=Table)
        assert (schemas := response.assets_updated(asset_type=Schema))
        assert len(schemas) == 1
        schema = client.asset.get_by_guid(guid=schemas[0].guid, asset_type=Schema)
        assert schema.attributes.tables
        tables = schema.attributes.tables
        assert len(tables) == 2
        # `schema.attributes.tables` ordering can differ,
        # so it's better to use "in" operator
        table_guids = [table.guid for table in tables]
        assert TestTable.table and TestTable.table.guid in table_guids
        assert overload_table.guid and overload_table.guid in table_guids

    @pytest.mark.order(after="test_create")
    def test_create_for_modification(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestTable.table
        table = TestTable.table
        assert table.qualified_name
        assert table.name
        description = f"{table.description} more stuff"
        table = Table.create_for_modification(
            qualified_name=table.qualified_name, name=table.name
        )
        table.description = description
        response = upsert(table)
        verify_asset_updated(response, Table)

    @pytest.mark.order(after="test_create")
    def test_trim_to_required(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestTable.table
        table = TestTable.table.trim_to_required()
        response = upsert(table)
        assert response.mutated_entities is None

    @pytest.mark.order(after="test_trim_to_required")
    def test_update_source_read_recent_user_record_list(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
        popularity_insight: PopularityInsights,
    ):
        assert TestTable.table
        table = TestTable.table.trim_to_required()
        self.time = popularity_insight.record_last_timestamp
        table.source_read_recent_user_record_list = [popularity_insight]
        response = upsert(table)
        verify_asset_updated(response, Table)

    @pytest.mark.order(after="test_update_source_read_recent_user_record_list")
    def test_source_read_recent_user_record_list_readable(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
        popularity_insight: PopularityInsights,
    ):
        assert TestTable.table
        asset = client.asset.get_by_guid(guid=TestTable.table.guid, asset_type=Table)
        assert asset.source_read_recent_user_record_list
        asset_popularity = asset.source_read_recent_user_record_list[0]
        self.verify_popularity(asset_popularity, popularity_insight)

    @pytest.mark.order(after="test_update_source_read_recent_user_record_list")
    def test_source_read_recent_user_record_list_readable_with_fluent_search(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
        popularity_insight: PopularityInsights,
    ):
        assert TestTable.table
        assert TestTable.table.qualified_name
        request = (
            FluentSearch.select()
            .where(Asset.QUALIFIED_NAME.eq(TestTable.table.qualified_name))
            .include_on_results(Asset.SOURCE_READ_RECENT_USER_RECORD_LIST)
            .to_request()
        )
        results = client.asset.search(request)
        assert results.count == 1
        for result in results:
            assert result.source_read_recent_user_record_list
            asset_popularity = result.source_read_recent_user_record_list[0]
            self.verify_popularity(asset_popularity, popularity_insight)

    def verify_popularity(self, asset_popularity, popularity_insight):
        assert popularity_insight.record_user == asset_popularity.record_user
        assert (
            popularity_insight.record_query_count == asset_popularity.record_query_count
        )
        assert (
            popularity_insight.record_compute_cost
            == asset_popularity.record_compute_cost
        )
        assert (
            popularity_insight.record_query_count == asset_popularity.record_query_count
        )
        assert (
            popularity_insight.record_total_user_count
            == asset_popularity.record_total_user_count
        )
        assert (
            popularity_insight.record_compute_cost_unit
            == asset_popularity.record_compute_cost_unit
        )
        assert (
            popularity_insight.record_query_duration
            == asset_popularity.record_query_duration
        )
        assert popularity_insight.record_warehouse == asset_popularity.record_warehouse


@pytest.mark.order(after="TestTable")
class TestView:
    view: Optional[View] = None

    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        view_name = TestId.make_unique("My_View")
        assert TestSchema.schema is not None
        assert TestSchema.schema.qualified_name
        view = View.create(
            name=view_name,
            schema_qualified_name=TestSchema.schema.qualified_name,
        )
        response = upsert(view)
        assert response.mutated_entities
        assert response.mutated_entities.CREATE
        assert len(response.mutated_entities.CREATE) == 1
        assert isinstance(response.mutated_entities.CREATE[0], View)
        assert response.guid_assignments
        view = response.mutated_entities.CREATE[0]
        TestView.view = view

    def test_overload_creator(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        view_name = TestId.make_unique("My_View_Overload")
        assert TestDatabase.database is not None
        assert TestDatabase.database.name
        assert TestDatabase.database.qualified_name
        assert TestSchema.schema is not None
        assert TestSchema.schema.name
        assert TestSchema.schema.qualified_name
        assert TestConnection.connection is not None
        assert TestConnection.connection.qualified_name

        view = View.creator(
            name=view_name,
            schema_name=TestSchema.schema.name,
            schema_qualified_name=TestSchema.schema.qualified_name,
            database_name=TestDatabase.database.name,
            database_qualified_name=TestDatabase.database.qualified_name,
            connection_qualified_name=TestConnection.connection.qualified_name,
        )
        response = upsert(view)
        assert response.mutated_entities
        assert response.mutated_entities.CREATE
        assert len(response.mutated_entities.CREATE) == 1
        assert isinstance(response.mutated_entities.CREATE[0], View)
        assert response.guid_assignments

    @pytest.mark.order(after="test_create")
    def test_create_for_modification(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestView.view
        view = TestView.view
        assert view.qualified_name
        assert view.name
        description = f"{view.description} more stuff"
        view = View.create_for_modification(
            qualified_name=view.qualified_name, name=view.name
        )
        view.description = description
        response = upsert(view)
        verify_asset_updated(response, View)

    @pytest.mark.order(after="test_create")
    def test_trim_to_required(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestView.view
        view = TestView.view.trim_to_required()
        response = upsert(view)
        assert response.mutated_entities is None


@pytest.mark.order(after="TestView")
class TestColumn:
    column: Optional[Column] = None

    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        column_name = TestId.make_unique("My_Column")
        assert TestTable.table is not None
        assert TestTable.table.qualified_name
        column = Column.create(
            name=column_name,
            parent_qualified_name=TestTable.table.qualified_name,
            parent_type=Table,
            order=1,
        )
        response = client.asset.save(column)
        assert (columns := response.assets_created(asset_type=Column))
        assert len(columns) == 1
        column = client.asset.get_by_guid(asset_type=Column, guid=columns[0].guid)
        table = client.asset.get_by_guid(asset_type=Table, guid=TestTable.table.guid)
        assert table.attributes.columns
        columns = table.attributes.columns
        assert len(columns) == 1
        assert columns[0].guid == column.guid
        TestColumn.column = column

    def test_overload_creator(
        self,
        client: AtlanClient,
    ):
        column_name = TestId.make_unique("My_Column_Overload")
        assert TestTable.table is not None
        assert TestTable.table.name
        assert TestTable.table.qualified_name
        assert TestDatabase.database is not None
        assert TestDatabase.database.name
        assert TestDatabase.database.qualified_name
        assert TestSchema.schema is not None
        assert TestSchema.schema.name
        assert TestSchema.schema.qualified_name
        assert TestConnection.connection is not None
        assert TestConnection.connection.qualified_name

        column = Column.creator(
            name=column_name,
            parent_type=Table,
            order=2,
            parent_name=TestTable.table.name,
            parent_qualified_name=TestTable.table.qualified_name,
            database_name=TestDatabase.database.name,
            database_qualified_name=TestDatabase.database.qualified_name,
            schema_name=TestSchema.schema.name,
            schema_qualified_name=TestSchema.schema.qualified_name,
            table_name=TestTable.table.name,
            table_qualified_name=TestTable.table.qualified_name,
            connection_qualified_name=TestConnection.connection.qualified_name,
        )
        response = client.asset.save(column)

        assert (columns := response.assets_created(asset_type=Column))
        assert len(columns) == 1
        overload_column = client.asset.get_by_guid(
            asset_type=Column, guid=columns[0].guid
        )
        table = client.asset.get_by_guid(asset_type=Table, guid=TestTable.table.guid)
        assert table.attributes.columns
        columns = table.attributes.columns

        assert len(columns) == 2
        # `table.attributes.columns` ordering can differ,
        # so it's better to use "in" operator
        column_guids = [column.guid for column in columns]
        assert TestColumn.column and TestColumn.column.guid in column_guids
        assert overload_column.guid and overload_column.guid in column_guids
        assert overload_column.attributes
        assert overload_column.attributes.schema_name == TestSchema.schema.name
        assert (
            overload_column.attributes.schema_qualified_name
            == TestSchema.schema.qualified_name
        )
        assert overload_column.attributes.database_name == TestDatabase.database.name
        assert (
            overload_column.attributes.database_qualified_name
            == TestDatabase.database.qualified_name
        )

    @pytest.mark.order(after="test_create")
    def test_create_for_modification(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestColumn.column
        column = TestColumn.column
        assert column.qualified_name
        assert column.name
        description = f"{column.description} more stuff"
        column = Column.create_for_modification(
            qualified_name=column.qualified_name, name=column.name
        )
        column.description = description
        response = upsert(column)
        verify_asset_updated(response, Column)

    @pytest.mark.order(after="test_create")
    def test_trim_to_required(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestColumn.column
        column = TestColumn.column.trim_to_required()
        response = upsert(column)
        assert response.mutated_entities is None


@pytest.mark.order(after="TestColumn")
class TestReadme:
    readme: Optional[Readme] = None

    def test_create(
        self,
        client: AtlanClient,
        upsert: Callable[[Asset], AssetMutationResponse],
    ):
        assert TestColumn.column
        readme = Readme.create(asset=TestColumn.column, content="<h1>Important</h1>")
        response = upsert(readme)
        assert (reaadmes := response.assets_created(asset_type=Readme))
        assert len(reaadmes) == 1
        assert (columns := response.assets_updated(asset_type=Column))
        assert len(columns) == 1
        readme = client.asset.get_by_guid(guid=reaadmes[0].guid, asset_type=Readme)
        TestReadme.readme = readme

    @pytest.mark.order(after="test_create")
    def test_create_for_modification(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestReadme.readme
        readme = TestReadme.readme
        assert readme.qualified_name
        assert readme.name
        description = f"{readme.description} more stuff"
        readme = Readme.create_for_modification(
            qualified_name=readme.qualified_name, name=readme.name
        )
        readme.description = description
        response = upsert(readme)
        verify_asset_updated(response, Readme)

    @pytest.mark.order(after="test_create")
    def test_trim_to_required(
        self, client: AtlanClient, upsert: Callable[[Asset], AssetMutationResponse]
    ):
        assert TestReadme.readme
        readme = TestReadme.readme
        readme = readme.trim_to_required()
        response = upsert(readme)
        assert response.mutated_entities is None
