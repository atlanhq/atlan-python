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

    DM_IS_NULLABLE: ClassVar[BooleanField] = BooleanField(
        "dmIsNullable", "dmIsNullable"
    )
    """
    When true, the values in this attribute can be null.
    """
    DM_IS_PRIMARY: ClassVar[BooleanField] = BooleanField("dmIsPrimary", "dmIsPrimary")
    """
    When true, this attribute forms the primary key for the entity.
    """
    DM_IS_FOREIGN: ClassVar[BooleanField] = BooleanField("dmIsForeign", "dmIsForeign")
    """
    When true, this attribute is a foreign key to another entity.
    """
    DM_IS_DERIVED: ClassVar[BooleanField] = BooleanField("dmIsDerived", "dmIsDerived")
    """
    When true, the values in this attribute are derived data.
    """
    DM_PRECISION: ClassVar[NumericField] = NumericField("dmPrecision", "dmPrecision")
    """
    Precision of the attribute.
    """
    DM_SCALE: ClassVar[NumericField] = NumericField("dmScale", "dmScale")
    """
    Scale of the attribute.
    """
    DM_DATA_TYPE: ClassVar[KeywordField] = KeywordField("dmDataType", "dmDataType")
    """
    Type of the attribute.
    """

    DM_ENTITIES: ClassVar[RelationField] = RelationField("dmEntities")
    """
    TBC
    """
    DM_RELATED_FROM_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dmRelatedFromAttributes"
    )
    """
    TBC
    """
    DM_MAPPED_TO_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dmMappedToAttributes"
    )
    """
    TBC
    """
    DM_RELATED_TO_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dmRelatedToAttributes"
    )
    """
    TBC
    """
    DM_MAPPED_FROM_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "dmMappedFromAttributes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dm_is_nullable",
        "dm_is_primary",
        "dm_is_foreign",
        "dm_is_derived",
        "dm_precision",
        "dm_scale",
        "dm_data_type",
        "dm_entities",
        "dm_related_from_attributes",
        "dm_mapped_to_attributes",
        "dm_related_to_attributes",
        "dm_mapped_from_attributes",
    ]

    @property
    def dm_is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.dm_is_nullable

    @dm_is_nullable.setter
    def dm_is_nullable(self, dm_is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_is_nullable = dm_is_nullable

    @property
    def dm_is_primary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.dm_is_primary

    @dm_is_primary.setter
    def dm_is_primary(self, dm_is_primary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_is_primary = dm_is_primary

    @property
    def dm_is_foreign(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.dm_is_foreign

    @dm_is_foreign.setter
    def dm_is_foreign(self, dm_is_foreign: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_is_foreign = dm_is_foreign

    @property
    def dm_is_derived(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.dm_is_derived

    @dm_is_derived.setter
    def dm_is_derived(self, dm_is_derived: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_is_derived = dm_is_derived

    @property
    def dm_precision(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dm_precision

    @dm_precision.setter
    def dm_precision(self, dm_precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_precision = dm_precision

    @property
    def dm_scale(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dm_scale

    @dm_scale.setter
    def dm_scale(self, dm_scale: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_scale = dm_scale

    @property
    def dm_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_data_type

    @dm_data_type.setter
    def dm_data_type(self, dm_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_data_type = dm_data_type

    @property
    def dm_entities(self) -> Optional[List[DMEntity]]:
        return None if self.attributes is None else self.attributes.dm_entities

    @dm_entities.setter
    def dm_entities(self, dm_entities: Optional[List[DMEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entities = dm_entities

    @property
    def dm_related_from_attributes(self) -> Optional[List[DMAttributeAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_related_from_attributes
        )

    @dm_related_from_attributes.setter
    def dm_related_from_attributes(
        self, dm_related_from_attributes: Optional[List[DMAttributeAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_related_from_attributes = dm_related_from_attributes

    @property
    def dm_mapped_to_attributes(self) -> Optional[List[DMAttribute]]:
        return (
            None if self.attributes is None else self.attributes.dm_mapped_to_attributes
        )

    @dm_mapped_to_attributes.setter
    def dm_mapped_to_attributes(
        self, dm_mapped_to_attributes: Optional[List[DMAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_mapped_to_attributes = dm_mapped_to_attributes

    @property
    def dm_related_to_attributes(self) -> Optional[List[DMAttributeAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_related_to_attributes
        )

    @dm_related_to_attributes.setter
    def dm_related_to_attributes(
        self, dm_related_to_attributes: Optional[List[DMAttributeAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_related_to_attributes = dm_related_to_attributes

    @property
    def dm_mapped_from_attributes(self) -> Optional[List[DMAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_mapped_from_attributes
        )

    @dm_mapped_from_attributes.setter
    def dm_mapped_from_attributes(
        self, dm_mapped_from_attributes: Optional[List[DMAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_mapped_from_attributes = dm_mapped_from_attributes

    class Attributes(DM.Attributes):
        dm_is_nullable: Optional[bool] = Field(default=None, description="")
        dm_is_primary: Optional[bool] = Field(default=None, description="")
        dm_is_foreign: Optional[bool] = Field(default=None, description="")
        dm_is_derived: Optional[bool] = Field(default=None, description="")
        dm_precision: Optional[int] = Field(default=None, description="")
        dm_scale: Optional[int] = Field(default=None, description="")
        dm_data_type: Optional[str] = Field(default=None, description="")
        dm_entities: Optional[List[DMEntity]] = Field(
            default=None, description=""
        )  # relationship
        dm_related_from_attributes: Optional[List[DMAttributeAssociation]] = Field(
            default=None, description=""
        )  # relationship
        dm_mapped_to_attributes: Optional[List[DMAttribute]] = Field(
            default=None, description=""
        )  # relationship
        dm_related_to_attributes: Optional[List[DMAttributeAssociation]] = Field(
            default=None, description=""
        )  # relationship
        dm_mapped_from_attributes: Optional[List[DMAttribute]] = Field(
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
