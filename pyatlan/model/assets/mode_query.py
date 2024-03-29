# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField, TextField

from .mode import Mode


class ModeQuery(Mode):
    """Description"""

    type_name: str = Field(default="ModeQuery", allow_mutation=False)

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

    """
    MODE_REPORT_IMPORT_COUNT: ClassVar[NumericField] = NumericField(
        "modeReportImportCount", "modeReportImportCount"
    )
    """

    """

    MODE_CHARTS: ClassVar[RelationField] = RelationField("modeCharts")
    """
    TBC
    """
    MODE_REPORT: ClassVar[RelationField] = RelationField("modeReport")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def mode_charts(self) -> Optional[List[ModeChart]]:
        return None if self.attributes is None else self.attributes.mode_charts

    @mode_charts.setter
    def mode_charts(self, mode_charts: Optional[List[ModeChart]]):
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
        mode_raw_query: Optional[str] = Field(default=None, description="")
        mode_report_import_count: Optional[int] = Field(default=None, description="")
        mode_charts: Optional[List[ModeChart]] = Field(
            default=None, description=""
        )  # relationship
        mode_report: Optional[ModeReport] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModeQuery.Attributes = Field(
        default_factory=lambda: ModeQuery.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .mode_chart import ModeChart  # noqa
from .mode_report import ModeReport  # noqa
