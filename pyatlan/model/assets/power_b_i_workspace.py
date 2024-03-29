# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .power_b_i import PowerBI


class PowerBIWorkspace(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIWorkspace":
            raise ValueError("must be PowerBIWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    Deprecated.
    """
    REPORT_COUNT: ClassVar[NumericField] = NumericField("reportCount", "reportCount")
    """
    Number of reports in this workspace.
    """
    DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "dashboardCount", "dashboardCount"
    )
    """
    Number of dashboards in this workspace.
    """
    DATASET_COUNT: ClassVar[NumericField] = NumericField("datasetCount", "datasetCount")
    """
    Number of datasets in this workspace.
    """
    DATAFLOW_COUNT: ClassVar[NumericField] = NumericField(
        "dataflowCount", "dataflowCount"
    )
    """
    Number of dataflows in this workspace.
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    DATASETS: ClassVar[RelationField] = RelationField("datasets")
    """
    TBC
    """
    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """
    DATAFLOWS: ClassVar[RelationField] = RelationField("dataflows")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "web_url",
        "report_count",
        "dashboard_count",
        "dataset_count",
        "dataflow_count",
        "reports",
        "datasets",
        "dashboards",
        "dataflows",
    ]

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def report_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def dashboard_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dashboard_count

    @dashboard_count.setter
    def dashboard_count(self, dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_count = dashboard_count

    @property
    def dataset_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dataset_count

    @dataset_count.setter
    def dataset_count(self, dataset_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_count = dataset_count

    @property
    def dataflow_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dataflow_count

    @dataflow_count.setter
    def dataflow_count(self, dataflow_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflow_count = dataflow_count

    @property
    def reports(self) -> Optional[List[PowerBIReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[List[PowerBIReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def datasets(self) -> Optional[List[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[List[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    @property
    def dashboards(self) -> Optional[List[PowerBIDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[List[PowerBIDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def dataflows(self) -> Optional[List[PowerBIDataflow]]:
        return None if self.attributes is None else self.attributes.dataflows

    @dataflows.setter
    def dataflows(self, dataflows: Optional[List[PowerBIDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflows = dataflows

    class Attributes(PowerBI.Attributes):
        web_url: Optional[str] = Field(default=None, description="")
        report_count: Optional[int] = Field(default=None, description="")
        dashboard_count: Optional[int] = Field(default=None, description="")
        dataset_count: Optional[int] = Field(default=None, description="")
        dataflow_count: Optional[int] = Field(default=None, description="")
        reports: Optional[List[PowerBIReport]] = Field(
            default=None, description=""
        )  # relationship
        datasets: Optional[List[PowerBIDataset]] = Field(
            default=None, description=""
        )  # relationship
        dashboards: Optional[List[PowerBIDashboard]] = Field(
            default=None, description=""
        )  # relationship
        dataflows: Optional[List[PowerBIDataflow]] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIWorkspace.Attributes = Field(
        default_factory=lambda: PowerBIWorkspace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dashboard import PowerBIDashboard  # noqa
from .power_b_i_dataflow import PowerBIDataflow  # noqa
from .power_b_i_dataset import PowerBIDataset  # noqa
from .power_b_i_report import PowerBIReport  # noqa
