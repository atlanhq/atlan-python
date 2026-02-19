# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Badge model in pyatlan_v9."""

from unittest.mock import Mock

import pytest

from pyatlan.model.enums import BadgeComparisonOperator, BadgeConditionColor
from pyatlan_v9.model import Badge, BadgeCondition

CM_ATTRIBUTE_NAME = "dummy"
CM_SET_NAME = "Monte Carlo"
BADGE_NAME = "bob"
CM_ATTR_ID = "WQ6XGXwq9o7UnZlkWyKhQN"
CM_ID = "scAesIb5UhKQdTwu4GuCSN"
BADGE_QUALIFIED_NAME = f"badges/global/{CM_ID}.{CM_ATTR_ID}"
BADGE_METADATA_ATTRIBUTE = f"{CM_ID}.{CM_ATTR_ID}"
BADGE_CONDITION = BadgeCondition.creator(
    badge_condition_operator=BadgeComparisonOperator.EQ,
    badge_condition_value="1",
    badge_condition_colorhex=BadgeConditionColor.RED,
)


@pytest.fixture()
def client() -> Mock:
    """Create a mocked client with custom metadata cache."""
    mock_client = Mock()
    cache = Mock()
    cache.get_attr_id_for_name.return_value = CM_ATTR_ID
    cache.get_id_for_name.return_value = CM_ID
    mock_client.custom_metadata_cache = cache
    return mock_client


@pytest.mark.parametrize(
    "name, cm_name, cm_attribute, badge_conditions, message",
    [
        (None, "Bob", "Dave", [BADGE_CONDITION], "name is required"),
        ("Bob", None, "Dave", [BADGE_CONDITION], "cm_name is required"),
        ("Bob", "", "Dave", [BADGE_CONDITION], "cm_name cannot be blank"),
        ("Bob", "Dave", None, [BADGE_CONDITION], "cm_attribute is required"),
        ("Bob", "Dave", "", [BADGE_CONDITION], "cm_attribute cannot be blank"),
        ("Bob", "tom", "Dave", None, "badge_conditions is required"),
        ("Bob", "tom", "Dave", [], "badge_conditions cannot be an empty list"),
    ],
)
def test_creator_when_required_parameters_are_missing_raises_value_error(
    name, cm_name, cm_attribute, badge_conditions, message, client
):
    """Test creator validation for required and non-empty fields."""
    with pytest.raises(ValueError, match=message):
        Badge.creator(
            client=client,
            name=name,
            cm_name=cm_name,
            cm_attribute=cm_attribute,
            badge_conditions=badge_conditions,
        )


def test_creator(client):
    """Test creator initializes qualifiedName and metadata attribute from cache."""
    badge = Badge.creator(
        client=client,
        name=BADGE_NAME,
        cm_name=CM_SET_NAME,
        cm_attribute=CM_ATTRIBUTE_NAME,
        badge_conditions=[BADGE_CONDITION],
    )
    assert badge.name == BADGE_NAME
    assert badge.qualified_name == BADGE_QUALIFIED_NAME
    assert badge.badge_metadata_attribute == BADGE_METADATA_ATTRIBUTE
    assert badge.badge_conditions == [BADGE_CONDITION]


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, BADGE_QUALIFIED_NAME, "qualified_name is required"),
        (BADGE_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        Badge.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates Badge for modification."""
    sut = Badge.updater(qualified_name=BADGE_QUALIFIED_NAME, name=BADGE_NAME)

    assert sut.qualified_name == BADGE_QUALIFIED_NAME
    assert sut.name == BADGE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = Badge.updater(
        qualified_name=BADGE_QUALIFIED_NAME, name=BADGE_NAME
    ).trim_to_required()

    assert sut.qualified_name == BADGE_QUALIFIED_NAME
    assert sut.name == BADGE_NAME
