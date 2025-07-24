# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AIApplication, AIModel
from pyatlan.model.enums import AIApplicationDevelopmentStage, AIModelStatus
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
