# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AIApplication model in pyatlan_v9."""

import pytest

from pyatlan.model.enums import AIApplicationDevelopmentStage
from pyatlan_v9.models import AIApplication
from tests_v9.unit.model.constants import (
    AI_APPLICATION_DEVELOPMENT_STAGE,
    AI_APPLICATION_DEVELOPMENT_STAGE_UPDATED,
    AI_APPLICATION_NAME,
    AI_APPLICATION_QUALIFIED_NAME,
    AI_APPLICATION_VERSION,
)


@pytest.mark.parametrize(
    "name, ai_application_version, ai_application_development_stage, message",
    [
        (
            None,
            AI_APPLICATION_VERSION,
            AI_APPLICATION_DEVELOPMENT_STAGE,
            "name is required",
        ),
        (
            AI_APPLICATION_NAME,
            None,
            AI_APPLICATION_DEVELOPMENT_STAGE,
            "ai_application_version is required",
        ),
        (
            AI_APPLICATION_NAME,
            AI_APPLICATION_VERSION,
            None,
            "ai_application_development_stage is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    ai_application_development_stage: AIApplicationDevelopmentStage,
    ai_application_version: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AIApplication.creator(
            name=name,
            ai_application_development_stage=ai_application_development_stage,
            ai_application_version=ai_application_version,
        )


def test_creator():
    """Test creator initializes required and derived fields."""
    ai_application = AIApplication.creator(
        name=AI_APPLICATION_NAME,
        ai_application_version=AI_APPLICATION_VERSION,
        ai_application_development_stage=AI_APPLICATION_DEVELOPMENT_STAGE,
    )

    assert ai_application.name == AI_APPLICATION_NAME
    assert ai_application.ai_application_version == AI_APPLICATION_VERSION
    assert (
        ai_application.ai_application_development_stage
        == AI_APPLICATION_DEVELOPMENT_STAGE
    )
    assert ai_application.qualified_name == AI_APPLICATION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, AI_APPLICATION_QUALIFIED_NAME, "qualified_name is required"),
        (AI_APPLICATION_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AIApplication.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates minimal updatable instance."""
    ai_application = AIApplication.updater(
        name=AI_APPLICATION_NAME, qualified_name=AI_APPLICATION_QUALIFIED_NAME
    )
    ai_application.ai_application_development_stage = (
        AI_APPLICATION_DEVELOPMENT_STAGE_UPDATED
    )

    assert ai_application.name == AI_APPLICATION_NAME
    assert ai_application.qualified_name == AI_APPLICATION_QUALIFIED_NAME
    assert (
        ai_application.ai_application_development_stage
        == AI_APPLICATION_DEVELOPMENT_STAGE_UPDATED
    )


def test_trim_to_required():
    """Test trim_to_required keeps only required updater fields."""
    ai_application = AIApplication.updater(
        name=AI_APPLICATION_NAME,
        qualified_name=AI_APPLICATION_QUALIFIED_NAME,
    ).trim_to_required()

    assert ai_application.name == AI_APPLICATION_NAME
    assert ai_application.qualified_name == AI_APPLICATION_QUALIFIED_NAME
