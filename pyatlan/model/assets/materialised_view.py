# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .s_q_l import SQL


class MaterialisedView(SQL):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        schema_qualified_name: str,
    ) -> MaterialisedView: ...

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
    ) -> MaterialisedView: ...

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
    ) -> MaterialisedView:
        validate_required_fields(
            ["name", "schema_qualified_name"], [name, schema_qualified_name]
        )
        attributes = MaterialisedView.Attributes.create(
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
    def create(cls, *, name: str, schema_qualified_name: str) -> MaterialisedView:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(name=name, schema_qualified_name=schema_qualified_name)

    type_name: str = Field(default="MaterialisedView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MaterialisedView":
            raise ValueError("must be MaterialisedView")
        return v

    def __setattr__(self, name, value):
        if name in MaterialisedView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    REFRESH_MODE: ClassVar[KeywordField] = KeywordField("refreshMode", "refreshMode")
    """
    Refresh mode for this materialized view.
    """
    REFRESH_METHOD: ClassVar[KeywordField] = KeywordField(
        "refreshMethod", "refreshMethod"
    )
    """
    Refresh method for this materialized view.
    """
    STALENESS: ClassVar[KeywordField] = KeywordField("staleness", "staleness")
    """
    Staleness of this materialized view.
    """
    STALE_SINCE_DATE: ClassVar[NumericField] = NumericField(
        "staleSinceDate", "staleSinceDate"
    )
    """
    Time (epoch) from which this materialized view is stale, in milliseconds.
    """
    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    Number of columns in this materialized view.
    """
    ROW_COUNT: ClassVar[NumericField] = NumericField("rowCount", "rowCount")
    """
    Number of rows in this materialized view.
    """
    SIZE_BYTES: ClassVar[NumericField] = NumericField("sizeBytes", "sizeBytes")
    """
    Size of this materialized view, in bytes.
    """
    IS_QUERY_PREVIEW: ClassVar[BooleanField] = BooleanField(
        "isQueryPreview", "isQueryPreview"
    )
    """
    Whether it's possible to run a preview query on this materialized view (true) or not (false).
    """
    QUERY_PREVIEW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "queryPreviewConfig", "queryPreviewConfig"
    )
    """
    Configuration for the query preview of this materialized view.
    """
    ALIAS: ClassVar[KeywordField] = KeywordField("alias", "alias")
    """
    Alias for this materialized view.
    """
    IS_TEMPORARY: ClassVar[BooleanField] = BooleanField("isTemporary", "isTemporary")
    """
    Whether this materialized view is temporary (true) or not (false).
    """
    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL definition of this materialized view.
    """

    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "refresh_mode",
        "refresh_method",
        "staleness",
        "stale_since_date",
        "column_count",
        "row_count",
        "size_bytes",
        "is_query_preview",
        "query_preview_config",
        "alias",
        "is_temporary",
        "definition",
        "columns",
        "atlan_schema",
    ]

    @property
    def refresh_mode(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.refresh_mode

    @refresh_mode.setter
    def refresh_mode(self, refresh_mode: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.refresh_mode = refresh_mode

    @property
    def refresh_method(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.refresh_method

    @refresh_method.setter
    def refresh_method(self, refresh_method: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.refresh_method = refresh_method

    @property
    def staleness(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.staleness

    @staleness.setter
    def staleness(self, staleness: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.staleness = staleness

    @property
    def stale_since_date(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.stale_since_date

    @stale_since_date.setter
    def stale_since_date(self, stale_since_date: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.stale_since_date = stale_since_date

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
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    @property
    def columns(self) -> Optional[List[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[List[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        refresh_mode: Optional[str] = Field(default=None, description="")
        refresh_method: Optional[str] = Field(default=None, description="")
        staleness: Optional[str] = Field(default=None, description="")
        stale_since_date: Optional[datetime] = Field(default=None, description="")
        column_count: Optional[int] = Field(default=None, description="")
        row_count: Optional[int] = Field(default=None, description="")
        size_bytes: Optional[int] = Field(default=None, description="")
        is_query_preview: Optional[bool] = Field(default=None, description="")
        query_preview_config: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        alias: Optional[str] = Field(default=None, description="")
        is_temporary: Optional[bool] = Field(default=None, description="")
        definition: Optional[str] = Field(default=None, description="")
        columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
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
        ) -> MaterialisedView.Attributes:
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
            atlan_schema = Schema.ref_by_qualified_name(schema_qualified_name)

            return MaterialisedView.Attributes(
                name=name,
                qualified_name=qualified_name,
                database_name=database_name,
                database_qualified_name=database_qualified_name,
                schema_qualified_name=schema_qualified_name,
                schema_name=schema_name,
                atlan_schema=atlan_schema,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
            )

    attributes: MaterialisedView.Attributes = Field(
        default_factory=lambda: MaterialisedView.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .column import Column  # noqa
from .schema import Schema  # noqa
