# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""AuthPolicy asset model for pyatlan_v9."""

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
from pyatlan_v9.utils import init_guid, validate_required_fields

from .asset import Asset, AssetAttributes, AssetNested


@register_asset
class AuthPolicy(Asset):
    """AuthPolicy asset — defines access policies for Persona and Purpose."""

    POLICY_FILTER_CRITERIA: ClassVar[Any] = None
    POLICY_TYPE: ClassVar[Any] = None
    POLICY_SERVICE_NAME: ClassVar[Any] = None
    POLICY_CATEGORY: ClassVar[Any] = None
    POLICY_SUB_CATEGORY: ClassVar[Any] = None
    POLICY_USERS: ClassVar[Any] = None
    POLICY_GROUPS: ClassVar[Any] = None
    POLICY_ROLES: ClassVar[Any] = None
    POLICY_ACTIONS: ClassVar[Any] = None
    POLICY_RESOURCES: ClassVar[Any] = None
    POLICY_RESOURCE_CATEGORY: ClassVar[Any] = None
    POLICY_PRIORITY: ClassVar[Any] = None
    IS_POLICY_ENABLED: ClassVar[Any] = None
    POLICY_MASK_TYPE: ClassVar[Any] = None
    POLICY_VALIDITY_SCHEDULE: ClassVar[Any] = None
    POLICY_RESOURCE_SIGNATURE: ClassVar[Any] = None
    POLICY_DELEGATE_ADMIN: ClassVar[Any] = None
    POLICY_CONDITIONS: ClassVar[Any] = None
    ACCESS_CONTROL: ClassVar[Any] = None

    @classmethod
    @init_guid
    def _create(cls, *, name: str) -> "AuthPolicy":
        validate_required_fields(["name"], [name])
        return cls(qualified_name=name, name=name, display_name="")

    type_name: Union[str, UnsetType] = "AuthPolicy"
    policy_filter_criteria: Union[str, None, UnsetType] = UNSET
    policy_type: Union[str, None, UnsetType] = UNSET
    policy_service_name: Union[str, None, UnsetType] = UNSET
    policy_category: Union[str, None, UnsetType] = UNSET
    policy_sub_category: Union[str, None, UnsetType] = UNSET
    policy_users: Union[Set[str], None, UnsetType] = UNSET
    policy_groups: Union[Set[str], None, UnsetType] = UNSET
    policy_roles: Union[Set[str], None, UnsetType] = UNSET
    policy_actions: Union[Set[str], None, UnsetType] = UNSET
    policy_resources: Union[Set[str], None, UnsetType] = UNSET
    policy_resource_category: Union[str, None, UnsetType] = UNSET
    policy_priority: Union[int, None, UnsetType] = UNSET
    is_policy_enabled: Union[bool, None, UnsetType] = UNSET
    policy_mask_type: Union[str, None, UnsetType] = UNSET
    policy_validity_schedule: Union[list[Any], None, UnsetType] = UNSET
    policy_resource_signature: Union[str, None, UnsetType] = UNSET
    policy_delegate_admin: Union[bool, None, UnsetType] = UNSET
    policy_conditions: Union[list[Any], None, UnsetType] = UNSET
    access_control: Union[Any, None, UnsetType] = UNSET
    connection_qualified_name: Union[str, None, UnsetType] = UNSET

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        if serde is None:
            serde = get_serde()
        if nested:
            return _auth_policy_to_nested_bytes(self, serde).decode("utf-8")
        return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "AuthPolicy":
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _auth_policy_from_nested_bytes(json_data, serde)


# ---------------------------------------------------------------------------
# Deferred field descriptor initialization
# ---------------------------------------------------------------------------
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

