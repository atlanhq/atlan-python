# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AuthPolicyType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)
from pyatlan.model.structs import AuthPolicyCondition, AuthPolicyValiditySchedule
from pyatlan.utils import validate_required_fields

from .asset import Asset, SelfAsset


class AuthPolicy(Asset, type_name="AuthPolicy"):
    """Description"""

    @classmethod
    def __create(cls, *, name: str) -> AuthPolicy:
        validate_required_fields(["name"], [name])
        attributes = AuthPolicy.Attributes._Attributes__create(name=name)  # type: ignore[attr-defined]
        return cls(attributes=attributes)

    @classmethod
    def updater(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = ""
        """
        This method is not available for AuthPolicy.
        Please retrieve the existing policy and then update it in its entirety.
        """,
    ) -> SelfAsset:
        raise NotImplementedError(
            "This method is not available for AuthPolicy. "
            "Please retrieve the existing policy and then update it in its entirety."
        )

    @classmethod
    def create_for_modification(
        cls: type[SelfAsset],
        qualified_name: str = "",
        name: str = ""
        """
        This method is not available for AuthPolicy.
        Please retrieve the existing policy and then update it in its entirety.
        """,
    ) -> SelfAsset:
        warn(
            (
                "This method is deprecated, please use 'updater' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.updater(qualified_name=qualified_name, name=name)

    type_name: str = Field(default="AuthPolicy", allow_mutation=False)

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

    _convenience_properties: ClassVar[List[str]] = [
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
    def policy_users(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.policy_users

    @policy_users.setter
    def policy_users(self, policy_users: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_users = policy_users

    @property
    def policy_groups(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.policy_groups

    @policy_groups.setter
    def policy_groups(self, policy_groups: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_groups = policy_groups

    @property
    def policy_roles(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.policy_roles

    @policy_roles.setter
    def policy_roles(self, policy_roles: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_roles = policy_roles

    @property
    def policy_actions(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.policy_actions

    @policy_actions.setter
    def policy_actions(self, policy_actions: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.policy_actions = policy_actions

    @property
    def policy_resources(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.policy_resources

    @policy_resources.setter
    def policy_resources(self, policy_resources: Optional[Set[str]]):
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
    def policy_validity_schedule(self) -> Optional[List[AuthPolicyValiditySchedule]]:
        return (
            None
            if self.attributes is None
            else self.attributes.policy_validity_schedule
        )

    @policy_validity_schedule.setter
    def policy_validity_schedule(
        self, policy_validity_schedule: Optional[List[AuthPolicyValiditySchedule]]
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
    def policy_conditions(self) -> Optional[List[AuthPolicyCondition]]:
        return None if self.attributes is None else self.attributes.policy_conditions

    @policy_conditions.setter
    def policy_conditions(self, policy_conditions: Optional[List[AuthPolicyCondition]]):
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
        policy_type: Optional[AuthPolicyType] = Field(default=None, description="")
        policy_service_name: Optional[str] = Field(default=None, description="")
        policy_category: Optional[str] = Field(default=None, description="")
        policy_sub_category: Optional[str] = Field(default=None, description="")
        policy_users: Optional[Set[str]] = Field(default=None, description="")
        policy_groups: Optional[Set[str]] = Field(default=None, description="")
        policy_roles: Optional[Set[str]] = Field(default=None, description="")
        policy_actions: Optional[Set[str]] = Field(default=None, description="")
        policy_resources: Optional[Set[str]] = Field(default=None, description="")
        policy_resource_category: Optional[str] = Field(default=None, description="")
        policy_priority: Optional[int] = Field(default=None, description="")
        is_policy_enabled: Optional[bool] = Field(default=None, description="")
        policy_mask_type: Optional[str] = Field(default=None, description="")
        policy_validity_schedule: Optional[List[AuthPolicyValiditySchedule]] = Field(
            default=None, description=""
        )
        policy_resource_signature: Optional[str] = Field(default=None, description="")
        policy_delegate_admin: Optional[bool] = Field(default=None, description="")
        policy_conditions: Optional[List[AuthPolicyCondition]] = Field(
            default=None, description=""
        )
        access_control: Optional[AccessControl] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        def __create(cls, name: str) -> AuthPolicy.Attributes:
            validate_required_fields(["name"], [name])
            return AuthPolicy.Attributes(
                qualified_name=name, name=name, display_name=""
            )

    attributes: AuthPolicy.Attributes = Field(
        default_factory=lambda: AuthPolicy.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .access_control import AccessControl  # noqa
