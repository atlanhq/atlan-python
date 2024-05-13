# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .cosmos_mongo_d_b import CosmosMongoDB


class CosmosMongoDBCollection(CosmosMongoDB):
    """Description"""

    type_name: str = Field(default="CosmosMongoDBCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CosmosMongoDBCollection":
            raise ValueError("must be CosmosMongoDBCollection")
        return v

    def __setattr__(self, name, value):
        if name in CosmosMongoDBCollection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    NO_SQL_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "noSQLSchemaDefinition", "noSQLSchemaDefinition"
    )
    """
    Represents attributes for describing the key schema for the table and indexes.
    """
    MONGO_DB_COLLECTION_SUBTYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "mongoDBCollectionSubtype",
        "mongoDBCollectionSubtype",
        "mongoDBCollectionSubtype.text",
    )
    """
    Subtype of a MongoDB collection, for example: Capped, Time Series, etc.
    """
    MONGO_DB_COLLECTION_IS_CAPPED: ClassVar[BooleanField] = BooleanField(
        "mongoDBCollectionIsCapped", "mongoDBCollectionIsCapped"
    )
    """
    Whether the collection is capped (true) or not (false).
    """
    MONGO_DB_COLLECTION_TIME_FIELD: ClassVar[KeywordField] = KeywordField(
        "mongoDBCollectionTimeField", "mongoDBCollectionTimeField"
    )
    """
    Name of the field containing the date in each time series document.
    """
    MONGO_DB_COLLECTION_TIME_GRANULARITY: ClassVar[KeywordField] = KeywordField(
        "mongoDBCollectionTimeGranularity", "mongoDBCollectionTimeGranularity"
    )
    """
    Closest match to the time span between consecutive incoming measurements.
    """
    MONGO_DB_COLLECTION_EXPIRE_AFTER_SECONDS: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionExpireAfterSeconds", "mongoDBCollectionExpireAfterSeconds"
    )
    """
    Seconds after which documents in a time series collection or clustered collection expire.
    """
    MONGO_DB_COLLECTION_MAXIMUM_DOCUMENT_COUNT: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionMaximumDocumentCount", "mongoDBCollectionMaximumDocumentCount"
    )
    """
    Maximum number of documents allowed in a capped collection.
    """
    MONGO_DB_COLLECTION_MAX_SIZE: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionMaxSize", "mongoDBCollectionMaxSize"
    )
    """
    Maximum size allowed in a capped collection.
    """
    MONGO_DB_COLLECTION_NUM_ORPHAN_DOCS: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionNumOrphanDocs", "mongoDBCollectionNumOrphanDocs"
    )
    """
    Number of orphaned documents in the collection.
    """
    MONGO_DB_COLLECTION_NUM_INDEXES: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionNumIndexes", "mongoDBCollectionNumIndexes"
    )
    """
    Number of indexes on the collection.
    """
    MONGO_DB_COLLECTION_TOTAL_INDEX_SIZE: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionTotalIndexSize", "mongoDBCollectionTotalIndexSize"
    )
    """
    Total size of all indexes.
    """
    MONGO_DB_COLLECTION_AVERAGE_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionAverageObjectSize", "mongoDBCollectionAverageObjectSize"
    )
    """
    Average size of an object in the collection.
    """
    MONGO_DB_COLLECTION_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "mongoDBCollectionSchemaDefinition", "mongoDBCollectionSchemaDefinition"
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

    DBT_SOURCES: ClassVar[RelationField] = RelationField("dbtSources")
    """
    TBC
    """
    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    FACTS: ClassVar[RelationField] = RelationField("facts")
    """
    TBC
    """
    SQL_DBT_MODELS: ClassVar[RelationField] = RelationField("sqlDbtModels")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """
    PARTITIONS: ClassVar[RelationField] = RelationField("partitions")
    """
    TBC
    """
    COSMOS_MONGO_DB_DATABASE: ClassVar[RelationField] = RelationField(
        "cosmosMongoDBDatabase"
    )
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    SQL_DBT_SOURCES: ClassVar[RelationField] = RelationField("sqlDBTSources")
    """
    TBC
    """
    DBT_MODELS: ClassVar[RelationField] = RelationField("dbtModels")
    """
    TBC
    """
    MONGO_DB_DATABASE: ClassVar[RelationField] = RelationField("mongoDBDatabase")
    """
    TBC
    """
    DIMENSIONS: ClassVar[RelationField] = RelationField("dimensions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "no_s_q_l_schema_definition",
        "mongo_d_b_collection_subtype",
        "mongo_d_b_collection_is_capped",
        "mongo_d_b_collection_time_field",
        "mongo_d_b_collection_time_granularity",
        "mongo_d_b_collection_expire_after_seconds",
        "mongo_d_b_collection_maximum_document_count",
        "mongo_d_b_collection_max_size",
        "mongo_d_b_collection_num_orphan_docs",
        "mongo_d_b_collection_num_indexes",
        "mongo_d_b_collection_total_index_size",
        "mongo_d_b_collection_average_object_size",
        "mongo_d_b_collection_schema_definition",
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
        "dbt_sources",
        "columns",
        "facts",
        "sql_dbt_models",
        "dbt_tests",
        "atlan_schema",
        "partitions",
        "cosmos_mongo_d_b_database",
        "queries",
        "sql_dbt_sources",
        "dbt_models",
        "mongo_d_b_database",
        "dimensions",
    ]

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
    def mongo_d_b_collection_subtype(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_subtype
        )

    @mongo_d_b_collection_subtype.setter
    def mongo_d_b_collection_subtype(self, mongo_d_b_collection_subtype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_subtype = mongo_d_b_collection_subtype

    @property
    def mongo_d_b_collection_is_capped(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_is_capped
        )

    @mongo_d_b_collection_is_capped.setter
    def mongo_d_b_collection_is_capped(
        self, mongo_d_b_collection_is_capped: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_is_capped = mongo_d_b_collection_is_capped

    @property
    def mongo_d_b_collection_time_field(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_time_field
        )

    @mongo_d_b_collection_time_field.setter
    def mongo_d_b_collection_time_field(
        self, mongo_d_b_collection_time_field: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_time_field = (
            mongo_d_b_collection_time_field
        )

    @property
    def mongo_d_b_collection_time_granularity(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_time_granularity
        )

    @mongo_d_b_collection_time_granularity.setter
    def mongo_d_b_collection_time_granularity(
        self, mongo_d_b_collection_time_granularity: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_time_granularity = (
            mongo_d_b_collection_time_granularity
        )

    @property
    def mongo_d_b_collection_expire_after_seconds(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_expire_after_seconds
        )

    @mongo_d_b_collection_expire_after_seconds.setter
    def mongo_d_b_collection_expire_after_seconds(
        self, mongo_d_b_collection_expire_after_seconds: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_expire_after_seconds = (
            mongo_d_b_collection_expire_after_seconds
        )

    @property
    def mongo_d_b_collection_maximum_document_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_maximum_document_count
        )

    @mongo_d_b_collection_maximum_document_count.setter
    def mongo_d_b_collection_maximum_document_count(
        self, mongo_d_b_collection_maximum_document_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_maximum_document_count = (
            mongo_d_b_collection_maximum_document_count
        )

    @property
    def mongo_d_b_collection_max_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_max_size
        )

    @mongo_d_b_collection_max_size.setter
    def mongo_d_b_collection_max_size(
        self, mongo_d_b_collection_max_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_max_size = mongo_d_b_collection_max_size

    @property
    def mongo_d_b_collection_num_orphan_docs(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_num_orphan_docs
        )

    @mongo_d_b_collection_num_orphan_docs.setter
    def mongo_d_b_collection_num_orphan_docs(
        self, mongo_d_b_collection_num_orphan_docs: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_num_orphan_docs = (
            mongo_d_b_collection_num_orphan_docs
        )

    @property
    def mongo_d_b_collection_num_indexes(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_num_indexes
        )

    @mongo_d_b_collection_num_indexes.setter
    def mongo_d_b_collection_num_indexes(
        self, mongo_d_b_collection_num_indexes: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_num_indexes = (
            mongo_d_b_collection_num_indexes
        )

    @property
    def mongo_d_b_collection_total_index_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_total_index_size
        )

    @mongo_d_b_collection_total_index_size.setter
    def mongo_d_b_collection_total_index_size(
        self, mongo_d_b_collection_total_index_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_total_index_size = (
            mongo_d_b_collection_total_index_size
        )

    @property
    def mongo_d_b_collection_average_object_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_average_object_size
        )

    @mongo_d_b_collection_average_object_size.setter
    def mongo_d_b_collection_average_object_size(
        self, mongo_d_b_collection_average_object_size: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_average_object_size = (
            mongo_d_b_collection_average_object_size
        )

    @property
    def mongo_d_b_collection_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_collection_schema_definition
        )

    @mongo_d_b_collection_schema_definition.setter
    def mongo_d_b_collection_schema_definition(
        self, mongo_d_b_collection_schema_definition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collection_schema_definition = (
            mongo_d_b_collection_schema_definition
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
    def dbt_sources(self) -> Optional[List[DbtSource]]:
        return None if self.attributes is None else self.attributes.dbt_sources

    @dbt_sources.setter
    def dbt_sources(self, dbt_sources: Optional[List[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_sources = dbt_sources

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
    def sql_dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.sql_dbt_models

    @sql_dbt_models.setter
    def sql_dbt_models(self, sql_dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_models = sql_dbt_models

    @property
    def dbt_tests(self) -> Optional[List[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[List[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    @property
    def partitions(self) -> Optional[List[TablePartition]]:
        return None if self.attributes is None else self.attributes.partitions

    @partitions.setter
    def partitions(self, partitions: Optional[List[TablePartition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partitions = partitions

    @property
    def cosmos_mongo_d_b_database(self) -> Optional[CosmosMongoDBDatabase]:
        return (
            None
            if self.attributes is None
            else self.attributes.cosmos_mongo_d_b_database
        )

    @cosmos_mongo_d_b_database.setter
    def cosmos_mongo_d_b_database(
        self, cosmos_mongo_d_b_database: Optional[CosmosMongoDBDatabase]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cosmos_mongo_d_b_database = cosmos_mongo_d_b_database

    @property
    def queries(self) -> Optional[List[Query]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[List[Query]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def sql_dbt_sources(self) -> Optional[List[DbtSource]]:
        return None if self.attributes is None else self.attributes.sql_dbt_sources

    @sql_dbt_sources.setter
    def sql_dbt_sources(self, sql_dbt_sources: Optional[List[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_sources = sql_dbt_sources

    @property
    def dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.dbt_models

    @dbt_models.setter
    def dbt_models(self, dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_models = dbt_models

    @property
    def mongo_d_b_database(self) -> Optional[MongoDBDatabase]:
        return None if self.attributes is None else self.attributes.mongo_d_b_database

    @mongo_d_b_database.setter
    def mongo_d_b_database(self, mongo_d_b_database: Optional[MongoDBDatabase]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_database = mongo_d_b_database

    @property
    def dimensions(self) -> Optional[List[Table]]:
        return None if self.attributes is None else self.attributes.dimensions

    @dimensions.setter
    def dimensions(self, dimensions: Optional[List[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dimensions = dimensions

    class Attributes(CosmosMongoDB.Attributes):
        no_s_q_l_schema_definition: Optional[str] = Field(default=None, description="")
        mongo_d_b_collection_subtype: Optional[str] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_is_capped: Optional[bool] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_time_field: Optional[str] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_time_granularity: Optional[str] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_expire_after_seconds: Optional[int] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_maximum_document_count: Optional[int] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_max_size: Optional[int] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_num_orphan_docs: Optional[int] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_num_indexes: Optional[int] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_total_index_size: Optional[int] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_average_object_size: Optional[int] = Field(
            default=None, description=""
        )
        mongo_d_b_collection_schema_definition: Optional[str] = Field(
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
        dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        facts: Optional[List[Table]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[List[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        partitions: Optional[List[TablePartition]] = Field(
            default=None, description=""
        )  # relationship
        cosmos_mongo_d_b_database: Optional[CosmosMongoDBDatabase] = Field(
            default=None, description=""
        )  # relationship
        queries: Optional[List[Query]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        mongo_d_b_database: Optional[MongoDBDatabase] = Field(
            default=None, description=""
        )  # relationship
        dimensions: Optional[List[Table]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CosmosMongoDBCollection.Attributes = Field(
        default_factory=lambda: CosmosMongoDBCollection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .column import Column  # noqa
from .cosmos_mongo_d_b_database import CosmosMongoDBDatabase  # noqa
from .dbt_model import DbtModel  # noqa
from .dbt_source import DbtSource  # noqa
from .dbt_test import DbtTest  # noqa
from .mongo_d_b_database import MongoDBDatabase  # noqa
from .query import Query  # noqa
from .schema import Schema  # noqa
from .table import Table  # noqa
from .table_partition import TablePartition  # noqa
