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

    D_M_CARDINALITY: ClassVar[KeywordField] = KeywordField(
        "dMCardinality", "dMCardinality"
    )
    """
    Cardinality of the data attribute association.
    """
    D_M_LABEL: ClassVar[KeywordField] = KeywordField("dMLabel", "dMLabel")
    """
    Label of the data attribute association.
    """

    D_M_ATTRIBUTE_TO: ClassVar[RelationField] = RelationField("dMAttributeTo")
    """
    TBC
    """
    D_M_ATTRIBUTE_FROM: ClassVar[RelationField] = RelationField("dMAttributeFrom")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "d_m_cardinality",
        "d_m_label",
        "d_m_attribute_to",
        "d_m_attribute_from",
    ]

    @property
    def d_m_cardinality(self) -> Optional[DMCardinalityType]:
        return None if self.attributes is None else self.attributes.d_m_cardinality

    @d_m_cardinality.setter
    def d_m_cardinality(self, d_m_cardinality: Optional[DMCardinalityType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_cardinality = d_m_cardinality

    @property
    def d_m_label(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_label

    @d_m_label.setter
    def d_m_label(self, d_m_label: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_label = d_m_label

    @property
    def d_m_attribute_to(self) -> Optional[DMAttribute]:
        return None if self.attributes is None else self.attributes.d_m_attribute_to

    @d_m_attribute_to.setter
    def d_m_attribute_to(self, d_m_attribute_to: Optional[DMAttribute]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_attribute_to = d_m_attribute_to

    @property
    def d_m_attribute_from(self) -> Optional[DMAttribute]:
        return None if self.attributes is None else self.attributes.d_m_attribute_from

    @d_m_attribute_from.setter
    def d_m_attribute_from(self, d_m_attribute_from: Optional[DMAttribute]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_attribute_from = d_m_attribute_from

    class Attributes(DM.Attributes):
        d_m_cardinality: Optional[DMCardinalityType] = Field(
            default=None, description=""
        )
        d_m_label: Optional[str] = Field(default=None, description="")
        d_m_attribute_to: Optional[DMAttribute] = Field(
            default=None, description=""
        )  # relationship
        d_m_attribute_from: Optional[DMAttribute] = Field(
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
