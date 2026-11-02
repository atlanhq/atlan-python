# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    SapAnalyticsCloudColumn,
    SapAnalyticsCloudFolder,
    SapAnalyticsCloudModel,
    SapAnalyticsCloudStory,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SAC")

ROOT_FOLDER_ID = f"root{MODULE_NAME}"
SUB_FOLDER_ID = f"sub{MODULE_NAME}"
STORY_ID = f"story{MODULE_NAME}"
MODEL_ID = f"model{MODULE_NAME}"
LIVE_MODEL_ID = f"t.4.live{MODULE_NAME}:live{MODULE_NAME}"
DIMENSION_NAME = "Account"
ATTRIBUTE_NAME = "ID"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client,
        name=MODULE_NAME,
        connector_type=AtlanConnectorType.SAP_ANALYTICS_CLOUD,
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def root_folder(
    client: AtlanClient, connection: Connection
) -> Generator[SapAnalyticsCloudFolder, None, None]:
    to_create = SapAnalyticsCloudFolder.creator(
        name=f"root_{MODULE_NAME}",
        resource_id=ROOT_FOLDER_ID,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapAnalyticsCloudFolder
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapAnalyticsCloudFolder)


@pytest.fixture(scope="module")
def sub_folder(
    client: AtlanClient, root_folder: SapAnalyticsCloudFolder
) -> Generator[SapAnalyticsCloudFolder, None, None]:
    to_create = SapAnalyticsCloudFolder.creator(
        name=f"sub_{MODULE_NAME}",
        resource_id=SUB_FOLDER_ID,
        parent_folder_qualified_name=root_folder.qualified_name,
        parent_folder_name=root_folder.name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapAnalyticsCloudFolder
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapAnalyticsCloudFolder)


@pytest.fixture(scope="module")
def story(
    client: AtlanClient, sub_folder: SapAnalyticsCloudFolder
) -> Generator[SapAnalyticsCloudStory, None, None]:
    to_create = SapAnalyticsCloudStory.creator(
        name=f"story_{MODULE_NAME}",
        resource_id=STORY_ID,
        parent_folder_qualified_name=sub_folder.qualified_name,
        parent_folder_name=sub_folder.name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapAnalyticsCloudStory
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapAnalyticsCloudStory)


@pytest.fixture(scope="module")
def model(
    client: AtlanClient, sub_folder: SapAnalyticsCloudFolder
) -> Generator[SapAnalyticsCloudModel, None, None]:
    to_create = SapAnalyticsCloudModel.creator(
        name=f"model_{MODULE_NAME}",
        resource_id=MODEL_ID,
        parent_folder_qualified_name=sub_folder.qualified_name,
        parent_folder_name=sub_folder.name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapAnalyticsCloudModel
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapAnalyticsCloudModel)


@pytest.fixture(scope="module")
def live_model(
    client: AtlanClient, connection: Connection
) -> Generator[SapAnalyticsCloudModel, None, None]:
    to_create = SapAnalyticsCloudModel.creator(
        name=f"live_{MODULE_NAME}",
        model_id=LIVE_MODEL_ID,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapAnalyticsCloudModel
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapAnalyticsCloudModel)


@pytest.fixture(scope="module")
def dimension(
    client: AtlanClient, model: SapAnalyticsCloudModel
) -> Generator[SapAnalyticsCloudColumn, None, None]:
    to_create = SapAnalyticsCloudColumn.creator(
        name=DIMENSION_NAME,
        sap_analytics_cloud_model_qualified_name=model.qualified_name,
        sap_analytics_cloud_model_name=model.name,
        order=1,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapAnalyticsCloudColumn
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapAnalyticsCloudColumn)


@pytest.fixture(scope="module")
def attribute(
    client: AtlanClient,
    model: SapAnalyticsCloudModel,
    dimension: SapAnalyticsCloudColumn,
) -> Generator[SapAnalyticsCloudColumn, None, None]:
    to_create = SapAnalyticsCloudColumn.creator(
        name=ATTRIBUTE_NAME,
        sap_analytics_cloud_model_qualified_name=model.qualified_name,
        sap_analytics_cloud_model_name=model.name,
        order=2,
        parent_column_name=dimension.name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SapAnalyticsCloudColumn
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SapAnalyticsCloudColumn)


