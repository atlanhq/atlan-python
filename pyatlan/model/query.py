# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import (
    HekaFlow,
    ParsingFlow,
    QueryParserSourceType,
    QueryStatus,
)


class ParsedQuery(AtlanObject):
    class DatabaseColumn(AtlanObject):
        id: Optional[str] = Field(
            default=None, description="Numeric identifier for the column."
        )
        name: Optional[str] = Field(
            default=None, description="Name of the column (unqualified)."
        )
        source: Optional[str] = Field(default=None, description="TBC")

    class RelationshipEndpoint(AtlanObject):
        id: Optional[str] = Field(
            default=None,
            description="Numeric identifier for the column referred to by this end of the relationship.",
        )
        column: Optional[str] = Field(
            default=None,
            description="Name of the column used by this end of the relationship.",
        )
        parent_id: Optional[str] = Field(
            default=None,
            description="Numeric identifier of the parent object in which the column exists.",
        )
        parent_name: Optional[str] = Field(
            default=None,
            description="Name of the parent object in which the column exists.",
        )

    class ParserError(AtlanObject):
        error_message: Optional[str] = Field(
            default=None, description="Description of the error."
        )
        error_type: Optional[str] = Field(
            default=None, description="Type of the error."
        )
        coordinates: Optional[List[Any]] = Field(description="TBC")

    class Relationship(AtlanObject):
        id: Optional[str] = Field(
            default=None, description="Numeric identifier for the relationship."
        )
        type: Optional[str] = Field(
            default=None, description="Type of the relationship."
        )
        effect_type: Optional[str] = Field(
            default=None,
            description="Type of effect made by the query (for example, select vs insert).",
        )
        target: Optional[ParsedQuery.RelationshipEndpoint] = Field(description="TBC")
        sources: Optional[List[ParsedQuery.RelationshipEndpoint]] = Field(
            description="TBC"
        )
        process_id: Optional[str] = Field(
            default=None,
            description="Numeric identifier for the procedure (if any) that manages this relationship.",
        )
        process_type: Optional[str] = Field(
            default=None,
            description="Type of procedure (if any) that manages this relationship.",
        )

    class DatabaseObject(AtlanObject):
        display_name: Optional[str] = Field(
            default=None,
            description="Fully-qualified name of the SQL object. (Only present on non-process objects.)",
        )
        id: Optional[str] = Field(
            default=None, description="Numeric identifier for the object."
        )
        name: Optional[str] = Field(
            default=None, description="Name of the object (unqualified)."
        )
        type: Optional[str] = Field(default=None, description="Type of the object.")
        database: Optional[str] = Field(
            default=None, description="Name of the database the object exists within."
        )
        db_schema: Optional[str] = Field(
            default=None,
            description="Name of the schema the object exists within.",
            alias="schema",
        )
        columns: Optional[List[ParsedQuery.DatabaseColumn]] = Field(
            description="List of details about the columns queried within the object."
            " (Only present on non-process objects.)"
        )
        procedure_name: Optional[str] = Field(
            default=None,
            description="Name of the procedure (only for process objects).",
        )
        query_hash_id: Optional[str] = Field(
            default=None,
            description="Unique hash representing the query (only for process objects).",
        )

    dbobjs: Optional[List[ParsedQuery.DatabaseObject]] = Field(
        description="All the database objects detected in the query."
    )
    relationships: Optional[List[ParsedQuery.Relationship]] = Field(
        description="All the relationship objects detected in the query."
    )
    errors: Optional[List[ParsedQuery.ParserError]] = Field(
        description="Any errors during parsing."
    )


class QueryParserRequest(AtlanObject):
    sql: str = Field(description="SQL query to be parsed.")
    source: QueryParserSourceType = Field(
        description="Dialect to use when parsing the SQL."
    )
    default_database: Optional[str] = Field(
        default=None,
        description="Default database name to use for unqualified objects in the SQL.",
    )
    default_schema: Optional[str] = Field(
        default=None,
        description="Default schema name to use for unqualified objects in the SQL.",
    )
    link_orphan_column_to_first_table: Optional[bool] = Field(description="TBC")
    show_join: Optional[bool] = Field(description="TBC")
    ignore_record_set: Optional[bool] = Field(description="TBC")
    ignore_coordinate: Optional[bool] = Field(description="TBC")

    @staticmethod
    def create(
        sql: str,
        source: QueryParserSourceType,
    ) -> QueryParserRequest:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["sql", "source"],
            [sql, source],
        )
        return QueryParserRequest(
            sql=sql,
            source=source,
            link_orphan_column_to_first_table=False,
            show_join=True,
            ignore_record_set=True,
            ignore_coordinate=True,
        )


