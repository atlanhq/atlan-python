# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .asset00 import Database, Table


class MongoDBCollection(Table):
    """Description"""

    type_name: str = Field("MongoDBCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MongoDBCollection":
            raise ValueError("must be MongoDBCollection")
        return v

    def __setattr__(self, name, value):
        if name in MongoDBCollection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MONGO_DB_COLLECTION_SUBTYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "mongoDBCollectionSubtype",
        "mongoDBCollectionSubtype",
        "mongoDBCollectionSubtype.text",
    )
    """
    Subtype of a MongoDB collection (e.g. Capped, Time Series etc.)
    """
    MONGO_DB_COLLECTION_IS_CAPPED: ClassVar[BooleanField] = BooleanField(
        "mongoDBCollectionIsCapped", "mongoDBCollectionIsCapped"
    )
    """
    If the collection is a capped collection
    """
    MONGO_DB_COLLECTION_TIME_FIELD: ClassVar[KeywordField] = KeywordField(
        "mongoDBCollectionTimeField", "mongoDBCollectionTimeField"
    )
    """
    The name of the field which contains the date in each time series document
    """
    MONGO_DB_COLLECTION_TIME_GRANULARITY: ClassVar[KeywordField] = KeywordField(
        "mongoDBCollectionTimeGranularity", "mongoDBCollectionTimeGranularity"
    )
    """
    Set the granularity to the value that is the closest match to the time span between consecutive incoming measurements
    """  # noqa: E501
    MONGO_DB_COLLECTION_EXPIRE_AFTER_SECONDS: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionExpireAfterSeconds", "mongoDBCollectionExpireAfterSeconds"
    )
    """
    Specifies the seconds after which documents in a time series collection or clustered collection expire
    """
    MONGO_DB_COLLECTION_MAXIMUM_DOCUMENT_COUNT: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionMaximumDocumentCount", "mongoDBCollectionMaximumDocumentCount"
    )
    """
    The maximum number of documents allowed in the capped collection
    """
    MONGO_DB_COLLECTION_MAX_SIZE: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionMaxSize", "mongoDBCollectionMaxSize"
    )
    """
    The maximum size allowed in the capped collection
    """
    MONGO_DB_COLLECTION_NUM_ORPHAN_DOCS: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionNumOrphanDocs", "mongoDBCollectionNumOrphanDocs"
    )
    """
    The number of orphaned documents in the collection
    """
    MONGO_DB_COLLECTION_NUM_INDEXES: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionNumIndexes", "mongoDBCollectionNumIndexes"
    )
    """
    The number of indexes on the collection
    """
    MONGO_DB_COLLECTION_TOTAL_INDEX_SIZE: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionTotalIndexSize", "mongoDBCollectionTotalIndexSize"
    )
    """
    The total size of all indexes
    """
    MONGO_DB_COLLECTION_AVERAGE_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "mongoDBCollectionAverageObjectSize", "mongoDBCollectionAverageObjectSize"
    )
    """
    The average size of an object in the collection
    """
    MONGO_DB_COLLECTION_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "mongoDBCollectionSchemaDefinition", "mongoDBCollectionSchemaDefinition"
    )
    """
    Definition of the schema applicable for the collection.
    """
    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    TBC
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    TBC
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    TBC
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    TBC
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    TBC
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    TBC
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "externalLocation", "externalLocation"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION_REGION: ClassVar[KeywordField] = KeywordField(
        "externalLocationRegion", "externalLocationRegion"
    )
    """
    TBC
    """
    EXTERNAL_LOCATION_FORMAT: ClassVar[KeywordField] = KeywordField(
        "externalLocationFormat", "externalLocationFormat"
    )
    """
    TBC
    """
    IS_PARTITIONED: ClassVar[BooleanField] = BooleanField(
        "isPartitioned", "isPartitioned"
    )
    """
    TBC
    """
    PARTITION_STRATEGY: ClassVar[KeywordField] = KeywordField(
        "partitionStrategy", "partitionStrategy"
    )
    """
    TBC
    """
    PARTITION_COUNT: ClassVar[NumericField] = NumericField(
        "partitionCount", "partitionCount"
    )
    """
    TBC
    """
    PARTITION_LIST: ClassVar[KeywordField] = KeywordField(
        "partitionList", "partitionList"
    )
    """
    TBC
    """
    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    TBC
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    TBC
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    TBC
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    TBC
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    TBC
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    TBC
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    TBC
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    TBC
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    TBC
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    TBC
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    TBC
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    TBC
    """
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    TBC
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    TBC
    """

    MONGO_DB_DATABASE: ClassVar[RelationField] = RelationField("mongoDBDatabase")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
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
        "is_profiled",
        "last_profiled_at",
        "mongo_d_b_database",
    ]

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
    def query_preview_config(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.query_preview_config

    @query_preview_config.setter
    def query_preview_config(self, query_preview_config: Optional[dict[str, str]]):
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
    def query_user_map(self) -> Optional[dict[str, int]]:
        return None if self.attributes is None else self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[dict[str, int]]):
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
    def mongo_d_b_database(self) -> Optional[MongoDBDatabase]:
        return None if self.attributes is None else self.attributes.mongo_d_b_database

    @mongo_d_b_database.setter
    def mongo_d_b_database(self, mongo_d_b_database: Optional[MongoDBDatabase]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_database = mongo_d_b_database

    class Attributes(Table.Attributes):
        mongo_d_b_collection_subtype: Optional[str] = Field(
            None, description="", alias="mongoDBCollectionSubtype"
        )
        mongo_d_b_collection_is_capped: Optional[bool] = Field(
            None, description="", alias="mongoDBCollectionIsCapped"
        )
        mongo_d_b_collection_time_field: Optional[str] = Field(
            None, description="", alias="mongoDBCollectionTimeField"
        )
        mongo_d_b_collection_time_granularity: Optional[str] = Field(
            None, description="", alias="mongoDBCollectionTimeGranularity"
        )
        mongo_d_b_collection_expire_after_seconds: Optional[int] = Field(
            None, description="", alias="mongoDBCollectionExpireAfterSeconds"
        )
        mongo_d_b_collection_maximum_document_count: Optional[int] = Field(
            None, description="", alias="mongoDBCollectionMaximumDocumentCount"
        )
        mongo_d_b_collection_max_size: Optional[int] = Field(
            None, description="", alias="mongoDBCollectionMaxSize"
        )
        mongo_d_b_collection_num_orphan_docs: Optional[int] = Field(
            None, description="", alias="mongoDBCollectionNumOrphanDocs"
        )
        mongo_d_b_collection_num_indexes: Optional[int] = Field(
            None, description="", alias="mongoDBCollectionNumIndexes"
        )
        mongo_d_b_collection_total_index_size: Optional[int] = Field(
            None, description="", alias="mongoDBCollectionTotalIndexSize"
        )
        mongo_d_b_collection_average_object_size: Optional[int] = Field(
            None, description="", alias="mongoDBCollectionAverageObjectSize"
        )
        mongo_d_b_collection_schema_definition: Optional[str] = Field(
            None, description="", alias="mongoDBCollectionSchemaDefinition"
        )
        column_count: Optional[int] = Field(None, description="", alias="columnCount")
        row_count: Optional[int] = Field(None, description="", alias="rowCount")
        size_bytes: Optional[int] = Field(None, description="", alias="sizeBytes")
        alias: Optional[str] = Field(None, description="", alias="alias")
        is_temporary: Optional[bool] = Field(None, description="", alias="isTemporary")
        is_query_preview: Optional[bool] = Field(
            None, description="", alias="isQueryPreview"
        )
        query_preview_config: Optional[dict[str, str]] = Field(
            None, description="", alias="queryPreviewConfig"
        )
        external_location: Optional[str] = Field(
            None, description="", alias="externalLocation"
        )
        external_location_region: Optional[str] = Field(
            None, description="", alias="externalLocationRegion"
        )
        external_location_format: Optional[str] = Field(
            None, description="", alias="externalLocationFormat"
        )
        is_partitioned: Optional[bool] = Field(
            None, description="", alias="isPartitioned"
        )
        partition_strategy: Optional[str] = Field(
            None, description="", alias="partitionStrategy"
        )
        partition_count: Optional[int] = Field(
            None, description="", alias="partitionCount"
        )
        partition_list: Optional[str] = Field(
            None, description="", alias="partitionList"
        )
        query_count: Optional[int] = Field(None, description="", alias="queryCount")
        query_user_count: Optional[int] = Field(
            None, description="", alias="queryUserCount"
        )
        query_user_map: Optional[dict[str, int]] = Field(
            None, description="", alias="queryUserMap"
        )
        query_count_updated_at: Optional[datetime] = Field(
            None, description="", alias="queryCountUpdatedAt"
        )
        database_name: Optional[str] = Field(None, description="", alias="databaseName")
        database_qualified_name: Optional[str] = Field(
            None, description="", alias="databaseQualifiedName"
        )
        schema_name: Optional[str] = Field(None, description="", alias="schemaName")
        schema_qualified_name: Optional[str] = Field(
            None, description="", alias="schemaQualifiedName"
        )
        table_name: Optional[str] = Field(None, description="", alias="tableName")
        table_qualified_name: Optional[str] = Field(
            None, description="", alias="tableQualifiedName"
        )
        view_name: Optional[str] = Field(None, description="", alias="viewName")
        view_qualified_name: Optional[str] = Field(
            None, description="", alias="viewQualifiedName"
        )
        is_profiled: Optional[bool] = Field(None, description="", alias="isProfiled")
        last_profiled_at: Optional[datetime] = Field(
            None, description="", alias="lastProfiledAt"
        )
        mongo_d_b_database: Optional[MongoDBDatabase] = Field(
            None, description="", alias="mongoDBDatabase"
        )  # relationship

    attributes: "MongoDBCollection.Attributes" = Field(
        default_factory=lambda: MongoDBCollection.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class MongoDBDatabase(Database):
    """Description"""

    type_name: str = Field("MongoDBDatabase", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MongoDBDatabase":
            raise ValueError("must be MongoDBDatabase")
        return v

    def __setattr__(self, name, value):
        if name in MongoDBDatabase._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MONGO_DB_DATABASE_COLLECTION_COUNT: ClassVar[NumericField] = NumericField(
        "mongoDBDatabaseCollectionCount", "mongoDBDatabaseCollectionCount"
    )
    """
    The number of collection in a MongoDB Database
    """
    SCHEMA_COUNT: ClassVar[NumericField] = NumericField("schemaCount", "schemaCount")
    """
    TBC
    """
    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    TBC
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    TBC
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    TBC
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    TBC
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    TBC
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    TBC
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    TBC
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    TBC
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    TBC
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    TBC
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    TBC
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    TBC
    """
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    TBC
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    TBC
    """

    MONGO_DB_COLLECTIONS: ClassVar[RelationField] = RelationField("mongoDBCollections")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "mongo_d_b_database_collection_count",
        "schema_count",
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
        "is_profiled",
        "last_profiled_at",
        "mongo_d_b_collections",
    ]

    @property
    def mongo_d_b_database_collection_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mongo_d_b_database_collection_count
        )

    @mongo_d_b_database_collection_count.setter
    def mongo_d_b_database_collection_count(
        self, mongo_d_b_database_collection_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_database_collection_count = (
            mongo_d_b_database_collection_count
        )

    @property
    def schema_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.schema_count

    @schema_count.setter
    def schema_count(self, schema_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_count = schema_count

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
    def query_user_map(self) -> Optional[dict[str, int]]:
        return None if self.attributes is None else self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[dict[str, int]]):
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
    def mongo_d_b_collections(self) -> Optional[list[MongoDBCollection]]:
        return (
            None if self.attributes is None else self.attributes.mongo_d_b_collections
        )

    @mongo_d_b_collections.setter
    def mongo_d_b_collections(
        self, mongo_d_b_collections: Optional[list[MongoDBCollection]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mongo_d_b_collections = mongo_d_b_collections

    class Attributes(Database.Attributes):
        mongo_d_b_database_collection_count: Optional[int] = Field(
            None, description="", alias="mongoDBDatabaseCollectionCount"
        )
        schema_count: Optional[int] = Field(None, description="", alias="schemaCount")
        query_count: Optional[int] = Field(None, description="", alias="queryCount")
        query_user_count: Optional[int] = Field(
            None, description="", alias="queryUserCount"
        )
        query_user_map: Optional[dict[str, int]] = Field(
            None, description="", alias="queryUserMap"
        )
        query_count_updated_at: Optional[datetime] = Field(
            None, description="", alias="queryCountUpdatedAt"
        )
        database_name: Optional[str] = Field(None, description="", alias="databaseName")
        database_qualified_name: Optional[str] = Field(
            None, description="", alias="databaseQualifiedName"
        )
        schema_name: Optional[str] = Field(None, description="", alias="schemaName")
        schema_qualified_name: Optional[str] = Field(
            None, description="", alias="schemaQualifiedName"
        )
        table_name: Optional[str] = Field(None, description="", alias="tableName")
        table_qualified_name: Optional[str] = Field(
            None, description="", alias="tableQualifiedName"
        )
        view_name: Optional[str] = Field(None, description="", alias="viewName")
        view_qualified_name: Optional[str] = Field(
            None, description="", alias="viewQualifiedName"
        )
        is_profiled: Optional[bool] = Field(None, description="", alias="isProfiled")
        last_profiled_at: Optional[datetime] = Field(
            None, description="", alias="lastProfiledAt"
        )
        mongo_d_b_collections: Optional[list[MongoDBCollection]] = Field(
            None, description="", alias="mongoDBCollections"
        )  # relationship

    attributes: "MongoDBDatabase.Attributes" = Field(
        default_factory=lambda: MongoDBDatabase.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


MongoDBCollection.Attributes.update_forward_refs()


MongoDBDatabase.Attributes.update_forward_refs()
