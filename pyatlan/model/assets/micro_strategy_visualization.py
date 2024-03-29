# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .micro_strategy import MicroStrategy


class MicroStrategyVisualization(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyVisualization", allow_mutation=False)

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
    Type of visualization.
    """
    MICRO_STRATEGY_DOSSIER_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "microStrategyDossierQualifiedName",
            "microStrategyDossierQualifiedName",
            "microStrategyDossierQualifiedName.text",
        )
    )
    """
    Unique name of the dossier in which this visualization exists.
    """
    MICRO_STRATEGY_DOSSIER_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "microStrategyDossierName",
        "microStrategyDossierName.keyword",
        "microStrategyDossierName",
    )
    """
    Simple name of the dossier in which this visualization exists.
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

    _convenience_properties: ClassVar[List[str]] = [
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
            default=None, description=""
        )
        micro_strategy_dossier_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        micro_strategy_dossier_name: Optional[str] = Field(default=None, description="")
        micro_strategy_dossier: Optional[MicroStrategyDossier] = Field(
            default=None, description=""
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyVisualization.Attributes = Field(
        default_factory=lambda: MicroStrategyVisualization.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_dossier import MicroStrategyDossier  # noqa
from .micro_strategy_project import MicroStrategyProject  # noqa
