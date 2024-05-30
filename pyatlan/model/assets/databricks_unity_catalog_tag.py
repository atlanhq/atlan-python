# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.model.structs import SourceTagAttribute

from .tag import Tag


class DatabricksUnityCatalogTag(Tag):
    """Description"""

    type_name: str = Field(default="DatabricksUnityCatalogTag", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DatabricksUnityCatalogTag":
            raise ValueError("must be DatabricksUnityCatalogTag")
        return v

    def __setattr__(self, name, value):
        if name in DatabricksUnityCatalogTag._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TAG_ID: ClassVar[KeywordField] = KeywordField("tagId", "tagId")
    """
    Unique identifier of the tag in the source system.
    """
    TAG_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "tagAttributes", "tagAttributes"
    )
    """
    Attributes associated with the tag in the source system.
    """
    TAG_ALLOWED_VALUES: ClassVar[KeywordTextField] = KeywordTextField(
        "tagAllowedValues", "tagAllowedValues", "tagAllowedValues.text"
    )
    """
    Allowed values for the tag in the source system. These are denormalized from tagAttributes for ease of querying.
    """
    MAPPED_CLASSIFICATION_NAME: ClassVar[KeywordField] = KeywordField(
        "mappedClassificationName", "mappedClassificationName"
    )
    """
    Name of the classification in Atlan that is mapped to this tag.
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
    SQL_DBT_MODELS: ClassVar[RelationField] = RelationField("sqlDbtModels")
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
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "tag_id",
        "tag_attributes",
        "tag_allowed_values",
        "mapped_atlan_tag_name",
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
        "sql_dbt_models",
        "sql_dbt_sources",
        "dbt_models",
        "dbt_tests",
    ]

    @property
    def tag_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tag_id

    @tag_id.setter
    def tag_id(self, tag_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_id = tag_id

    @property
    def tag_attributes(self) -> Optional[List[SourceTagAttribute]]:
        return None if self.attributes is None else self.attributes.tag_attributes

    @tag_attributes.setter
    def tag_attributes(self, tag_attributes: Optional[List[SourceTagAttribute]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_attributes = tag_attributes

    @property
    def tag_allowed_values(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.tag_allowed_values

    @tag_allowed_values.setter
    def tag_allowed_values(self, tag_allowed_values: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_allowed_values = tag_allowed_values

    @property
    def mapped_atlan_tag_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mapped_atlan_tag_name
        )

    @mapped_atlan_tag_name.setter
    def mapped_atlan_tag_name(self, mapped_atlan_tag_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mapped_atlan_tag_name = mapped_atlan_tag_name

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
    def sql_dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.sql_dbt_models

    @sql_dbt_models.setter
    def sql_dbt_models(self, sql_dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_models = sql_dbt_models

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
    def dbt_tests(self) -> Optional[List[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[List[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    class Attributes(Tag.Attributes):
        tag_id: Optional[str] = Field(default=None, description="")
        tag_attributes: Optional[List[SourceTagAttribute]] = Field(
            default=None, description=""
        )
        tag_allowed_values: Optional[Set[str]] = Field(default=None, description="")
        mapped_atlan_tag_name: Optional[str] = Field(default=None, description="")
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
        sql_dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[List[DbtTest]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DatabricksUnityCatalogTag.Attributes = Field(
        default_factory=lambda: DatabricksUnityCatalogTag.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dbt_model import DbtModel  # noqa
from .dbt_source import DbtSource  # noqa
from .dbt_test import DbtTest  # noqa
