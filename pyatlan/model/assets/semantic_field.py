# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.semantic import Semantic


class SemanticField(Semantic):
    """Description"""

    type_name: str = Field(default="SemanticField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SemanticField":
            raise ValueError("must be SemanticField")
        return v

    def __setattr__(self, name, value):
        if name in SemanticField._convenience_properties:
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

    _convenience_properties: ClassVar[List[str]] = [
        "semantic_expression",
        "semantic_type",
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

    class Attributes(Semantic.Attributes):
        semantic_expression: Optional[str] = Field(default=None, description="")
        semantic_type: Optional[str] = Field(default=None, description="")

    attributes: SemanticField.Attributes = Field(
        default_factory=lambda: SemanticField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


SemanticField.Attributes.update_forward_refs()
