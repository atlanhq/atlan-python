import pytest

from pyatlan.model.assets import AIModel
from pyatlan.model.enums import AIModelStatus
from tests.unit.model.constants import (
    AI_MODEL_NAME,
    AI_MODEL_QUALIFIED_NAME,
    AI_MODEL_STATUS,
    AI_MODEL_STATUS_UPDATED,
    AI_MODEL_VERSION,
)


@pytest.mark.parametrize(
    "name, ai_model_status, message",
    [
        (
            None,
            AI_MODEL_STATUS,
            "name is required",
        ),
        (
            AI_MODEL_NAME,
            None,
            "ai_model_status is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    ai_model_status: AIModelStatus,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        AIModel.creator(
            name=name,
            ai_model_status=ai_model_status,
        )


def test_creator():
    ai_model = AIModel.creator(
        name=AI_MODEL_NAME,
        ai_model_status=AI_MODEL_STATUS,
    )

    assert ai_model.name == AI_MODEL_NAME
    assert ai_model.ai_model_status == AI_MODEL_STATUS
    assert ai_model.qualified_name == AI_MODEL_QUALIFIED_NAME


def test_creator_with_optional_parameters():
    owner_groups = {"group1", "group2"}
    owner_users = {"user1", "user2"}
    ai_model_version = AI_MODEL_VERSION

    ai_model = AIModel.creator(
        name=AI_MODEL_NAME,
        ai_model_status=AI_MODEL_STATUS,
        owner_groups=owner_groups,
        owner_users=owner_users,
        ai_model_version=ai_model_version,
    )

    assert ai_model.name == AI_MODEL_NAME
    assert ai_model.ai_model_status == AI_MODEL_STATUS
    assert ai_model.ai_model_version == ai_model_version
    assert ai_model.qualified_name == AI_MODEL_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, AI_MODEL_QUALIFIED_NAME, "qualified_name is required"),
        (AI_MODEL_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AIModel.updater(qualified_name=qualified_name, name=name)


def test_updater():
    ai_model = AIModel.updater(
        name=AI_MODEL_NAME, qualified_name=AI_MODEL_QUALIFIED_NAME
    )
    ai_model.ai_model_status = AI_MODEL_STATUS_UPDATED

    assert ai_model.name == AI_MODEL_NAME
    assert ai_model.qualified_name == AI_MODEL_QUALIFIED_NAME
    assert ai_model.ai_model_status == AI_MODEL_STATUS_UPDATED


def test_trim_to_required():
    ai_model = AIModel.updater(
        name=AI_MODEL_NAME,
        qualified_name=AI_MODEL_QUALIFIED_NAME,
    ).trim_to_required()

    assert ai_model.name == AI_MODEL_NAME
    assert ai_model.qualified_name == AI_MODEL_QUALIFIED_NAME
