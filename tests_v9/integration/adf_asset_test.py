# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    AdfActivity,
    AdfDataset,
    AdfLinkedservice,
    AdfPipeline,
    Connection,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("ADF")
FACTORY_NAME = f"factory_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client,
        name=MODULE_NAME,
        connector_type=AtlanConnectorType.AZURE_DATA_FACTORY,
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def linkedservice(
    client: AtlanClient, connection: Connection
) -> Generator[AdfLinkedservice, None, None]:
    to_create = AdfLinkedservice.creator(
        name=f"linkedservice_{MODULE_NAME}",
        adf_factory_name=FACTORY_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=AdfLinkedservice)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AdfLinkedservice)


@pytest.fixture(scope="module")
def dataset(
    client: AtlanClient, connection: Connection, linkedservice: AdfLinkedservice
) -> Generator[AdfDataset, None, None]:
    to_create = AdfDataset.creator(
        name=f"dataset_{MODULE_NAME}",
        adf_factory_name=FACTORY_NAME,
        connection_qualified_name=connection.qualified_name,
        adf_linkedservice_name=linkedservice.name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=AdfDataset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AdfDataset)


@pytest.fixture(scope="module")
def pipeline(
    client: AtlanClient, connection: Connection
) -> Generator[AdfPipeline, None, None]:
    # AdfPipeline has no creator yet; build it the way atlan-adf-app does.
    name = f"pipeline_{MODULE_NAME}"
    to_create = AdfPipeline(
        guid="-1",
        name=name,
        qualified_name=f"{connection.qualified_name}/factory/{FACTORY_NAME}/pipeline/{name}",
        adf_factory_name=FACTORY_NAME,
        connection_qualified_name=connection.qualified_name,
        connector_name=AtlanConnectorType.AZURE_DATA_FACTORY.value,
    )
    result = client.asset.save(to_create).assets_created(asset_type=AdfPipeline)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AdfPipeline)


@pytest.fixture(scope="module")
def activity(
    client: AtlanClient, pipeline: AdfPipeline
) -> Generator[AdfActivity, None, None]:
    to_create = AdfActivity.creator(
        name=f"activity_{MODULE_NAME}",
        adf_pipeline_qualified_name=pipeline.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=AdfActivity)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AdfActivity)


def _assert_retrieved(client, asset, asset_type, connection, qualified_name):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.AZURE_DATA_FACTORY
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert retrieved.adf_factory_name == FACTORY_NAME
    return retrieved


def test_linkedservice(
    client: AtlanClient, connection: Connection, linkedservice: AdfLinkedservice
):
    _assert_retrieved(
        client,
        linkedservice,
        AdfLinkedservice,
        connection,
        f"{connection.qualified_name}/factory/{FACTORY_NAME}"
        f"/linkedservices/linkedservice_{MODULE_NAME}",
    )


def test_dataset(
    client: AtlanClient,
    connection: Connection,
    linkedservice: AdfLinkedservice,
    dataset: AdfDataset,
):
    retrieved = _assert_retrieved(
        client,
        dataset,
        AdfDataset,
        connection,
        f"{connection.qualified_name}/factory/{FACTORY_NAME}"
        f"/datasets/dataset_{MODULE_NAME}",
    )
    assert retrieved.adf_dataset_linked_service == linkedservice.name
    assert retrieved.adf_linkedservice.guid == linkedservice.guid


def test_activity(
    client: AtlanClient,
    connection: Connection,
    pipeline: AdfPipeline,
    activity: AdfActivity,
):
    retrieved = _assert_retrieved(
        client,
        activity,
        AdfActivity,
        connection,
        f"{pipeline.qualified_name}/activities/activity_{MODULE_NAME}",
    )
    assert retrieved.adf_pipeline_qualified_name == pipeline.qualified_name
    assert retrieved.adf_pipeline.guid == pipeline.guid
