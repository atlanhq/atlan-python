# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, Database, Schema, SqlInsightJoin, Table
from pyatlan.model.enums import (
    AtlanConnectorType,
    SqlInsightJoinCardinality,
    SqlInsightJoinType,
)
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SQL_INSIGHT_JOIN")

DATABASE_NAME = f"test_db_{MODULE_NAME}"
SCHEMA_NAME = f"test_schema_{MODULE_NAME}"
SOURCE_TABLE_NAME = f"test_gl_balances_{MODULE_NAME}"
JOINED_TABLE_NAME = f"test_dsmt_product_{MODULE_NAME}"
COLUMN_PAIRS = [{"source_column": "PRODUCT_ID", "joined_column": "PRODUCT_ID"}]
WHEN_TO_USE = "Enrich GL balance rows with product hierarchy (SDK integration test)"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SNOWFLAKE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, connection: Connection
) -> Generator[Database, None, None]:
    assert connection.qualified_name
    to_create = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=Database)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Database)


@pytest.fixture(scope="module")
def schema(client: AtlanClient, database: Database) -> Generator[Schema, None, None]:
    assert database.qualified_name
    to_create = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=database.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=Schema)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Schema)


@pytest.fixture(scope="module")
def source_table(client: AtlanClient, schema: Schema) -> Generator[Table, None, None]:
    assert schema.qualified_name
    to_create = Table.creator(
        name=SOURCE_TABLE_NAME, schema_qualified_name=schema.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=Table)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Table)


@pytest.fixture(scope="module")
def joined_table(client: AtlanClient, schema: Schema) -> Generator[Table, None, None]:
    assert schema.qualified_name
    to_create = Table.creator(
        name=JOINED_TABLE_NAME, schema_qualified_name=schema.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=Table)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Table)


@pytest.fixture(scope="module")
def sql_insight_join(
    client: AtlanClient, source_table: Table, joined_table: Table
) -> Generator[SqlInsightJoin, None, None]:
    to_create = SqlInsightJoin.creator(
        source_dataset=source_table,
        joined_dataset=joined_table,
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
        cardinality=SqlInsightJoinCardinality.MANY_TO_ONE,
        when_to_use=WHEN_TO_USE,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SqlInsightJoin)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SqlInsightJoin)


def test_sql_insight_join(
    client: AtlanClient,
    source_table: Table,
    joined_table: Table,
    sql_insight_join: SqlInsightJoin,
):
    assert sql_insight_join
    assert sql_insight_join.guid
    # deterministic, miner-identical identity
    assert sql_insight_join.qualified_name == SqlInsightJoin.generate_qualified_name(
        source_qualified_name=source_table.qualified_name or "",
        joined_qualified_name=joined_table.qualified_name or "",
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
    )
    assert sql_insight_join.name == f"{SOURCE_TABLE_NAME} JOIN {JOINED_TABLE_NAME}"


def test_sql_insight_join_read_back_carries_both_anchorings(
    client: AtlanClient,
    source_table: Table,
    joined_table: Table,
    sql_insight_join: SqlInsightJoin,
):
    assert sql_insight_join.guid
    retrieved = client.asset.get_by_guid(
        sql_insight_join.guid,
        asset_type=SqlInsightJoin,
        ignore_relationships=False,
    )
    # string attributes (read by metadata-lakehouse consumers)
    assert (
        retrieved.sql_insight_join_source_dataset_qualified_name
        == source_table.qualified_name
    )
    assert (
        retrieved.sql_insight_join_joined_dataset_qualified_name
        == joined_table.qualified_name
    )
    assert retrieved.sql_insight_join_type == SqlInsightJoinType.LEFT
    assert (
        retrieved.sql_insight_join_cardinality == SqlInsightJoinCardinality.MANY_TO_ONE
    )
    assert retrieved.sql_insight_join_when_to_use == WHEN_TO_USE
    # a human-declared join must not claim observed usage
    assert retrieved.sql_insight_join_query_count == 0
    assert retrieved.sql_insight_join_unique_users == 0
    pairs = retrieved.sql_insight_join_column_pairs
    assert pairs
    pair = pairs[0]
    assert pair.sql_insight_join_column_pair_source_column_qualified_name == (
        f"{source_table.qualified_name}/PRODUCT_ID"
    )
    # relationship edges live server-side (rendered on the asset page) — a row
    # missing these is store-visible but invisible on the asset page.
    source_edge = retrieved.attributes.sql_insight_source_dataset
    joined_edge = retrieved.attributes.sql_insight_joined_dataset
    assert source_edge is not None and source_edge.guid == source_table.guid
    assert joined_edge is not None and joined_edge.guid == joined_table.guid


def test_sql_insight_join_upsert_converges_on_same_entity(
    client: AtlanClient,
    source_table: Table,
    joined_table: Table,
    sql_insight_join: SqlInsightJoin,
):
    # Re-confirming the same join must update the existing entity (same guid),
    # never duplicate it — identity is the derived qualifiedName.
    again = SqlInsightJoin.creator(
        source_dataset=source_table,
        joined_dataset=joined_table,
        column_pairs=COLUMN_PAIRS,
        join_type=SqlInsightJoinType.LEFT,
        cardinality=SqlInsightJoinCardinality.MANY_TO_ONE,
        when_to_use=f"{WHEN_TO_USE} (re-confirmed)",
    )
    response = client.asset.save(again)
    assert not response.assets_created(asset_type=SqlInsightJoin)
    updated = response.assets_updated(asset_type=SqlInsightJoin)
    assert len(updated) == 1
    assert updated[0].guid == sql_insight_join.guid
