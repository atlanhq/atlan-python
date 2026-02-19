# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

import json
from typing import Any, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan.model.enums import DataQualityRuleTemplateConfigRuleConditions
from pyatlan.utils import validate_required_fields, validate_type


class DQCondition(msgspec.Struct, kw_only=True):
    """Data quality rule condition."""

    type: DataQualityRuleTemplateConfigRuleConditions
    """Condition type."""

    value: Union[str, int, list[str], dict[str, Any], None] = None
    """Condition value."""

    min_value: Union[int, None] = None
    """Minimum value for range-based conditions."""

    max_value: Union[int, None] = None
    """Maximum value for range-based conditions."""

    reference_table: Union[str, None] = None
    """Qualified name of the reference table for IN_LIST_REFERENCE condition."""

    reference_column: Union[str, None] = None
    """Qualified name of the reference column for IN_LIST_REFERENCE condition."""

    target_table: Union[str, None] = None
    """Qualified name of the target table for reconciliation conditions."""

    target_column: Union[str, None] = None
    """Qualified name of the target column for reconciliation conditions."""

    def __post_init__(self) -> None:
        """Validate condition fields based on the condition type."""
        DQRTCRC = DataQualityRuleTemplateConfigRuleConditions

        if self.type == DQRTCRC.STRING_LENGTH_BETWEEN:
            validate_required_fields(
                ["min_value", "max_value"], [self.min_value, self.max_value]
            )
            if (self.min_value is not None and self.min_value < 0) or (
                self.max_value is not None and self.max_value < 0
            ):
                raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                    f"min_value={self.min_value}, max_value={self.max_value}",
                    "min_value, max_value",
                    "non-negative integers",
                )
            if (
                self.min_value is not None
                and self.max_value is not None
                and self.min_value > self.max_value
            ):
                raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                    f"min_value={self.min_value}, max_value={self.max_value}",
                    "min_value, max_value",
                    "min_value <= max_value",
                )
        elif self.type == DQRTCRC.IN_LIST_REFERENCE:
            validate_required_fields(
                ["reference_table", "reference_column"],
                [self.reference_table, self.reference_column],
            )
        elif self.type == DQRTCRC.ROW_COUNT_RECON:
            validate_required_fields(["target_table"], [self.target_table])
        elif self.type in [
            DQRTCRC.AVERAGE_RECON,
            DQRTCRC.SUM_RECON,
            DQRTCRC.DUPLICATE_COUNT_RECON,
            DQRTCRC.UNIQUE_COUNT_RECON,
        ]:
            validate_required_fields(
                ["target_table", "target_column"],
                [self.target_table, self.target_column],
            )
        else:
            validate_required_fields(["value"], [self.value])
            if self.type in [DQRTCRC.IN_LIST, DQRTCRC.NOT_IN_LIST]:
                validate_type("value", list, self.value)
            elif self.type in [DQRTCRC.REGEX_MATCH, DQRTCRC.REGEX_NOT_MATCH]:
                validate_type("value", str, self.value)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict suitable for API submission."""
        DQRTCRC = DataQualityRuleTemplateConfigRuleConditions
        result: dict[str, Any] = {"type": self.type.value}

        if self.type == DQRTCRC.STRING_LENGTH_BETWEEN:
            result["value"] = {"minValue": self.min_value, "maxValue": self.max_value}
        elif self.type == DQRTCRC.IN_LIST_REFERENCE:
            result["value"] = {
                "reference_table": self.reference_table,
                "reference_column": self.reference_column,
            }
        elif self.type == DQRTCRC.ROW_COUNT_RECON:
            result["value"] = {"target_table": self.target_table}
        elif self.type in [
            DQRTCRC.AVERAGE_RECON,
            DQRTCRC.SUM_RECON,
            DQRTCRC.DUPLICATE_COUNT_RECON,
            DQRTCRC.UNIQUE_COUNT_RECON,
        ]:
            result["value"] = {
                "target_table": self.target_table,
                "target_column": self.target_column,
            }
        else:
            result["value"] = {"value": self.value}

        return result


class DQRuleConditionsBuilder:
    """Builder for data quality rule conditions."""

    def __init__(self) -> None:
        self._conditions: list[DQCondition] = []

    def add_condition(
        self,
        type: DataQualityRuleTemplateConfigRuleConditions,
        value: Union[str, int, list[str], None] = None,
        min_value: Union[int, None] = None,
        max_value: Union[int, None] = None,
        reference_table: Union[str, None] = None,
        reference_column: Union[str, None] = None,
        target_table: Union[str, None] = None,
        target_column: Union[str, None] = None,
    ) -> DQRuleConditionsBuilder:
        """
        Add a condition to the builder.

        :param type: the condition type enum value
        :param value: value of type str, int, or list depending on condition type
        :param min_value: minimum value for range-based conditions
        :param max_value: maximum value for range-based conditions
        :param reference_table: qualified name of the reference table
        :param reference_column: qualified name of the reference column
        :param target_table: qualified name of the target table
        :param target_column: qualified name of the target column
        :returns: the builder for method chaining
        """
        self._conditions.append(
            DQCondition(
                type=type,
                value=value,
                min_value=min_value,
                max_value=max_value,
                reference_table=reference_table,
                reference_column=reference_column,
                target_table=target_table,
                target_column=target_column,
            )
        )
        return self

    def build(self) -> str:
        """
        Build the conditions JSON string.

        :returns: JSON string of the conditions
        :raises: InvalidRequestError if conditions list is empty
        """
        if not self._conditions:
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                "empty conditions list", "conditions", "at least one condition"
            )

        return json.dumps(
            {"conditions": [condition.to_dict() for condition in self._conditions]}
        )
