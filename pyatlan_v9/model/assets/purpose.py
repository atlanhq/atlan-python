# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Purpose asset model for pyatlan_v9."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Set, Union
from warnings import warn

import msgspec
from msgspec import UNSET, UnsetType

from pyatlan.model.enums import (
    AuthPolicyCategory,
    AuthPolicyResourceCategory,
    AuthPolicyType,
    DataAction,
    PurposeMetadataAction,
)
from pyatlan_v9.model.conversion_utils import (
    build_attributes_kwargs,
    build_flat_kwargs,
    merge_relationships,
)
from pyatlan_v9.model.core import AtlanTagName
from pyatlan_v9.model.serde import Serde, get_serde
from pyatlan_v9.model.structs import SourceTagAttachment
from pyatlan_v9.model.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .asset import Asset, AssetAttributes, AssetNested
from .auth_policy import AuthPolicy

if TYPE_CHECKING:
    from pyatlan_v9.client.atlan import AtlanClient


class PurposeClassification(msgspec.Struct, kw_only=True, rename="camel"):
    """Classification view used by Purpose to retain source-tag attachments."""

    type_name: Any = None
    source_tag_attachments: list[SourceTagAttachment] = msgspec.field(
        default_factory=list
    )
    entity_status: Union[str, None] = None


