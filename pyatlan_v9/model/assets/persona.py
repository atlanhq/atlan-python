# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Persona asset model for pyatlan_v9."""

from __future__ import annotations

from typing import Any, ClassVar, Set, Union
from warnings import warn

from msgspec import UNSET, UnsetType

from pyatlan.model.enums import (
    AuthPolicyCategory,
    AuthPolicyResourceCategory,
    AuthPolicyType,
    DataAction,
    PersonaDomainAction,
    PersonaGlossaryAction,
    PersonaMetadataAction,
)
from pyatlan_v9.model.conversion_utils import (
    build_attributes_kwargs,
    build_flat_kwargs,
    merge_relationships,
)
from pyatlan_v9.model.serde import Serde, get_serde
from pyatlan_v9.model.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .asset import Asset, AssetAttributes, AssetNested
from .auth_policy import AuthPolicy


@register_asset
class Persona(Asset):
    """Persona asset in Atlan — an access-control construct scoping
    visibility for users/groups across connections and glossaries."""

    PERSONA_GROUPS: ClassVar[Any] = None
    PERSONA_USERS: ClassVar[Any] = None
    ROLE_ID: ClassVar[Any] = None
    IS_ACCESS_CONTROL_ENABLED: ClassVar[Any] = None
    DENY_CUSTOM_METADATA_GUIDS: ClassVar[Any] = None

    type_name: Union[str, UnsetType] = "Persona"
    persona_groups: Union[Set[str], None, UnsetType] = UNSET
    persona_users: Union[Set[str], None, UnsetType] = UNSET
    role_id: Union[str, None, UnsetType] = UNSET
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

    @classmethod
    @init_guid
    def creator(cls, *, name: str) -> "Persona":
        validate_required_fields(["name"], [name])
        return cls(
            qualified_name=name,
            name=name,
            display_name=name,
            is_access_control_enabled=True,
            description="",
        )

    @classmethod
    def updater(
        cls, *, qualified_name: str, name: str, is_enabled: bool = True
    ) -> "Persona":
        validate_required_fields(
            ["name", "qualified_name", "is_enabled"],
            [name, qualified_name, is_enabled],
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
    ) -> "Persona":
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
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PersonaMetadataAction],
        connection_qualified_name: str,
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "actions", "resources"],
            [name, persona_id, policy_type, actions, resources],
        )
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.connection_qualified_name = connection_qualified_name
        policy.policy_resources = resources
        policy.policy_resource_category = AuthPolicyResourceCategory.CUSTOM.value
        policy.policy_service_name = "atlas"
        policy.policy_sub_category = "metadata"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    def create_data_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        connection_qualified_name: str,
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "resources"],
            [name, persona_id, policy_type, resources],
        )
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {DataAction.SELECT.value}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.connection_qualified_name = connection_qualified_name
        policy.policy_resources = resources
        policy.policy_resources.add("entity-type:*")
        policy.policy_resource_category = AuthPolicyResourceCategory.ENTITY.value
        policy.policy_service_name = "heka"
        policy.policy_sub_category = "data"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    def create_glossary_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PersonaGlossaryAction],
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "policy_type", "actions", "resources"],
            [name, persona_id, policy_type, actions, resources],
        )
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = policy_type
        policy.policy_resources = resources
        policy.policy_resource_category = AuthPolicyResourceCategory.CUSTOM.value
        policy.policy_service_name = "atlas"
        policy.policy_sub_category = "glossary"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    @classmethod
    def create_domain_policy(
        cls,
        *,
        name: str,
        persona_id: str,
        actions: Set[PersonaDomainAction],
        resources: Set[str],
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "persona_id", "actions", "resources"],
            [name, persona_id, actions, resources],
        )
        policy = AuthPolicy._create(name=name)
        policy.policy_actions = {x.value for x in actions}
        policy.policy_category = AuthPolicyCategory.PERSONA.value
        policy.policy_type = AuthPolicyType.ALLOW
        policy.policy_resources = resources
        policy.policy_resource_category = AuthPolicyResourceCategory.CUSTOM.value
        policy.policy_service_name = "atlas"
        policy.policy_sub_category = "domain"
        persona = Persona()
        persona.guid = persona_id
        policy.access_control = persona
        return policy

    def trim_to_required(self) -> "Persona":
        return Persona.updater(qualified_name=self.qualified_name, name=self.name)

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        if serde is None:
            serde = get_serde()
        if nested:
            return _persona_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "Persona":
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _persona_from_nested_bytes(json_data, serde)


# ---------------------------------------------------------------------------
# Deferred field descriptor initialization
# ---------------------------------------------------------------------------
from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField

Persona.PERSONA_GROUPS = KeywordField("personaGroups", "personaGroups")
Persona.PERSONA_USERS = KeywordField("personaUsers", "personaUsers")
Persona.ROLE_ID = KeywordField("roleId", "roleId")
Persona.IS_ACCESS_CONTROL_ENABLED = BooleanField(
    "isAccessControlEnabled", "isAccessControlEnabled"
)
Persona.DENY_CUSTOM_METADATA_GUIDS = KeywordField(
    "denyCustomMetadataGuids", "denyCustomMetadataGuids"
)


# =============================================================================
# NESTED FORMAT CLASSES
# =============================================================================


class PersonaAttributes(AssetAttributes):
    """Persona-specific nested attributes."""

    persona_groups: Union[Set[str], None, UnsetType] = UNSET
    persona_users: Union[Set[str], None, UnsetType] = UNSET
    role_id: Union[str, None, UnsetType] = UNSET
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


class PersonaNested(AssetNested):
    """Persona entity in nested API format."""

    attributes: Union[PersonaAttributes, UnsetType] = UNSET


# =============================================================================
# CONVERSION FUNCTIONS
# =============================================================================


def _persona_to_nested(persona: Persona) -> PersonaNested:
    attrs_kwargs = build_attributes_kwargs(persona, PersonaAttributes)
    attrs = PersonaAttributes(**attrs_kwargs)
    return PersonaNested(
        guid=persona.guid,
        type_name=persona.type_name,
        status=persona.status,
        version=persona.version,
        create_time=persona.create_time,
        update_time=persona.update_time,
        created_by=persona.created_by,
        updated_by=persona.updated_by,
        classifications=persona.classifications,
        classification_names=persona.classification_names,
        meanings=persona.meanings,
        labels=persona.labels,
        business_attributes=persona.business_attributes,
        custom_attributes=persona.custom_attributes,
        pending_tasks=persona.pending_tasks,
        proxy=persona.proxy,
        is_incomplete=persona.is_incomplete,
        provenance_type=persona.provenance_type,
        home_id=persona.home_id,
        attributes=attrs,
    )


def _persona_from_nested(nested: PersonaNested) -> Persona:
    attrs = nested.attributes if nested.attributes is not UNSET else PersonaAttributes()
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        [],
        object,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, AssetNested, PersonaAttributes
    )
    return Persona(**kwargs)


def _persona_to_nested_bytes(persona: Persona, serde: Serde) -> bytes:
    return serde.encode(_persona_to_nested(persona))


def _persona_from_nested_bytes(data: bytes, serde: Serde) -> Persona:
    nested = serde.decode(data, PersonaNested)
    return _persona_from_nested(nested)
