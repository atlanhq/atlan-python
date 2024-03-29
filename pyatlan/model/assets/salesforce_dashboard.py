# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .salesforce import Salesforce


class SalesforceDashboard(Salesforce):
    """Description"""

    type_name: str = Field(default="SalesforceDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceDashboard":
            raise ValueError("must be SalesforceDashboard")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_ID: ClassVar[KeywordField] = KeywordField("sourceId", "sourceId")
    """
    Identifier of the dashboard in Salesforce.
    """
    DASHBOARD_TYPE: ClassVar[KeywordField] = KeywordField(
        "dashboardType", "dashboardType"
    )
    """
    Type of dashboard in Salesforce.
    """
    REPORT_COUNT: ClassVar[NumericField] = NumericField("reportCount", "reportCount")
    """
    Number of reports linked to the dashboard in Salesforce.
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    ORGANIZATION: ClassVar[RelationField] = RelationField("organization")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "source_id",
        "dashboard_type",
        "report_count",
        "reports",
        "organization",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def dashboard_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dashboard_type

    @dashboard_type.setter
    def dashboard_type(self, dashboard_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_type = dashboard_type

    @property
    def report_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def reports(self) -> Optional[List[SalesforceReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[List[SalesforceReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def organization(self) -> Optional[SalesforceOrganization]:
        return None if self.attributes is None else self.attributes.organization

    @organization.setter
    def organization(self, organization: Optional[SalesforceOrganization]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization = organization

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(default=None, description="")
        dashboard_type: Optional[str] = Field(default=None, description="")
        report_count: Optional[int] = Field(default=None, description="")
        reports: Optional[List[SalesforceReport]] = Field(
            default=None, description=""
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            default=None, description=""
        )  # relationship

    attributes: SalesforceDashboard.Attributes = Field(
        default_factory=lambda: SalesforceDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .salesforce_organization import SalesforceOrganization  # noqa
from .salesforce_report import SalesforceReport  # noqa
