# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, RelationField

from .s_a_p_b_w import SAPBW


class SAPBWInfoSourceField(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWInfoSourceField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWInfoSourceField":
            raise ValueError("must be SAPBWInfoSourceField")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWInfoSourceField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_IS_KEY_FIELD: ClassVar[BooleanField] = BooleanField(
        "sapBwIsKeyField", "sapBwIsKeyField"
    )
    """
    Whether this field is a key field (RSKSFIELDNEW.KEYFLAG).
    """

    SAP_BW_INFO_SOURCE: ClassVar[RelationField] = RelationField("sapBwInfoSource")
    """
    TBC
    """
    SAP_BW_INFO_OBJECTS: ClassVar[RelationField] = RelationField("sapBwInfoObjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_is_key_field",
        "sap_bw_info_source",
        "sap_bw_info_objects",
    ]

    @property
    def sap_bw_is_key_field(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.sap_bw_is_key_field

    @sap_bw_is_key_field.setter
    def sap_bw_is_key_field(self, sap_bw_is_key_field: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_is_key_field = sap_bw_is_key_field

    @property
    def sap_bw_info_source(self) -> Optional[SAPBWInfoSource]:
        return None if self.attributes is None else self.attributes.sap_bw_info_source

    @sap_bw_info_source.setter
    def sap_bw_info_source(self, sap_bw_info_source: Optional[SAPBWInfoSource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_source = sap_bw_info_source

    @property
    def sap_bw_info_objects(self) -> Optional[List[SAPBWInfoObject]]:
        return None if self.attributes is None else self.attributes.sap_bw_info_objects

    @sap_bw_info_objects.setter
    def sap_bw_info_objects(self, sap_bw_info_objects: Optional[List[SAPBWInfoObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_objects = sap_bw_info_objects

    class Attributes(SAPBW.Attributes):
        sap_bw_is_key_field: Optional[bool] = Field(default=None, description="")
        sap_bw_info_source: Optional[SAPBWInfoSource] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_objects: Optional[List[SAPBWInfoObject]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWInfoSourceField.Attributes = Field(
        default_factory=lambda: SAPBWInfoSourceField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_info_object import SAPBWInfoObject  # noqa: E402, F401
from .s_a_p_b_w_info_source import SAPBWInfoSource  # noqa: E402, F401

SAPBWInfoSourceField.Attributes.update_forward_refs()
