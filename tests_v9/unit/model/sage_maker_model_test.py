# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SageMakerModel model in pyatlan_v9.

atlan-sagemaker-app emits SageMakerModel only from model packages, as
``{conn}/{region}/{group_name}/{version}`` (``connector.py:1089``). The
standalone ``{region}/{model_name}`` records built by ``process_models`` are
never transformed, so there is one creator shape. The parity test uses the
literal qualifiedName so a creator change that would re-key models fails here.
"""

import pytest

from pyatlan_v9.model import SageMakerModel

CONNECTION_QUALIFIED_NAME = "default/sagemaker/1700000000"
MODEL_GROUP_NAME = "churn-models"
MODEL_GROUP_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/us-east-1/{MODEL_GROUP_NAME}"
VERSION = "3"
NAME = f"{MODEL_GROUP_NAME}/{VERSION}"
QUALIFIED_NAME = f"{MODEL_GROUP_QUALIFIED_NAME}/{VERSION}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-sagemaker-app's process_model_packages inputs and output."""
    sut = SageMakerModel.creator(
        version="3",
        model_group_qualified_name="default/sagemaker/1700000000/us-east-1/churn-models",
    )

    assert sut.qualified_name == "default/sagemaker/1700000000/us-east-1/churn-models/3"
    assert sut.name == "churn-models/3"
    assert (
        sut.sage_maker_model_model_group_qualified_name
        == "default/sagemaker/1700000000/us-east-1/churn-models"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "version, model_group_qualified_name, message",
    [
        (None, MODEL_GROUP_QUALIFIED_NAME, "version is required"),
        (" ", MODEL_GROUP_QUALIFIED_NAME, "version cannot be blank"),
        (VERSION, None, "model_group_qualified_name is required"),
        (VERSION, " ", "model_group_qualified_name cannot be blank"),
        (
            VERSION,
            f"us-east-1/{MODEL_GROUP_NAME}",
            "model_group_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    version: str, model_group_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SageMakerModel.creator(
            version=version, model_group_qualified_name=model_group_qualified_name
        )


def test_creator():
    """Test creator derives the group, region and connection from the group qn."""
    sut = SageMakerModel.creator(
        version=VERSION, model_group_qualified_name=MODEL_GROUP_QUALIFIED_NAME
    )

    assert sut.name == NAME
    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.sage_maker_model_version == VERSION
    assert sut.sage_maker_model_model_group_name == MODEL_GROUP_NAME
    assert sut.sage_maker_model_model_group_qualified_name == MODEL_GROUP_QUALIFIED_NAME
    assert sut.aws_region == "us-east-1"
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "sagemaker"
    assert sut.sage_maker_model_group.unique_attributes == {
        "qualifiedName": MODEL_GROUP_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit name and connection qualified name."""
    sut = SageMakerModel.creator(
        version=VERSION,
        model_group_qualified_name=MODEL_GROUP_QUALIFIED_NAME,
        name="churn v3",
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == "churn v3"
    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, NAME, "qualified_name is required"),
        (QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SageMakerModel.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an instance for modification."""
    sut = SageMakerModel.updater(qualified_name=QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME


def test_trim_to_required():
    """Test trim_to_required keeps only the update fields."""
    sut = SageMakerModel.updater(
        qualified_name=QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME
