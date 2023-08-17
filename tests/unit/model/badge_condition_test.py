import pytest

from pyatlan.model.enums import BadgeComparisonOperator, BadgeConditionColor
from pyatlan.model.structs import BadgeCondition


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
def test_create_when_required_parameter_is_missing_then_raises_value_error(
    condition_operator, condition_value, condition_colorhex, message
):
    with pytest.raises(ValueError, match=message):
        BadgeCondition.create(
            badge_condition_operator=condition_operator,
            badge_condition_value=condition_value,
            badge_condition_colorhex=condition_colorhex,
        )


def test_create_with_badge_condition_color():
    condition_operator = BadgeComparisonOperator.EQ
    condition_value = "1"
    condition_colorhex = BadgeConditionColor.RED

    sut = BadgeCondition.create(
        badge_condition_operator=condition_operator,
        badge_condition_value=condition_value,
        badge_condition_colorhex=condition_colorhex,
    )

    assert sut.badge_condition_operator == condition_operator.value
    assert sut.badge_condition_value == condition_value
    assert sut.badge_condition_colorhex == condition_colorhex.value


def test_create_with_badge_condition_color_as_str():
    condition_operator = BadgeComparisonOperator.EQ
    condition_value = "1"
    condition_colorhex = "#BF1B1B"

    sut = BadgeCondition.create(
        badge_condition_operator=condition_operator,
        badge_condition_value=condition_value,
        badge_condition_colorhex=condition_colorhex,
    )

    assert sut.badge_condition_operator == condition_operator.value
    assert sut.badge_condition_value == condition_value
    assert sut.badge_condition_colorhex == condition_colorhex
