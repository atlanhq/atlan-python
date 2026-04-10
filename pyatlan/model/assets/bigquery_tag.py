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
from pyatlan.model.structs import SourceTagAttribute

from .core.tag import Tag


class BigqueryTag(Tag):
    """Description"""

    type_name: str = Field(default="BigqueryTag", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BigqueryTag":
            raise ValueError("must be BigqueryTag")
        return v

    def __setattr__(self, name, value):
        if name in BigqueryTag._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BIGQUERY_TAG_TYPE: ClassVar[KeywordField] = KeywordField(
        "bigqueryTagType", "bigqueryTagType"
    )
    """
    The specific type or category of the Bigquery tag, which can be used for classification and organization of Bigquery assets.
    """  # noqa: E501
    BIGQUERY_TAG_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "bigqueryTagHierarchy", "bigqueryTagHierarchy"
    )
    """
    List of top-level upstream nested bigquery tags.
    """
    BIGQUERY_TAG_TAXONOMY_PROPERTIES: ClassVar[KeywordField] = KeywordField(
        "bigqueryTagTaxonomyProperties", "bigqueryTagTaxonomyProperties"
    )
    """
    Properties of the bigquery tag taxonomy attribute.
    """
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
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
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

    DBT_SOURCES: ClassVar[RelationField] = RelationField("dbtSources")
    """
    TBC
    """
    SNOWFLAKE_SEMANTIC_LOGICAL_TABLES: ClassVar[RelationField] = RelationField(
        "snowflakeSemanticLogicalTables"
    )
    """
    TBC
    """
    SQL_DBT_MODELS: ClassVar[RelationField] = RelationField("sqlDbtModels")
    """
    TBC
    """
    SQL_INSIGHT_INCOMING_JOINS: ClassVar[RelationField] = RelationField(
        "sqlInsightIncomingJoins"
    )
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    SQL_INSIGHT_BUSINESS_QUESTIONS: ClassVar[RelationField] = RelationField(
        "sqlInsightBusinessQuestions"
    )
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
    DBT_SEED_ASSETS: ClassVar[RelationField] = RelationField("dbtSeedAssets")
    """
    TBC
    """
    SQL_INSIGHT_OUTGOING_JOINS: ClassVar[RelationField] = RelationField(
        "sqlInsightOutgoingJoins"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "bigquery_tag_type",
        "bigquery_tag_hierarchy",
        "bigquery_tag_taxonomy_properties",
        "tag_id",
        "tag_attributes",
        "tag_allowed_values",
        "mapped_atlan_tag_name",
        "catalog_dataset_guid",
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
        "dbt_sources",
        "snowflake_semantic_logical_tables",
        "sql_dbt_models",
        "sql_insight_incoming_joins",
        "dbt_tests",
        "sql_insight_business_questions",
        "sql_dbt_sources",
        "dbt_models",
        "dbt_seed_assets",
        "sql_insight_outgoing_joins",
    ]

    @property
    def bigquery_tag_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.bigquery_tag_type

    @bigquery_tag_type.setter
    def bigquery_tag_type(self, bigquery_tag_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_tag_type = bigquery_tag_type

    @property
    def bigquery_tag_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.bigquery_tag_hierarchy
        )

    @bigquery_tag_hierarchy.setter
    def bigquery_tag_hierarchy(
        self, bigquery_tag_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_tag_hierarchy = bigquery_tag_hierarchy

    @property
    def bigquery_tag_taxonomy_properties(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.bigquery_tag_taxonomy_properties
        )

    @bigquery_tag_taxonomy_properties.setter
    def bigquery_tag_taxonomy_properties(
        self, bigquery_tag_taxonomy_properties: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_tag_taxonomy_properties = (
            bigquery_tag_taxonomy_properties
        )

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
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

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
    def dbt_sources(self) -> Optional[List[DbtSource]]:
        return None if self.attributes is None else self.attributes.dbt_sources

    @dbt_sources.setter
    def dbt_sources(self, dbt_sources: Optional[List[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_sources = dbt_sources

    @property
    def snowflake_semantic_logical_tables(
        self,
    ) -> Optional[List[SnowflakeSemanticLogicalTable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_semantic_logical_tables
        )

    @snowflake_semantic_logical_tables.setter
    def snowflake_semantic_logical_tables(
        self,
        snowflake_semantic_logical_tables: Optional[
            List[SnowflakeSemanticLogicalTable]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_semantic_logical_tables = (
            snowflake_semantic_logical_tables
        )

    @property
    def sql_dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.sql_dbt_models

    @sql_dbt_models.setter
    def sql_dbt_models(self, sql_dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_models = sql_dbt_models

    @property
    def sql_insight_incoming_joins(self) -> Optional[List[SqlInsightJoin]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_incoming_joins
        )

    @sql_insight_incoming_joins.setter
    def sql_insight_incoming_joins(
        self, sql_insight_incoming_joins: Optional[List[SqlInsightJoin]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_incoming_joins = sql_insight_incoming_joins

    @property
    def dbt_tests(self) -> Optional[List[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[List[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def sql_insight_business_questions(
        self,
    ) -> Optional[List[SqlInsightBusinessQuestion]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_questions
        )

    @sql_insight_business_questions.setter
    def sql_insight_business_questions(
        self, sql_insight_business_questions: Optional[List[SqlInsightBusinessQuestion]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_questions = sql_insight_business_questions

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
    def dbt_seed_assets(self) -> Optional[List[DbtSeed]]:
        return None if self.attributes is None else self.attributes.dbt_seed_assets

    @dbt_seed_assets.setter
    def dbt_seed_assets(self, dbt_seed_assets: Optional[List[DbtSeed]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_seed_assets = dbt_seed_assets

    @property
    def sql_insight_outgoing_joins(self) -> Optional[List[SqlInsightJoin]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_outgoing_joins
        )

    @sql_insight_outgoing_joins.setter
    def sql_insight_outgoing_joins(
        self, sql_insight_outgoing_joins: Optional[List[SqlInsightJoin]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_outgoing_joins = sql_insight_outgoing_joins

    class Attributes(Tag.Attributes):
        bigquery_tag_type: Optional[str] = Field(default=None, description="")
        bigquery_tag_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        bigquery_tag_taxonomy_properties: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        tag_id: Optional[str] = Field(default=None, description="")
        tag_attributes: Optional[List[SourceTagAttribute]] = Field(
            default=None, description=""
        )
        tag_allowed_values: Optional[Set[str]] = Field(default=None, description="")
        mapped_atlan_tag_name: Optional[str] = Field(default=None, description="")
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
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
        dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        snowflake_semantic_logical_tables: Optional[
            List[SnowflakeSemanticLogicalTable]
        ] = Field(default=None, description="")  # relationship
        sql_dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        sql_insight_incoming_joins: Optional[List[SqlInsightJoin]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[List[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        sql_insight_business_questions: Optional[List[SqlInsightBusinessQuestion]] = (
            Field(default=None, description="")
        )  # relationship
        sql_dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_seed_assets: Optional[List[DbtSeed]] = Field(
            default=None, description=""
        )  # relationship
        sql_insight_outgoing_joins: Optional[List[SqlInsightJoin]] = Field(
            default=None, description=""
        )  # relationship

    attributes: BigqueryTag.Attributes = Field(
        default_factory=lambda: BigqueryTag.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.dbt_model import DbtModel  # noqa: E402, F401
from .core.dbt_seed import DbtSeed  # noqa: E402, F401
from .core.dbt_source import DbtSource  # noqa: E402, F401
from .core.dbt_test import DbtTest  # noqa: E402, F401
from .core.snowflake_semantic_logical_table import (
    SnowflakeSemanticLogicalTable,  # noqa: E402, F401
)
from .core.sql_insight_business_question import (
    SqlInsightBusinessQuestion,  # noqa: E402, F401
)
from .core.sql_insight_join import SqlInsightJoin  # noqa: E402, F401

BigqueryTag.Attributes.update_forward_refs()