AuthPolicy.POLICY_FILTER_CRITERIA = TextField(
    "policyFilterCriteria", "policyFilterCriteria"
)
AuthPolicy.POLICY_TYPE = KeywordField("policyType", "policyType")
AuthPolicy.POLICY_SERVICE_NAME = KeywordField("policyServiceName", "policyServiceName")
AuthPolicy.POLICY_CATEGORY = KeywordField("policyCategory", "policyCategory")
AuthPolicy.POLICY_SUB_CATEGORY = KeywordField("policySubCategory", "policySubCategory")
AuthPolicy.POLICY_USERS = KeywordField("policyUsers", "policyUsers")
AuthPolicy.POLICY_GROUPS = KeywordField("policyGroups", "policyGroups")
AuthPolicy.POLICY_ROLES = KeywordField("policyRoles", "policyRoles")
AuthPolicy.POLICY_ACTIONS = KeywordField("policyActions", "policyActions")
AuthPolicy.POLICY_RESOURCES = KeywordField("policyResources", "policyResources")
AuthPolicy.POLICY_RESOURCE_CATEGORY = KeywordField(
    "policyResourceCategory", "policyResourceCategory"
)
AuthPolicy.POLICY_PRIORITY = NumericField("policyPriority", "policyPriority")
AuthPolicy.IS_POLICY_ENABLED = BooleanField("isPolicyEnabled", "isPolicyEnabled")
AuthPolicy.POLICY_MASK_TYPE = KeywordField("policyMaskType", "policyMaskType")
AuthPolicy.POLICY_VALIDITY_SCHEDULE = KeywordField(
    "policyValiditySchedule", "policyValiditySchedule"
)
AuthPolicy.POLICY_RESOURCE_SIGNATURE = KeywordField(
    "policyResourceSignature", "policyResourceSignature"
)
AuthPolicy.POLICY_DELEGATE_ADMIN = BooleanField(
    "policyDelegateAdmin", "policyDelegateAdmin"
)
AuthPolicy.POLICY_CONDITIONS = KeywordField("policyConditions", "policyConditions")
AuthPolicy.ACCESS_CONTROL = RelationField("accessControl")


# =============================================================================
# NESTED FORMAT CLASSES
# =============================================================================


class AuthPolicyAttributes(AssetAttributes):
    policy_filter_criteria: Union[str, None, UnsetType] = UNSET
    policy_type: Union[str, None, UnsetType] = UNSET
    policy_service_name: Union[str, None, UnsetType] = UNSET
    policy_category: Union[str, None, UnsetType] = UNSET
    policy_sub_category: Union[str, None, UnsetType] = UNSET
    policy_users: Union[Set[str], None, UnsetType] = UNSET
    policy_groups: Union[Set[str], None, UnsetType] = UNSET
    policy_roles: Union[Set[str], None, UnsetType] = UNSET
    policy_actions: Union[Set[str], None, UnsetType] = UNSET
    policy_resources: Union[Set[str], None, UnsetType] = UNSET
    policy_resource_category: Union[str, None, UnsetType] = UNSET
    policy_priority: Union[int, None, UnsetType] = UNSET
    is_policy_enabled: Union[bool, None, UnsetType] = UNSET
    policy_mask_type: Union[str, None, UnsetType] = UNSET
    policy_validity_schedule: Union[list[Any], None, UnsetType] = UNSET
    policy_resource_signature: Union[str, None, UnsetType] = UNSET
    policy_delegate_admin: Union[bool, None, UnsetType] = UNSET
    policy_conditions: Union[list[Any], None, UnsetType] = UNSET
    connection_qualified_name: Union[str, None, UnsetType] = UNSET


class AuthPolicyNested(AssetNested):
    attributes: Union[AuthPolicyAttributes, UnsetType] = UNSET


def _auth_policy_to_nested(ap: AuthPolicy) -> AuthPolicyNested:
    attrs_kwargs = build_attributes_kwargs(ap, AuthPolicyAttributes)
    attrs = AuthPolicyAttributes(**attrs_kwargs)
    return AuthPolicyNested(
        guid=ap.guid,
        type_name=ap.type_name,
        status=ap.status,
        version=ap.version,
        create_time=ap.create_time,
        update_time=ap.update_time,
        created_by=ap.created_by,
        updated_by=ap.updated_by,
        classifications=ap.classifications,
        classification_names=ap.classification_names,
        meanings=ap.meanings,
        labels=ap.labels,
        business_attributes=ap.business_attributes,
        custom_attributes=ap.custom_attributes,
        pending_tasks=ap.pending_tasks,
        proxy=ap.proxy,
        is_incomplete=ap.is_incomplete,
        provenance_type=ap.provenance_type,
        home_id=ap.home_id,
        attributes=attrs,
    )


def _auth_policy_from_nested(nested: AuthPolicyNested) -> AuthPolicy:
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else AuthPolicyAttributes()
    )
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        [],
        object,
    )
    kwargs = build_flat_kwargs(
        nested, attrs, merged_rels, AssetNested, AuthPolicyAttributes
    )
    return AuthPolicy(**kwargs)


def _auth_policy_to_nested_bytes(ap: AuthPolicy, serde: Serde) -> bytes:
    return serde.encode(_auth_policy_to_nested(ap))


def _auth_policy_from_nested_bytes(data: bytes, serde: Serde) -> AuthPolicy:
    nested = serde.decode(data, AuthPolicyNested)
    return _auth_policy_from_nested(nested)
