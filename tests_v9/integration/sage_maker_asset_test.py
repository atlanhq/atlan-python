# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    SageMakerFeature,
    SageMakerFeatureGroup,
    SageMakerModel,
    SageMakerModelDeployment,
    SageMakerModelGroup,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SAGEMAKER")
AWS_REGION = "us-east-1"
MODEL_VERSION = "1"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SAGEMAKER
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def model_group(
    client: AtlanClient, connection: Connection
) -> Generator[SageMakerModelGroup, None, None]:
    to_create = SageMakerModelGroup.creator(
        name=f"model_group_{MODULE_NAME}",
        aws_region=AWS_REGION,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SageMakerModelGroup
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SageMakerModelGroup)


@pytest.fixture(scope="module")
def model(
    client: AtlanClient, model_group: SageMakerModelGroup
) -> Generator[SageMakerModel, None, None]:
    to_create = SageMakerModel.creator(
        version=MODEL_VERSION,
        model_group_qualified_name=model_group.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SageMakerModel)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SageMakerModel)


@pytest.fixture(scope="module")
def model_deployment(
    client: AtlanClient, connection: Connection
) -> Generator[SageMakerModelDeployment, None, None]:
    to_create = SageMakerModelDeployment.creator(
        name=f"endpoint_{MODULE_NAME}",
        aws_region=AWS_REGION,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SageMakerModelDeployment
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SageMakerModelDeployment)


@pytest.fixture(scope="module")
def feature_group(
    client: AtlanClient, connection: Connection
) -> Generator[SageMakerFeatureGroup, None, None]:
    to_create = SageMakerFeatureGroup.creator(
        name=f"feature_group_{MODULE_NAME}",
        aws_region=AWS_REGION,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=SageMakerFeatureGroup
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SageMakerFeatureGroup)


@pytest.fixture(scope="module")
def feature(
    client: AtlanClient, feature_group: SageMakerFeatureGroup
) -> Generator[SageMakerFeature, None, None]:
    to_create = SageMakerFeature.creator(
        name=f"feature_{MODULE_NAME}",
        feature_group_qualified_name=feature_group.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SageMakerFeature)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SageMakerFeature)


def _assert_retrieved(client, asset, asset_type, connection, qualified_name):
    assert asset.guid
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.SAGEMAKER
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_model_group(
    client: AtlanClient, connection: Connection, model_group: SageMakerModelGroup
):
    _assert_retrieved(
        client,
        model_group,
        SageMakerModelGroup,
        connection,
        f"{connection.qualified_name}/{AWS_REGION}/model_group_{MODULE_NAME}",
    )


def test_model(
    client: AtlanClient,
    connection: Connection,
    model_group: SageMakerModelGroup,
    model: SageMakerModel,
):
    retrieved = _assert_retrieved(
        client,
        model,
        SageMakerModel,
        connection,
        f"{model_group.qualified_name}/{MODEL_VERSION}",
    )
    assert retrieved.name == f"model_group_{MODULE_NAME}/{MODEL_VERSION}"
    assert retrieved.sage_maker_model_version == MODEL_VERSION
    assert (
        retrieved.sage_maker_model_model_group_qualified_name
        == model_group.qualified_name
    )
    assert retrieved.sage_maker_model_group.guid == model_group.guid


def test_model_deployment(
    client: AtlanClient,
    connection: Connection,
    model_deployment: SageMakerModelDeployment,
):
    _assert_retrieved(
        client,
        model_deployment,
        SageMakerModelDeployment,
        connection,
        f"{connection.qualified_name}/{AWS_REGION}/endpoint_{MODULE_NAME}",
    )


def test_feature_group(
    client: AtlanClient, connection: Connection, feature_group: SageMakerFeatureGroup
):
    _assert_retrieved(
        client,
        feature_group,
        SageMakerFeatureGroup,
        connection,
        f"{connection.qualified_name}/{AWS_REGION}/feature_group_{MODULE_NAME}",
    )


def test_feature(
    client: AtlanClient,
    connection: Connection,
    feature_group: SageMakerFeatureGroup,
    feature: SageMakerFeature,
):
    retrieved = _assert_retrieved(
        client,
        feature,
        SageMakerFeature,
        connection,
        f"{feature_group.qualified_name}/feature_{MODULE_NAME}",
    )
    assert retrieved.sage_maker_feature_group_name == feature_group.name
    assert (
        retrieved.sage_maker_feature_group_qualified_name
        == feature_group.qualified_name
    )
    assert retrieved.sage_maker_feature_group.guid == feature_group.guid
