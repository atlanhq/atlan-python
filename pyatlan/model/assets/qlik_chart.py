# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .qlik import Qlik


class QlikChart(Qlik):
    """Description"""

    type_name: str = Field(default="QlikChart", allow_mutation=False)

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
    Subtitle of this chart.
    """
    QLIK_CHART_FOOTNOTE: ClassVar[TextField] = TextField(
        "qlikChartFootnote", "qlikChartFootnote"
    )
    """
    Footnote of this chart.
    """
    QLIK_CHART_ORIENTATION: ClassVar[KeywordField] = KeywordField(
        "qlikChartOrientation", "qlikChartOrientation"
    )
    """
    Orientation of this chart.
    """
    QLIK_CHART_TYPE: ClassVar[KeywordField] = KeywordField(
        "qlikChartType", "qlikChartType"
    )
    """
    Subtype of this chart, for example: bar, graph, pie, etc.
    """

    QLIK_SHEET: ClassVar[RelationField] = RelationField("qlikSheet")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
        qlik_chart_subtitle: Optional[str] = Field(default=None, description="")
        qlik_chart_footnote: Optional[str] = Field(default=None, description="")
        qlik_chart_orientation: Optional[str] = Field(default=None, description="")
        qlik_chart_type: Optional[str] = Field(default=None, description="")
        qlik_sheet: Optional[QlikSheet] = Field(
            default=None, description=""
        )  # relationship

    attributes: QlikChart.Attributes = Field(
        default_factory=lambda: QlikChart.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .qlik_sheet import QlikSheet  # noqa
