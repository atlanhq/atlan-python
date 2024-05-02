# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .salesforce import Salesforce


class SalesforceReport(Salesforce):
    """Description"""

    type_name: str = Field(default="SalesforceReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceReport":
            raise ValueError("must be SalesforceReport")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_ID: ClassVar[KeywordField] = KeywordField("sourceId", "sourceId")
    """
    Identifier of the report in Salesforce.
    """
    REPORT_TYPE: ClassVar[KeywordField] = KeywordField("reportType", "reportType")
    """
    Type of report in Salesforce.
    """
    DETAIL_COLUMNS: ClassVar[KeywordField] = KeywordField(
        "detailColumns", "detailColumns"
    )
    """
    List of column names on the report.
    """

    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """
    ORGANIZATION: ClassVar[RelationField] = RelationField("organization")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "source_id",
        "report_type",
        "detail_columns",
        "dashboards",
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
    def report_type(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.report_type

    @report_type.setter
    def report_type(self, report_type: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_type = report_type

    @property
    def detail_columns(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.detail_columns

    @detail_columns.setter
    def detail_columns(self, detail_columns: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detail_columns = detail_columns

    @property
    def dashboards(self) -> Optional[List[SalesforceDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[List[SalesforceDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

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
        report_type: Optional[Dict[str, str]] = Field(default=None, description="")
        detail_columns: Optional[Set[str]] = Field(default=None, description="")
        dashboards: Optional[List[SalesforceDashboard]] = Field(
            default=None, description=""
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            default=None, description=""
        )  # relationship

    attributes: SalesforceReport.Attributes = Field(
        default_factory=lambda: SalesforceReport.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .salesforce_dashboard import SalesforceDashboard  # noqa
from .salesforce_organization import SalesforceOrganization  # noqa
