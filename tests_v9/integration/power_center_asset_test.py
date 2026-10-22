# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, Flow
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("POWERCENTER")

FOLDER_NAME = f"folder_{MODULE_NAME}"
WORKFLOW_NAME = f"wf_{MODULE_NAME}"
SESSION_NAME = f"s_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client,
        name=MODULE_NAME,
        connector_type=AtlanConnectorType.INFORMATICA_POWERCENTER,
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def flow(client: AtlanClient, connection: Connection) -> Generator[Flow, None, None]:
    to_create = Flow.creator(
        connection_qualified_name=connection.qualified_name,
        folder_name=FOLDER_NAME,
        workflow_name=WORKFLOW_NAME,
        session_name=SESSION_NAME,
    )
    result = client.asset.save(to_create).assets_created(asset_type=Flow)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Flow)


def test_flow(client: AtlanClient, connection: Connection, flow: Flow):
    expected_qualified_name = (
        f"{connection.qualified_name}/{FOLDER_NAME}/{WORKFLOW_NAME}/{SESSION_NAME}"
    )
    assert flow.guid
    assert flow.qualified_name == expected_qualified_name

    retrieved = client.asset.get_by_qualified_name(
        expected_qualified_name, asset_type=Flow
    )
    assert retrieved.guid == flow.guid
    assert retrieved.name == f"{FOLDER_NAME}/{WORKFLOW_NAME}/{SESSION_NAME}"
    assert retrieved.connector_name == AtlanConnectorType.INFORMATICA_POWERCENTER
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert retrieved.flow_folder_name == FOLDER_NAME
