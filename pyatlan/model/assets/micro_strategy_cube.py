# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .micro_strategy import MicroStrategy


class MicroStrategyCube(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyCube", allow_mutation=False)

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
    Type of cube, for example: OLAP or MTDI.
    """
    MICRO_STRATEGY_CUBE_QUERY: ClassVar[KeywordField] = KeywordField(
        "microStrategyCubeQuery", "microStrategyCubeQuery"
    )
    """
    Query used to create the cube.
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

    _convenience_properties: ClassVar[List[str]] = [
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
        micro_strategy_cube_type: Optional[str] = Field(default=None, description="")
        micro_strategy_cube_query: Optional[str] = Field(default=None, description="")
        micro_strategy_metrics: Optional[List[MicroStrategyMetric]] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_attributes: Optional[List[MicroStrategyAttribute]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyCube.Attributes = Field(
        default_factory=lambda: MicroStrategyCube.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_attribute import MicroStrategyAttribute  # noqa
from .micro_strategy_metric import MicroStrategyMetric  # noqa
from .micro_strategy_project import MicroStrategyProject  # noqa
