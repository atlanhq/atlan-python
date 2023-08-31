# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .asset47 import MicroStrategy


class MicroStrategyReport(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyReport":
            raise ValueError("must be MicroStrategyReport")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_REPORT_TYPE: ClassVar[KeywordField] = KeywordField(
        "microStrategyReportType", "microStrategyReportType"
    )
    """
    Whether the report is a Grid or Chart report
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
    MICRO_STRATEGY_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "microStrategyAttributes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_report_type",
        "micro_strategy_metrics",
        "micro_strategy_project",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_report_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_report_type
        )

    @micro_strategy_report_type.setter
    def micro_strategy_report_type(self, micro_strategy_report_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_report_type = micro_strategy_report_type

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
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

    @property
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_report_type: Optional[str] = Field(
            None, description="", alias="microStrategyReportType"
        )
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyReport.Attributes" = Field(
        default_factory=lambda: MicroStrategyReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyProject(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyProject":
            raise ValueError("must be MicroStrategyProject")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyProject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_REPORTS: ClassVar[RelationField] = RelationField(
        "microStrategyReports"
    )
    """
    TBC
    """
    MICRO_STRATEGY_FACTS: ClassVar[RelationField] = RelationField("microStrategyFacts")
    """
    TBC
    """
    MICRO_STRATEGY_METRICS: ClassVar[RelationField] = RelationField(
        "microStrategyMetrics"
    )
    """
    TBC
    """
    MICRO_STRATEGY_VISUALIZATIONS: ClassVar[RelationField] = RelationField(
        "microStrategyVisualizations"
    )
    """
    TBC
    """
    MICRO_STRATEGY_DOCUMENTS: ClassVar[RelationField] = RelationField(
        "microStrategyDocuments"
    )
    """
    TBC
    """
    MICRO_STRATEGY_CUBES: ClassVar[RelationField] = RelationField("microStrategyCubes")
    """
    TBC
    """
    MICRO_STRATEGY_DOSSIERS: ClassVar[RelationField] = RelationField(
        "microStrategyDossiers"
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

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_reports",
        "micro_strategy_facts",
        "micro_strategy_metrics",
        "micro_strategy_visualizations",
        "micro_strategy_documents",
        "micro_strategy_cubes",
        "micro_strategy_dossiers",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_reports(self) -> Optional[list[MicroStrategyReport]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_reports
        )

    @micro_strategy_reports.setter
    def micro_strategy_reports(
        self, micro_strategy_reports: Optional[list[MicroStrategyReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_reports = micro_strategy_reports

    @property
    def micro_strategy_facts(self) -> Optional[list[MicroStrategyFact]]:
        return None if self.attributes is None else self.attributes.micro_strategy_facts

    @micro_strategy_facts.setter
    def micro_strategy_facts(
        self, micro_strategy_facts: Optional[list[MicroStrategyFact]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_facts = micro_strategy_facts

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_visualizations(
        self,
    ) -> Optional[list[MicroStrategyVisualization]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_visualizations
        )

    @micro_strategy_visualizations.setter
    def micro_strategy_visualizations(
        self, micro_strategy_visualizations: Optional[list[MicroStrategyVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_visualizations = micro_strategy_visualizations

    @property
    def micro_strategy_documents(self) -> Optional[list[MicroStrategyDocument]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_documents
        )

    @micro_strategy_documents.setter
    def micro_strategy_documents(
        self, micro_strategy_documents: Optional[list[MicroStrategyDocument]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_documents = micro_strategy_documents

    @property
    def micro_strategy_cubes(self) -> Optional[list[MicroStrategyCube]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cubes

    @micro_strategy_cubes.setter
    def micro_strategy_cubes(
        self, micro_strategy_cubes: Optional[list[MicroStrategyCube]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cubes = micro_strategy_cubes

    @property
    def micro_strategy_dossiers(self) -> Optional[list[MicroStrategyDossier]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_dossiers
        )

    @micro_strategy_dossiers.setter
    def micro_strategy_dossiers(
        self, micro_strategy_dossiers: Optional[list[MicroStrategyDossier]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossiers = micro_strategy_dossiers

    @property
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_reports: Optional[list[MicroStrategyReport]] = Field(
            None, description="", alias="microStrategyReports"
        )  # relationship
        micro_strategy_facts: Optional[list[MicroStrategyFact]] = Field(
            None, description="", alias="microStrategyFacts"
        )  # relationship
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_visualizations: Optional[
            list[MicroStrategyVisualization]
        ] = Field(
            None, description="", alias="microStrategyVisualizations"
        )  # relationship
        micro_strategy_documents: Optional[list[MicroStrategyDocument]] = Field(
            None, description="", alias="microStrategyDocuments"
        )  # relationship
        micro_strategy_cubes: Optional[list[MicroStrategyCube]] = Field(
            None, description="", alias="microStrategyCubes"
        )  # relationship
        micro_strategy_dossiers: Optional[list[MicroStrategyDossier]] = Field(
            None, description="", alias="microStrategyDossiers"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyProject.Attributes" = Field(
        default_factory=lambda: MicroStrategyProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyMetric(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyMetric", allow_mutation=False)

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
    Metric expression text
    """
    MICRO_STRATEGY_ATTRIBUTE_QUALIFIED_NAMES: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "microStrategyAttributeQualifiedNames",
        "microStrategyAttributeQualifiedNames",
        "microStrategyAttributeQualifiedNames.text",
    )
    """
    Related attribute qualified name list
    """
    MICRO_STRATEGY_ATTRIBUTE_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyAttributeNames",
        "microStrategyAttributeNames.keyword",
        "microStrategyAttributeNames",
    )
    """
    Related attribute name list
    """
    MICRO_STRATEGY_FACT_QUALIFIED_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyFactQualifiedNames",
        "microStrategyFactQualifiedNames",
        "microStrategyFactQualifiedNames.text",
    )
    """
    Related fact qualified name list
    """
    MICRO_STRATEGY_FACT_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyFactNames",
        "microStrategyFactNames.keyword",
        "microStrategyFactNames",
    )
    """
    Related fact name list
    """
    MICRO_STRATEGY_METRIC_PARENT_QUALIFIED_NAMES: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "microStrategyMetricParentQualifiedNames",
        "microStrategyMetricParentQualifiedNames",
        "microStrategyMetricParentQualifiedNames.text",
    )
    """
    Related parent metric qualified name list
    """
    MICRO_STRATEGY_METRIC_PARENT_NAMES: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyMetricParentNames",
        "microStrategyMetricParentNames.keyword",
        "microStrategyMetricParentNames",
    )
    """
    Related parent metric name list
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

    _convenience_properties: ClassVar[list[str]] = [
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
    def micro_strategy_attribute_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_qualified_names
        )

    @micro_strategy_attribute_qualified_names.setter
    def micro_strategy_attribute_qualified_names(
        self, micro_strategy_attribute_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_qualified_names = (
            micro_strategy_attribute_qualified_names
        )

    @property
    def micro_strategy_attribute_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_names
        )

    @micro_strategy_attribute_names.setter
    def micro_strategy_attribute_names(
        self, micro_strategy_attribute_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_names = micro_strategy_attribute_names

    @property
    def micro_strategy_fact_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_qualified_names
        )

    @micro_strategy_fact_qualified_names.setter
    def micro_strategy_fact_qualified_names(
        self, micro_strategy_fact_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_qualified_names = (
            micro_strategy_fact_qualified_names
        )

    @property
    def micro_strategy_fact_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_names
        )

    @micro_strategy_fact_names.setter
    def micro_strategy_fact_names(self, micro_strategy_fact_names: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_names = micro_strategy_fact_names

    @property
    def micro_strategy_metric_parent_qualified_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parent_qualified_names
        )

    @micro_strategy_metric_parent_qualified_names.setter
    def micro_strategy_metric_parent_qualified_names(
        self, micro_strategy_metric_parent_qualified_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parent_qualified_names = (
            micro_strategy_metric_parent_qualified_names
        )

    @property
    def micro_strategy_metric_parent_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parent_names
        )

    @micro_strategy_metric_parent_names.setter
    def micro_strategy_metric_parent_names(
        self, micro_strategy_metric_parent_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parent_names = (
            micro_strategy_metric_parent_names
        )

    @property
    def micro_strategy_metric_parents(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_parents
        )

    @micro_strategy_metric_parents.setter
    def micro_strategy_metric_parents(
        self, micro_strategy_metric_parents: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metric_parents = micro_strategy_metric_parents

    @property
    def micro_strategy_facts(self) -> Optional[list[MicroStrategyFact]]:
        return None if self.attributes is None else self.attributes.micro_strategy_facts

    @micro_strategy_facts.setter
    def micro_strategy_facts(
        self, micro_strategy_facts: Optional[list[MicroStrategyFact]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_facts = micro_strategy_facts

    @property
    def micro_strategy_reports(self) -> Optional[list[MicroStrategyReport]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_reports
        )

    @micro_strategy_reports.setter
    def micro_strategy_reports(
        self, micro_strategy_reports: Optional[list[MicroStrategyReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_reports = micro_strategy_reports

    @property
    def micro_strategy_cubes(self) -> Optional[list[MicroStrategyCube]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cubes

    @micro_strategy_cubes.setter
    def micro_strategy_cubes(
        self, micro_strategy_cubes: Optional[list[MicroStrategyCube]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cubes = micro_strategy_cubes

    @property
    def micro_strategy_metric_children(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_metric_children
        )

    @micro_strategy_metric_children.setter
    def micro_strategy_metric_children(
        self, micro_strategy_metric_children: Optional[list[MicroStrategyMetric]]
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
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_metric_expression: Optional[str] = Field(
            None, description="", alias="microStrategyMetricExpression"
        )
        micro_strategy_attribute_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyAttributeQualifiedNames"
        )
        micro_strategy_attribute_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyAttributeNames"
        )
        micro_strategy_fact_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyFactQualifiedNames"
        )
        micro_strategy_fact_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyFactNames"
        )
        micro_strategy_metric_parent_qualified_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyMetricParentQualifiedNames"
        )
        micro_strategy_metric_parent_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyMetricParentNames"
        )
        micro_strategy_metric_parents: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetricParents"
        )  # relationship
        micro_strategy_facts: Optional[list[MicroStrategyFact]] = Field(
            None, description="", alias="microStrategyFacts"
        )  # relationship
        micro_strategy_reports: Optional[list[MicroStrategyReport]] = Field(
            None, description="", alias="microStrategyReports"
        )  # relationship
        micro_strategy_cubes: Optional[list[MicroStrategyCube]] = Field(
            None, description="", alias="microStrategyCubes"
        )  # relationship
        micro_strategy_metric_children: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetricChildren"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyMetric.Attributes" = Field(
        default_factory=lambda: MicroStrategyMetric.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyCube(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyCube", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyCube":
            raise ValueError("must be MicroStrategyCube")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyCube._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_CUBE_TYPE: ClassVar[KeywordField] = KeywordField(
        "microStrategyCubeType", "microStrategyCubeType"
    )
    """
    Whether the cube is an OLAP or MTDI cube
    """
    MICRO_STRATEGY_CUBE_QUERY: ClassVar[KeywordField] = KeywordField(
        "microStrategyCubeQuery", "microStrategyCubeQuery"
    )
    """
    The query used to create the cube
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
    MICRO_STRATEGY_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "microStrategyAttributes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_cube_type",
        "micro_strategy_cube_query",
        "micro_strategy_metrics",
        "micro_strategy_project",
        "micro_strategy_attributes",
    ]

    @property
    def micro_strategy_cube_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_type
        )

    @micro_strategy_cube_type.setter
    def micro_strategy_cube_type(self, micro_strategy_cube_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_type = micro_strategy_cube_type

    @property
    def micro_strategy_cube_query(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_cube_query
        )

    @micro_strategy_cube_query.setter
    def micro_strategy_cube_query(self, micro_strategy_cube_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cube_query = micro_strategy_cube_query

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
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

    @property
    def micro_strategy_attributes(self) -> Optional[list[MicroStrategyAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attributes
        )

    @micro_strategy_attributes.setter
    def micro_strategy_attributes(
        self, micro_strategy_attributes: Optional[list[MicroStrategyAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attributes = micro_strategy_attributes

    class Attributes(MicroStrategy.Attributes):
        micro_strategy_cube_type: Optional[str] = Field(
            None, description="", alias="microStrategyCubeType"
        )
        micro_strategy_cube_query: Optional[str] = Field(
            None, description="", alias="microStrategyCubeQuery"
        )
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            None, description="", alias="microStrategyAttributes"
        )  # relationship

    attributes: "MicroStrategyCube.Attributes" = Field(
        default_factory=lambda: MicroStrategyCube.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyDossier(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyDossier", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyDossier":
            raise ValueError("must be MicroStrategyDossier")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyDossier._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_DOSSIER_CHAPTER_NAMES: ClassVar[KeywordField] = KeywordField(
        "microStrategyDossierChapterNames", "microStrategyDossierChapterNames"
    )
    """
    Dossier chapter name list
    """

    MICRO_STRATEGY_VISUALIZATIONS: ClassVar[RelationField] = RelationField(
        "microStrategyVisualizations"
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

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_dossier_chapter_names",
        "micro_strategy_visualizations",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_dossier_chapter_names(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_dossier_chapter_names
        )

    @micro_strategy_dossier_chapter_names.setter
    def micro_strategy_dossier_chapter_names(
        self, micro_strategy_dossier_chapter_names: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier_chapter_names = (
            micro_strategy_dossier_chapter_names
        )

    @property
    def micro_strategy_visualizations(
        self,
    ) -> Optional[list[MicroStrategyVisualization]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_visualizations
        )

    @micro_strategy_visualizations.setter
    def micro_strategy_visualizations(
        self, micro_strategy_visualizations: Optional[list[MicroStrategyVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_visualizations = micro_strategy_visualizations

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
        micro_strategy_dossier_chapter_names: Optional[set[str]] = Field(
            None, description="", alias="microStrategyDossierChapterNames"
        )
        micro_strategy_visualizations: Optional[
            list[MicroStrategyVisualization]
        ] = Field(
            None, description="", alias="microStrategyVisualizations"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyDossier.Attributes" = Field(
        default_factory=lambda: MicroStrategyDossier.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyFact(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyFact", allow_mutation=False)

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
    Fact expression list
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

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_fact_expressions",
        "micro_strategy_metrics",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_fact_expressions(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_fact_expressions
        )

    @micro_strategy_fact_expressions.setter
    def micro_strategy_fact_expressions(
        self, micro_strategy_fact_expressions: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_fact_expressions = (
            micro_strategy_fact_expressions
        )

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
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
        micro_strategy_fact_expressions: Optional[set[str]] = Field(
            None, description="", alias="microStrategyFactExpressions"
        )
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyFact.Attributes" = Field(
        default_factory=lambda: MicroStrategyFact.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyDocument(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyDocument", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyDocument":
            raise ValueError("must be MicroStrategyDocument")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyDocument._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_PROJECT: ClassVar[RelationField] = RelationField(
        "microStrategyProject"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_project",
    ]

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
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyDocument.Attributes" = Field(
        default_factory=lambda: MicroStrategyDocument.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyAttribute(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyAttribute", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyAttribute":
            raise ValueError("must be MicroStrategyAttribute")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyAttribute._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_ATTRIBUTE_FORMS: ClassVar[KeywordField] = KeywordField(
        "microStrategyAttributeForms", "microStrategyAttributeForms"
    )
    """
    Attribute form name, description, displayFormat and expression as JSON string
    """

    MICRO_STRATEGY_REPORTS: ClassVar[RelationField] = RelationField(
        "microStrategyReports"
    )
    """
    TBC
    """
    MICRO_STRATEGY_METRICS: ClassVar[RelationField] = RelationField(
        "microStrategyMetrics"
    )
    """
    TBC
    """
    MICRO_STRATEGY_CUBES: ClassVar[RelationField] = RelationField("microStrategyCubes")
    """
    TBC
    """
    MICRO_STRATEGY_PROJECT: ClassVar[RelationField] = RelationField(
        "microStrategyProject"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_attribute_forms",
        "micro_strategy_reports",
        "micro_strategy_metrics",
        "micro_strategy_cubes",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_attribute_forms(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_attribute_forms
        )

    @micro_strategy_attribute_forms.setter
    def micro_strategy_attribute_forms(
        self, micro_strategy_attribute_forms: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_attribute_forms = micro_strategy_attribute_forms

    @property
    def micro_strategy_reports(self) -> Optional[list[MicroStrategyReport]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_reports
        )

    @micro_strategy_reports.setter
    def micro_strategy_reports(
        self, micro_strategy_reports: Optional[list[MicroStrategyReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_reports = micro_strategy_reports

    @property
    def micro_strategy_metrics(self) -> Optional[list[MicroStrategyMetric]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_metrics
        )

    @micro_strategy_metrics.setter
    def micro_strategy_metrics(
        self, micro_strategy_metrics: Optional[list[MicroStrategyMetric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_metrics = micro_strategy_metrics

    @property
    def micro_strategy_cubes(self) -> Optional[list[MicroStrategyCube]]:
        return None if self.attributes is None else self.attributes.micro_strategy_cubes

    @micro_strategy_cubes.setter
    def micro_strategy_cubes(
        self, micro_strategy_cubes: Optional[list[MicroStrategyCube]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_cubes = micro_strategy_cubes

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
        micro_strategy_attribute_forms: Optional[str] = Field(
            None, description="", alias="microStrategyAttributeForms"
        )
        micro_strategy_reports: Optional[list[MicroStrategyReport]] = Field(
            None, description="", alias="microStrategyReports"
        )  # relationship
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            None, description="", alias="microStrategyMetrics"
        )  # relationship
        micro_strategy_cubes: Optional[list[MicroStrategyCube]] = Field(
            None, description="", alias="microStrategyCubes"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyAttribute.Attributes" = Field(
        default_factory=lambda: MicroStrategyAttribute.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MicroStrategyVisualization(MicroStrategy):
    """Description"""

    type_name: str = Field("MicroStrategyVisualization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MicroStrategyVisualization":
            raise ValueError("must be MicroStrategyVisualization")
        return v

    def __setattr__(self, name, value):
        if name in MicroStrategyVisualization._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MICRO_STRATEGY_VISUALIZATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "microStrategyVisualizationType", "microStrategyVisualizationType"
    )
    """
    Visualization type name
    """
    MICRO_STRATEGY_DOSSIER_QUALIFIED_NAME: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "microStrategyDossierQualifiedName",
        "microStrategyDossierQualifiedName",
        "microStrategyDossierQualifiedName.text",
    )
    """
    Parent dossier qualified name
    """
    MICRO_STRATEGY_DOSSIER_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyDossierName",
        "microStrategyDossierName.keyword",
        "microStrategyDossierName",
    )
    """
    Parent dossier name
    """

    MICRO_STRATEGY_DOSSIER: ClassVar[RelationField] = RelationField(
        "microStrategyDossier"
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

    _convenience_properties: ClassVar[list[str]] = [
        "micro_strategy_visualization_type",
        "micro_strategy_dossier_qualified_name",
        "micro_strategy_dossier_name",
        "micro_strategy_dossier",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_visualization_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_visualization_type
        )

    @micro_strategy_visualization_type.setter
    def micro_strategy_visualization_type(
        self, micro_strategy_visualization_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_visualization_type = (
            micro_strategy_visualization_type
        )

    @property
    def micro_strategy_dossier_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_dossier_qualified_name
        )

    @micro_strategy_dossier_qualified_name.setter
    def micro_strategy_dossier_qualified_name(
        self, micro_strategy_dossier_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier_qualified_name = (
            micro_strategy_dossier_qualified_name
        )

    @property
    def micro_strategy_dossier_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_dossier_name
        )

    @micro_strategy_dossier_name.setter
    def micro_strategy_dossier_name(self, micro_strategy_dossier_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier_name = micro_strategy_dossier_name

    @property
    def micro_strategy_dossier(self) -> Optional[MicroStrategyDossier]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_dossier
        )

    @micro_strategy_dossier.setter
    def micro_strategy_dossier(
        self, micro_strategy_dossier: Optional[MicroStrategyDossier]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier = micro_strategy_dossier

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
        micro_strategy_visualization_type: Optional[str] = Field(
            None, description="", alias="microStrategyVisualizationType"
        )
        micro_strategy_dossier_qualified_name: Optional[str] = Field(
            None, description="", alias="microStrategyDossierQualifiedName"
        )
        micro_strategy_dossier_name: Optional[str] = Field(
            None, description="", alias="microStrategyDossierName"
        )
        micro_strategy_dossier: Optional[MicroStrategyDossier] = Field(
            None, description="", alias="microStrategyDossier"
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            None, description="", alias="microStrategyProject"
        )  # relationship

    attributes: "MicroStrategyVisualization.Attributes" = Field(
        default_factory=lambda: MicroStrategyVisualization.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


MicroStrategyReport.Attributes.update_forward_refs()


MicroStrategyProject.Attributes.update_forward_refs()


MicroStrategyMetric.Attributes.update_forward_refs()


MicroStrategyCube.Attributes.update_forward_refs()


MicroStrategyDossier.Attributes.update_forward_refs()


MicroStrategyFact.Attributes.update_forward_refs()


MicroStrategyDocument.Attributes.update_forward_refs()


MicroStrategyAttribute.Attributes.update_forward_refs()


MicroStrategyVisualization.Attributes.update_forward_refs()
