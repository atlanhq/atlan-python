# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .micro_strategy import MicroStrategy


class MicroStrategyProject(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyProject", allow_mutation=False)

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

    _convenience_properties: ClassVar[List[str]] = [
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
    def micro_strategy_visualizations(
        self,
    ) -> Optional[List[MicroStrategyVisualization]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_visualizations
        )

    @micro_strategy_visualizations.setter
    def micro_strategy_visualizations(
        self, micro_strategy_visualizations: Optional[List[MicroStrategyVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_visualizations = micro_strategy_visualizations

    @property
    def micro_strategy_documents(self) -> Optional[List[MicroStrategyDocument]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_documents
        )

    @micro_strategy_documents.setter
    def micro_strategy_documents(
        self, micro_strategy_documents: Optional[List[MicroStrategyDocument]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_documents = micro_strategy_documents

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
    def micro_strategy_dossiers(self) -> Optional[List[MicroStrategyDossier]]:
        return (
            None if self.attributes is None else self.attributes.micro_strategy_dossiers
        )

    @micro_strategy_dossiers.setter
    def micro_strategy_dossiers(
        self, micro_strategy_dossiers: Optional[List[MicroStrategyDossier]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossiers = micro_strategy_dossiers

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
        micro_strategy_reports: Optional[List[MicroStrategyReport]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_facts: Optional[List[MicroStrategyFact]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_metrics: Optional[List[MicroStrategyMetric]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_visualizations: Optional[List[MicroStrategyVisualization]] = (
            Field(default=None, description="")
        )  # relationship
        micro_strategy_documents: Optional[List[MicroStrategyDocument]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_cubes: Optional[List[MicroStrategyCube]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_dossiers: Optional[List[MicroStrategyDossier]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_attributes: Optional[List[MicroStrategyAttribute]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyProject.Attributes = Field(
        default_factory=lambda: MicroStrategyProject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_attribute import MicroStrategyAttribute  # noqa
from .micro_strategy_cube import MicroStrategyCube  # noqa
from .micro_strategy_document import MicroStrategyDocument  # noqa
from .micro_strategy_dossier import MicroStrategyDossier  # noqa
from .micro_strategy_fact import MicroStrategyFact  # noqa
from .micro_strategy_metric import MicroStrategyMetric  # noqa
from .micro_strategy_report import MicroStrategyReport  # noqa
from .micro_strategy_visualization import MicroStrategyVisualization  # noqa