@register_asset
class Purpose(Asset):
    """Purpose asset in Atlan."""

    type_name: Union[str, UnsetType] = "Purpose"

    is_access_control_enabled: Union[bool, None, UnsetType] = UNSET
    deny_custom_metadata_guids: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_filters: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_types: Union[Set[str], None, UnsetType] = UNSET
    deny_sidebar_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_navigation_pages: Union[Set[str], None, UnsetType] = UNSET
    default_navigation: Union[str, None, UnsetType] = UNSET
    display_preferences: Union[Set[str], None, UnsetType] = UNSET
    channel_link: Union[str, None, UnsetType] = UNSET
    deny_asset_metadata_types: Union[Set[str], None, UnsetType] = UNSET
    policies: Union[list[AuthPolicy], None, UnsetType] = UNSET
    purpose_classifications: Union[list[Any], None, UnsetType] = UNSET
    classifications: Union[list[PurposeClassification], None, UnsetType] = UNSET

    @property
    def purpose_atlan_tags(self) -> Union[list[AtlanTagName], None]:
        """Expose purpose classifications as AtlanTagName objects for parity."""
        if self.purpose_classifications in (UNSET, None):
            return None
        return [
            tag if isinstance(tag, AtlanTagName) else AtlanTagName(str(tag))
            for tag in self.purpose_classifications
        ]

    @purpose_atlan_tags.setter
    def purpose_atlan_tags(self, value: Union[list[AtlanTagName], None]) -> None:
        if value is None:
            self.purpose_classifications = None
        else:
            self.purpose_classifications = [str(tag) for tag in value]

    @classmethod
    @init_guid
    def creator(cls, *, name: str, atlan_tags: list[AtlanTagName]) -> "Purpose":
        """Create a new Purpose asset."""
        validate_required_fields(["name", "atlan_tags"], [name, atlan_tags])
        return cls(
            name=name,
            qualified_name=name,
            display_name=name,
            description="",
            is_access_control_enabled=True,
            purpose_classifications=[str(tag) for tag in atlan_tags],
        )

    @classmethod
    def updater(
        cls, *, qualified_name: str, name: str, is_enabled: bool = True
    ) -> "Purpose":
        """Create a Purpose asset for update operations."""
        validate_required_fields(
            ["qualified_name", "name", "is_enabled"],
            [qualified_name, name, is_enabled],
        )
        return cls(
            qualified_name=qualified_name,
            name=name,
            is_access_control_enabled=is_enabled,
        )

    @classmethod
    def create_for_modification(
        cls,
        qualified_name: str = "",
        name: str = "",
        is_enabled: bool = True,
    ) -> "Purpose":
        warn(
            (
                "This method is deprecated, please use 'updater' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.updater(
            qualified_name=qualified_name, name=name, is_enabled=is_enabled
        )

    @classmethod
    def create_metadata_policy(
        cls,
        *,
        client: "AtlanClient",
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PurposeMetadataAction],
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["client", "name", "purpose_id", "policy_type", "actions"],
            [client, name, purpose_id, policy_type, actions],
        )
        target_found = False
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PURPOSE.value
        policy.policy_type = policy_type
        policy.policy_resource_category = AuthPolicyResourceCategory.TAG.value
        policy.policy_service_name = "atlas_tag"
        policy.policy_sub_category = "metadata"
        purpose = Purpose()
        purpose.guid = purpose_id
        policy.access_control = purpose
        if all_users:
            target_found = True
            policy.policy_groups = {"public"}
        else:
            if policy_groups:
                for group_name in policy_groups:
                    if not client.group_cache.get_id_for_name(group_name):
                        raise ValueError(
                            f"Provided group name {group_name} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                for username in policy_users:
                    if not client.user_cache.get_id_for_name(username):
                        raise ValueError(
                            f"Provided username {username} was not found in Atlan."
                        )
                target_found = True
                policy.policy_users = policy_users
            else:
                policy.policy_users = None
        if target_found:
            return policy
        else:
            raise ValueError("No user or group specified for the policy.")

    @classmethod
    def create_data_policy(
        cls,
        *,
        client: "AtlanClient",
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["client", "name", "purpose_id", "policy_type"],
            [client, name, purpose_id, policy_type],
        )
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {DataAction.SELECT.value}
        policy.policy_category = AuthPolicyCategory.PURPOSE.value
        policy.policy_type = policy_type
        policy.policy_resource_category = AuthPolicyResourceCategory.TAG.value
        policy.policy_service_name = "atlas_tag"
        policy.policy_sub_category = "data"
        purpose = Purpose()
        purpose.guid = purpose_id
        policy.access_control = purpose
        if all_users:
            target_found = True
            policy.policy_groups = {"public"}
        else:
            if policy_groups:
                for group_name in policy_groups:
                    if not client.group_cache.get_id_for_name(group_name):
                        raise ValueError(
                            f"Provided group name {group_name} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                for username in policy_users:
                    if not client.user_cache.get_id_for_name(username):
                        raise ValueError(
                            f"Provided username {username} was not found in Atlan."
                        )
                target_found = True
                policy.policy_users = policy_users
            else:
                policy.policy_users = None
        if target_found:
            return policy
        else:
            raise ValueError("No user or group specified for the policy.")

    def trim_to_required(self) -> "Purpose":
        """Return only required fields for updates."""
        return Purpose.updater(qualified_name=self.qualified_name, name=self.name)

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """Serialize the Purpose to JSON."""
        if serde is None:
            serde = get_serde()
        if nested:
            return _purpose_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "Purpose":
        """Deserialize a Purpose from nested API JSON."""
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _purpose_from_nested_bytes(json_data, serde)


class PurposeAttributes(AssetAttributes):
    """Purpose-specific nested attributes."""

    is_access_control_enabled: Union[bool, None, UnsetType] = UNSET
    deny_custom_metadata_guids: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_filters: Union[Set[str], None, UnsetType] = UNSET
    deny_asset_types: Union[Set[str], None, UnsetType] = UNSET
    deny_sidebar_tabs: Union[Set[str], None, UnsetType] = UNSET
    deny_navigation_pages: Union[Set[str], None, UnsetType] = UNSET
    default_navigation: Union[str, None, UnsetType] = UNSET
    display_preferences: Union[Set[str], None, UnsetType] = UNSET
    channel_link: Union[str, None, UnsetType] = UNSET
    deny_asset_metadata_types: Union[Set[str], None, UnsetType] = UNSET
    purpose_classifications: Union[list[Any], None, UnsetType] = UNSET


class PurposeNested(AssetNested):
    """Purpose entity in nested API format."""

    attributes: Union[PurposeAttributes, UnsetType] = UNSET


def _purpose_to_nested(purpose: Purpose) -> PurposeNested:
    attrs_kwargs = build_attributes_kwargs(purpose, PurposeAttributes)
    attrs = PurposeAttributes(**attrs_kwargs)
    return PurposeNested(
        guid=purpose.guid,
        type_name=purpose.type_name,
        status=purpose.status,
        version=purpose.version,
        create_time=purpose.create_time,
        update_time=purpose.update_time,
        created_by=purpose.created_by,
        updated_by=purpose.updated_by,
        classifications=purpose.classifications,
        classification_names=purpose.classification_names,
        meanings=purpose.meanings,
        labels=purpose.labels,
        business_attributes=purpose.business_attributes,
        custom_attributes=purpose.custom_attributes,
        pending_tasks=purpose.pending_tasks,
        proxy=purpose.proxy,
        is_incomplete=purpose.is_incomplete,
        provenance_type=purpose.provenance_type,
        home_id=purpose.home_id,
        attributes=attrs,
    )


def _purpose_from_nested(nested: PurposeNested) -> Purpose:
    attrs = nested.attributes if nested.attributes is not UNSET else PurposeAttributes()
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        [],
        object,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, AssetNested, PurposeAttributes
    )
    purpose = Purpose(**kwargs)
    if (
        purpose.classifications is not UNSET
        and purpose.classifications is not None
        and purpose.classifications
        and isinstance(purpose.classifications[0], dict)
    ):
        purpose.classifications = [
            msgspec.convert(classification, type=PurposeClassification)
            for classification in purpose.classifications
        ]
    return purpose


def _purpose_to_nested_bytes(purpose: Purpose, serde: Serde) -> bytes:
    return serde.encode(_purpose_to_nested(purpose))


def _purpose_from_nested_bytes(data: bytes, serde: Serde) -> Purpose:
    nested = serde.decode(data, PurposeNested)
    return _purpose_from_nested(nested)
