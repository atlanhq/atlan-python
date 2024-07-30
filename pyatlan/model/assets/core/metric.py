# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .data_quality import DataQuality


class Metric(DataQuality):
    """Description"""

    type_name: str = Field(default="Metric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Metric":
            raise ValueError("must be Metric")
        return v

    def __setattr__(self, name, value):
        if name in Metric._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    METRIC_TYPE: ClassVar[KeywordField] = KeywordField("metricType", "metricType")
    """
    Type of the metric.
    """
    METRIC_SQL: ClassVar[KeywordField] = KeywordField("metricSQL", "metricSQL")
    """
    SQL query used to compute the metric.
    """
    METRIC_FILTERS: ClassVar[TextField] = TextField("metricFilters", "metricFilters")
    """
    Filters to be applied to the metric query.
    """
    METRIC_TIME_GRAINS: ClassVar[TextField] = TextField(
        "metricTimeGrains", "metricTimeGrains"
    )
    """
    List of time grains to be applied to the metric query.
    """

    METRIC_TIMESTAMP_COLUMN: ClassVar[RelationField] = RelationField(
        "metricTimestampColumn"
    )
    """
    TBC
    """
    ASSETS: ClassVar[RelationField] = RelationField("assets")
    """
    TBC
    """
    METRIC_DIMENSION_COLUMNS: ClassVar[RelationField] = RelationField(
        "metricDimensionColumns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "metric_type",
        "metric_s_q_l",
        "metric_filters",
        "metric_time_grains",
        "metric_timestamp_column",
        "assets",
        "metric_dimension_columns",
    ]

    @property
    def metric_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_type

    @metric_type.setter
    def metric_type(self, metric_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_type = metric_type

    @property
    def metric_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_s_q_l

    @metric_s_q_l.setter
    def metric_s_q_l(self, metric_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_s_q_l = metric_s_q_l

    @property
    def metric_filters(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_filters

    @metric_filters.setter
    def metric_filters(self, metric_filters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_filters = metric_filters

    @property
    def metric_time_grains(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.metric_time_grains

    @metric_time_grains.setter
    def metric_time_grains(self, metric_time_grains: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_time_grains = metric_time_grains

    @property
    def metric_timestamp_column(self) -> Optional[Column]:
        return (
            None if self.attributes is None else self.attributes.metric_timestamp_column
        )

    @metric_timestamp_column.setter
    def metric_timestamp_column(self, metric_timestamp_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_timestamp_column = metric_timestamp_column

    @property
    def assets(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.assets

    @assets.setter
    def assets(self, assets: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assets = assets

    @property
    def metric_dimension_columns(self) -> Optional[List[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.metric_dimension_columns
        )

    @metric_dimension_columns.setter
    def metric_dimension_columns(
        self, metric_dimension_columns: Optional[List[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_dimension_columns = metric_dimension_columns

    class Attributes(DataQuality.Attributes):
        metric_type: Optional[str] = Field(default=None, description="")
        metric_s_q_l: Optional[str] = Field(default=None, description="")
        metric_filters: Optional[str] = Field(default=None, description="")
        metric_time_grains: Optional[Set[str]] = Field(default=None, description="")
        metric_timestamp_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship
        metric_dimension_columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship

    attributes: Metric.Attributes = Field(
        default_factory=lambda: Metric.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


# Imports required for fixing circular dependencies:
from .asset import Asset  # noqa # isort:skip
from .catalog import Catalog  # noqa # isort:skip
from .s_q_l import SQL  # noqa # isort:skip


from .asset import Asset  # noqa
from .column import Column  # noqa
