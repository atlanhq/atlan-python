# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.enums import AuthPolicyType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)
from pyatlan.model.structs import AuthPolicyCondition, AuthPolicyValiditySchedule
from pyatlan.utils import validate_required_fields

from .asset00 import Asset


class AuthPolicy(Asset, type_name="AuthPolicy"):
    """Description"""

    @classmethod
    # @validate_arguments()
    def __create(cls, *, name: str) -> AuthPolicy:
        validate_required_fields(["name"], [name])
        attributes = AuthPolicy.Attributes._Attributes__create(name=name)  # type: ignore
        return cls(attributes=attributes)

    type_name: str = Field("AuthPolicy", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AuthPolicy":
            raise ValueError("must be AuthPolicy")
        return v

    def __setattr__(self, name, value):
        if name in AuthPolicy._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    POLICY_TYPE: ClassVar[KeywordField] = KeywordField("policyType", "policyType")
    """
    TBC
    """
    POLICY_SERVICE_NAME: ClassVar[KeywordField] = KeywordField(
        "policyServiceName", "policyServiceName"
    )
    """
    TBC
    """
    POLICY_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "policyCategory", "policyCategory"
    )
    """
    TBC
    """
    POLICY_SUB_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "policySubCategory", "policySubCategory"
    )
    """
    TBC
    """
    POLICY_USERS: ClassVar[KeywordField] = KeywordField("policyUsers", "policyUsers")
    """
    TBC
    """
    POLICY_GROUPS: ClassVar[KeywordField] = KeywordField("policyGroups", "policyGroups")
    """
    TBC
    """
    POLICY_ROLES: ClassVar[KeywordField] = KeywordField("policyRoles", "policyRoles")
    """
    TBC
    """
    POLICY_ACTIONS: ClassVar[KeywordField] = KeywordField(
        "policyActions", "policyActions"
    )
    """
    TBC
    """
    POLICY_RESOURCES: ClassVar[KeywordField] = KeywordField(
        "policyResources", "policyResources"
    )
    """
    TBC
    """
    POLICY_RESOURCE_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "policyResourceCategory", "policyResourceCategory"
    )
    """
    TBC
    """
    POLICY_PRIORITY: ClassVar[NumericField] = NumericField(
        "policyPriority", "policyPriority"
    )
    """
    TBC
    """
    IS_POLICY_ENABLED: ClassVar[BooleanField] = BooleanField(
        "isPolicyEnabled", "isPolicyEnabled"
    )
    """
    TBC
    """
    POLICY_MASK_TYPE: ClassVar[KeywordField] = KeywordField(
        "policyMaskType", "policyMaskType"
    )
    """
    TBC
    """
    POLICY_VALIDITY_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "policyValiditySchedule", "policyValiditySchedule"
    )
    """
    TBC
    """
    POLICY_RESOURCE_SIGNATURE: ClassVar[KeywordField] = KeywordField(
        "policyResourceSignature", "policyResourceSignature"
    )
    """
    TBC
    """
    POLICY_DELEGATE_ADMIN: ClassVar[BooleanField] = BooleanField(
        "policyDelegateAdmin", "policyDelegateAdmin"
    )
    """
    TBC
    """
    POLICY_CONDITIONS: ClassVar[KeywordField] = KeywordField(
        "policyConditions", "policyConditions"
    )
    """
    TBC
    """

    ACCESS_CONTROL: ClassVar[RelationField] = RelationField("accessControl")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "policy_type",
        "policy_service_name",
        "policy_category",
        "policy_sub_category",
        "policy_users",
        "policy_groups",
        "policy_roles",
        "policy_actions",
        "policy_resources",
        "policy_resource_category",
        "policy_priority",
        "is_policy_enabled",
        "policy_mask_type",
        "policy_validity_schedule",
        "policy_resource_signature",
        "policy_delegate_admin",
        "policy_conditions",
        "access_control",
    ]

    @property
    def policy_type(self) -> Optional[AuthPolicyType]:
        return None if self.attributes is None else self.attributes.policy_type

    @policy_type.setter
    def policy_type(self, policy_type: Optional[AuthPolicyType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_type = policy_type

    @property
    def policy_service_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_service_name

    @policy_service_name.setter
    def policy_service_name(self, policy_service_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_service_name = policy_service_name

    @property
    def policy_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_category

    @policy_category.setter
    def policy_category(self, policy_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_category = policy_category

    @property
    def policy_sub_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_sub_category

    @policy_sub_category.setter
    def policy_sub_category(self, policy_sub_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_sub_category = policy_sub_category

    @property
    def policy_users(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_users

    @policy_users.setter
    def policy_users(self, policy_users: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_users = policy_users

    @property
    def policy_groups(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_groups

    @policy_groups.setter
    def policy_groups(self, policy_groups: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_groups = policy_groups

    @property
    def policy_roles(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_roles

    @policy_roles.setter
    def policy_roles(self, policy_roles: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_roles = policy_roles

    @property
    def policy_actions(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_actions

    @policy_actions.setter
    def policy_actions(self, policy_actions: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_actions = policy_actions

    @property
    def policy_resources(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.policy_resources

    @policy_resources.setter
    def policy_resources(self, policy_resources: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_resources = policy_resources

    @property
    def policy_resource_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_resource_category
        )

    @policy_resource_category.setter
    def policy_resource_category(self, policy_resource_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_resource_category = policy_resource_category

    @property
    def policy_priority(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.policy_priority

    @policy_priority.setter
    def policy_priority(self, policy_priority: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_priority = policy_priority

    @property
    def is_policy_enabled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_policy_enabled

    @is_policy_enabled.setter
    def is_policy_enabled(self, is_policy_enabled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_policy_enabled = is_policy_enabled

    @property
    def policy_mask_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.policy_mask_type

    @policy_mask_type.setter
    def policy_mask_type(self, policy_mask_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_mask_type = policy_mask_type

    @property
    def policy_validity_schedule(self) -> Optional[list[AuthPolicyValiditySchedule]]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_validity_schedule
        )

    @policy_validity_schedule.setter
    def policy_validity_schedule(
        self, policy_validity_schedule: Optional[list[AuthPolicyValiditySchedule]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_validity_schedule = policy_validity_schedule

    @property
    def policy_resource_signature(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_resource_signature
        )

    @policy_resource_signature.setter
    def policy_resource_signature(self, policy_resource_signature: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_resource_signature = policy_resource_signature

    @property
    def policy_delegate_admin(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.policy_delegate_admin
        )

    @policy_delegate_admin.setter
    def policy_delegate_admin(self, policy_delegate_admin: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_delegate_admin = policy_delegate_admin

    @property
    def policy_conditions(self) -> Optional[list[AuthPolicyCondition]]:
        return None if self.attributes is None else self.attributes.policy_conditions

    @policy_conditions.setter
    def policy_conditions(self, policy_conditions: Optional[list[AuthPolicyCondition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_conditions = policy_conditions

    @property
    def access_control(self) -> Optional[AccessControl]:
        return None if self.attributes is None else self.attributes.access_control

    @access_control.setter
    def access_control(self, access_control: Optional[AccessControl]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.access_control = access_control

    class Attributes(Asset.Attributes):
        policy_type: Optional[AuthPolicyType] = Field(
            None, description="", alias="policyType"
        )
        policy_service_name: Optional[str] = Field(
            None, description="", alias="policyServiceName"
        )
        policy_category: Optional[str] = Field(
            None, description="", alias="policyCategory"
        )
        policy_sub_category: Optional[str] = Field(
            None, description="", alias="policySubCategory"
        )
        policy_users: Optional[set[str]] = Field(
            None, description="", alias="policyUsers"
        )
        policy_groups: Optional[set[str]] = Field(
            None, description="", alias="policyGroups"
        )
        policy_roles: Optional[set[str]] = Field(
            None, description="", alias="policyRoles"
        )
        policy_actions: Optional[set[str]] = Field(
            None, description="", alias="policyActions"
        )
        policy_resources: Optional[set[str]] = Field(
            None, description="", alias="policyResources"
        )
        policy_resource_category: Optional[str] = Field(
            None, description="", alias="policyResourceCategory"
        )
        policy_priority: Optional[int] = Field(
            None, description="", alias="policyPriority"
        )
        is_policy_enabled: Optional[bool] = Field(
            None, description="", alias="isPolicyEnabled"
        )
        policy_mask_type: Optional[str] = Field(
            None, description="", alias="policyMaskType"
        )
        policy_validity_schedule: Optional[list[AuthPolicyValiditySchedule]] = Field(
            None, description="", alias="policyValiditySchedule"
        )
        policy_resource_signature: Optional[str] = Field(
            None, description="", alias="policyResourceSignature"
        )
        policy_delegate_admin: Optional[bool] = Field(
            None, description="", alias="policyDelegateAdmin"
        )
        policy_conditions: Optional[list[AuthPolicyCondition]] = Field(
            None, description="", alias="policyConditions"
        )
        access_control: Optional[AccessControl] = Field(
            None, description="", alias="accessControl"
        )  # relationship

        @classmethod
        # @validate_arguments()
        def __create(cls, name: str) -> AuthPolicy.Attributes:
            validate_required_fields(["name"], [name])
            return AuthPolicy.Attributes(
                qualified_name=name, name=name, display_name=""
            )

    attributes: "AuthPolicy.Attributes" = Field(
        default_factory=lambda: AuthPolicy.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class AccessControl(Asset, type_name="AccessControl"):
    """Description"""

    type_name: str = Field("AccessControl", allow_mutation=False)

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
    CHANNEL_LINK: ClassVar[KeywordField] = KeywordField("channelLink", "channelLink")
    """
    TBC
    """

    POLICIES: ClassVar[RelationField] = RelationField("policies")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "is_access_control_enabled",
        "deny_custom_metadata_guids",
        "deny_asset_tabs",
        "channel_link",
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
    def deny_custom_metadata_guids(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.deny_custom_metadata_guids
        )

    @deny_custom_metadata_guids.setter
    def deny_custom_metadata_guids(
        self, deny_custom_metadata_guids: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_custom_metadata_guids = deny_custom_metadata_guids

    @property
    def deny_asset_tabs(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.deny_asset_tabs

    @deny_asset_tabs.setter
    def deny_asset_tabs(self, deny_asset_tabs: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.deny_asset_tabs = deny_asset_tabs

    @property
    def channel_link(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.channel_link

    @channel_link.setter
    def channel_link(self, channel_link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.channel_link = channel_link

    @property
    def policies(self) -> Optional[list[AuthPolicy]]:
        return None if self.attributes is None else self.attributes.policies

    @policies.setter
    def policies(self, policies: Optional[list[AuthPolicy]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policies = policies

    class Attributes(Asset.Attributes):
        is_access_control_enabled: Optional[bool] = Field(
            None, description="", alias="isAccessControlEnabled"
        )
        deny_custom_metadata_guids: Optional[set[str]] = Field(
            None, description="", alias="denyCustomMetadataGuids"
        )
        deny_asset_tabs: Optional[set[str]] = Field(
            None, description="", alias="denyAssetTabs"
        )
        channel_link: Optional[str] = Field(None, description="", alias="channelLink")
        policies: Optional[list[AuthPolicy]] = Field(
            None, description="", alias="policies"
        )  # relationship

    attributes: "AccessControl.Attributes" = Field(
        default_factory=lambda: AccessControl.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


AuthPolicy.Attributes.update_forward_refs()


AccessControl.Attributes.update_forward_refs()
