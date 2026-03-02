# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""AccessControl asset model for pyatlan_v9."""

from __future__ import annotations

from typing import Any, ClassVar, Optional, Set, Union

from msgspec import UNSET, UnsetType

from pyatlan_v9.model.conversion_utils import (
    build_attributes_kwargs,
    build_flat_kwargs,
    merge_relationships,
)
from pyatlan_v9.model.serde import Serde, get_serde
from pyatlan_v9.model.transform import register_asset
from pyatlan_v9.utils import validate_required_fields

from .asset import Asset, AssetAttributes, AssetNested
from .auth_policy import AuthPolicy


@register_asset
class AccessControl(Asset):
    """AccessControl asset — base type for Persona and Purpose access policies."""

    IS_ACCESS_CONTROL_ENABLED: ClassVar[Any] = None
    DENY_SIDEBAR_TABS: ClassVar[Any] = None
    DENY_CUSTOM_METADATA_GUIDS: ClassVar[Any] = None
    DENY_ASSET_METADATA_TYPES: ClassVar[Any] = None
    DENY_ASSET_TABS: ClassVar[Any] = None
    DENY_ASSET_FILTERS: ClassVar[Any] = None
    CHANNEL_LINK: ClassVar[Any] = None
    DENY_ASSET_TYPES: ClassVar[Any] = None
    DENY_NAVIGATION_PAGES: ClassVar[Any] = None
    DEFAULT_NAVIGATION: ClassVar[Any] = None
    DISPLAY_PREFERENCES: ClassVar[Any] = None
    POLICIES: ClassVar[Any] = None

    type_name: Union[str, UnsetType] = "AccessControl"
    is_access_control_enabled: Union[bool, None, UnsetType] = UNSET
    deny_sidebar_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_custom_metadata_guids: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_metadata_types: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_filters: Union[Set[str], None, UnsetType] = UNSET
    channel_link: Union[str, None, UnsetType] = UNSET
    deny_asset_types: Union[Set[str], None, UnsetType] = UNSET
    deny_navigation_pages: Union[Set[str], None, UnsetType] = UNSET
    default_navigation: Union[str, None, UnsetType] = UNSET
    display_preferences: Union[Set[str], None, UnsetType] = UNSET
    policies: Union[list[AuthPolicy], None, UnsetType] = UNSET

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        if serde is None:
            serde = get_serde()
        if nested:
            return _access_control_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "AccessControl":
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _access_control_from_nested_bytes(json_data, serde)


# ---------------------------------------------------------------------------
# Deferred field descriptor initialization
# ---------------------------------------------------------------------------
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    RelationField,
    TextField,
)

AccessControl.IS_ACCESS_CONTROL_ENABLED = BooleanField(
    "isAccessControlEnabled", "isAccessControlEnabled"
)
AccessControl.DENY_SIDEBAR_TABS = KeywordField("denySidebarTabs", "denySidebarTabs")
AccessControl.DENY_CUSTOM_METADATA_GUIDS = KeywordField(
    "denyCustomMetadataGuids", "denyCustomMetadataGuids"
)
AccessControl.DENY_ASSET_METADATA_TYPES = KeywordField(
    "denyAssetMetadataTypes", "denyAssetMetadataTypes"
)
AccessControl.DENY_ASSET_TABS = KeywordField("denyAssetTabs", "denyAssetTabs")
AccessControl.DENY_ASSET_FILTERS = TextField("denyAssetFilters", "denyAssetFilters")
AccessControl.CHANNEL_LINK = TextField("channelLink", "channelLink")
AccessControl.DENY_ASSET_TYPES = TextField("denyAssetTypes", "denyAssetTypes")
AccessControl.DENY_NAVIGATION_PAGES = TextField(
    "denyNavigationPages", "denyNavigationPages"
)
AccessControl.DEFAULT_NAVIGATION = TextField("defaultNavigation", "defaultNavigation")
AccessControl.DISPLAY_PREFERENCES = KeywordField(
    "displayPreferences", "displayPreferences"
)
AccessControl.POLICIES = RelationField("policies")


# =============================================================================
# NESTED FORMAT CLASSES
# =============================================================================


class AccessControlAttributes(AssetAttributes):
    is_access_control_enabled: Union[bool, None, UnsetType] = UNSET
    deny_sidebar_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_custom_metadata_guids: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_metadata_types: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_filters: Union[Set[str], None, UnsetType] = UNSET
    channel_link: Union[str, None, UnsetType] = UNSET
    deny_asset_types: Union[Set[str], None, UnsetType] = UNSET
    deny_navigation_pages: Union[Set[str], None, UnsetType] = UNSET
    default_navigation: Union[str, None, UnsetType] = UNSET
    display_preferences: Union[Set[str], None, UnsetType] = UNSET


class AccessControlNested(AssetNested):
    attributes: Union[AccessControlAttributes, UnsetType] = UNSET


def _access_control_to_nested(ac: AccessControl) -> AccessControlNested:
    attrs_kwargs = build_attributes_kwargs(ac, AccessControlAttributes)
    attrs = AccessControlAttributes(**attrs_kwargs)
    return AccessControlNested(
        guid=ac.guid,
        type_name=ac.type_name,
        status=ac.status,
        version=ac.version,
        create_time=ac.create_time,
        update_time=ac.update_time,
        created_by=ac.created_by,
        updated_by=ac.updated_by,
        classifications=ac.classifications,
        classification_names=ac.classification_names,
        meanings=ac.meanings,
        labels=ac.labels,
        business_attributes=ac.business_attributes,
        custom_attributes=ac.custom_attributes,
        pending_tasks=ac.pending_tasks,
        proxy=ac.proxy,
        is_incomplete=ac.is_incomplete,
        provenance_type=ac.provenance_type,
        home_id=ac.home_id,
        attributes=attrs,
    )


def _access_control_from_nested(nested: AccessControlNested) -> AccessControl:
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else AccessControlAttributes()
    )
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        [],
        object,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, AssetNested, AccessControlAttributes
    )
    return AccessControl(**kwargs)


def _access_control_to_nested_bytes(ac: AccessControl, serde: Serde) -> bytes:
    return serde.encode(_access_control_to_nested(ac))


def _access_control_from_nested_bytes(data: bytes, serde: Serde) -> AccessControl:
    nested = serde.decode(data, AccessControlNested)
    return _access_control_from_nested(nested)
