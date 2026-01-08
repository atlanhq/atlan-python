# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .core.semantic import Semantic


class SemanticMeasure(Semantic):
    """Description"""

    type_name: str = Field(default="SemanticMeasure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SemanticMeasure":
            raise ValueError("must be SemanticMeasure")
        return v

    def __setattr__(self, name, value):
        if name in SemanticMeasure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SEMANTIC_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "semanticExpression", "semanticExpression"
    )
    """
    Column name or SQL expression for the semantic field.
    """
    SEMANTIC_TYPE: ClassVar[KeywordField] = KeywordField("semanticType", "semanticType")
    """
    Detailed type of the semantic field (e.g., type of measure, type of dimension, or type of entity).
    """

    SEMANTIC_MODEL: ClassVar[RelationField] = RelationField("semanticModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "semantic_expression",
        "semantic_type",
        "semantic_model",
    ]

    @property
    def semantic_expression(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.semantic_expression

    @semantic_expression.setter
    def semantic_expression(self, semantic_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_expression = semantic_expression

    @property
    def semantic_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.semantic_type

    @semantic_type.setter
    def semantic_type(self, semantic_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_type = semantic_type

    @property
    def semantic_model(self) -> Optional[SemanticModel]:
        return None if self.attributes is None else self.attributes.semantic_model

    @semantic_model.setter
    def semantic_model(self, semantic_model: Optional[SemanticModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.semantic_model = semantic_model

    class Attributes(Semantic.Attributes):
        semantic_expression: Optional[str] = Field(default=None, description="")
        semantic_type: Optional[str] = Field(default=None, description="")
        semantic_model: Optional[SemanticModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: SemanticMeasure.Attributes = Field(
        default_factory=lambda: SemanticMeasure.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .semantic_model import SemanticModel  # noqa: E402, F401

SemanticMeasure.Attributes.update_forward_refs()
