# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Union

import msgspec

from pyatlan.model.enums import (
    HekaFlow,
    ParsingFlow,
    QueryParserSourceType,
    QueryStatus,
)
from pyatlan.utils import validate_required_fields


class DatabaseColumn(msgspec.Struct, kw_only=True):
    """Column referenced in a parsed query."""

    id: Union[str, None] = None
    """Numeric identifier for the column."""
    name: Union[str, None] = None
    """Name of the column (unqualified)."""
    source: Union[str, None] = None


class RelationshipEndpoint(msgspec.Struct, kw_only=True):
    """Endpoint of a lineage relationship in a parsed query."""

    id: Union[str, None] = None
    """Numeric identifier for the column."""
    column: Union[str, None] = None
    """Name of the column."""
    parent_id: Union[str, None] = None
    """Numeric identifier of the parent object."""
    parent_name: Union[str, None] = None
    """Name of the parent object."""


class ParserError(msgspec.Struct, kw_only=True):
    """Error encountered during query parsing."""

    error_message: Union[str, None] = None
    """Description of the error."""
    error_type: Union[str, None] = None
    """Type of the error."""
    coordinates: Union[list[Any], None] = None


class QueryRelationship(msgspec.Struct, kw_only=True):
    """Relationship detected in a parsed query."""

    id: Union[str, None] = None
    """Numeric identifier for the relationship."""
    type: Union[str, None] = None
    """Type of the relationship."""
    effect_type: Union[str, None] = None
    """Type of effect made by the query (e.g. select vs insert)."""
    target: Union[RelationshipEndpoint, None] = None
    sources: Union[list[RelationshipEndpoint], None] = None
    process_id: Union[str, None] = None
    """Numeric identifier for the procedure."""
    process_type: Union[str, None] = None
    """Type of procedure."""


class DatabaseObject(msgspec.Struct, kw_only=True):
    """Database object detected in a parsed query."""

    display_name: Union[str, None] = None
    """Fully-qualified name of the SQL object."""
    id: Union[str, None] = None
    """Numeric identifier for the object."""
    name: Union[str, None] = None
    """Name of the object (unqualified)."""
    type: Union[str, None] = None
    """Type of the object."""
    database: Union[str, None] = None
    """Name of the database."""
    db_schema: Union[str, None] = msgspec.field(default=None, name="schema")
    """Name of the schema."""
    columns: Union[list[DatabaseColumn], None] = None
    """List of columns queried within the object."""
    procedure_name: Union[str, None] = None
    """Name of the procedure (only for process objects)."""
    query_hash_id: Union[str, None] = None
    """Unique hash representing the query (only for process objects)."""


class ParsedQuery(msgspec.Struct, kw_only=True):
    """Result of parsing a SQL query."""

    dbobjs: Union[list[DatabaseObject], None] = None
    """All the database objects detected in the query."""
    relationships: Union[list[QueryRelationship], None] = None
    """All the relationship objects detected in the query."""
    errors: Union[list[ParserError], None] = None
    """Any errors during parsing."""


class QueryParserRequest(msgspec.Struct, kw_only=True):
    """Request to parse a SQL query."""

    sql: str
    """SQL query to be parsed."""
    source: QueryParserSourceType
    """Dialect to use when parsing the SQL."""
    default_database: Union[str, None] = None
    """Default database name for unqualified objects."""
    default_schema: Union[str, None] = None
    """Default schema name for unqualified objects."""
    link_orphan_column_to_first_table: Union[bool, None] = None
    show_join: Union[bool, None] = None
    ignore_record_set: Union[bool, None] = None
    ignore_coordinate: Union[bool, None] = None

    @staticmethod
    def creator(
        sql: str,
        source: QueryParserSourceType,
    ) -> QueryParserRequest:
        """
        Create a query parser request.

        :param sql: SQL query to be parsed
        :param source: dialect to use when parsing
        :returns: a configured QueryParserRequest
        """
        validate_required_fields(["sql", "source"], [sql, source])
        return QueryParserRequest(
            sql=sql,
            source=source,
            link_orphan_column_to_first_table=False,
            show_join=True,
            ignore_record_set=True,
            ignore_coordinate=True,
        )


class QueryRequest(msgspec.Struct, kw_only=True):
    """Request to run a SQL query."""

    sql: str
    """SQL query to run."""
    data_source_name: str
    """Unique name of the connection to use for the query."""
    default_schema: str
    """Default schema name in the form 'DB.SCHEMA'."""


class ColumnType(msgspec.Struct, kw_only=True):
    """SQL column type details."""

    id: Union[int, None] = None
    name: Union[str, None] = None
    """SQL name of the data type."""
    rep: Union[str, None] = None


