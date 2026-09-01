# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
from datetime import datetime
from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.model.structs import PopularityInsights
from pyatlan.utils import init_guid, validate_required_fields

from .sql_insight import SqlInsight


class SqlInsightFilter(SqlInsight):
    """Description"""

    @staticmethod
    def generate_qualified_name(*, column_qualified_name: str, operator: str) -> str:
        """
        Derive the deterministic qualifiedName for a SqlInsightFilter, identical to
        the SQL-Intelligence miner's formula — so a human-confirmed filter and a
        later mined observation of the same filter converge on one entity instead
        of duplicating:

        ``column_qn || '/filter/' || md5(operator)``

        Note this hangs off the COLUMN, not the dataset: filters sit one level
        deeper than joins and business questions.

        :param column_qualified_name: unique name of the column being filtered
        :param operator: the filter operator, e.g. ``IN``, ``=``, ``BETWEEN``
        :returns: the deterministic qualifiedName for the filter entity
        """
        digest = hashlib.md5(  # noqa: S324 (miner-compatible identity, not crypto)
            operator.encode()
        ).hexdigest()
        return f"{column_qualified_name}/filter/{digest}"

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        column: Column,
        operator: str,
        predicate_sql: Optional[str] = None,
        when_to_use: Optional[str] = None,
        common_values: Optional[Set[str]] = None,
        name: Optional[str] = None,
    ) -> SqlInsightFilter:
        """
        Create a SqlInsightFilter on a column, carrying both the string
        qualified-name attributes (the dataset attribute is how the asset page's
        Usage & Intelligence tab finds filters) and the column relationship edge —
        plus a deterministic, miner-identical qualifiedName so repeated
        confirmation or a later mined observation converges on the same entity.

        :param column: the column being filtered, e.g.
            ``Column.ref_by_qualified_name(...)`` or a search result — must carry
            its qualifiedName
        :param operator: the filter operator, e.g. ``IN``, ``=``, ``BETWEEN``.
            The qualifiedName is derived from this, so two filters on the same
            column with the same operator are ONE entity
        :param predicate_sql: optional SQL predicate the filter applies
        :param when_to_use: optional guidance on when this filter should be used
        :param common_values: optional set of values commonly filtered on
        :param name: optional display name (defaults to "<COLUMN> <OPERATOR>")
        :returns: the minimal request to create the SqlInsightFilter
        """
        attributes = SqlInsightFilter.Attributes.creator(
            column=column,
            operator=operator,
            predicate_sql=predicate_sql,
            when_to_use=when_to_use,
            common_values=common_values,
            name=name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="SqlInsightFilter", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SqlInsightFilter":
            raise ValueError("must be SqlInsightFilter")
        return v

    def __setattr__(self, name, value):
        if name in SqlInsightFilter._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SQL_INSIGHT_FILTER_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sqlInsightFilterDatasetQualifiedName", "sqlInsightFilterDatasetQualifiedName"
    )
    """
    Qualified name of the dataset containing the filtered column.
    """
    SQL_INSIGHT_FILTER_COLUMN_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sqlInsightFilterColumnQualifiedName", "sqlInsightFilterColumnQualifiedName"
    )
    """
    Qualified name of the filtered column.
    """
    SQL_INSIGHT_FILTER_COMMON_VALUES: ClassVar[KeywordField] = KeywordField(
        "sqlInsightFilterCommonValues", "sqlInsightFilterCommonValues"
    )
    """
    Common values observed for this filter.
    """
    SQL_INSIGHT_FILTER_OPERATOR: ClassVar[KeywordField] = KeywordField(
        "sqlInsightFilterOperator", "sqlInsightFilterOperator"
    )
    """
    SQL operator observed on this column, such as =, !=, IN, LIKE.
    """
    SQL_INSIGHT_FILTER_PREDICATE_SQL: ClassVar[KeywordField] = KeywordField(
        "sqlInsightFilterPredicateSQL", "sqlInsightFilterPredicateSQL"
    )
    """
    SQL predicate expression for this filter pattern.
    """
    SQL_INSIGHT_FILTER_WHEN_TO_USE: ClassVar[KeywordField] = KeywordField(
        "sqlInsightFilterWhenToUse", "sqlInsightFilterWhenToUse"
    )
    """
    Guidance on when this filter pattern should be used.
    """
    SQL_INSIGHT_FILTER_QUERY_COUNT: ClassVar[NumericField] = NumericField(
        "sqlInsightFilterQueryCount", "sqlInsightFilterQueryCount"
    )
    """
    Number of queries that use this filter pattern.
    """
    SQL_INSIGHT_FILTER_UNIQUE_USERS: ClassVar[NumericField] = NumericField(
        "sqlInsightFilterUniqueUsers", "sqlInsightFilterUniqueUsers"
    )
    """
    Number of unique users who have used this filter pattern.
    """
    SQL_INSIGHT_FILTER_LAST_SEEN_AT: ClassVar[NumericField] = NumericField(
        "sqlInsightFilterLastSeenAt", "sqlInsightFilterLastSeenAt"
    )
    """
    Time (epoch) at which this filter pattern was last observed, in milliseconds.
    """
    SQL_INSIGHT_FILTER_EXAMPLE_QUERIES: ClassVar[KeywordField] = KeywordField(
        "sqlInsightFilterExampleQueries", "sqlInsightFilterExampleQueries"
    )
    """
    Example SQL queries that demonstrate this filter pattern, with usage details.
    """

    SQL_INSIGHT_COLUMN: ClassVar[RelationField] = RelationField("sqlInsightColumn")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sql_insight_filter_dataset_qualified_name",
        "sql_insight_filter_column_qualified_name",
        "sql_insight_filter_common_values",
        "sql_insight_filter_operator",
        "sql_insight_filter_predicate_s_q_l",
        "sql_insight_filter_when_to_use",
        "sql_insight_filter_query_count",
        "sql_insight_filter_unique_users",
        "sql_insight_filter_last_seen_at",
        "sql_insight_filter_example_queries",
        "sql_insight_column",
    ]

    @property
    def sql_insight_filter_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_dataset_qualified_name
        )

    @sql_insight_filter_dataset_qualified_name.setter
    def sql_insight_filter_dataset_qualified_name(
        self, sql_insight_filter_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_dataset_qualified_name = (
            sql_insight_filter_dataset_qualified_name
        )

    @property
    def sql_insight_filter_column_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_column_qualified_name
        )

    @sql_insight_filter_column_qualified_name.setter
    def sql_insight_filter_column_qualified_name(
        self, sql_insight_filter_column_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_column_qualified_name = (
            sql_insight_filter_column_qualified_name
        )

    @property
    def sql_insight_filter_common_values(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_common_values
        )

    @sql_insight_filter_common_values.setter
    def sql_insight_filter_common_values(
        self, sql_insight_filter_common_values: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_common_values = (
            sql_insight_filter_common_values
        )

    @property
    def sql_insight_filter_operator(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_operator
        )

    @sql_insight_filter_operator.setter
    def sql_insight_filter_operator(self, sql_insight_filter_operator: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_operator = sql_insight_filter_operator

    @property
    def sql_insight_filter_predicate_s_q_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_predicate_s_q_l
        )

    @sql_insight_filter_predicate_s_q_l.setter
    def sql_insight_filter_predicate_s_q_l(
        self, sql_insight_filter_predicate_s_q_l: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_predicate_s_q_l = (
            sql_insight_filter_predicate_s_q_l
        )

    @property
    def sql_insight_filter_when_to_use(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_when_to_use
        )

    @sql_insight_filter_when_to_use.setter
    def sql_insight_filter_when_to_use(
        self, sql_insight_filter_when_to_use: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_when_to_use = sql_insight_filter_when_to_use

    @property
    def sql_insight_filter_query_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_query_count
        )

    @sql_insight_filter_query_count.setter
    def sql_insight_filter_query_count(
        self, sql_insight_filter_query_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_query_count = sql_insight_filter_query_count

    @property
    def sql_insight_filter_unique_users(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_unique_users
        )

    @sql_insight_filter_unique_users.setter
    def sql_insight_filter_unique_users(
        self, sql_insight_filter_unique_users: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_unique_users = (
            sql_insight_filter_unique_users
        )

    @property
    def sql_insight_filter_last_seen_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_last_seen_at
        )

    @sql_insight_filter_last_seen_at.setter
    def sql_insight_filter_last_seen_at(
        self, sql_insight_filter_last_seen_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_last_seen_at = (
            sql_insight_filter_last_seen_at
        )

    @property
    def sql_insight_filter_example_queries(self) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_filter_example_queries
        )

    @sql_insight_filter_example_queries.setter
    def sql_insight_filter_example_queries(
        self, sql_insight_filter_example_queries: Optional[List[PopularityInsights]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_filter_example_queries = (
            sql_insight_filter_example_queries
        )

    @property
    def sql_insight_column(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.sql_insight_column

    @sql_insight_column.setter
    def sql_insight_column(self, sql_insight_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_column = sql_insight_column

    class Attributes(SqlInsight.Attributes):
        sql_insight_filter_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_filter_column_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_filter_common_values: Optional[Set[str]] = Field(
            default=None, description=""
        )
        sql_insight_filter_operator: Optional[str] = Field(default=None, description="")
        sql_insight_filter_predicate_s_q_l: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_filter_when_to_use: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_filter_query_count: Optional[int] = Field(
            default=None, description=""
        )
        sql_insight_filter_unique_users: Optional[int] = Field(
            default=None, description=""
        )
        sql_insight_filter_last_seen_at: Optional[datetime] = Field(
            default=None, description=""
        )
        sql_insight_filter_example_queries: Optional[List[PopularityInsights]] = Field(
            default=None, description=""
        )
        sql_insight_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            column: Column,
            operator: str,
            predicate_sql: Optional[str] = None,
            when_to_use: Optional[str] = None,
            common_values: Optional[Set[str]] = None,
            name: Optional[str] = None,
        ) -> SqlInsightFilter.Attributes:
            validate_required_fields(["column", "operator"], [column, operator])
            column_qualified_name = column.qualified_name
            validate_required_fields(["column.qualified_name"], [column_qualified_name])
            # A filter's qualifiedName is <columnQN>/filter/md5(operator), and a
            # column's own qualifiedName is <datasetQN>/<column>. So the dataset is
            # the column's parent, never a separate input that could disagree with it.
            dataset_qualified_name = column_qualified_name.rsplit("/", 1)[0]  # type: ignore[union-attr]
            return SqlInsightFilter.Attributes(
                name=name
                or f"{column_qualified_name.rsplit('/', 1)[-1]} {operator}",  # type: ignore[union-attr]
                qualified_name=SqlInsightFilter.generate_qualified_name(
                    column_qualified_name=column_qualified_name,  # type: ignore[arg-type]
                    operator=operator,
                ),
                # Both are load-bearing: the Usage & Intelligence tab finds filters by
                # the dataset ATTRIBUTE, while the column RELATIONSHIP is what renders
                # the row on the column itself. A filter missing either is half-visible.
                sql_insight_filter_dataset_qualified_name=dataset_qualified_name,
                sql_insight_filter_column_qualified_name=column_qualified_name,
                sql_insight_filter_operator=operator,
                sql_insight_filter_predicate_s_q_l=predicate_sql,
                sql_insight_filter_when_to_use=when_to_use,
                sql_insight_filter_common_values=common_values,
                # A human-declared filter has no observed usage: never claim any.
                sql_insight_filter_query_count=0,
                sql_insight_filter_unique_users=0,
                sql_insight_column=column,
            )

    attributes: SqlInsightFilter.Attributes = Field(
        default_factory=lambda: SqlInsightFilter.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .column import Column  # noqa: E402, F401
