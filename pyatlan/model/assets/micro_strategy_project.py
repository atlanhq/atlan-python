# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

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
            default=None, description=""
        )  # relationship
        micro_strategy_facts: Optional[list[MicroStrategyFact]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_metrics: Optional[list[MicroStrategyMetric]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_visualizations: Optional[
            list[MicroStrategyVisualization]
        ] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_documents: Optional[list[MicroStrategyDocument]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_cubes: Optional[list[MicroStrategyCube]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_dossiers: Optional[list[MicroStrategyDossier]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_attributes: Optional[list[MicroStrategyAttribute]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "MicroStrategyProject.Attributes" = Field(
        default_factory=lambda: MicroStrategyProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


from .micro_strategy_attribute import MicroStrategyAttribute  # noqa
from .micro_strategy_cube import MicroStrategyCube  # noqa
from .micro_strategy_document import MicroStrategyDocument  # noqa
from .micro_strategy_dossier import MicroStrategyDossier  # noqa
from .micro_strategy_fact import MicroStrategyFact  # noqa
from .micro_strategy_metric import MicroStrategyMetric  # noqa
from .micro_strategy_report import MicroStrategyReport  # noqa
from .micro_strategy_visualization import MicroStrategyVisualization  # noqa
