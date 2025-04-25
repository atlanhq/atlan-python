# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)

from .cassandra import Cassandra


class CassandraView(Cassandra):
    """Description"""

    type_name: str = Field(default="CassandraView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CassandraView":
            raise ValueError("must be CassandraView")
        return v

    def __setattr__(self, name, value):
        if name in CassandraView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CASSANDRA_VIEW_TABLE_ID: ClassVar[KeywordField] = KeywordField(
        "cassandraViewTableId", "cassandraViewTableId"
    )
    """
    ID of the base table in the CassandraView.
    """
    CASSANDRA_VIEW_BLOOM_FILTER_FP_CHANCE: ClassVar[NumericField] = NumericField(
        "cassandraViewBloomFilterFPChance", "cassandraViewBloomFilterFPChance"
    )
    """
    False positive chance for the Bloom filter in the CassandraView.
    """
    CASSANDRA_VIEW_CACHING: ClassVar[KeywordField] = KeywordField(
        "cassandraViewCaching", "cassandraViewCaching"
    )
    """
    Caching configuration in the CassandraView.
    """
    CASSANDRA_VIEW_COMMENT: ClassVar[KeywordField] = KeywordField(
        "cassandraViewComment", "cassandraViewComment"
    )
    """
    Comment describing the CassandraView.
    """
    CASSANDRA_VIEW_COMPACTION: ClassVar[KeywordField] = KeywordField(
        "cassandraViewCompaction", "cassandraViewCompaction"
    )
    """
    Compaction for the CassandraView.
    """
    CASSANDRA_VIEW_CRC_CHECK_CHANCE: ClassVar[NumericField] = NumericField(
        "cassandraViewCRCCheckChance", "cassandraViewCRCCheckChance"
    )
    """
    CRC check chance for the CassandraView.
    """
    CASSANDRA_VIEW_DC_LOCAL_READ_REPAIR_CHANCE: ClassVar[NumericField] = NumericField(
        "cassandraViewDCLocalReadRepairChance", "cassandraViewDCLocalReadRepairChance"
    )
    """
    DC-local read repair chance for the CassandraView.
    """
    CASSANDRA_VIEW_DEFAULT_TTL: ClassVar[NumericField] = NumericField(
        "cassandraViewDefaultTTL", "cassandraViewDefaultTTL"
    )
    """
    Default time-to-live (TTL) for the CassandraView.
    """
    CASSANDRA_VIEW_GC_GRACE_SECONDS: ClassVar[NumericField] = NumericField(
        "cassandraViewGCGraceSeconds", "cassandraViewGCGraceSeconds"
    )
    """
    Grace period for garbage collection in the CassandraView.
    """
    CASSANDRA_VIEW_INCLUDE_ALL_COLUMNS: ClassVar[BooleanField] = BooleanField(
        "cassandraViewIncludeAllColumns", "cassandraViewIncludeAllColumns"
    )
    """
    Whether to include all columns in the CassandraView.
    """
    CASSANDRA_VIEW_MAX_INDEX_INTERVAL: ClassVar[NumericField] = NumericField(
        "cassandraViewMaxIndexInterval", "cassandraViewMaxIndexInterval"
    )
    """
    Maximum index interval for the CassandraView.
    """
    CASSANDRA_VIEW_MEMBTABLE_FLUSH_PERIOD_IN_MS: ClassVar[NumericField] = NumericField(
        "cassandraViewMembtableFlushPeriodInMS", "cassandraViewMembtableFlushPeriodInMS"
    )
    """
    Memtable flush period (in milliseconds) for the CassandraView.
    """
    CASSANDRA_VIEW_MIN_INDEX_INTERVAL: ClassVar[NumericField] = NumericField(
        "cassandraViewMinIndexInterval", "cassandraViewMinIndexInterval"
    )
    """
    Minimum index interval for the CassandraView.
    """
    CASSANDRA_VIEW_READ_REPAIR_INTERVAL: ClassVar[NumericField] = NumericField(
        "cassandraViewReadRepairInterval", "cassandraViewReadRepairInterval"
    )
    """
    Read repair interval for the CassandraView.
    """
    CASSANDRA_VIEW_QUERY: ClassVar[KeywordField] = KeywordField(
        "cassandraViewQuery", "cassandraViewQuery"
    )
    """
    Query used in the CassandraView.
    """
    CASSANDRA_VIEW_WHERE_CLAUSE: ClassVar[KeywordField] = KeywordField(
        "cassandraViewWhereClause", "cassandraViewWhereClause"
    )
    """
    Where clause used for the CassandraView query.
    """
    CASSANDRA_VIEW_SPECULATIVE_RETRY: ClassVar[KeywordField] = KeywordField(
        "cassandraViewSpeculativeRetry", "cassandraViewSpeculativeRetry"
    )
    """
    SpeculativeRetry setting for the CassandraView.
    """

    CASSANDRA_KEYSPACE: ClassVar[RelationField] = RelationField("cassandraKeyspace")
    """
    TBC
    """
    CASSANDRA_COLUMNS: ClassVar[RelationField] = RelationField("cassandraColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cassandra_view_table_id",
        "cassandra_view_bloom_filter_f_p_chance",
        "cassandra_view_caching",
        "cassandra_view_comment",
        "cassandra_view_compaction",
        "cassandra_view_c_r_c_check_chance",
        "cassandra_view_d_c_local_read_repair_chance",
        "cassandra_view_default_t_t_l",
        "cassandra_view_g_c_grace_seconds",
        "cassandra_view_include_all_columns",
        "cassandra_view_max_index_interval",
        "cassandra_view_membtable_flush_period_in_m_s",
        "cassandra_view_min_index_interval",
        "cassandra_view_read_repair_interval",
        "cassandra_view_query",
        "cassandra_view_where_clause",
        "cassandra_view_speculative_retry",
        "cassandra_keyspace",
        "cassandra_columns",
    ]

    @property
    def cassandra_view_table_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_view_table_id
        )

    @cassandra_view_table_id.setter
    def cassandra_view_table_id(self, cassandra_view_table_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_table_id = cassandra_view_table_id

    @property
    def cassandra_view_bloom_filter_f_p_chance(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_bloom_filter_f_p_chance
        )

    @cassandra_view_bloom_filter_f_p_chance.setter
    def cassandra_view_bloom_filter_f_p_chance(
        self, cassandra_view_bloom_filter_f_p_chance: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_bloom_filter_f_p_chance = (
            cassandra_view_bloom_filter_f_p_chance
        )

    @property
    def cassandra_view_caching(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.cassandra_view_caching
        )

    @cassandra_view_caching.setter
    def cassandra_view_caching(self, cassandra_view_caching: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_caching = cassandra_view_caching

    @property
    def cassandra_view_comment(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_view_comment
        )

    @cassandra_view_comment.setter
    def cassandra_view_comment(self, cassandra_view_comment: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_comment = cassandra_view_comment

    @property
    def cassandra_view_compaction(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_compaction
        )

    @cassandra_view_compaction.setter
    def cassandra_view_compaction(
        self, cassandra_view_compaction: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_compaction = cassandra_view_compaction

    @property
    def cassandra_view_c_r_c_check_chance(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_c_r_c_check_chance
        )

    @cassandra_view_c_r_c_check_chance.setter
    def cassandra_view_c_r_c_check_chance(
        self, cassandra_view_c_r_c_check_chance: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_c_r_c_check_chance = (
            cassandra_view_c_r_c_check_chance
        )

    @property
    def cassandra_view_d_c_local_read_repair_chance(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_d_c_local_read_repair_chance
        )

    @cassandra_view_d_c_local_read_repair_chance.setter
    def cassandra_view_d_c_local_read_repair_chance(
        self, cassandra_view_d_c_local_read_repair_chance: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_d_c_local_read_repair_chance = (
            cassandra_view_d_c_local_read_repair_chance
        )

    @property
    def cassandra_view_default_t_t_l(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_default_t_t_l
        )

    @cassandra_view_default_t_t_l.setter
    def cassandra_view_default_t_t_l(self, cassandra_view_default_t_t_l: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_default_t_t_l = cassandra_view_default_t_t_l

    @property
    def cassandra_view_g_c_grace_seconds(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_g_c_grace_seconds
        )

    @cassandra_view_g_c_grace_seconds.setter
    def cassandra_view_g_c_grace_seconds(
        self, cassandra_view_g_c_grace_seconds: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_g_c_grace_seconds = (
            cassandra_view_g_c_grace_seconds
        )

    @property
    def cassandra_view_include_all_columns(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_include_all_columns
        )

    @cassandra_view_include_all_columns.setter
    def cassandra_view_include_all_columns(
        self, cassandra_view_include_all_columns: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_include_all_columns = (
            cassandra_view_include_all_columns
        )

    @property
    def cassandra_view_max_index_interval(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_max_index_interval
        )

    @cassandra_view_max_index_interval.setter
    def cassandra_view_max_index_interval(
        self, cassandra_view_max_index_interval: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_max_index_interval = (
            cassandra_view_max_index_interval
        )

    @property
    def cassandra_view_membtable_flush_period_in_m_s(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_membtable_flush_period_in_m_s
        )

    @cassandra_view_membtable_flush_period_in_m_s.setter
    def cassandra_view_membtable_flush_period_in_m_s(
        self, cassandra_view_membtable_flush_period_in_m_s: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_membtable_flush_period_in_m_s = (
            cassandra_view_membtable_flush_period_in_m_s
        )

    @property
    def cassandra_view_min_index_interval(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_min_index_interval
        )

    @cassandra_view_min_index_interval.setter
    def cassandra_view_min_index_interval(
        self, cassandra_view_min_index_interval: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_min_index_interval = (
            cassandra_view_min_index_interval
        )

    @property
    def cassandra_view_read_repair_interval(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_read_repair_interval
        )

    @cassandra_view_read_repair_interval.setter
    def cassandra_view_read_repair_interval(
        self, cassandra_view_read_repair_interval: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_read_repair_interval = (
            cassandra_view_read_repair_interval
        )

    @property
    def cassandra_view_query(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cassandra_view_query

    @cassandra_view_query.setter
    def cassandra_view_query(self, cassandra_view_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_query = cassandra_view_query

    @property
    def cassandra_view_where_clause(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_where_clause
        )

    @cassandra_view_where_clause.setter
    def cassandra_view_where_clause(self, cassandra_view_where_clause: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_where_clause = cassandra_view_where_clause

    @property
    def cassandra_view_speculative_retry(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_speculative_retry
        )

    @cassandra_view_speculative_retry.setter
    def cassandra_view_speculative_retry(
        self, cassandra_view_speculative_retry: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_speculative_retry = (
            cassandra_view_speculative_retry
        )

    @property
    def cassandra_keyspace(self) -> Optional[CassandraKeyspace]:
        return None if self.attributes is None else self.attributes.cassandra_keyspace

    @cassandra_keyspace.setter
    def cassandra_keyspace(self, cassandra_keyspace: Optional[CassandraKeyspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_keyspace = cassandra_keyspace

    @property
    def cassandra_columns(self) -> Optional[List[CassandraColumn]]:
        return None if self.attributes is None else self.attributes.cassandra_columns

    @cassandra_columns.setter
    def cassandra_columns(self, cassandra_columns: Optional[List[CassandraColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_columns = cassandra_columns

    class Attributes(Cassandra.Attributes):
        cassandra_view_table_id: Optional[str] = Field(default=None, description="")
        cassandra_view_bloom_filter_f_p_chance: Optional[float] = Field(
            default=None, description=""
        )
        cassandra_view_caching: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        cassandra_view_comment: Optional[str] = Field(default=None, description="")
        cassandra_view_compaction: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        cassandra_view_c_r_c_check_chance: Optional[float] = Field(
            default=None, description=""
        )
        cassandra_view_d_c_local_read_repair_chance: Optional[float] = Field(
            default=None, description=""
        )
        cassandra_view_default_t_t_l: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_view_g_c_grace_seconds: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_view_include_all_columns: Optional[bool] = Field(
            default=None, description=""
        )
        cassandra_view_max_index_interval: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_view_membtable_flush_period_in_m_s: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_view_min_index_interval: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_view_read_repair_interval: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_view_query: Optional[str] = Field(default=None, description="")
        cassandra_view_where_clause: Optional[str] = Field(default=None, description="")
        cassandra_view_speculative_retry: Optional[str] = Field(
            default=None, description=""
        )
        cassandra_keyspace: Optional[CassandraKeyspace] = Field(
            default=None, description=""
        )  # relationship
        cassandra_columns: Optional[List[CassandraColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CassandraView.Attributes = Field(
        default_factory=lambda: CassandraView.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cassandra_column import CassandraColumn  # noqa: E402, F401
from .cassandra_keyspace import CassandraKeyspace  # noqa: E402, F401

CassandraView.Attributes.update_forward_refs()
