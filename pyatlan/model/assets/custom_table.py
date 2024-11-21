# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import TableType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import CustomRatings

from .core.table import Table


class CustomTable(Table):
    """Description"""

    type_name: str = Field(default="CustomTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CustomTable":
            raise ValueError("must be CustomTable")
        return v

    def __setattr__(self, name, value):
        if name in CustomTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUSTOM_RATINGS: ClassVar[KeywordField] = KeywordField(
        "customRatings", "customRatings"
    )
    """
    Ratings for the CustomTable asset from the source system.
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
    EXTERNAL_LOCATION: ClassVar[TextField] = TextField(
        "externalLocation", "externalLocation"
    )
    """
    External location of this table, for example: an S3 object location.
    """
    EXTERNAL_LOCATION_REGION: ClassVar[TextField] = TextField(
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
    PARTITION_LIST: ClassVar[TextField] = TextField("partitionList", "partitionList")
    """
    List of partitions in this table.
    """
    IS_SHARDED: ClassVar[BooleanField] = BooleanField("isSharded", "isSharded")
    """
    Whether this table is a sharded table (true) or not (false).
    """
    TABLE_TYPE: ClassVar[KeywordField] = KeywordField("tableType", "tableType")
    """
    Type of the table.
    """
    ICEBERG_CATALOG_NAME: ClassVar[KeywordField] = KeywordField(
        "icebergCatalogName", "icebergCatalogName"
    )
    """
    iceberg table catalog name (can be any user defined name)
    """
    ICEBERG_TABLE_TYPE: ClassVar[KeywordField] = KeywordField(
        "icebergTableType", "icebergTableType"
    )
    """
    iceberg table type (managed vs unmanaged)
    """
    ICEBERG_CATALOG_SOURCE: ClassVar[KeywordField] = KeywordField(
        "icebergCatalogSource", "icebergCatalogSource"
    )
    """
    iceberg table catalog type (glue, polaris, snowflake)
    """
    ICEBERG_CATALOG_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "icebergCatalogTableName", "icebergCatalogTableName"
    )
    """
    catalog table name (actual table name on the catalog side).
    """
    ICEBERG_CATALOG_TABLE_NAMESPACE: ClassVar[KeywordField] = KeywordField(
        "icebergCatalogTableNamespace", "icebergCatalogTableNamespace"
    )
    """
    catalog table namespace (actual database name on the catalog side).
    """
    TABLE_EXTERNAL_VOLUME_NAME: ClassVar[KeywordField] = KeywordField(
        "tableExternalVolumeName", "tableExternalVolumeName"
    )
    """
    external volume name for the table.
    """
    ICEBERG_TABLE_BASE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "icebergTableBaseLocation", "icebergTableBaseLocation"
    )
    """
    iceberg table base location inside the external volume.
    """
    TABLE_RETENTION_TIME: ClassVar[NumericField] = NumericField(
        "tableRetentionTime", "tableRetentionTime"
    )
    """
    Data retention time in days.
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

    CUSTOM_FIELDS: ClassVar[RelationField] = RelationField("customFields")
    """
    TBC
    """
    CUSTOM_DATASET: ClassVar[RelationField] = RelationField("customDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "custom_ratings",
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
        "table_type",
        "iceberg_catalog_name",
        "iceberg_table_type",
        "iceberg_catalog_source",
        "iceberg_catalog_table_name",
        "iceberg_catalog_table_namespace",
        "table_external_volume_name",
        "iceberg_table_base_location",
        "table_retention_time",
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
        "custom_fields",
        "custom_dataset",
    ]

    @property
    def custom_ratings(self) -> Optional[List[CustomRatings]]:
        return None if self.attributes is None else self.attributes.custom_ratings

    @custom_ratings.setter
    def custom_ratings(self, custom_ratings: Optional[List[CustomRatings]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_ratings = custom_ratings

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
    def table_type(self) -> Optional[TableType]:
        return None if self.attributes is None else self.attributes.table_type

    @table_type.setter
    def table_type(self, table_type: Optional[TableType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_type = table_type

    @property
    def iceberg_catalog_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.iceberg_catalog_name

    @iceberg_catalog_name.setter
    def iceberg_catalog_name(self, iceberg_catalog_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_catalog_name = iceberg_catalog_name

    @property
    def iceberg_table_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.iceberg_table_type

    @iceberg_table_type.setter
    def iceberg_table_type(self, iceberg_table_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_table_type = iceberg_table_type

    @property
    def iceberg_catalog_source(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.iceberg_catalog_source
        )

    @iceberg_catalog_source.setter
    def iceberg_catalog_source(self, iceberg_catalog_source: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_catalog_source = iceberg_catalog_source

    @property
    def iceberg_catalog_table_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_catalog_table_name
        )

    @iceberg_catalog_table_name.setter
    def iceberg_catalog_table_name(self, iceberg_catalog_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_catalog_table_name = iceberg_catalog_table_name

    @property
    def iceberg_catalog_table_namespace(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_catalog_table_namespace
        )

    @iceberg_catalog_table_namespace.setter
    def iceberg_catalog_table_namespace(
        self, iceberg_catalog_table_namespace: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_catalog_table_namespace = (
            iceberg_catalog_table_namespace
        )

    @property
    def table_external_volume_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.table_external_volume_name
        )

    @table_external_volume_name.setter
    def table_external_volume_name(self, table_external_volume_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_external_volume_name = table_external_volume_name

    @property
    def iceberg_table_base_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_table_base_location
        )

    @iceberg_table_base_location.setter
    def iceberg_table_base_location(self, iceberg_table_base_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_table_base_location = iceberg_table_base_location

    @property
    def table_retention_time(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.table_retention_time

    @table_retention_time.setter
    def table_retention_time(self, table_retention_time: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_retention_time = table_retention_time

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
    def custom_fields(self) -> Optional[List[CustomField]]:
        return None if self.attributes is None else self.attributes.custom_fields

    @custom_fields.setter
    def custom_fields(self, custom_fields: Optional[List[CustomField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_fields = custom_fields

    @property
    def custom_dataset(self) -> Optional[CustomDataset]:
        return None if self.attributes is None else self.attributes.custom_dataset

    @custom_dataset.setter
    def custom_dataset(self, custom_dataset: Optional[CustomDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_dataset = custom_dataset

    class Attributes(Table.Attributes):
        custom_ratings: Optional[List[CustomRatings]] = Field(
            default=None, description=""
        )
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
        table_type: Optional[TableType] = Field(default=None, description="")
        iceberg_catalog_name: Optional[str] = Field(default=None, description="")
        iceberg_table_type: Optional[str] = Field(default=None, description="")
        iceberg_catalog_source: Optional[str] = Field(default=None, description="")
        iceberg_catalog_table_name: Optional[str] = Field(default=None, description="")
        iceberg_catalog_table_namespace: Optional[str] = Field(
            default=None, description=""
        )
        table_external_volume_name: Optional[str] = Field(default=None, description="")
        iceberg_table_base_location: Optional[str] = Field(default=None, description="")
        table_retention_time: Optional[int] = Field(default=None, description="")
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
        custom_fields: Optional[List[CustomField]] = Field(
            default=None, description=""
        )  # relationship
        custom_dataset: Optional[CustomDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: CustomTable.Attributes = Field(
        default_factory=lambda: CustomTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .custom_dataset import CustomDataset  # noqa
from .custom_field import CustomField  # noqa

CustomTable.Attributes.update_forward_refs()
