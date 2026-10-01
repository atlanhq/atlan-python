# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .core.sap_analytics_cloud import SapAnalyticsCloud


class SapAnalyticsCloudModel(SapAnalyticsCloud):
    """Description"""

    type_name: str = Field(default="SapAnalyticsCloudModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapAnalyticsCloudModel":
            raise ValueError("must be SapAnalyticsCloudModel")
        return v

    def __setattr__(self, name, value):
        if name in SapAnalyticsCloudModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ANALYTICS_CLOUD_MODEL_KIND: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudModelKind", "sapAnalyticsCloudModelKind"
    )
    """
    Whether this model is an analytic model or a planning model, as reported by the source. ANALYTIC for a read-only model used for analysis and reporting, PLANNING for a model that supports write-back, versions and planning operations.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_DATA_ACCESS_MODE: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudDataAccessMode", "sapAnalyticsCloudDataAccessMode"
    )
    """
    How this model reaches its data, as reported by the source. IMPORT when the data is acquired into SAP Analytics Cloud and stored there, LIVE when it stays in a remote system and is queried live over a connection.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_PROVIDER_ID: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudProviderId", "sapAnalyticsCloudProviderId"
    )
    """
    Identifier of the OData provider that exposes this model's metadata. This is the key that joins a model to its columns.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_MODEL_ID: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudModelId", "sapAnalyticsCloudModelId"
    )
    """
    Model identifier reported by the SAP Analytics Cloud tenant APIs, which differs from the file-repository resource identifier for live models.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_STORY_COUNT: ClassVar[NumericField] = NumericField(
        "sapAnalyticsCloudStoryCount", "sapAnalyticsCloudStoryCount"
    )
    """
    Number of SAP Analytics Cloud stories that consume this model, as reported by the source.
    """
    SAP_ANALYTICS_CLOUD_LIVE_CONNECTION_ID: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudLiveConnectionId", "sapAnalyticsCloudLiveConnectionId"
    )
    """
    Identifier of the remote connection a live model reads from. Empty for imported models.
    """
    SAP_ANALYTICS_CLOUD_LIVE_CONNECTION_NAME: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudLiveConnectionName", "sapAnalyticsCloudLiveConnectionName"
    )
    """
    Simple name of the remote connection a live model reads from. Empty for imported models.
    """
    SAP_ANALYTICS_CLOUD_LIVE_CONNECTION_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudLiveConnectionType", "sapAnalyticsCloudLiveConnectionType"
    )
    """
    Type of the remote connection a live model reads from, such as DIRECT. Empty for imported models.
    """
    SAP_ANALYTICS_CLOUD_LIVE_CONNECTION_SYSTEM_TYPE: ClassVar[KeywordField] = (
        KeywordField(
            "sapAnalyticsCloudLiveConnectionSystemType",
            "sapAnalyticsCloudLiveConnectionSystemType",
        )
    )
    """
    Type of the remote system a live model reads from, such as DWC for SAP Datasphere. Empty for imported models.
    """
    SAP_ANALYTICS_CLOUD_LIVE_CONNECTION_HOST: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudLiveConnectionHost", "sapAnalyticsCloudLiveConnectionHost"
    )
    """
    Host of the remote system a live model reads from. Empty for imported models.
    """
    SAP_ANALYTICS_CLOUD_LIVE_CONNECTION_PORT: ClassVar[NumericField] = NumericField(
        "sapAnalyticsCloudLiveConnectionPort", "sapAnalyticsCloudLiveConnectionPort"
    )
    """
    Port of the remote system a live model reads from. Empty for imported models.
    """
    SAP_ANALYTICS_CLOUD_LIVE_CONNECTION_PROTOCOL: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudLiveConnectionProtocol",
        "sapAnalyticsCloudLiveConnectionProtocol",
    )
    """
    Protocol used to reach the remote system a live model reads from, such as HTTPS. Empty for imported models.
    """

    SAP_ANALYTICS_CLOUD_COLUMNS: ClassVar[RelationField] = RelationField(
        "sapAnalyticsCloudColumns"
    )
    """
    TBC
    """
    SAP_ANALYTICS_CLOUD_FOLDER: ClassVar[RelationField] = RelationField(
        "sapAnalyticsCloudFolder"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_analytics_cloud_model_kind",
        "sap_analytics_cloud_data_access_mode",
        "sap_analytics_cloud_provider_id",
        "sap_analytics_cloud_model_id",
        "sap_analytics_cloud_story_count",
        "sap_analytics_cloud_live_connection_id",
        "sap_analytics_cloud_live_connection_name",
        "sap_analytics_cloud_live_connection_type",
        "sap_analytics_cloud_live_connection_system_type",
        "sap_analytics_cloud_live_connection_host",
        "sap_analytics_cloud_live_connection_port",
        "sap_analytics_cloud_live_connection_protocol",
        "sap_analytics_cloud_columns",
        "sap_analytics_cloud_folder",
    ]

    @property
    def sap_analytics_cloud_model_kind(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_model_kind
        )

    @sap_analytics_cloud_model_kind.setter
    def sap_analytics_cloud_model_kind(
        self, sap_analytics_cloud_model_kind: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_model_kind = sap_analytics_cloud_model_kind

    @property
    def sap_analytics_cloud_data_access_mode(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_data_access_mode
        )

    @sap_analytics_cloud_data_access_mode.setter
    def sap_analytics_cloud_data_access_mode(
        self, sap_analytics_cloud_data_access_mode: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_data_access_mode = (
            sap_analytics_cloud_data_access_mode
        )

    @property
    def sap_analytics_cloud_provider_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_provider_id
        )

    @sap_analytics_cloud_provider_id.setter
    def sap_analytics_cloud_provider_id(
        self, sap_analytics_cloud_provider_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_provider_id = (
            sap_analytics_cloud_provider_id
        )

    @property
    def sap_analytics_cloud_model_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_model_id
        )

    @sap_analytics_cloud_model_id.setter
    def sap_analytics_cloud_model_id(self, sap_analytics_cloud_model_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_model_id = sap_analytics_cloud_model_id

    @property
    def sap_analytics_cloud_story_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_story_count
        )

    @sap_analytics_cloud_story_count.setter
    def sap_analytics_cloud_story_count(
        self, sap_analytics_cloud_story_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_story_count = (
            sap_analytics_cloud_story_count
        )

    @property
    def sap_analytics_cloud_live_connection_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_live_connection_id
        )

    @sap_analytics_cloud_live_connection_id.setter
    def sap_analytics_cloud_live_connection_id(
        self, sap_analytics_cloud_live_connection_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_live_connection_id = (
            sap_analytics_cloud_live_connection_id
        )

    @property
    def sap_analytics_cloud_live_connection_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_live_connection_name
        )

    @sap_analytics_cloud_live_connection_name.setter
    def sap_analytics_cloud_live_connection_name(
        self, sap_analytics_cloud_live_connection_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_live_connection_name = (
            sap_analytics_cloud_live_connection_name
        )

    @property
    def sap_analytics_cloud_live_connection_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_live_connection_type
        )

    @sap_analytics_cloud_live_connection_type.setter
    def sap_analytics_cloud_live_connection_type(
        self, sap_analytics_cloud_live_connection_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_live_connection_type = (
            sap_analytics_cloud_live_connection_type
        )

    @property
    def sap_analytics_cloud_live_connection_system_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_live_connection_system_type
        )

    @sap_analytics_cloud_live_connection_system_type.setter
    def sap_analytics_cloud_live_connection_system_type(
        self, sap_analytics_cloud_live_connection_system_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_live_connection_system_type = (
            sap_analytics_cloud_live_connection_system_type
        )

    @property
    def sap_analytics_cloud_live_connection_host(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_live_connection_host
        )

    @sap_analytics_cloud_live_connection_host.setter
    def sap_analytics_cloud_live_connection_host(
        self, sap_analytics_cloud_live_connection_host: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_live_connection_host = (
            sap_analytics_cloud_live_connection_host
        )

    @property
    def sap_analytics_cloud_live_connection_port(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_live_connection_port
        )

    @sap_analytics_cloud_live_connection_port.setter
    def sap_analytics_cloud_live_connection_port(
        self, sap_analytics_cloud_live_connection_port: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_live_connection_port = (
            sap_analytics_cloud_live_connection_port
        )

    @property
    def sap_analytics_cloud_live_connection_protocol(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_live_connection_protocol
        )

    @sap_analytics_cloud_live_connection_protocol.setter
    def sap_analytics_cloud_live_connection_protocol(
        self, sap_analytics_cloud_live_connection_protocol: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_live_connection_protocol = (
            sap_analytics_cloud_live_connection_protocol
        )

    @property
    def sap_analytics_cloud_columns(self) -> Optional[List[SapAnalyticsCloudColumn]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_columns
        )

    @sap_analytics_cloud_columns.setter
    def sap_analytics_cloud_columns(
        self, sap_analytics_cloud_columns: Optional[List[SapAnalyticsCloudColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_columns = sap_analytics_cloud_columns

    @property
    def sap_analytics_cloud_folder(self) -> Optional[SapAnalyticsCloudFolder]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_folder
        )

    @sap_analytics_cloud_folder.setter
    def sap_analytics_cloud_folder(
        self, sap_analytics_cloud_folder: Optional[SapAnalyticsCloudFolder]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_folder = sap_analytics_cloud_folder

    class Attributes(SapAnalyticsCloud.Attributes):
        sap_analytics_cloud_model_kind: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_data_access_mode: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_provider_id: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_model_id: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_story_count: Optional[int] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_live_connection_id: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_live_connection_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_live_connection_type: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_live_connection_system_type: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_live_connection_host: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_live_connection_port: Optional[int] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_live_connection_protocol: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_columns: Optional[List[SapAnalyticsCloudColumn]] = Field(
            default=None, description=""
        )  # relationship
        sap_analytics_cloud_folder: Optional[SapAnalyticsCloudFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapAnalyticsCloudModel.Attributes = Field(
        default_factory=lambda: SapAnalyticsCloudModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_analytics_cloud_column import SapAnalyticsCloudColumn  # noqa: E402, F401
from .sap_analytics_cloud_folder import SapAnalyticsCloudFolder  # noqa: E402, F401

SapAnalyticsCloudModel.Attributes.update_forward_refs()
