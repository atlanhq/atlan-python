# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set

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

from .dremio import Dremio


class DremioPhysicalDataset(Dremio):
    """Description"""

    type_name: str = Field(default="DremioPhysicalDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DremioPhysicalDataset":
            raise ValueError("must be DremioPhysicalDataset")
        return v

    def __setattr__(self, name, value):
        if name in DremioPhysicalDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DREMIO_ID: ClassVar[KeywordField] = KeywordField("dremioId", "dremioId")
    """
    Source ID of this asset in Dremio.
    """
    DREMIO_SPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSpaceQualifiedName", "dremioSpaceQualifiedName"
    )
    """
    Unique qualified name of the Dremio Space containing this asset.
    """
    DREMIO_SPACE_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSpaceName", "dremioSpaceName"
    )
    """
    Simple name of the Dremio Space containing this asset.
    """
    DREMIO_SOURCE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSourceQualifiedName", "dremioSourceQualifiedName"
    )
    """
    Unique qualified name of the Dremio Source containing this asset.
    """
    DREMIO_SOURCE_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSourceName", "dremioSourceName"
    )
    """
    Simple name of the Dremio Source containing this asset.
    """
    DREMIO_PARENT_FOLDER_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioParentFolderQualifiedName", "dremioParentFolderQualifiedName"
    )
    """
    Unique qualified name of the immediate parent folder containing this asset.
    """
    DREMIO_FOLDER_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "dremioFolderHierarchy", "dremioFolderHierarchy"
    )
    """
    Ordered array of folder assets with qualified name and name representing the complete folder hierarchy path for this asset, from immediate parent to root folder.
    """  # noqa: E501
    DREMIO_LABELS: ClassVar[KeywordField] = KeywordField("dremioLabels", "dremioLabels")
    """
    Dremio Labels associated with this asset.
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
    SQL_AI_MODEL_CONTEXT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sqlAIModelContextQualifiedName", "sqlAIModelContextQualifiedName"
    )
    """
    Unique name of the context in which the model versions exist, or empty if it does not exist within an AI model context.
    """  # noqa: E501
    SQL_IS_SECURE: ClassVar[BooleanField] = BooleanField("sqlIsSecure", "sqlIsSecure")
    """
    Whether this asset is secure (true) or not (false).
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
    TABLE_OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "tableObjectCount", "tableObjectCount"
    )
    """
    Number of objects in this table.
    """
    ALIAS: ClassVar[TextField] = TextField("alias", "alias")
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
    TABLE_DEFINITION: ClassVar[TextField] = TextField(
        "tableDefinition", "tableDefinition"
    )
    """
    Definition of the table.
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
    Iceberg table catalog name (can be any user defined name)
    """
    ICEBERG_TABLE_TYPE: ClassVar[KeywordField] = KeywordField(
        "icebergTableType", "icebergTableType"
    )
    """
    Iceberg table type (managed vs unmanaged)
    """
    ICEBERG_CATALOG_SOURCE: ClassVar[KeywordField] = KeywordField(
        "icebergCatalogSource", "icebergCatalogSource"
    )
    """
    Iceberg table catalog type (glue, polaris, snowflake)
    """
    ICEBERG_CATALOG_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "icebergCatalogTableName", "icebergCatalogTableName"
    )
    """
    Catalog table name (actual table name on the catalog side).
    """
    TABLE_IMPALA_PARAMETERS: ClassVar[KeywordField] = KeywordField(
        "tableImpalaParameters", "tableImpalaParameters"
    )
    """
    Extra attributes for Impala
    """
    ICEBERG_CATALOG_TABLE_NAMESPACE: ClassVar[KeywordField] = KeywordField(
        "icebergCatalogTableNamespace", "icebergCatalogTableNamespace"
    )
    """
    Catalog table namespace (actual database name on the catalog side).
    """
    TABLE_EXTERNAL_VOLUME_NAME: ClassVar[KeywordField] = KeywordField(
        "tableExternalVolumeName", "tableExternalVolumeName"
    )
    """
    External volume name for the table.
    """
    ICEBERG_TABLE_BASE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "icebergTableBaseLocation", "icebergTableBaseLocation"
    )
    """
    Iceberg table base location inside the external volume.
    """
    TABLE_RETENTION_TIME: ClassVar[NumericField] = NumericField(
        "tableRetentionTime", "tableRetentionTime"
    )
    """
    Data retention time in days.
    """

    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    FACTS: ClassVar[RelationField] = RelationField("facts")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """
    DREMIO_FOLDER: ClassVar[RelationField] = RelationField("dremioFolder")
    """
    TBC
    """
    PARTITIONS: ClassVar[RelationField] = RelationField("partitions")
    """
    TBC
    """
    DREMIO_SOURCE: ClassVar[RelationField] = RelationField("dremioSource")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    DIMENSIONS: ClassVar[RelationField] = RelationField("dimensions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dremio_id",
        "dremio_space_qualified_name",
        "dremio_space_name",
        "dremio_source_qualified_name",
        "dremio_source_name",
        "dremio_parent_folder_qualified_name",
        "dremio_folder_hierarchy",
        "dremio_labels",
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
        "sql_a_i_model_context_qualified_name",
        "sql_is_secure",
        "column_count",
        "row_count",
        "size_bytes",
        "table_object_count",
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
        "table_definition",
        "partition_list",
        "is_sharded",
        "table_type",
        "iceberg_catalog_name",
        "iceberg_table_type",
        "iceberg_catalog_source",
        "iceberg_catalog_table_name",
        "table_impala_parameters",
        "iceberg_catalog_table_namespace",
        "table_external_volume_name",
        "iceberg_table_base_location",
        "table_retention_time",
        "columns",
        "facts",
        "atlan_schema",
        "dremio_folder",
        "partitions",
        "dremio_source",
        "queries",
        "dimensions",
    ]

    @property
    def dremio_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dremio_id

    @dremio_id.setter
    def dremio_id(self, dremio_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_id = dremio_id

    @property
    def dremio_space_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_space_qualified_name
        )

    @dremio_space_qualified_name.setter
    def dremio_space_qualified_name(self, dremio_space_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_space_qualified_name = dremio_space_qualified_name

    @property
    def dremio_space_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dremio_space_name

    @dremio_space_name.setter
    def dremio_space_name(self, dremio_space_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_space_name = dremio_space_name

    @property
    def dremio_source_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_source_qualified_name
        )

    @dremio_source_qualified_name.setter
    def dremio_source_qualified_name(self, dremio_source_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_qualified_name = dremio_source_qualified_name

    @property
    def dremio_source_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dremio_source_name

    @dremio_source_name.setter
    def dremio_source_name(self, dremio_source_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_name = dremio_source_name

    @property
    def dremio_parent_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_parent_folder_qualified_name
        )

    @dremio_parent_folder_qualified_name.setter
    def dremio_parent_folder_qualified_name(
        self, dremio_parent_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_parent_folder_qualified_name = (
            dremio_parent_folder_qualified_name
        )

    @property
    def dremio_folder_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.dremio_folder_hierarchy
        )

    @dremio_folder_hierarchy.setter
    def dremio_folder_hierarchy(
        self, dremio_folder_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_folder_hierarchy = dremio_folder_hierarchy

    @property
    def dremio_labels(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.dremio_labels

    @dremio_labels.setter
    def dremio_labels(self, dremio_labels: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_labels = dremio_labels

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
    def sql_a_i_model_context_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_a_i_model_context_qualified_name
        )

    @sql_a_i_model_context_qualified_name.setter
    def sql_a_i_model_context_qualified_name(
        self, sql_a_i_model_context_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_a_i_model_context_qualified_name = (
            sql_a_i_model_context_qualified_name
        )

    @property
    def sql_is_secure(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.sql_is_secure

    @sql_is_secure.setter
    def sql_is_secure(self, sql_is_secure: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_is_secure = sql_is_secure

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
    def table_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.table_object_count

    @table_object_count.setter
    def table_object_count(self, table_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_object_count = table_object_count

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
    def table_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_definition

    @table_definition.setter
    def table_definition(self, table_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_definition = table_definition

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
    def table_impala_parameters(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.table_impala_parameters
        )

    @table_impala_parameters.setter
    def table_impala_parameters(
        self, table_impala_parameters: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_impala_parameters = table_impala_parameters

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
    def columns(self) -> Optional[List[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[List[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def facts(self) -> Optional[List[Table]]:
        return None if self.attributes is None else self.attributes.facts

    @facts.setter
    def facts(self, facts: Optional[List[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.facts = facts

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    @property
    def dremio_folder(self) -> Optional[DremioFolder]:
        return None if self.attributes is None else self.attributes.dremio_folder

    @dremio_folder.setter
    def dremio_folder(self, dremio_folder: Optional[DremioFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_folder = dremio_folder

    @property
    def partitions(self) -> Optional[List[TablePartition]]:
        return None if self.attributes is None else self.attributes.partitions

    @partitions.setter
    def partitions(self, partitions: Optional[List[TablePartition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partitions = partitions

    @property
    def dremio_source(self) -> Optional[DremioSource]:
        return None if self.attributes is None else self.attributes.dremio_source

    @dremio_source.setter
    def dremio_source(self, dremio_source: Optional[DremioSource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source = dremio_source

    @property
    def queries(self) -> Optional[List[Query]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[List[Query]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def dimensions(self) -> Optional[List[Table]]:
        return None if self.attributes is None else self.attributes.dimensions

    @dimensions.setter
    def dimensions(self, dimensions: Optional[List[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dimensions = dimensions

    class Attributes(Dremio.Attributes):
        dremio_id: Optional[str] = Field(default=None, description="")
        dremio_space_qualified_name: Optional[str] = Field(default=None, description="")
        dremio_space_name: Optional[str] = Field(default=None, description="")
        dremio_source_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dremio_source_name: Optional[str] = Field(default=None, description="")
        dremio_parent_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dremio_folder_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        dremio_labels: Optional[Set[str]] = Field(default=None, description="")
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
        sql_a_i_model_context_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_is_secure: Optional[bool] = Field(default=None, description="")
        column_count: Optional[int] = Field(default=None, description="")
        row_count: Optional[int] = Field(default=None, description="")
        size_bytes: Optional[int] = Field(default=None, description="")
        table_object_count: Optional[int] = Field(default=None, description="")
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
        table_definition: Optional[str] = Field(default=None, description="")
        partition_list: Optional[str] = Field(default=None, description="")
        is_sharded: Optional[bool] = Field(default=None, description="")
        table_type: Optional[TableType] = Field(default=None, description="")
        iceberg_catalog_name: Optional[str] = Field(default=None, description="")
        iceberg_table_type: Optional[str] = Field(default=None, description="")
        iceberg_catalog_source: Optional[str] = Field(default=None, description="")
        iceberg_catalog_table_name: Optional[str] = Field(default=None, description="")
        table_impala_parameters: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        iceberg_catalog_table_namespace: Optional[str] = Field(
            default=None, description=""
        )
        table_external_volume_name: Optional[str] = Field(default=None, description="")
        iceberg_table_base_location: Optional[str] = Field(default=None, description="")
        table_retention_time: Optional[int] = Field(default=None, description="")
        columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        facts: Optional[List[Table]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        dremio_folder: Optional[DremioFolder] = Field(
            default=None, description=""
        )  # relationship
        partitions: Optional[List[TablePartition]] = Field(
            default=None, description=""
        )  # relationship
        dremio_source: Optional[DremioSource] = Field(
            default=None, description=""
        )  # relationship
        queries: Optional[List[Query]] = Field(
            default=None, description=""
        )  # relationship
        dimensions: Optional[List[Table]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DremioPhysicalDataset.Attributes = Field(
        default_factory=lambda: DremioPhysicalDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.column import Column  # noqa: E402, F401
from .core.query import Query  # noqa: E402, F401
from .core.schema import Schema  # noqa: E402, F401
from .core.table import Table  # noqa: E402, F401
from .core.table_partition import TablePartition  # noqa: E402, F401
from .dremio_folder import DremioFolder  # noqa: E402, F401
from .dremio_source import DremioSource  # noqa: E402, F401

DremioPhysicalDataset.Attributes.update_forward_refs()
