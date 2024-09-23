# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import ModelCardinalityType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .model import Model


class ModelAttributeAssociation(Model):
    """Description"""

    type_name: str = Field(default="ModelAttributeAssociation", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModelAttributeAssociation":
            raise ValueError("must be ModelAttributeAssociation")
        return v

    def __setattr__(self, name, value):
        if name in ModelAttributeAssociation._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODEL_ATTRIBUTE_ASSOCIATION_CARDINALITY: ClassVar[KeywordField] = KeywordField(
        "modelAttributeAssociationCardinality", "modelAttributeAssociationCardinality"
    )
    """
    Cardinality of the data attribute association.
    """
    MODEL_ATTRIBUTE_ASSOCIATION_LABEL: ClassVar[KeywordField] = KeywordField(
        "modelAttributeAssociationLabel", "modelAttributeAssociationLabel"
    )
    """
    Label of the data attribute association.
    """
    MODEL_ATTRIBUTE_ASSOCIATION_TO_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "modelAttributeAssociationToQualifiedName",
            "modelAttributeAssociationToQualifiedName",
        )
    )
    """
    Unique name of the association to which this attribute is related.
    """
    MODEL_ATTRIBUTE_ASSOCIATION_FROM_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "modelAttributeAssociationFromQualifiedName",
            "modelAttributeAssociationFromQualifiedName",
        )
    )
    """
    Unique name of the association from which this attribute is related.
    """

    MODEL_ATTRIBUTE_ASSOCIATION_FROM: ClassVar[RelationField] = RelationField(
        "modelAttributeAssociationFrom"
    )
    """
    TBC
    """
    MODEL_ATTRIBUTE_ASSOCIATION_TO: ClassVar[RelationField] = RelationField(
        "modelAttributeAssociationTo"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "model_attribute_association_cardinality",
        "model_attribute_association_label",
        "model_attribute_association_to_qualified_name",
        "model_attribute_association_from_qualified_name",
        "model_attribute_association_from",
        "model_attribute_association_to",
    ]

    @property
    def model_attribute_association_cardinality(self) -> Optional[ModelCardinalityType]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_association_cardinality
        )

    @model_attribute_association_cardinality.setter
    def model_attribute_association_cardinality(
        self, model_attribute_association_cardinality: Optional[ModelCardinalityType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_association_cardinality = (
            model_attribute_association_cardinality
        )

    @property
    def model_attribute_association_label(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_association_label
        )

    @model_attribute_association_label.setter
    def model_attribute_association_label(
        self, model_attribute_association_label: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_association_label = (
            model_attribute_association_label
        )

    @property
    def model_attribute_association_to_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_association_to_qualified_name
        )

    @model_attribute_association_to_qualified_name.setter
    def model_attribute_association_to_qualified_name(
        self, model_attribute_association_to_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_association_to_qualified_name = (
            model_attribute_association_to_qualified_name
        )

    @property
    def model_attribute_association_from_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_association_from_qualified_name
        )

    @model_attribute_association_from_qualified_name.setter
    def model_attribute_association_from_qualified_name(
        self, model_attribute_association_from_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_association_from_qualified_name = (
            model_attribute_association_from_qualified_name
        )

    @property
    def model_attribute_association_from(self) -> Optional[ModelAttribute]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_association_from
        )

    @model_attribute_association_from.setter
    def model_attribute_association_from(
        self, model_attribute_association_from: Optional[ModelAttribute]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_association_from = (
            model_attribute_association_from
        )

    @property
    def model_attribute_association_to(self) -> Optional[ModelAttribute]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_attribute_association_to
        )

    @model_attribute_association_to.setter
    def model_attribute_association_to(
        self, model_attribute_association_to: Optional[ModelAttribute]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_attribute_association_to = model_attribute_association_to

    class Attributes(Model.Attributes):
        model_attribute_association_cardinality: Optional[ModelCardinalityType] = Field(
            default=None, description=""
        )
        model_attribute_association_label: Optional[str] = Field(
            default=None, description=""
        )
        model_attribute_association_to_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        model_attribute_association_from_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        model_attribute_association_from: Optional[ModelAttribute] = Field(
            default=None, description=""
        )  # relationship
        model_attribute_association_to: Optional[ModelAttribute] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModelAttributeAssociation.Attributes = Field(
        default_factory=lambda: ModelAttributeAssociation.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .model_attribute import ModelAttribute  # noqa

ModelAttributeAssociation.Attributes.update_forward_refs()
