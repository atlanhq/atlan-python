# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .asset46 import Sisense


class SisenseFolder(Sisense):
    """Description"""

    type_name: str = Field("SisenseFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseFolder":
            raise ValueError("must be SisenseFolder")
        return v

    def __setattr__(self, name, value):
        if name in SisenseFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_FOLDER_PARENT_FOLDER_QUALIFIED_NAME: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "sisenseFolderParentFolderQualifiedName",
        "sisenseFolderParentFolderQualifiedName",
        "sisenseFolderParentFolderQualifiedName.text",
    )
    """
    Unique name of the parent folder in which this folder exists.
    """

    SISENSE_CHILD_FOLDERS: ClassVar[RelationField] = RelationField(
        "sisenseChildFolders"
    )
    """
    TBC
    """
    SISENSE_WIDGETS: ClassVar[RelationField] = RelationField("sisenseWidgets")
    """
    TBC
    """
    SISENSE_DASHBOARDS: ClassVar[RelationField] = RelationField("sisenseDashboards")
    """
    TBC
    """
    SISENSE_PARENT_FOLDER: ClassVar[RelationField] = RelationField(
        "sisenseParentFolder"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sisense_folder_parent_folder_qualified_name",
        "sisense_child_folders",
        "sisense_widgets",
        "sisense_dashboards",
        "sisense_parent_folder",
    ]

    @property
    def sisense_folder_parent_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_folder_parent_folder_qualified_name
        )

    @sisense_folder_parent_folder_qualified_name.setter
    def sisense_folder_parent_folder_qualified_name(
        self, sisense_folder_parent_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_folder_parent_folder_qualified_name = (
            sisense_folder_parent_folder_qualified_name
        )

    @property
    def sisense_child_folders(self) -> Optional[list[SisenseFolder]]:
        return (
            None if self.attributes is None else self.attributes.sisense_child_folders
        )

    @sisense_child_folders.setter
    def sisense_child_folders(
        self, sisense_child_folders: Optional[list[SisenseFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_child_folders = sisense_child_folders

    @property
    def sisense_widgets(self) -> Optional[list[SisenseWidget]]:
        return None if self.attributes is None else self.attributes.sisense_widgets

    @sisense_widgets.setter
    def sisense_widgets(self, sisense_widgets: Optional[list[SisenseWidget]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widgets = sisense_widgets

    @property
    def sisense_dashboards(self) -> Optional[list[SisenseDashboard]]:
        return None if self.attributes is None else self.attributes.sisense_dashboards

    @sisense_dashboards.setter
    def sisense_dashboards(self, sisense_dashboards: Optional[list[SisenseDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboards = sisense_dashboards

    @property
    def sisense_parent_folder(self) -> Optional[SisenseFolder]:
        return (
            None if self.attributes is None else self.attributes.sisense_parent_folder
        )

    @sisense_parent_folder.setter
    def sisense_parent_folder(self, sisense_parent_folder: Optional[SisenseFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_parent_folder = sisense_parent_folder

    class Attributes(Sisense.Attributes):
        sisense_folder_parent_folder_qualified_name: Optional[str] = Field(
            None, description="", alias="sisenseFolderParentFolderQualifiedName"
        )
        sisense_child_folders: Optional[list[SisenseFolder]] = Field(
            None, description="", alias="sisenseChildFolders"
        )  # relationship
        sisense_widgets: Optional[list[SisenseWidget]] = Field(
            None, description="", alias="sisenseWidgets"
        )  # relationship
        sisense_dashboards: Optional[list[SisenseDashboard]] = Field(
            None, description="", alias="sisenseDashboards"
        )  # relationship
        sisense_parent_folder: Optional[SisenseFolder] = Field(
            None, description="", alias="sisenseParentFolder"
        )  # relationship

    attributes: "SisenseFolder.Attributes" = Field(
        default_factory=lambda: SisenseFolder.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SisenseWidget(Sisense):
    """Description"""

    type_name: str = Field("SisenseWidget", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseWidget":
            raise ValueError("must be SisenseWidget")
        return v

    def __setattr__(self, name, value):
        if name in SisenseWidget._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_WIDGET_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseWidgetColumnCount", "sisenseWidgetColumnCount"
    )
    """
    Number of columns used in this widget.
    """
    SISENSE_WIDGET_SUB_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseWidgetSubType", "sisenseWidgetSubType"
    )
    """
    Subtype of this widget.
    """
    SISENSE_WIDGET_SIZE: ClassVar[KeywordField] = KeywordField(
        "sisenseWidgetSize", "sisenseWidgetSize"
    )
    """
    Size of this widget.
    """
    SISENSE_WIDGET_DASHBOARD_QUALIFIED_NAME: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "sisenseWidgetDashboardQualifiedName",
        "sisenseWidgetDashboardQualifiedName",
        "sisenseWidgetDashboardQualifiedName.text",
    )
    """
    Unique name of the dashboard in which this widget exists.
    """
    SISENSE_WIDGET_FOLDER_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sisenseWidgetFolderQualifiedName",
        "sisenseWidgetFolderQualifiedName",
        "sisenseWidgetFolderQualifiedName.text",
    )
    """
    Unique name of the folder in which this widget exists.
    """

    SISENSE_DATAMODEL_TABLES: ClassVar[RelationField] = RelationField(
        "sisenseDatamodelTables"
    )
    """
    TBC
    """
    SISENSE_FOLDER: ClassVar[RelationField] = RelationField("sisenseFolder")
    """
    TBC
    """
    SISENSE_DASHBOARD: ClassVar[RelationField] = RelationField("sisenseDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sisense_widget_column_count",
        "sisense_widget_sub_type",
        "sisense_widget_size",
        "sisense_widget_dashboard_qualified_name",
        "sisense_widget_folder_qualified_name",
        "sisense_datamodel_tables",
        "sisense_folder",
        "sisense_dashboard",
    ]

    @property
    def sisense_widget_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_widget_column_count
        )

    @sisense_widget_column_count.setter
    def sisense_widget_column_count(self, sisense_widget_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_column_count = sisense_widget_column_count

    @property
    def sisense_widget_sub_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sisense_widget_sub_type
        )

    @sisense_widget_sub_type.setter
    def sisense_widget_sub_type(self, sisense_widget_sub_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_sub_type = sisense_widget_sub_type

    @property
    def sisense_widget_size(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sisense_widget_size

    @sisense_widget_size.setter
    def sisense_widget_size(self, sisense_widget_size: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_size = sisense_widget_size

    @property
    def sisense_widget_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_widget_dashboard_qualified_name
        )

    @sisense_widget_dashboard_qualified_name.setter
    def sisense_widget_dashboard_qualified_name(
        self, sisense_widget_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_dashboard_qualified_name = (
            sisense_widget_dashboard_qualified_name
        )

    @property
    def sisense_widget_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_widget_folder_qualified_name
        )

    @sisense_widget_folder_qualified_name.setter
    def sisense_widget_folder_qualified_name(
        self, sisense_widget_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_folder_qualified_name = (
            sisense_widget_folder_qualified_name
        )

    @property
    def sisense_datamodel_tables(self) -> Optional[list[SisenseDatamodelTable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_tables
        )

    @sisense_datamodel_tables.setter
    def sisense_datamodel_tables(
        self, sisense_datamodel_tables: Optional[list[SisenseDatamodelTable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_tables = sisense_datamodel_tables

    @property
    def sisense_folder(self) -> Optional[SisenseFolder]:
        return None if self.attributes is None else self.attributes.sisense_folder

    @sisense_folder.setter
    def sisense_folder(self, sisense_folder: Optional[SisenseFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_folder = sisense_folder

    @property
    def sisense_dashboard(self) -> Optional[SisenseDashboard]:
        return None if self.attributes is None else self.attributes.sisense_dashboard

    @sisense_dashboard.setter
    def sisense_dashboard(self, sisense_dashboard: Optional[SisenseDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboard = sisense_dashboard

    class Attributes(Sisense.Attributes):
        sisense_widget_column_count: Optional[int] = Field(
            None, description="", alias="sisenseWidgetColumnCount"
        )
        sisense_widget_sub_type: Optional[str] = Field(
            None, description="", alias="sisenseWidgetSubType"
        )
        sisense_widget_size: Optional[str] = Field(
            None, description="", alias="sisenseWidgetSize"
        )
        sisense_widget_dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="sisenseWidgetDashboardQualifiedName"
        )
        sisense_widget_folder_qualified_name: Optional[str] = Field(
            None, description="", alias="sisenseWidgetFolderQualifiedName"
        )
        sisense_datamodel_tables: Optional[list[SisenseDatamodelTable]] = Field(
            None, description="", alias="sisenseDatamodelTables"
        )  # relationship
        sisense_folder: Optional[SisenseFolder] = Field(
            None, description="", alias="sisenseFolder"
        )  # relationship
        sisense_dashboard: Optional[SisenseDashboard] = Field(
            None, description="", alias="sisenseDashboard"
        )  # relationship

    attributes: "SisenseWidget.Attributes" = Field(
        default_factory=lambda: SisenseWidget.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SisenseDatamodel(Sisense):
    """Description"""

    type_name: str = Field("SisenseDatamodel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseDatamodel":
            raise ValueError("must be SisenseDatamodel")
        return v

    def __setattr__(self, name, value):
        if name in SisenseDatamodel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_DATAMODEL_TABLE_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelTableCount", "sisenseDatamodelTableCount"
    )
    """
    Number of tables in this datamodel.
    """
    SISENSE_DATAMODEL_SERVER: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelServer", "sisenseDatamodelServer"
    )
    """
    Hostname of the server on which this datamodel was created.
    """
    SISENSE_DATAMODEL_REVISION: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelRevision", "sisenseDatamodelRevision"
    )
    """
    Revision of this datamodel.
    """
    SISENSE_DATAMODEL_LAST_BUILD_TIME: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelLastBuildTime", "sisenseDatamodelLastBuildTime"
    )
    """
    Time (epoch) when this datamodel was last built, in milliseconds.
    """
    SISENSE_DATAMODEL_LAST_SUCCESSFUL_BUILD_TIME: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelLastSuccessfulBuildTime",
        "sisenseDatamodelLastSuccessfulBuildTime",
    )
    """
    Time (epoch) when this datamodel was last built successfully, in milliseconds.
    """
    SISENSE_DATAMODEL_LAST_PUBLISH_TIME: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelLastPublishTime", "sisenseDatamodelLastPublishTime"
    )
    """
    Time (epoch) when this datamodel was last published, in milliseconds.
    """
    SISENSE_DATAMODEL_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelType", "sisenseDatamodelType"
    )
    """
    Type of this datamodel, for example: 'extract' or 'custom'.
    """
    SISENSE_DATAMODEL_RELATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelRelationType", "sisenseDatamodelRelationType"
    )
    """
    Default relation type for this datamodel. 'extract' type Datamodels have regular relations by default. 'live' type Datamodels have direct relations by default.
    """  # noqa: E501

    SISENSE_DATAMODEL_TABLES: ClassVar[RelationField] = RelationField(
        "sisenseDatamodelTables"
    )
    """
    TBC
    """
    SISENSE_DASHBOARDS: ClassVar[RelationField] = RelationField("sisenseDashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sisense_datamodel_table_count",
        "sisense_datamodel_server",
        "sisense_datamodel_revision",
        "sisense_datamodel_last_build_time",
        "sisense_datamodel_last_successful_build_time",
        "sisense_datamodel_last_publish_time",
        "sisense_datamodel_type",
        "sisense_datamodel_relation_type",
        "sisense_datamodel_tables",
        "sisense_dashboards",
    ]

    @property
    def sisense_datamodel_table_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_count
        )

    @sisense_datamodel_table_count.setter
    def sisense_datamodel_table_count(
        self, sisense_datamodel_table_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_count = sisense_datamodel_table_count

    @property
    def sisense_datamodel_server(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_server
        )

    @sisense_datamodel_server.setter
    def sisense_datamodel_server(self, sisense_datamodel_server: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_server = sisense_datamodel_server

    @property
    def sisense_datamodel_revision(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_revision
        )

    @sisense_datamodel_revision.setter
    def sisense_datamodel_revision(self, sisense_datamodel_revision: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_revision = sisense_datamodel_revision

    @property
    def sisense_datamodel_last_build_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_last_build_time
        )

    @sisense_datamodel_last_build_time.setter
    def sisense_datamodel_last_build_time(
        self, sisense_datamodel_last_build_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_last_build_time = (
            sisense_datamodel_last_build_time
        )

    @property
    def sisense_datamodel_last_successful_build_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_last_successful_build_time
        )

    @sisense_datamodel_last_successful_build_time.setter
    def sisense_datamodel_last_successful_build_time(
        self, sisense_datamodel_last_successful_build_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_last_successful_build_time = (
            sisense_datamodel_last_successful_build_time
        )

    @property
    def sisense_datamodel_last_publish_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_last_publish_time
        )

    @sisense_datamodel_last_publish_time.setter
    def sisense_datamodel_last_publish_time(
        self, sisense_datamodel_last_publish_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_last_publish_time = (
            sisense_datamodel_last_publish_time
        )

    @property
    def sisense_datamodel_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sisense_datamodel_type
        )

    @sisense_datamodel_type.setter
    def sisense_datamodel_type(self, sisense_datamodel_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_type = sisense_datamodel_type

    @property
    def sisense_datamodel_relation_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_relation_type
        )

    @sisense_datamodel_relation_type.setter
    def sisense_datamodel_relation_type(
        self, sisense_datamodel_relation_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_relation_type = (
            sisense_datamodel_relation_type
        )

    @property
    def sisense_datamodel_tables(self) -> Optional[list[SisenseDatamodelTable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_tables
        )

    @sisense_datamodel_tables.setter
    def sisense_datamodel_tables(
        self, sisense_datamodel_tables: Optional[list[SisenseDatamodelTable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_tables = sisense_datamodel_tables

    @property
    def sisense_dashboards(self) -> Optional[list[SisenseDashboard]]:
        return None if self.attributes is None else self.attributes.sisense_dashboards

    @sisense_dashboards.setter
    def sisense_dashboards(self, sisense_dashboards: Optional[list[SisenseDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboards = sisense_dashboards

    class Attributes(Sisense.Attributes):
        sisense_datamodel_table_count: Optional[int] = Field(
            None, description="", alias="sisenseDatamodelTableCount"
        )
        sisense_datamodel_server: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelServer"
        )
        sisense_datamodel_revision: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelRevision"
        )
        sisense_datamodel_last_build_time: Optional[datetime] = Field(
            None, description="", alias="sisenseDatamodelLastBuildTime"
        )
        sisense_datamodel_last_successful_build_time: Optional[datetime] = Field(
            None, description="", alias="sisenseDatamodelLastSuccessfulBuildTime"
        )
        sisense_datamodel_last_publish_time: Optional[datetime] = Field(
            None, description="", alias="sisenseDatamodelLastPublishTime"
        )
        sisense_datamodel_type: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelType"
        )
        sisense_datamodel_relation_type: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelRelationType"
        )
        sisense_datamodel_tables: Optional[list[SisenseDatamodelTable]] = Field(
            None, description="", alias="sisenseDatamodelTables"
        )  # relationship
        sisense_dashboards: Optional[list[SisenseDashboard]] = Field(
            None, description="", alias="sisenseDashboards"
        )  # relationship

    attributes: "SisenseDatamodel.Attributes" = Field(
        default_factory=lambda: SisenseDatamodel.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SisenseDatamodelTable(Sisense):
    """Description"""

    type_name: str = Field("SisenseDatamodelTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseDatamodelTable":
            raise ValueError("must be SisenseDatamodelTable")
        return v

    def __setattr__(self, name, value):
        if name in SisenseDatamodelTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_DATAMODEL_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sisenseDatamodelQualifiedName",
        "sisenseDatamodelQualifiedName",
        "sisenseDatamodelQualifiedName.text",
    )
    """
    Unique name of the datamodel in which this datamodel table exists.
    """
    SISENSE_DATAMODEL_TABLE_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelTableColumnCount", "sisenseDatamodelTableColumnCount"
    )
    """
    Number of columns present in this datamodel table.
    """
    SISENSE_DATAMODEL_TABLE_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableType", "sisenseDatamodelTableType"
    )
    """
    Type of this datamodel table, for example: 'base' for regular tables, 'custom' for SQL expression-based tables.
    """
    SISENSE_DATAMODEL_TABLE_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableExpression", "sisenseDatamodelTableExpression"
    )
    """
    SQL expression of this datamodel table.
    """
    SISENSE_DATAMODEL_TABLE_IS_MATERIALIZED: ClassVar[BooleanField] = BooleanField(
        "sisenseDatamodelTableIsMaterialized", "sisenseDatamodelTableIsMaterialized"
    )
    """
    Whether this datamodel table is materialised (true) or not (false).
    """
    SISENSE_DATAMODEL_TABLE_IS_HIDDEN: ClassVar[BooleanField] = BooleanField(
        "sisenseDatamodelTableIsHidden", "sisenseDatamodelTableIsHidden"
    )
    """
    Whether this datamodel table is hidden in Sisense (true) or not (false).
    """
    SISENSE_DATAMODEL_TABLE_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableSchedule", "sisenseDatamodelTableSchedule"
    )
    """
    JSON specifying the refresh schedule of this datamodel table.
    """
    SISENSE_DATAMODEL_TABLE_LIVE_QUERY_SETTINGS: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableLiveQuerySettings",
        "sisenseDatamodelTableLiveQuerySettings",
    )
    """
    JSON specifying the LiveQuery settings of this datamodel table.
    """

    SISENSE_DATAMODEL: ClassVar[RelationField] = RelationField("sisenseDatamodel")
    """
    TBC
    """
    SISENSE_WIDGETS: ClassVar[RelationField] = RelationField("sisenseWidgets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sisense_datamodel_qualified_name",
        "sisense_datamodel_table_column_count",
        "sisense_datamodel_table_type",
        "sisense_datamodel_table_expression",
        "sisense_datamodel_table_is_materialized",
        "sisense_datamodel_table_is_hidden",
        "sisense_datamodel_table_schedule",
        "sisense_datamodel_table_live_query_settings",
        "sisense_datamodel",
        "sisense_widgets",
    ]

    @property
    def sisense_datamodel_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_qualified_name
        )

    @sisense_datamodel_qualified_name.setter
    def sisense_datamodel_qualified_name(
        self, sisense_datamodel_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_qualified_name = (
            sisense_datamodel_qualified_name
        )

    @property
    def sisense_datamodel_table_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_column_count
        )

    @sisense_datamodel_table_column_count.setter
    def sisense_datamodel_table_column_count(
        self, sisense_datamodel_table_column_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_column_count = (
            sisense_datamodel_table_column_count
        )

    @property
    def sisense_datamodel_table_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_type
        )

    @sisense_datamodel_table_type.setter
    def sisense_datamodel_table_type(self, sisense_datamodel_table_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_type = sisense_datamodel_table_type

    @property
    def sisense_datamodel_table_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_expression
        )

    @sisense_datamodel_table_expression.setter
    def sisense_datamodel_table_expression(
        self, sisense_datamodel_table_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_expression = (
            sisense_datamodel_table_expression
        )

    @property
    def sisense_datamodel_table_is_materialized(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_is_materialized
        )

    @sisense_datamodel_table_is_materialized.setter
    def sisense_datamodel_table_is_materialized(
        self, sisense_datamodel_table_is_materialized: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_is_materialized = (
            sisense_datamodel_table_is_materialized
        )

    @property
    def sisense_datamodel_table_is_hidden(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_is_hidden
        )

    @sisense_datamodel_table_is_hidden.setter
    def sisense_datamodel_table_is_hidden(
        self, sisense_datamodel_table_is_hidden: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_is_hidden = (
            sisense_datamodel_table_is_hidden
        )

    @property
    def sisense_datamodel_table_schedule(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_schedule
        )

    @sisense_datamodel_table_schedule.setter
    def sisense_datamodel_table_schedule(
        self, sisense_datamodel_table_schedule: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_schedule = (
            sisense_datamodel_table_schedule
        )

    @property
    def sisense_datamodel_table_live_query_settings(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_live_query_settings
        )

    @sisense_datamodel_table_live_query_settings.setter
    def sisense_datamodel_table_live_query_settings(
        self, sisense_datamodel_table_live_query_settings: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_live_query_settings = (
            sisense_datamodel_table_live_query_settings
        )

    @property
    def sisense_datamodel(self) -> Optional[SisenseDatamodel]:
        return None if self.attributes is None else self.attributes.sisense_datamodel

    @sisense_datamodel.setter
    def sisense_datamodel(self, sisense_datamodel: Optional[SisenseDatamodel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel = sisense_datamodel

    @property
    def sisense_widgets(self) -> Optional[list[SisenseWidget]]:
        return None if self.attributes is None else self.attributes.sisense_widgets

    @sisense_widgets.setter
    def sisense_widgets(self, sisense_widgets: Optional[list[SisenseWidget]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widgets = sisense_widgets

    class Attributes(Sisense.Attributes):
        sisense_datamodel_qualified_name: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelQualifiedName"
        )
        sisense_datamodel_table_column_count: Optional[int] = Field(
            None, description="", alias="sisenseDatamodelTableColumnCount"
        )
        sisense_datamodel_table_type: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelTableType"
        )
        sisense_datamodel_table_expression: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelTableExpression"
        )
        sisense_datamodel_table_is_materialized: Optional[bool] = Field(
            None, description="", alias="sisenseDatamodelTableIsMaterialized"
        )
        sisense_datamodel_table_is_hidden: Optional[bool] = Field(
            None, description="", alias="sisenseDatamodelTableIsHidden"
        )
        sisense_datamodel_table_schedule: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelTableSchedule"
        )
        sisense_datamodel_table_live_query_settings: Optional[str] = Field(
            None, description="", alias="sisenseDatamodelTableLiveQuerySettings"
        )
        sisense_datamodel: Optional[SisenseDatamodel] = Field(
            None, description="", alias="sisenseDatamodel"
        )  # relationship
        sisense_widgets: Optional[list[SisenseWidget]] = Field(
            None, description="", alias="sisenseWidgets"
        )  # relationship

    attributes: "SisenseDatamodelTable.Attributes" = Field(
        default_factory=lambda: SisenseDatamodelTable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SisenseDashboard(Sisense):
    """Description"""

    type_name: str = Field("SisenseDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseDashboard":
            raise ValueError("must be SisenseDashboard")
        return v

    def __setattr__(self, name, value):
        if name in SisenseDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_DASHBOARD_FOLDER_QUALIFIED_NAME: ClassVar[
        KeywordTextField
    ] = KeywordTextField(
        "sisenseDashboardFolderQualifiedName",
        "sisenseDashboardFolderQualifiedName",
        "sisenseDashboardFolderQualifiedName.text",
    )
    """
    Unique name of the folder in which this dashboard exists.
    """
    SISENSE_DASHBOARD_WIDGET_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseDashboardWidgetCount", "sisenseDashboardWidgetCount"
    )
    """
    Number of widgets in this dashboard.
    """

    SISENSE_DATAMODELS: ClassVar[RelationField] = RelationField("sisenseDatamodels")
    """
    TBC
    """
    SISENSE_WIDGETS: ClassVar[RelationField] = RelationField("sisenseWidgets")
    """
    TBC
    """
    SISENSE_FOLDER: ClassVar[RelationField] = RelationField("sisenseFolder")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sisense_dashboard_folder_qualified_name",
        "sisense_dashboard_widget_count",
        "sisense_datamodels",
        "sisense_widgets",
        "sisense_folder",
    ]

    @property
    def sisense_dashboard_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_dashboard_folder_qualified_name
        )

    @sisense_dashboard_folder_qualified_name.setter
    def sisense_dashboard_folder_qualified_name(
        self, sisense_dashboard_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboard_folder_qualified_name = (
            sisense_dashboard_folder_qualified_name
        )

    @property
    def sisense_dashboard_widget_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_dashboard_widget_count
        )

    @sisense_dashboard_widget_count.setter
    def sisense_dashboard_widget_count(
        self, sisense_dashboard_widget_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboard_widget_count = sisense_dashboard_widget_count

    @property
    def sisense_datamodels(self) -> Optional[list[SisenseDatamodel]]:
        return None if self.attributes is None else self.attributes.sisense_datamodels

    @sisense_datamodels.setter
    def sisense_datamodels(self, sisense_datamodels: Optional[list[SisenseDatamodel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodels = sisense_datamodels

    @property
    def sisense_widgets(self) -> Optional[list[SisenseWidget]]:
        return None if self.attributes is None else self.attributes.sisense_widgets

    @sisense_widgets.setter
    def sisense_widgets(self, sisense_widgets: Optional[list[SisenseWidget]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widgets = sisense_widgets

    @property
    def sisense_folder(self) -> Optional[SisenseFolder]:
        return None if self.attributes is None else self.attributes.sisense_folder

    @sisense_folder.setter
    def sisense_folder(self, sisense_folder: Optional[SisenseFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_folder = sisense_folder

    class Attributes(Sisense.Attributes):
        sisense_dashboard_folder_qualified_name: Optional[str] = Field(
            None, description="", alias="sisenseDashboardFolderQualifiedName"
        )
        sisense_dashboard_widget_count: Optional[int] = Field(
            None, description="", alias="sisenseDashboardWidgetCount"
        )
        sisense_datamodels: Optional[list[SisenseDatamodel]] = Field(
            None, description="", alias="sisenseDatamodels"
        )  # relationship
        sisense_widgets: Optional[list[SisenseWidget]] = Field(
            None, description="", alias="sisenseWidgets"
        )  # relationship
        sisense_folder: Optional[SisenseFolder] = Field(
            None, description="", alias="sisenseFolder"
        )  # relationship

    attributes: "SisenseDashboard.Attributes" = Field(
        default_factory=lambda: SisenseDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


SisenseFolder.Attributes.update_forward_refs()


SisenseWidget.Attributes.update_forward_refs()


SisenseDatamodel.Attributes.update_forward_refs()


SisenseDatamodelTable.Attributes.update_forward_refs()


SisenseDashboard.Attributes.update_forward_refs()
