# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    BigqueryRoutine,
    Connection,
    Database,
    GCPDataplexAspectType,
    Schema,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("DATAPLEX")

ASPECT_TYPE_ID = f"aspect_{MODULE_NAME}"
RESOURCE_NAME = f"projects/sdk-test/locations/global/aspectTypes/{ASPECT_TYPE_ID}"
DATABASE_NAME = f"project_{MODULE_NAME}"
SCHEMA_NAME = f"dataset_{MODULE_NAME}"
ROUTINE_NAME = f"routine_{MODULE_NAME}"
ROUTINE_DEFINITION = "CREATE PROCEDURE ds.p() BEGIN SELECT 1; END"


@pytest.fixture(scope="module")
def dataplex_connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.DATAPLEX
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def bigquery_connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.BIGQUERY
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def aspect_type(
    client: AtlanClient, dataplex_connection: Connection
) -> Generator[GCPDataplexAspectType, None, None]:
    to_create = GCPDataplexAspectType.creator(
        resource_name=RESOURCE_NAME,
        connection_qualified_name=dataplex_connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=GCPDataplexAspectType
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=GCPDataplexAspectType)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, bigquery_connection: Connection
) -> Generator[Database, None, None]:
    to_create = Database.creator(
        name=DATABASE_NAME,
        connection_qualified_name=bigquery_connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=Database)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Database)


@pytest.fixture(scope="module")
def schema(client: AtlanClient, database: Database) -> Generator[Schema, None, None]:
    to_create = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=database.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=Schema)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Schema)


@pytest.fixture(scope="module")
def routine(
    client: AtlanClient, schema: Schema
) -> Generator[BigqueryRoutine, None, None]:
    to_create = BigqueryRoutine.creator(
        name=ROUTINE_NAME,
        definition=ROUTINE_DEFINITION,
        schema_qualified_name=schema.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=BigqueryRoutine)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=BigqueryRoutine)


def test_aspect_type(
    client: AtlanClient,
    dataplex_connection: Connection,
    aspect_type: GCPDataplexAspectType,
):
    assert aspect_type.guid
    retrieved = client.asset.get_by_guid(
        aspect_type.guid, asset_type=GCPDataplexAspectType
    )
    assert retrieved.qualified_name == (
        f"{dataplex_connection.qualified_name}/aspect-type/{RESOURCE_NAME}"
    )
    assert retrieved.name == ASPECT_TYPE_ID
    assert retrieved.gcp_dataplex_aspect_type_resource_name == RESOURCE_NAME
    assert retrieved.gcp_dataplex_aspect_type_project == "sdk-test"
    assert retrieved.gcp_dataplex_aspect_type_location == "global"
    assert retrieved.connector_name == AtlanConnectorType.DATAPLEX
    assert retrieved.connection_qualified_name == dataplex_connection.qualified_name


def test_routine(
    client: AtlanClient,
    bigquery_connection: Connection,
    schema: Schema,
    routine: BigqueryRoutine,
):
    assert routine.guid
    retrieved = client.asset.get_by_guid(
        routine.guid, asset_type=BigqueryRoutine, ignore_relationships=False
    )
    assert retrieved.qualified_name == (
        f"{bigquery_connection.qualified_name}/{DATABASE_NAME}/{SCHEMA_NAME}"
        f"/_routines_/{ROUTINE_NAME}"
    )
    assert retrieved.name == ROUTINE_NAME
    assert retrieved.definition == ROUTINE_DEFINITION
    assert retrieved.schema_qualified_name == schema.qualified_name
    assert retrieved.database_name == DATABASE_NAME
    assert retrieved.connector_name == AtlanConnectorType.BIGQUERY
    assert retrieved.connection_qualified_name == bigquery_connection.qualified_name
    assert retrieved.atlan_schema.guid == schema.guid
