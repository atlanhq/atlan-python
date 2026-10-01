# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .core.sap_analytics_cloud import SapAnalyticsCloud


class SapAnalyticsCloudFolder(SapAnalyticsCloud):
    """Description"""

    type_name: str = Field(default="SapAnalyticsCloudFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapAnalyticsCloudFolder":
            raise ValueError("must be SapAnalyticsCloudFolder")
        return v

    def __setattr__(self, name, value):
        if name in SapAnalyticsCloudFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ANALYTICS_CLOUD_PARENT_FOLDER: ClassVar[RelationField] = RelationField(
        "sapAnalyticsCloudParentFolder"
    )
    """
    TBC
    """
    SAP_ANALYTICS_CLOUD_MODELS: ClassVar[RelationField] = RelationField(
        "sapAnalyticsCloudModels"
    )
    """
    TBC
    """
    SAP_ANALYTICS_CLOUD_STORIES: ClassVar[RelationField] = RelationField(
        "sapAnalyticsCloudStories"
    )
    """
    TBC
    """
    SAP_ANALYTICS_CLOUD_SUB_FOLDERS: ClassVar[RelationField] = RelationField(
        "sapAnalyticsCloudSubFolders"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_analytics_cloud_parent_folder",
        "sap_analytics_cloud_models",
        "sap_analytics_cloud_stories",
        "sap_analytics_cloud_sub_folders",
    ]

    @property
    def sap_analytics_cloud_parent_folder(self) -> Optional[SapAnalyticsCloudFolder]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_parent_folder
        )

    @sap_analytics_cloud_parent_folder.setter
    def sap_analytics_cloud_parent_folder(
        self, sap_analytics_cloud_parent_folder: Optional[SapAnalyticsCloudFolder]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_parent_folder = (
            sap_analytics_cloud_parent_folder
        )

    @property
    def sap_analytics_cloud_models(self) -> Optional[List[SapAnalyticsCloudModel]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_models
        )

    @sap_analytics_cloud_models.setter
    def sap_analytics_cloud_models(
        self, sap_analytics_cloud_models: Optional[List[SapAnalyticsCloudModel]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_models = sap_analytics_cloud_models

    @property
    def sap_analytics_cloud_stories(self) -> Optional[List[SapAnalyticsCloudStory]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_stories
        )

    @sap_analytics_cloud_stories.setter
    def sap_analytics_cloud_stories(
        self, sap_analytics_cloud_stories: Optional[List[SapAnalyticsCloudStory]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_stories = sap_analytics_cloud_stories

    @property
    def sap_analytics_cloud_sub_folders(
        self,
    ) -> Optional[List[SapAnalyticsCloudFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_sub_folders
        )

    @sap_analytics_cloud_sub_folders.setter
    def sap_analytics_cloud_sub_folders(
        self, sap_analytics_cloud_sub_folders: Optional[List[SapAnalyticsCloudFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_sub_folders = (
            sap_analytics_cloud_sub_folders
        )

    class Attributes(SapAnalyticsCloud.Attributes):
        sap_analytics_cloud_parent_folder: Optional[SapAnalyticsCloudFolder] = Field(
            default=None, description=""
        )  # relationship
        sap_analytics_cloud_models: Optional[List[SapAnalyticsCloudModel]] = Field(
            default=None, description=""
        )  # relationship
        sap_analytics_cloud_stories: Optional[List[SapAnalyticsCloudStory]] = Field(
            default=None, description=""
        )  # relationship
        sap_analytics_cloud_sub_folders: Optional[List[SapAnalyticsCloudFolder]] = (
            Field(default=None, description="")
        )  # relationship

    attributes: SapAnalyticsCloudFolder.Attributes = Field(
        default_factory=lambda: SapAnalyticsCloudFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_analytics_cloud_model import SapAnalyticsCloudModel  # noqa: E402, F401
from .sap_analytics_cloud_story import SapAnalyticsCloudStory  # noqa: E402, F401

SapAnalyticsCloudFolder.Attributes.update_forward_refs()
