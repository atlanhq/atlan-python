# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType, TableType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .table import Table


class DocumentDBCollection(Table):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str,
        database_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
    ) -> DocumentDBCollection:
        validate_required_fields(
            ["name", "database_qualified_name"], [name, database_qualified_name]
        )
        attributes = DocumentDBCollection.Attributes.creator(
            name=name,
            database_qualified_name=database_qualified_name,
            database_name=database_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="DocumentDBCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DocumentDBCollection":
            raise ValueError("must be DocumentDBCollection")
        return v

    def __setattr__(self, name, value):
        if name in DocumentDBCollection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DOCUMENT_DB_COLLECTION_SUBTYPE: ClassVar[KeywordField] = KeywordField(
        "documentDBCollectionSubtype", "documentDBCollectionSubtype"
    )
    """
    Subtype of a DocumentDBCollection, for example: Capped, Time Series, etc.
    """
    DOCUMENT_DB_COLLECTION_IS_CAPPED: ClassVar[BooleanField] = BooleanField(
        "documentDBCollectionIsCapped", "documentDBCollectionIsCapped"
    )
    """
    Whether the collection is capped (true) or not (false).
    """
    DOCUMENT_DB_COLLECTION_TIME_FIELD: ClassVar[KeywordField] = KeywordField(
        "documentDBCollectionTimeField", "documentDBCollectionTimeField"
    )
    """
    Name of the field containing the date in each time series document.
    """
    DOCUMENT_DB_COLLECTION_TIME_GRANULARITY: ClassVar[KeywordField] = KeywordField(
        "documentDBCollectionTimeGranularity", "documentDBCollectionTimeGranularity"
    )
    """
    Closest match to the time span between consecutive incoming measurements.
    """
    DOCUMENT_DB_COLLECTION_EXPIRE_AFTER_SECONDS: ClassVar[NumericField] = NumericField(
        "documentDBCollectionExpireAfterSeconds",
        "documentDBCollectionExpireAfterSeconds",
    )
    """
    Seconds after which documents in a time series collection or clustered collection expire.
    """
    DOCUMENT_DB_COLLECTION_MAXIMUM_DOCUMENT_COUNT: ClassVar[NumericField] = (
        NumericField(
            "documentDBCollectionMaximumDocumentCount",
            "documentDBCollectionMaximumDocumentCount",
        )
    )
    """
    Maximum number of documents allowed in a capped collection.
    """
    DOCUMENT_DB_COLLECTION_MAX_SIZE: ClassVar[NumericField] = NumericField(
        "documentDBCollectionMaxSize", "documentDBCollectionMaxSize"
    )
    """
    Maximum size allowed in a capped collection.
    """
    DOCUMENT_DB_COLLECTION_NUM_ORPHAN_DOCS: ClassVar[NumericField] = NumericField(
        "documentDBCollectionNumOrphanDocs", "documentDBCollectionNumOrphanDocs"
    )
    """
    Number of orphaned documents in the collection.
    """
    DOCUMENT_DB_COLLECTION_NUM_INDEXES: ClassVar[NumericField] = NumericField(
        "documentDBCollectionNumIndexes", "documentDBCollectionNumIndexes"
    )
    """
    Number of indexes in the collection.
    """
    DOCUMENT_DB_COLLECTION_TOTAL_INDEX_SIZE: ClassVar[NumericField] = NumericField(
        "documentDBCollectionTotalIndexSize", "documentDBCollectionTotalIndexSize"
    )
    """
    Total size of all indexes.
    """
    DOCUMENT_DB_COLLECTION_AVERAGE_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "documentDBCollectionAverageObjectSize", "documentDBCollectionAverageObjectSize"
    )
    """
    Average size of an object in the collection.
    """
    DOCUMENT_DB_COLLECTION_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "documentDBCollectionSchemaDefinition", "documentDBCollectionSchemaDefinition"
    )
    """
    Definition of the schema applicable for the collection.
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
    NO_SQL_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "noSQLSchemaDefinition", "noSQLSchemaDefinition"
    )
    """
    Represents attributes for describing the key schema for the table and indexes.
    """

    DOCUMENT_DB_DATABASE: ClassVar[RelationField] = RelationField("documentDBDatabase")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "document_d_b_collection_subtype",
        "document_d_b_collection_is_capped",
        "document_d_b_collection_time_field",
        "document_d_b_collection_time_granularity",
        "document_d_b_collection_expire_after_seconds",
        "document_d_b_collection_maximum_document_count",
        "document_d_b_collection_max_size",
        "document_d_b_collection_num_orphan_docs",
        "document_d_b_collection_num_indexes",
        "document_d_b_collection_total_index_size",
        "document_d_b_collection_average_object_size",
        "document_d_b_collection_schema_definition",
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
        "no_s_q_l_schema_definition",
        "document_d_b_database",
    ]

    @property
    def document_d_b_collection_subtype(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_subtype
        )

    @document_d_b_collection_subtype.setter
    def document_d_b_collection_subtype(
        self, document_d_b_collection_subtype: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_subtype = (
            document_d_b_collection_subtype
        )

    @property
    def document_d_b_collection_is_capped(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_is_capped
        )

    @document_d_b_collection_is_capped.setter
    def document_d_b_collection_is_capped(
        self, document_d_b_collection_is_capped: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_is_capped = (
            document_d_b_collection_is_capped
        )

    @property
    def document_d_b_collection_time_field(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_time_field
        )

    @document_d_b_collection_time_field.setter
    def document_d_b_collection_time_field(
        self, document_d_b_collection_time_field: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_time_field = (
            document_d_b_collection_time_field
        )

    @property
    def document_d_b_collection_time_granularity(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_time_granularity
        )

    @document_d_b_collection_time_granularity.setter
    def document_d_b_collection_time_granularity(
        self, document_d_b_collection_time_granularity: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_time_granularity = (
            document_d_b_collection_time_granularity
        )

    @property
    def document_d_b_collection_expire_after_seconds(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_expire_after_seconds
        )

    @document_d_b_collection_expire_after_seconds.setter
    def document_d_b_collection_expire_after_seconds(
        self, document_d_b_collection_expire_after_seconds: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_expire_after_seconds = (
            document_d_b_collection_expire_after_seconds
        )

    @property
    def document_d_b_collection_maximum_document_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_maximum_document_count
        )

    @document_d_b_collection_maximum_document_count.setter
    def document_d_b_collection_maximum_document_count(
        self, document_d_b_collection_maximum_document_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_maximum_document_count = (
            document_d_b_collection_maximum_document_count
        )

    @property
    def document_d_b_collection_max_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_max_size
        )

    @document_d_b_collection_max_size.setter
    def document_d_b_collection_max_size(
        self, document_d_b_collection_max_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_max_size = (
            document_d_b_collection_max_size
        )

    @property
    def document_d_b_collection_num_orphan_docs(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_num_orphan_docs
        )

    @document_d_b_collection_num_orphan_docs.setter
    def document_d_b_collection_num_orphan_docs(
        self, document_d_b_collection_num_orphan_docs: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_num_orphan_docs = (
            document_d_b_collection_num_orphan_docs
        )

    @property
    def document_d_b_collection_num_indexes(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_num_indexes
        )

    @document_d_b_collection_num_indexes.setter
    def document_d_b_collection_num_indexes(
        self, document_d_b_collection_num_indexes: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_num_indexes = (
            document_d_b_collection_num_indexes
        )

    @property
    def document_d_b_collection_total_index_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_total_index_size
        )

    @document_d_b_collection_total_index_size.setter
    def document_d_b_collection_total_index_size(
        self, document_d_b_collection_total_index_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_total_index_size = (
            document_d_b_collection_total_index_size
        )

    @property
    def document_d_b_collection_average_object_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_average_object_size
        )

    @document_d_b_collection_average_object_size.setter
    def document_d_b_collection_average_object_size(
        self, document_d_b_collection_average_object_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_average_object_size = (
            document_d_b_collection_average_object_size
        )

    @property
    def document_d_b_collection_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.document_d_b_collection_schema_definition
        )

    @document_d_b_collection_schema_definition.setter
    def document_d_b_collection_schema_definition(
        self, document_d_b_collection_schema_definition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_collection_schema_definition = (
            document_d_b_collection_schema_definition
        )

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
    def document_d_b_database(self) -> Optional[DocumentDBDatabase]:
        return (
            None if self.attributes is None else self.attributes.document_d_b_database
        )

    @document_d_b_database.setter
    def document_d_b_database(
        self, document_d_b_database: Optional[DocumentDBDatabase]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.document_d_b_database = document_d_b_database

    class Attributes(Table.Attributes):
        document_d_b_collection_subtype: Optional[str] = Field(
            default=None, description=""
        )
        document_d_b_collection_is_capped: Optional[bool] = Field(
            default=None, description=""
        )
        document_d_b_collection_time_field: Optional[str] = Field(
            default=None, description=""
        )
        document_d_b_collection_time_granularity: Optional[str] = Field(
            default=None, description=""
        )
        document_d_b_collection_expire_after_seconds: Optional[int] = Field(
            default=None, description=""
        )
        document_d_b_collection_maximum_document_count: Optional[int] = Field(
            default=None, description=""
        )
        document_d_b_collection_max_size: Optional[int] = Field(
            default=None, description=""
        )
        document_d_b_collection_num_orphan_docs: Optional[int] = Field(
            default=None, description=""
        )
        document_d_b_collection_num_indexes: Optional[int] = Field(
            default=None, description=""
        )
        document_d_b_collection_total_index_size: Optional[int] = Field(
            default=None, description=""
        )
        document_d_b_collection_average_object_size: Optional[int] = Field(
            default=None, description=""
        )
        document_d_b_collection_schema_definition: Optional[str] = Field(
            default=None, description=""
        )
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
        no_s_q_l_schema_definition: Optional[str] = Field(default=None, description="")
        document_d_b_database: Optional[DocumentDBDatabase] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            database_qualified_name: str,
            database_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
        ) -> DocumentDBCollection.Attributes:
            validate_required_fields(
                ["name", "database_qualified_name"], [name, database_qualified_name]
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    database_qualified_name, "database_qualified_name", 4
                )

            fields = database_qualified_name.split("/")
            database_name = database_name or fields[3]
            qualified_name = f"{database_qualified_name}/{name}"
            connection_qualified_name = connection_qualified_name or connection_qn

            return DocumentDBCollection.Attributes(
                name=name,
                qualified_name=qualified_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
            )

    attributes: DocumentDBCollection.Attributes = Field(
        default_factory=lambda: DocumentDBCollection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .document_d_b_database import DocumentDBDatabase  # noqa: E402, F401
