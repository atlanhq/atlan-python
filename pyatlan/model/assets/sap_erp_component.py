# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .s_a_p import SAP


class SapErpComponent(SAP):
    """Description"""

    type_name: str = Field(default="SapErpComponent", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpComponent":
            raise ValueError("must be SapErpComponent")
        return v

    def __setattr__(self, name, value):
        if name in SapErpComponent._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_TABLES: ClassVar[RelationField] = RelationField("sapErpTables")
    """
    TBC
    """
    SAP_ERP_VIEWS: ClassVar[RelationField] = RelationField("sapErpViews")
    """
    TBC
    """
    CHILD_COMPONENTS: ClassVar[RelationField] = RelationField("childComponents")
    """
    TBC
    """
    SAP_ERP_CDS_VIEWS: ClassVar[RelationField] = RelationField("sapErpCdsViews")
    """
    TBC
    """
    SAP_ERP_FUNCTION_MODULES: ClassVar[RelationField] = RelationField(
        "sapErpFunctionModules"
    )
    """
    TBC
    """
    SAP_ERP_ABAP_PROGRAMS: ClassVar[RelationField] = RelationField("sapErpAbapPrograms")
    """
    TBC
    """
    SAP_ERP_TRANSACTION_CODES: ClassVar[RelationField] = RelationField(
        "sapErpTransactionCodes"
    )
    """
    TBC
    """
    PARENT_COMPONENT: ClassVar[RelationField] = RelationField("parentComponent")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_tables",
        "sap_erp_views",
        "child_components",
        "sap_erp_cds_views",
        "sap_erp_function_modules",
        "sap_erp_abap_programs",
        "sap_erp_transaction_codes",
        "parent_component",
    ]

    @property
    def sap_erp_tables(self) -> Optional[List[SapErpTable]]:
        return None if self.attributes is None else self.attributes.sap_erp_tables

    @sap_erp_tables.setter
    def sap_erp_tables(self, sap_erp_tables: Optional[List[SapErpTable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_tables = sap_erp_tables

    @property
    def sap_erp_views(self) -> Optional[List[SapErpView]]:
        return None if self.attributes is None else self.attributes.sap_erp_views

    @sap_erp_views.setter
    def sap_erp_views(self, sap_erp_views: Optional[List[SapErpView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_views = sap_erp_views

    @property
    def child_components(self) -> Optional[List[SapErpComponent]]:
        return None if self.attributes is None else self.attributes.child_components

    @child_components.setter
    def child_components(self, child_components: Optional[List[SapErpComponent]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.child_components = child_components

    @property
    def sap_erp_cds_views(self) -> Optional[List[SapErpCdsView]]:
        return None if self.attributes is None else self.attributes.sap_erp_cds_views

    @sap_erp_cds_views.setter
    def sap_erp_cds_views(self, sap_erp_cds_views: Optional[List[SapErpCdsView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_cds_views = sap_erp_cds_views

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
    def sap_erp_abap_programs(self) -> Optional[List[SapErpAbapProgram]]:
        return (
            None if self.attributes is None else self.attributes.sap_erp_abap_programs
        )

    @sap_erp_abap_programs.setter
    def sap_erp_abap_programs(
        self, sap_erp_abap_programs: Optional[List[SapErpAbapProgram]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_abap_programs = sap_erp_abap_programs

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

    @property
    def parent_component(self) -> Optional[SapErpComponent]:
        return None if self.attributes is None else self.attributes.parent_component

    @parent_component.setter
    def parent_component(self, parent_component: Optional[SapErpComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_component = parent_component

    class Attributes(SAP.Attributes):
        sap_erp_tables: Optional[List[SapErpTable]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_views: Optional[List[SapErpView]] = Field(
            default=None, description=""
        )  # relationship
        child_components: Optional[List[SapErpComponent]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_cds_views: Optional[List[SapErpCdsView]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_function_modules: Optional[List[SapErpFunctionModule]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_abap_programs: Optional[List[SapErpAbapProgram]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_transaction_codes: Optional[List[SapErpTransactionCode]] = Field(
            default=None, description=""
        )  # relationship
        parent_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpComponent.Attributes = Field(
        default_factory=lambda: SapErpComponent.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_abap_program import SapErpAbapProgram  # noqa: E402, F401
from .sap_erp_cds_view import SapErpCdsView  # noqa: E402, F401
from .sap_erp_function_module import SapErpFunctionModule  # noqa: E402, F401
from .sap_erp_table import SapErpTable  # noqa: E402, F401
from .sap_erp_transaction_code import SapErpTransactionCode  # noqa: E402, F401
from .sap_erp_view import SapErpView  # noqa: E402, F401

SapErpComponent.Attributes.update_forward_refs()
