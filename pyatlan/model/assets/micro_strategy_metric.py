# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .micro_strategy import MicroStrategy


class MicroStrategyMetric(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyMetric":
            raise ValueError("must be MicroStrategyMetric")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyMetric._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_METRIC_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "microStrategyMetricExpression", "microStrategyMetricExpression"
    )
    """
    Text specifiying this metric's expression.
    """
    MICRO_STRATEGY_ATTRIBUTE_QUALIFIED_NAMES: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyAttributeQualifiedNames",
            "microStrategyAttributeQualifiedNames",
            "microStrategyAttributeQualifiedNames.text",
        )
    )
    """
    List of unique names of attributes related to this metric.
    """
    MICRO_STRATEGY_ATTRIBUTE_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyAttributeNames",
        "microStrategyAttributeNames.keyword",
        "microStrategyAttributeNames",
    )
    """
    List of simple names of attributes related to this metric.
    """
    MICRO_STRATEGY_FACT_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyFactQualifiedNames",
        "microStrategyFactQualifiedNames",
        "microStrategyFactQualifiedNames.text",
    )
    """
    List of unique names of facts related to this metric.
    """
    MICRO_STRATEGY_FACT_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyFactNames",
        "microStrategyFactNames.keyword",
        "microStrategyFactNames",
    )
    """
    List of simple names of facts related to this metric.
    """
    MICRO_STRATEGY_METRIC_PARENT_QUALIFIED_NAMES: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyMetricParentQualifiedNames",
            "microStrategyMetricParentQualifiedNames",
            "microStrategyMetricParentQualifiedNames.text",
        )
    )
    """
    List of unique names of parent metrics of this metric.
    """
    MICRO_STRATEGY_METRIC_PARENT_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyMetricParentNames",
        "microStrategyMetricParentNames.keyword",
        "microStrategyMetricParentNames",
    )
    """
    List of simple names of parent metrics of this metric.
    """

    MICRO_STRATEGY_METRIC_PARENTS: ClassVar[RelationField] = RelationField(
        "microStrategyMetricParents"
    )
    """
    TBC
    """
    MICRO_STRATEGY_FACTS: ClassVar[RelationField] = RelationField("microStrategyFacts")
    """
    TBC
    """
    MICRO_STRATEGY_REPORTS: ClassVar[RelationField] = RelationField(
        "microStrategyReports"
    )
    """
    TBC
    """
    MICRO_STRATEGY_CUBES: ClassVar[RelationField] = RelationField("microStrategyCubes")
    """
    TBC
    """
    MICRO_STRATEGY_METRIC_CHILDREN: ClassVar[RelationField] = RelationField(
        "microStrategyMetricChildren"
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
    MICRO_STRATEGY_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "microStrategyAttributes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "micro_strategy_metric_expression",
        "micro_strategy_attribute_qualified_names",
        "micro_strategy_attribute_names",
        "micro_strategy_fact_qualified_names",
        "micro_strategy_fact_names",
        "micro_strategy_metric_parent_qualified_names",
        "micro_strategy_metric_parent_names",
        "micro_strategy_metric_parents",
        "micro_strategy_facts",
        "micro_strategy_reports",
        "micro_strategy_cubes",
        "micro_strategy_metric_children",
        "micro_strategy_project",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_metric_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_expression
        )

    @micro_strategy_metric_expression.setter
    def micro_strategy_metric_expression(
        self, micro_strategy_metric_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_expression = (
            micro_strategy_metric_expression
        )

    @property
    def micro_strategy_attribute_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_qualified_names
        )

    @micro_strategy_attribute_qualified_names.setter
    def micro_strategy_attribute_qualified_names(
        self, micro_strategy_attribute_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_qualified_names = (
            micro_strategy_attribute_qualified_names
        )

    @property
    def micro_strategy_attribute_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_names
        )

    @micro_strategy_attribute_names.setter
    def micro_strategy_attribute_names(
        self, micro_strategy_attribute_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_names = micro_strategy_attribute_names

    @property
    def micro_strategy_fact_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_qualified_names
        )

    @micro_strategy_fact_qualified_names.setter
    def micro_strategy_fact_qualified_names(
        self, micro_strategy_fact_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_qualified_names = (
            micro_strategy_fact_qualified_names
        )

    @property
    def micro_strategy_fact_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_names
        )

    @micro_strategy_fact_names.setter
    def micro_strategy_fact_names(self, micro_strategy_fact_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_names = micro_strategy_fact_names

    @property
    def micro_strategy_metric_parent_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parent_qualified_names
        )

    @micro_strategy_metric_parent_qualified_names.setter
    def micro_strategy_metric_parent_qualified_names(
        self, micro_strategy_metric_parent_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parent_qualified_names = (
            micro_strategy_metric_parent_qualified_names
        )

    @property
    def micro_strategy_metric_parent_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parent_names
        )

    @micro_strategy_metric_parent_names.setter
    def micro_strategy_metric_parent_names(
        self, micro_strategy_metric_parent_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parent_names = (
            micro_strategy_metric_parent_names
        )

    @property
    def micro_strategy_metric_parents(self) -> Optional[List[MicroStrategyMetric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parents
        )

    @micro_strategy_metric_parents.setter
    def micro_strategy_metric_parents(
        self, micro_strategy_metric_parents: Optional[List[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parents = micro_strategy_metric_parents

    @property
    def micro_strategy_facts(self) -> Optional[List[MicroStrategyFact]]:
        return None if self.attributes is None else self.attributes.micro_strategy_facts

    @micro_strategy_facts.setter
    def micro_strategy_facts(
        self, micro_strategy_facts: Optional[List[MicroStrategyFact]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_facts = micro_strategy_facts

    @property
    def micro_strategy_reports(self) -> Optional[List[MicroStrategyReport]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_reports
        )

    @micro_strategy_reports.setter
    def micro_strategy_reports(
        self, micro_strategy_reports: Optional[List[MicroStrategyReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_reports = micro_strategy_reports

    @property
    def micro_strategy_cubes(self) -> Optional[List[MicroStrategyCube]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cubes

    @micro_strategy_cubes.setter
    def micro_strategy_cubes(
        self, micro_strategy_cubes: Optional[List[MicroStrategyCube]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cubes = micro_strategy_cubes

    @property
    def micro_strategy_metric_children(self) -> Optional[List[MicroStrategyMetric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_children
        )

    @micro_strategy_metric_children.setter
    def micro_strategy_metric_children(
        self, micro_strategy_metric_children: Optional[List[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_children = micro_strategy_metric_children

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

    @property
    def micro_strategy_attributes(self) -> Optional[List[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[List[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_metric_expression: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_attribute_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_attribute_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_fact_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_fact_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_metric_parent_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_metric_parent_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_metric_parents: Optional[List[MicroStrategyMetric]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_facts: Optional[List[MicroStrategyFact]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_reports: Optional[List[MicroStrategyReport]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_cubes: Optional[List[MicroStrategyCube]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_metric_children: Optional[List[MicroStrategyMetric]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_attributes: Optional[List[MicroStrategyAttribute]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyMetric.Attributes = Field(
        default_factory=lambda: MicroStrategyMetric.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_attribute import MicroStrategyAttribute  # noqa
from .micro_strategy_cube import MicroStrategyCube  # noqa
from .micro_strategy_fact import MicroStrategyFact  # noqa
from .micro_strategy_project import MicroStrategyProject  # noqa
from .micro_strategy_report import MicroStrategyReport  # noqa
