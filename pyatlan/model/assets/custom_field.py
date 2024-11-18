# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import CustomTemperatureType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import ColumnValueFrequencyMap, Histogram

from .core.column import Column


class CustomField(Column):
    """Description"""

    type_name: str = Field(default="CustomField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CustomField":
            raise ValueError("must be CustomField")
        return v

    def __setattr__(self, name, value):
        if name in CustomField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUSTOM_TEMPERATURE: ClassVar[KeywordField] = KeywordField(
        "customTemperature", "customTemperature"
    )
    """
    Temperature of the CustomTable asset.
    """
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
    RAW_DATA_TYPE_DEFINITION: ClassVar[TextField] = TextField(
        "rawDataTypeDefinition", "rawDataTypeDefinition"
    )
    """

    """
    ORDER: ClassVar[NumericField] = NumericField("order", "order")
    """
    Order (position) in which this column appears in the table (starting at 1).
    """
    NESTED_COLUMN_ORDER: ClassVar[KeywordField] = KeywordField(
        "nestedColumnOrder", "nestedColumnOrder"
    )
    """
    Order (position) in which this column appears in the nested Column (nest level starts at 1).
    """
    NESTED_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "nestedColumnCount", "nestedColumnCount"
    )
    """
    Number of columns nested within this (STRUCT or NESTED) column.
    """
    COLUMN_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "columnHierarchy", "columnHierarchy"
    )
    """
    List of top-level upstream nested columns.
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
    DEFAULT_VALUE: ClassVar[TextField] = TextField("defaultValue", "defaultValue")
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
    COLUMN_MAXS: ClassVar[TextField] = TextField("columnMaxs", "columnMaxs")
    """
    List of the greatest values in a column.
    """
    COLUMN_MINIMUM_STRING_LENGTH: ClassVar[NumericField] = NumericField(
        "columnMinimumStringLength", "columnMinimumStringLength"
    )
    """
    Length of the shortest value in a string column.
    """
    COLUMN_MINS: ClassVar[TextField] = TextField("columnMins", "columnMins")
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
    NOSQL_COLLECTION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "nosqlCollectionName", "nosqlCollectionName.keyword", "nosqlCollectionName"
    )
    """
    Simple name of the cosmos/mongo collection in which this SQL asset (column) exists, or empty if it does not exist within a cosmos/mongo collection.
    """  # noqa: E501
    NOSQL_COLLECTION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "nosqlCollectionQualifiedName", "nosqlCollectionQualifiedName"
    )
    """
    Unique name of the cosmos/mongo collection in which this SQL asset (column) exists, or empty if it does not exist within a cosmos/mongo collection.
    """  # noqa: E501
    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    Number of times this asset has been queried.
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    Number of unique users who have queried this asset.
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    Map of unique users who have queried this asset to the number of times they have queried it.
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    Time (epoch) at which the query count was last updated, in milliseconds.
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    Simple name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    Unique name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    Simple name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    Unique name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    Simple name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    Unique name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    Simple name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    Unique name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    CALCULATION_VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "calculationViewName", "calculationViewName.keyword", "calculationViewName"
    )
    """
    Simple name of the calculation view in which this SQL asset exists, or empty if it does not exist within a calculation view.
    """  # noqa: E501
    CALCULATION_VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "calculationViewQualifiedName", "calculationViewQualifiedName"
    )
    """
    Unique name of the calculation view in which this SQL asset exists, or empty if it does not exist within a calculation view.
    """  # noqa: E501
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    Whether this asset has been profiled (true) or not (false).
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    Time (epoch) at which this asset was last profiled, in milliseconds.
    """
    ASSET_APPLICATION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "assetApplicationQualifiedName", "assetApplicationQualifiedName"
    )
    """
    Qualified name of the Application Container that contains this asset.
    """
    CUSTOM_SOURCE_ID: ClassVar[KeywordField] = KeywordField(
        "customSourceId", "customSourceId"
    )
    """
    Unique identifier for the Custom asset from the source system.
    """
    CUSTOM_DATASET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "customDatasetName", "customDatasetName.keyword", "customDatasetName"
    )
    """
    Simple name of the dataset in which this asset exists, or empty if it is itself a dataset.
    """
    CUSTOM_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "customDatasetQualifiedName", "customDatasetQualifiedName"
    )
    """
    Unique name of the dataset in which this asset exists, or empty if it is itself a dataset.
    """

    CUSTOM_TABLE: ClassVar[RelationField] = RelationField("customTable")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "custom_temperature",
        "data_type",
        "sub_data_type",
        "raw_data_type_definition",
        "order",
        "nested_column_order",
        "nested_column_count",
        "column_hierarchy",
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
        "nosql_collection_name",
        "nosql_collection_qualified_name",
        "query_count",
        "query_user_count",
        "query_user_map",
        "query_count_updated_at",
        "database_name",
        "database_qualified_name",
        "schema_name",
        "schema_qualified_name",
        "table_name",
        "table_qualified_name",
        "view_name",
        "view_qualified_name",
        "calculation_view_name",
        "calculation_view_qualified_name",
        "is_profiled",
        "last_profiled_at",
        "asset_application_qualified_name",
        "custom_source_id",
        "custom_dataset_name",
        "custom_dataset_qualified_name",
        "custom_table",
    ]

    @property
    def custom_temperature(self) -> Optional[CustomTemperatureType]:
        return None if self.attributes is None else self.attributes.custom_temperature

    @custom_temperature.setter
    def custom_temperature(self, custom_temperature: Optional[CustomTemperatureType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_temperature = custom_temperature

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
    def nested_column_order(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.nested_column_order

    @nested_column_order.setter
    def nested_column_order(self, nested_column_order: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nested_column_order = nested_column_order

    @property
    def nested_column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.nested_column_count

    @nested_column_count.setter
    def nested_column_count(self, nested_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nested_column_count = nested_column_count

    @property
    def column_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.column_hierarchy

    @column_hierarchy.setter
    def column_hierarchy(self, column_hierarchy: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_hierarchy = column_hierarchy

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
    def nosql_collection_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.nosql_collection_name
        )

    @nosql_collection_name.setter
    def nosql_collection_name(self, nosql_collection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nosql_collection_name = nosql_collection_name

    @property
    def nosql_collection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.nosql_collection_qualified_name
        )

    @nosql_collection_qualified_name.setter
    def nosql_collection_qualified_name(
        self, nosql_collection_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.nosql_collection_qualified_name = (
            nosql_collection_qualified_name
        )

    @property
    def query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_count

    @query_count.setter
    def query_count(self, query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count = query_count

    @property
    def query_user_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_user_count

    @query_user_count.setter
    def query_user_count(self, query_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_count = query_user_count

    @property
    def query_user_map(self) -> Optional[Dict[str, int]]:
        return None if self.attributes is None else self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[Dict[str, int]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_map = query_user_map

    @property
    def query_count_updated_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.query_count_updated_at
        )

    @query_count_updated_at.setter
    def query_count_updated_at(self, query_count_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count_updated_at = query_count_updated_at

    @property
    def database_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.database_name

    @database_name.setter
    def database_name(self, database_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_name = database_name

    @property
    def database_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.database_qualified_name
        )

    @database_qualified_name.setter
    def database_qualified_name(self, database_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_qualified_name = database_qualified_name

    @property
    def schema_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.schema_name

    @schema_name.setter
    def schema_name(self, schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_name = schema_name

    @property
    def schema_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.schema_qualified_name
        )

    @schema_qualified_name.setter
    def schema_qualified_name(self, schema_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_qualified_name = schema_qualified_name

    @property
    def table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_name

    @table_name.setter
    def table_name(self, table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_name = table_name

    @property
    def table_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_qualified_name

    @table_qualified_name.setter
    def table_qualified_name(self, table_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_qualified_name = table_qualified_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def view_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_qualified_name

    @view_qualified_name.setter
    def view_qualified_name(self, view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_qualified_name = view_qualified_name

    @property
    def calculation_view_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.calculation_view_name
        )

    @calculation_view_name.setter
    def calculation_view_name(self, calculation_view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_name = calculation_view_name

    @property
    def calculation_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.calculation_view_qualified_name
        )

    @calculation_view_qualified_name.setter
    def calculation_view_qualified_name(
        self, calculation_view_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_qualified_name = (
            calculation_view_qualified_name
        )

    @property
    def is_profiled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_profiled

    @is_profiled.setter
    def is_profiled(self, is_profiled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_profiled = is_profiled

    @property
    def last_profiled_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.last_profiled_at

    @last_profiled_at.setter
    def last_profiled_at(self, last_profiled_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_profiled_at = last_profiled_at

    @property
    def asset_application_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_application_qualified_name
        )

    @asset_application_qualified_name.setter
    def asset_application_qualified_name(
        self, asset_application_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_application_qualified_name = (
            asset_application_qualified_name
        )

    @property
    def custom_source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.custom_source_id

    @custom_source_id.setter
    def custom_source_id(self, custom_source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_source_id = custom_source_id

    @property
    def custom_dataset_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.custom_dataset_name

    @custom_dataset_name.setter
    def custom_dataset_name(self, custom_dataset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_dataset_name = custom_dataset_name

    @property
    def custom_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.custom_dataset_qualified_name
        )

    @custom_dataset_qualified_name.setter
    def custom_dataset_qualified_name(
        self, custom_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_dataset_qualified_name = custom_dataset_qualified_name

    @property
    def custom_table(self) -> Optional[CustomTable]:
        return None if self.attributes is None else self.attributes.custom_table

    @custom_table.setter
    def custom_table(self, custom_table: Optional[CustomTable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_table = custom_table

    class Attributes(Column.Attributes):
        custom_temperature: Optional[CustomTemperatureType] = Field(
            default=None, description=""
        )
        data_type: Optional[str] = Field(default=None, description="")
        sub_data_type: Optional[str] = Field(default=None, description="")
        raw_data_type_definition: Optional[str] = Field(default=None, description="")
        order: Optional[int] = Field(default=None, description="")
        nested_column_order: Optional[str] = Field(default=None, description="")
        nested_column_count: Optional[int] = Field(default=None, description="")
        column_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
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
        nosql_collection_name: Optional[str] = Field(default=None, description="")
        nosql_collection_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        query_count: Optional[int] = Field(default=None, description="")
        query_user_count: Optional[int] = Field(default=None, description="")
        query_user_map: Optional[Dict[str, int]] = Field(default=None, description="")
        query_count_updated_at: Optional[datetime] = Field(default=None, description="")
        database_name: Optional[str] = Field(default=None, description="")
        database_qualified_name: Optional[str] = Field(default=None, description="")
        schema_name: Optional[str] = Field(default=None, description="")
        schema_qualified_name: Optional[str] = Field(default=None, description="")
        table_name: Optional[str] = Field(default=None, description="")
        table_qualified_name: Optional[str] = Field(default=None, description="")
        view_name: Optional[str] = Field(default=None, description="")
        view_qualified_name: Optional[str] = Field(default=None, description="")
        calculation_view_name: Optional[str] = Field(default=None, description="")
        calculation_view_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        is_profiled: Optional[bool] = Field(default=None, description="")
        last_profiled_at: Optional[datetime] = Field(default=None, description="")
        asset_application_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        custom_source_id: Optional[str] = Field(default=None, description="")
        custom_dataset_name: Optional[str] = Field(default=None, description="")
        custom_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        custom_table: Optional[CustomTable] = Field(
            default=None, description=""
        )  # relationship

    attributes: CustomField.Attributes = Field(
        default_factory=lambda: CustomField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .custom_table import CustomTable  # noqa

CustomField.Attributes.update_forward_refs()
