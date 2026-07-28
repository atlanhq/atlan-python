# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Union

from pydantic.v1 import Field, validator

from pyatlan.model.enums import SqlInsightJoinCardinality, SqlInsightJoinType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.model.structs import PopularityInsights, SqlInsightJoinColumnPair
from pyatlan.utils import init_guid, validate_required_fields

from .sql_insight import SqlInsight


class SqlInsightJoin(SqlInsight):
    """Description"""

    @staticmethod
    def generate_qualified_name(
        *,
        source_qualified_name: str,
        joined_qualified_name: str,
        column_pairs: List[Dict[str, str]],
        join_type: Union[SqlInsightJoinType, str] = SqlInsightJoinType.INNER,
    ) -> str:
        """
        Derive the deterministic qualifiedName for a SqlInsightJoin, identical to
        the SQL-Intelligence miner's formula — so a human-confirmed join and a
        later mined observation of the same join converge on one entity instead
        of duplicating:

        ``source_qn || '/join/' || md5(joined_qn || '|' || sorted_pairs || '|' || join_type)``

        where ``sorted_pairs`` joins ``SOURCE=JOINED`` bare column names with
        commas, ordered by source column.

        :param source_qualified_name: unique name of the source (left) dataset
        :param joined_qualified_name: unique name of the joined (right) dataset
        :param column_pairs: join keys as dicts with bare (unqualified) column
            names, e.g. ``[{"source_column": "ACCOUNT_ID", "joined_column": "ACCOUNTID"}]``
        :param join_type: type of the join (INNER, LEFT, RIGHT, FULL, CROSS)
        :returns: the deterministic qualifiedName for the join entity
        """
        join_type_value = (
            join_type.value
            if isinstance(join_type, SqlInsightJoinType)
            else str(join_type)
        )
        sorted_pairs = ",".join(
            f"{pair['source_column']}={pair['joined_column']}"
            for pair in sorted(column_pairs, key=lambda pair: pair["source_column"])
        )
        digest = hashlib.md5(  # noqa: S324 (miner-compatible identity, not crypto)
            f"{joined_qualified_name}|{sorted_pairs}|{join_type_value}".encode()
        ).hexdigest()
        return f"{source_qualified_name}/join/{digest}"

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        source_dataset: SQL,
        joined_dataset: SQL,
        column_pairs: List[Dict[str, str]],
        join_type: SqlInsightJoinType = SqlInsightJoinType.INNER,
        cardinality: SqlInsightJoinCardinality = SqlInsightJoinCardinality.MANY_TO_ONE,
        when_to_use: Optional[str] = None,
        name: Optional[str] = None,
    ) -> SqlInsightJoin:
        """
        Create a SqlInsightJoin between two SQL datasets, carrying both the
        string qualified-name attributes (read by metadata-lakehouse consumers)
        and the dataset relationship edges (rendered on the asset page) — plus a
        deterministic, miner-identical qualifiedName so repeated confirmation or
        a later mined observation converges on the same entity.

        :param source_dataset: source (left) dataset, e.g.
            ``Table.ref_by_qualified_name(...)`` or a search result — must carry
            its real type (Table / View / MaterialisedView) and qualifiedName
        :param joined_dataset: joined (right) dataset, same requirements
        :param column_pairs: join keys as dicts with bare (unqualified) column
            names, e.g. ``[{"source_column": "ACCOUNT_ID", "joined_column": "ACCOUNTID"}]``
        :param join_type: type of the join (defaults to INNER)
        :param cardinality: cardinality of the join (defaults to MANY_TO_ONE)
        :param when_to_use: optional guidance on when this join should be used
        :param name: optional display name (defaults to "<SOURCE> JOIN <JOINED>")
        :returns: the minimal request to create the SqlInsightJoin
        """
        attributes = SqlInsightJoin.Attributes.creator(
            source_dataset=source_dataset,
            joined_dataset=joined_dataset,
            column_pairs=column_pairs,
            join_type=join_type,
            cardinality=cardinality,
            when_to_use=when_to_use,
            name=name,
        )
        return cls(attributes=attributes)

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

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            source_dataset: SQL,
            joined_dataset: SQL,
            column_pairs: List[Dict[str, str]],
            join_type: SqlInsightJoinType = SqlInsightJoinType.INNER,
            cardinality: SqlInsightJoinCardinality = SqlInsightJoinCardinality.MANY_TO_ONE,
            when_to_use: Optional[str] = None,
            name: Optional[str] = None,
        ) -> SqlInsightJoin.Attributes:
            validate_required_fields(
                ["source_dataset", "joined_dataset", "column_pairs"],
                [source_dataset, joined_dataset, column_pairs],
            )
            source_qualified_name = source_dataset.qualified_name
            joined_qualified_name = joined_dataset.qualified_name
            validate_required_fields(
                ["source_dataset.qualified_name", "joined_dataset.qualified_name"],
                [source_qualified_name, joined_qualified_name],
            )
            for pair in column_pairs:
                if (
                    not isinstance(pair, dict)
                    or not pair.get("source_column")
                    or not pair.get("joined_column")
                ):
                    raise ValueError(
                        "each column pair must be a dict with non-empty "
                        "'source_column' and 'joined_column' bare column names"
                    )
            return SqlInsightJoin.Attributes(
                name=name
                or (
                    f"{source_qualified_name.rsplit('/', 1)[-1]} JOIN "  # type: ignore[union-attr]
                    f"{joined_qualified_name.rsplit('/', 1)[-1]}"  # type: ignore[union-attr]
                ),
                qualified_name=SqlInsightJoin.generate_qualified_name(
                    source_qualified_name=source_qualified_name,  # type: ignore[arg-type]
                    joined_qualified_name=joined_qualified_name,  # type: ignore[arg-type]
                    column_pairs=column_pairs,
                    join_type=join_type,
                ),
                sql_insight_join_source_dataset_qualified_name=source_qualified_name,
                sql_insight_join_joined_dataset_qualified_name=joined_qualified_name,
                sql_insight_join_type=join_type,
                sql_insight_join_cardinality=cardinality,
                sql_insight_join_when_to_use=when_to_use,
                sql_insight_join_column_pairs=[
                    SqlInsightJoinColumnPair(
                        sql_insight_join_column_pair_source_column_qualified_name=(
                            f"{source_qualified_name}/{pair['source_column']}"
                        ),
                        sql_insight_join_column_pair_joined_column_qualified_name=(
                            f"{joined_qualified_name}/{pair['joined_column']}"
                        ),
                    )
                    for pair in column_pairs
                ],
                # A human-declared join has no observed usage: never claim any.
                sql_insight_join_query_count=0,
                sql_insight_join_unique_users=0,
                sql_insight_source_dataset=source_dataset,
                sql_insight_joined_dataset=joined_dataset,
            )

    attributes: SqlInsightJoin.Attributes = Field(
        default_factory=lambda: SqlInsightJoin.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_q_l import SQL  # noqa: E402, F401