class ColumnDetails(msgspec.Struct, kw_only=True):
    """Details about a column returned from a query."""

    ordinal: Union[int, None] = None
    """Position of the column (1-based)."""
    auto_increment: Union[bool, None] = None
    case_sensitive: Union[bool, None] = None
    searchable: Union[bool, None] = None
    currency: Union[bool, None] = None
    nullable: Union[int, None] = None
    signed: Union[bool, None] = None
    display_size: Union[int, None] = None
    label: Union[str, None] = None
    """Display value for the column's name."""
    column_name: Union[str, None] = None
    """Name of the column (technical)."""
    schema_name: Union[str, None] = None
    """Name of the schema."""
    precision: Union[int, None] = None
    scale: Union[int, None] = None
    table_name: Union[str, None] = None
    """Name of the table."""
    catalog_name: Union[str, None] = None
    """Name of the database."""
    read_only: Union[bool, None] = None
    writable: Union[bool, None] = None
    definitely_writable: Union[bool, None] = None
    column_class_name: Union[str, None] = None
    """Canonical name of the Java class."""
    type: Union[ColumnType, None] = None
    """Details about the (SQL) data type."""


class AssetDetails(msgspec.Struct, kw_only=True):
    """Asset details in a query response."""

    connection_name: Union[str, None] = None
    """Simple name of the connection."""
    connection_qn: Union[str, None] = None
    """Unique name of the connection."""
    database: Union[str, None] = None
    """Simple name of the database."""
    schema_: Union[str, None] = msgspec.field(default=None, name="schema")
    """Simple name of the schema."""
    table: Union[str, None] = None
    """Simple name of the table."""


class QueryDetails(msgspec.Struct, kw_only=True):
    """Details about a query that was run."""

    total_rows_streamed: Union[int, None] = None
    """Total number of results returned."""
    status: Union[QueryStatus, None] = None
    """Status of the query."""
    parsed_query: Union[str, None] = None
    pushdown_query: Union[str, None] = None
    """Query sent to the data store."""
    execution_time: Union[int, None] = None
    """How long the query took, in milliseconds."""
    source_query_id: Union[str, None] = None
    result_output_location: Union[str, None] = None
    warnings: Union[list[str], None] = None
    """Warnings produced when running the query."""
    parsing_flow: Union[ParsingFlow, None] = None
    """How the query was parsed."""
    heka_flow: Union[HekaFlow, None] = None
    """How the query was run."""
    s3_upload_path: Union[str, None] = None
    source_first_connection_time: Union[int, None] = None
    source_first_connection_time_perc: Union[float, None] = None
    explain_call_time_perc: Union[float, None] = None
    init_data_source_time: Union[int, None] = None
    init_data_source_time_perc: Union[float, None] = None
    authorization_time: Union[int, None] = None
    authorization_time_perc: Union[float, None] = None
    rewrite_validation_time: Union[int, None] = None
    rewrite_validation_time_perc: Union[float, None] = None
    extract_table_metadata_time: Union[int, None] = None
    """Elapsed time to extract table metadata, in milliseconds."""
    extract_table_metadata_time_perc: Union[float, None] = None
    execution_time_internal: Union[int, None] = None
    """Elapsed time to run the query (from internal engine), in milliseconds."""
    execution_time_perc: Union[float, None] = None
    bypass_query_time: Union[int, None] = None
    bypass_parsing_percentage: Union[float, None] = None
    check_insights_enabled_time: Union[int, None] = None
    check_insights_enabled_percentage: Union[float, None] = None
    initialization_time: Union[int, None] = None
    initialization_percentage: Union[float, None] = None
    extract_credentials_time: Union[int, None] = None
    extract_credentials_percentage: Union[float, None] = None
    overall_time: Union[int, None] = None
    overall_time_percentage: Union[float, None] = None
    heka_atlan_time: Union[int, None] = None
    calcite_parsing_percentage: Union[float, None] = None
    calcite_validation_percentage: Union[float, None] = None
    asset: Union[AssetDetails, None] = None
    """Metadata about the asset used in the query."""
    developer_message: Union[str, None] = None
    """Detailed back-end error message."""
    line: Union[int, None] = None
    """Line number of the validation error."""
    column: Union[int, None] = None
    """Column position of the validation error."""
    obj: Union[str, None] = None
    """Name of the object that caused the validation error."""


class QueryResponse:
    """
    Consolidated response from multiple events related to the same query.

    Replaces the Pydantic model with a plain class since it has custom
    __init__ logic for consolidating event data.
    """

    def __init__(self, events: Union[list[dict[str, Any]], None] = None):
        self.request_id: Union[str, None] = None
        self.error_name: Union[str, None] = None
        self.error_message: Union[str, None] = None
        self.error_code: Union[str, None] = None
        self.query_id: Union[str, None] = None
        self.rows: Union[list[list[str]], None] = None
        self.columns: Union[list[ColumnDetails], None] = None
        self.details: Union[QueryDetails, None] = None

        if not events:
            return

        self.rows = []
        self.columns = []
        for event in events:
            event_rows = event.get("rows")
            event_columns = event.get("columns")
            if event_rows:
                self.rows.extend(event_rows)
            if not self.columns and event_columns:
                self.columns = msgspec.convert(
                    event_columns, list[ColumnDetails], strict=False
                )

        last_event = events[-1]
        self.request_id = last_event.get("requestId")
        self.error_name = last_event.get("errorName")
        self.error_message = last_event.get("errorMessage")
        self.error_code = last_event.get("errorCode")
        self.query_id = last_event.get("queryId")
        details_raw = last_event.get("details")
        if details_raw:
            self.details = msgspec.convert(details_raw, QueryDetails, strict=False)
