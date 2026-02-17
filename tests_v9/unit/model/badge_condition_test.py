# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for BadgeCondition in pyatlan_v9."""

import pytest

from pyatlan.model.enums import BadgeComparisonOperator, BadgeConditionColor
from pyatlan_v9.model import BadgeCondition


@pytest.mark.parametrize(
    "condition_operator, condition_value, condition_colorhex, message",
    [
        (
            None,
            "1",
            BadgeConditionColor.RED,
            "badge_condition_operator is required",
        ),
        (
            BadgeComparisonOperator.EQ,
            None,
            BadgeConditionColor.RED,
            "badge_condition_value is required",
        ),
        (
            BadgeComparisonOperator.EQ,
            "1",
            None,
            "badge_condition_colorhex is required",
        ),
    ],
)
def test_creator_when_required_parameter_is_missing_then_raises_value_error(
    condition_operator, condition_value, condition_colorhex, message
):
    """Test creator validation for required fields."""
    with pytest.raises(ValueError, match=message):
        BadgeCondition.creator(
            badge_condition_operator=condition_operator,
            badge_condition_value=condition_value,
            badge_condition_colorhex=condition_colorhex,
        )


def test_creator_with_badge_condition_color():
    """Test creator with enum-based badge color."""
    condition_operator = BadgeComparisonOperator.EQ
    condition_value = "1"
    condition_colorhex = BadgeConditionColor.RED

    sut = BadgeCondition.creator(
        badge_condition_operator=condition_operator,
        badge_condition_value=condition_value,
        badge_condition_colorhex=condition_colorhex,
    )

    assert sut.badge_condition_operator == condition_operator.value
    assert sut.badge_condition_value == condition_value
    assert sut.badge_condition_colorhex == condition_colorhex.value


def test_creator_with_badge_condition_color_as_str():
    """Test creator with literal color string."""
    condition_operator = BadgeComparisonOperator.EQ
    condition_value = "1"
    condition_colorhex = "#BF1B1B"

    sut = BadgeCondition.creator(
        badge_condition_operator=condition_operator,
        badge_condition_value=condition_value,
        badge_condition_colorhex=condition_colorhex,
    )

    assert sut.badge_condition_operator == condition_operator.value
    assert sut.badge_condition_value == condition_value
    assert sut.badge_condition_colorhex == condition_colorhex
