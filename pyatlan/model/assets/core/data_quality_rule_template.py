# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    DataQualityDimension,
    DataQualityRuleTemplateMetricValueType,
)
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.model.structs import DataQualityRuleTemplateConfig

from .data_quality import DataQuality


class DataQualityRuleTemplate(DataQuality):
    """Description"""

    type_name: str = Field(default="DataQualityRuleTemplate", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataQualityRuleTemplate":
            raise ValueError("must be DataQualityRuleTemplate")
        return v

    def __setattr__(self, name, value):
        if name in DataQualityRuleTemplate._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DQ_RULE_TEMPLATE_DIMENSION: ClassVar[KeywordField] = KeywordField(
        "dqRuleTemplateDimension", "dqRuleTemplateDimension"
    )
    """
    Name of the dimension the rule belongs to.
    """
    DQ_RULE_TEMPLATE_CONFIG: ClassVar[KeywordField] = KeywordField(
        "dqRuleTemplateConfig", "dqRuleTemplateConfig"
    )
    """
    Rule config that will help render the form and define the rule.
    """
    DQ_RULE_TEMPLATE_METRIC_VALUE_TYPE: ClassVar[KeywordField] = KeywordField(
        "dqRuleTemplateMetricValueType", "dqRuleTemplateMetricValueType"
    )
    """
    Type of the metric value returned by the rule(absolute, percentage, time etc.).
    """

    DQ_RULES: ClassVar[RelationField] = RelationField("dqRules")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dq_rule_template_dimension",
        "dq_rule_template_config",
        "dq_rule_template_metric_value_type",
        "dq_rules",
    ]

    @property
    def dq_rule_template_dimension(self) -> Optional[DataQualityDimension]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_template_dimension
        )

    @dq_rule_template_dimension.setter
    def dq_rule_template_dimension(
        self, dq_rule_template_dimension: Optional[DataQualityDimension]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_template_dimension = dq_rule_template_dimension

    @property
    def dq_rule_template_config(self) -> Optional[DataQualityRuleTemplateConfig]:
        return (
            None if self.attributes is None else self.attributes.dq_rule_template_config
        )

    @dq_rule_template_config.setter
    def dq_rule_template_config(
        self, dq_rule_template_config: Optional[DataQualityRuleTemplateConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_template_config = dq_rule_template_config

    @property
    def dq_rule_template_metric_value_type(
        self,
    ) -> Optional[DataQualityRuleTemplateMetricValueType]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_template_metric_value_type
        )

    @dq_rule_template_metric_value_type.setter
    def dq_rule_template_metric_value_type(
        self,
        dq_rule_template_metric_value_type: Optional[
            DataQualityRuleTemplateMetricValueType
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_template_metric_value_type = (
            dq_rule_template_metric_value_type
        )

    @property
    def dq_rules(self) -> Optional[List[DataQualityRule]]:
        return None if self.attributes is None else self.attributes.dq_rules

    @dq_rules.setter
    def dq_rules(self, dq_rules: Optional[List[DataQualityRule]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rules = dq_rules

    class Attributes(DataQuality.Attributes):
        dq_rule_template_dimension: Optional[DataQualityDimension] = Field(
            default=None, description=""
        )
        dq_rule_template_config: Optional[DataQualityRuleTemplateConfig] = Field(
            default=None, description=""
        )
        dq_rule_template_metric_value_type: Optional[
            DataQualityRuleTemplateMetricValueType
        ] = Field(default=None, description="")
        dq_rules: Optional[List[DataQualityRule]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DataQualityRuleTemplate.Attributes = Field(
        default_factory=lambda: DataQualityRuleTemplate.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .data_quality_rule import DataQualityRule  # noqa: E402, F401
