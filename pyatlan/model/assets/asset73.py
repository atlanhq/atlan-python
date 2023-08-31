# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .asset48 import Qlik


class QlikApp(Qlik):
    """Description"""

    type_name: str = Field("QlikApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikApp":
            raise ValueError("must be QlikApp")
        return v

    def __setattr__(self, name, value):
        if name in QlikApp._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_HAS_SECTION_ACCESS: ClassVar[BooleanField] = BooleanField(
        "qlikHasSectionAccess", "qlikHasSectionAccess"
    )
    """
    Whether section access/data masking is enabled on source
    """
    QLIK_ORIGIN_APP_ID: ClassVar[KeywordField] = KeywordField(
        "qlikOriginAppId", "qlikOriginAppId"
    )
    """
    originAppId value for a qlik app
    """
    QLIK_IS_ENCRYPTED: ClassVar[BooleanField] = BooleanField(
        "qlikIsEncrypted", "qlikIsEncrypted"
    )
    """
    Whether a qlik app is encrypted
    """
    QLIK_IS_DIRECT_QUERY_MODE: ClassVar[BooleanField] = BooleanField(
        "qlikIsDirectQueryMode", "qlikIsDirectQueryMode"
    )
    """
    Whether a qlik app is in direct query mode
    """
    QLIK_APP_STATIC_BYTE_SIZE: ClassVar[NumericField] = NumericField(
        "qlikAppStaticByteSize", "qlikAppStaticByteSize"
    )
    """
    Static space taken by a qlik app
    """

    QLIK_SPACE: ClassVar[RelationField] = RelationField("qlikSpace")
    """
    TBC
    """
    QLIK_SHEETS: ClassVar[RelationField] = RelationField("qlikSheets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "qlik_has_section_access",
        "qlik_origin_app_id",
        "qlik_is_encrypted",
        "qlik_is_direct_query_mode",
        "qlik_app_static_byte_size",
        "qlik_space",
        "qlik_sheets",
    ]

    @property
    def qlik_has_section_access(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.qlik_has_section_access
        )

    @qlik_has_section_access.setter
    def qlik_has_section_access(self, qlik_has_section_access: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_has_section_access = qlik_has_section_access

    @property
    def qlik_origin_app_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_origin_app_id

    @qlik_origin_app_id.setter
    def qlik_origin_app_id(self, qlik_origin_app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_origin_app_id = qlik_origin_app_id

    @property
    def qlik_is_encrypted(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.qlik_is_encrypted

    @qlik_is_encrypted.setter
    def qlik_is_encrypted(self, qlik_is_encrypted: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_encrypted = qlik_is_encrypted

    @property
    def qlik_is_direct_query_mode(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_is_direct_query_mode
        )

    @qlik_is_direct_query_mode.setter
    def qlik_is_direct_query_mode(self, qlik_is_direct_query_mode: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_is_direct_query_mode = qlik_is_direct_query_mode

    @property
    def qlik_app_static_byte_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_app_static_byte_size
        )

    @qlik_app_static_byte_size.setter
    def qlik_app_static_byte_size(self, qlik_app_static_byte_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app_static_byte_size = qlik_app_static_byte_size

    @property
    def qlik_space(self) -> Optional[QlikSpace]:
        return None if self.attributes is None else self.attributes.qlik_space

    @qlik_space.setter
    def qlik_space(self, qlik_space: Optional[QlikSpace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space = qlik_space

    @property
    def qlik_sheets(self) -> Optional[list[QlikSheet]]:
        return None if self.attributes is None else self.attributes.qlik_sheets

    @qlik_sheets.setter
    def qlik_sheets(self, qlik_sheets: Optional[list[QlikSheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheets = qlik_sheets

    class Attributes(Qlik.Attributes):
        qlik_has_section_access: Optional[bool] = Field(
            None, description="", alias="qlikHasSectionAccess"
        )
        qlik_origin_app_id: Optional[str] = Field(
            None, description="", alias="qlikOriginAppId"
        )
        qlik_is_encrypted: Optional[bool] = Field(
            None, description="", alias="qlikIsEncrypted"
        )
        qlik_is_direct_query_mode: Optional[bool] = Field(
            None, description="", alias="qlikIsDirectQueryMode"
        )
        qlik_app_static_byte_size: Optional[int] = Field(
            None, description="", alias="qlikAppStaticByteSize"
        )
        qlik_space: Optional[QlikSpace] = Field(
            None, description="", alias="qlikSpace"
        )  # relationship
        qlik_sheets: Optional[list[QlikSheet]] = Field(
            None, description="", alias="qlikSheets"
        )  # relationship

    attributes: "QlikApp.Attributes" = Field(
        default_factory=lambda: QlikApp.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikChart(Qlik):
    """Description"""

    type_name: str = Field("QlikChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikChart":
            raise ValueError("must be QlikChart")
        return v

    def __setattr__(self, name, value):
        if name in QlikChart._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_CHART_SUBTITLE: ClassVar[TextField] = TextField(
        "qlikChartSubtitle", "qlikChartSubtitle"
    )
    """
    Subtitle of a qlik chart
    """
    QLIK_CHART_FOOTNOTE: ClassVar[TextField] = TextField(
        "qlikChartFootnote", "qlikChartFootnote"
    )
    """
    Footnote of a qlik chart
    """
    QLIK_CHART_ORIENTATION: ClassVar[KeywordField] = KeywordField(
        "qlikChartOrientation", "qlikChartOrientation"
    )
    """
    Orientation of a qlik chart
    """
    QLIK_CHART_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikChartType", "qlikChartType"
    )
    """
    Subtype of an qlik chart. E.g. bar, graph, pie etc
    """

    QLIK_SHEET: ClassVar[RelationField] = RelationField("qlikSheet")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "qlik_chart_subtitle",
        "qlik_chart_footnote",
        "qlik_chart_orientation",
        "qlik_chart_type",
        "qlik_sheet",
    ]

    @property
    def qlik_chart_subtitle(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_chart_subtitle

    @qlik_chart_subtitle.setter
    def qlik_chart_subtitle(self, qlik_chart_subtitle: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_subtitle = qlik_chart_subtitle

    @property
    def qlik_chart_footnote(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_chart_footnote

    @qlik_chart_footnote.setter
    def qlik_chart_footnote(self, qlik_chart_footnote: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_footnote = qlik_chart_footnote

    @property
    def qlik_chart_orientation(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.qlik_chart_orientation
        )

    @qlik_chart_orientation.setter
    def qlik_chart_orientation(self, qlik_chart_orientation: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_orientation = qlik_chart_orientation

    @property
    def qlik_chart_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_chart_type

    @qlik_chart_type.setter
    def qlik_chart_type(self, qlik_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_chart_type = qlik_chart_type

    @property
    def qlik_sheet(self) -> Optional[QlikSheet]:
        return None if self.attributes is None else self.attributes.qlik_sheet

    @qlik_sheet.setter
    def qlik_sheet(self, qlik_sheet: Optional[QlikSheet]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheet = qlik_sheet

    class Attributes(Qlik.Attributes):
        qlik_chart_subtitle: Optional[str] = Field(
            None, description="", alias="qlikChartSubtitle"
        )
        qlik_chart_footnote: Optional[str] = Field(
            None, description="", alias="qlikChartFootnote"
        )
        qlik_chart_orientation: Optional[str] = Field(
            None, description="", alias="qlikChartOrientation"
        )
        qlik_chart_type: Optional[str] = Field(
            None, description="", alias="qlikChartType"
        )
        qlik_sheet: Optional[QlikSheet] = Field(
            None, description="", alias="qlikSheet"
        )  # relationship

    attributes: "QlikChart.Attributes" = Field(
        default_factory=lambda: QlikChart.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikDataset(Qlik):
    """Description"""

    type_name: str = Field("QlikDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikDataset":
            raise ValueError("must be QlikDataset")
        return v

    def __setattr__(self, name, value):
        if name in QlikDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_DATASET_TECHNICAL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikDatasetTechnicalName",
        "qlikDatasetTechnicalName.keyword",
        "qlikDatasetTechnicalName",
    )
    """
    Technical name of a qlik data asset
    """
    QLIK_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikDatasetType", "qlikDatasetType"
    )
    """
    Type of an qlik data asset. E.g. qix-df, snowflake etc
    """
    QLIK_DATASET_URI: ClassVar[KeywordTextField] = KeywordTextField(
        "qlikDatasetUri", "qlikDatasetUri", "qlikDatasetUri.text"
    )
    """
    URI of a qlik dataset
    """
    QLIK_DATASET_SUBTYPE: ClassVar[KeywordField] = KeywordField(
        "qlikDatasetSubtype", "qlikDatasetSubtype"
    )
    """
    Subtype of an qlik dataset asset
    """

    QLIK_SPACE: ClassVar[RelationField] = RelationField("qlikSpace")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "qlik_dataset_technical_name",
        "qlik_dataset_type",
        "qlik_dataset_uri",
        "qlik_dataset_subtype",
        "qlik_space",
    ]

    @property
    def qlik_dataset_technical_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.qlik_dataset_technical_name
        )

    @qlik_dataset_technical_name.setter
    def qlik_dataset_technical_name(self, qlik_dataset_technical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_technical_name = qlik_dataset_technical_name

    @property
    def qlik_dataset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_type

    @qlik_dataset_type.setter
    def qlik_dataset_type(self, qlik_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_type = qlik_dataset_type

    @property
    def qlik_dataset_uri(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_uri

    @qlik_dataset_uri.setter
    def qlik_dataset_uri(self, qlik_dataset_uri: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_uri = qlik_dataset_uri

    @property
    def qlik_dataset_subtype(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_dataset_subtype

    @qlik_dataset_subtype.setter
    def qlik_dataset_subtype(self, qlik_dataset_subtype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_dataset_subtype = qlik_dataset_subtype

    @property
    def qlik_space(self) -> Optional[QlikSpace]:
        return None if self.attributes is None else self.attributes.qlik_space

    @qlik_space.setter
    def qlik_space(self, qlik_space: Optional[QlikSpace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space = qlik_space

    class Attributes(Qlik.Attributes):
        qlik_dataset_technical_name: Optional[str] = Field(
            None, description="", alias="qlikDatasetTechnicalName"
        )
        qlik_dataset_type: Optional[str] = Field(
            None, description="", alias="qlikDatasetType"
        )
        qlik_dataset_uri: Optional[str] = Field(
            None, description="", alias="qlikDatasetUri"
        )
        qlik_dataset_subtype: Optional[str] = Field(
            None, description="", alias="qlikDatasetSubtype"
        )
        qlik_space: Optional[QlikSpace] = Field(
            None, description="", alias="qlikSpace"
        )  # relationship

    attributes: "QlikDataset.Attributes" = Field(
        default_factory=lambda: QlikDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikSheet(Qlik):
    """Description"""

    type_name: str = Field("QlikSheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSheet":
            raise ValueError("must be QlikSheet")
        return v

    def __setattr__(self, name, value):
        if name in QlikSheet._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_SHEET_IS_APPROVED: ClassVar[BooleanField] = BooleanField(
        "qlikSheetIsApproved", "qlikSheetIsApproved"
    )
    """
    Whether a qlik sheet is approved
    """

    QLIK_APP: ClassVar[RelationField] = RelationField("qlikApp")
    """
    TBC
    """
    QLIK_CHARTS: ClassVar[RelationField] = RelationField("qlikCharts")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "qlik_sheet_is_approved",
        "qlik_app",
        "qlik_charts",
    ]

    @property
    def qlik_sheet_is_approved(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.qlik_sheet_is_approved
        )

    @qlik_sheet_is_approved.setter
    def qlik_sheet_is_approved(self, qlik_sheet_is_approved: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_sheet_is_approved = qlik_sheet_is_approved

    @property
    def qlik_app(self) -> Optional[QlikApp]:
        return None if self.attributes is None else self.attributes.qlik_app

    @qlik_app.setter
    def qlik_app(self, qlik_app: Optional[QlikApp]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_app = qlik_app

    @property
    def qlik_charts(self) -> Optional[list[QlikChart]]:
        return None if self.attributes is None else self.attributes.qlik_charts

    @qlik_charts.setter
    def qlik_charts(self, qlik_charts: Optional[list[QlikChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_charts = qlik_charts

    class Attributes(Qlik.Attributes):
        qlik_sheet_is_approved: Optional[bool] = Field(
            None, description="", alias="qlikSheetIsApproved"
        )
        qlik_app: Optional[QlikApp] = Field(
            None, description="", alias="qlikApp"
        )  # relationship
        qlik_charts: Optional[list[QlikChart]] = Field(
            None, description="", alias="qlikCharts"
        )  # relationship

    attributes: "QlikSheet.Attributes" = Field(
        default_factory=lambda: QlikSheet.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class QlikSpace(Qlik):
    """Description"""

    type_name: str = Field("QlikSpace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QlikSpace":
            raise ValueError("must be QlikSpace")
        return v

    def __setattr__(self, name, value):
        if name in QlikSpace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QLIK_SPACE_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikSpaceType", "qlikSpaceType"
    )
    """
    Type of a qlik space. E.g. Private, Shared etc
    """

    QLIK_DATASETS: ClassVar[RelationField] = RelationField("qlikDatasets")
    """
    TBC
    """
    QLIK_APPS: ClassVar[RelationField] = RelationField("qlikApps")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "qlik_space_type",
        "qlik_datasets",
        "qlik_apps",
    ]

    @property
    def qlik_space_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.qlik_space_type

    @qlik_space_type.setter
    def qlik_space_type(self, qlik_space_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_space_type = qlik_space_type

    @property
    def qlik_datasets(self) -> Optional[list[QlikDataset]]:
        return None if self.attributes is None else self.attributes.qlik_datasets

    @qlik_datasets.setter
    def qlik_datasets(self, qlik_datasets: Optional[list[QlikDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_datasets = qlik_datasets

    @property
    def qlik_apps(self) -> Optional[list[QlikApp]]:
        return None if self.attributes is None else self.attributes.qlik_apps

    @qlik_apps.setter
    def qlik_apps(self, qlik_apps: Optional[list[QlikApp]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.qlik_apps = qlik_apps

    class Attributes(Qlik.Attributes):
        qlik_space_type: Optional[str] = Field(
            None, description="", alias="qlikSpaceType"
        )
        qlik_datasets: Optional[list[QlikDataset]] = Field(
            None, description="", alias="qlikDatasets"
        )  # relationship
        qlik_apps: Optional[list[QlikApp]] = Field(
            None, description="", alias="qlikApps"
        )  # relationship

    attributes: "QlikSpace.Attributes" = Field(
        default_factory=lambda: QlikSpace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


QlikApp.Attributes.update_forward_refs()


QlikChart.Attributes.update_forward_refs()


QlikDataset.Attributes.update_forward_refs()


QlikSheet.Attributes.update_forward_refs()


QlikSpace.Attributes.update_forward_refs()
