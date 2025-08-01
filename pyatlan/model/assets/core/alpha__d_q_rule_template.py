# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import alpha_DQDimension, alpha_DQRuleTemplateMetricValueType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.model.structs import alpha_DQRuleTemplateConfig

from .data_quality import DataQuality


class alpha_DQRuleTemplate(DataQuality):
    """Description"""

    type_name: str = Field(default="alpha_DQRuleTemplate", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "alpha_DQRuleTemplate":
            raise ValueError("must be alpha_DQRuleTemplate")
        return v

    def __setattr__(self, name, value):
        if name in alpha_DQRuleTemplate._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ALPHADQ_RULE_TEMPLATE_DIMENSION: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleTemplateDimension", "alpha_dqRuleTemplateDimension"
    )
    """
    Name of the dimension the rule belongs to
    """
    ALPHADQ_RULE_TEMPLATE_CONFIG: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleTemplateConfig", "alpha_dqRuleTemplateConfig"
    )
    """
    rule config that will help render the form and define the rule.
    """
    ALPHADQ_RULE_TEMPLATE_METRIC_VALUE_TYPE: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleTemplateMetricValueType", "alpha_dqRuleTemplateMetricValueType"
    )
    """
    Type of the metric value returned by the rule(absolute, percentage, time etc.)
    """

    ALPHADQ_RULES: ClassVar[RelationField] = RelationField("alpha_dqRules")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "alpha_dq_rule_template_dimension",
        "alpha_dq_rule_template_config",
        "alpha_dq_rule_template_metric_value_type",
        "alpha_dq_rules",
    ]

    @property
    def alpha_dq_rule_template_dimension(self) -> Optional[alpha_DQDimension]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_template_dimension
        )

    @alpha_dq_rule_template_dimension.setter
    def alpha_dq_rule_template_dimension(
        self, alpha_dq_rule_template_dimension: Optional[alpha_DQDimension]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_template_dimension = (
            alpha_dq_rule_template_dimension
        )

    @property
    def alpha_dq_rule_template_config(self) -> Optional[alpha_DQRuleTemplateConfig]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_template_config
        )

    @alpha_dq_rule_template_config.setter
    def alpha_dq_rule_template_config(
        self, alpha_dq_rule_template_config: Optional[alpha_DQRuleTemplateConfig]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_template_config = alpha_dq_rule_template_config

    @property
    def alpha_dq_rule_template_metric_value_type(
        self,
    ) -> Optional[alpha_DQRuleTemplateMetricValueType]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_template_metric_value_type
        )

    @alpha_dq_rule_template_metric_value_type.setter
    def alpha_dq_rule_template_metric_value_type(
        self,
        alpha_dq_rule_template_metric_value_type: Optional[
            alpha_DQRuleTemplateMetricValueType
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_template_metric_value_type = (
            alpha_dq_rule_template_metric_value_type
        )

    @property
    def alpha_dq_rules(self) -> Optional[List[alpha_DQRule]]:
        return None if self.attributes is None else self.attributes.alpha_dq_rules

    @alpha_dq_rules.setter
    def alpha_dq_rules(self, alpha_dq_rules: Optional[List[alpha_DQRule]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rules = alpha_dq_rules

    class Attributes(DataQuality.Attributes):
        alpha_dq_rule_template_dimension: Optional[alpha_DQDimension] = Field(
            default=None, description=""
        )
        alpha_dq_rule_template_config: Optional[alpha_DQRuleTemplateConfig] = Field(
            default=None, description=""
        )
        alpha_dq_rule_template_metric_value_type: Optional[
            alpha_DQRuleTemplateMetricValueType
        ] = Field(default=None, description="")
        alpha_dq_rules: Optional[List[alpha_DQRule]] = Field(
            default=None, description=""
        )  # relationship

    attributes: alpha_DQRuleTemplate.Attributes = Field(
        default_factory=lambda: alpha_DQRuleTemplate.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .alpha__d_q_rule import alpha_DQRule  # noqa: E402, F401
