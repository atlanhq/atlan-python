# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import SqlInsightJoinCardinality, SqlInsightJoinType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.model.structs import PopularityInsights, SqlInsightJoinColumnPair

from .sql_insight import SqlInsight


class SqlInsightJoin(SqlInsight):
    """Description"""

    type_name: str = Field(default="SqlInsightJoin", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SqlInsightJoin":
            raise ValueError("must be SqlInsightJoin")
        return v

    def __setattr__(self, name, value):
        if name in SqlInsightJoin._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SQL_INSIGHT_JOIN_SOURCE_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "sqlInsightJoinSourceDatasetQualifiedName",
            "sqlInsightJoinSourceDatasetQualifiedName",
        )
    )
    """
    Qualified name of the source dataset in this join pattern.
    """
    SQL_INSIGHT_JOIN_JOINED_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "sqlInsightJoinJoinedDatasetQualifiedName",
            "sqlInsightJoinJoinedDatasetQualifiedName",
        )
    )
    """
    Qualified name of the joined dataset in this join pattern.
    """
    SQL_INSIGHT_JOIN_TYPE: ClassVar[KeywordField] = KeywordField(
        "sqlInsightJoinType", "sqlInsightJoinType"
    )
    """
    Type of SQL join observed in this pattern.
    """
    SQL_INSIGHT_JOIN_CARDINALITY: ClassVar[KeywordField] = KeywordField(
        "sqlInsightJoinCardinality", "sqlInsightJoinCardinality"
    )
    """
    Observed cardinality of the join relationship.
    """
    SQL_INSIGHT_JOIN_WHEN_TO_USE: ClassVar[KeywordField] = KeywordField(
        "sqlInsightJoinWhenToUse", "sqlInsightJoinWhenToUse"
    )
    """
    Guidance on when this join pattern should be used.
    """
    SQL_INSIGHT_JOIN_COLUMN_PAIRS: ClassVar[KeywordField] = KeywordField(
        "sqlInsightJoinColumnPairs", "sqlInsightJoinColumnPairs"
    )
    """
    Column mappings in this join, pairing source columns to joined columns.
    """
    SQL_INSIGHT_JOIN_QUERY_COUNT: ClassVar[NumericField] = NumericField(
        "sqlInsightJoinQueryCount", "sqlInsightJoinQueryCount"
    )
    """
    Number of queries that use this join pattern.
    """
    SQL_INSIGHT_JOIN_UNIQUE_USERS: ClassVar[NumericField] = NumericField(
        "sqlInsightJoinUniqueUsers", "sqlInsightJoinUniqueUsers"
    )
    """
    Number of unique users who have used this join pattern.
    """
    SQL_INSIGHT_JOIN_LAST_SEEN_AT: ClassVar[NumericField] = NumericField(
        "sqlInsightJoinLastSeenAt", "sqlInsightJoinLastSeenAt"
    )
    """
    Time (epoch) at which this join pattern was last observed, in milliseconds.
    """
    SQL_INSIGHT_JOIN_EXAMPLE_QUERIES: ClassVar[KeywordField] = KeywordField(
        "sqlInsightJoinExampleQueries", "sqlInsightJoinExampleQueries"
    )
    """
    Example SQL queries that demonstrate this join pattern, with usage details.
    """

    SQL_INSIGHT_SOURCE_DATASET: ClassVar[RelationField] = RelationField(
        "sqlInsightSourceDataset"
    )
    """
    TBC
    """
    SQL_INSIGHT_JOINED_DATASET: ClassVar[RelationField] = RelationField(
        "sqlInsightJoinedDataset"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sql_insight_join_source_dataset_qualified_name",
        "sql_insight_join_joined_dataset_qualified_name",
        "sql_insight_join_type",
        "sql_insight_join_cardinality",
        "sql_insight_join_when_to_use",
        "sql_insight_join_column_pairs",
        "sql_insight_join_query_count",
        "sql_insight_join_unique_users",
        "sql_insight_join_last_seen_at",
        "sql_insight_join_example_queries",
        "sql_insight_source_dataset",
        "sql_insight_joined_dataset",
    ]

    @property
    def sql_insight_join_source_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_source_dataset_qualified_name
        )

    @sql_insight_join_source_dataset_qualified_name.setter
    def sql_insight_join_source_dataset_qualified_name(
        self, sql_insight_join_source_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_source_dataset_qualified_name = (
            sql_insight_join_source_dataset_qualified_name
        )

    @property
    def sql_insight_join_joined_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_joined_dataset_qualified_name
        )

    @sql_insight_join_joined_dataset_qualified_name.setter
    def sql_insight_join_joined_dataset_qualified_name(
        self, sql_insight_join_joined_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_joined_dataset_qualified_name = (
            sql_insight_join_joined_dataset_qualified_name
        )

    @property
    def sql_insight_join_type(self) -> Optional[SqlInsightJoinType]:
        return (
            None if self.attributes is None else self.attributes.sql_insight_join_type
        )

    @sql_insight_join_type.setter
    def sql_insight_join_type(
        self, sql_insight_join_type: Optional[SqlInsightJoinType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_type = sql_insight_join_type

    @property
    def sql_insight_join_cardinality(self) -> Optional[SqlInsightJoinCardinality]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_cardinality
        )

    @sql_insight_join_cardinality.setter
    def sql_insight_join_cardinality(
        self, sql_insight_join_cardinality: Optional[SqlInsightJoinCardinality]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_cardinality = sql_insight_join_cardinality

    @property
    def sql_insight_join_when_to_use(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_when_to_use
        )

    @sql_insight_join_when_to_use.setter
    def sql_insight_join_when_to_use(self, sql_insight_join_when_to_use: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_when_to_use = sql_insight_join_when_to_use

    @property
    def sql_insight_join_column_pairs(self) -> Optional[List[SqlInsightJoinColumnPair]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_column_pairs
        )

    @sql_insight_join_column_pairs.setter
    def sql_insight_join_column_pairs(
        self, sql_insight_join_column_pairs: Optional[List[SqlInsightJoinColumnPair]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_column_pairs = sql_insight_join_column_pairs

    @property
    def sql_insight_join_query_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_query_count
        )

    @sql_insight_join_query_count.setter
    def sql_insight_join_query_count(self, sql_insight_join_query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_query_count = sql_insight_join_query_count

    @property
    def sql_insight_join_unique_users(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_unique_users
        )

    @sql_insight_join_unique_users.setter
    def sql_insight_join_unique_users(
        self, sql_insight_join_unique_users: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_unique_users = sql_insight_join_unique_users

    @property
    def sql_insight_join_last_seen_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_last_seen_at
        )

    @sql_insight_join_last_seen_at.setter
    def sql_insight_join_last_seen_at(
        self, sql_insight_join_last_seen_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_last_seen_at = sql_insight_join_last_seen_at

    @property
    def sql_insight_join_example_queries(self) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_join_example_queries
        )

    @sql_insight_join_example_queries.setter
    def sql_insight_join_example_queries(
        self, sql_insight_join_example_queries: Optional[List[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_join_example_queries = (
            sql_insight_join_example_queries
        )

    @property
    def sql_insight_source_dataset(self) -> Optional[SQL]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_source_dataset
        )

    @sql_insight_source_dataset.setter
    def sql_insight_source_dataset(self, sql_insight_source_dataset: Optional[SQL]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_source_dataset = sql_insight_source_dataset

    @property
    def sql_insight_joined_dataset(self) -> Optional[SQL]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_joined_dataset
        )

    @sql_insight_joined_dataset.setter
    def sql_insight_joined_dataset(self, sql_insight_joined_dataset: Optional[SQL]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_joined_dataset = sql_insight_joined_dataset

    class Attributes(SqlInsight.Attributes):
        sql_insight_join_source_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_join_joined_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_join_type: Optional[SqlInsightJoinType] = Field(
            default=None, description=""
        )
        sql_insight_join_cardinality: Optional[SqlInsightJoinCardinality] = Field(
            default=None, description=""
        )
        sql_insight_join_when_to_use: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_join_column_pairs: Optional[List[SqlInsightJoinColumnPair]] = Field(
            default=None, description=""
        )
        sql_insight_join_query_count: Optional[int] = Field(
            default=None, description=""
        )
        sql_insight_join_unique_users: Optional[int] = Field(
            default=None, description=""
        )
        sql_insight_join_last_seen_at: Optional[datetime] = Field(
            default=None, description=""
        )
        sql_insight_join_example_queries: Optional[List[PopularityInsights]] = Field(
            default=None, description=""
        )
        sql_insight_source_dataset: Optional[SQL] = Field(
            default=None, description=""
        )  # relationship
        sql_insight_joined_dataset: Optional[SQL] = Field(
            default=None, description=""
        )  # relationship

    attributes: SqlInsightJoin.Attributes = Field(
        default_factory=lambda: SqlInsightJoin.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_q_l import SQL  # noqa: E402, F401
