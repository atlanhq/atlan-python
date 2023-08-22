# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .asset37 import Mode


class ModeReport(Mode):
    """Description"""

    type_name: str = Field("ModeReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeReport":
            raise ValueError("must be ModeReport")
        return v

    def __setattr__(self, name, value):
        if name in ModeReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_COLLECTION_TOKEN: ClassVar[KeywordField] = KeywordField(
        "modeCollectionToken", "modeCollectionToken"
    )
    """
    TBC
    """
    MODE_REPORT_PUBLISHED_AT: ClassVar[NumericField] = NumericField(
        "modeReportPublishedAt", "modeReportPublishedAt"
    )
    """
    TBC
    """
    MODE_QUERY_COUNT: ClassVar[NumericField] = NumericField(
        "modeQueryCount", "modeQueryCount"
    )
    """
    TBC
    """
    MODE_CHART_COUNT: ClassVar[NumericField] = NumericField(
        "modeChartCount", "modeChartCount"
    )
    """
    TBC
    """
    MODE_QUERY_PREVIEW: ClassVar[TextField] = TextField(
        "modeQueryPreview", "modeQueryPreview"
    )
    """
    TBC
    """
    MODE_IS_PUBLIC: ClassVar[BooleanField] = BooleanField(
        "modeIsPublic", "modeIsPublic"
    )
    """
    TBC
    """
    MODE_IS_SHARED: ClassVar[BooleanField] = BooleanField(
        "modeIsShared", "modeIsShared"
    )
    """
    TBC
    """

    MODE_QUERIES: ClassVar[RelationField] = RelationField("modeQueries")
    """
    TBC
    """
    MODE_COLLECTIONS: ClassVar[RelationField] = RelationField("modeCollections")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mode_collection_token",
        "mode_report_published_at",
        "mode_query_count",
        "mode_chart_count",
        "mode_query_preview",
        "mode_is_public",
        "mode_is_shared",
        "mode_queries",
        "mode_collections",
    ]

    @property
    def mode_collection_token(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_token
        )

    @mode_collection_token.setter
    def mode_collection_token(self, mode_collection_token: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_token = mode_collection_token

    @property
    def mode_report_published_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_report_published_at
        )

    @mode_report_published_at.setter
    def mode_report_published_at(self, mode_report_published_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_published_at = mode_report_published_at

    @property
    def mode_query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.mode_query_count

    @mode_query_count.setter
    def mode_query_count(self, mode_query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_count = mode_query_count

    @property
    def mode_chart_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.mode_chart_count

    @mode_chart_count.setter
    def mode_chart_count(self, mode_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_chart_count = mode_chart_count

    @property
    def mode_query_preview(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_query_preview

    @mode_query_preview.setter
    def mode_query_preview(self, mode_query_preview: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query_preview = mode_query_preview

    @property
    def mode_is_public(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.mode_is_public

    @mode_is_public.setter
    def mode_is_public(self, mode_is_public: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_public = mode_is_public

    @property
    def mode_is_shared(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.mode_is_shared

    @mode_is_shared.setter
    def mode_is_shared(self, mode_is_shared: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_is_shared = mode_is_shared

    @property
    def mode_queries(self) -> Optional[list[ModeQuery]]:
        return None if self.attributes is None else self.attributes.mode_queries

    @mode_queries.setter
    def mode_queries(self, mode_queries: Optional[list[ModeQuery]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_queries = mode_queries

    @property
    def mode_collections(self) -> Optional[list[ModeCollection]]:
        return None if self.attributes is None else self.attributes.mode_collections

    @mode_collections.setter
    def mode_collections(self, mode_collections: Optional[list[ModeCollection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collections = mode_collections

    class Attributes(Mode.Attributes):
        mode_collection_token: Optional[str] = Field(
            None, description="", alias="modeCollectionToken"
        )
        mode_report_published_at: Optional[datetime] = Field(
            None, description="", alias="modeReportPublishedAt"
        )
        mode_query_count: Optional[int] = Field(
            None, description="", alias="modeQueryCount"
        )
        mode_chart_count: Optional[int] = Field(
            None, description="", alias="modeChartCount"
        )
        mode_query_preview: Optional[str] = Field(
            None, description="", alias="modeQueryPreview"
        )
        mode_is_public: Optional[bool] = Field(
            None, description="", alias="modeIsPublic"
        )
        mode_is_shared: Optional[bool] = Field(
            None, description="", alias="modeIsShared"
        )
        mode_queries: Optional[list[ModeQuery]] = Field(
            None, description="", alias="modeQueries"
        )  # relationship
        mode_collections: Optional[list[ModeCollection]] = Field(
            None, description="", alias="modeCollections"
        )  # relationship

    attributes: "ModeReport.Attributes" = Field(
        default_factory=lambda: ModeReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeQuery(Mode):
    """Description"""

    type_name: str = Field("ModeQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeQuery":
            raise ValueError("must be ModeQuery")
        return v

    def __setattr__(self, name, value):
        if name in ModeQuery._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_RAW_QUERY: ClassVar[TextField] = TextField("modeRawQuery", "modeRawQuery")
    """
    TBC
    """
    MODE_REPORT_IMPORT_COUNT: ClassVar[NumericField] = NumericField(
        "modeReportImportCount", "modeReportImportCount"
    )
    """
    TBC
    """

    MODE_CHARTS: ClassVar[RelationField] = RelationField("modeCharts")
    """
    TBC
    """
    MODE_REPORT: ClassVar[RelationField] = RelationField("modeReport")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mode_raw_query",
        "mode_report_import_count",
        "mode_charts",
        "mode_report",
    ]

    @property
    def mode_raw_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_raw_query

    @mode_raw_query.setter
    def mode_raw_query(self, mode_raw_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_raw_query = mode_raw_query

    @property
    def mode_report_import_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mode_report_import_count
        )

    @mode_report_import_count.setter
    def mode_report_import_count(self, mode_report_import_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report_import_count = mode_report_import_count

    @property
    def mode_charts(self) -> Optional[list[ModeChart]]:
        return None if self.attributes is None else self.attributes.mode_charts

    @mode_charts.setter
    def mode_charts(self, mode_charts: Optional[list[ModeChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_charts = mode_charts

    @property
    def mode_report(self) -> Optional[ModeReport]:
        return None if self.attributes is None else self.attributes.mode_report

    @mode_report.setter
    def mode_report(self, mode_report: Optional[ModeReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_report = mode_report

    class Attributes(Mode.Attributes):
        mode_raw_query: Optional[str] = Field(
            None, description="", alias="modeRawQuery"
        )
        mode_report_import_count: Optional[int] = Field(
            None, description="", alias="modeReportImportCount"
        )
        mode_charts: Optional[list[ModeChart]] = Field(
            None, description="", alias="modeCharts"
        )  # relationship
        mode_report: Optional[ModeReport] = Field(
            None, description="", alias="modeReport"
        )  # relationship

    attributes: "ModeQuery.Attributes" = Field(
        default_factory=lambda: ModeQuery.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeChart(Mode):
    """Description"""

    type_name: str = Field("ModeChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeChart":
            raise ValueError("must be ModeChart")
        return v

    def __setattr__(self, name, value):
        if name in ModeChart._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_CHART_TYPE: ClassVar[KeywordField] = KeywordField(
        "modeChartType", "modeChartType"
    )
    """
    TBC
    """

    MODE_QUERY: ClassVar[RelationField] = RelationField("modeQuery")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mode_chart_type",
        "mode_query",
    ]

    @property
    def mode_chart_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_chart_type

    @mode_chart_type.setter
    def mode_chart_type(self, mode_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_chart_type = mode_chart_type

    @property
    def mode_query(self) -> Optional[ModeQuery]:
        return None if self.attributes is None else self.attributes.mode_query

    @mode_query.setter
    def mode_query(self, mode_query: Optional[ModeQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_query = mode_query

    class Attributes(Mode.Attributes):
        mode_chart_type: Optional[str] = Field(
            None, description="", alias="modeChartType"
        )
        mode_query: Optional[ModeQuery] = Field(
            None, description="", alias="modeQuery"
        )  # relationship

    attributes: "ModeChart.Attributes" = Field(
        default_factory=lambda: ModeChart.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeWorkspace(Mode):
    """Description"""

    type_name: str = Field("ModeWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeWorkspace":
            raise ValueError("must be ModeWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in ModeWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_COLLECTION_COUNT: ClassVar[NumericField] = NumericField(
        "modeCollectionCount", "modeCollectionCount"
    )
    """
    TBC
    """

    MODE_COLLECTIONS: ClassVar[RelationField] = RelationField("modeCollections")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mode_collection_count",
        "mode_collections",
    ]

    @property
    def mode_collection_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_count
        )

    @mode_collection_count.setter
    def mode_collection_count(self, mode_collection_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_count = mode_collection_count

    @property
    def mode_collections(self) -> Optional[list[ModeCollection]]:
        return None if self.attributes is None else self.attributes.mode_collections

    @mode_collections.setter
    def mode_collections(self, mode_collections: Optional[list[ModeCollection]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collections = mode_collections

    class Attributes(Mode.Attributes):
        mode_collection_count: Optional[int] = Field(
            None, description="", alias="modeCollectionCount"
        )
        mode_collections: Optional[list[ModeCollection]] = Field(
            None, description="", alias="modeCollections"
        )  # relationship

    attributes: "ModeWorkspace.Attributes" = Field(
        default_factory=lambda: ModeWorkspace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ModeCollection(Mode):
    """Description"""

    type_name: str = Field("ModeCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModeCollection":
            raise ValueError("must be ModeCollection")
        return v

    def __setattr__(self, name, value):
        if name in ModeCollection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODE_COLLECTION_TYPE: ClassVar[KeywordField] = KeywordField(
        "modeCollectionType", "modeCollectionType"
    )
    """
    TBC
    """
    MODE_COLLECTION_STATE: ClassVar[KeywordField] = KeywordField(
        "modeCollectionState", "modeCollectionState"
    )
    """
    TBC
    """

    MODE_WORKSPACE: ClassVar[RelationField] = RelationField("modeWorkspace")
    """
    TBC
    """
    MODE_REPORTS: ClassVar[RelationField] = RelationField("modeReports")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mode_collection_type",
        "mode_collection_state",
        "mode_workspace",
        "mode_reports",
    ]

    @property
    def mode_collection_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mode_collection_type

    @mode_collection_type.setter
    def mode_collection_type(self, mode_collection_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_type = mode_collection_type

    @property
    def mode_collection_state(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mode_collection_state
        )

    @mode_collection_state.setter
    def mode_collection_state(self, mode_collection_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_collection_state = mode_collection_state

    @property
    def mode_workspace(self) -> Optional[ModeWorkspace]:
        return None if self.attributes is None else self.attributes.mode_workspace

    @mode_workspace.setter
    def mode_workspace(self, mode_workspace: Optional[ModeWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_workspace = mode_workspace

    @property
    def mode_reports(self) -> Optional[list[ModeReport]]:
        return None if self.attributes is None else self.attributes.mode_reports

    @mode_reports.setter
    def mode_reports(self, mode_reports: Optional[list[ModeReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mode_reports = mode_reports

    class Attributes(Mode.Attributes):
        mode_collection_type: Optional[str] = Field(
            None, description="", alias="modeCollectionType"
        )
        mode_collection_state: Optional[str] = Field(
            None, description="", alias="modeCollectionState"
        )
        mode_workspace: Optional[ModeWorkspace] = Field(
            None, description="", alias="modeWorkspace"
        )  # relationship
        mode_reports: Optional[list[ModeReport]] = Field(
            None, description="", alias="modeReports"
        )  # relationship

    attributes: "ModeCollection.Attributes" = Field(
        default_factory=lambda: ModeCollection.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


ModeReport.Attributes.update_forward_refs()


ModeQuery.Attributes.update_forward_refs()


ModeChart.Attributes.update_forward_refs()


ModeWorkspace.Attributes.update_forward_refs()


ModeCollection.Attributes.update_forward_refs()
