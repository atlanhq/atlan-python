# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .core.s_a_p import SAP


class SapErpFioriApp(SAP):
    """Description"""

    type_name: str = Field(default="SapErpFioriApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpFioriApp":
            raise ValueError("must be SapErpFioriApp")
        return v

    def __setattr__(self, name, value):
        if name in SapErpFioriApp._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_FIORI_APP_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapErpFioriAppType", "sapErpFioriAppType"
    )
    """
    Application type of the Fiori App from sap.app.type in the manifest, such as application, transactional, or factsheet.
    """  # noqa: E501
    SAP_ERP_FIORI_APP_ARCHE_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapErpFioriAppArcheType", "sapErpFioriAppArcheType"
    )
    """
    Fiori archetype from sap.fiori.archeType in the manifest, such as transactional.
    """
    SAP_ERP_FIORI_APP_IS_CUSTOM: ClassVar[BooleanField] = BooleanField(
        "sapErpFioriAppIsCustom", "sapErpFioriAppIsCustom"
    )
    """
    When true, the Fiori App has no sap.fiori.registrationIds in its manifest and is treated as a customer (Z-app) build.
    """  # noqa: E501
    SAP_ERP_FIORI_APP_BSP_APPLICATION: ClassVar[KeywordField] = KeywordField(
        "sapErpFioriAppBspApplication", "sapErpFioriAppBspApplication"
    )
    """
    BSP container name for the Fiori App as registered in O2APPL (e.g. ATP_ABOPVARS1).
    """
    SAP_ERP_FIORI_APP_ODATA_SERVICE_NAME: ClassVar[KeywordField] = KeywordField(
        "sapErpFioriAppOdataServiceName", "sapErpFioriAppOdataServiceName"
    )
    """
    Resolved OData service name extracted from the manifest mainService URI (e.g. UI_ABOPVARIANT_CONFIGURE or C_SUPPLIEREVALUATION_CDS).
    """  # noqa: E501
    SAP_ERP_FIORI_APP_ODATA_SERVICE_URI: ClassVar[KeywordField] = KeywordField(
        "sapErpFioriAppOdataServiceUri", "sapErpFioriAppOdataServiceUri"
    )
    """
    Full OData service URI from sap.app.dataSources.mainService.uri in the manifest.
    """
    SAP_ERP_FIORI_APP_ODATA_VERSION: ClassVar[KeywordField] = KeywordField(
        "sapErpFioriAppOdataVersion", "sapErpFioriAppOdataVersion"
    )
    """
    OData protocol version of the Fiori App's main data source, such as 2.0 or 4.0.
    """

    SAP_ERP_COMPONENT: ClassVar[RelationField] = RelationField("sapErpComponent")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_fiori_app_type",
        "sap_erp_fiori_app_arche_type",
        "sap_erp_fiori_app_is_custom",
        "sap_erp_fiori_app_bsp_application",
        "sap_erp_fiori_app_odata_service_name",
        "sap_erp_fiori_app_odata_service_uri",
        "sap_erp_fiori_app_odata_version",
        "sap_erp_component",
    ]

    @property
    def sap_erp_fiori_app_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sap_erp_fiori_app_type
        )

    @sap_erp_fiori_app_type.setter
    def sap_erp_fiori_app_type(self, sap_erp_fiori_app_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_fiori_app_type = sap_erp_fiori_app_type

    @property
    def sap_erp_fiori_app_arche_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_fiori_app_arche_type
        )

    @sap_erp_fiori_app_arche_type.setter
    def sap_erp_fiori_app_arche_type(self, sap_erp_fiori_app_arche_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_fiori_app_arche_type = sap_erp_fiori_app_arche_type

    @property
    def sap_erp_fiori_app_is_custom(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_fiori_app_is_custom
        )

    @sap_erp_fiori_app_is_custom.setter
    def sap_erp_fiori_app_is_custom(self, sap_erp_fiori_app_is_custom: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_fiori_app_is_custom = sap_erp_fiori_app_is_custom

    @property
    def sap_erp_fiori_app_bsp_application(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_fiori_app_bsp_application
        )

    @sap_erp_fiori_app_bsp_application.setter
    def sap_erp_fiori_app_bsp_application(
        self, sap_erp_fiori_app_bsp_application: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_fiori_app_bsp_application = (
            sap_erp_fiori_app_bsp_application
        )

    @property
    def sap_erp_fiori_app_odata_service_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_fiori_app_odata_service_name
        )

    @sap_erp_fiori_app_odata_service_name.setter
    def sap_erp_fiori_app_odata_service_name(
        self, sap_erp_fiori_app_odata_service_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_fiori_app_odata_service_name = (
            sap_erp_fiori_app_odata_service_name
        )

    @property
    def sap_erp_fiori_app_odata_service_uri(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_fiori_app_odata_service_uri
        )

    @sap_erp_fiori_app_odata_service_uri.setter
    def sap_erp_fiori_app_odata_service_uri(
        self, sap_erp_fiori_app_odata_service_uri: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_fiori_app_odata_service_uri = (
            sap_erp_fiori_app_odata_service_uri
        )

    @property
    def sap_erp_fiori_app_odata_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_fiori_app_odata_version
        )

    @sap_erp_fiori_app_odata_version.setter
    def sap_erp_fiori_app_odata_version(
        self, sap_erp_fiori_app_odata_version: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_fiori_app_odata_version = (
            sap_erp_fiori_app_odata_version
        )

    @property
    def sap_erp_component(self) -> Optional[SapErpComponent]:
        return None if self.attributes is None else self.attributes.sap_erp_component

    @sap_erp_component.setter
    def sap_erp_component(self, sap_erp_component: Optional[SapErpComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_component = sap_erp_component

    class Attributes(SAP.Attributes):
        sap_erp_fiori_app_type: Optional[str] = Field(default=None, description="")
        sap_erp_fiori_app_arche_type: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_fiori_app_is_custom: Optional[bool] = Field(
            default=None, description=""
        )
        sap_erp_fiori_app_bsp_application: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_fiori_app_odata_service_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_fiori_app_odata_service_uri: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_fiori_app_odata_version: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_component: Optional[SapErpComponent] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpFioriApp.Attributes = Field(
        default_factory=lambda: SapErpFioriApp.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_erp_component import SapErpComponent  # noqa: E402, F401

SapErpFioriApp.Attributes.update_forward_refs()
