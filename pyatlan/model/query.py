# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import QueryParserSourceType


class ParsedQuery(AtlanObject):
    class DatabaseColumn(AtlanObject):
        id: Optional[str] = Field(description="Numeric identifier for the column.")
        name: Optional[str] = Field(description="Name of the column (unqualified).")
        source: Optional[str] = Field(description="TBC")

    class RelationshipEndpoint(AtlanObject):
        id: Optional[str] = Field(
            description="Numeric identifier for the column referred to by this end of the relationship."
        )
        column: Optional[str] = Field(
            description="Name of the column used by this end of the relationship."
        )
        parent_id: Optional[str] = Field(
            description="Numeric identifier of the parent object in which the column exists."
        )
        parent_name: Optional[str] = Field(
            description="Name of the parent object in which the column exists."
        )

    class ParserError(AtlanObject):
        error_message: Optional[str] = Field(description="Description of the error.")
        error_type: Optional[str] = Field(description="Type of the error.")
        coordinates: Optional[List[Any]] = Field(description="TBC")

    class Relationship(AtlanObject):
        id: Optional[str] = Field(
            description="Numeric identifier for the relationship."
        )
        type: Optional[str] = Field(description="Type of the relationship.")
        effect_type: Optional[str] = Field(
            description="Type of effect made by the query (for example, select vs insert)."
        )
        target: Optional[ParsedQuery.RelationshipEndpoint] = Field(description="TBC")
        sources: Optional[List[ParsedQuery.RelationshipEndpoint]] = Field(
            description="TBC"
        )
        process_id: Optional[str] = Field(
            description="Numeric identifier for the procedure (if any) that manages this relationship."
        )
        process_type: Optional[str] = Field(
            description="Type of procedure (if any) that manages this relationship."
        )

    class DatabaseObject(AtlanObject):
        display_name: Optional[str] = Field(
            description="Fully-qualified name of the SQL object. (Only present on non-process objects.)"
        )
        id: Optional[str] = Field(description="Numeric identifier for the object.")
        name: Optional[str] = Field(description="Name of the object (unqualified).")
        type: Optional[str] = Field(description="Type of the object.")
        database: Optional[str] = Field(
            description="Name of the database the object exists within."
        )
        db_schema: Optional[str] = Field(
            description="Name of the schema the object exists within.", alias="schema"
        )
        columns: Optional[List[ParsedQuery.DatabaseColumn]] = Field(
            description="List of details about the columns queried within the object."
            " (Only present on non-process objects.)"
        )
        procedure_name: Optional[str] = Field(
            description="Name of the procedure (only for process objects)."
        )
        query_hash_id: Optional[str] = Field(
            description="Unique hash representing the query (only for process objects)."
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
        description="Default database name to use for unqualified objects in the SQL."
    )
    default_schema: Optional[str] = Field(
        description="Default schema name to use for unqualified objects in the SQL."
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
