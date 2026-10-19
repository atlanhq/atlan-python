# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, FlowControlOperation
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("FCO")
WORKSPACE_ID = f"ws{MODULE_NAME}"
NOTEBOOK_ID = f"nb{MODULE_NAME}"
JOB_KEY = f"job{MODULE_NAME}"
REGION = "us-east-1"
JOB_NAME = f"training-{MODULE_NAME}"


@pytest.fixture(scope="module")
def fabric_connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.FABRIC
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def sagemaker_connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SAGEMAKER
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


def _save(client: AtlanClient, to_create: FlowControlOperation) -> FlowControlOperation:
    return client.asset.save(to_create).assets_created(asset_type=FlowControlOperation)[
        0
    ]


@pytest.fixture(scope="module")
def notebook(
    client: AtlanClient, fabric_connection: Connection
) -> Generator[FlowControlOperation, None, None]:
    result = _save(
        client,
        FlowControlOperation.creator(
            name=f"notebook_{MODULE_NAME}",
            connection_qualified_name=fabric_connection.qualified_name,
            scope=WORKSPACE_ID,
            source_id=NOTEBOOK_ID,
            flow_id=NOTEBOOK_ID,
        ),
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=FlowControlOperation)


@pytest.fixture(scope="module")
def spark_job(
    client: AtlanClient, fabric_connection: Connection, notebook: FlowControlOperation
) -> Generator[FlowControlOperation, None, None]:
    result = _save(
        client,
        FlowControlOperation.creator(
            name=f"job_{MODULE_NAME}",
            connection_qualified_name=fabric_connection.qualified_name,
            parent_qualified_name=notebook.qualified_name,
            source_id=JOB_KEY,
            flow_id=JOB_KEY,
        ),
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=FlowControlOperation)


@pytest.fixture(scope="module")
def sagemaker_job(
    client: AtlanClient, sagemaker_connection: Connection
) -> Generator[FlowControlOperation, None, None]:
    result = _save(
        client,
        FlowControlOperation.creator(
            name=JOB_NAME,
            connection_qualified_name=sagemaker_connection.qualified_name,
            scope=REGION,
            source_id=JOB_NAME,
        ),
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=FlowControlOperation)


def test_fabric_notebook_and_spark_job(
    client: AtlanClient,
    fabric_connection: Connection,
    notebook: FlowControlOperation,
    spark_job: FlowControlOperation,
):
    conn_qn = fabric_connection.qualified_name
    assert notebook.guid
    assert notebook.qualified_name == f"{conn_qn}/{WORKSPACE_ID}/{NOTEBOOK_ID}"
    assert spark_job.qualified_name == f"{notebook.qualified_name}/jobs/{JOB_KEY}"

    restored = client.asset.get_by_qualified_name(
        asset_type=FlowControlOperation,
        qualified_name=spark_job.qualified_name,
        ignore_relationships=False,
    )
    assert restored.guid == spark_job.guid
    assert restored.connection_qualified_name == conn_qn
    assert restored.connector_name == "fabric"
    assert restored.flow_id == JOB_KEY
    assert restored.flow_controlled_by.guid == notebook.guid


def test_sagemaker_job(
    client: AtlanClient,
    sagemaker_connection: Connection,
    sagemaker_job: FlowControlOperation,
):
    conn_qn = sagemaker_connection.qualified_name
    assert sagemaker_job.guid
    assert sagemaker_job.qualified_name == f"{conn_qn}/{REGION}/{JOB_NAME}"
    restored = client.asset.get_by_qualified_name(
        asset_type=FlowControlOperation, qualified_name=sagemaker_job.qualified_name
    )
    assert restored.guid == sagemaker_job.guid
    assert restored.connector_name == "sagemaker"
