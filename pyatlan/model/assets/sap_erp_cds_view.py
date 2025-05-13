# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .s_a_p import SAP


class SapErpCdsView(SAP):
    """Description"""

    type_name: str = Field(default="SapErpCdsView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpCdsView":
            raise ValueError("must be SapErpCdsView")
        return v

    def __setattr__(self, name, value):
        if name in SapErpCdsView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_CDS_VIEW_TECHNICAL_NAME: ClassVar[KeywordField] = KeywordField(
        "sapErpCdsViewTechnicalName", "sapErpCdsViewTechnicalName"
    )
    """
    The technical database view name of the SAP ERP CDS View.
    """
    SAP_ERP_CDS_VIEW_SOURCE_NAME: ClassVar[KeywordField] = KeywordField(
        "sapErpCdsViewSourceName", "sapErpCdsViewSourceName"
    )
    """
    The source name of the SAP ERP CDS View Definition.
    """
    SAP_ERP_CDS_VIEW_SOURCE_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapErpCdsViewSourceType", "sapErpCdsViewSourceType"
    )
    """
    The source type of the SAP ERP CDS View Definition.
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
        "sap_erp_cds_view_technical_name",
        "sap_erp_cds_view_source_name",
        "sap_erp_cds_view_source_type",
        "sap_erp_component",
        "sap_erp_columns",
    ]

    @property
    def sap_erp_cds_view_technical_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_cds_view_technical_name
        )

    @sap_erp_cds_view_technical_name.setter
    def sap_erp_cds_view_technical_name(
        self, sap_erp_cds_view_technical_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_cds_view_technical_name = (
            sap_erp_cds_view_technical_name
        )

    @property
    def sap_erp_cds_view_source_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_cds_view_source_name
        )

    @sap_erp_cds_view_source_name.setter
    def sap_erp_cds_view_source_name(self, sap_erp_cds_view_source_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_cds_view_source_name = sap_erp_cds_view_source_name

    @property
    def sap_erp_cds_view_source_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_cds_view_source_type
        )

    @sap_erp_cds_view_source_type.setter
    def sap_erp_cds_view_source_type(self, sap_erp_cds_view_source_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_cds_view_source_type = sap_erp_cds_view_source_type

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
        sap_erp_cds_view_technical_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_cds_view_source_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_cds_view_source_type: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_columns: Optional[List[SapErpColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpCdsView.Attributes = Field(
        default_factory=lambda: SapErpCdsView.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_column import SapErpColumn  # noqa: E402, F401
from .sap_erp_component import SapErpComponent  # noqa: E402, F401

SapErpCdsView.Attributes.update_forward_refs()
