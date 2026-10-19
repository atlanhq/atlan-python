# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    DbtDimension,
    DbtEntity,
    DbtMeasure,
    DbtMetric,
    DbtModel,
    DbtModelColumn,
    DbtSeed,
    DbtSemanticModel,
    DbtSource,
    DbtTag,
    DbtTest,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("DBT")

ACCOUNT_ID = "70403103932498"
PROJECT_ID = "70403104069713"
ENVIRONMENT_ID = "70403103991524"
BASE = f"account/{ACCOUNT_ID}/project/{PROJECT_ID}"
ENV = f"{BASE}/env/{ENVIRONMENT_ID}"

SOURCE_UID = f"source.{MODULE_NAME}.raw.orders"
MODEL_UID = f"model.{MODULE_NAME}.orders"
SEED_UID = f"seed.{MODULE_NAME}.raw_customers"
SEMANTIC_MODEL_UID = f"semantic_model.{MODULE_NAME}.orders"
METRIC_UID = f"metric.{MODULE_NAME}.order_total"
TEST_UID = f"test.{MODULE_NAME}.not_null_orders_id"
FIELD_NAME = "order_count"


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.DBT
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


def _ids(connection: Connection, with_env: bool = True) -> dict:
    ids = dict(
        connection_qualified_name=connection.qualified_name,
        account_id=ACCOUNT_ID,
        project_id=PROJECT_ID,
    )
    if with_env:
        ids["environment_id"] = ENVIRONMENT_ID
    return ids


@pytest.fixture(scope="module")
def source(client: AtlanClient, connection: Connection):
    to_create = DbtSource.creator(
        name=SOURCE_UID.split(".")[-1],
        unique_id=SOURCE_UID,
        **_ids(connection, with_env=False),
    )
    result = _save(client, to_create, DbtSource)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtSource)


@pytest.fixture(scope="module")
def model(client: AtlanClient, connection: Connection):
    to_create = DbtModel.creator(
        name=MODEL_UID.split(".")[-1],
        unique_id=MODEL_UID,
        **_ids(connection),
    )
    result = _save(client, to_create, DbtModel)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtModel)


@pytest.fixture(scope="module")
def seed(client: AtlanClient, connection: Connection):
    to_create = DbtSeed.creator(
        name=SEED_UID.split(".")[-1],
        unique_id=SEED_UID,
        **_ids(connection),
    )
    result = _save(client, to_create, DbtSeed)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtSeed)


@pytest.fixture(scope="module")
def semantic_model(client: AtlanClient, connection: Connection):
    to_create = DbtSemanticModel.creator(
        name=SEMANTIC_MODEL_UID.split(".")[-1],
        unique_id=SEMANTIC_MODEL_UID,
        **_ids(connection),
    )
    result = _save(client, to_create, DbtSemanticModel)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtSemanticModel)


@pytest.fixture(scope="module")
def metric(client: AtlanClient, connection: Connection):
    to_create = DbtMetric.creator(
        name=METRIC_UID.split(".")[-1],
        unique_id=METRIC_UID,
        **_ids(connection),
    )
    result = _save(client, to_create, DbtMetric)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtMetric)


@pytest.fixture(scope="module")
def dbt_test(client: AtlanClient, connection: Connection):
    to_create = DbtTest.creator(
        name=TEST_UID.split(".")[-1],
        unique_id=TEST_UID,
        **_ids(connection),
    )
    result = _save(client, to_create, DbtTest)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtTest)


@pytest.fixture(scope="module")
def tag(client: AtlanClient, connection: Connection):
    to_create = DbtTag.creator(
        name=f"tag_{MODULE_NAME}", **_ids(connection, with_env=False)
    )
    result = _save(client, to_create, DbtTag)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtTag)


@pytest.fixture(scope="module")
def measure(client: AtlanClient, semantic_model: DbtSemanticModel):
    to_create = DbtMeasure.creator(
        name=FIELD_NAME, semantic_model_qualified_name=semantic_model.qualified_name
    )
    result = _save(client, to_create, DbtMeasure)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtMeasure)


