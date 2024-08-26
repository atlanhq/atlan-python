# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, TextField

from .incident import Incident


class BusinessPolicyIncident(Incident):
    """Description"""

    type_name: str = Field(default="BusinessPolicyIncident", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BusinessPolicyIncident":
            raise ValueError("must be BusinessPolicyIncident")
        return v

    def __setattr__(self, name, value):
        if name in BusinessPolicyIncident._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BUSINESS_POLICY_INCIDENT_NONCOMPLIANT_COUNT: ClassVar[NumericField] = NumericField(
        "businessPolicyIncidentNoncompliantCount",
        "businessPolicyIncidentNoncompliantCount",
    )
    """
    count of noncompliant assets in the incident
    """
    BUSINESS_POLICY_INCIDENT_RELATED_POLICY_GUI_DS: ClassVar[KeywordField] = (
        KeywordField(
            "businessPolicyIncidentRelatedPolicyGUIDs",
            "businessPolicyIncidentRelatedPolicyGUIDs",
        )
    )
    """
    policy ids related to this incident
    """
    BUSINESS_POLICY_INCIDENT_FILTER_DSL: ClassVar[TextField] = TextField(
        "businessPolicyIncidentFilterDSL", "businessPolicyIncidentFilterDSL"
    )
    """
    Filter ES DSL to denote the associate asset/s involved.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "business_policy_incident_noncompliant_count",
        "business_policy_incident_related_policy_g_u_i_ds",
        "business_policy_incident_filter_d_s_l",
    ]

    @property
    def business_policy_incident_noncompliant_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_incident_noncompliant_count
        )

    @business_policy_incident_noncompliant_count.setter
    def business_policy_incident_noncompliant_count(
        self, business_policy_incident_noncompliant_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_incident_noncompliant_count = (
            business_policy_incident_noncompliant_count
        )

    @property
    def business_policy_incident_related_policy_g_u_i_ds(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_incident_related_policy_g_u_i_ds
        )

    @business_policy_incident_related_policy_g_u_i_ds.setter
    def business_policy_incident_related_policy_g_u_i_ds(
        self, business_policy_incident_related_policy_g_u_i_ds: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_incident_related_policy_g_u_i_ds = (
            business_policy_incident_related_policy_g_u_i_ds
        )

    @property
    def business_policy_incident_filter_d_s_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.business_policy_incident_filter_d_s_l
        )

    @business_policy_incident_filter_d_s_l.setter
    def business_policy_incident_filter_d_s_l(
        self, business_policy_incident_filter_d_s_l: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.business_policy_incident_filter_d_s_l = (
            business_policy_incident_filter_d_s_l
        )

    class Attributes(Incident.Attributes):
        business_policy_incident_noncompliant_count: Optional[int] = Field(
            default=None, description=""
        )
        business_policy_incident_related_policy_g_u_i_ds: Optional[Set[str]] = Field(
            default=None, description=""
        )
        business_policy_incident_filter_d_s_l: Optional[str] = Field(
            default=None, description=""
        )

    attributes: BusinessPolicyIncident.Attributes = Field(
        default_factory=lambda: BusinessPolicyIncident.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


BusinessPolicyIncident.Attributes.update_forward_refs()
