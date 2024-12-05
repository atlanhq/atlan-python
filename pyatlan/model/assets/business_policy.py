# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .core.asset import Asset


class BusinessPolicy(Asset, type_name="BusinessPolicy"):
    """Description"""

    type_name: str = Field(default="BusinessPolicy", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BusinessPolicy":
            raise ValueError("must be BusinessPolicy")
        return v

    def __setattr__(self, name, value):
        if name in BusinessPolicy._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BUSINESS_POLICY_TYPE: ClassVar[KeywordField] = KeywordField(
        "businessPolicyType", "businessPolicyType"
    )
    """
    Type of business policy
    """
    BUSINESS_POLICY_LONG_DESCRIPTION: ClassVar[RelationField] = RelationField(
        "businessPolicyLongDescription"
    )
    """
    Body of the business policy, a long readme like document
    """
    BUSINESS_POLICY_VALID_TILL: ClassVar[NumericField] = NumericField(
        "businessPolicyValidTill", "businessPolicyValidTill"
    )
    """
    Validity end date of the policy
    """
    BUSINESS_POLICY_VALID_FROM: ClassVar[NumericField] = NumericField(
        "businessPolicyValidFrom", "businessPolicyValidFrom"
    )
    """
    Validity start date of the policy
    """
    BUSINESS_POLICY_VERSION: ClassVar[NumericField] = NumericField(
        "businessPolicyVersion", "businessPolicyVersion"
    )
    """
    Version of the policy
    """
    BUSINESS_POLICY_REVIEW_PERIOD: ClassVar[KeywordField] = KeywordField(
        "businessPolicyReviewPeriod", "businessPolicyReviewPeriod"
    )
    """
    Duration for the business policy to complete review.
    """
    BUSINESS_POLICY_FILTER_DSL: ClassVar[TextField] = TextField(
        "businessPolicyFilterDSL", "businessPolicyFilterDSL"
    )
    """
    Business Policy Filter ES DSL to denote the associate asset/s involved.
    """
    BUSINESS_POLICY_BASE_PARENT_GUID: ClassVar[KeywordField] = KeywordField(
        "businessPolicyBaseParentGuid", "businessPolicyBaseParentGuid"
    )
    """
    Base parent Guid for policy used in version
    """
    BUSINESS_POLICY_SELECTED_APPROVAL_WF: ClassVar[TextField] = TextField(
        "businessPolicySelectedApprovalWF", "businessPolicySelectedApprovalWF"
    )
    """
    Selected approval workflow id for business policy
    """

    EXCEPTIONS_FOR_BUSINESS_POLICY: ClassVar[RelationField] = RelationField(
        "exceptionsForBusinessPolicy"
    )
    """
    TBC
    """
    RELATED_BUSINESS_POLICIES: ClassVar[RelationField] = RelationField(
        "relatedBusinessPolicies"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "business_policy_type",
        "business_policy_long_description",
        "business_policy_valid_till",
        "business_policy_valid_from",
        "business_policy_version",
        "business_policy_review_period",
        "business_policy_filter_d_s_l",
        "business_policy_base_parent_guid",
        "business_policy_selected_approval_w_f",
        "exceptions_for_business_policy",
        "related_business_policies",
    ]

    @property
    def business_policy_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.business_policy_type

    @business_policy_type.setter
    def business_policy_type(self, business_policy_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_type = business_policy_type

    @property
    def business_policy_long_description(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_long_description
        )

    @business_policy_long_description.setter
    def business_policy_long_description(
        self, business_policy_long_description: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_long_description = (
            business_policy_long_description
        )

    @property
    def business_policy_valid_till(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_valid_till
        )

    @business_policy_valid_till.setter
    def business_policy_valid_till(
        self, business_policy_valid_till: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_valid_till = business_policy_valid_till

    @property
    def business_policy_valid_from(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_valid_from
        )

    @business_policy_valid_from.setter
    def business_policy_valid_from(
        self, business_policy_valid_from: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_valid_from = business_policy_valid_from

    @property
    def business_policy_version(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.business_policy_version
        )

    @business_policy_version.setter
    def business_policy_version(self, business_policy_version: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_version = business_policy_version

    @property
    def business_policy_review_period(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_review_period
        )

    @business_policy_review_period.setter
    def business_policy_review_period(
        self, business_policy_review_period: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_review_period = business_policy_review_period

    @property
    def business_policy_filter_d_s_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_filter_d_s_l
        )

    @business_policy_filter_d_s_l.setter
    def business_policy_filter_d_s_l(self, business_policy_filter_d_s_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_filter_d_s_l = business_policy_filter_d_s_l

    @property
    def business_policy_base_parent_guid(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_base_parent_guid
        )

    @business_policy_base_parent_guid.setter
    def business_policy_base_parent_guid(
        self, business_policy_base_parent_guid: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_base_parent_guid = (
            business_policy_base_parent_guid
        )

    @property
    def business_policy_selected_approval_w_f(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_selected_approval_w_f
        )

    @business_policy_selected_approval_w_f.setter
    def business_policy_selected_approval_w_f(
        self, business_policy_selected_approval_w_f: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_selected_approval_w_f = (
            business_policy_selected_approval_w_f
        )

    @property
    def exceptions_for_business_policy(self) -> Optional[List[BusinessPolicyException]]:
        return (
            None
            if self.attributes is None
            else self.attributes.exceptions_for_business_policy
        )

    @exceptions_for_business_policy.setter
    def exceptions_for_business_policy(
        self, exceptions_for_business_policy: Optional[List[BusinessPolicyException]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.exceptions_for_business_policy = exceptions_for_business_policy

    @property
    def related_business_policies(self) -> Optional[List[BusinessPolicy]]:
        return (
            None
            if self.attributes is None
            else self.attributes.related_business_policies
        )

    @related_business_policies.setter
    def related_business_policies(
        self, related_business_policies: Optional[List[BusinessPolicy]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.related_business_policies = related_business_policies

    class Attributes(Asset.Attributes):
        business_policy_type: Optional[str] = Field(default=None, description="")
        business_policy_long_description: Optional[str] = Field(
            default=None, description=""
        )
        business_policy_valid_till: Optional[datetime] = Field(
            default=None, description=""
        )
        business_policy_valid_from: Optional[datetime] = Field(
            default=None, description=""
        )
        business_policy_version: Optional[int] = Field(default=None, description="")
        business_policy_review_period: Optional[str] = Field(
            default=None, description=""
        )
        business_policy_filter_d_s_l: Optional[str] = Field(
            default=None, description=""
        )
        business_policy_base_parent_guid: Optional[str] = Field(
            default=None, description=""
        )
        business_policy_selected_approval_w_f: Optional[str] = Field(
            default=None, description=""
        )
        exceptions_for_business_policy: Optional[List[BusinessPolicyException]] = Field(
            default=None, description=""
        )  # relationship
        related_business_policies: Optional[List[BusinessPolicy]] = Field(
            default=None, description=""
        )  # relationship

    attributes: BusinessPolicy.Attributes = Field(
        default_factory=lambda: BusinessPolicy.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .business_policy_exception import BusinessPolicyException  # noqa

BusinessPolicy.Attributes.update_forward_refs()
