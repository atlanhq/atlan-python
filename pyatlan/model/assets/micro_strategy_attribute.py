# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .micro_strategy import MicroStrategy


class MicroStrategyAttribute(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyAttribute", allow_mutation=False)

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
    JSON string specifying the attribute's name, description, displayFormat, etc.
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

    _convenience_properties: ClassVar[List[str]] = [
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
            default=None, description=""
        )
        micro_strategy_reports: Optional[List[MicroStrategyReport]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_metrics: Optional[List[MicroStrategyMetric]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_cubes: Optional[List[MicroStrategyCube]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyAttribute.Attributes = Field(
        default_factory=lambda: MicroStrategyAttribute.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_cube import MicroStrategyCube  # noqa
from .micro_strategy_metric import MicroStrategyMetric  # noqa
from .micro_strategy_project import MicroStrategyProject  # noqa
from .micro_strategy_report import MicroStrategyReport  # noqa
