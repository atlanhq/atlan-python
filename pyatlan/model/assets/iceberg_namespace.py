# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


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
)

from .core.schema import Schema


class IcebergNamespace(Schema):
    """Description"""

    type_name: str = Field(default="IcebergNamespace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "IcebergNamespace":
            raise ValueError("must be IcebergNamespace")
        return v

    def __setattr__(self, name, value):
        if name in IcebergNamespace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TABLE_COUNT: ClassVar[NumericField] = NumericField("tableCount", "tableCount")
    """
    Number of tables in this schema.
    """
    SCHEMA_EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "schemaExternalLocation", "schemaExternalLocation"
    )
    """
    External location of this schema, for example: an S3 object location.
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
    SQL_AI_MODEL_CONTEXT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sqlAIModelContextQualifiedName", "sqlAIModelContextQualifiedName"
    )
    """
    Unique name of the context in which the model versions exist, or empty if it does not exist within an AI model context.
    """  # noqa: E501
    SQL_IS_SECURE: ClassVar[BooleanField] = BooleanField("sqlIsSecure", "sqlIsSecure")
    """
    Whether this asset is secure (true) or not (false).
    """
    SQL_HAS_AI_INSIGHTS: ClassVar[BooleanField] = BooleanField(
        "sqlHasAiInsights", "sqlHasAiInsights"
    )
    """
    Whether this asset has any AI insights data available.
    """
    SQL_AI_INSIGHTS_LAST_ANALYZED_AT: ClassVar[NumericField] = NumericField(
        "sqlAiInsightsLastAnalyzedAt", "sqlAiInsightsLastAnalyzedAt"
    )
    """
    Time (epoch) at which this asset was last analyzed for AI insights, in milliseconds.
    """
    SQL_AI_INSIGHTS_POPULAR_BUSINESS_QUESTION_COUNT: ClassVar[NumericField] = (
        NumericField(
            "sqlAiInsightsPopularBusinessQuestionCount",
            "sqlAiInsightsPopularBusinessQuestionCount",
        )
    )
    """
    Number of popular business questions associated with this asset.
    """
    SQL_AI_INSIGHTS_POPULAR_JOIN_COUNT: ClassVar[NumericField] = NumericField(
        "sqlAiInsightsPopularJoinCount", "sqlAiInsightsPopularJoinCount"
    )
    """
    Number of popular join patterns associated with this asset.
    """
    SQL_AI_INSIGHTS_POPULAR_FILTER_COUNT: ClassVar[NumericField] = NumericField(
        "sqlAiInsightsPopularFilterCount", "sqlAiInsightsPopularFilterCount"
    )
    """
    Number of popular filter patterns associated with this asset.
    """
    SQL_AI_INSIGHTS_RELATIONSHIP_COUNT: ClassVar[NumericField] = NumericField(
        "sqlAiInsightsRelationshipCount", "sqlAiInsightsRelationshipCount"
    )
    """
    Number of relationship insights associated with this asset.
    """
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
    """
    ICEBERG_PARENT_NAMESPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "icebergParentNamespaceQualifiedName", "icebergParentNamespaceQualifiedName"
    )
    """
    Unique name of the immediate parent namespace in which this asset exists.
    """
    ICEBERG_NAMESPACE_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "icebergNamespaceHierarchy", "icebergNamespaceHierarchy"
    )
    """
    Ordered array of namespace assets with qualified name and name representing the complete namespace hierarchy path for this asset, from immediate parent to root namespace.
    """  # noqa: E501

    ICEBERG_PARENT_NAMESPACE: ClassVar[RelationField] = RelationField(
        "icebergParentNamespace"
    )
    """
    TBC
    """
    ICEBERG_SUB_NAMESPACES: ClassVar[RelationField] = RelationField(
        "icebergSubNamespaces"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "table_count",
        "schema_external_location",
        "views_count",
        "linked_schema_qualified_name",
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
        "sql_a_i_model_context_qualified_name",
        "sql_is_secure",
        "sql_has_ai_insights",
        "sql_ai_insights_last_analyzed_at",
        "sql_ai_insights_popular_business_question_count",
        "sql_ai_insights_popular_join_count",
        "sql_ai_insights_popular_filter_count",
        "sql_ai_insights_relationship_count",
        "catalog_dataset_guid",
        "iceberg_parent_namespace_qualified_name",
        "iceberg_namespace_hierarchy",
        "iceberg_parent_namespace",
        "iceberg_sub_namespaces",
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
    def schema_external_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_external_location
        )

    @schema_external_location.setter
    def schema_external_location(self, schema_external_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_external_location = schema_external_location

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
    def sql_a_i_model_context_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_a_i_model_context_qualified_name
        )

    @sql_a_i_model_context_qualified_name.setter
    def sql_a_i_model_context_qualified_name(
        self, sql_a_i_model_context_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_a_i_model_context_qualified_name = (
            sql_a_i_model_context_qualified_name
        )

    @property
    def sql_is_secure(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.sql_is_secure

    @sql_is_secure.setter
    def sql_is_secure(self, sql_is_secure: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_is_secure = sql_is_secure

    @property
    def sql_has_ai_insights(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.sql_has_ai_insights

    @sql_has_ai_insights.setter
    def sql_has_ai_insights(self, sql_has_ai_insights: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_has_ai_insights = sql_has_ai_insights

    @property
    def sql_ai_insights_last_analyzed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_ai_insights_last_analyzed_at
        )

    @sql_ai_insights_last_analyzed_at.setter
    def sql_ai_insights_last_analyzed_at(
        self, sql_ai_insights_last_analyzed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_ai_insights_last_analyzed_at = (
            sql_ai_insights_last_analyzed_at
        )

    @property
    def sql_ai_insights_popular_business_question_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_ai_insights_popular_business_question_count
        )

    @sql_ai_insights_popular_business_question_count.setter
    def sql_ai_insights_popular_business_question_count(
        self, sql_ai_insights_popular_business_question_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_ai_insights_popular_business_question_count = (
            sql_ai_insights_popular_business_question_count
        )

    @property
    def sql_ai_insights_popular_join_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_ai_insights_popular_join_count
        )

    @sql_ai_insights_popular_join_count.setter
    def sql_ai_insights_popular_join_count(
        self, sql_ai_insights_popular_join_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_ai_insights_popular_join_count = (
            sql_ai_insights_popular_join_count
        )

    @property
    def sql_ai_insights_popular_filter_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_ai_insights_popular_filter_count
        )

    @sql_ai_insights_popular_filter_count.setter
    def sql_ai_insights_popular_filter_count(
        self, sql_ai_insights_popular_filter_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_ai_insights_popular_filter_count = (
            sql_ai_insights_popular_filter_count
        )

    @property
    def sql_ai_insights_relationship_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_ai_insights_relationship_count
        )

    @sql_ai_insights_relationship_count.setter
    def sql_ai_insights_relationship_count(
        self, sql_ai_insights_relationship_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_ai_insights_relationship_count = (
            sql_ai_insights_relationship_count
        )

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

    @property
    def iceberg_parent_namespace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_parent_namespace_qualified_name
        )

    @iceberg_parent_namespace_qualified_name.setter
    def iceberg_parent_namespace_qualified_name(
        self, iceberg_parent_namespace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_parent_namespace_qualified_name = (
            iceberg_parent_namespace_qualified_name
        )

    @property
    def iceberg_namespace_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_namespace_hierarchy
        )

    @iceberg_namespace_hierarchy.setter
    def iceberg_namespace_hierarchy(
        self, iceberg_namespace_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_namespace_hierarchy = iceberg_namespace_hierarchy

    @property
    def iceberg_parent_namespace(self) -> Optional[IcebergNamespace]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_parent_namespace
        )

    @iceberg_parent_namespace.setter
    def iceberg_parent_namespace(
        self, iceberg_parent_namespace: Optional[IcebergNamespace]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_parent_namespace = iceberg_parent_namespace

    @property
    def iceberg_sub_namespaces(self) -> Optional[List[IcebergNamespace]]:
        return (
            None if self.attributes is None else self.attributes.iceberg_sub_namespaces
        )

    @iceberg_sub_namespaces.setter
    def iceberg_sub_namespaces(
        self, iceberg_sub_namespaces: Optional[List[IcebergNamespace]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_sub_namespaces = iceberg_sub_namespaces

    class Attributes(Schema.Attributes):
        table_count: Optional[int] = Field(default=None, description="")
        schema_external_location: Optional[str] = Field(default=None, description="")
        views_count: Optional[int] = Field(default=None, description="")
        linked_schema_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
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
        sql_a_i_model_context_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_is_secure: Optional[bool] = Field(default=None, description="")
        sql_has_ai_insights: Optional[bool] = Field(default=None, description="")
        sql_ai_insights_last_analyzed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        sql_ai_insights_popular_business_question_count: Optional[int] = Field(
            default=None, description=""
        )
        sql_ai_insights_popular_join_count: Optional[int] = Field(
            default=None, description=""
        )
        sql_ai_insights_popular_filter_count: Optional[int] = Field(
            default=None, description=""
        )
        sql_ai_insights_relationship_count: Optional[int] = Field(
            default=None, description=""
        )
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
        iceberg_parent_namespace_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        iceberg_namespace_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        iceberg_parent_namespace: Optional[IcebergNamespace] = Field(
            default=None, description=""
        )  # relationship
        iceberg_sub_namespaces: Optional[List[IcebergNamespace]] = Field(
            default=None, description=""
        )  # relationship

    attributes: IcebergNamespace.Attributes = Field(
        default_factory=lambda: IcebergNamespace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


IcebergNamespace.Attributes.update_forward_refs()
