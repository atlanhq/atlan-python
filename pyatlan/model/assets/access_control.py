# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .asset import Asset


class AccessControl(Asset, type_name="AccessControl"):
    """Description"""

    type_name: str = Field(default="AccessControl", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AccessControl":
            raise ValueError("must be AccessControl")
        return v

    def __setattr__(self, name, value):
        if name in AccessControl._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    IS_ACCESS_CONTROL_ENABLED: ClassVar[BooleanField] = BooleanField(
        "isAccessControlEnabled", "isAccessControlEnabled"
    )
    """
    TBC
    """
    DENY_CUSTOM_METADATA_GUIDS: ClassVar[KeywordField] = KeywordField(
        "denyCustomMetadataGuids", "denyCustomMetadataGuids"
    )
    """
    TBC
    """
    DENY_ASSET_TABS: ClassVar[KeywordField] = KeywordField(
        "denyAssetTabs", "denyAssetTabs"
    )
    """
    TBC
    """
    DENY_ASSET_FILTERS: ClassVar[KeywordField] = KeywordField(
        "denyAssetFilters", "denyAssetFilters"
    )
    """
    TBC
    """
    CHANNEL_LINK: ClassVar[KeywordField] = KeywordField("channelLink", "channelLink")
    """
    TBC
    """
    DENY_ASSET_TYPES: ClassVar[KeywordField] = KeywordField(
        "denyAssetTypes", "denyAssetTypes"
    )
    """
    TBC
    """
    DENY_NAVIGATION_PAGES: ClassVar[KeywordField] = KeywordField(
        "denyNavigationPages", "denyNavigationPages"
    )
    """
    TBC
    """
    DEFAULT_NAVIGATION: ClassVar[KeywordField] = KeywordField(
        "defaultNavigation", "defaultNavigation"
    )
    """
    TBC
    """
    DISPLAY_PREFERENCES: ClassVar[KeywordField] = KeywordField(
        "displayPreferences", "displayPreferences"
    )
    """
    TBC
    """

    POLICIES: ClassVar[RelationField] = RelationField("policies")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "is_access_control_enabled",
        "deny_custom_metadata_guids",
        "deny_asset_tabs",
        "deny_asset_filters",
        "channel_link",
        "deny_asset_types",
        "deny_navigation_pages",
        "default_navigation",
        "display_preferences",
        "policies",
    ]

    @property
    def is_access_control_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_access_control_enabled
        )

    @is_access_control_enabled.setter
    def is_access_control_enabled(self, is_access_control_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_access_control_enabled = is_access_control_enabled

    @property
    def deny_custom_metadata_guids(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.deny_custom_metadata_guids
        )

    @deny_custom_metadata_guids.setter
    def deny_custom_metadata_guids(
        self, deny_custom_metadata_guids: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_custom_metadata_guids = deny_custom_metadata_guids

    @property
    def deny_asset_tabs(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.deny_asset_tabs

    @deny_asset_tabs.setter
    def deny_asset_tabs(self, deny_asset_tabs: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_asset_tabs = deny_asset_tabs

    @property
    def deny_asset_filters(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.deny_asset_filters

    @deny_asset_filters.setter
    def deny_asset_filters(self, deny_asset_filters: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_asset_filters = deny_asset_filters

    @property
    def channel_link(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.channel_link

    @channel_link.setter
    def channel_link(self, channel_link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.channel_link = channel_link

    @property
    def deny_asset_types(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.deny_asset_types

    @deny_asset_types.setter
    def deny_asset_types(self, deny_asset_types: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_asset_types = deny_asset_types

    @property
    def deny_navigation_pages(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.deny_navigation_pages
        )

    @deny_navigation_pages.setter
    def deny_navigation_pages(self, deny_navigation_pages: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_navigation_pages = deny_navigation_pages

    @property
    def default_navigation(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.default_navigation

    @default_navigation.setter
    def default_navigation(self, default_navigation: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_navigation = default_navigation

    @property
    def display_preferences(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.display_preferences

    @display_preferences.setter
    def display_preferences(self, display_preferences: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.display_preferences = display_preferences

    @property
    def policies(self) -> Optional[List[AuthPolicy]]:
        return None if self.attributes is None else self.attributes.policies

    @policies.setter
    def policies(self, policies: Optional[List[AuthPolicy]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policies = policies

    class Attributes(Asset.Attributes):
        is_access_control_enabled: Optional[bool] = Field(default=None, description="")
        deny_custom_metadata_guids: Optional[Set[str]] = Field(
            default=None, description=""
        )
        deny_asset_tabs: Optional[Set[str]] = Field(default=None, description="")
        deny_asset_filters: Optional[Set[str]] = Field(default=None, description="")
        channel_link: Optional[str] = Field(default=None, description="")
        deny_asset_types: Optional[Set[str]] = Field(default=None, description="")
        deny_navigation_pages: Optional[Set[str]] = Field(default=None, description="")
        default_navigation: Optional[str] = Field(default=None, description="")
        display_preferences: Optional[Set[str]] = Field(default=None, description="")
        policies: Optional[List[AuthPolicy]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AccessControl.Attributes = Field(
        default_factory=lambda: AccessControl.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .auth_policy import AuthPolicy  # noqa
