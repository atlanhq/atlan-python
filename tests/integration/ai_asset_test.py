# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AIApplication, AIModel, Asset, Connection, Table
from pyatlan.model.enums import (
    AIApplicationDevelopmentStage,
    AIDatasetType,
    AIModelStatus,
)
from pyatlan.model.fluent_search import FluentSearch
from tests.integration.client import TestId, delete_asset

MODULE_NAME = TestId.make_unique("AI")

AI_MODEL_NAME = f"test_ai_model_{MODULE_NAME}"
AI_APPLICATION_NAME = f"test_ai_application_{MODULE_NAME}"
AI_APPLICATION_VERSION = "2.0"


@pytest.fixture(scope="module")
def ai_model(client: AtlanClient) -> Generator[AIModel, None, None]:
    to_create = AIModel.creator(
        name=AI_MODEL_NAME,
        ai_model_status=AIModelStatus.ACTIVE,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AIModel)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AIModel)


def test_ai_model(
    ai_model: AIModel,
):
    assert ai_model
    assert ai_model.guid
    assert ai_model.qualified_name
    assert ai_model.name == AI_MODEL_NAME
    assert ai_model.connector_name == "ai"
    assert ai_model.ai_model_status == AIModelStatus.ACTIVE


@pytest.fixture(scope="module")
def ai_application(client: AtlanClient) -> Generator[AIApplication, None, None]:
    to_create = AIApplication.creator(
        name=AI_APPLICATION_NAME,
        ai_application_version=AI_APPLICATION_VERSION,
        ai_application_development_stage=AIApplicationDevelopmentStage.PRODUCTION,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AIApplication)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AIApplication)


def test_ai_application(
    ai_application: AIApplication,
):
    assert ai_application
    assert ai_application.guid
    assert ai_application.qualified_name
    assert ai_application.name == AI_APPLICATION_NAME
    assert ai_application.connector_name == "ai"
    assert ai_application.ai_application_version == AI_APPLICATION_VERSION
    assert (
        ai_application.ai_application_development_stage
        == AIApplicationDevelopmentStage.PRODUCTION
    )


def _update_ai_application(client, ai_application: AIApplication):
    updated = AIApplication.updater(
        qualified_name=ai_application.qualified_name, name=ai_application.name
    )
    updated.ai_application_development_stage = AIApplicationDevelopmentStage.DEVELOPMENT
    updated_response = client.asset.save(updated)
    assert updated_response
    assert updated_response.mutated_entities.UPDATE[0]
    updated_response = updated_response.mutated_entities.UPDATE[0]
    assert updated_response.qualified_name
    assert updated_response.name == AI_APPLICATION_NAME
    assert updated_response.connector_name == "ai"
    assert updated_response.ai_application_version == AI_APPLICATION_VERSION
    assert (
        updated_response.ai_application_development_stage
        == AIApplicationDevelopmentStage.DEVELOPMENT
    )


def _update_ai_model(client, ai_model: AIModel):
    updated = AIModel.updater(
        qualified_name=ai_model.qualified_name, name=ai_model.name
    )
    updated.ai_model_version = "2.1"
    updated_response = client.asset.save(updated)
    assert updated_response
    assert updated_response.mutated_entities.UPDATE[0]
    updated_response = updated_response.mutated_entities.UPDATE[0]
    assert updated_response.qualified_name
    assert updated_response.name == AI_MODEL_NAME
    assert updated_response.connector_name == "ai"
    assert updated_response.ai_model_version == "2.1"


def test_update_ai_assets(
    client: AtlanClient,
    ai_model: AIModel,
    ai_application: AIApplication,
):
    _update_ai_application(client, ai_application)
    _update_ai_model(client, ai_model)


