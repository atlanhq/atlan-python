# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SageMakerModelGroup model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-sagemaker-app emits today,
``{conn}/{region}/{name}`` (``connector.py:911``),
so a creator change that would re-key existing model groups fails here.
"""

import pytest

from pyatlan_v9.model import SageMakerModelGroup

CONNECTION_QUALIFIED_NAME = "default/sagemaker/1700000000"
AWS_REGION = "us-east-1"
NAME = "churn-models"
QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{AWS_REGION}/{NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-sagemaker-app's process_model_groups inputs and output."""
    sut = SageMakerModelGroup.creator(
        name="churn-models",
        aws_region="us-east-1",
        connection_qualified_name="default/sagemaker/1700000000",
    )

    assert sut.qualified_name == "default/sagemaker/1700000000/us-east-1/churn-models"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, aws_region, connection_qualified_name, message",
    [
        (None, AWS_REGION, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", AWS_REGION, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (NAME, None, CONNECTION_QUALIFIED_NAME, "aws_region is required"),
        (NAME, " ", CONNECTION_QUALIFIED_NAME, "aws_region cannot be blank"),
        (NAME, AWS_REGION, None, "connection_qualified_name is required"),
        (NAME, AWS_REGION, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, aws_region: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SageMakerModelGroup.creator(
            name=name,
            aws_region=aws_region,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the denormalised connection attributes."""
    sut = SageMakerModelGroup.creator(
        name=NAME,
        aws_region=AWS_REGION,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == NAME
    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.aws_region == AWS_REGION
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "sagemaker"
    sut.validate(for_creation=True)


def test_validate_rejects_malformed_qualified_name():
    """The typedef's qualifiedNameFormula needs a region segment."""
    sut = SageMakerModelGroup.creator(
        name=NAME,
        aws_region=AWS_REGION,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )
    sut.qualified_name = NAME
    with pytest.raises(ValueError, match="does not match expected pattern"):
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
        SageMakerModelGroup.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an instance for modification."""
    sut = SageMakerModelGroup.updater(qualified_name=QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME


def test_trim_to_required():
    """Test trim_to_required keeps only the update fields."""
    sut = SageMakerModelGroup.updater(
        qualified_name=QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME
