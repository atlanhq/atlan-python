# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SageMakerFeature model in pyatlan_v9.

atlan-sagemaker-app emits ``{region}/{group_name}/{feature_name}``
(``connector.py:1562``) and ``asset_mapper._prefix_qn`` prepends the
connection, so the published qualifiedName is
``{conn}/{region}/{group_name}/{feature_name}``. The parity test uses that
literal string so a creator change that would re-key features fails here.
"""

import pytest

from pyatlan_v9.model import SageMakerFeature

CONNECTION_QUALIFIED_NAME = "default/sagemaker/1700000000"
FEATURE_GROUP_NAME = "customers-fg"
FEATURE_GROUP_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/us-east-1/{FEATURE_GROUP_NAME}"
)
NAME = "customer_id"
QUALIFIED_NAME = f"{FEATURE_GROUP_QUALIFIED_NAME}/{NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-sagemaker-app's process_feature_groups inputs and output."""
    sut = SageMakerFeature.creator(
        name="customer_id",
        feature_group_qualified_name="default/sagemaker/1700000000/us-east-1/customers-fg",
    )

    assert (
        sut.qualified_name
        == "default/sagemaker/1700000000/us-east-1/customers-fg/customer_id"
    )
    assert sut.sage_maker_feature_group.unique_attributes == {
        "qualifiedName": "default/sagemaker/1700000000/us-east-1/customers-fg"
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, feature_group_qualified_name, message",
    [
        (None, FEATURE_GROUP_QUALIFIED_NAME, "name is required"),
        (" ", FEATURE_GROUP_QUALIFIED_NAME, "name cannot be blank"),
        (NAME, None, "feature_group_qualified_name is required"),
        (NAME, " ", "feature_group_qualified_name cannot be blank"),
        (
            NAME,
            f"us-east-1/{FEATURE_GROUP_NAME}",
            "feature_group_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, feature_group_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SageMakerFeature.creator(
            name=name, feature_group_qualified_name=feature_group_qualified_name
        )


def test_creator():
    """Test creator derives the group, region and connection from the group qn."""
    sut = SageMakerFeature.creator(
        name=NAME, feature_group_qualified_name=FEATURE_GROUP_QUALIFIED_NAME
    )

    assert sut.name == NAME
    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.sage_maker_feature_group_name == FEATURE_GROUP_NAME
    assert sut.sage_maker_feature_group_qualified_name == FEATURE_GROUP_QUALIFIED_NAME
    assert sut.aws_region == "us-east-1"
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "sagemaker"
    assert sut.sage_maker_feature_group.unique_attributes == {
        "qualifiedName": FEATURE_GROUP_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = SageMakerFeature.creator(
        name=NAME,
        feature_group_qualified_name=FEATURE_GROUP_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

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
        SageMakerFeature.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an instance for modification."""
    sut = SageMakerFeature.updater(qualified_name=QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME


def test_trim_to_required():
    """Test trim_to_required keeps only the update fields."""
    sut = SageMakerFeature.updater(
        qualified_name=QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == NAME
