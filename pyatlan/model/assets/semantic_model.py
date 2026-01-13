# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .core.semantic import Semantic


class SemanticModel(Semantic):
    """Description"""

    type_name: str = Field(default="SemanticModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SemanticModel":
            raise ValueError("must be SemanticModel")
        return v

    def __setattr__(self, name, value):
        if name in SemanticModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SEMANTIC_ENTITIES: ClassVar[RelationField] = RelationField("semanticEntities")
    """
    TBC
    """
    SEMANTIC_MEASURES: ClassVar[RelationField] = RelationField("semanticMeasures")
    """
    TBC
    """
    SEMANTIC_DIMENSIONS: ClassVar[RelationField] = RelationField("semanticDimensions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "semantic_entities",
        "semantic_measures",
        "semantic_dimensions",
    ]

    @property
    def semantic_entities(self) -> Optional[List[SemanticEntity]]:
        return None if self.attributes is None else self.attributes.semantic_entities

    @semantic_entities.setter
    def semantic_entities(self, semantic_entities: Optional[List[SemanticEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_entities = semantic_entities

    @property
    def semantic_measures(self) -> Optional[List[SemanticMeasure]]:
        return None if self.attributes is None else self.attributes.semantic_measures

    @semantic_measures.setter
    def semantic_measures(self, semantic_measures: Optional[List[SemanticMeasure]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_measures = semantic_measures

    @property
    def semantic_dimensions(self) -> Optional[List[SemanticDimension]]:
        return None if self.attributes is None else self.attributes.semantic_dimensions

    @semantic_dimensions.setter
    def semantic_dimensions(
        self, semantic_dimensions: Optional[List[SemanticDimension]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_dimensions = semantic_dimensions

    class Attributes(Semantic.Attributes):
        semantic_entities: Optional[List[SemanticEntity]] = Field(
            default=None, description=""
        )  # relationship
        semantic_measures: Optional[List[SemanticMeasure]] = Field(
            default=None, description=""
        )  # relationship
        semantic_dimensions: Optional[List[SemanticDimension]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SemanticModel.Attributes = Field(
        default_factory=lambda: SemanticModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .semantic_dimension import SemanticDimension  # noqa: E402, F401
from .semantic_entity import SemanticEntity  # noqa: E402, F401
from .semantic_measure import SemanticMeasure  # noqa: E402, F401

SemanticModel.Attributes.update_forward_refs()
