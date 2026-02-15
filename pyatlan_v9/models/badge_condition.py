# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Badge condition struct for pyatlan_v9."""

from __future__ import annotations

from typing import Union

import msgspec

from pyatlan.model.enums import BadgeComparisonOperator, BadgeConditionColor
from pyatlan_v9.utils import validate_required_fields


class BadgeCondition(msgspec.Struct, kw_only=True):
    """Condition used to derive a badge color for a value."""

    badge_condition_operator: Union[str, None] = None
    badge_condition_value: Union[str, None] = None
    badge_condition_colorhex: Union[str, None] = None

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
