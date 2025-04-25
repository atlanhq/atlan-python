# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p import SAP


class SapErpTable(SAP):
    """Description"""

    type_name: str = Field(default="SapErpTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpTable":
            raise ValueError("must be SapErpTable")
        return v

    def __setattr__(self, name, value):
        if name in SapErpTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_TABLE_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapErpTableType", "sapErpTableType"
    )
    """
    Type of the SAP ERP table.
    """
    SAP_ERP_TABLE_DELIVERY_CLASS: ClassVar[KeywordField] = KeywordField(
        "sapErpTableDeliveryClass", "sapErpTableDeliveryClass"
    )
    """
    Defines the delivery class of the SAP ERP table, determining how the table's data is transported and managed during system updates.
    """  # noqa: E501

    SAP_ERP_COMPONENT: ClassVar[RelationField] = RelationField("sapErpComponent")
    """
    TBC
    """
    SAP_ERP_COLUMNS: ClassVar[RelationField] = RelationField("sapErpColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_table_type",
        "sap_erp_table_delivery_class",
        "sap_erp_component",
        "sap_erp_columns",
    ]

    @property
    def sap_erp_table_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_erp_table_type

    @sap_erp_table_type.setter
    def sap_erp_table_type(self, sap_erp_table_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_table_type = sap_erp_table_type

    @property
    def sap_erp_table_delivery_class(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_table_delivery_class
        )

    @sap_erp_table_delivery_class.setter
    def sap_erp_table_delivery_class(self, sap_erp_table_delivery_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_table_delivery_class = sap_erp_table_delivery_class

    @property
    def sap_erp_component(self) -> Optional[SapErpComponent]:
        return None if self.attributes is None else self.attributes.sap_erp_component

    @sap_erp_component.setter
    def sap_erp_component(self, sap_erp_component: Optional[SapErpComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_component = sap_erp_component

    @property
    def sap_erp_columns(self) -> Optional[List[SapErpColumn]]:
        return None if self.attributes is None else self.attributes.sap_erp_columns

    @sap_erp_columns.setter
    def sap_erp_columns(self, sap_erp_columns: Optional[List[SapErpColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_columns = sap_erp_columns

    class Attributes(SAP.Attributes):
        sap_erp_table_type: Optional[str] = Field(default=None, description="")
        sap_erp_table_delivery_class: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_columns: Optional[List[SapErpColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpTable.Attributes = Field(
        default_factory=lambda: SapErpTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_column import SapErpColumn  # noqa: E402, F401
from .sap_erp_component import SapErpComponent  # noqa: E402, F401

SapErpTable.Attributes.update_forward_refs()
