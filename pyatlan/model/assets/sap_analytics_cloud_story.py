# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .core.sap_analytics_cloud import SapAnalyticsCloud


class SapAnalyticsCloudStory(SapAnalyticsCloud):
    """Description"""

    type_name: str = Field(default="SapAnalyticsCloudStory", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapAnalyticsCloudStory":
            raise ValueError("must be SapAnalyticsCloudStory")
        return v

    def __setattr__(self, name, value):
        if name in SapAnalyticsCloudStory._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ANALYTICS_CLOUD_STORY_KIND: ClassVar[KeywordField] = KeywordField(
        "sapAnalyticsCloudStoryKind", "sapAnalyticsCloudStoryKind"
    )
    """
    Subtype of this story as reported by the source, such as COMPOSITE for a story that embeds other stories or TEMPLATE for a story used as the starting point for new ones. Empty for an ordinary story.
    """  # noqa: E501
    SAP_ANALYTICS_CLOUD_IS_SAMPLE: ClassVar[BooleanField] = BooleanField(
        "sapAnalyticsCloudIsSample", "sapAnalyticsCloudIsSample"
    )
    """
    Whether this story is one of the samples shipped with SAP Analytics Cloud rather than tenant content.
    """

    SAP_ANALYTICS_CLOUD_FOLDER: ClassVar[RelationField] = RelationField(
        "sapAnalyticsCloudFolder"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_analytics_cloud_story_kind",
        "sap_analytics_cloud_is_sample",
        "sap_analytics_cloud_folder",
    ]

    @property
    def sap_analytics_cloud_story_kind(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_story_kind
        )

    @sap_analytics_cloud_story_kind.setter
    def sap_analytics_cloud_story_kind(
        self, sap_analytics_cloud_story_kind: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_story_kind = sap_analytics_cloud_story_kind

    @property
    def sap_analytics_cloud_is_sample(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_analytics_cloud_is_sample
        )

    @sap_analytics_cloud_is_sample.setter
    def sap_analytics_cloud_is_sample(
        self, sap_analytics_cloud_is_sample: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_analytics_cloud_is_sample = sap_analytics_cloud_is_sample

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
        sap_analytics_cloud_story_kind: Optional[str] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_is_sample: Optional[bool] = Field(
            default=None, description=""
        )
        sap_analytics_cloud_folder: Optional[SapAnalyticsCloudFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapAnalyticsCloudStory.Attributes = Field(
        default_factory=lambda: SapAnalyticsCloudStory.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sap_analytics_cloud_folder import SapAnalyticsCloudFolder  # noqa: E402, F401

SapAnalyticsCloudStory.Attributes.update_forward_refs()
