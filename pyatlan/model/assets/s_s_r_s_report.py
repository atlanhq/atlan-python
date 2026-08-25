# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .s_s_r_s import SSRS


class SSRSReport(SSRS):
    """Description"""

    type_name: str = Field(default="SSRSReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SSRSReport":
            raise ValueError("must be SSRSReport")
        return v

    def __setattr__(self, name, value):
        if name in SSRSReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SSRS_REPORT_SIZE: ClassVar[NumericField] = NumericField(
        "ssrsReportSize", "ssrsReportSize"
    )
    """
    Size of the report.
    """
    SSRS_REPORT_PARAMETERS: ClassVar[KeywordField] = KeywordField(
        "ssrsReportParameters", "ssrsReportParameters"
    )
    """
    Parameters for the report.
    """
    SSRS_REPORT_DATA_SET_COUNT: ClassVar[NumericField] = NumericField(
        "ssrsReportDataSetCount", "ssrsReportDataSetCount"
    )
    """
    Number of datasets in this report.
    """
    SSRS_REPORT_DATA_SOURCE_COUNT: ClassVar[NumericField] = NumericField(
        "ssrsReportDataSourceCount", "ssrsReportDataSourceCount"
    )
    """
    Number of data sources in this report.
    """

    SSRS_LINKED_REPORTS: ClassVar[RelationField] = RelationField("ssrsLinkedReports")
    """
    TBC
    """
    SSRS_LINKED_FROM_REPORTS: ClassVar[RelationField] = RelationField(
        "ssrsLinkedFromReports"
    )
    """
    TBC
    """
    SSRS_FOLDER: ClassVar[RelationField] = RelationField("ssrsFolder")
    """
    TBC
    """
    SSRS_DATA_SETS: ClassVar[RelationField] = RelationField("ssrsDataSets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ssrs_report_size",
        "ssrs_report_parameters",
        "ssrs_report_data_set_count",
        "ssrs_report_data_source_count",
        "ssrs_linked_reports",
        "ssrs_linked_from_reports",
        "ssrs_folder",
        "ssrs_data_sets",
    ]

    @property
    def ssrs_report_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.ssrs_report_size

    @ssrs_report_size.setter
    def ssrs_report_size(self, ssrs_report_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_report_size = ssrs_report_size

    @property
    def ssrs_report_parameters(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ssrs_report_parameters
        )

    @ssrs_report_parameters.setter
    def ssrs_report_parameters(self, ssrs_report_parameters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_report_parameters = ssrs_report_parameters

    @property
    def ssrs_report_data_set_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_report_data_set_count
        )

    @ssrs_report_data_set_count.setter
    def ssrs_report_data_set_count(self, ssrs_report_data_set_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_report_data_set_count = ssrs_report_data_set_count

    @property
    def ssrs_report_data_source_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_report_data_source_count
        )

    @ssrs_report_data_source_count.setter
    def ssrs_report_data_source_count(
        self, ssrs_report_data_source_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_report_data_source_count = ssrs_report_data_source_count

    @property
    def ssrs_linked_reports(self) -> Optional[List[SSRSReport]]:
        return None if self.attributes is None else self.attributes.ssrs_linked_reports

    @ssrs_linked_reports.setter
    def ssrs_linked_reports(self, ssrs_linked_reports: Optional[List[SSRSReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_linked_reports = ssrs_linked_reports

    @property
    def ssrs_linked_from_reports(self) -> Optional[List[SSRSReport]]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_linked_from_reports
        )

    @ssrs_linked_from_reports.setter
    def ssrs_linked_from_reports(
        self, ssrs_linked_from_reports: Optional[List[SSRSReport]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_linked_from_reports = ssrs_linked_from_reports

    @property
    def ssrs_folder(self) -> Optional[SSRSFolder]:
        return None if self.attributes is None else self.attributes.ssrs_folder

    @ssrs_folder.setter
    def ssrs_folder(self, ssrs_folder: Optional[SSRSFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_folder = ssrs_folder

    @property
    def ssrs_data_sets(self) -> Optional[List[SSRSDataSet]]:
        return None if self.attributes is None else self.attributes.ssrs_data_sets

    @ssrs_data_sets.setter
    def ssrs_data_sets(self, ssrs_data_sets: Optional[List[SSRSDataSet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_sets = ssrs_data_sets

    class Attributes(SSRS.Attributes):
        ssrs_report_size: Optional[int] = Field(default=None, description="")
        ssrs_report_parameters: Optional[str] = Field(default=None, description="")
        ssrs_report_data_set_count: Optional[int] = Field(default=None, description="")
        ssrs_report_data_source_count: Optional[int] = Field(
            default=None, description=""
        )
        ssrs_linked_reports: Optional[List[SSRSReport]] = Field(
            default=None, description=""
        )  # relationship
        ssrs_linked_from_reports: Optional[List[SSRSReport]] = Field(
            default=None, description=""
        )  # relationship
        ssrs_folder: Optional[SSRSFolder] = Field(
            default=None, description=""
        )  # relationship
        ssrs_data_sets: Optional[List[SSRSDataSet]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SSRSReport.Attributes = Field(
        default_factory=lambda: SSRSReport.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_s_r_s_data_set import SSRSDataSet  # noqa: E402, F401
from .s_s_r_s_folder import SSRSFolder  # noqa: E402, F401

SSRSReport.Attributes.update_forward_refs()
