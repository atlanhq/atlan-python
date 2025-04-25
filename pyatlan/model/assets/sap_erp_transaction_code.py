# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .s_a_p import SAP


class SapErpTransactionCode(SAP):
    """Description"""

    type_name: str = Field(default="SapErpTransactionCode", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpTransactionCode":
            raise ValueError("must be SapErpTransactionCode")
        return v

    def __setattr__(self, name, value):
        if name in SapErpTransactionCode._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_COMPONENT: ClassVar[RelationField] = RelationField("sapErpComponent")
    """
    TBC
    """
    SAP_ERP_ABAP_PROGRAM: ClassVar[RelationField] = RelationField("sapErpAbapProgram")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_component",
        "sap_erp_abap_program",
    ]

    @property
    def sap_erp_component(self) -> Optional[SapErpComponent]:
        return None if self.attributes is None else self.attributes.sap_erp_component

    @sap_erp_component.setter
    def sap_erp_component(self, sap_erp_component: Optional[SapErpComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_component = sap_erp_component

    @property
    def sap_erp_abap_program(self) -> Optional[SapErpAbapProgram]:
        return None if self.attributes is None else self.attributes.sap_erp_abap_program

    @sap_erp_abap_program.setter
    def sap_erp_abap_program(self, sap_erp_abap_program: Optional[SapErpAbapProgram]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_abap_program = sap_erp_abap_program

    class Attributes(SAP.Attributes):
        sap_erp_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_abap_program: Optional[SapErpAbapProgram] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpTransactionCode.Attributes = Field(
        default_factory=lambda: SapErpTransactionCode.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_abap_program import SapErpAbapProgram  # noqa: E402, F401
from .sap_erp_component import SapErpComponent  # noqa: E402, F401

SapErpTransactionCode.Attributes.update_forward_refs()
