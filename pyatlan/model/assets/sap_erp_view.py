# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p import SAP


class SapErpView(SAP):
    """Description"""

    type_name: str = Field(default="SapErpView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpView":
            raise ValueError("must be SapErpView")
        return v

    def __setattr__(self, name, value):
        if name in SapErpView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_VIEW_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapErpViewType", "sapErpViewType"
    )
    """
    Type of the SAP ERP View.
    """
    SAP_ERP_VIEW_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "sapErpViewDefinition", "sapErpViewDefinition"
    )
    """
    Specifies the definition of the SAP ERP View
    """

    SAP_ERP_COMPONENT: ClassVar[RelationField] = RelationField("sapErpComponent")
    """
    TBC
    """
    SAP_ERP_COLUMNS: ClassVar[RelationField] = RelationField("sapErpColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_view_type",
        "sap_erp_view_definition",
        "sap_erp_component",
        "sap_erp_columns",
    ]

    @property
    def sap_erp_view_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_erp_view_type

    @sap_erp_view_type.setter
    def sap_erp_view_type(self, sap_erp_view_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_view_type = sap_erp_view_type

    @property
    def sap_erp_view_definition(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sap_erp_view_definition
        )

    @sap_erp_view_definition.setter
    def sap_erp_view_definition(self, sap_erp_view_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_view_definition = sap_erp_view_definition

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
        sap_erp_view_type: Optional[str] = Field(default=None, description="")
        sap_erp_view_definition: Optional[str] = Field(default=None, description="")
        sap_erp_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_columns: Optional[List[SapErpColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpView.Attributes = Field(
        default_factory=lambda: SapErpView.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_column import SapErpColumn  # noqa: E402, F401
from .sap_erp_component import SapErpComponent  # noqa: E402, F401

SapErpView.Attributes.update_forward_refs()
