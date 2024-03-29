# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .salesforce import Salesforce


class SalesforceOrganization(Salesforce):
    """Description"""

    type_name: str = Field(default="SalesforceOrganization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceOrganization":
            raise ValueError("must be SalesforceOrganization")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceOrganization._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_ID: ClassVar[KeywordField] = KeywordField("sourceId", "sourceId")
    """
    Identifier of the organization in Salesforce.
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    OBJECTS: ClassVar[RelationField] = RelationField("objects")
    """
    TBC
    """
    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "source_id",
        "reports",
        "objects",
        "dashboards",
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
    def reports(self) -> Optional[List[SalesforceReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[List[SalesforceReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def objects(self) -> Optional[List[SalesforceObject]]:
        return None if self.attributes is None else self.attributes.objects

    @objects.setter
    def objects(self, objects: Optional[List[SalesforceObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.objects = objects

    @property
    def dashboards(self) -> Optional[List[SalesforceDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[List[SalesforceDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(default=None, description="")
        reports: Optional[List[SalesforceReport]] = Field(
            default=None, description=""
        )  # relationship
        objects: Optional[List[SalesforceObject]] = Field(
            default=None, description=""
        )  # relationship
        dashboards: Optional[List[SalesforceDashboard]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SalesforceOrganization.Attributes = Field(
        default_factory=lambda: SalesforceOrganization.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .salesforce_dashboard import SalesforceDashboard  # noqa
from .salesforce_object import SalesforceObject  # noqa
from .salesforce_report import SalesforceReport  # noqa
