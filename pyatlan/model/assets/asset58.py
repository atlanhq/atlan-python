# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    KeywordTextStemmedField,
    NumericField,
    RelationField,
    TextField,
)

from .asset36 import Preset


class PresetChart(Preset):
    """Description"""

    type_name: str = Field("PresetChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetChart":
            raise ValueError("must be PresetChart")
        return v

    def __setattr__(self, name, value):
        if name in PresetChart._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_CHART_DESCRIPTION_MARKDOWN: ClassVar[TextField] = TextField(
        "presetChartDescriptionMarkdown", "presetChartDescriptionMarkdown"
    )
    """
    TBC
    """
    PRESET_CHART_FORM_DATA: ClassVar[KeywordField] = KeywordField(
        "presetChartFormData", "presetChartFormData"
    )
    """
    TBC
    """

    PRESET_DASHBOARD: ClassVar[RelationField] = RelationField("presetDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "preset_chart_description_markdown",
        "preset_chart_form_data",
        "preset_dashboard",
    ]

    @property
    def preset_chart_description_markdown(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_chart_description_markdown
        )

    @preset_chart_description_markdown.setter
    def preset_chart_description_markdown(
        self, preset_chart_description_markdown: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_chart_description_markdown = (
            preset_chart_description_markdown
        )

    @property
    def preset_chart_form_data(self) -> Optional[dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.preset_chart_form_data
        )

    @preset_chart_form_data.setter
    def preset_chart_form_data(self, preset_chart_form_data: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_chart_form_data = preset_chart_form_data

    @property
    def preset_dashboard(self) -> Optional[PresetDashboard]:
        return None if self.attributes is None else self.attributes.preset_dashboard

    @preset_dashboard.setter
    def preset_dashboard(self, preset_dashboard: Optional[PresetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard = preset_dashboard

    class Attributes(Preset.Attributes):
        preset_chart_description_markdown: Optional[str] = Field(
            None, description="", alias="presetChartDescriptionMarkdown"
        )
        preset_chart_form_data: Optional[dict[str, str]] = Field(
            None, description="", alias="presetChartFormData"
        )
        preset_dashboard: Optional[PresetDashboard] = Field(
            None, description="", alias="presetDashboard"
        )  # relationship

    attributes: "PresetChart.Attributes" = Field(
        default_factory=lambda: PresetChart.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetDataset(Preset):
    """Description"""

    type_name: str = Field("PresetDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDataset":
            raise ValueError("must be PresetDataset")
        return v

    def __setattr__(self, name, value):
        if name in PresetDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_DATASET_DATASOURCE_NAME: ClassVar[
        KeywordTextStemmedField
    ] = KeywordTextStemmedField(
        "presetDatasetDatasourceName",
        "presetDatasetDatasourceName.keyword",
        "presetDatasetDatasourceName",
        "presetDatasetDatasourceName.stemmed",
    )
    """
    TBC
    """
    PRESET_DATASET_ID: ClassVar[NumericField] = NumericField(
        "presetDatasetId", "presetDatasetId"
    )
    """
    TBC
    """
    PRESET_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "presetDatasetType", "presetDatasetType"
    )
    """
    TBC
    """

    PRESET_DASHBOARD: ClassVar[RelationField] = RelationField("presetDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "preset_dataset_datasource_name",
        "preset_dataset_id",
        "preset_dataset_type",
        "preset_dashboard",
    ]

    @property
    def preset_dataset_datasource_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dataset_datasource_name
        )

    @preset_dataset_datasource_name.setter
    def preset_dataset_datasource_name(
        self, preset_dataset_datasource_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_datasource_name = preset_dataset_datasource_name

    @property
    def preset_dataset_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.preset_dataset_id

    @preset_dataset_id.setter
    def preset_dataset_id(self, preset_dataset_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_id = preset_dataset_id

    @property
    def preset_dataset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.preset_dataset_type

    @preset_dataset_type.setter
    def preset_dataset_type(self, preset_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dataset_type = preset_dataset_type

    @property
    def preset_dashboard(self) -> Optional[PresetDashboard]:
        return None if self.attributes is None else self.attributes.preset_dashboard

    @preset_dashboard.setter
    def preset_dashboard(self, preset_dashboard: Optional[PresetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard = preset_dashboard

    class Attributes(Preset.Attributes):
        preset_dataset_datasource_name: Optional[str] = Field(
            None, description="", alias="presetDatasetDatasourceName"
        )
        preset_dataset_id: Optional[int] = Field(
            None, description="", alias="presetDatasetId"
        )
        preset_dataset_type: Optional[str] = Field(
            None, description="", alias="presetDatasetType"
        )
        preset_dashboard: Optional[PresetDashboard] = Field(
            None, description="", alias="presetDashboard"
        )  # relationship

    attributes: "PresetDataset.Attributes" = Field(
        default_factory=lambda: PresetDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetDashboard(Preset):
    """Description"""

    type_name: str = Field("PresetDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDashboard":
            raise ValueError("must be PresetDashboard")
        return v

    def __setattr__(self, name, value):
        if name in PresetDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_DASHBOARD_CHANGED_BY_NAME: ClassVar[
        KeywordTextStemmedField
    ] = KeywordTextStemmedField(
        "presetDashboardChangedByName",
        "presetDashboardChangedByName.keyword",
        "presetDashboardChangedByName",
        "presetDashboardChangedByName.stemmed",
    )
    """
    TBC
    """
    PRESET_DASHBOARD_CHANGED_BY_URL: ClassVar[KeywordField] = KeywordField(
        "presetDashboardChangedByURL", "presetDashboardChangedByURL"
    )
    """
    TBC
    """
    PRESET_DASHBOARD_IS_MANAGED_EXTERNALLY: ClassVar[BooleanField] = BooleanField(
        "presetDashboardIsManagedExternally", "presetDashboardIsManagedExternally"
    )
    """
    TBC
    """
    PRESET_DASHBOARD_IS_PUBLISHED: ClassVar[BooleanField] = BooleanField(
        "presetDashboardIsPublished", "presetDashboardIsPublished"
    )
    """
    TBC
    """
    PRESET_DASHBOARD_THUMBNAIL_URL: ClassVar[KeywordField] = KeywordField(
        "presetDashboardThumbnailURL", "presetDashboardThumbnailURL"
    )
    """
    TBC
    """
    PRESET_DASHBOARD_CHART_COUNT: ClassVar[NumericField] = NumericField(
        "presetDashboardChartCount", "presetDashboardChartCount"
    )
    """
    TBC
    """

    PRESET_DATASETS: ClassVar[RelationField] = RelationField("presetDatasets")
    """
    TBC
    """
    PRESET_CHARTS: ClassVar[RelationField] = RelationField("presetCharts")
    """
    TBC
    """
    PRESET_WORKSPACE: ClassVar[RelationField] = RelationField("presetWorkspace")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "preset_dashboard_changed_by_name",
        "preset_dashboard_changed_by_url",
        "preset_dashboard_is_managed_externally",
        "preset_dashboard_is_published",
        "preset_dashboard_thumbnail_url",
        "preset_dashboard_chart_count",
        "preset_datasets",
        "preset_charts",
        "preset_workspace",
    ]

    @property
    def preset_dashboard_changed_by_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_changed_by_name
        )

    @preset_dashboard_changed_by_name.setter
    def preset_dashboard_changed_by_name(
        self, preset_dashboard_changed_by_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_changed_by_name = (
            preset_dashboard_changed_by_name
        )

    @property
    def preset_dashboard_changed_by_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_changed_by_url
        )

    @preset_dashboard_changed_by_url.setter
    def preset_dashboard_changed_by_url(
        self, preset_dashboard_changed_by_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_changed_by_url = (
            preset_dashboard_changed_by_url
        )

    @property
    def preset_dashboard_is_managed_externally(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_is_managed_externally
        )

    @preset_dashboard_is_managed_externally.setter
    def preset_dashboard_is_managed_externally(
        self, preset_dashboard_is_managed_externally: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_is_managed_externally = (
            preset_dashboard_is_managed_externally
        )

    @property
    def preset_dashboard_is_published(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_is_published
        )

    @preset_dashboard_is_published.setter
    def preset_dashboard_is_published(
        self, preset_dashboard_is_published: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_is_published = preset_dashboard_is_published

    @property
    def preset_dashboard_thumbnail_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_thumbnail_url
        )

    @preset_dashboard_thumbnail_url.setter
    def preset_dashboard_thumbnail_url(
        self, preset_dashboard_thumbnail_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_thumbnail_url = preset_dashboard_thumbnail_url

    @property
    def preset_dashboard_chart_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_chart_count
        )

    @preset_dashboard_chart_count.setter
    def preset_dashboard_chart_count(self, preset_dashboard_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_chart_count = preset_dashboard_chart_count

    @property
    def preset_datasets(self) -> Optional[list[PresetDataset]]:
        return None if self.attributes is None else self.attributes.preset_datasets

    @preset_datasets.setter
    def preset_datasets(self, preset_datasets: Optional[list[PresetDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_datasets = preset_datasets

    @property
    def preset_charts(self) -> Optional[list[PresetChart]]:
        return None if self.attributes is None else self.attributes.preset_charts

    @preset_charts.setter
    def preset_charts(self, preset_charts: Optional[list[PresetChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_charts = preset_charts

    @property
    def preset_workspace(self) -> Optional[PresetWorkspace]:
        return None if self.attributes is None else self.attributes.preset_workspace

    @preset_workspace.setter
    def preset_workspace(self, preset_workspace: Optional[PresetWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace = preset_workspace

    class Attributes(Preset.Attributes):
        preset_dashboard_changed_by_name: Optional[str] = Field(
            None, description="", alias="presetDashboardChangedByName"
        )
        preset_dashboard_changed_by_url: Optional[str] = Field(
            None, description="", alias="presetDashboardChangedByURL"
        )
        preset_dashboard_is_managed_externally: Optional[bool] = Field(
            None, description="", alias="presetDashboardIsManagedExternally"
        )
        preset_dashboard_is_published: Optional[bool] = Field(
            None, description="", alias="presetDashboardIsPublished"
        )
        preset_dashboard_thumbnail_url: Optional[str] = Field(
            None, description="", alias="presetDashboardThumbnailURL"
        )
        preset_dashboard_chart_count: Optional[int] = Field(
            None, description="", alias="presetDashboardChartCount"
        )
        preset_datasets: Optional[list[PresetDataset]] = Field(
            None, description="", alias="presetDatasets"
        )  # relationship
        preset_charts: Optional[list[PresetChart]] = Field(
            None, description="", alias="presetCharts"
        )  # relationship
        preset_workspace: Optional[PresetWorkspace] = Field(
            None, description="", alias="presetWorkspace"
        )  # relationship

    attributes: "PresetDashboard.Attributes" = Field(
        default_factory=lambda: PresetDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PresetWorkspace(Preset):
    """Description"""

    type_name: str = Field("PresetWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetWorkspace":
            raise ValueError("must be PresetWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in PresetWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_WORKSPACE_PUBLIC_DASHBOARDS_ALLOWED: ClassVar[BooleanField] = BooleanField(
        "presetWorkspacePublicDashboardsAllowed",
        "presetWorkspacePublicDashboardsAllowed",
    )
    """
    TBC
    """
    PRESET_WORKSPACE_CLUSTER_ID: ClassVar[NumericField] = NumericField(
        "presetWorkspaceClusterId", "presetWorkspaceClusterId"
    )
    """
    TBC
    """
    PRESET_WORKSPACE_HOSTNAME: ClassVar[KeywordTextField] = KeywordTextField(
        "presetWorkspaceHostname",
        "presetWorkspaceHostname",
        "presetWorkspaceHostname.text",
    )
    """
    TBC
    """
    PRESET_WORKSPACE_IS_IN_MAINTENANCE_MODE: ClassVar[BooleanField] = BooleanField(
        "presetWorkspaceIsInMaintenanceMode", "presetWorkspaceIsInMaintenanceMode"
    )
    """
    TBC
    """
    PRESET_WORKSPACE_REGION: ClassVar[KeywordTextField] = KeywordTextField(
        "presetWorkspaceRegion", "presetWorkspaceRegion", "presetWorkspaceRegion.text"
    )
    """
    TBC
    """
    PRESET_WORKSPACE_STATUS: ClassVar[KeywordField] = KeywordField(
        "presetWorkspaceStatus", "presetWorkspaceStatus"
    )
    """
    TBC
    """
    PRESET_WORKSPACE_DEPLOYMENT_ID: ClassVar[NumericField] = NumericField(
        "presetWorkspaceDeploymentId", "presetWorkspaceDeploymentId"
    )
    """
    TBC
    """
    PRESET_WORKSPACE_DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "presetWorkspaceDashboardCount", "presetWorkspaceDashboardCount"
    )
    """
    TBC
    """
    PRESET_WORKSPACE_DATASET_COUNT: ClassVar[NumericField] = NumericField(
        "presetWorkspaceDatasetCount", "presetWorkspaceDatasetCount"
    )
    """
    TBC
    """

    PRESET_DASHBOARDS: ClassVar[RelationField] = RelationField("presetDashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "preset_workspace_public_dashboards_allowed",
        "preset_workspace_cluster_id",
        "preset_workspace_hostname",
        "preset_workspace_is_in_maintenance_mode",
        "preset_workspace_region",
        "preset_workspace_status",
        "preset_workspace_deployment_id",
        "preset_workspace_dashboard_count",
        "preset_workspace_dataset_count",
        "preset_dashboards",
    ]

    @property
    def preset_workspace_public_dashboards_allowed(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_public_dashboards_allowed
        )

    @preset_workspace_public_dashboards_allowed.setter
    def preset_workspace_public_dashboards_allowed(
        self, preset_workspace_public_dashboards_allowed: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_public_dashboards_allowed = (
            preset_workspace_public_dashboards_allowed
        )

    @property
    def preset_workspace_cluster_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_cluster_id
        )

    @preset_workspace_cluster_id.setter
    def preset_workspace_cluster_id(self, preset_workspace_cluster_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_cluster_id = preset_workspace_cluster_id

    @property
    def preset_workspace_hostname(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_hostname
        )

    @preset_workspace_hostname.setter
    def preset_workspace_hostname(self, preset_workspace_hostname: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_hostname = preset_workspace_hostname

    @property
    def preset_workspace_is_in_maintenance_mode(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_is_in_maintenance_mode
        )

    @preset_workspace_is_in_maintenance_mode.setter
    def preset_workspace_is_in_maintenance_mode(
        self, preset_workspace_is_in_maintenance_mode: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_is_in_maintenance_mode = (
            preset_workspace_is_in_maintenance_mode
        )

    @property
    def preset_workspace_region(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.preset_workspace_region
        )

    @preset_workspace_region.setter
    def preset_workspace_region(self, preset_workspace_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_region = preset_workspace_region

    @property
    def preset_workspace_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.preset_workspace_status
        )

    @preset_workspace_status.setter
    def preset_workspace_status(self, preset_workspace_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_status = preset_workspace_status

    @property
    def preset_workspace_deployment_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_deployment_id
        )

    @preset_workspace_deployment_id.setter
    def preset_workspace_deployment_id(
        self, preset_workspace_deployment_id: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_deployment_id = preset_workspace_deployment_id

    @property
    def preset_workspace_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_dashboard_count
        )

    @preset_workspace_dashboard_count.setter
    def preset_workspace_dashboard_count(
        self, preset_workspace_dashboard_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_dashboard_count = (
            preset_workspace_dashboard_count
        )

    @property
    def preset_workspace_dataset_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_dataset_count
        )

    @preset_workspace_dataset_count.setter
    def preset_workspace_dataset_count(
        self, preset_workspace_dataset_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_dataset_count = preset_workspace_dataset_count

    @property
    def preset_dashboards(self) -> Optional[list[PresetDashboard]]:
        return None if self.attributes is None else self.attributes.preset_dashboards

    @preset_dashboards.setter
    def preset_dashboards(self, preset_dashboards: Optional[list[PresetDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboards = preset_dashboards

    class Attributes(Preset.Attributes):
        preset_workspace_public_dashboards_allowed: Optional[bool] = Field(
            None, description="", alias="presetWorkspacePublicDashboardsAllowed"
        )
        preset_workspace_cluster_id: Optional[int] = Field(
            None, description="", alias="presetWorkspaceClusterId"
        )
        preset_workspace_hostname: Optional[str] = Field(
            None, description="", alias="presetWorkspaceHostname"
        )
        preset_workspace_is_in_maintenance_mode: Optional[bool] = Field(
            None, description="", alias="presetWorkspaceIsInMaintenanceMode"
        )
        preset_workspace_region: Optional[str] = Field(
            None, description="", alias="presetWorkspaceRegion"
        )
        preset_workspace_status: Optional[str] = Field(
            None, description="", alias="presetWorkspaceStatus"
        )
        preset_workspace_deployment_id: Optional[int] = Field(
            None, description="", alias="presetWorkspaceDeploymentId"
        )
        preset_workspace_dashboard_count: Optional[int] = Field(
            None, description="", alias="presetWorkspaceDashboardCount"
        )
        preset_workspace_dataset_count: Optional[int] = Field(
            None, description="", alias="presetWorkspaceDatasetCount"
        )
        preset_dashboards: Optional[list[PresetDashboard]] = Field(
            None, description="", alias="presetDashboards"
        )  # relationship

    attributes: "PresetWorkspace.Attributes" = Field(
        default_factory=lambda: PresetWorkspace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


PresetChart.Attributes.update_forward_refs()


PresetDataset.Attributes.update_forward_refs()


PresetDashboard.Attributes.update_forward_refs()


PresetWorkspace.Attributes.update_forward_refs()