def _retrieve(client: AtlanClient, asset, asset_type, connection: Connection):
    retrieved = client.asset.get_by_qualified_name(
        asset.qualified_name, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.guid == asset.guid
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.SAP_ANALYTICS_CLOUD
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_root_folder(
    client: AtlanClient,
    connection: Connection,
    root_folder: SapAnalyticsCloudFolder,
):
    assert root_folder.guid
    assert root_folder.qualified_name == f"{connection.qualified_name}/{ROOT_FOLDER_ID}"
    retrieved = _retrieve(client, root_folder, SapAnalyticsCloudFolder, connection)
    assert retrieved.sap_analytics_cloud_resource_id == ROOT_FOLDER_ID


def test_sub_folder(
    client: AtlanClient,
    connection: Connection,
    root_folder: SapAnalyticsCloudFolder,
    sub_folder: SapAnalyticsCloudFolder,
):
    assert sub_folder.guid
    assert sub_folder.qualified_name == (
        f"{connection.qualified_name}/{ROOT_FOLDER_ID}/{SUB_FOLDER_ID}"
    )
    retrieved = _retrieve(client, sub_folder, SapAnalyticsCloudFolder, connection)
    assert (
        retrieved.sap_analytics_cloud_parent_folder_qualified_name
        == root_folder.qualified_name
    )
    assert retrieved.sap_analytics_cloud_parent_folder.guid == root_folder.guid


def test_story(
    client: AtlanClient,
    connection: Connection,
    sub_folder: SapAnalyticsCloudFolder,
    story: SapAnalyticsCloudStory,
):
    assert story.guid
    assert story.qualified_name == f"{sub_folder.qualified_name}/{STORY_ID}"
    retrieved = _retrieve(client, story, SapAnalyticsCloudStory, connection)
    assert retrieved.sap_analytics_cloud_folder.guid == sub_folder.guid


def test_model(
    client: AtlanClient,
    connection: Connection,
    sub_folder: SapAnalyticsCloudFolder,
    model: SapAnalyticsCloudModel,
):
    assert model.guid
    assert model.qualified_name == f"{sub_folder.qualified_name}/{MODEL_ID}"
    retrieved = _retrieve(client, model, SapAnalyticsCloudModel, connection)
    assert retrieved.sap_analytics_cloud_folder.guid == sub_folder.guid


def test_live_model(
    client: AtlanClient,
    connection: Connection,
    live_model: SapAnalyticsCloudModel,
):
    assert live_model.guid
    assert live_model.qualified_name == f"{connection.qualified_name}/{LIVE_MODEL_ID}"
    retrieved = _retrieve(client, live_model, SapAnalyticsCloudModel, connection)
    assert retrieved.sap_analytics_cloud_model_id == LIVE_MODEL_ID


def test_dimension(
    client: AtlanClient,
    connection: Connection,
    model: SapAnalyticsCloudModel,
    dimension: SapAnalyticsCloudColumn,
):
    assert dimension.guid
    assert dimension.qualified_name == f"{model.qualified_name}/{DIMENSION_NAME}"
    retrieved = _retrieve(client, dimension, SapAnalyticsCloudColumn, connection)
    assert retrieved.sap_analytics_cloud_model_qualified_name == model.qualified_name
    assert retrieved.sap_analytics_cloud_model.guid == model.guid


def test_attribute(
    client: AtlanClient,
    connection: Connection,
    model: SapAnalyticsCloudModel,
    dimension: SapAnalyticsCloudColumn,
    attribute: SapAnalyticsCloudColumn,
):
    assert attribute.guid
    assert attribute.qualified_name == (
        f"{model.qualified_name}/{DIMENSION_NAME}/{ATTRIBUTE_NAME}"
    )
    retrieved = _retrieve(client, attribute, SapAnalyticsCloudColumn, connection)
    assert retrieved.sap_analytics_cloud_model.guid == model.guid
    assert retrieved.parent_column_qualified_name == dimension.qualified_name
    assert retrieved.parent_column.guid == dimension.guid
