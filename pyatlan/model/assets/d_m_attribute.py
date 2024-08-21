# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, NumericField, RelationField

from .d_m import DM


class DMAttribute(DM):
    """Description"""

    type_name: str = Field(default="DMAttribute", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DMAttribute":
            raise ValueError("must be DMAttribute")
        return v

    def __setattr__(self, name, value):
        if name in DMAttribute._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    D_M_IS_NULLABLE: ClassVar[BooleanField] = BooleanField(
        "dMIsNullable", "dMIsNullable"
    )
    """
    Whether this attribute is nullable or not.
    """
    D_M_PRIMARY_KEY_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dMPrimaryKeyIndicator", "dMPrimaryKeyIndicator"
    )
    """
    Whether this attribute is primary key indicator or not.
    """
    D_M_FOREIGN_KEY_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dMForeignKeyIndicator", "dMForeignKeyIndicator"
    )
    """
    Whether this attribute is foreign key indicator or not.
    """
    D_M_DERIVED_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dMDerivedIndicator", "dMDerivedIndicator"
    )
    """
    Whether this attribute is derived indicator or not.
    """
    D_M_PRECISION: ClassVar[NumericField] = NumericField("dMPrecision", "dMPrecision")
    """
    Precision of the attribute.
    """
    D_M_SCALE: ClassVar[NumericField] = NumericField("dMScale", "dMScale")
    """
    Scale of the attribute.
    """

    D_M_ENTITY: ClassVar[RelationField] = RelationField("dMEntity")
    """
    TBC
    """
    D_M_RELATED_TO_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dMRelatedToAttributes"
    )
    """
    TBC
    """
    D_M_MAPPED_TO_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dMMappedToAttributes"
    )
    """
    TBC
    """
    D_M_MAPPED_FROM_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dMMappedFromAttributes"
    )
    """
    TBC
    """
    D_M_RELATED_FROM_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dMRelatedFromAttributes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "d_m_is_nullable",
        "d_m_primary_key_indicator",
        "d_m_foreign_key_indicator",
        "d_m_derived_indicator",
        "d_m_precision",
        "d_m_scale",
        "d_m_entity",
        "d_m_related_to_attributes",
        "d_m_mapped_to_attributes",
        "d_m_mapped_from_attributes",
        "d_m_related_from_attributes",
    ]

    @property
    def d_m_is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.d_m_is_nullable

    @d_m_is_nullable.setter
    def d_m_is_nullable(self, d_m_is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_is_nullable = d_m_is_nullable

    @property
    def d_m_primary_key_indicator(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_primary_key_indicator
        )

    @d_m_primary_key_indicator.setter
    def d_m_primary_key_indicator(self, d_m_primary_key_indicator: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_primary_key_indicator = d_m_primary_key_indicator

    @property
    def d_m_foreign_key_indicator(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_foreign_key_indicator
        )

    @d_m_foreign_key_indicator.setter
    def d_m_foreign_key_indicator(self, d_m_foreign_key_indicator: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_foreign_key_indicator = d_m_foreign_key_indicator

    @property
    def d_m_derived_indicator(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.d_m_derived_indicator
        )

    @d_m_derived_indicator.setter
    def d_m_derived_indicator(self, d_m_derived_indicator: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_derived_indicator = d_m_derived_indicator

    @property
    def d_m_precision(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.d_m_precision

    @d_m_precision.setter
    def d_m_precision(self, d_m_precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_precision = d_m_precision

    @property
    def d_m_scale(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.d_m_scale

    @d_m_scale.setter
    def d_m_scale(self, d_m_scale: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_scale = d_m_scale

    @property
    def d_m_entity(self) -> Optional[DMEntity]:
        return None if self.attributes is None else self.attributes.d_m_entity

    @d_m_entity.setter
    def d_m_entity(self, d_m_entity: Optional[DMEntity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entity = d_m_entity

    @property
    def d_m_related_to_attributes(self) -> Optional[List[DMAttributeAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_related_to_attributes
        )

    @d_m_related_to_attributes.setter
    def d_m_related_to_attributes(
        self, d_m_related_to_attributes: Optional[List[DMAttributeAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_related_to_attributes = d_m_related_to_attributes

    @property
    def d_m_mapped_to_attributes(self) -> Optional[List[DMAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_mapped_to_attributes
        )

    @d_m_mapped_to_attributes.setter
    def d_m_mapped_to_attributes(
        self, d_m_mapped_to_attributes: Optional[List[DMAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_mapped_to_attributes = d_m_mapped_to_attributes

    @property
    def d_m_mapped_from_attributes(self) -> Optional[List[DMAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_mapped_from_attributes
        )

    @d_m_mapped_from_attributes.setter
    def d_m_mapped_from_attributes(
        self, d_m_mapped_from_attributes: Optional[List[DMAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_mapped_from_attributes = d_m_mapped_from_attributes

    @property
    def d_m_related_from_attributes(self) -> Optional[List[DMAttributeAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_related_from_attributes
        )

    @d_m_related_from_attributes.setter
    def d_m_related_from_attributes(
        self, d_m_related_from_attributes: Optional[List[DMAttributeAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_related_from_attributes = d_m_related_from_attributes

    class Attributes(DM.Attributes):
        d_m_is_nullable: Optional[bool] = Field(default=None, description="")
        d_m_primary_key_indicator: Optional[bool] = Field(default=None, description="")
        d_m_foreign_key_indicator: Optional[bool] = Field(default=None, description="")
        d_m_derived_indicator: Optional[bool] = Field(default=None, description="")
        d_m_precision: Optional[int] = Field(default=None, description="")
        d_m_scale: Optional[int] = Field(default=None, description="")
        d_m_entity: Optional[DMEntity] = Field(
            default=None, description=""
        )  # relationship
        d_m_related_to_attributes: Optional[List[DMAttributeAssociation]] = Field(
            default=None, description=""
        )  # relationship
        d_m_mapped_to_attributes: Optional[List[DMAttribute]] = Field(
            default=None, description=""
        )  # relationship
        d_m_mapped_from_attributes: Optional[List[DMAttribute]] = Field(
            default=None, description=""
        )  # relationship
        d_m_related_from_attributes: Optional[List[DMAttributeAssociation]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DMAttribute.Attributes = Field(
        default_factory=lambda: DMAttribute.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .d_m_attribute_association import DMAttributeAssociation  # noqa
from .d_m_entity import DMEntity  # noqa

DMAttribute.Attributes.update_forward_refs()
