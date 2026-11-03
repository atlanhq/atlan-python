# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    Database,
    SapDatasphereReplicationFlow,
    Schema,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SAP_DATASPHERE")
# atlan-sapdatasphere-app models each Datasphere space as a Schema under a
# synthetic DEFAULT database, named by norm(space).
DATABASE_NAME = "DEFAULT"
SPACE_NAME = MODULE_NAME  # raw, contains "-" so norm() is exercised
SCHEMA_NAME = MODULE_NAME.replace("-", "_")
FLOW_NAME = f"rf {MODULE_NAME}.v1"
FLOW_QN_SEGMENT = FLOW_NAME.replace(" ", "_").replace("-", "_").replace(".", "_")


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client,
        name=MODULE_NAME,
        connector_type=AtlanConnectorType.SAP_DATASPHERE,
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, connection: Connection
) -> Generator[Database, None, None]:
    to_create = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
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
def replication_flow(
    client: AtlanClient, connection: Connection, schema: Schema
) -> Generator[SapDatasphereReplicationFlow, None, None]:
    to_create = SapDatasphereReplicationFlow.creator(
        name=FLOW_NAME,
        space_name=SPACE_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapDatasphereReplicationFlow
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapDatasphereReplicationFlow)


def test_schema_matches_derived_space_qualified_name(
    schema: Schema, connection: Connection
):
    assert schema.qualified_name == (
        f"{connection.qualified_name}/{DATABASE_NAME}/{SCHEMA_NAME}"
    )


def test_replication_flow(
    client: AtlanClient,
    replication_flow: SapDatasphereReplicationFlow,
    connection: Connection,
    schema: Schema,
):
    assert replication_flow.guid
    assert replication_flow.name == FLOW_NAME
    assert replication_flow.qualified_name == (
        f"{connection.qualified_name}/flow/{SCHEMA_NAME}/{FLOW_QN_SEGMENT}"
    )
    assert replication_flow.connection_qualified_name == connection.qualified_name
    assert replication_flow.connector_name == AtlanConnectorType.SAP_DATASPHERE.value

    # No `attributes=`: that routes through index search, which is eventually
    # consistent and can miss an asset saved a moment ago. The direct API is not.
    retrieved = client.asset.get_by_qualified_name(
        qualified_name=replication_flow.qualified_name,
        asset_type=SapDatasphereReplicationFlow,
        ignore_relationships=False,
    )
    assert retrieved.guid == replication_flow.guid
    assert retrieved.sap_datasphere_replication_flow_space_name == SPACE_NAME
    assert (
        retrieved.sap_datasphere_replication_flow_space_qualified_name
        == schema.qualified_name
    )
    assert retrieved.sap_datasphere_schema
    assert retrieved.sap_datasphere_schema.guid == schema.guid