@pytest.fixture(scope="module")
def dimension(client: AtlanClient, semantic_model: DbtSemanticModel):
    to_create = DbtDimension.creator(
        name=FIELD_NAME, semantic_model_qualified_name=semantic_model.qualified_name
    )
    result = _save(client, to_create, DbtDimension)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtDimension)


@pytest.fixture(scope="module")
def entity(client: AtlanClient, semantic_model: DbtSemanticModel):
    to_create = DbtEntity.creator(
        name=FIELD_NAME, semantic_model_qualified_name=semantic_model.qualified_name
    )
    result = _save(client, to_create, DbtEntity)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtEntity)


@pytest.fixture(scope="module")
def model_column(client: AtlanClient, model: DbtModel):
    to_create = DbtModelColumn.creator(
        name="order_id", model_qualified_name=model.qualified_name
    )
    result = _save(client, to_create, DbtModelColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtModelColumn)


@pytest.fixture(scope="module")
def seed_column(client: AtlanClient, seed: DbtSeed):
    to_create = DbtModelColumn.creator(
        name="customer_id", seed_qualified_name=seed.qualified_name
    )
    result = _save(client, to_create, DbtModelColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DbtModelColumn)


def _assert_retrieved(client, asset, asset_type, connection, expected_suffix):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == f"{connection.qualified_name}/{expected_suffix}"
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.DBT
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_source(client: AtlanClient, connection: Connection, source):
    retrieved = _assert_retrieved(
        client, source, DbtSource, connection, f"{BASE}/{SOURCE_UID}"
    )
    assert retrieved.asset_dbt_unique_id == SOURCE_UID


@pytest.mark.parametrize(
    "fixture_name, asset_type, unique_id",
    [
        ("model", DbtModel, MODEL_UID),
        ("seed", DbtSeed, SEED_UID),
        ("semantic_model", DbtSemanticModel, SEMANTIC_MODEL_UID),
        ("metric", DbtMetric, METRIC_UID),
        ("dbt_test", DbtTest, TEST_UID),
    ],
)
def test_env_scoped(
    request,
    client: AtlanClient,
    connection: Connection,
    fixture_name,
    asset_type,
    unique_id,
):
    asset = request.getfixturevalue(fixture_name)
    retrieved = _assert_retrieved(
        client, asset, asset_type, connection, f"{ENV}/{unique_id}"
    )
    assert retrieved.asset_dbt_unique_id == unique_id


def test_tag(client: AtlanClient, connection: Connection, tag):
    _assert_retrieved(client, tag, DbtTag, connection, f"{BASE}/tag/{tag.name}")


@pytest.mark.parametrize(
    "fixture_name, asset_type, kind",
    [
        ("measure", DbtMeasure, "measure"),
        ("dimension", DbtDimension, "dimension"),
        ("entity", DbtEntity, "entity"),
    ],
)
def test_semantic_field(
    request,
    client: AtlanClient,
    connection: Connection,
    semantic_model,
    fixture_name,
    asset_type,
    kind,
):
    asset = request.getfixturevalue(fixture_name)
    retrieved = _assert_retrieved(
        client,
        asset,
        asset_type,
        connection,
        f"{ENV}/{SEMANTIC_MODEL_UID}/{kind}/{FIELD_NAME}",
    )
    assert retrieved.semantic_model.guid == semantic_model.guid
    assert retrieved.dbt_semantic_model_qualified_name == semantic_model.qualified_name


def test_model_column(client: AtlanClient, connection: Connection, model, model_column):
    retrieved = _assert_retrieved(
        client, model_column, DbtModelColumn, connection, f"{ENV}/{MODEL_UID}/order_id"
    )
    assert retrieved.dbt_model.guid == model.guid
    assert retrieved.dbt_model_qualified_name == model.qualified_name


def test_seed_column(client: AtlanClient, connection: Connection, seed, seed_column):
    retrieved = _assert_retrieved(
        client,
        seed_column,
        DbtModelColumn,
        connection,
        f"{ENV}/{SEED_UID}/customer_id",
    )
    assert retrieved.dbt_seed.guid == seed.guid
    assert retrieved.dbt_model_qualified_name == seed.qualified_name
