# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)

from .model import Model


class ModelAttribute(Model):
    """Description"""

    type_name: str = Field(default="ModelAttribute", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModelAttribute":
            raise ValueError("must be ModelAttribute")
        return v

    def __setattr__(self, name, value):
        if name in ModelAttribute._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODEL_ATTRIBUTE_IS_NULLABLE: ClassVar[BooleanField] = BooleanField(
        "modelAttributeIsNullable", "modelAttributeIsNullable"
    )
    """
    When true, the values in this attribute can be null.
    """
    MODEL_ATTRIBUTE_IS_PRIMARY: ClassVar[BooleanField] = BooleanField(
        "modelAttributeIsPrimary", "modelAttributeIsPrimary"
    )
    """
    When true, this attribute forms the primary key for the entity.
    """
    MODEL_ATTRIBUTE_IS_FOREIGN: ClassVar[BooleanField] = BooleanField(
        "modelAttributeIsForeign", "modelAttributeIsForeign"
    )
    """
    When true, this attribute is a foreign key to another entity.
    """
    MODEL_ATTRIBUTE_IS_DERIVED: ClassVar[BooleanField] = BooleanField(
        "modelAttributeIsDerived", "modelAttributeIsDerived"
    )
    """
    When true, the values in this attribute are derived data.
    """
    MODEL_ATTRIBUTE_PRECISION: ClassVar[NumericField] = NumericField(
        "modelAttributePrecision", "modelAttributePrecision"
    )
    """
    Precision of the attribute.
    """
    MODEL_ATTRIBUTE_SCALE: ClassVar[NumericField] = NumericField(
        "modelAttributeScale", "modelAttributeScale"
    )
    """
    Scale of the attribute.
    """
    MODEL_ATTRIBUTE_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "modelAttributeDataType", "modelAttributeDataType"
    )
    """
    Type of the attribute.
    """

    MODEL_ATTRIBUTE_RELATED_TO_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "modelAttributeRelatedToAttributes"
    )
    """
    TBC
    """
    MODEL_ATTRIBUTE_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelAttributeEntities"
    )
    """
    TBC
    """
    MODEL_ATTRIBUTE_RELATED_FROM_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "modelAttributeRelatedFromAttributes"
    )
    """
    TBC
    """
    MODEL_ATTRIBUTE_MAPPED_TO_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "modelAttributeMappedToAttributes"
    )
    """
    TBC
    """
    MODEL_ATTRIBUTE_MAPPED_FROM_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "modelAttributeMappedFromAttributes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "model_attribute_is_nullable",
        "model_attribute_is_primary",
        "model_attribute_is_foreign",
        "model_attribute_is_derived",
        "model_attribute_precision",
        "model_attribute_scale",
        "model_attribute_data_type",
        "model_attribute_related_to_attributes",
        "model_attribute_entities",
        "model_attribute_related_from_attributes",
        "model_attribute_mapped_to_attributes",
        "model_attribute_mapped_from_attributes",
    ]

    @property
    def model_attribute_is_nullable(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_is_nullable
        )

    @model_attribute_is_nullable.setter
    def model_attribute_is_nullable(self, model_attribute_is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_is_nullable = model_attribute_is_nullable

    @property
    def model_attribute_is_primary(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_is_primary
        )

    @model_attribute_is_primary.setter
    def model_attribute_is_primary(self, model_attribute_is_primary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_is_primary = model_attribute_is_primary

    @property
    def model_attribute_is_foreign(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_is_foreign
        )

    @model_attribute_is_foreign.setter
    def model_attribute_is_foreign(self, model_attribute_is_foreign: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_is_foreign = model_attribute_is_foreign

    @property
    def model_attribute_is_derived(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_is_derived
        )

    @model_attribute_is_derived.setter
    def model_attribute_is_derived(self, model_attribute_is_derived: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_is_derived = model_attribute_is_derived

    @property
    def model_attribute_precision(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_precision
        )

    @model_attribute_precision.setter
    def model_attribute_precision(self, model_attribute_precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_precision = model_attribute_precision

    @property
    def model_attribute_scale(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.model_attribute_scale
        )

    @model_attribute_scale.setter
    def model_attribute_scale(self, model_attribute_scale: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_scale = model_attribute_scale

    @property
    def model_attribute_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_data_type
        )

    @model_attribute_data_type.setter
    def model_attribute_data_type(self, model_attribute_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_data_type = model_attribute_data_type

    @property
    def model_attribute_related_to_attributes(
        self,
    ) -> Optional[List[ModelAttributeAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_related_to_attributes
        )

    @model_attribute_related_to_attributes.setter
    def model_attribute_related_to_attributes(
        self,
        model_attribute_related_to_attributes: Optional[
            List[ModelAttributeAssociation]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_related_to_attributes = (
            model_attribute_related_to_attributes
        )

    @property
    def model_attribute_entities(self) -> Optional[List[ModelEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_entities
        )

    @model_attribute_entities.setter
    def model_attribute_entities(
        self, model_attribute_entities: Optional[List[ModelEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_entities = model_attribute_entities

    @property
    def model_attribute_related_from_attributes(
        self,
    ) -> Optional[List[ModelAttributeAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_related_from_attributes
        )

    @model_attribute_related_from_attributes.setter
    def model_attribute_related_from_attributes(
        self,
        model_attribute_related_from_attributes: Optional[
            List[ModelAttributeAssociation]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_related_from_attributes = (
            model_attribute_related_from_attributes
        )

    @property
    def model_attribute_mapped_to_attributes(self) -> Optional[List[ModelAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_mapped_to_attributes
        )

    @model_attribute_mapped_to_attributes.setter
    def model_attribute_mapped_to_attributes(
        self, model_attribute_mapped_to_attributes: Optional[List[ModelAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_mapped_to_attributes = (
            model_attribute_mapped_to_attributes
        )

    @property
    def model_attribute_mapped_from_attributes(self) -> Optional[List[ModelAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_mapped_from_attributes
        )

    @model_attribute_mapped_from_attributes.setter
    def model_attribute_mapped_from_attributes(
        self, model_attribute_mapped_from_attributes: Optional[List[ModelAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_mapped_from_attributes = (
            model_attribute_mapped_from_attributes
        )

    class Attributes(Model.Attributes):
        model_attribute_is_nullable: Optional[bool] = Field(
            default=None, description=""
        )
        model_attribute_is_primary: Optional[bool] = Field(default=None, description="")
        model_attribute_is_foreign: Optional[bool] = Field(default=None, description="")
        model_attribute_is_derived: Optional[bool] = Field(default=None, description="")
        model_attribute_precision: Optional[int] = Field(default=None, description="")
        model_attribute_scale: Optional[int] = Field(default=None, description="")
        model_attribute_data_type: Optional[str] = Field(default=None, description="")
        model_attribute_related_to_attributes: Optional[
            List[ModelAttributeAssociation]
        ] = Field(
            default=None, description=""
        )  # relationship
        model_attribute_entities: Optional[List[ModelEntity]] = Field(
            default=None, description=""
        )  # relationship
        model_attribute_related_from_attributes: Optional[
            List[ModelAttributeAssociation]
        ] = Field(
            default=None, description=""
        )  # relationship
        model_attribute_mapped_to_attributes: Optional[List[ModelAttribute]] = Field(
            default=None, description=""
        )  # relationship
        model_attribute_mapped_from_attributes: Optional[List[ModelAttribute]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModelAttribute.Attributes = Field(
        default_factory=lambda: ModelAttribute.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .model_attribute_association import ModelAttributeAssociation  # noqa
from .model_entity import ModelEntity  # noqa

ModelAttribute.Attributes.update_forward_refs()
