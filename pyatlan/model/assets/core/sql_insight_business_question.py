# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.model.structs import PopularityInsights
from pyatlan.utils import init_guid, validate_required_fields

from .sql_insight import SqlInsight


class SqlInsightBusinessQuestion(SqlInsight):
    """Description"""

    @staticmethod
    def generate_qualified_name(
        *, dataset_qualified_name: str, question_text: str
    ) -> str:
        """
        Derive the deterministic qualifiedName for a SqlInsightBusinessQuestion,
        identical to the SQL-Intelligence miner's formula — so a human-confirmed
        question and a later mined observation of the same question converge on
        one entity instead of duplicating:

        ``dataset_qn || '/question/' || md5(question_text)``

        The hash is over the question TEXT alone, so rewording a question makes a
        new entity rather than updating the old one.

        :param dataset_qualified_name: unique name of the dataset the question is about
        :param question_text: the business question, verbatim
        :returns: the deterministic qualifiedName for the business-question entity
        """
        digest = hashlib.md5(  # noqa: S324 (miner-compatible identity, not crypto)
            question_text.encode()
        ).hexdigest()
        return f"{dataset_qualified_name}/question/{digest}"

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        dataset: SQL,
        question_text: str,
        canonical_sql: Optional[str] = None,
        name: Optional[str] = None,
    ) -> SqlInsightBusinessQuestion:
        """
        Create a SqlInsightBusinessQuestion against a SQL dataset, carrying both
        the string qualified-name attribute and the dataset relationship edge —
        plus a deterministic, miner-identical qualifiedName so repeated
        confirmation or a later mined observation converges on the same entity.

        :param dataset: the dataset the question is about, e.g.
            ``Table.ref_by_qualified_name(...)`` or a search result — must carry
            its real type (Table / View / MaterialisedView) and qualifiedName
        :param question_text: the business question, verbatim. The qualifiedName is
            derived from this, so rewording it creates a NEW entity
        :param canonical_sql: optional SQL that answers the question
        :param name: optional display name (defaults to the question text)
        :returns: the minimal request to create the SqlInsightBusinessQuestion
        """
        attributes = SqlInsightBusinessQuestion.Attributes.creator(
            dataset=dataset,
            question_text=question_text,
            canonical_sql=canonical_sql,
            name=name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="SqlInsightBusinessQuestion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SqlInsightBusinessQuestion":
            raise ValueError("must be SqlInsightBusinessQuestion")
        return v

    def __setattr__(self, name, value):
        if name in SqlInsightBusinessQuestion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SQL_INSIGHT_BUSINESS_QUESTION_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "sqlInsightBusinessQuestionDatasetQualifiedName",
            "sqlInsightBusinessQuestionDatasetQualifiedName",
        )
    )
    """
    Qualified name of the dataset this business question relates to.
    """
    SQL_INSIGHT_BUSINESS_QUESTION_TEXT: ClassVar[KeywordField] = KeywordField(
        "sqlInsightBusinessQuestionText", "sqlInsightBusinessQuestionText"
    )
    """
    Natural language text of the business question.
    """
    SQL_INSIGHT_BUSINESS_QUESTION_CANONICAL_SQL: ClassVar[KeywordField] = KeywordField(
        "sqlInsightBusinessQuestionCanonicalSQL",
        "sqlInsightBusinessQuestionCanonicalSQL",
    )
    """
    Canonical SQL query that answers this business question.
    """
    SQL_INSIGHT_BUSINESS_QUESTION_QUERY_COUNT: ClassVar[NumericField] = NumericField(
        "sqlInsightBusinessQuestionQueryCount", "sqlInsightBusinessQuestionQueryCount"
    )
    """
    Number of queries associated with this business question.
    """
    SQL_INSIGHT_BUSINESS_QUESTION_UNIQUE_USERS: ClassVar[NumericField] = NumericField(
        "sqlInsightBusinessQuestionUniqueUsers", "sqlInsightBusinessQuestionUniqueUsers"
    )
    """
    Number of unique users who have asked this question.
    """
    SQL_INSIGHT_BUSINESS_QUESTION_LAST_SEEN_AT: ClassVar[NumericField] = NumericField(
        "sqlInsightBusinessQuestionLastSeenAt", "sqlInsightBusinessQuestionLastSeenAt"
    )
    """
    Time (epoch) at which this question was last observed, in milliseconds.
    """
    SQL_INSIGHT_BUSINESS_QUESTION_EXAMPLE_QUERIES: ClassVar[KeywordField] = (
        KeywordField(
            "sqlInsightBusinessQuestionExampleQueries",
            "sqlInsightBusinessQuestionExampleQueries",
        )
    )
    """
    Example SQL queries that demonstrate this business question, with usage details.
    """

    SQL_INSIGHT_DATASET: ClassVar[RelationField] = RelationField("sqlInsightDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sql_insight_business_question_dataset_qualified_name",
        "sql_insight_business_question_text",
        "sql_insight_business_question_canonical_s_q_l",
        "sql_insight_business_question_query_count",
        "sql_insight_business_question_unique_users",
        "sql_insight_business_question_last_seen_at",
        "sql_insight_business_question_example_queries",
        "sql_insight_dataset",
    ]

    @property
    def sql_insight_business_question_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_question_dataset_qualified_name
        )

    @sql_insight_business_question_dataset_qualified_name.setter
    def sql_insight_business_question_dataset_qualified_name(
        self, sql_insight_business_question_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_question_dataset_qualified_name = (
            sql_insight_business_question_dataset_qualified_name
        )

    @property
    def sql_insight_business_question_text(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_question_text
        )

    @sql_insight_business_question_text.setter
    def sql_insight_business_question_text(
        self, sql_insight_business_question_text: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_question_text = (
            sql_insight_business_question_text
        )

    @property
    def sql_insight_business_question_canonical_s_q_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_question_canonical_s_q_l
        )

    @sql_insight_business_question_canonical_s_q_l.setter
    def sql_insight_business_question_canonical_s_q_l(
        self, sql_insight_business_question_canonical_s_q_l: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_question_canonical_s_q_l = (
            sql_insight_business_question_canonical_s_q_l
        )

    @property
    def sql_insight_business_question_query_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_question_query_count
        )

    @sql_insight_business_question_query_count.setter
    def sql_insight_business_question_query_count(
        self, sql_insight_business_question_query_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_question_query_count = (
            sql_insight_business_question_query_count
        )

    @property
    def sql_insight_business_question_unique_users(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_question_unique_users
        )

    @sql_insight_business_question_unique_users.setter
    def sql_insight_business_question_unique_users(
        self, sql_insight_business_question_unique_users: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_question_unique_users = (
            sql_insight_business_question_unique_users
        )

    @property
    def sql_insight_business_question_last_seen_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_question_last_seen_at
        )

    @sql_insight_business_question_last_seen_at.setter
    def sql_insight_business_question_last_seen_at(
        self, sql_insight_business_question_last_seen_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_question_last_seen_at = (
            sql_insight_business_question_last_seen_at
        )

    @property
    def sql_insight_business_question_example_queries(
        self,
    ) -> Optional[List[PopularityInsights]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sql_insight_business_question_example_queries
        )

    @sql_insight_business_question_example_queries.setter
    def sql_insight_business_question_example_queries(
        self,
        sql_insight_business_question_example_queries: Optional[
            List[PopularityInsights]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_business_question_example_queries = (
            sql_insight_business_question_example_queries
        )

    @property
    def sql_insight_dataset(self) -> Optional[SQL]:
        return None if self.attributes is None else self.attributes.sql_insight_dataset

    @sql_insight_dataset.setter
    def sql_insight_dataset(self, sql_insight_dataset: Optional[SQL]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_insight_dataset = sql_insight_dataset

    class Attributes(SqlInsight.Attributes):
        sql_insight_business_question_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_business_question_text: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_business_question_canonical_s_q_l: Optional[str] = Field(
            default=None, description=""
        )
        sql_insight_business_question_query_count: Optional[int] = Field(
            default=None, description=""
        )
        sql_insight_business_question_unique_users: Optional[int] = Field(
            default=None, description=""
        )
        sql_insight_business_question_last_seen_at: Optional[datetime] = Field(
            default=None, description=""
        )
        sql_insight_business_question_example_queries: Optional[
            List[PopularityInsights]
        ] = Field(default=None, description="")
        sql_insight_dataset: Optional[SQL] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            dataset: SQL,
            question_text: str,
            canonical_sql: Optional[str] = None,
            name: Optional[str] = None,
        ) -> SqlInsightBusinessQuestion.Attributes:
            validate_required_fields(
                ["dataset", "question_text"], [dataset, question_text]
            )
            dataset_qualified_name = dataset.qualified_name
            validate_required_fields(
                ["dataset.qualified_name"], [dataset_qualified_name]
            )
            return SqlInsightBusinessQuestion.Attributes(
                name=name or question_text,
                qualified_name=SqlInsightBusinessQuestion.generate_qualified_name(
                    dataset_qualified_name=dataset_qualified_name,  # type: ignore[arg-type]
                    question_text=question_text,
                ),
                sql_insight_business_question_dataset_qualified_name=dataset_qualified_name,
                sql_insight_business_question_text=question_text,
                sql_insight_business_question_canonical_s_q_l=canonical_sql,
                # A human-declared question has no observed usage: never claim any.
                sql_insight_business_question_query_count=0,
                sql_insight_business_question_unique_users=0,
                sql_insight_dataset=dataset,
            )

    attributes: SqlInsightBusinessQuestion.Attributes = Field(
        default_factory=lambda: SqlInsightBusinessQuestion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_q_l import SQL  # noqa: E402, F401
