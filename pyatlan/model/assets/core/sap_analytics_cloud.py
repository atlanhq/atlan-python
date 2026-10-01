# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .s_a_p import SAP


class SapAnalyticsCloud(SAP):
    """Description"""

    type_name: str = Field(default="SapAnalyticsCloud", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapAnalyticsCloud":
            raise ValueError("must be SapAnalyticsCloud")
        return v

    def __setattr__(self, name, value):
        if name in SapAnalyticsCloud._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ANALYTICS_CLOUD_RESOURCE_ID: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudResourceId", "sapAnalyticsCloudResourceId"
    )
    """
    Identifier of this asset in the SAP Analytics Cloud file repository. Stable across renames and used by the source APIs to address the resource.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_OBJECT_ID: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudObjectId", "sapAnalyticsCloudObjectId"
    )
    """
    Underlying object identifier reported by the SAP Analytics Cloud file repository for this asset.
    """
    SAP_ANALYTICS_CLOUD_REPOSITORY_PARTITION: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudRepositoryPartition", "sapAnalyticsCloudRepositoryPartition"
    )
    """
    Partition of the SAP Analytics Cloud file repository this asset lives in: PUBLIC for shared tenant content, SYSTEM for SAP-shipped content and SAP Analytics Cloud's own telemetry, USERS for the container holding per-user private areas, and PRIVATE for an individual user's own content. Reported by the source as folderType, and carried by every resource rather than only by folders.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_WORKSPACE_ID: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudWorkspaceId", "sapAnalyticsCloudWorkspaceId"
    )
    """
    Identifier of the SAP Analytics Cloud workspace that owns this asset.
    """
    SAP_ANALYTICS_CLOUD_WORKSPACE_NAME: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudWorkspaceName", "sapAnalyticsCloudWorkspaceName"
    )
    """
    Simple name of the SAP Analytics Cloud workspace that owns this asset.
    """
    SAP_ANALYTICS_CLOUD_PARENT_FOLDER_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "sapAnalyticsCloudParentFolderQualifiedName",
            "sapAnalyticsCloudParentFolderQualifiedName",
        )
    )
    """
    Unique name of the SAP Analytics Cloud folder that directly contains this asset. Empty for a root-level folder and for a live model, neither of which is contained by a folder.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_PARENT_FOLDER_NAME: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudParentFolderName", "sapAnalyticsCloudParentFolderName"
    )
    """
    Simple name of the SAP Analytics Cloud folder that directly contains this asset. Empty for a root-level folder and for a live model, neither of which is contained by a folder.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "sap_analytics_cloud_resource_id",
        "sap_analytics_cloud_object_id",
        "sap_analytics_cloud_repository_partition",
        "sap_analytics_cloud_workspace_id",
        "sap_analytics_cloud_workspace_name",
        "sap_analytics_cloud_parent_folder_qualified_name",
        "sap_analytics_cloud_parent_folder_name",
    ]

    @property
    def sap_analytics_cloud_resource_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_resource_id
        )

    @sap_analytics_cloud_resource_id.setter
    def sap_analytics_cloud_resource_id(
        self, sap_analytics_cloud_resource_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_resource_id = (
            sap_analytics_cloud_resource_id
        )

    @property
    def sap_analytics_cloud_object_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_object_id
        )

    @sap_analytics_cloud_object_id.setter
    def sap_analytics_cloud_object_id(
        self, sap_analytics_cloud_object_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_object_id = sap_analytics_cloud_object_id

    @property
    def sap_analytics_cloud_repository_partition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_repository_partition
        )

    @sap_analytics_cloud_repository_partition.setter
    def sap_analytics_cloud_repository_partition(
        self, sap_analytics_cloud_repository_partition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_repository_partition = (
            sap_analytics_cloud_repository_partition
        )

    @property
    def sap_analytics_cloud_workspace_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_workspace_id
        )

    @sap_analytics_cloud_workspace_id.setter
    def sap_analytics_cloud_workspace_id(
        self, sap_analytics_cloud_workspace_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_workspace_id = (
            sap_analytics_cloud_workspace_id
        )

    @property
    def sap_analytics_cloud_workspace_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_workspace_name
        )

    @sap_analytics_cloud_workspace_name.setter
    def sap_analytics_cloud_workspace_name(
        self, sap_analytics_cloud_workspace_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_workspace_name = (
            sap_analytics_cloud_workspace_name
        )

    @property
    def sap_analytics_cloud_parent_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_parent_folder_qualified_name
        )

    @sap_analytics_cloud_parent_folder_qualified_name.setter
    def sap_analytics_cloud_parent_folder_qualified_name(
        self, sap_analytics_cloud_parent_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_parent_folder_qualified_name = (
            sap_analytics_cloud_parent_folder_qualified_name
        )

    @property
    def sap_analytics_cloud_parent_folder_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_parent_folder_name
        )

    @sap_analytics_cloud_parent_folder_name.setter
    def sap_analytics_cloud_parent_folder_name(
        self, sap_analytics_cloud_parent_folder_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_parent_folder_name = (
            sap_analytics_cloud_parent_folder_name
        )

    class Attributes(SAP.Attributes):
        sap_analytics_cloud_resource_id: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_object_id: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_repository_partition: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_workspace_id: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_workspace_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_parent_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_parent_folder_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: SapAnalyticsCloud.Attributes = Field(
        default_factory=lambda: SapAnalyticsCloud.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
