# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .mode import Mode


class ModeChart(Mode):
    """Description"""

    type_name: str = Field(default="ModeChart", allow_mutation=False)

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
    Type of chart.
    """

    MODE_QUERY: ClassVar[RelationField] = RelationField("modeQuery")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
        mode_chart_type: Optional[str] = Field(default=None, description="")
        mode_query: Optional[ModeQuery] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModeChart.Attributes = Field(
        default_factory=lambda: ModeChart.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .mode_query import ModeQuery  # noqa
