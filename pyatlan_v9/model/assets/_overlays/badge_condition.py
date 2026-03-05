# IMPORT: from pyatlan.model.enums import BadgeComparisonOperator, BadgeConditionColor
# INTERNAL_IMPORT: from pyatlan.utils import validate_required_fields

    @classmethod
    def creator(
        cls,
        *,
        badge_condition_operator: BadgeComparisonOperator,
        badge_condition_value: str,
        badge_condition_colorhex: Union[BadgeConditionColor, str],
    ) -> "BadgeCondition":
        """Create a badge condition."""
        validate_required_fields(
            [
                "badge_condition_operator",
                "badge_condition_value",
                "badge_condition_colorhex",
            ],
            [badge_condition_operator, badge_condition_value, badge_condition_colorhex],
        )
        return cls(
            badge_condition_operator=badge_condition_operator.value,
            badge_condition_value=badge_condition_value,
            badge_condition_colorhex=(
                badge_condition_colorhex.value
                if isinstance(badge_condition_colorhex, BadgeConditionColor)
                else badge_condition_colorhex
            ),
        )
