# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DMCardinalityType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .d_m import DM


class DMAttributeAssociation(DM):
    """Description"""

    type_name: str = Field(default="DMAttributeAssociation", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DMAttributeAssociation":
            raise ValueError("must be DMAttributeAssociation")
        return v

    def __setattr__(self, name, value):
        if name in DMAttributeAssociation._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DM_CARDINALITY: ClassVar[KeywordField] = KeywordField(
        "dmCardinality", "dmCardinality"
    )
    """
    Cardinality of the data attribute association.
    """
    DM_LABEL: ClassVar[KeywordField] = KeywordField("dmLabel", "dmLabel")
    """
    Label of the data attribute association.
    """
    DM_ATTRIBUTE_TO_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dmAttributeToQualifiedName", "dmAttributeToQualifiedName"
    )
    """
    Unique name of the association to which this attribute is related.
    """
    DM_ATTRIBUTE_FROM_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dmAttributeFromQualifiedName", "dmAttributeFromQualifiedName"
    )
    """
    Unique name of the association from this attribute is related.
    """

    DM_ATTRIBUTE_FROM: ClassVar[RelationField] = RelationField("dmAttributeFrom")
    """
    TBC
    """
    DM_ATTRIBUTE_TO: ClassVar[RelationField] = RelationField("dmAttributeTo")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dm_cardinality",
        "dm_label",
        "dm_attribute_to_qualified_name",
        "dm_attribute_from_qualified_name",
        "dm_attribute_from",
        "dm_attribute_to",
    ]

    @property
    def dm_cardinality(self) -> Optional[DMCardinalityType]:
        return None if self.attributes is None else self.attributes.dm_cardinality

    @dm_cardinality.setter
    def dm_cardinality(self, dm_cardinality: Optional[DMCardinalityType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_cardinality = dm_cardinality

    @property
    def dm_label(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_label

    @dm_label.setter
    def dm_label(self, dm_label: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_label = dm_label

    @property
    def dm_attribute_to_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_attribute_to_qualified_name
        )

    @dm_attribute_to_qualified_name.setter
    def dm_attribute_to_qualified_name(
        self, dm_attribute_to_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_attribute_to_qualified_name = dm_attribute_to_qualified_name

    @property
    def dm_attribute_from_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_attribute_from_qualified_name
        )

    @dm_attribute_from_qualified_name.setter
    def dm_attribute_from_qualified_name(
        self, dm_attribute_from_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_attribute_from_qualified_name = (
            dm_attribute_from_qualified_name
        )

    @property
    def dm_attribute_from(self) -> Optional[DMAttribute]:
        return None if self.attributes is None else self.attributes.dm_attribute_from

    @dm_attribute_from.setter
    def dm_attribute_from(self, dm_attribute_from: Optional[DMAttribute]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_attribute_from = dm_attribute_from

    @property
    def dm_attribute_to(self) -> Optional[DMAttribute]:
        return None if self.attributes is None else self.attributes.dm_attribute_to

    @dm_attribute_to.setter
    def dm_attribute_to(self, dm_attribute_to: Optional[DMAttribute]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_attribute_to = dm_attribute_to

    class Attributes(DM.Attributes):
        dm_cardinality: Optional[DMCardinalityType] = Field(
            default=None, description=""
        )
        dm_label: Optional[str] = Field(default=None, description="")
        dm_attribute_to_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dm_attribute_from_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dm_attribute_from: Optional[DMAttribute] = Field(
            default=None, description=""
        )  # relationship
        dm_attribute_to: Optional[DMAttribute] = Field(
            default=None, description=""
        )  # relationship

    attributes: DMAttributeAssociation.Attributes = Field(
        default_factory=lambda: DMAttributeAssociation.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .d_m_attribute import DMAttribute  # noqa

DMAttributeAssociation.Attributes.update_forward_refs()
