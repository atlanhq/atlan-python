# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional, Set

from pydantic import Field, validator

from pyatlan.model.enums import (
    AuthPolicyCategory,
    AuthPolicyResourceCategory,
    AuthPolicyType,
    DataAction,
    PurposeMetadataAction,
)
from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.utils import validate_required_fields

from .asset00 import SelfAsset
from .asset05 import AccessControl, AuthPolicy


class Purpose(AccessControl):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(cls, *, name: str, atlan_tags: list[str]) -> Purpose:
        validate_required_fields(["name", "atlan_tags"], [name, atlan_tags])
        attributes = Purpose.Attributes.create(name=name, atlan_tags=atlan_tags)
        return cls(attributes=attributes)

    @classmethod
    # @validate_arguments()
    def create_metadata_policy(
        cls,
        *,
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        actions: Set[PurposeMetadataAction],
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "purpose_id", "policy_type", "actions"],
            [name, purpose_id, policy_type, actions],
        )
        target_found = False
        policy = AuthPolicy._AuthPolicy__create(name=name)  # type: ignore
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
                from pyatlan.cache.group_cache import GroupCache

                for group_alias in policy_groups:
                    if not GroupCache.get_id_for_alias(group_alias):
                        raise ValueError(
                            f"Provided group name {group_alias} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                from pyatlan.cache.user_cache import UserCache

                for username in policy_users:
                    if not UserCache.get_id_for_name(username):
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
    # @validate_arguments()
    def create_data_policy(
        cls,
        *,
        name: str,
        purpose_id: str,
        policy_type: AuthPolicyType,
        policy_groups: Optional[Set[str]] = None,
        policy_users: Optional[Set[str]] = None,
        all_users: bool = False,
    ) -> AuthPolicy:
        validate_required_fields(
            ["name", "purpose_id", "policy_type"], [name, purpose_id, policy_type]
        )
        policy = AuthPolicy._AuthPolicy__create(name=name)  # type: ignore
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
                from pyatlan.cache.group_cache import GroupCache

                for group_alias in policy_groups:
                    if not GroupCache.get_id_for_alias(group_alias):
                        raise ValueError(
                            f"Provided group name {group_alias} was not found in Atlan."
                        )
                target_found = True
                policy.policy_groups = policy_groups
            else:
                policy.policy_groups = None
            if policy_users:
                from pyatlan.cache.user_cache import UserCache

                for username in policy_users:
                    if not UserCache.get_id_for_name(username):
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
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = "",
        is_enabled: bool = True,
    ) -> SelfAsset:
        validate_required_fields(
            ["name", "qualified_name", "is_enabled"],
            [name, qualified_name, is_enabled],
        )
        return cls(
            attributes=cls.Attributes(
                qualified_name=qualified_name,
                name=name,
                is_access_control_enabled=is_enabled,
            )
        )

    type_name: str = Field("Purpose", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Purpose":
            raise ValueError("must be Purpose")
        return v

    def __setattr__(self, name, value):
        if name in Purpose._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PURPOSE_CLASSIFICATIONS: ClassVar[KeywordField] = KeywordField(
        "purposeClassifications", "purposeClassifications"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "purpose_atlan_tags",
    ]

    @property
    def purpose_atlan_tags(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.purpose_atlan_tags

    @purpose_atlan_tags.setter
    def purpose_atlan_tags(self, purpose_atlan_tags: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.purpose_atlan_tags = purpose_atlan_tags

    class Attributes(AccessControl.Attributes):
        purpose_atlan_tags: Optional[set[str]] = Field(
            None, description="", alias="purposeClassifications"
        )

        @classmethod
        # @validate_arguments()
        def create(cls, name: str, atlan_tags: list[str]) -> Purpose.Attributes:
            validate_required_fields(["name", "atlan_tags"], [name, atlan_tags])
            return Purpose.Attributes(
                qualified_name=name,
                name=name,
                display_name=name,
                is_access_control_enabled=True,
                description="",
                purpose_atlan_tags=atlan_tags,
            )

    attributes: "Purpose.Attributes" = Field(
        default_factory=lambda: Purpose.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Purpose.Attributes.update_forward_refs()
