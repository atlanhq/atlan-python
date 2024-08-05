# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .core.asset import Asset


class BusinessPolicyLog(Asset, type_name="BusinessPolicyLog"):
    """Description"""

    type_name: str = Field(default="BusinessPolicyLog", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BusinessPolicyLog":
            raise ValueError("must be BusinessPolicyLog")
        return v

    def __setattr__(self, name, value):
        if name in BusinessPolicyLog._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BUSINESS_POLICY_ID: ClassVar[KeywordField] = KeywordField(
        "businessPolicyId", "businessPolicyId"
    )
    """
    business policy guid for which log are created
    """
    BUSINESS_POLICY_LOG_POLICY_TYPE: ClassVar[KeywordField] = KeywordField(
        "businessPolicyLogPolicyType", "businessPolicyLogPolicyType"
    )
    """
    business policy type for which log are created
    """
    GOVERNED_ASSETS_COUNT: ClassVar[NumericField] = NumericField(
        "governedAssetsCount", "governedAssetsCount"
    )
    """
    number of governed assets in the policy
    """
    NON_GOVERNED_ASSETS_COUNT: ClassVar[NumericField] = NumericField(
        "nonGovernedAssetsCount", "nonGovernedAssetsCount"
    )
    """
    number of non governed assets in the policy
    """
    COMPLIANT_ASSETS_COUNT: ClassVar[NumericField] = NumericField(
        "compliantAssetsCount", "compliantAssetsCount"
    )
    """
    number of compliant assets in the policy
    """
    NON_COMPLIANT_ASSETS_COUNT: ClassVar[NumericField] = NumericField(
        "nonCompliantAssetsCount", "nonCompliantAssetsCount"
    )
    """
    number of non compliant assets in the policy
    """

    _convenience_properties: ClassVar[List[str]] = [
        "business_policy_id",
        "business_policy_log_policy_type",
        "governed_assets_count",
        "non_governed_assets_count",
        "compliant_assets_count",
        "non_compliant_assets_count",
    ]

    @property
    def business_policy_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.business_policy_id

    @business_policy_id.setter
    def business_policy_id(self, business_policy_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_id = business_policy_id

    @property
    def business_policy_log_policy_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_log_policy_type
        )

    @business_policy_log_policy_type.setter
    def business_policy_log_policy_type(
        self, business_policy_log_policy_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_log_policy_type = (
            business_policy_log_policy_type
        )

    @property
    def governed_assets_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.governed_assets_count
        )

    @governed_assets_count.setter
    def governed_assets_count(self, governed_assets_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.governed_assets_count = governed_assets_count

    @property
    def non_governed_assets_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.non_governed_assets_count
        )

    @non_governed_assets_count.setter
    def non_governed_assets_count(self, non_governed_assets_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.non_governed_assets_count = non_governed_assets_count

    @property
    def compliant_assets_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.compliant_assets_count
        )

    @compliant_assets_count.setter
    def compliant_assets_count(self, compliant_assets_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.compliant_assets_count = compliant_assets_count

    @property
    def non_compliant_assets_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.non_compliant_assets_count
        )

    @non_compliant_assets_count.setter
    def non_compliant_assets_count(self, non_compliant_assets_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.non_compliant_assets_count = non_compliant_assets_count

    class Attributes(Asset.Attributes):
        business_policy_id: Optional[str] = Field(default=None, description="")
        business_policy_log_policy_type: Optional[str] = Field(
            default=None, description=""
        )
        governed_assets_count: Optional[int] = Field(default=None, description="")
        non_governed_assets_count: Optional[int] = Field(default=None, description="")
        compliant_assets_count: Optional[int] = Field(default=None, description="")
        non_compliant_assets_count: Optional[int] = Field(default=None, description="")

    attributes: BusinessPolicyLog.Attributes = Field(
        default_factory=lambda: BusinessPolicyLog.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


BusinessPolicyLog.Attributes.update_forward_refs()