def test_ai_model_processes_creator(
    client: AtlanClient,
    ai_model: AIModel,
):
    query = (
        FluentSearch()
        .where(Connection.NAME.eq("development"))
        .where(Connection.CONNECTOR_NAME.eq("snowflake"))
        .include_on_results("qualified_name")
    ).to_request()
    connection_response = client.asset.search(query).current_page()[0]
    assert connection_response.qualified_name
    query = (
        FluentSearch()
        .where(Asset.CONNECTION_QUALIFIED_NAME.eq(connection_response.qualified_name))
        .where(Asset.TYPE_NAME.eq("Table"))
        .include_on_results("guid")
    ).to_request()
    guids = [result.guid for result in client.asset.search(query)]
    database_dict = {
        AIDatasetType.TRAINING: [
            Table.ref_by_guid(guid=guids[0]),
            Table.ref_by_guid(guid=guids[1]),
        ],
        AIDatasetType.TESTING: [Table.ref_by_guid(guid=guids[1])],
        AIDatasetType.INFERENCE: [Table.ref_by_guid(guid=guids[2])],
        AIDatasetType.VALIDATION: [Table.ref_by_guid(guid=guids[3])],
        AIDatasetType.OUTPUT: [Table.ref_by_guid(guid=guids[4])],
    }
    created_processes = AIModel.processes_creator(
        client, a_i_model_guid=ai_model.guid, database_dict=database_dict
    )

    mutation_response = client.asset.save(created_processes)  # type: ignore
    assert (
        mutation_response.mutated_entities and mutation_response.mutated_entities.CREATE
    )
    assert mutation_response.mutated_entities.CREATE[0]
    assert (
        mutation_response.mutated_entities.CREATE[0].ai_dataset_type  # type: ignore
        == AIDatasetType.TRAINING
    )
    assert (
        mutation_response.mutated_entities.CREATE[0].inputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[0].inputs[0].guid == guids[0]  # type: ignore
    )
    assert (
        mutation_response.mutated_entities.CREATE[0].outputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[0].outputs[0].guid  # type: ignore
        == ai_model.guid
    )
    assert mutation_response.mutated_entities.CREATE[1]
    assert (
        mutation_response.mutated_entities.CREATE[1].ai_dataset_type  # type: ignore
        == AIDatasetType.TRAINING
    )
    assert (
        mutation_response.mutated_entities.CREATE[1].inputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[1].inputs[0].guid == guids[1]  # type: ignore
    )
    assert (
        mutation_response.mutated_entities.CREATE[1].outputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[1].outputs[0].guid  # type: ignore
        == ai_model.guid
    )
    assert mutation_response.mutated_entities.CREATE[2]
    assert (
        mutation_response.mutated_entities.CREATE[2].ai_dataset_type  # type: ignore
        == AIDatasetType.TESTING
    )
    assert (
        mutation_response.mutated_entities.CREATE[2].inputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[2].inputs[0].guid == guids[1]  # type: ignore
    )
    assert (
        mutation_response.mutated_entities.CREATE[2].outputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[2].outputs[0].guid  # type: ignore
        == ai_model.guid
    )
    assert mutation_response.mutated_entities.CREATE[3]
    assert (
        mutation_response.mutated_entities.CREATE[3].ai_dataset_type  # type: ignore
        == AIDatasetType.INFERENCE
    )
    assert (
        mutation_response.mutated_entities.CREATE[3].inputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[3].inputs[0].guid == guids[2]  # type: ignore
    )
    assert (
        mutation_response.mutated_entities.CREATE[3].outputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[3].outputs[0].guid  # type: ignore
        == ai_model.guid
    )
    assert mutation_response.mutated_entities.CREATE[4]
    assert (
        mutation_response.mutated_entities.CREATE[4].ai_dataset_type  # type: ignore
        == AIDatasetType.VALIDATION
    )
    assert (
        mutation_response.mutated_entities.CREATE[4].inputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[4].inputs[0].guid == guids[3]  # type: ignore
    )
    assert (
        mutation_response.mutated_entities.CREATE[4].outputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[4].outputs[0].guid  # type: ignore
        == ai_model.guid
    )
    assert mutation_response.mutated_entities.CREATE[5]  # type: ignore
    assert (
        mutation_response.mutated_entities.CREATE[5].ai_dataset_type  # type: ignore
        == AIDatasetType.OUTPUT
    )
    assert (
        mutation_response.mutated_entities.CREATE[5].inputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[5].inputs[0].guid == ai_model.guid  # type: ignore
    )
    assert (
        mutation_response.mutated_entities.CREATE[5].outputs  # type: ignore
        and mutation_response.mutated_entities.CREATE[5].outputs[0].guid == guids[4]  # type: ignore
    )
