# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


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

from .snowflake import Snowflake


class SnowflakeV1CortexSearchService(Snowflake):
    """Description"""

    type_name: str = Field(
        default="SnowflakeV1CortexSearchService", allow_mutation=False
    )

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeV1CortexSearchService":
            raise ValueError("must be SnowflakeV1CortexSearchService")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeV1CortexSearchService._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SNOWFLAKE_V1CORTEX_SEARCH_SERVICE_EMBEDDING_MODEL: ClassVar[KeywordField] = (
        KeywordField(
            "snowflakeV1CortexSearchServiceEmbeddingModel",
            "snowflakeV1CortexSearchServiceEmbeddingModel",
        )
    )
    """
    Embedding model used by this search service (for example, snowflake-arctic-embed-m, voyage-multilingual-2).
    """
    SNOWFLAKE_V1CORTEX_SEARCH_SERVICE_INDEXED_COLUMNS: ClassVar[KeywordField] = (
        KeywordField(
            "snowflakeV1CortexSearchServiceIndexedColumns",
            "snowflakeV1CortexSearchServiceIndexedColumns",
        )
    )
    """
    Columns of the base table that are indexed for retrieval by this search service.
    """
    SNOWFLAKE_V1CORTEX_SEARCH_SERVICE_LAST_REFRESH_AT: ClassVar[NumericField] = (
        NumericField(
            "snowflakeV1CortexSearchServiceLastRefreshAt",
            "snowflakeV1CortexSearchServiceLastRefreshAt",
        )
    )
    """
    Time (epoch) at which the search index was last refreshed, in milliseconds.
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
    SQL_COALESCE_LAST_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "sqlCoalesceLastRunStatus", "sqlCoalesceLastRunStatus"
    )
    """
    Status of the Coalesce run. One of: success, failure, cancelled, or skipped.
    """
    SQL_COALESCE_NODE_STATUS: ClassVar[KeywordField] = KeywordField(
        "sqlCoalesceNodeStatus", "sqlCoalesceNodeStatus"
    )
    """
    Status of the Coalesce node for a given run.
    """
    SQL_COALESCE_LAST_RUN_AT: ClassVar[NumericField] = NumericField(
        "sqlCoalesceLastRunAt", "sqlCoalesceLastRunAt"
    )
    """
    Time (epoch) at which the Coalesce node that materialized this asset last ran, in milliseconds.
    """
    SQL_COALESCE_NODE_TYPE: ClassVar[KeywordField] = KeywordField(
        "sqlCoalesceNodeType", "sqlCoalesceNodeType"
    )
    """
    Type of the Coalesce node.
    """
    SQL_COALESCE_ENVIRONMENT_ID: ClassVar[KeywordField] = KeywordField(
        "sqlCoalesceEnvironmentId", "sqlCoalesceEnvironmentId"
    )
    """
    Identifier of the Coalesce environment.
    """
    SQL_COALESCE_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sqlCoalesceEnvironmentName",
        "sqlCoalesceEnvironmentName.keyword",
        "sqlCoalesceEnvironmentName",
    )
    """
    Name of the Coalesce environment.
    """
    SQL_COALESCE_PROJECT_ID: ClassVar[KeywordField] = KeywordField(
        "sqlCoalesceProjectId", "sqlCoalesceProjectId"
    )
    """
    Identifier of the Coalesce project.
    """
    SQL_COALESCE_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sqlCoalesceProjectName",
        "sqlCoalesceProjectName.keyword",
        "sqlCoalesceProjectName",
    )
    """
    Name of the Coalesce project.
    """
    SQL_SHARE_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "sqlShareQualifiedNames", "sqlShareQualifiedNames"
    )
    """
    Qualified names of data shares this asset is granted to.
    """
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
    """

    SNOWFLAKE_SNOWFLAKE_CORTEX_SEARCH_SERVICES: ClassVar[RelationField] = RelationField(
        "snowflakeSnowflakeCortexSearchServices"
    )
    """
    TBC
    """
    SNOWFLAKE_CORTEX_SEARCH_SERVICE_SCHEMA: ClassVar[RelationField] = RelationField(
        "snowflakeCortexSearchServiceSchema"
    )
    """
    TBC
    """
    SNOWFLAKE_CORTEX_SEARCH_SERVICE: ClassVar[RelationField] = RelationField(
        "snowflakeCortexSearchService"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "snowflake_v1_cortex_search_service_embedding_model",
        "snowflake_v1_cortex_search_service_indexed_columns",
        "snowflake_v1_cortex_search_service_last_refresh_at",
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
        "sql_coalesce_last_run_status",
        "sql_coalesce_node_status",
        "sql_coalesce_last_run_at",
        "sql_coalesce_node_type",
        "sql_coalesce_environment_id",
        "sql_coalesce_environment_name",
        "sql_coalesce_project_id",
        "sql_coalesce_project_name",
        "sql_share_qualified_names",
        "catalog_dataset_guid",
        "snowflake_snowflake_cortex_search_services",
        "snowflake_cortex_search_service_schema",
        "snowflake_cortex_search_service",
    ]

    @property
    def snowflake_v1_cortex_search_service_embedding_model(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_v1_cortex_search_service_embedding_model
        )

    @snowflake_v1_cortex_search_service_embedding_model.setter
    def snowflake_v1_cortex_search_service_embedding_model(
        self, snowflake_v1_cortex_search_service_embedding_model: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_v1_cortex_search_service_embedding_model = (
            snowflake_v1_cortex_search_service_embedding_model
        )

    @property
    def snowflake_v1_cortex_search_service_indexed_columns(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_v1_cortex_search_service_indexed_columns
        )

    @snowflake_v1_cortex_search_service_indexed_columns.setter
    def snowflake_v1_cortex_search_service_indexed_columns(
        self, snowflake_v1_cortex_search_service_indexed_columns: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_v1_cortex_search_service_indexed_columns = (
            snowflake_v1_cortex_search_service_indexed_columns
        )

    @property
    def snowflake_v1_cortex_search_service_last_refresh_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_v1_cortex_search_service_last_refresh_at
        )

    @snowflake_v1_cortex_search_service_last_refresh_at.setter
    def snowflake_v1_cortex_search_service_last_refresh_at(
        self, snowflake_v1_cortex_search_service_last_refresh_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_v1_cortex_search_service_last_refresh_at = (
            snowflake_v1_cortex_search_service_last_refresh_at
        )

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
    def sql_coalesce_last_run_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_coalesce_last_run_status
        )

    @sql_coalesce_last_run_status.setter
    def sql_coalesce_last_run_status(self, sql_coalesce_last_run_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_last_run_status = sql_coalesce_last_run_status

    @property
    def sql_coalesce_node_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_coalesce_node_status
        )

    @sql_coalesce_node_status.setter
    def sql_coalesce_node_status(self, sql_coalesce_node_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_node_status = sql_coalesce_node_status

    @property
    def sql_coalesce_last_run_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_coalesce_last_run_at
        )

    @sql_coalesce_last_run_at.setter
    def sql_coalesce_last_run_at(self, sql_coalesce_last_run_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_last_run_at = sql_coalesce_last_run_at

    @property
    def sql_coalesce_node_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sql_coalesce_node_type
        )

    @sql_coalesce_node_type.setter
    def sql_coalesce_node_type(self, sql_coalesce_node_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_node_type = sql_coalesce_node_type

    @property
    def sql_coalesce_environment_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_coalesce_environment_id
        )

    @sql_coalesce_environment_id.setter
    def sql_coalesce_environment_id(self, sql_coalesce_environment_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_environment_id = sql_coalesce_environment_id

    @property
    def sql_coalesce_environment_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_coalesce_environment_name
        )

    @sql_coalesce_environment_name.setter
    def sql_coalesce_environment_name(
        self, sql_coalesce_environment_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_environment_name = sql_coalesce_environment_name

    @property
    def sql_coalesce_project_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sql_coalesce_project_id
        )

    @sql_coalesce_project_id.setter
    def sql_coalesce_project_id(self, sql_coalesce_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_project_id = sql_coalesce_project_id

    @property
    def sql_coalesce_project_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_coalesce_project_name
        )

    @sql_coalesce_project_name.setter
    def sql_coalesce_project_name(self, sql_coalesce_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_coalesce_project_name = sql_coalesce_project_name

    @property
    def sql_share_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_share_qualified_names
        )

    @sql_share_qualified_names.setter
    def sql_share_qualified_names(self, sql_share_qualified_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_share_qualified_names = sql_share_qualified_names

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

    @property
    def snowflake_snowflake_cortex_search_services(self) -> Optional[Table]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_snowflake_cortex_search_services
        )

    @snowflake_snowflake_cortex_search_services.setter
    def snowflake_snowflake_cortex_search_services(
        self, snowflake_snowflake_cortex_search_services: Optional[Table]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_snowflake_cortex_search_services = (
            snowflake_snowflake_cortex_search_services
        )

    @property
    def snowflake_cortex_search_service_schema(self) -> Optional[Schema]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_cortex_search_service_schema
        )

    @snowflake_cortex_search_service_schema.setter
    def snowflake_cortex_search_service_schema(
        self, snowflake_cortex_search_service_schema: Optional[Schema]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_cortex_search_service_schema = (
            snowflake_cortex_search_service_schema
        )

    @property
    def snowflake_cortex_search_service(self) -> Optional[SnowflakeV1CortexAgentTool]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_cortex_search_service
        )

    @snowflake_cortex_search_service.setter
    def snowflake_cortex_search_service(
        self, snowflake_cortex_search_service: Optional[SnowflakeV1CortexAgentTool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_cortex_search_service = (
            snowflake_cortex_search_service
        )

    class Attributes(Snowflake.Attributes):
        snowflake_v1_cortex_search_service_embedding_model: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_v1_cortex_search_service_indexed_columns: Optional[Set[str]] = Field(
            default=None, description=""
        )
        snowflake_v1_cortex_search_service_last_refresh_at: Optional[datetime] = Field(
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
        sql_coalesce_last_run_status: Optional[str] = Field(
            default=None, description=""
        )
        sql_coalesce_node_status: Optional[str] = Field(default=None, description="")
        sql_coalesce_last_run_at: Optional[datetime] = Field(
            default=None, description=""
        )
        sql_coalesce_node_type: Optional[str] = Field(default=None, description="")
        sql_coalesce_environment_id: Optional[str] = Field(default=None, description="")
        sql_coalesce_environment_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_coalesce_project_id: Optional[str] = Field(default=None, description="")
        sql_coalesce_project_name: Optional[str] = Field(default=None, description="")
        sql_share_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
        snowflake_snowflake_cortex_search_services: Optional[Table] = Field(
            default=None, description=""
        )  # relationship
        snowflake_cortex_search_service_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        snowflake_cortex_search_service: Optional[SnowflakeV1CortexAgentTool] = Field(
            default=None, description=""
        )  # relationship

    attributes: SnowflakeV1CortexSearchService.Attributes = Field(
        default_factory=lambda: SnowflakeV1CortexSearchService.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .schema import Schema  # noqa: E402, F401
from .snowflake_v1_cortex_agent_tool import (
    SnowflakeV1CortexAgentTool,  # noqa: E402, F401
)
from .table import Table  # noqa: E402, F401
