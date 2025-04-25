# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .s_a_p import SAP


class SapErpFunctionModule(SAP):
    """Description"""

    type_name: str = Field(default="SapErpFunctionModule", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpFunctionModule":
            raise ValueError("must be SapErpFunctionModule")
        return v

    def __setattr__(self, name, value):
        if name in SapErpFunctionModule._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_FUNCTION_MODULE_GROUP: ClassVar[KeywordField] = KeywordField(
        "sapErpFunctionModuleGroup", "sapErpFunctionModuleGroup"
    )
    """
    Represents the group to which the SAP ERP function module belongs.
    """
    SAP_ERP_FUNCTION_MODULE_IMPORT_PARAMS: ClassVar[KeywordField] = KeywordField(
        "sapErpFunctionModuleImportParams", "sapErpFunctionModuleImportParams"
    )
    """
    Parameters imported by the SAP ERP function module, defined as key-value pairs.
    """
    SAP_ERP_FUNCTION_MODULE_IMPORT_PARAMS_COUNT: ClassVar[NumericField] = NumericField(
        "sapErpFunctionModuleImportParamsCount", "sapErpFunctionModuleImportParamsCount"
    )
    """
    Represents the total number of Import Parameters in a given SAP ERP Function Module.
    """
    SAP_ERP_FUNCTION_MODULE_EXPORT_PARAMS: ClassVar[KeywordField] = KeywordField(
        "sapErpFunctionModuleExportParams", "sapErpFunctionModuleExportParams"
    )
    """
    Parameters exported by the SAP ERP function module, defined as key-value pairs.
    """
    SAP_ERP_FUNCTION_MODULE_EXPORT_PARAMS_COUNT: ClassVar[NumericField] = NumericField(
        "sapErpFunctionModuleExportParamsCount", "sapErpFunctionModuleExportParamsCount"
    )
    """
    Represents the total number of Export Parameters in a given SAP ERP Function Module.
    """
    SAP_ERP_FUNCTION_EXCEPTION_LIST: ClassVar[KeywordField] = KeywordField(
        "sapErpFunctionExceptionList", "sapErpFunctionExceptionList"
    )
    """
    List of exceptions raised by the SAP ERP function module, defined as key-value pairs.
    """
    SAP_ERP_FUNCTION_EXCEPTION_LIST_COUNT: ClassVar[NumericField] = NumericField(
        "sapErpFunctionExceptionListCount", "sapErpFunctionExceptionListCount"
    )
    """
    Represents the total number of Exceptions in a given SAP ERP Function Module.
    """

    SAP_ERP_COMPONENT: ClassVar[RelationField] = RelationField("sapErpComponent")
    """
    TBC
    """
    SAP_ERP_ABAP_PROGRAM: ClassVar[RelationField] = RelationField("sapErpAbapProgram")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_function_module_group",
        "sap_erp_function_module_import_params",
        "sap_erp_function_module_import_params_count",
        "sap_erp_function_module_export_params",
        "sap_erp_function_module_export_params_count",
        "sap_erp_function_exception_list",
        "sap_erp_function_exception_list_count",
        "sap_erp_component",
        "sap_erp_abap_program",
    ]

    @property
    def sap_erp_function_module_group(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_module_group
        )

    @sap_erp_function_module_group.setter
    def sap_erp_function_module_group(
        self, sap_erp_function_module_group: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_module_group = sap_erp_function_module_group

    @property
    def sap_erp_function_module_import_params(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_module_import_params
        )

    @sap_erp_function_module_import_params.setter
    def sap_erp_function_module_import_params(
        self, sap_erp_function_module_import_params: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_module_import_params = (
            sap_erp_function_module_import_params
        )

    @property
    def sap_erp_function_module_import_params_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_module_import_params_count
        )

    @sap_erp_function_module_import_params_count.setter
    def sap_erp_function_module_import_params_count(
        self, sap_erp_function_module_import_params_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_module_import_params_count = (
            sap_erp_function_module_import_params_count
        )

    @property
    def sap_erp_function_module_export_params(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_module_export_params
        )

    @sap_erp_function_module_export_params.setter
    def sap_erp_function_module_export_params(
        self, sap_erp_function_module_export_params: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_module_export_params = (
            sap_erp_function_module_export_params
        )

    @property
    def sap_erp_function_module_export_params_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_module_export_params_count
        )

    @sap_erp_function_module_export_params_count.setter
    def sap_erp_function_module_export_params_count(
        self, sap_erp_function_module_export_params_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_module_export_params_count = (
            sap_erp_function_module_export_params_count
        )

    @property
    def sap_erp_function_exception_list(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_exception_list
        )

    @sap_erp_function_exception_list.setter
    def sap_erp_function_exception_list(
        self, sap_erp_function_exception_list: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_exception_list = (
            sap_erp_function_exception_list
        )

    @property
    def sap_erp_function_exception_list_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_function_exception_list_count
        )

    @sap_erp_function_exception_list_count.setter
    def sap_erp_function_exception_list_count(
        self, sap_erp_function_exception_list_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_function_exception_list_count = (
            sap_erp_function_exception_list_count
        )

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
        sap_erp_function_module_group: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_function_module_import_params: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        sap_erp_function_module_import_params_count: Optional[int] = Field(
            default=None, description=""
        )
        sap_erp_function_module_export_params: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        sap_erp_function_module_export_params_count: Optional[int] = Field(
            default=None, description=""
        )
        sap_erp_function_exception_list: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        sap_erp_function_exception_list_count: Optional[int] = Field(
            default=None, description=""
        )
        sap_erp_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_abap_program: Optional[SapErpAbapProgram] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpFunctionModule.Attributes = Field(
        default_factory=lambda: SapErpFunctionModule.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_abap_program import SapErpAbapProgram  # noqa: E402, F401
from .sap_erp_component import SapErpComponent  # noqa: E402, F401

SapErpFunctionModule.Attributes.update_forward_refs()
