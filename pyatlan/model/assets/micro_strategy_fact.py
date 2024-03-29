# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .micro_strategy import MicroStrategy


class MicroStrategyFact(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyFact", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyFact":
            raise ValueError("must be MicroStrategyFact")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyFact._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_FACT_EXPRESSIONS: ClassVar[KeywordField] = KeywordField(
        "microStrategyFactExpressions", "microStrategyFactExpressions"
    )
    """
    List of expressions for this fact.
    """

    MICRO_STRATEGY_METRICS: ClassVar[RelationField] = RelationField(
        "microStrategyMetrics"
    )
    """
    TBC
    """
    MICRO_STRATEGY_PROJECT: ClassVar[RelationField] = RelationField(
        "microStrategyProject"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "micro_strategy_fact_expressions",
        "micro_strategy_metrics",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_fact_expressions(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_expressions
        )

    @micro_strategy_fact_expressions.setter
    def micro_strategy_fact_expressions(
        self, micro_strategy_fact_expressions: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_expressions = (
            micro_strategy_fact_expressions
        )

    @property
    def micro_strategy_metrics(self) -> Optional[List[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[List[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_project(self) -> Optional[MicroStrategyProject]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_project
        )

    @micro_strategy_project.setter
    def micro_strategy_project(
        self, micro_strategy_project: Optional[MicroStrategyProject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_project = micro_strategy_project

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_fact_expressions: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_metrics: Optional[List[MicroStrategyMetric]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyFact.Attributes = Field(
        default_factory=lambda: MicroStrategyFact.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_metric import MicroStrategyMetric  # noqa
from .micro_strategy_project import MicroStrategyProject  # noqa