ParsedQuery.Relationship.update_forward_refs()
ParsedQuery.DatabaseObject.update_forward_refs()
ParsedQuery.update_forward_refs()


class QueryRequest(AtlanObject):
    sql: str = Field(description="SQL query to run.")
    data_source_name: str = Field(
        description="Unique name of the connection to use for the query."
    )
    default_schema: str = Field(
        description="Default schema name to use for unqualified objects "
        "in the SQL, in the form `DB.SCHEMA`."
    )


class QueryResponse(AtlanObject):
    """
    Create a single consolidated response
    from multiple events related to the same query.
    """

    def __init__(self, events: Optional[List[Dict[str, Any]]] = None):
        super().__init__()
        if not events:
            return
        self.rows = []
        self.columns = []
        # Populate the results from all events that have rows
        for event in events:
            event_rows = event.get("rows")
            event_columns = event.get("columns")
            if event_rows:
                self.rows.extend(event_rows)
            if not self.columns and event_columns:
                # Only need to do this once
                self.columns = event_columns
        # Populate the remainder from the final event
        last_event = events[-1]
        self.request_id = last_event.get("requestId")
        self.error_name = last_event.get("errorName")
        self.error_message = last_event.get("errorMessage")
        self.error_code = last_event.get("errorCode")
        self.query_id = last_event.get("queryId")
        self.details = last_event.get("details")

    request_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for the request, if there was any error.",
    )
    error_name: Optional[str] = Field(
        default=None, description="Unique name for the error, if there was any error."
    )
    error_message: Optional[str] = Field(
        default=None, description="Explanation of the error, if there was any error."
    )
    error_code: Optional[str] = Field(
        default=None, description="Unique code for the error, if there was any error."
    )
    query_id: Optional[str] = Field(
        default=None,
        description="Unique identifier (GUID) for the specific run of the query.",
    )
    rows: Optional[List[List[str]]] = Field(
        description="Results of the query. Each element is of "
        "the outer list is a single row, while each inner list gives "
        "the column values for that row (in order)"
    )

    class ColumnType(AtlanObject):
        id: Optional[int] = Field(
            description="Unique identifier for the request, if there was any error."
        )
        name: Optional[str] = Field(
            default=None, description="SQL name of the data type for this column.."
        )
        rep: Optional[str]

    class ColumnDetails(AtlanObject):
        """
        Details about the type of column that was returned from a query that was run.
        """

        ordinal: Optional[int] = Field(description="Position of the column (1-based).")
        auto_increment: Optional[bool] = Field(description="TBC")
        case_sensitive: Optional[bool] = Field(description="TBC")
        searchable: Optional[bool] = Field(description="TBC")
        currency: Optional[bool] = Field(description="TBC")
        nullable: Optional[int] = Field(description="TBC")
        signed: Optional[bool] = Field(description="TBC")
        display_size: Optional[int] = Field(description="TBC")
        label: Optional[str] = Field(
            default=None, description="Display value for the column's name."
        )
        column_name: Optional[str] = Field(
            default=None, description="Name of the column (technical)."
        )
        schema_name: Optional[str] = Field(
            default=None,
            description="Name of the schema in which this column's table is contained.",
        )
        precision: Optional[int] = Field(description="TBC")
        scale: Optional[int] = Field(description="TBC")
        table_name: Optional[str] = Field(
            default=None,
            description="Name of the table in which the column is contained.",
        )
        catalog_name: Optional[str] = Field(
            default=None,
            description="Name of the database in which the table's schema is contained.",
        )
        read_only: Optional[bool] = Field(description="TBC")
        writable: Optional[bool] = Field(description="TBC")
        definitely_writable: Optional[bool] = Field(description="TBC")
        column_class_name: Optional[str] = Field(
            default=None,
            description="Canonical name of the Java class representing this column's values.",
        )
        type: Optional[QueryResponse.ColumnType] = Field(
            description="Details about the (SQL) data type of the column."
        )

    columns: Optional[List[QueryResponse.ColumnDetails]] = Field(
        description="Columns that are present in each row of the results. "
        "The order of the elements of this list will match the order of "
        "the inner list of values for the `rows`."
    )

    class AssetDetails(AtlanObject):
        connection_name: Optional[str] = Field(
            default=None, description="Simple name of the connection."
        )
        connection_qn: Optional[str] = Field(
            default=None, description="Unique name of the connection."
        )
        database: Optional[str] = Field(
            default=None, description="Simple name of the database."
        )
        schema_: Optional[str] = Field(
            default=None, alias="schema", description="Simple name of the schema."
        )
        table: Optional[str] = Field(
            default=None, description="Simple name of the table."
        )

    class QueryDetails(AtlanObject):
        """
        Details about a query that was run.
        """

        total_rows_streamed: Optional[int] = Field(
            description="Total number of results returned by the query."
        )
        status: Optional[QueryStatus] = Field(description="Status of the query.")
        parsed_query: Optional[str] = Field(default=None, description="TBC")
        pushdown_query: Optional[str] = Field(
            default=None, description="Query that was sent to the data store."
        )
        execution_time: Optional[int] = Field(
            description="How long the query took to run, in milliseconds."
        )
        source_query_id: Optional[str] = Field(default=None, description="TBC")
        result_output_location: Optional[str] = Field(default=None, description="TBC")
        warnings: Optional[List[str]] = Field(
            default=None,
            description="List of any warnings produced when running the query.",
        )
        parsing_flow: Optional[ParsingFlow] = Field(
            description="How the query was parsed prior to running."
        )
        heka_flow: Optional[HekaFlow] = Field(description="How the query was run.")
        s3_upload_path: Optional[str] = Field(default=None, description="TBC")
        source_first_connection_time: Optional[int] = Field(description="TBC")
        source_first_connection_time_perc: Optional[float] = Field(description="TBC")
        explain_call_time_perc: Optional[float] = Field(description="TBC")
        init_data_source_time: Optional[int] = Field(description="TBC")
        init_data_source_time_perc: Optional[float] = Field(description="TBC")
        authorization_time: Optional[int] = Field(description="TBC")
        authorization_time_perc: Optional[float] = Field(description="TBC")
        rewrite_validation_time: Optional[int] = Field(description="TBC")
        rewrite_validation_time_perc: Optional[float] = Field(description="TBC")
        extract_table_metadata_time: Optional[int] = Field(
            description="Elapsed time to extract table metadata, in milliseconds."
        )
        extract_table_metadata_time_perc: Optional[float] = Field(description="TBC")
        execution_time_internal: Optional[int] = Field(
            description="Elapsed time to run the query (from internal engine), in milliseconds."
        )
        execution_time_perc: Optional[float] = Field(description="TBC")
        bypass_query_time: Optional[int] = Field(description="TBC")
        bypass_parsing_percentage: Optional[float] = Field(description="TBC")
        check_insights_enabled_time: Optional[int] = Field(description="TBC")
        check_insights_enabled_percentage: Optional[float] = Field(description="TBC")
        initialization_time: Optional[int] = Field(description="TBC")
        initialization_percentage: Optional[float] = Field(description="TBC")
        extract_credentials_time: Optional[int] = Field(description="TBC")
        extract_credentials_percentage: Optional[float] = Field(description="TBC")
        overall_time: Optional[int] = Field(description="TBC")
        overall_time_percentage: Optional[float] = Field(description="TBC")
        heka_atlan_time: Optional[int] = Field(description="TBC")
        calcite_parsing_percentage: Optional[float] = Field(description="TBC")
        calcite_validation_percentage: Optional[float] = Field(description="TBC")
        asset: Optional[QueryResponse.AssetDetails] = Field(
            description="Metadata about the asset used in the query, in case of any errors."
        )
        developer_message: Optional[str] = Field(
            default=None,
            description="Detailed back-end error message that could be helpful for developers.",
        )
        line: Optional[int] = Field(
            description="Line number of the query that had a validation error, if any."
        )
        column: Optional[int] = Field(
            description="Column position of the validation error, if any."
        )
        obj: Optional[str] = Field(
            default=None,
            description="Name of the object that caused the validation error, if any.",
        )

    details: Optional[QueryResponse.QueryDetails] = Field(
        description="Details about the query."
    )


QueryResponse.ColumnType.update_forward_refs()
QueryResponse.ColumnDetails.update_forward_refs()
QueryResponse.AssetDetails.update_forward_refs()
QueryResponse.QueryDetails.update_forward_refs()
QueryResponse.update_forward_refs()
