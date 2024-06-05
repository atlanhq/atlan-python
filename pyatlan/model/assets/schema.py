# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .s_q_l import SQL


class Schema(SQL):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str,
    ) -> Schema: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str,
        database_name: str,
        connection_qualified_name: str,
    ) -> Schema: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        database_qualified_name: str,
        database_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
    ) -> Schema:
        validate_required_fields(
            ["name", "database_qualified_name"], [name, database_qualified_name]
        )
        attributes = Schema.Attributes.create(
            name=name,
            database_qualified_name=database_qualified_name,
            database_name=database_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, database_qualified_name: str) -> Schema:
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
            database_qualified_name=database_qualified_name,
        )

    type_name: str = Field(default="Schema", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Schema":
            raise ValueError("must be Schema")
        return v

    def __setattr__(self, name, value):
        if name in Schema._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TABLE_COUNT: ClassVar[NumericField] = NumericField("tableCount", "tableCount")
    """
    Number of tables in this schema.
    """
    VIEWS_COUNT: ClassVar[NumericField] = NumericField("viewsCount", "viewsCount")
    """
    Number of views in this schema.
    """
    LINKED_SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "linkedSchemaQualifiedName", "linkedSchemaQualifiedName"
    )
    """
    Unique name of the Linked Schema on which this Schema is dependent. This concept is mostly applicable for linked datasets/datasource in Google BigQuery via Analytics Hub Listing
    """  # noqa: E501

    SNOWFLAKE_TAGS: ClassVar[RelationField] = RelationField("snowflakeTags")
    """
    TBC
    """
    FUNCTIONS: ClassVar[RelationField] = RelationField("functions")
    """
    TBC
    """
    TABLES: ClassVar[RelationField] = RelationField("tables")
    """
    TBC
    """
    DATABASE: ClassVar[RelationField] = RelationField("database")
    """
    TBC
    """
    PROCEDURES: ClassVar[RelationField] = RelationField("procedures")
    """
    TBC
    """
    VIEWS: ClassVar[RelationField] = RelationField("views")
    """
    TBC
    """
    MATERIALISED_VIEWS: ClassVar[RelationField] = RelationField("materialisedViews")
    """
    TBC
    """
    SNOWFLAKE_DYNAMIC_TABLES: ClassVar[RelationField] = RelationField(
        "snowflakeDynamicTables"
    )
    """
    TBC
    """
    SNOWFLAKE_PIPES: ClassVar[RelationField] = RelationField("snowflakePipes")
    """
    TBC
    """
    SNOWFLAKE_STREAMS: ClassVar[RelationField] = RelationField("snowflakeStreams")
    """
    TBC
    """
    CALCULATION_VIEWS: ClassVar[RelationField] = RelationField("calculationViews")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "table_count",
        "views_count",
        "linked_schema_qualified_name",
        "snowflake_tags",
        "functions",
        "tables",
        "database",
        "procedures",
        "views",
        "materialised_views",
        "snowflake_dynamic_tables",
        "snowflake_pipes",
        "snowflake_streams",
        "calculation_views",
    ]

    @property
    def table_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.table_count

    @table_count.setter
    def table_count(self, table_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_count = table_count

    @property
    def views_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.views_count

    @views_count.setter
    def views_count(self, views_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views_count = views_count

    @property
    def linked_schema_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.linked_schema_qualified_name
        )

    @linked_schema_qualified_name.setter
    def linked_schema_qualified_name(self, linked_schema_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.linked_schema_qualified_name = linked_schema_qualified_name

    @property
    def snowflake_tags(self) -> Optional[List[SnowflakeTag]]:
        return None if self.attributes is None else self.attributes.snowflake_tags

    @snowflake_tags.setter
    def snowflake_tags(self, snowflake_tags: Optional[List[SnowflakeTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_tags = snowflake_tags

    @property
    def functions(self) -> Optional[List[Function]]:
        return None if self.attributes is None else self.attributes.functions

    @functions.setter
    def functions(self, functions: Optional[List[Function]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.functions = functions

    @property
    def tables(self) -> Optional[List[Table]]:
        return None if self.attributes is None else self.attributes.tables

    @tables.setter
    def tables(self, tables: Optional[List[Table]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tables = tables

    @property
    def database(self) -> Optional[Database]:
        return None if self.attributes is None else self.attributes.database

    @database.setter
    def database(self, database: Optional[Database]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database = database

    @property
    def procedures(self) -> Optional[List[Procedure]]:
        return None if self.attributes is None else self.attributes.procedures

    @procedures.setter
    def procedures(self, procedures: Optional[List[Procedure]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.procedures = procedures

    @property
    def views(self) -> Optional[List[View]]:
        return None if self.attributes is None else self.attributes.views

    @views.setter
    def views(self, views: Optional[List[View]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views = views

    @property
    def materialised_views(self) -> Optional[List[MaterialisedView]]:
        return None if self.attributes is None else self.attributes.materialised_views

    @materialised_views.setter
    def materialised_views(self, materialised_views: Optional[List[MaterialisedView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.materialised_views = materialised_views

    @property
    def snowflake_dynamic_tables(self) -> Optional[List[SnowflakeDynamicTable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_dynamic_tables
        )

    @snowflake_dynamic_tables.setter
    def snowflake_dynamic_tables(
        self, snowflake_dynamic_tables: Optional[List[SnowflakeDynamicTable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_dynamic_tables = snowflake_dynamic_tables

    @property
    def snowflake_pipes(self) -> Optional[List[SnowflakePipe]]:
        return None if self.attributes is None else self.attributes.snowflake_pipes

    @snowflake_pipes.setter
    def snowflake_pipes(self, snowflake_pipes: Optional[List[SnowflakePipe]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_pipes = snowflake_pipes

    @property
    def snowflake_streams(self) -> Optional[List[SnowflakeStream]]:
        return None if self.attributes is None else self.attributes.snowflake_streams

    @snowflake_streams.setter
    def snowflake_streams(self, snowflake_streams: Optional[List[SnowflakeStream]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_streams = snowflake_streams

    @property
    def calculation_views(self) -> Optional[List[CalculationView]]:
        return None if self.attributes is None else self.attributes.calculation_views

    @calculation_views.setter
    def calculation_views(self, calculation_views: Optional[List[CalculationView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_views = calculation_views

    class Attributes(SQL.Attributes):
        table_count: Optional[int] = Field(default=None, description="")
        views_count: Optional[int] = Field(default=None, description="")
        linked_schema_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_tags: Optional[List[SnowflakeTag]] = Field(
            default=None, description=""
        )  # relationship
        functions: Optional[List[Function]] = Field(
            default=None, description=""
        )  # relationship
        tables: Optional[List[Table]] = Field(
            default=None, description=""
        )  # relationship
        database: Optional[Database] = Field(
            default=None, description=""
        )  # relationship
        procedures: Optional[List[Procedure]] = Field(
            default=None, description=""
        )  # relationship
        views: Optional[List[View]] = Field(
            default=None, description=""
        )  # relationship
        materialised_views: Optional[List[MaterialisedView]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_dynamic_tables: Optional[List[SnowflakeDynamicTable]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_pipes: Optional[List[SnowflakePipe]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_streams: Optional[List[SnowflakeStream]] = Field(
            default=None, description=""
        )  # relationship
        calculation_views: Optional[List[CalculationView]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            database_qualified_name: str,
            database_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
        ) -> Schema.Attributes:
            validate_required_fields(
                ["name, database_qualified_name"], [name, database_qualified_name]
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
            database = Database.ref_by_qualified_name(database_qualified_name)

            return Schema.Attributes(
                name=name,
                qualified_name=qualified_name,
                database=database,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
            )

    attributes: Schema.Attributes = Field(
        default_factory=lambda: Schema.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .calculation_view import CalculationView  # noqa
from .database import Database  # noqa
from .function import Function  # noqa
from .materialised_view import MaterialisedView  # noqa
from .procedure import Procedure  # noqa
from .snowflake_dynamic_table import SnowflakeDynamicTable  # noqa
from .snowflake_pipe import SnowflakePipe  # noqa
from .snowflake_stream import SnowflakeStream  # noqa
from .snowflake_tag import SnowflakeTag  # noqa
from .table import Table  # noqa
from .view import View  # noqa
