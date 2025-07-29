import pytest

from pyatlan.model.assets import AIApplication
from pyatlan.model.enums import AIApplicationDevelopmentStage
from tests.unit.model.constants import (
    AI_APPLICATION_VERSION,
    AI_APPLICATION_NAME,
    AI_APPLICATION_DEVELOPMENT_STAGE,
    AI_APPLICATION_QUALIFIED_NAME,
    AI_APPLICATION_DEVELOPMENT_STAGE_UPDATED,
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
    with pytest.raises(ValueError, match=message):
        AIApplication.creator(
            name=name,
            ai_application_development_stage=ai_application_development_stage,
            ai_application_version=ai_application_version,
        )


def test_creator():
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
    with pytest.raises(ValueError, match=message):
        AIApplication.updater(qualified_name=qualified_name, name=name)


def test_updater():
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
    dag = AIApplication.updater(
        name=AI_APPLICATION_NAME,
        qualified_name=AI_APPLICATION_QUALIFIED_NAME,
    ).trim_to_required()

    assert dag.name == AI_APPLICATION_NAME
    assert dag.qualified_name == AI_APPLICATION_QUALIFIED_NAME
