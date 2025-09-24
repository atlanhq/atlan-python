# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import Field

from pyatlan.errors import ErrorCode
from pyatlan.model.enums import DataQualityRuleTemplateConfigRuleConditions
from pyatlan.model.structs import AtlanObject
from pyatlan.utils import validate_required_fields, validate_type


class DQCondition(AtlanObject):
    """Data quality rule condition."""

    type: DataQualityRuleTemplateConfigRuleConditions = Field(description="")
    value: Optional[Union[str, int, List[str], Dict[str, Any]]] = Field(
        default=None, description=""
    )
    min_value: Optional[int] = Field(default=None, description="")
    max_value: Optional[int] = Field(default=None, description="")

    def __init__(
        self,
        type: DataQualityRuleTemplateConfigRuleConditions,
        value: Optional[Union[str, int, List[str], Dict[str, Any]]] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(
            type=type, value=value, min_value=min_value, max_value=max_value, **kwargs
        )

        if (
            self.type
            == DataQualityRuleTemplateConfigRuleConditions.STRING_LENGTH_BETWEEN
        ):
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
        else:
            validate_required_fields(["value"], [self.value])
            if self.type in [
                DataQualityRuleTemplateConfigRuleConditions.IN_LIST,
                DataQualityRuleTemplateConfigRuleConditions.NOT_IN_LIST,
            ]:
                validate_type("value", list, self.value)
            elif self.type in [
                DataQualityRuleTemplateConfigRuleConditions.REGEX_MATCH,
                DataQualityRuleTemplateConfigRuleConditions.REGEX_NOT_MATCH,
            ]:
                validate_type("value", str, self.value)

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"type": self.type.value}

        if (
            self.type
            == DataQualityRuleTemplateConfigRuleConditions.STRING_LENGTH_BETWEEN
        ):
            result["value"] = {"minValue": self.min_value, "maxValue": self.max_value}
        else:
            result["value"] = {"value": self.value}

        return result


class DQRuleConditionsBuilder:
    """Builder for data quality rule conditions."""

    def __init__(self) -> None:
        self._conditions: List[DQCondition] = []

    def add_condition(
        self,
        type: DataQualityRuleTemplateConfigRuleConditions,
        value: Optional[Union[str, int, List[str]]] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ) -> DQRuleConditionsBuilder:
        """
        Add a condition to the builder.

        :param type: the condition type enum value
        :param value: value of type str, int, or list depending on condition type
        :param min_value: minimum value for range-based conditions
        :param max_value: maximum value for range-based conditions
        :returns: the builder for method chaining
        """
        self._conditions.append(
            DQCondition(
                type=type, value=value, min_value=min_value, max_value=max_value
            )
        )
        return self

    def build(self) -> str:
        if not self._conditions:
            raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                "empty conditions list", "conditions", "at least one condition"
            )

        return json.dumps(
            {"conditions": [condition.to_dict() for condition in self._conditions]}
        )


DQCondition.update_forward_refs()
