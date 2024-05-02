# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .micro_strategy import MicroStrategy


class MicroStrategyDossier(MicroStrategy):
    """Description"""

    type_name: str = Field(default="MicroStrategyDossier", allow_mutation=False)

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
    List of chapter names in this dossier.
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

    _convenience_properties: ClassVar[List[str]] = [
        "micro_strategy_dossier_chapter_names",
        "micro_strategy_visualizations",
        "micro_strategy_project",
    ]

    @property
    def micro_strategy_dossier_chapter_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.micro_strategy_dossier_chapter_names
        )

    @micro_strategy_dossier_chapter_names.setter
    def micro_strategy_dossier_chapter_names(
        self, micro_strategy_dossier_chapter_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.micro_strategy_dossier_chapter_names = (
            micro_strategy_dossier_chapter_names
        )

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
        micro_strategy_dossier_chapter_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        micro_strategy_visualizations: Optional[List[MicroStrategyVisualization]] = (
            Field(default=None, description="")
        )  # relationship
        micro_strategy_project: Optional[MicroStrategyProject] = Field(
            default=None, description=""
        )  # relationship

    attributes: MicroStrategyDossier.Attributes = Field(
        default_factory=lambda: MicroStrategyDossier.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .micro_strategy_project import MicroStrategyProject  # noqa
from .micro_strategy_visualization import MicroStrategyVisualization  # noqa
