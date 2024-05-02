# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DynamoDBStatus
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .table import Table


class DynamoDBTable(Table):
    """Description"""

    type_name: str = Field(default="DynamoDBTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DynamoDBTable":
            raise ValueError("must be DynamoDBTable")
        return v

    def __setattr__(self, name, value):
        if name in DynamoDBTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DYNAMO_DB_TABLE_GSI_COUNT: ClassVar[NumericField] = NumericField(
        "dynamoDBTableGSICount", "dynamoDBTableGSICount"
    )
    """
    Represents the number of global secondary indexes on the table.
    """
    DYNAMO_DB_TABLE_LSI_COUNT: ClassVar[NumericField] = NumericField(
        "dynamoDBTableLSICount", "dynamoDBTableLSICount"
    )
    """
    Represents the number of local secondary indexes on the table.
    """
    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    Number of columns in this table.
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    Number of rows in this table.
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    Size of this table, in bytes.
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    Alias for this table.
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    Whether this table is temporary (true) or not (false).
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    Whether preview queries are allowed for this table (true) or not (false).
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    Configuration for preview queries.
    """
    EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "externalLocation", "externalLocation"
    )
    """
    External location of this table, for example: an S3 object location.
    """
    EXTERNAL_LOCATION_REGION: ClassVar[KeywordField] = KeywordField(
        "externalLocationRegion", "externalLocationRegion"
    )
    """
    Region of the external location of this table, for example: S3 region.
    """
    EXTERNAL_LOCATION_FORMAT: ClassVar[KeywordField] = KeywordField(
        "externalLocationFormat", "externalLocationFormat"
    )
    """
    Format of the external location of this table, for example: JSON, CSV, PARQUET, etc.
    """
    IS_PARTITIONED: ClassVar[BooleanField] = BooleanField(
        "isPartitioned", "isPartitioned"
    )
    """
    Whether this table is partitioned (true) or not (false).
    """
    PARTITION_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "partitionStrategy", "partitionStrategy"
    )
    """
    Partition strategy for this table.
    """
    PARTITION_COUNT: ClassVar[NumericField] = NumericField(
        "partitionCount", "partitionCount"
    )
    """
    Number of partitions in this table.
    """
    PARTITION_LIST: ClassVar[KeywordField] = KeywordField(
        "partitionList", "partitionList"
    )
    """
    List of partitions in this table.
    """
    IS_SHARDED: ClassVar[BooleanField] = BooleanField("isSharded", "isSharded")
    """
    Whether this table is a sharded table (true) or not (false).
    """
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
    DYNAMO_DB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dynamoDBStatus", "dynamoDBStatus"
    )
    """
    Status of the DynamoDB Asset
    """
    DYNAMO_DB_PARTITION_KEY: ClassVar[KeywordField] = KeywordField(
        "dynamoDBPartitionKey", "dynamoDBPartitionKey"
    )
    """
    Specifies the partition key of the DynamoDB Table/Index
    """
    DYNAMO_DB_SORT_KEY: ClassVar[KeywordField] = KeywordField(
        "dynamoDBSortKey", "dynamoDBSortKey"
    )
    """
    Specifies the sort key of the DynamoDB Table/Index
    """
    DYNAMO_DB_READ_CAPACITY_UNITS: ClassVar[NumericField] = NumericField(
        "dynamoDBReadCapacityUnits", "dynamoDBReadCapacityUnits"
    )
    """
    The maximum number of strongly consistent reads consumed per second before DynamoDB returns a ThrottlingException
    """
    DYNAMO_DB_WRITE_CAPACITY_UNITS: ClassVar[NumericField] = NumericField(
        "dynamoDBWriteCapacityUnits", "dynamoDBWriteCapacityUnits"
    )
    """
    The maximum number of writes consumed per second before DynamoDB returns a ThrottlingException
    """
    NO_SQL_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "noSQLSchemaDefinition", "noSQLSchemaDefinition"
    )
    """
    Represents attributes for describing the key schema for the table and indexes.
    """

    DYNAMO_DB_LOCAL_SECONDARY_INDEXES: ClassVar[RelationField] = RelationField(
        "dynamoDBLocalSecondaryIndexes"
    )
    """
    TBC
    """
    DYNAMO_DB_GLOBAL_SECONDARY_INDEXES: ClassVar[RelationField] = RelationField(
        "dynamoDBGlobalSecondaryIndexes"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dynamo_dbtable_g_s_i_count",
        "dynamo_dbtable_l_s_i_count",
        "column_count",
        "row_count",
        "size_bytes",
        "alias",
        "is_temporary",
        "is_query_preview",
        "query_preview_config",
        "external_location",
        "external_location_region",
        "external_location_format",
        "is_partitioned",
        "partition_strategy",
        "partition_count",
        "partition_list",
        "is_sharded",
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
        "dynamo_d_b_status",
        "dynamo_d_b_partition_key",
        "dynamo_d_b_sort_key",
        "dynamo_d_b_read_capacity_units",
        "dynamo_d_b_write_capacity_units",
        "no_s_q_l_schema_definition",
        "dynamo_d_b_local_secondary_indexes",
        "dynamo_d_b_global_secondary_indexes",
    ]

    @property
    def dynamo_dbtable_g_s_i_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_dbtable_g_s_i_count
        )

    @dynamo_dbtable_g_s_i_count.setter
    def dynamo_dbtable_g_s_i_count(self, dynamo_dbtable_g_s_i_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_dbtable_g_s_i_count = dynamo_dbtable_g_s_i_count

    @property
    def dynamo_dbtable_l_s_i_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_dbtable_l_s_i_count
        )

    @dynamo_dbtable_l_s_i_count.setter
    def dynamo_dbtable_l_s_i_count(self, dynamo_dbtable_l_s_i_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_dbtable_l_s_i_count = dynamo_dbtable_l_s_i_count

    @property
    def column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def row_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.row_count

    @row_count.setter
    def row_count(self, row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.row_count = row_count

    @property
    def size_bytes(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.size_bytes

    @size_bytes.setter
    def size_bytes(self, size_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.size_bytes = size_bytes

    @property
    def alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.alias

    @alias.setter
    def alias(self, alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alias = alias

    @property
    def is_temporary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_temporary

    @is_temporary.setter
    def is_temporary(self, is_temporary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_temporary = is_temporary

    @property
    def is_query_preview(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_query_preview

    @is_query_preview.setter
    def is_query_preview(self, is_query_preview: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_query_preview = is_query_preview

    @property
    def query_preview_config(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_preview_config = query_preview_config

    @property
    def external_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.external_location

    @external_location.setter
    def external_location(self, external_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location = external_location

    @property
    def external_location_region(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.external_location_region
        )

    @external_location_region.setter
    def external_location_region(self, external_location_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_region = external_location_region

    @property
    def external_location_format(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.external_location_format
        )

    @external_location_format.setter
    def external_location_format(self, external_location_format: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_location_format = external_location_format

    @property
    def is_partitioned(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_partitioned

    @is_partitioned.setter
    def is_partitioned(self, is_partitioned: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_partitioned = is_partitioned

    @property
    def partition_strategy(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partition_strategy

    @partition_strategy.setter
    def partition_strategy(self, partition_strategy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_strategy = partition_strategy

    @property
    def partition_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.partition_count

    @partition_count.setter
    def partition_count(self, partition_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_count = partition_count

    @property
    def partition_list(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partition_list

    @partition_list.setter
    def partition_list(self, partition_list: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partition_list = partition_list

    @property
    def is_sharded(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_sharded

    @is_sharded.setter
    def is_sharded(self, is_sharded: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_sharded = is_sharded

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
    def dynamo_d_b_status(self) -> Optional[DynamoDBStatus]:
        return None if self.attributes is None else self.attributes.dynamo_d_b_status

    @dynamo_d_b_status.setter
    def dynamo_d_b_status(self, dynamo_d_b_status: Optional[DynamoDBStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_status = dynamo_d_b_status

    @property
    def dynamo_d_b_partition_key(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_partition_key
        )

    @dynamo_d_b_partition_key.setter
    def dynamo_d_b_partition_key(self, dynamo_d_b_partition_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_partition_key = dynamo_d_b_partition_key

    @property
    def dynamo_d_b_sort_key(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dynamo_d_b_sort_key

    @dynamo_d_b_sort_key.setter
    def dynamo_d_b_sort_key(self, dynamo_d_b_sort_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_sort_key = dynamo_d_b_sort_key

    @property
    def dynamo_d_b_read_capacity_units(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_read_capacity_units
        )

    @dynamo_d_b_read_capacity_units.setter
    def dynamo_d_b_read_capacity_units(
        self, dynamo_d_b_read_capacity_units: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_read_capacity_units = dynamo_d_b_read_capacity_units

    @property
    def dynamo_d_b_write_capacity_units(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_write_capacity_units
        )

    @dynamo_d_b_write_capacity_units.setter
    def dynamo_d_b_write_capacity_units(
        self, dynamo_d_b_write_capacity_units: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_write_capacity_units = (
            dynamo_d_b_write_capacity_units
        )

    @property
    def no_s_q_l_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.no_s_q_l_schema_definition
        )

    @no_s_q_l_schema_definition.setter
    def no_s_q_l_schema_definition(self, no_s_q_l_schema_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.no_s_q_l_schema_definition = no_s_q_l_schema_definition

    @property
    def dynamo_d_b_local_secondary_indexes(
        self,
    ) -> Optional[List[DynamoDBLocalSecondaryIndex]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_local_secondary_indexes
        )

    @dynamo_d_b_local_secondary_indexes.setter
    def dynamo_d_b_local_secondary_indexes(
        self,
        dynamo_d_b_local_secondary_indexes: Optional[List[DynamoDBLocalSecondaryIndex]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_local_secondary_indexes = (
            dynamo_d_b_local_secondary_indexes
        )

    @property
    def dynamo_d_b_global_secondary_indexes(
        self,
    ) -> Optional[List[DynamoDBGlobalSecondaryIndex]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dynamo_d_b_global_secondary_indexes
        )

    @dynamo_d_b_global_secondary_indexes.setter
    def dynamo_d_b_global_secondary_indexes(
        self,
        dynamo_d_b_global_secondary_indexes: Optional[
            List[DynamoDBGlobalSecondaryIndex]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dynamo_d_b_global_secondary_indexes = (
            dynamo_d_b_global_secondary_indexes
        )

    class Attributes(Table.Attributes):
        dynamo_dbtable_g_s_i_count: Optional[int] = Field(default=None, description="")
        dynamo_dbtable_l_s_i_count: Optional[int] = Field(default=None, description="")
        column_count: Optional[int] = Field(default=None, description="")
        row_count: Optional[int] = Field(default=None, description="")
        size_bytes: Optional[int] = Field(default=None, description="")
        alias: Optional[str] = Field(default=None, description="")
        is_temporary: Optional[bool] = Field(default=None, description="")
        is_query_preview: Optional[bool] = Field(default=None, description="")
        query_preview_config: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        external_location: Optional[str] = Field(default=None, description="")
        external_location_region: Optional[str] = Field(default=None, description="")
        external_location_format: Optional[str] = Field(default=None, description="")
        is_partitioned: Optional[bool] = Field(default=None, description="")
        partition_strategy: Optional[str] = Field(default=None, description="")
        partition_count: Optional[int] = Field(default=None, description="")
        partition_list: Optional[str] = Field(default=None, description="")
        is_sharded: Optional[bool] = Field(default=None, description="")
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
        dynamo_d_b_status: Optional[DynamoDBStatus] = Field(
            default=None, description=""
        )
        dynamo_d_b_partition_key: Optional[str] = Field(default=None, description="")
        dynamo_d_b_sort_key: Optional[str] = Field(default=None, description="")
        dynamo_d_b_read_capacity_units: Optional[int] = Field(
            default=None, description=""
        )
        dynamo_d_b_write_capacity_units: Optional[int] = Field(
            default=None, description=""
        )
        no_s_q_l_schema_definition: Optional[str] = Field(default=None, description="")
        dynamo_d_b_local_secondary_indexes: Optional[
            List[DynamoDBLocalSecondaryIndex]
        ] = Field(
            default=None, description=""
        )  # relationship
        dynamo_d_b_global_secondary_indexes: Optional[
            List[DynamoDBGlobalSecondaryIndex]
        ] = Field(
            default=None, description=""
        )  # relationship

    attributes: DynamoDBTable.Attributes = Field(
        default_factory=lambda: DynamoDBTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dynamo_d_b_global_secondary_index import DynamoDBGlobalSecondaryIndex  # noqa
from .dynamo_d_b_local_secondary_index import DynamoDBLocalSecondaryIndex  # noqa
