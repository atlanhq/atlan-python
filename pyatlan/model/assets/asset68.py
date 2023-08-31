# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.enums import (
    QuickSightAnalysisStatus,
    QuickSightDatasetFieldType,
    QuickSightDatasetImportMode,
    QuickSightFolderType,
)
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .asset44 import QuickSight


class QuickSightFolder(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightFolder":
            raise ValueError("must be QuickSightFolder")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_FOLDER_TYPE: ClassVar[KeywordField] = KeywordField(
        "quickSightFolderType", "quickSightFolderType"
    )
    """
    Shared or private type of folder
    """
    QUICK_SIGHT_FOLDER_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "quickSightFolderHierarchy", "quickSightFolderHierarchy"
    )
    """
    Detailed path of the folder
    """

    QUICK_SIGHT_DASHBOARDS: ClassVar[RelationField] = RelationField(
        "quickSightDashboards"
    )
    """
    TBC
    """
    QUICK_SIGHT_DATASETS: ClassVar[RelationField] = RelationField("quickSightDatasets")
    """
    TBC
    """
    QUICK_SIGHT_ANALYSES: ClassVar[RelationField] = RelationField("quickSightAnalyses")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_folder_type",
        "quick_sight_folder_hierarchy",
        "quick_sight_dashboards",
        "quick_sight_datasets",
        "quick_sight_analyses",
    ]

    @property
    def quick_sight_folder_type(self) -> Optional[QuickSightFolderType]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_folder_type
        )

    @quick_sight_folder_type.setter
    def quick_sight_folder_type(
        self, quick_sight_folder_type: Optional[QuickSightFolderType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_type = quick_sight_folder_type

    @property
    def quick_sight_folder_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_folder_hierarchy
        )

    @quick_sight_folder_hierarchy.setter
    def quick_sight_folder_hierarchy(
        self, quick_sight_folder_hierarchy: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_folder_hierarchy = quick_sight_folder_hierarchy

    @property
    def quick_sight_dashboards(self) -> Optional[list[QuickSightDashboard]]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_dashboards
        )

    @quick_sight_dashboards.setter
    def quick_sight_dashboards(
        self, quick_sight_dashboards: Optional[list[QuickSightDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboards = quick_sight_dashboards

    @property
    def quick_sight_datasets(self) -> Optional[list[QuickSightDataset]]:
        return None if self.attributes is None else self.attributes.quick_sight_datasets

    @quick_sight_datasets.setter
    def quick_sight_datasets(
        self, quick_sight_datasets: Optional[list[QuickSightDataset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_datasets = quick_sight_datasets

    @property
    def quick_sight_analyses(self) -> Optional[list[QuickSightAnalysis]]:
        return None if self.attributes is None else self.attributes.quick_sight_analyses

    @quick_sight_analyses.setter
    def quick_sight_analyses(
        self, quick_sight_analyses: Optional[list[QuickSightAnalysis]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analyses = quick_sight_analyses

    class Attributes(QuickSight.Attributes):
        quick_sight_folder_type: Optional[QuickSightFolderType] = Field(
            None, description="", alias="quickSightFolderType"
        )
        quick_sight_folder_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="quickSightFolderHierarchy"
        )
        quick_sight_dashboards: Optional[list[QuickSightDashboard]] = Field(
            None, description="", alias="quickSightDashboards"
        )  # relationship
        quick_sight_datasets: Optional[list[QuickSightDataset]] = Field(
            None, description="", alias="quickSightDatasets"
        )  # relationship
        quick_sight_analyses: Optional[list[QuickSightAnalysis]] = Field(
            None, description="", alias="quickSightAnalyses"
        )  # relationship

    attributes: "QuickSightFolder.Attributes" = Field(
        default_factory=lambda: QuickSightFolder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDashboardVisual(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDashboardVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboardVisual":
            raise ValueError("must be QuickSightDashboardVisual")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDashboardVisual._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DASHBOARD_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "quickSightDashboardQualifiedName",
        "quickSightDashboardQualifiedName",
        "quickSightDashboardQualifiedName.text",
    )
    """
    TBC
    """

    QUICK_SIGHT_DASHBOARD: ClassVar[RelationField] = RelationField(
        "quickSightDashboard"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_dashboard_qualified_name",
        "quick_sight_dashboard",
    ]

    @property
    def quick_sight_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_qualified_name
        )

    @quick_sight_dashboard_qualified_name.setter
    def quick_sight_dashboard_qualified_name(
        self, quick_sight_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_qualified_name = (
            quick_sight_dashboard_qualified_name
        )

    @property
    def quick_sight_dashboard(self) -> Optional[QuickSightDashboard]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_dashboard
        )

    @quick_sight_dashboard.setter
    def quick_sight_dashboard(
        self, quick_sight_dashboard: Optional[QuickSightDashboard]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard = quick_sight_dashboard

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightDashboardQualifiedName"
        )
        quick_sight_dashboard: Optional[QuickSightDashboard] = Field(
            None, description="", alias="quickSightDashboard"
        )  # relationship

    attributes: "QuickSightDashboardVisual.Attributes" = Field(
        default_factory=lambda: QuickSightDashboardVisual.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightAnalysisVisual(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightAnalysisVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysisVisual":
            raise ValueError("must be QuickSightAnalysisVisual")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightAnalysisVisual._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_ANALYSIS_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "quickSightAnalysisQualifiedName",
        "quickSightAnalysisQualifiedName",
        "quickSightAnalysisQualifiedName.text",
    )
    """
    Qualified name of the QuickSight Analysis
    """

    QUICK_SIGHT_ANALYSIS: ClassVar[RelationField] = RelationField("quickSightAnalysis")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_analysis_qualified_name",
        "quick_sight_analysis",
    ]

    @property
    def quick_sight_analysis_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_qualified_name
        )

    @quick_sight_analysis_qualified_name.setter
    def quick_sight_analysis_qualified_name(
        self, quick_sight_analysis_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_qualified_name = (
            quick_sight_analysis_qualified_name
        )

    @property
    def quick_sight_analysis(self) -> Optional[QuickSightAnalysis]:
        return None if self.attributes is None else self.attributes.quick_sight_analysis

    @quick_sight_analysis.setter
    def quick_sight_analysis(self, quick_sight_analysis: Optional[QuickSightAnalysis]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis = quick_sight_analysis

    class Attributes(QuickSight.Attributes):
        quick_sight_analysis_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightAnalysisQualifiedName"
        )
        quick_sight_analysis: Optional[QuickSightAnalysis] = Field(
            None, description="", alias="quickSightAnalysis"
        )  # relationship

    attributes: "QuickSightAnalysisVisual.Attributes" = Field(
        default_factory=lambda: QuickSightAnalysisVisual.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDatasetField(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDatasetField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDatasetField":
            raise ValueError("must be QuickSightDatasetField")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDatasetField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DATASET_FIELD_TYPE: ClassVar[KeywordField] = KeywordField(
        "quickSightDatasetFieldType", "quickSightDatasetFieldType"
    )
    """
    Datatype of column in the dataset
    """
    QUICK_SIGHT_DATASET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "quickSightDatasetQualifiedName",
        "quickSightDatasetQualifiedName",
        "quickSightDatasetQualifiedName.text",
    )
    """
    Qualified name of the parent dataset
    """

    QUICK_SIGHT_DATASET: ClassVar[RelationField] = RelationField("quickSightDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_dataset_field_type",
        "quick_sight_dataset_qualified_name",
        "quick_sight_dataset",
    ]

    @property
    def quick_sight_dataset_field_type(self) -> Optional[QuickSightDatasetFieldType]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_field_type
        )

    @quick_sight_dataset_field_type.setter
    def quick_sight_dataset_field_type(
        self, quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_field_type = quick_sight_dataset_field_type

    @property
    def quick_sight_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_qualified_name
        )

    @quick_sight_dataset_qualified_name.setter
    def quick_sight_dataset_qualified_name(
        self, quick_sight_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_qualified_name = (
            quick_sight_dataset_qualified_name
        )

    @property
    def quick_sight_dataset(self) -> Optional[QuickSightDataset]:
        return None if self.attributes is None else self.attributes.quick_sight_dataset

    @quick_sight_dataset.setter
    def quick_sight_dataset(self, quick_sight_dataset: Optional[QuickSightDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset = quick_sight_dataset

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType] = Field(
            None, description="", alias="quickSightDatasetFieldType"
        )
        quick_sight_dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="quickSightDatasetQualifiedName"
        )
        quick_sight_dataset: Optional[QuickSightDataset] = Field(
            None, description="", alias="quickSightDataset"
        )  # relationship

    attributes: "QuickSightDatasetField.Attributes" = Field(
        default_factory=lambda: QuickSightDatasetField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightAnalysis(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightAnalysis", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightAnalysis":
            raise ValueError("must be QuickSightAnalysis")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightAnalysis._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_ANALYSIS_STATUS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisStatus", "quickSightAnalysisStatus"
    )
    """
    Status of quicksight analysis
    """
    QUICK_SIGHT_ANALYSIS_CALCULATED_FIELDS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisCalculatedFields", "quickSightAnalysisCalculatedFields"
    )
    """
    Calculated fields of quicksight analysis
    """
    QUICK_SIGHT_ANALYSIS_PARAMETER_DECLARATIONS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisParameterDeclarations",
        "quickSightAnalysisParameterDeclarations",
    )
    """
    parameters used for quicksight analysis
    """
    QUICK_SIGHT_ANALYSIS_FILTER_GROUPS: ClassVar[KeywordField] = KeywordField(
        "quickSightAnalysisFilterGroups", "quickSightAnalysisFilterGroups"
    )
    """
    Filter groups used for quicksight analysis
    """

    QUICK_SIGHT_ANALYSIS_VISUALS: ClassVar[RelationField] = RelationField(
        "quickSightAnalysisVisuals"
    )
    """
    TBC
    """
    QUICK_SIGHT_ANALYSIS_FOLDERS: ClassVar[RelationField] = RelationField(
        "quickSightAnalysisFolders"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_analysis_status",
        "quick_sight_analysis_calculated_fields",
        "quick_sight_analysis_parameter_declarations",
        "quick_sight_analysis_filter_groups",
        "quick_sight_analysis_visuals",
        "quick_sight_analysis_folders",
    ]

    @property
    def quick_sight_analysis_status(self) -> Optional[QuickSightAnalysisStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_status
        )

    @quick_sight_analysis_status.setter
    def quick_sight_analysis_status(
        self, quick_sight_analysis_status: Optional[QuickSightAnalysisStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_status = quick_sight_analysis_status

    @property
    def quick_sight_analysis_calculated_fields(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_calculated_fields
        )

    @quick_sight_analysis_calculated_fields.setter
    def quick_sight_analysis_calculated_fields(
        self, quick_sight_analysis_calculated_fields: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_calculated_fields = (
            quick_sight_analysis_calculated_fields
        )

    @property
    def quick_sight_analysis_parameter_declarations(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_parameter_declarations
        )

    @quick_sight_analysis_parameter_declarations.setter
    def quick_sight_analysis_parameter_declarations(
        self, quick_sight_analysis_parameter_declarations: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_parameter_declarations = (
            quick_sight_analysis_parameter_declarations
        )

    @property
    def quick_sight_analysis_filter_groups(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_filter_groups
        )

    @quick_sight_analysis_filter_groups.setter
    def quick_sight_analysis_filter_groups(
        self, quick_sight_analysis_filter_groups: Optional[set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_filter_groups = (
            quick_sight_analysis_filter_groups
        )

    @property
    def quick_sight_analysis_visuals(self) -> Optional[list[QuickSightAnalysisVisual]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_visuals
        )

    @quick_sight_analysis_visuals.setter
    def quick_sight_analysis_visuals(
        self, quick_sight_analysis_visuals: Optional[list[QuickSightAnalysisVisual]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_visuals = quick_sight_analysis_visuals

    @property
    def quick_sight_analysis_folders(self) -> Optional[list[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_analysis_folders
        )

    @quick_sight_analysis_folders.setter
    def quick_sight_analysis_folders(
        self, quick_sight_analysis_folders: Optional[list[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_analysis_folders = quick_sight_analysis_folders

    class Attributes(QuickSight.Attributes):
        quick_sight_analysis_status: Optional[QuickSightAnalysisStatus] = Field(
            None, description="", alias="quickSightAnalysisStatus"
        )
        quick_sight_analysis_calculated_fields: Optional[set[str]] = Field(
            None, description="", alias="quickSightAnalysisCalculatedFields"
        )
        quick_sight_analysis_parameter_declarations: Optional[set[str]] = Field(
            None, description="", alias="quickSightAnalysisParameterDeclarations"
        )
        quick_sight_analysis_filter_groups: Optional[set[str]] = Field(
            None, description="", alias="quickSightAnalysisFilterGroups"
        )
        quick_sight_analysis_visuals: Optional[list[QuickSightAnalysisVisual]] = Field(
            None, description="", alias="quickSightAnalysisVisuals"
        )  # relationship
        quick_sight_analysis_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightAnalysisFolders"
        )  # relationship

    attributes: "QuickSightAnalysis.Attributes" = Field(
        default_factory=lambda: QuickSightAnalysis.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDashboard(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboard":
            raise ValueError("must be QuickSightDashboard")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DASHBOARD_PUBLISHED_VERSION_NUMBER: ClassVar[
        NumericField
    ] = NumericField(
        "quickSightDashboardPublishedVersionNumber",
        "quickSightDashboardPublishedVersionNumber",
    )
    """
    Version number of the dashboard published
    """
    QUICK_SIGHT_DASHBOARD_LAST_PUBLISHED_TIME: ClassVar[NumericField] = NumericField(
        "quickSightDashboardLastPublishedTime", "quickSightDashboardLastPublishedTime"
    )
    """
    Last published time of dashboard
    """

    QUICK_SIGHT_DASHBOARD_FOLDERS: ClassVar[RelationField] = RelationField(
        "quickSightDashboardFolders"
    )
    """
    TBC
    """
    QUICK_SIGHT_DASHBOARD_VISUALS: ClassVar[RelationField] = RelationField(
        "quickSightDashboardVisuals"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_dashboard_published_version_number",
        "quick_sight_dashboard_last_published_time",
        "quick_sight_dashboard_folders",
        "quick_sight_dashboard_visuals",
    ]

    @property
    def quick_sight_dashboard_published_version_number(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_published_version_number
        )

    @quick_sight_dashboard_published_version_number.setter
    def quick_sight_dashboard_published_version_number(
        self, quick_sight_dashboard_published_version_number: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_published_version_number = (
            quick_sight_dashboard_published_version_number
        )

    @property
    def quick_sight_dashboard_last_published_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_last_published_time
        )

    @quick_sight_dashboard_last_published_time.setter
    def quick_sight_dashboard_last_published_time(
        self, quick_sight_dashboard_last_published_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_last_published_time = (
            quick_sight_dashboard_last_published_time
        )

    @property
    def quick_sight_dashboard_folders(self) -> Optional[list[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_folders
        )

    @quick_sight_dashboard_folders.setter
    def quick_sight_dashboard_folders(
        self, quick_sight_dashboard_folders: Optional[list[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_folders = quick_sight_dashboard_folders

    @property
    def quick_sight_dashboard_visuals(
        self,
    ) -> Optional[list[QuickSightDashboardVisual]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_visuals
        )

    @quick_sight_dashboard_visuals.setter
    def quick_sight_dashboard_visuals(
        self, quick_sight_dashboard_visuals: Optional[list[QuickSightDashboardVisual]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_visuals = quick_sight_dashboard_visuals

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_published_version_number: Optional[int] = Field(
            None, description="", alias="quickSightDashboardPublishedVersionNumber"
        )
        quick_sight_dashboard_last_published_time: Optional[datetime] = Field(
            None, description="", alias="quickSightDashboardLastPublishedTime"
        )
        quick_sight_dashboard_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightDashboardFolders"
        )  # relationship
        quick_sight_dashboard_visuals: Optional[
            list[QuickSightDashboardVisual]
        ] = Field(
            None, description="", alias="quickSightDashboardVisuals"
        )  # relationship

    attributes: "QuickSightDashboard.Attributes" = Field(
        default_factory=lambda: QuickSightDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QuickSightDataset(QuickSight):
    """Description"""

    type_name: str = Field("QuickSightDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDataset":
            raise ValueError("must be QuickSightDataset")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DATASET_IMPORT_MODE: ClassVar[KeywordField] = KeywordField(
        "quickSightDatasetImportMode", "quickSightDatasetImportMode"
    )
    """
    Quicksight dataset importMode indicates a value that indicates whether you want to import the data into SPICE
    """
    QUICK_SIGHT_DATASET_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "quickSightDatasetColumnCount", "quickSightDatasetColumnCount"
    )
    """
    Quicksight dataset column count indicates number of columns present in the dataset
    """

    QUICK_SIGHT_DATASET_FOLDERS: ClassVar[RelationField] = RelationField(
        "quickSightDatasetFolders"
    )
    """
    TBC
    """
    QUICK_SIGHT_DATASET_FIELDS: ClassVar[RelationField] = RelationField(
        "quickSightDatasetFields"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "quick_sight_dataset_import_mode",
        "quick_sight_dataset_column_count",
        "quick_sight_dataset_folders",
        "quick_sight_dataset_fields",
    ]

    @property
    def quick_sight_dataset_import_mode(self) -> Optional[QuickSightDatasetImportMode]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_import_mode
        )

    @quick_sight_dataset_import_mode.setter
    def quick_sight_dataset_import_mode(
        self, quick_sight_dataset_import_mode: Optional[QuickSightDatasetImportMode]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_import_mode = (
            quick_sight_dataset_import_mode
        )

    @property
    def quick_sight_dataset_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_column_count
        )

    @quick_sight_dataset_column_count.setter
    def quick_sight_dataset_column_count(
        self, quick_sight_dataset_column_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_column_count = (
            quick_sight_dataset_column_count
        )

    @property
    def quick_sight_dataset_folders(self) -> Optional[list[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_folders
        )

    @quick_sight_dataset_folders.setter
    def quick_sight_dataset_folders(
        self, quick_sight_dataset_folders: Optional[list[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_folders = quick_sight_dataset_folders

    @property
    def quick_sight_dataset_fields(self) -> Optional[list[QuickSightDatasetField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_fields
        )

    @quick_sight_dataset_fields.setter
    def quick_sight_dataset_fields(
        self, quick_sight_dataset_fields: Optional[list[QuickSightDatasetField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_fields = quick_sight_dataset_fields

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_import_mode: Optional[QuickSightDatasetImportMode] = Field(
            None, description="", alias="quickSightDatasetImportMode"
        )
        quick_sight_dataset_column_count: Optional[int] = Field(
            None, description="", alias="quickSightDatasetColumnCount"
        )
        quick_sight_dataset_folders: Optional[list[QuickSightFolder]] = Field(
            None, description="", alias="quickSightDatasetFolders"
        )  # relationship
        quick_sight_dataset_fields: Optional[list[QuickSightDatasetField]] = Field(
            None, description="", alias="quickSightDatasetFields"
        )  # relationship

    attributes: "QuickSightDataset.Attributes" = Field(
        default_factory=lambda: QuickSightDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


QuickSightFolder.Attributes.update_forward_refs()


QuickSightDashboardVisual.Attributes.update_forward_refs()


QuickSightAnalysisVisual.Attributes.update_forward_refs()


QuickSightDatasetField.Attributes.update_forward_refs()


QuickSightAnalysis.Attributes.update_forward_refs()


QuickSightDashboard.Attributes.update_forward_refs()


QuickSightDataset.Attributes.update_forward_refs()
