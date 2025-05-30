# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType, TableType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .s_q_l import SQL


class Table(SQL):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str,
    ) -> Table: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str,
        schema_name: str,
        database_name: str,
        database_qualified_name: str,
        connection_qualified_name: str,
    ) -> Table: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str,
        schema_name: Optional[str] = None,
        database_name: Optional[str] = None,
        database_qualified_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
    ) -> Table:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = Table.Attributes.create(
            name=name,
            schema_qualified_name=schema_qualified_name,
            schema_name=schema_name,
            database_name=database_name,
            database_qualified_name=database_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, schema_qualified_name: str) -> Table:
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
            schema_qualified_name=schema_qualified_name,
        )

    type_name: str = Field(default="Table", allow_mutation=True)

    @validator("type_name")
    def validate_type_name(cls, v):
        return v

    def __setattr__(self, name, value):
        if name in Table._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

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
    PARTITIONS: ClassVar[RelationField] = RelationField("partitions")
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
        "partitions",
        "queries",
        "dimensions",
    ]

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
    def partitions(self) -> Optional[List[TablePartition]]:
        return None if self.attributes is None else self.attributes.partitions

    @partitions.setter
    def partitions(self, partitions: Optional[List[TablePartition]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partitions = partitions

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

    class Attributes(SQL.Attributes):
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
        partitions: Optional[List[TablePartition]] = Field(
            default=None, description=""
        )  # relationship
        queries: Optional[List[Query]] = Field(
            default=None, description=""
        )  # relationship
        dimensions: Optional[List[Table]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            schema_qualified_name: str,
            schema_name: Optional[str] = None,
            database_name: Optional[str] = None,
            database_qualified_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
        ) -> Table.Attributes:
            validate_required_fields(
                ["name, schema_qualified_name"], [name, schema_qualified_name]
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    schema_qualified_name, "schema_qualified_name", 5
                )

            fields = schema_qualified_name.split("/")
            qualified_name = f"{schema_qualified_name}/{name}"
            connection_qualified_name = connection_qualified_name or connection_qn
            database_name = database_name or fields[3]
            schema_name = schema_name or fields[4]
            database_qualified_name = (
                database_qualified_name
                or f"{connection_qualified_name}/{database_name}"
            )

            return Table.Attributes(
                name=name,
                qualified_name=qualified_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                schema_name=schema_name,
                schema_qualified_name=schema_qualified_name,
                atlan_schema=Schema.ref_by_qualified_name(schema_qualified_name),
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
            )

    attributes: Table.Attributes = Field(
        default_factory=lambda: Table.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .column import Column  # noqa: E402, F401
from .query import Query  # noqa: E402, F401
from .schema import Schema  # noqa: E402, F401
from .table_partition import TablePartition  # noqa: E402, F401
