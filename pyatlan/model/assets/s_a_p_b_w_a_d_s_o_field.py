# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .s_a_p_b_w import SAPBW


class SAPBWADSOField(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWADSOField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWADSOField":
            raise ValueError("must be SAPBWADSOField")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWADSOField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_ADSO: ClassVar[RelationField] = RelationField("sapBwAdso")
    """
    TBC
    """
    SAP_BW_INFO_OBJECTS: ClassVar[RelationField] = RelationField("sapBwInfoObjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_adso",
        "sap_bw_info_objects",
    ]

    @property
    def sap_bw_adso(self) -> Optional[SAPBWADSO]:
        return None if self.attributes is None else self.attributes.sap_bw_adso

    @sap_bw_adso.setter
    def sap_bw_adso(self, sap_bw_adso: Optional[SAPBWADSO]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_adso = sap_bw_adso

    @property
    def sap_bw_info_objects(self) -> Optional[List[SAPBWInfoObject]]:
        return None if self.attributes is None else self.attributes.sap_bw_info_objects

    @sap_bw_info_objects.setter
    def sap_bw_info_objects(self, sap_bw_info_objects: Optional[List[SAPBWInfoObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_info_objects = sap_bw_info_objects

    class Attributes(SAPBW.Attributes):
        sap_bw_adso: Optional[SAPBWADSO] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_info_objects: Optional[List[SAPBWInfoObject]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWADSOField.Attributes = Field(
        default_factory=lambda: SAPBWADSOField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_a_d_s_o import SAPBWADSO  # noqa: E402, F401
from .s_a_p_b_w_info_object import SAPBWInfoObject  # noqa: E402, F401

SAPBWADSOField.Attributes.update_forward_refs()
