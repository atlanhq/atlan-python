# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, RelationField

from .s_a_p_b_w import SAPBW


class SAPBWCompositeProvider(SAPBW):
    """Description"""

    type_name: str = Field(default="SAPBWCompositeProvider", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAPBWCompositeProvider":
            raise ValueError("must be SAPBWCompositeProvider")
        return v

    def __setattr__(self, name, value):
        if name in SAPBWCompositeProvider._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_BW_IS_HANA_MODEL: ClassVar[BooleanField] = BooleanField(
        "sapBwIsHanaModel", "sapBwIsHanaModel"
    )
    """
    Whether this CompositeProvider is a HANA model (RSOHCPR.HANAMODELFL).
    """

    SAP_BW_ADSOS: ClassVar[RelationField] = RelationField("sapBwAdsos")
    """
    TBC
    """
    SAP_BW_COMPOSITE_PROVIDER_FIELDS: ClassVar[RelationField] = RelationField(
        "sapBwCompositeProviderFields"
    )
    """
    TBC
    """
    SAP_BW_INFO_AREA: ClassVar[RelationField] = RelationField("sapBwInfoArea")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_bw_is_hana_model",
        "sap_bw_adsos",
        "sap_bw_composite_provider_fields",
        "sap_bw_info_area",
    ]

    @property
    def sap_bw_is_hana_model(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.sap_bw_is_hana_model

    @sap_bw_is_hana_model.setter
    def sap_bw_is_hana_model(self, sap_bw_is_hana_model: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_is_hana_model = sap_bw_is_hana_model

    @property
    def sap_bw_adsos(self) -> Optional[List[SAPBWADSO]]:
        return None if self.attributes is None else self.attributes.sap_bw_adsos

    @sap_bw_adsos.setter
    def sap_bw_adsos(self, sap_bw_adsos: Optional[List[SAPBWADSO]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_adsos = sap_bw_adsos

    @property
    def sap_bw_composite_provider_fields(
        self,
    ) -> Optional[List[SAPBWCompositeProviderField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_bw_composite_provider_fields
        )

    @sap_bw_composite_provider_fields.setter
    def sap_bw_composite_provider_fields(
        self,
        sap_bw_composite_provider_fields: Optional[List[SAPBWCompositeProviderField]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_bw_composite_provider_fields = (
            sap_bw_composite_provider_fields
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
        sap_bw_is_hana_model: Optional[bool] = Field(default=None, description="")
        sap_bw_adsos: Optional[List[SAPBWADSO]] = Field(
            default=None, description=""
        )  # relationship
        sap_bw_composite_provider_fields: Optional[
            List[SAPBWCompositeProviderField]
        ] = Field(default=None, description="")  # relationship
        sap_bw_info_area: Optional[SAPBWInfoArea] = Field(
            default=None, description=""
        )  # relationship

    attributes: SAPBWCompositeProvider.Attributes = Field(
        default_factory=lambda: SAPBWCompositeProvider.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_a_p_b_w_a_d_s_o import SAPBWADSO  # noqa: E402, F401
from .s_a_p_b_w_composite_provider_field import (
    SAPBWCompositeProviderField,  # noqa: E402, F401
)
from .s_a_p_b_w_info_area import SAPBWInfoArea  # noqa: E402, F401

SAPBWCompositeProvider.Attributes.update_forward_refs()
