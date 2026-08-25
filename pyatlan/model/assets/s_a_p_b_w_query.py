# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p_b_w import SAPBW


class SAPBWQuery(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWQuery":
            raise ValueError("must be SAPBWQuery")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWQuery._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_QUERY_UID: ClassVar[KeywordField] = KeywordField(
        "sapBwQueryUid", "sapBwQueryUid"
    )
    """
    Internal stable UID of the query (RSZCOMPDIR.COMPUID). This is the join key inside SAP BW and is the preferred identifier for qualifiedName.
    """  # noqa: E501

    SAP_BW_QUERY_ELEMENTS: ClassVar[RelationField] = RelationField("sapBwQueryElements")
    """
    TBC
    """
    SAP_BW_INFO_AREA: ClassVar[RelationField] = RelationField("sapBwInfoArea")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_query_uid",
        "sap_bw_query_elements",
        "sap_bw_info_area",
    ]

    @property
    def sap_bw_query_uid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_query_uid

    @sap_bw_query_uid.setter
    def sap_bw_query_uid(self, sap_bw_query_uid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_query_uid = sap_bw_query_uid

    @property
    def sap_bw_query_elements(self) -> Optional[List[SAPBWQueryElement]]:
        return (
            None if self.attributes is None else self.attributes.sap_bw_query_elements
        )

    @sap_bw_query_elements.setter
    def sap_bw_query_elements(
        self, sap_bw_query_elements: Optional[List[SAPBWQueryElement]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_query_elements = sap_bw_query_elements

    @property
    def sap_bw_info_area(self) -> Optional[SAPBWInfoArea]:
        return None if self.attributes is None else self.attributes.sap_bw_info_area

    @sap_bw_info_area.setter
    def sap_bw_info_area(self, sap_bw_info_area: Optional[SAPBWInfoArea]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_area = sap_bw_info_area

    class Attributes(SAPBW.Attributes):
        sap_bw_query_uid: Optional[str] = Field(default=None, description="")
        sap_bw_query_elements: Optional[List[SAPBWQueryElement]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_area: Optional[SAPBWInfoArea] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWQuery.Attributes = Field(
        default_factory=lambda: SAPBWQuery.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_info_area import SAPBWInfoArea  # noqa: E402, F401
from .s_a_p_b_w_query_element import SAPBWQueryElement  # noqa: E402, F401

SAPBWQuery.Attributes.update_forward_refs()
