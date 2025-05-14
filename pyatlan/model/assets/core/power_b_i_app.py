# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .power_b_i import PowerBI


class PowerBIApp(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIApp":
            raise ValueError("must be PowerBIApp")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIApp._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    POWER_BI_APP_ID: ClassVar[KeywordField] = KeywordField(
        "powerBIAppId", "powerBIAppId"
    )
    """
    Unique ID of the PowerBI App in the PowerBI Assets Ecosystem.
    """
    POWER_BI_APP_USERS: ClassVar[KeywordField] = KeywordField(
        "powerBIAppUsers", "powerBIAppUsers"
    )
    """
    List of users and their permission access for a PowerBI App.
    """
    POWER_BI_APP_GROUPS: ClassVar[KeywordField] = KeywordField(
        "powerBIAppGroups", "powerBIAppGroups"
    )
    """
    List of groups and their permission access for a PowerBI App.
    """

    POWER_BI_DASHBOARDS: ClassVar[RelationField] = RelationField("powerBIDashboards")
    """
    TBC
    """
    POWER_BI_REPORTS: ClassVar[RelationField] = RelationField("powerBIReports")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "power_b_i_app_id",
        "power_b_i_app_users",
        "power_b_i_app_groups",
        "power_b_i_dashboards",
        "power_b_i_reports",
    ]

    @property
    def power_b_i_app_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.power_b_i_app_id

    @power_b_i_app_id.setter
    def power_b_i_app_id(self, power_b_i_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_app_id = power_b_i_app_id

    @property
    def power_b_i_app_users(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.power_b_i_app_users

    @power_b_i_app_users.setter
    def power_b_i_app_users(self, power_b_i_app_users: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_app_users = power_b_i_app_users

    @property
    def power_b_i_app_groups(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.power_b_i_app_groups

    @power_b_i_app_groups.setter
    def power_b_i_app_groups(
        self, power_b_i_app_groups: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_app_groups = power_b_i_app_groups

    @property
    def power_b_i_dashboards(self) -> Optional[List[PowerBIDashboard]]:
        return None if self.attributes is None else self.attributes.power_b_i_dashboards

    @power_b_i_dashboards.setter
    def power_b_i_dashboards(
        self, power_b_i_dashboards: Optional[List[PowerBIDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dashboards = power_b_i_dashboards

    @property
    def power_b_i_reports(self) -> Optional[List[PowerBIReport]]:
        return None if self.attributes is None else self.attributes.power_b_i_reports

    @power_b_i_reports.setter
    def power_b_i_reports(self, power_b_i_reports: Optional[List[PowerBIReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_reports = power_b_i_reports

    class Attributes(PowerBI.Attributes):
        power_b_i_app_id: Optional[str] = Field(default=None, description="")
        power_b_i_app_users: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        power_b_i_app_groups: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        power_b_i_dashboards: Optional[List[PowerBIDashboard]] = Field(
            default=None, description=""
        )  # relationship
        power_b_i_reports: Optional[List[PowerBIReport]] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIApp.Attributes = Field(
        default_factory=lambda: PowerBIApp.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dashboard import PowerBIDashboard  # noqa: E402, F401
from .power_b_i_report import PowerBIReport  # noqa: E402, F401
