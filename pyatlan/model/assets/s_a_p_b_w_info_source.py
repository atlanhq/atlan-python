# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .s_a_p_b_w import SAPBW


class SAPBWInfoSource(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWInfoSource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWInfoSource":
            raise ValueError("must be SAPBWInfoSource")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWInfoSource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_INFO_SOURCE_FIELDS: ClassVar[RelationField] = RelationField(
        "sapBwInfoSourceFields"
    )
    """
    TBC
    """
    SAP_BW_INFO_AREA: ClassVar[RelationField] = RelationField("sapBwInfoArea")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_info_source_fields",
        "sap_bw_info_area",
    ]

    @property
    def sap_bw_info_source_fields(self) -> Optional[List[SAPBWInfoSourceField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_info_source_fields
        )

    @sap_bw_info_source_fields.setter
    def sap_bw_info_source_fields(
        self, sap_bw_info_source_fields: Optional[List[SAPBWInfoSourceField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_source_fields = sap_bw_info_source_fields

    @property
    def sap_bw_info_area(self) -> Optional[SAPBWInfoArea]:
        return None if self.attributes is None else self.attributes.sap_bw_info_area

    @sap_bw_info_area.setter
    def sap_bw_info_area(self, sap_bw_info_area: Optional[SAPBWInfoArea]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_area = sap_bw_info_area

    class Attributes(SAPBW.Attributes):
        sap_bw_info_source_fields: Optional[List[SAPBWInfoSourceField]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_area: Optional[SAPBWInfoArea] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWInfoSource.Attributes = Field(
        default_factory=lambda: SAPBWInfoSource.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_info_area import SAPBWInfoArea  # noqa: E402, F401
from .s_a_p_b_w_info_source_field import SAPBWInfoSourceField  # noqa: E402, F401

SAPBWInfoSource.Attributes.update_forward_refs()
