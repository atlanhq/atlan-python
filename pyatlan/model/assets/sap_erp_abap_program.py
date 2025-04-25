# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p import SAP


class SapErpAbapProgram(SAP):
    """Description"""

    type_name: str = Field(default="SapErpAbapProgram", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpAbapProgram":
            raise ValueError("must be SapErpAbapProgram")
        return v

    def __setattr__(self, name, value):
        if name in SapErpAbapProgram._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_ABAP_PROGRAM_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapErpAbapProgramType", "sapErpAbapProgramType"
    )
    """
    Specifies the type of ABAP program in SAP ERP (e.g., Report, Module Pool, Function Group).
    """

    SAP_ERP_COMPONENT: ClassVar[RelationField] = RelationField("sapErpComponent")
    """
    TBC
    """
    SAP_ERP_FUNCTION_MODULES: ClassVar[RelationField] = RelationField(
        "sapErpFunctionModules"
    )
    """
    TBC
    """
    SAP_ERP_TRANSACTION_CODES: ClassVar[RelationField] = RelationField(
        "sapErpTransactionCodes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_abap_program_type",
        "sap_erp_component",
        "sap_erp_function_modules",
        "sap_erp_transaction_codes",
    ]

    @property
    def sap_erp_abap_program_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_abap_program_type
        )

    @sap_erp_abap_program_type.setter
    def sap_erp_abap_program_type(self, sap_erp_abap_program_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_abap_program_type = sap_erp_abap_program_type

    @property
    def sap_erp_component(self) -> Optional[SapErpComponent]:
        return None if self.attributes is None else self.attributes.sap_erp_component

    @sap_erp_component.setter
    def sap_erp_component(self, sap_erp_component: Optional[SapErpComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_component = sap_erp_component

    @property
    def sap_erp_function_modules(self) -> Optional[List[SapErpFunctionModule]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_modules
        )

    @sap_erp_function_modules.setter
    def sap_erp_function_modules(
        self, sap_erp_function_modules: Optional[List[SapErpFunctionModule]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_modules = sap_erp_function_modules

    @property
    def sap_erp_transaction_codes(self) -> Optional[List[SapErpTransactionCode]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_transaction_codes
        )

    @sap_erp_transaction_codes.setter
    def sap_erp_transaction_codes(
        self, sap_erp_transaction_codes: Optional[List[SapErpTransactionCode]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_transaction_codes = sap_erp_transaction_codes

    class Attributes(SAP.Attributes):
        sap_erp_abap_program_type: Optional[str] = Field(default=None, description="")
        sap_erp_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_function_modules: Optional[List[SapErpFunctionModule]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_transaction_codes: Optional[List[SapErpTransactionCode]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpAbapProgram.Attributes = Field(
        default_factory=lambda: SapErpAbapProgram.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_component import SapErpComponent  # noqa: E402, F401
from .sap_erp_function_module import SapErpFunctionModule  # noqa: E402, F401
from .sap_erp_transaction_code import SapErpTransactionCode  # noqa: E402, F401

SapErpAbapProgram.Attributes.update_forward_refs()
