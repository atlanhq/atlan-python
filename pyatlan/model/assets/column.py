# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.model.structs import ColumnValueFrequencyMap, Histogram
from pyatlan.utils import init_guid, validate_required_fields

from .s_q_l import SQL


class Column(SQL):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        parent_type: type,
        order: int,
    ) -> Column: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        parent_type: type,
        order: int,
        parent_name: str,
        database_name: str,
        database_qualified_name: str,
        schema_name: str,
        schema_qualified_name: str,
        table_name: str,
        table_qualified_name: str,
        connection_qualified_name: str,
    ) -> Column: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_qualified_name: str,
        parent_type: type,
        order: int,
        parent_name: Optional[str] = None,
        database_name: Optional[str] = None,
        database_qualified_name: Optional[str] = None,
        schema_name: Optional[str] = None,
        schema_qualified_name: Optional[str] = None,
        table_name: Optional[str] = None,
        table_qualified_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
    ) -> Column:
        return Column(
            attributes=Column.Attributes.create(
                name=name,
                parent_qualified_name=parent_qualified_name,
                parent_type=parent_type,
                order=order,
                parent_name=parent_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                schema_name=schema_name,
                schema_qualified_name=schema_qualified_name,
                table_name=table_name,
                table_qualified_name=table_qualified_name,
                connection_qualified_name=connection_qualified_name,
            )
        )

    @classmethod
    @init_guid
    def create(
        cls, *, name: str, parent_qualified_name: str, parent_type: type, order: int
    ) -> Column:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            parent_qualified_name=parent_qualified_name,
            parent_type=parent_type,
            order=order,
        )

    type_name: str = Field(default="Column", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Column":
            raise ValueError("must be Column")
        return v

    def __setattr__(self, name, value):
        if name in Column._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "dataType", "dataType", "dataType.text"
    )
    """
    Data type of values in this column.
    """
    SUB_DATA_TYPE: ClassVar[KeywordField] = KeywordField("subDataType", "subDataType")
    """
    Sub-data type of this column.
    """
    RAW_DATA_TYPE_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "rawDataTypeDefinition", "rawDataTypeDefinition"
    )
    """

    """
    ORDER: ClassVar[NumericField] = NumericField("order", "order")
    """
    Order (position) in which this column appears in the table (starting at 1).
    """
    NESTED_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "nestedColumnCount", "nestedColumnCount"
    )
    """
    Number of columns nested within this (STRUCT or NESTED) column.
    """
    IS_PARTITION: ClassVar[BooleanField] = BooleanField("isPartition", "isPartition")
    """
    Whether this column is a partition column (true) or not (false).
    """
    PARTITION_ORDER: ClassVar[NumericField] = NumericField(
        "partitionOrder", "partitionOrder"
    )
    """
    Order (position) of this partition column in the table.
    """
    IS_CLUSTERED: ClassVar[BooleanField] = BooleanField("isClustered", "isClustered")
    """
    Whether this column is a clustered column (true) or not (false).
    """
    IS_PRIMARY: ClassVar[BooleanField] = BooleanField("isPrimary", "isPrimary")
    """
    When true, this column is the primary key for the table.
    """
    IS_FOREIGN: ClassVar[BooleanField] = BooleanField("isForeign", "isForeign")
    """
    When true, this column is a foreign key to another table. NOTE: this must be true when using the foreignKeyTo relationship to specify columns that refer to this column as a foreign key.
    """  # noqa: E501
    IS_INDEXED: ClassVar[BooleanField] = BooleanField("isIndexed", "isIndexed")
    """
    When true, this column is indexed in the database.
    """
    IS_SORT: ClassVar[BooleanField] = BooleanField("isSort", "isSort")
    """
    Whether this column is a sort column (true) or not (false).
    """
    IS_DIST: ClassVar[BooleanField] = BooleanField("isDist", "isDist")
    """
    Whether this column is a distribution column (true) or not (false).
    """
    IS_PINNED: ClassVar[BooleanField] = BooleanField("isPinned", "isPinned")
    """
    Whether this column is pinned (true) or not (false).
    """
    PINNED_BY: ClassVar[KeywordField] = KeywordField("pinnedBy", "pinnedBy")
    """
    User who pinned this column.
    """
    PINNED_AT: ClassVar[NumericField] = NumericField("pinnedAt", "pinnedAt")
    """
    Time (epoch) at which this column was pinned, in milliseconds.
    """
    PRECISION: ClassVar[NumericField] = NumericField("precision", "precision")
    """
    Total number of digits allowed, when the dataType is numeric.
    """
    DEFAULT_VALUE: ClassVar[KeywordField] = KeywordField("defaultValue", "defaultValue")
    """
    Default value for this column.
    """
    IS_NULLABLE: ClassVar[BooleanField] = BooleanField("isNullable", "isNullable")
    """
    When true, the values in this column can be null.
    """
    NUMERIC_SCALE: ClassVar[NumericField] = NumericField("numericScale", "numericScale")
    """
    Number of digits allowed to the right of the decimal point.
    """
    MAX_LENGTH: ClassVar[NumericField] = NumericField("maxLength", "maxLength")
    """
    Maximum length of a value in this column.
    """
    VALIDATIONS: ClassVar[KeywordField] = KeywordField("validations", "validations")
    """
    Validations for this column.
    """
    PARENT_COLUMN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentColumnQualifiedName",
        "parentColumnQualifiedName",
        "parentColumnQualifiedName.text",
    )
    """
    Unique name of the column this column is nested within, for STRUCT and NESTED columns.
    """
    PARENT_COLUMN_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentColumnName", "parentColumnName.keyword", "parentColumnName"
    )
    """
    Simple name of the column this column is nested within, for STRUCT and NESTED columns.
    """
    COLUMN_DISTINCT_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnDistinctValuesCount", "columnDistinctValuesCount"
    )
    """
    Number of rows that contain distinct values.
    """
    COLUMN_DISTINCT_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnDistinctValuesCountLong", "columnDistinctValuesCountLong"
    )
    """
    Number of rows that contain distinct values.
    """
    COLUMN_HISTOGRAM: ClassVar[KeywordField] = KeywordField(
        "columnHistogram", "columnHistogram"
    )
    """
    List of values in a histogram that represents the contents of this column.
    """
    COLUMN_MAX: ClassVar[NumericField] = NumericField("columnMax", "columnMax")
    """
    Greatest value in a numeric column.
    """
    COLUMN_MIN: ClassVar[NumericField] = NumericField("columnMin", "columnMin")
    """
    Least value in a numeric column.
    """
    COLUMN_MEAN: ClassVar[NumericField] = NumericField("columnMean", "columnMean")
    """
    Arithmetic mean of the values in a numeric column.
    """
    COLUMN_SUM: ClassVar[NumericField] = NumericField("columnSum", "columnSum")
    """
    Calculated sum of the values in a numeric column.
    """
    COLUMN_MEDIAN: ClassVar[NumericField] = NumericField("columnMedian", "columnMedian")
    """
    Calculated median of the values in a numeric column.
    """
    COLUMN_STANDARD_DEVIATION: ClassVar[NumericField] = NumericField(
        "columnStandardDeviation", "columnStandardDeviation"
    )
    """
    Calculated standard deviation of the values in a numeric column.
    """
    COLUMN_UNIQUE_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnUniqueValuesCount", "columnUniqueValuesCount"
    )
    """
    Number of rows in which a value in this column appears only once.
    """
    COLUMN_UNIQUE_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnUniqueValuesCountLong", "columnUniqueValuesCountLong"
    )
    """
    Number of rows in which a value in this column appears only once.
    """
    COLUMN_AVERAGE: ClassVar[NumericField] = NumericField(
        "columnAverage", "columnAverage"
    )
    """
    Average value in this column.
    """
    COLUMN_AVERAGE_LENGTH: ClassVar[NumericField] = NumericField(
        "columnAverageLength", "columnAverageLength"
    )
    """
    Average length of values in a string column.
    """
    COLUMN_DUPLICATE_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnDuplicateValuesCount", "columnDuplicateValuesCount"
    )
    """
    Number of rows that contain duplicate values.
    """
    COLUMN_DUPLICATE_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnDuplicateValuesCountLong", "columnDuplicateValuesCountLong"
    )
    """
    Number of rows that contain duplicate values.
    """
    COLUMN_MAXIMUM_STRING_LENGTH: ClassVar[NumericField] = NumericField(
        "columnMaximumStringLength", "columnMaximumStringLength"
    )
    """
    Length of the longest value in a string column.
    """
    COLUMN_MAXS: ClassVar[KeywordField] = KeywordField("columnMaxs", "columnMaxs")
    """
    List of the greatest values in a column.
    """
    COLUMN_MINIMUM_STRING_LENGTH: ClassVar[NumericField] = NumericField(
        "columnMinimumStringLength", "columnMinimumStringLength"
    )
    """
    Length of the shortest value in a string column.
    """
    COLUMN_MINS: ClassVar[KeywordField] = KeywordField("columnMins", "columnMins")
    """
    List of the least values in a column.
    """
    COLUMN_MISSING_VALUES_COUNT: ClassVar[NumericField] = NumericField(
        "columnMissingValuesCount", "columnMissingValuesCount"
    )
    """
    Number of rows in a column that do not contain content.
    """
    COLUMN_MISSING_VALUES_COUNT_LONG: ClassVar[NumericField] = NumericField(
        "columnMissingValuesCountLong", "columnMissingValuesCountLong"
    )
    """
    Number of rows in a column that do not contain content.
    """
    COLUMN_MISSING_VALUES_PERCENTAGE: ClassVar[NumericField] = NumericField(
        "columnMissingValuesPercentage", "columnMissingValuesPercentage"
    )
    """
    Percentage of rows in a column that do not contain content.
    """
    COLUMN_UNIQUENESS_PERCENTAGE: ClassVar[NumericField] = NumericField(
        "columnUniquenessPercentage", "columnUniquenessPercentage"
    )
    """
    Ratio indicating how unique data in this column is: 0 indicates that all values are the same, 100 indicates that all values in this column are unique.
    """  # noqa: E501
    COLUMN_VARIANCE: ClassVar[NumericField] = NumericField(
        "columnVariance", "columnVariance"
    )
    """
    Calculated variance of the values in a numeric column.
    """
    COLUMN_TOP_VALUES: ClassVar[KeywordField] = KeywordField(
        "columnTopValues", "columnTopValues"
    )
    """
    List of top values in this column.
    """
    COLUMN_DEPTH_LEVEL: ClassVar[NumericField] = NumericField(
        "columnDepthLevel", "columnDepthLevel"
    )
    """
    Level of nesting of this column, used for STRUCT and NESTED columns.
    """

    SNOWFLAKE_DYNAMIC_TABLE: ClassVar[RelationField] = RelationField(
        "snowflakeDynamicTable"
    )
    """
    TBC
    """
    VIEW: ClassVar[RelationField] = RelationField("view")
    """
    TBC
    """
    NESTED_COLUMNS: ClassVar[RelationField] = RelationField("nestedColumns")
    """
    TBC
    """
    DATA_QUALITY_METRIC_DIMENSIONS: ClassVar[RelationField] = RelationField(
        "dataQualityMetricDimensions"
    )
    """
    TBC
    """
    DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField("dbtModelColumns")
    """
    TBC
    """
    TABLE: ClassVar[RelationField] = RelationField("table")
    """
    TBC
    """
    COLUMN_DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField(
        "columnDbtModelColumns"
    )
    """
    TBC
    """
    MATERIALISED_VIEW: ClassVar[RelationField] = RelationField("materialisedView")
    """
    TBC
    """
    CALCULATION_VIEW: ClassVar[RelationField] = RelationField("calculationView")
    """
    TBC
    """
    PARENT_COLUMN: ClassVar[RelationField] = RelationField("parentColumn")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    METRIC_TIMESTAMPS: ClassVar[RelationField] = RelationField("metricTimestamps")
    """
    TBC
    """
    FOREIGN_KEY_TO: ClassVar[RelationField] = RelationField("foreignKeyTo")
    """
    TBC
    """
    FOREIGN_KEY_FROM: ClassVar[RelationField] = RelationField("foreignKeyFrom")
    """
    TBC
    """
    DBT_METRICS: ClassVar[RelationField] = RelationField("dbtMetrics")
    """
    TBC
    """
    TABLE_PARTITION: ClassVar[RelationField] = RelationField("tablePartition")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_type",
        "sub_data_type",
        "raw_data_type_definition",
        "order",
        "nested_column_count",
        "is_partition",
        "partition_order",
        "is_clustered",
        "is_primary",
        "is_foreign",
        "is_indexed",
        "is_sort",
        "is_dist",
        "is_pinned",
        "pinned_by",
        "pinned_at",
        "precision",
        "default_value",
        "is_nullable",
        "numeric_scale",
        "max_length",
        "validations",
        "parent_column_qualified_name",
        "parent_column_name",
        "column_distinct_values_count",
        "column_distinct_values_count_long",
        "column_histogram",
        "column_max",
        "column_min",
        "column_mean",
        "column_sum",
        "column_median",
        "column_standard_deviation",
        "column_unique_values_count",
        "column_unique_values_count_long",
        "column_average",
        "column_average_length",
        "column_duplicate_values_count",
        "column_duplicate_values_count_long",
        "column_maximum_string_length",
        "column_maxs",
        "column_minimum_string_length",
        "column_mins",
        "column_missing_values_count",
        "column_missing_values_count_long",
        "column_missing_values_percentage",
        "column_uniqueness_percentage",
        "column_variance",
        "column_top_values",
        "column_depth_level",
        "snowflake_dynamic_table",
        "view",
        "nested_columns",
        "data_quality_metric_dimensions",
        "dbt_model_columns",
        "table",
        "column_dbt_model_columns",
        "materialised_view",
        "calculation_view",
        "parent_column",
        "queries",
        "metric_timestamps",
        "foreign_key_to",
        "foreign_key_from",
        "dbt_metrics",
        "table_partition",
    ]

    @property
    def data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_type

    @data_type.setter
    def data_type(self, data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_type = data_type

    @property
    def sub_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sub_data_type

    @sub_data_type.setter
    def sub_data_type(self, sub_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sub_data_type = sub_data_type

    @property
    def raw_data_type_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.raw_data_type_definition
        )

    @raw_data_type_definition.setter
    def raw_data_type_definition(self, raw_data_type_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.raw_data_type_definition = raw_data_type_definition

    @property
    def order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.order

    @order.setter
    def order(self, order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.order = order

    @property
    def nested_column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.nested_column_count

    @nested_column_count.setter
    def nested_column_count(self, nested_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nested_column_count = nested_column_count

    @property
    def is_partition(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_partition

    @is_partition.setter
    def is_partition(self, is_partition: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partition = is_partition

    @property
    def partition_order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.partition_order

    @partition_order.setter
    def partition_order(self, partition_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_order = partition_order

    @property
    def is_clustered(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_clustered

    @is_clustered.setter
    def is_clustered(self, is_clustered: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_clustered = is_clustered

    @property
    def is_primary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_primary

    @is_primary.setter
    def is_primary(self, is_primary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_primary = is_primary

    @property
    def is_foreign(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_foreign

    @is_foreign.setter
    def is_foreign(self, is_foreign: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_foreign = is_foreign

    @property
    def is_indexed(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_indexed

    @is_indexed.setter
    def is_indexed(self, is_indexed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_indexed = is_indexed

    @property
    def is_sort(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_sort

    @is_sort.setter
    def is_sort(self, is_sort: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sort = is_sort

    @property
    def is_dist(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_dist

    @is_dist.setter
    def is_dist(self, is_dist: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_dist = is_dist

    @property
    def is_pinned(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_pinned

    @is_pinned.setter
    def is_pinned(self, is_pinned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_pinned = is_pinned

    @property
    def pinned_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.pinned_by

    @pinned_by.setter
    def pinned_by(self, pinned_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pinned_by = pinned_by

    @property
    def pinned_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.pinned_at

    @pinned_at.setter
    def pinned_at(self, pinned_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pinned_at = pinned_at

    @property
    def precision(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.precision

    @precision.setter
    def precision(self, precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.precision = precision

    @property
    def default_value(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.default_value

    @default_value.setter
    def default_value(self, default_value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_value = default_value

    @property
    def is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_nullable

    @is_nullable.setter
    def is_nullable(self, is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_nullable = is_nullable

    @property
    def numeric_scale(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.numeric_scale

    @numeric_scale.setter
    def numeric_scale(self, numeric_scale: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.numeric_scale = numeric_scale

    @property
    def max_length(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.max_length

    @max_length.setter
    def max_length(self, max_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.max_length = max_length

    @property
    def validations(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.validations

    @validations.setter
    def validations(self, validations: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.validations = validations

    @property
    def parent_column_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.parent_column_qualified_name
        )

    @parent_column_qualified_name.setter
    def parent_column_qualified_name(self, parent_column_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_column_qualified_name = parent_column_qualified_name

    @property
    def parent_column_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.parent_column_name

    @parent_column_name.setter
    def parent_column_name(self, parent_column_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_column_name = parent_column_name

    @property
    def column_distinct_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_distinct_values_count
        )

    @column_distinct_values_count.setter
    def column_distinct_values_count(self, column_distinct_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_distinct_values_count = column_distinct_values_count

    @property
    def column_distinct_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_distinct_values_count_long
        )

    @column_distinct_values_count_long.setter
    def column_distinct_values_count_long(
        self, column_distinct_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_distinct_values_count_long = (
            column_distinct_values_count_long
        )

    @property
    def column_histogram(self) -> Optional[Histogram]:
        return None if self.attributes is None else self.attributes.column_histogram

    @column_histogram.setter
    def column_histogram(self, column_histogram: Optional[Histogram]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_histogram = column_histogram

    @property
    def column_max(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_max

    @column_max.setter
    def column_max(self, column_max: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_max = column_max

    @property
    def column_min(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_min

    @column_min.setter
    def column_min(self, column_min: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_min = column_min

    @property
    def column_mean(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_mean

    @column_mean.setter
    def column_mean(self, column_mean: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_mean = column_mean

    @property
    def column_sum(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_sum

    @column_sum.setter
    def column_sum(self, column_sum: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_sum = column_sum

    @property
    def column_median(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_median

    @column_median.setter
    def column_median(self, column_median: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_median = column_median

    @property
    def column_standard_deviation(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_standard_deviation
        )

    @column_standard_deviation.setter
    def column_standard_deviation(self, column_standard_deviation: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_standard_deviation = column_standard_deviation

    @property
    def column_unique_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_unique_values_count
        )

    @column_unique_values_count.setter
    def column_unique_values_count(self, column_unique_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_unique_values_count = column_unique_values_count

    @property
    def column_unique_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_unique_values_count_long
        )

    @column_unique_values_count_long.setter
    def column_unique_values_count_long(
        self, column_unique_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_unique_values_count_long = (
            column_unique_values_count_long
        )

    @property
    def column_average(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_average

    @column_average.setter
    def column_average(self, column_average: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_average = column_average

    @property
    def column_average_length(self) -> Optional[float]:
        return (
            None if self.attributes is None else self.attributes.column_average_length
        )

    @column_average_length.setter
    def column_average_length(self, column_average_length: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_average_length = column_average_length

    @property
    def column_duplicate_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_duplicate_values_count
        )

    @column_duplicate_values_count.setter
    def column_duplicate_values_count(
        self, column_duplicate_values_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_duplicate_values_count = column_duplicate_values_count

    @property
    def column_duplicate_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_duplicate_values_count_long
        )

    @column_duplicate_values_count_long.setter
    def column_duplicate_values_count_long(
        self, column_duplicate_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_duplicate_values_count_long = (
            column_duplicate_values_count_long
        )

    @property
    def column_maximum_string_length(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_maximum_string_length
        )

    @column_maximum_string_length.setter
    def column_maximum_string_length(self, column_maximum_string_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_maximum_string_length = column_maximum_string_length

    @property
    def column_maxs(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.column_maxs

    @column_maxs.setter
    def column_maxs(self, column_maxs: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_maxs = column_maxs

    @property
    def column_minimum_string_length(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_minimum_string_length
        )

    @column_minimum_string_length.setter
    def column_minimum_string_length(self, column_minimum_string_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_minimum_string_length = column_minimum_string_length

    @property
    def column_mins(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.column_mins

    @column_mins.setter
    def column_mins(self, column_mins: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_mins = column_mins

    @property
    def column_missing_values_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_missing_values_count
        )

    @column_missing_values_count.setter
    def column_missing_values_count(self, column_missing_values_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_missing_values_count = column_missing_values_count

    @property
    def column_missing_values_count_long(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_missing_values_count_long
        )

    @column_missing_values_count_long.setter
    def column_missing_values_count_long(
        self, column_missing_values_count_long: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_missing_values_count_long = (
            column_missing_values_count_long
        )

    @property
    def column_missing_values_percentage(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_missing_values_percentage
        )

    @column_missing_values_percentage.setter
    def column_missing_values_percentage(
        self, column_missing_values_percentage: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_missing_values_percentage = (
            column_missing_values_percentage
        )

    @property
    def column_uniqueness_percentage(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_uniqueness_percentage
        )

    @column_uniqueness_percentage.setter
    def column_uniqueness_percentage(
        self, column_uniqueness_percentage: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_uniqueness_percentage = column_uniqueness_percentage

    @property
    def column_variance(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.column_variance

    @column_variance.setter
    def column_variance(self, column_variance: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_variance = column_variance

    @property
    def column_top_values(self) -> Optional[List[ColumnValueFrequencyMap]]:
        return None if self.attributes is None else self.attributes.column_top_values

    @column_top_values.setter
    def column_top_values(
        self, column_top_values: Optional[List[ColumnValueFrequencyMap]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_top_values = column_top_values

    @property
    def column_depth_level(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_depth_level

    @column_depth_level.setter
    def column_depth_level(self, column_depth_level: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_depth_level = column_depth_level

    @property
    def snowflake_dynamic_table(self) -> Optional[SnowflakeDynamicTable]:
        return (
            None if self.attributes is None else self.attributes.snowflake_dynamic_table
        )

    @snowflake_dynamic_table.setter
    def snowflake_dynamic_table(
        self, snowflake_dynamic_table: Optional[SnowflakeDynamicTable]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_dynamic_table = snowflake_dynamic_table

    @property
    def view(self) -> Optional[View]:
        return None if self.attributes is None else self.attributes.view

    @view.setter
    def view(self, view: Optional[View]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view = view

    @property
    def nested_columns(self) -> Optional[List[Column]]:
        return None if self.attributes is None else self.attributes.nested_columns

    @nested_columns.setter
    def nested_columns(self, nested_columns: Optional[List[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nested_columns = nested_columns

    @property
    def data_quality_metric_dimensions(self) -> Optional[List[Metric]]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_quality_metric_dimensions
        )

    @data_quality_metric_dimensions.setter
    def data_quality_metric_dimensions(
        self, data_quality_metric_dimensions: Optional[List[Metric]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_quality_metric_dimensions = data_quality_metric_dimensions

    @property
    def dbt_model_columns(self) -> Optional[List[DbtModelColumn]]:
        return None if self.attributes is None else self.attributes.dbt_model_columns

    @dbt_model_columns.setter
    def dbt_model_columns(self, dbt_model_columns: Optional[List[DbtModelColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_columns = dbt_model_columns

    @property
    def table(self) -> Optional[Table]:
        return None if self.attributes is None else self.attributes.table

    @table.setter
    def table(self, table: Optional[Table]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table = table

    @property
    def column_dbt_model_columns(self) -> Optional[List[DbtModelColumn]]:
        return (
            None
            if self.attributes is None
            else self.attributes.column_dbt_model_columns
        )

    @column_dbt_model_columns.setter
    def column_dbt_model_columns(
        self, column_dbt_model_columns: Optional[List[DbtModelColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_dbt_model_columns = column_dbt_model_columns

    @property
    def materialised_view(self) -> Optional[MaterialisedView]:
        return None if self.attributes is None else self.attributes.materialised_view

    @materialised_view.setter
    def materialised_view(self, materialised_view: Optional[MaterialisedView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.materialised_view = materialised_view

    @property
    def calculation_view(self) -> Optional[CalculationView]:
        return None if self.attributes is None else self.attributes.calculation_view

    @calculation_view.setter
    def calculation_view(self, calculation_view: Optional[CalculationView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view = calculation_view

    @property
    def parent_column(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.parent_column

    @parent_column.setter
    def parent_column(self, parent_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_column = parent_column

    @property
    def queries(self) -> Optional[List[Query]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[List[Query]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def metric_timestamps(self) -> Optional[List[Metric]]:
        return None if self.attributes is None else self.attributes.metric_timestamps

    @metric_timestamps.setter
    def metric_timestamps(self, metric_timestamps: Optional[List[Metric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_timestamps = metric_timestamps

    @property
    def foreign_key_to(self) -> Optional[List[Column]]:
        return None if self.attributes is None else self.attributes.foreign_key_to

    @foreign_key_to.setter
    def foreign_key_to(self, foreign_key_to: Optional[List[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.foreign_key_to = foreign_key_to

    @property
    def foreign_key_from(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.foreign_key_from

    @foreign_key_from.setter
    def foreign_key_from(self, foreign_key_from: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.foreign_key_from = foreign_key_from

    @property
    def dbt_metrics(self) -> Optional[List[DbtMetric]]:
        return None if self.attributes is None else self.attributes.dbt_metrics

    @dbt_metrics.setter
    def dbt_metrics(self, dbt_metrics: Optional[List[DbtMetric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metrics = dbt_metrics

    @property
    def table_partition(self) -> Optional[TablePartition]:
        return None if self.attributes is None else self.attributes.table_partition

    @table_partition.setter
    def table_partition(self, table_partition: Optional[TablePartition]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_partition = table_partition

    class Attributes(SQL.Attributes):
        data_type: Optional[str] = Field(default=None, description="")
        sub_data_type: Optional[str] = Field(default=None, description="")
        raw_data_type_definition: Optional[str] = Field(default=None, description="")
        order: Optional[int] = Field(default=None, description="")
        nested_column_count: Optional[int] = Field(default=None, description="")
        is_partition: Optional[bool] = Field(default=None, description="")
        partition_order: Optional[int] = Field(default=None, description="")
        is_clustered: Optional[bool] = Field(default=None, description="")
        is_primary: Optional[bool] = Field(default=None, description="")
        is_foreign: Optional[bool] = Field(default=None, description="")
        is_indexed: Optional[bool] = Field(default=None, description="")
        is_sort: Optional[bool] = Field(default=None, description="")
        is_dist: Optional[bool] = Field(default=None, description="")
        is_pinned: Optional[bool] = Field(default=None, description="")
        pinned_by: Optional[str] = Field(default=None, description="")
        pinned_at: Optional[datetime] = Field(default=None, description="")
        precision: Optional[int] = Field(default=None, description="")
        default_value: Optional[str] = Field(default=None, description="")
        is_nullable: Optional[bool] = Field(default=None, description="")
        numeric_scale: Optional[float] = Field(default=None, description="")
        max_length: Optional[int] = Field(default=None, description="")
        validations: Optional[Dict[str, str]] = Field(default=None, description="")
        parent_column_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        parent_column_name: Optional[str] = Field(default=None, description="")
        column_distinct_values_count: Optional[int] = Field(
            default=None, description=""
        )
        column_distinct_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_histogram: Optional[Histogram] = Field(default=None, description="")
        column_max: Optional[float] = Field(default=None, description="")
        column_min: Optional[float] = Field(default=None, description="")
        column_mean: Optional[float] = Field(default=None, description="")
        column_sum: Optional[float] = Field(default=None, description="")
        column_median: Optional[float] = Field(default=None, description="")
        column_standard_deviation: Optional[float] = Field(default=None, description="")
        column_unique_values_count: Optional[int] = Field(default=None, description="")
        column_unique_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_average: Optional[float] = Field(default=None, description="")
        column_average_length: Optional[float] = Field(default=None, description="")
        column_duplicate_values_count: Optional[int] = Field(
            default=None, description=""
        )
        column_duplicate_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_maximum_string_length: Optional[int] = Field(
            default=None, description=""
        )
        column_maxs: Optional[Set[str]] = Field(default=None, description="")
        column_minimum_string_length: Optional[int] = Field(
            default=None, description=""
        )
        column_mins: Optional[Set[str]] = Field(default=None, description="")
        column_missing_values_count: Optional[int] = Field(default=None, description="")
        column_missing_values_count_long: Optional[int] = Field(
            default=None, description=""
        )
        column_missing_values_percentage: Optional[float] = Field(
            default=None, description=""
        )
        column_uniqueness_percentage: Optional[float] = Field(
            default=None, description=""
        )
        column_variance: Optional[float] = Field(default=None, description="")
        column_top_values: Optional[List[ColumnValueFrequencyMap]] = Field(
            default=None, description=""
        )
        column_depth_level: Optional[int] = Field(default=None, description="")
        snowflake_dynamic_table: Optional[SnowflakeDynamicTable] = Field(
            default=None, description=""
        )  # relationship
        view: Optional[View] = Field(default=None, description="")  # relationship
        nested_columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        data_quality_metric_dimensions: Optional[List[Metric]] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_columns: Optional[List[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        table: Optional[Table] = Field(default=None, description="")  # relationship
        column_dbt_model_columns: Optional[List[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        materialised_view: Optional[MaterialisedView] = Field(
            default=None, description=""
        )  # relationship
        calculation_view: Optional[CalculationView] = Field(
            default=None, description=""
        )  # relationship
        parent_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        queries: Optional[List[Query]] = Field(
            default=None, description=""
        )  # relationship
        metric_timestamps: Optional[List[Metric]] = Field(
            default=None, description=""
        )  # relationship
        foreign_key_to: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        foreign_key_from: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        dbt_metrics: Optional[List[DbtMetric]] = Field(
            default=None, description=""
        )  # relationship
        table_partition: Optional[TablePartition] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            parent_qualified_name: str,
            parent_type: type,
            order: int,
            parent_name: Optional[str] = None,
            database_name: Optional[str] = None,
            database_qualified_name: Optional[str] = None,
            schema_name: Optional[str] = None,
            schema_qualified_name: Optional[str] = None,
            table_name: Optional[str] = None,
            table_qualified_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
        ) -> Column.Attributes:
            validate_required_fields(
                ["name", "parent_qualified_name", "parent_type", "order"],
                [name, parent_qualified_name, parent_type, order],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    parent_qualified_name, "parent_qualified_name", 6
                )
            if order < 0:
                raise ValueError("Order must be be a positive integer")

            fields = parent_qualified_name.split("/")
            qualified_name = f"{parent_qualified_name}/{name}"
            connection_qualified_name = connection_qualified_name or connection_qn
            database_name = database_name or fields[3]
            schema_name = schema_name or fields[4]
            parent_name = parent_name or fields[5]
            database_qualified_name = (
                database_qualified_name
                or f"{connection_qualified_name}/{database_name}"
            )
            schema_qualified_name = (
                schema_qualified_name or f"{database_qualified_name}/{schema_name}"
            )

            column = Column.Attributes(
                name=name,
                order=order,
                qualified_name=qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
                schema_name=schema_name,
                schema_qualified_name=schema_qualified_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
            )

            if parent_type == Table:
                column.table_qualified_name = parent_qualified_name
                column.table = Table.ref_by_qualified_name(parent_qualified_name)
                column.table_name = parent_name
            elif parent_type == View:
                column.view_qualified_name = parent_qualified_name
                column.view = View.ref_by_qualified_name(parent_qualified_name)
                column.view_name = parent_name
            elif parent_type == MaterialisedView:
                column.view_qualified_name = parent_qualified_name
                column.materialised_view = MaterialisedView.ref_by_qualified_name(
                    parent_qualified_name
                )
                column.view_name = parent_name
            elif parent_type == TablePartition:
                column.table_qualified_name = table_qualified_name
                column.table_partition = TablePartition.ref_by_qualified_name(
                    parent_qualified_name
                )
                column.table_name = table_name
            else:
                raise ValueError(
                    "parent_type must be either Table, View, MaterializeView or TablePartition"
                )
            return column

    attributes: Column.Attributes = Field(
        default_factory=lambda: Column.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .calculation_view import CalculationView  # noqa
from .dbt_metric import DbtMetric  # noqa
from .dbt_model_column import DbtModelColumn  # noqa
from .materialised_view import MaterialisedView  # noqa
from .metric import Metric  # noqa
from .query import Query  # noqa
from .snowflake_dynamic_table import SnowflakeDynamicTable  # noqa
from .table import Table  # noqa
from .table_partition import TablePartition  # noqa
from .view import View  # noqa
