# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)

from .core.asset import Asset


class BusinessPolicyException(Asset, type_name="BusinessPolicyException"):
    """Description"""

    type_name: str = Field(default="BusinessPolicyException", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BusinessPolicyException":
            raise ValueError("must be BusinessPolicyException")
        return v

    def __setattr__(self, name, value):
        if name in BusinessPolicyException._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BUSINESS_POLICY_EXCEPTION_USERS: ClassVar[KeywordField] = KeywordField(
        "businessPolicyExceptionUsers", "businessPolicyExceptionUsers"
    )
    """
    List of users who are part of this exception
    """
    BUSINESS_POLICY_EXCEPTION_GROUPS: ClassVar[KeywordField] = KeywordField(
        "businessPolicyExceptionGroups", "businessPolicyExceptionGroups"
    )
    """
    List of groups who are part of this exception
    """
    BUSINESS_POLICY_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "businessPolicyQualifiedName",
        "businessPolicyQualifiedName",
        "businessPolicyQualifiedName.text",
    )
    """
    Unique name of the business policy through which this asset is accessible.
    """
    BUSINESS_POLICY_EXCEPTION_FILTER_DSL: ClassVar[TextField] = TextField(
        "businessPolicyExceptionFilterDSL", "businessPolicyExceptionFilterDSL"
    )
    """
    Business Policy Exception Filter ES DSL to denote the associate asset/s involved.
    """

    BUSINESS_POLICY_FOR_EXCEPTION: ClassVar[RelationField] = RelationField(
        "businessPolicyForException"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "business_policy_exception_users",
        "business_policy_exception_groups",
        "business_policy_qualified_name",
        "business_policy_exception_filter_d_s_l",
        "business_policy_for_exception",
    ]

    @property
    def business_policy_exception_users(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_exception_users
        )

    @business_policy_exception_users.setter
    def business_policy_exception_users(
        self, business_policy_exception_users: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_exception_users = (
            business_policy_exception_users
        )

    @property
    def business_policy_exception_groups(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_exception_groups
        )

    @business_policy_exception_groups.setter
    def business_policy_exception_groups(
        self, business_policy_exception_groups: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_exception_groups = (
            business_policy_exception_groups
        )

    @property
    def business_policy_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_qualified_name
        )

    @business_policy_qualified_name.setter
    def business_policy_qualified_name(
        self, business_policy_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_qualified_name = business_policy_qualified_name

    @property
    def business_policy_exception_filter_d_s_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_exception_filter_d_s_l
        )

    @business_policy_exception_filter_d_s_l.setter
    def business_policy_exception_filter_d_s_l(
        self, business_policy_exception_filter_d_s_l: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_exception_filter_d_s_l = (
            business_policy_exception_filter_d_s_l
        )

    @property
    def business_policy_for_exception(self) -> Optional[BusinessPolicy]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_for_exception
        )

    @business_policy_for_exception.setter
    def business_policy_for_exception(
        self, business_policy_for_exception: Optional[BusinessPolicy]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_for_exception = business_policy_for_exception

    class Attributes(Asset.Attributes):
        business_policy_exception_users: Optional[Set[str]] = Field(
            default=None, description=""
        )
        business_policy_exception_groups: Optional[Set[str]] = Field(
            default=None, description=""
        )
        business_policy_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        business_policy_exception_filter_d_s_l: Optional[str] = Field(
            default=None, description=""
        )
        business_policy_for_exception: Optional[BusinessPolicy] = Field(
            default=None, description=""
        )  # relationship

    attributes: BusinessPolicyException.Attributes = Field(
        default_factory=lambda: BusinessPolicyException.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .business_policy import BusinessPolicy  # noqa

BusinessPolicyException.Attributes.update_forward_refs()
