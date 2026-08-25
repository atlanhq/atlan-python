# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import SnowflakeListingDistribution, SnowflakeListingState
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .core.snowflake import Snowflake


class SnowflakeListing(Snowflake):
    """Description"""

    type_name: str = Field(default="SnowflakeListing", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeListing":
            raise ValueError("must be SnowflakeListing")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeListing._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SNOWFLAKE_LISTING_TITLE: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingTitle", "snowflakeListingTitle"
    )
    """
    Snowflake's source-truthful title for the listing. Distinct from `name` (the non-human-readable Snowflake identifier).
    """  # noqa: E501
    SNOWFLAKE_LISTING_SUBTITLE: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingSubtitle", "snowflakeListingSubtitle"
    )
    """
    Marketplace subtitle of the listing.
    """
    SNOWFLAKE_LISTING_UNIFORM_LISTING_LOCATOR: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingUniformListingLocator", "snowflakeListingUniformListingLocator"
    )
    """
    Uniform Listing Locator (ULL) of the listing.
    """
    SNOWFLAKE_LISTING_STATE: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingState", "snowflakeListingState"
    )
    """
    Publication state of the listing.
    """
    SNOWFLAKE_LISTING_DISTRIBUTION: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingDistribution", "snowflakeListingDistribution"
    )
    """
    Distribution scope of the listing (organization-internal vs external marketplace/exchange).
    """
    SNOWFLAKE_LISTING_IS_SHARE: ClassVar[BooleanField] = BooleanField(
        "snowflakeListingIsShare", "snowflakeListingIsShare"
    )
    """
    Whether this listing wraps a data share (true) or not (false).
    """
    SNOWFLAKE_LISTING_IS_APPLICATION: ClassVar[BooleanField] = BooleanField(
        "snowflakeListingIsApplication", "snowflakeListingIsApplication"
    )
    """
    Whether this listing wraps a Snowflake Native App (true) or not (false).
    """
    SNOWFLAKE_LISTING_APPLICATION_PACKAGE: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingApplicationPackage", "snowflakeListingApplicationPackage"
    )
    """
    Application package name when this listing wraps a Native App.
    """
    SNOWFLAKE_LISTING_CATEGORIES: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingCategories", "snowflakeListingCategories"
    )
    """
    Discovery categories assigned to the listing.
    """
    SNOWFLAKE_LISTING_DATA_ATTRIBUTES: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingDataAttributes", "snowflakeListingDataAttributes"
    )
    """
    Data properties of the listing (refresh rate, history, freshness window) as a JSON blob emitted by Snowflake.
    """
    SNOWFLAKE_LISTING_TERMS: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingTerms", "snowflakeListingTerms"
    )
    """
    Terms of service for the listing.
    """
    SNOWFLAKE_LISTING_PROFILE: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingProfile", "snowflakeListingProfile"
    )
    """
    External Snowflake provider profile attached to the listing.
    """
    SNOWFLAKE_LISTING_SUPPORT_CONTACT: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingSupportContact", "snowflakeListingSupportContact"
    )
    """
    Contact info for the listing.
    """
    SNOWFLAKE_LISTING_RESHARING: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingResharing", "snowflakeListingResharing"
    )
    """
    Resharing configuration for the listing.
    """
    SNOWFLAKE_LISTING_AUTO_FULFILLMENT: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingAutoFulfillment", "snowflakeListingAutoFulfillment"
    )
    """
    Auto-fulfillment configuration for the listing.
    """
    SNOWFLAKE_LISTING_TARGETS: ClassVar[KeywordField] = KeywordField(
        "snowflakeListingTargets", "snowflakeListingTargets"
    )
    """
    Distribution targets of the listing (accounts, regions) as a JSON blob emitted by Snowflake.
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

    SNOWFLAKE_SHARES: ClassVar[RelationField] = RelationField("snowflakeShares")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "snowflake_listing_title",
        "snowflake_listing_subtitle",
        "snowflake_listing_uniform_listing_locator",
        "snowflake_listing_state",
        "snowflake_listing_distribution",
        "snowflake_listing_is_share",
        "snowflake_listing_is_application",
        "snowflake_listing_application_package",
        "snowflake_listing_categories",
        "snowflake_listing_data_attributes",
        "snowflake_listing_terms",
        "snowflake_listing_profile",
        "snowflake_listing_support_contact",
        "snowflake_listing_resharing",
        "snowflake_listing_auto_fulfillment",
        "snowflake_listing_targets",
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
        "snowflake_shares",
    ]

    @property
    def snowflake_listing_title(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.snowflake_listing_title
        )

    @snowflake_listing_title.setter
    def snowflake_listing_title(self, snowflake_listing_title: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_title = snowflake_listing_title

    @property
    def snowflake_listing_subtitle(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_subtitle
        )

    @snowflake_listing_subtitle.setter
    def snowflake_listing_subtitle(self, snowflake_listing_subtitle: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_subtitle = snowflake_listing_subtitle

    @property
    def snowflake_listing_uniform_listing_locator(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_uniform_listing_locator
        )

    @snowflake_listing_uniform_listing_locator.setter
    def snowflake_listing_uniform_listing_locator(
        self, snowflake_listing_uniform_listing_locator: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_uniform_listing_locator = (
            snowflake_listing_uniform_listing_locator
        )

    @property
    def snowflake_listing_state(self) -> Optional[SnowflakeListingState]:
        return (
            None if self.attributes is None else self.attributes.snowflake_listing_state
        )

    @snowflake_listing_state.setter
    def snowflake_listing_state(
        self, snowflake_listing_state: Optional[SnowflakeListingState]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_state = snowflake_listing_state

    @property
    def snowflake_listing_distribution(self) -> Optional[SnowflakeListingDistribution]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_distribution
        )

    @snowflake_listing_distribution.setter
    def snowflake_listing_distribution(
        self, snowflake_listing_distribution: Optional[SnowflakeListingDistribution]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_distribution = snowflake_listing_distribution

    @property
    def snowflake_listing_is_share(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_is_share
        )

    @snowflake_listing_is_share.setter
    def snowflake_listing_is_share(self, snowflake_listing_is_share: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_is_share = snowflake_listing_is_share

    @property
    def snowflake_listing_is_application(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_is_application
        )

    @snowflake_listing_is_application.setter
    def snowflake_listing_is_application(
        self, snowflake_listing_is_application: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_is_application = (
            snowflake_listing_is_application
        )

    @property
    def snowflake_listing_application_package(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_application_package
        )

    @snowflake_listing_application_package.setter
    def snowflake_listing_application_package(
        self, snowflake_listing_application_package: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_application_package = (
            snowflake_listing_application_package
        )

    @property
    def snowflake_listing_categories(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_categories
        )

    @snowflake_listing_categories.setter
    def snowflake_listing_categories(
        self, snowflake_listing_categories: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_categories = snowflake_listing_categories

    @property
    def snowflake_listing_data_attributes(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_data_attributes
        )

    @snowflake_listing_data_attributes.setter
    def snowflake_listing_data_attributes(
        self, snowflake_listing_data_attributes: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_data_attributes = (
            snowflake_listing_data_attributes
        )

    @property
    def snowflake_listing_terms(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.snowflake_listing_terms
        )

    @snowflake_listing_terms.setter
    def snowflake_listing_terms(self, snowflake_listing_terms: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_terms = snowflake_listing_terms

    @property
    def snowflake_listing_profile(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_profile
        )

    @snowflake_listing_profile.setter
    def snowflake_listing_profile(self, snowflake_listing_profile: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_profile = snowflake_listing_profile

    @property
    def snowflake_listing_support_contact(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_support_contact
        )

    @snowflake_listing_support_contact.setter
    def snowflake_listing_support_contact(
        self, snowflake_listing_support_contact: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_support_contact = (
            snowflake_listing_support_contact
        )

    @property
    def snowflake_listing_resharing(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_resharing
        )

    @snowflake_listing_resharing.setter
    def snowflake_listing_resharing(self, snowflake_listing_resharing: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_resharing = snowflake_listing_resharing

    @property
    def snowflake_listing_auto_fulfillment(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_auto_fulfillment
        )

    @snowflake_listing_auto_fulfillment.setter
    def snowflake_listing_auto_fulfillment(
        self, snowflake_listing_auto_fulfillment: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_auto_fulfillment = (
            snowflake_listing_auto_fulfillment
        )

    @property
    def snowflake_listing_targets(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.snowflake_listing_targets
        )

    @snowflake_listing_targets.setter
    def snowflake_listing_targets(self, snowflake_listing_targets: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_listing_targets = snowflake_listing_targets

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
    def snowflake_shares(self) -> Optional[List[SnowflakeShare]]:
        return None if self.attributes is None else self.attributes.snowflake_shares

    @snowflake_shares.setter
    def snowflake_shares(self, snowflake_shares: Optional[List[SnowflakeShare]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.snowflake_shares = snowflake_shares

    class Attributes(Snowflake.Attributes):
        snowflake_listing_title: Optional[str] = Field(default=None, description="")
        snowflake_listing_subtitle: Optional[str] = Field(default=None, description="")
        snowflake_listing_uniform_listing_locator: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_listing_state: Optional[SnowflakeListingState] = Field(
            default=None, description=""
        )
        snowflake_listing_distribution: Optional[SnowflakeListingDistribution] = Field(
            default=None, description=""
        )
        snowflake_listing_is_share: Optional[bool] = Field(default=None, description="")
        snowflake_listing_is_application: Optional[bool] = Field(
            default=None, description=""
        )
        snowflake_listing_application_package: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_listing_categories: Optional[Set[str]] = Field(
            default=None, description=""
        )
        snowflake_listing_data_attributes: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_listing_terms: Optional[str] = Field(default=None, description="")
        snowflake_listing_profile: Optional[str] = Field(default=None, description="")
        snowflake_listing_support_contact: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_listing_resharing: Optional[str] = Field(default=None, description="")
        snowflake_listing_auto_fulfillment: Optional[str] = Field(
            default=None, description=""
        )
        snowflake_listing_targets: Optional[str] = Field(default=None, description="")
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
        snowflake_shares: Optional[List[SnowflakeShare]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SnowflakeListing.Attributes = Field(
        default_factory=lambda: SnowflakeListing.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .snowflake_share import SnowflakeShare  # noqa: E402, F401

SnowflakeListing.Attributes.update_forward_refs()
