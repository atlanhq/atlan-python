# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .power_b_i import PowerBI


class PowerBITile(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBITile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBITile":
            raise ValueError("must be PowerBITile")
        return v

    def __setattr__(self, name, value):
        if name in PowerBITile._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this tile exists.
    """
    DASHBOARD_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dashboardQualifiedName", "dashboardQualifiedName"
    )
    """
    Unique name of the dashboard in which this tile is pinned.
    """

    REPORT: ClassVar[RelationField] = RelationField("report")
    """
    TBC
    """
    DATASET: ClassVar[RelationField] = RelationField("dataset")
    """
    TBC
    """
    DASHBOARD: ClassVar[RelationField] = RelationField("dashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "dashboard_qualified_name",
        "report",
        "dataset",
        "dashboard",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dashboard_qualified_name
        )

    @dashboard_qualified_name.setter
    def dashboard_qualified_name(self, dashboard_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_qualified_name = dashboard_qualified_name

    @property
    def report(self) -> Optional[PowerBIReport]:
        return None if self.attributes is None else self.attributes.report

    @report.setter
    def report(self, report: Optional[PowerBIReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report = report

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

    @property
    def dashboard(self) -> Optional[PowerBIDashboard]:
        return None if self.attributes is None else self.attributes.dashboard

    @dashboard.setter
    def dashboard(self, dashboard: Optional[PowerBIDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard = dashboard

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        dashboard_qualified_name: Optional[str] = Field(default=None, description="")
        report: Optional[PowerBIReport] = Field(
            default=None, description=""
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            default=None, description=""
        )  # relationship
        dashboard: Optional[PowerBIDashboard] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBITile.Attributes = Field(
        default_factory=lambda: PowerBITile.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dashboard import PowerBIDashboard  # noqa
from .power_b_i_dataset import PowerBIDataset  # noqa
from .power_b_i_report import PowerBIReport  # noqa
