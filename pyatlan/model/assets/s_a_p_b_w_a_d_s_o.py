# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p_b_w import SAPBW


class SAPBWADSO(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWADSO", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWADSO":
            raise ValueError("must be SAPBWADSO")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWADSO._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_PLANNING_MODE: ClassVar[KeywordField] = KeywordField(
        "sapBwPlanningMode", "sapBwPlanningMode"
    )
    """
    Whether this ADSO supports planning or write-back (RSOADSO.PLANNING_MODE).
    """
    SAP_BW_DIRECT_UPDATE: ClassVar[KeywordField] = KeywordField(
        "sapBwDirectUpdate", "sapBwDirectUpdate"
    )
    """
    Subtype indicator (RSOADSO.DIRECT_UPDATE) for direct update versus standard storage.
    """

    SAP_BW_ADSO_FIELDS: ClassVar[RelationField] = RelationField("sapBwAdsoFields")
    """
    TBC
    """
    SAP_BW_MEMBER_OF_COMPOSITE_PROVIDERS: ClassVar[RelationField] = RelationField(
        "sapBwMemberOfCompositeProviders"
    )
    """
    TBC
    """
    SAP_BW_INFO_AREA: ClassVar[RelationField] = RelationField("sapBwInfoArea")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_planning_mode",
        "sap_bw_direct_update",
        "sap_bw_adso_fields",
        "sap_bw_member_of_composite_providers",
        "sap_bw_info_area",
    ]

    @property
    def sap_bw_planning_mode(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_planning_mode

    @sap_bw_planning_mode.setter
    def sap_bw_planning_mode(self, sap_bw_planning_mode: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_planning_mode = sap_bw_planning_mode

    @property
    def sap_bw_direct_update(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_bw_direct_update

    @sap_bw_direct_update.setter
    def sap_bw_direct_update(self, sap_bw_direct_update: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_direct_update = sap_bw_direct_update

    @property
    def sap_bw_adso_fields(self) -> Optional[List[SAPBWADSOField]]:
        return None if self.attributes is None else self.attributes.sap_bw_adso_fields

    @sap_bw_adso_fields.setter
    def sap_bw_adso_fields(self, sap_bw_adso_fields: Optional[List[SAPBWADSOField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_adso_fields = sap_bw_adso_fields

    @property
    def sap_bw_member_of_composite_providers(
        self,
    ) -> Optional[List[SAPBWCompositeProvider]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_member_of_composite_providers
        )

    @sap_bw_member_of_composite_providers.setter
    def sap_bw_member_of_composite_providers(
        self,
        sap_bw_member_of_composite_providers: Optional[List[SAPBWCompositeProvider]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_member_of_composite_providers = (
            sap_bw_member_of_composite_providers
        )

    @property
    def sap_bw_info_area(self) -> Optional[SAPBWInfoArea]:
        return None if self.attributes is None else self.attributes.sap_bw_info_area

    @sap_bw_info_area.setter
    def sap_bw_info_area(self, sap_bw_info_area: Optional[SAPBWInfoArea]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_area = sap_bw_info_area

    class Attributes(SAPBW.Attributes):
        sap_bw_planning_mode: Optional[str] = Field(default=None, description="")
        sap_bw_direct_update: Optional[str] = Field(default=None, description="")
        sap_bw_adso_fields: Optional[List[SAPBWADSOField]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_member_of_composite_providers: Optional[List[SAPBWCompositeProvider]] = (
            Field(default=None, description="")
        )  # relationship
        sap_bw_info_area: Optional[SAPBWInfoArea] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWADSO.Attributes = Field(
        default_factory=lambda: SAPBWADSO.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_a_d_s_o_field import SAPBWADSOField  # noqa: E402, F401
from .s_a_p_b_w_composite_provider import SAPBWCompositeProvider  # noqa: E402, F401
from .s_a_p_b_w_info_area import SAPBWInfoArea  # noqa: E402, F401

SAPBWADSO.Attributes.update_forward_refs()
