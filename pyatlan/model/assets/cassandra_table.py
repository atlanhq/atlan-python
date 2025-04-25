# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)

from .cassandra import Cassandra


class CassandraTable(Cassandra):
    """Description"""

    type_name: str = Field(default="CassandraTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CassandraTable":
            raise ValueError("must be CassandraTable")
        return v

    def __setattr__(self, name, value):
        if name in CassandraTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CASSANDRA_TABLE_BLOOM_FILTER_FP_CHANCE: ClassVar[NumericField] = NumericField(
        "cassandraTableBloomFilterFPChance", "cassandraTableBloomFilterFPChance"
    )
    """
    Bloom filter false positive chance for the CassandraTable.
    """
    CASSANDRA_TABLE_CACHING: ClassVar[KeywordField] = KeywordField(
        "cassandraTableCaching", "cassandraTableCaching"
    )
    """
    Caching behavior in Cassandra.
    """
    CASSANDRA_TABLE_COMMENT: ClassVar[KeywordField] = KeywordField(
        "cassandraTableComment", "cassandraTableComment"
    )
    """
    Comment describing the CassandraTable's purpose or usage in Cassandra.
    """
    CASSANDRA_TABLE_COMPACTION: ClassVar[KeywordField] = KeywordField(
        "cassandraTableCompaction", "cassandraTableCompaction"
    )
    """
    Compaction used for the CassandraTable in Cassandra.
    """
    CASSANDRA_TABLE_COMPRESSION: ClassVar[KeywordField] = KeywordField(
        "cassandraTableCompression", "cassandraTableCompression"
    )
    """
    Compression used for the CassandraTable in Cassandra.
    """
    CASSANDRA_TABLE_CRC_CHECK_CHANCE: ClassVar[NumericField] = NumericField(
        "cassandraTableCRCCheckChance", "cassandraTableCRCCheckChance"
    )
    """
    CRC check chance for the CassandraTable.
    """
    CASSANDRA_TABLE_DC_LOCAL_READ_REPAIR_CHANCE: ClassVar[NumericField] = NumericField(
        "cassandraTableDCLocalReadRepairChance", "cassandraTableDCLocalReadRepairChance"
    )
    """
    Local read repair chance in Cassandra.
    """
    CASSANDRA_TABLE_DEFAULT_TTL: ClassVar[NumericField] = NumericField(
        "cassandraTableDefaultTTL", "cassandraTableDefaultTTL"
    )
    """
    Default time-to-live for the CassandraTable in Cassandra.
    """
    CASSANDRA_TABLE_FLAGS: ClassVar[KeywordField] = KeywordField(
        "cassandraTableFlags", "cassandraTableFlags"
    )
    """
    Flags associated with the CassandraTable.
    """
    CASSANDRA_TABLE_GC_GRACE_SECONDS: ClassVar[NumericField] = NumericField(
        "cassandraTableGCGraceSeconds", "cassandraTableGCGraceSeconds"
    )
    """
    Grace period for garbage collection in the CassandraTable.
    """
    CASSANDRA_TABLE_ID: ClassVar[KeywordField] = KeywordField(
        "cassandraTableId", "cassandraTableId"
    )
    """
    Unique identifier for the CassandraTable.
    """
    CASSANDRA_TABLE_MAX_INDEX_INTERVAL: ClassVar[NumericField] = NumericField(
        "cassandraTableMaxIndexInterval", "cassandraTableMaxIndexInterval"
    )
    """
    Maximum index interval for the CassandraTable.
    """
    CASSANDRA_TABLE_MEMTABLE_FLUSH_PERIOD_IN_MS: ClassVar[NumericField] = NumericField(
        "cassandraTableMemtableFlushPeriodInMs", "cassandraTableMemtableFlushPeriodInMs"
    )
    """
    Memtable flush period for the CassandraTable (in milliseconds).
    """
    CASSANDRA_TABLE_MIN_INDEX_INTERVAL: ClassVar[NumericField] = NumericField(
        "cassandraTableMinIndexInterval", "cassandraTableMinIndexInterval"
    )
    """
    Minimum index interval for the CassandraTable.
    """
    CASSANDRA_TABLE_READ_REPAIR_CHANCE: ClassVar[NumericField] = NumericField(
        "cassandraTableReadRepairChance", "cassandraTableReadRepairChance"
    )
    """
    Read repair chance for the CassandraTable.
    """
    CASSANDRA_TABLE_SPECULATIVE_RETRY: ClassVar[KeywordField] = KeywordField(
        "cassandraTableSpeculativeRetry", "cassandraTableSpeculativeRetry"
    )
    """
    Speculative retry setting for the CassandraTable.
    """
    CASSANDRA_TABLE_VIRTUAL: ClassVar[BooleanField] = BooleanField(
        "cassandraTableVirtual", "cassandraTableVirtual"
    )
    """
    Indicates whether the CassandraTable is virtual.
    """
    CASSANDRA_TABLE_QUERY: ClassVar[KeywordField] = KeywordField(
        "cassandraTableQuery", "cassandraTableQuery"
    )
    """
    Query used to create the CassandraTable in Cassandra.
    """

    CASSANDRA_KEYSPACE: ClassVar[RelationField] = RelationField("cassandraKeyspace")
    """
    TBC
    """
    CASSANDRA_COLUMNS: ClassVar[RelationField] = RelationField("cassandraColumns")
    """
    TBC
    """
    CASSANDRA_INDEXES: ClassVar[RelationField] = RelationField("cassandraIndexes")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cassandra_table_bloom_filter_f_p_chance",
        "cassandra_table_caching",
        "cassandra_table_comment",
        "cassandra_table_compaction",
        "cassandra_table_compression",
        "cassandra_table_c_r_c_check_chance",
        "cassandra_table_d_c_local_read_repair_chance",
        "cassandra_table_default_t_t_l",
        "cassandra_table_flags",
        "cassandra_table_g_c_grace_seconds",
        "cassandra_table_id",
        "cassandra_table_max_index_interval",
        "cassandra_table_memtable_flush_period_in_ms",
        "cassandra_table_min_index_interval",
        "cassandra_table_read_repair_chance",
        "cassandra_table_speculative_retry",
        "cassandra_table_virtual",
        "cassandra_table_query",
        "cassandra_keyspace",
        "cassandra_columns",
        "cassandra_indexes",
    ]

    @property
    def cassandra_table_bloom_filter_f_p_chance(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_bloom_filter_f_p_chance
        )

    @cassandra_table_bloom_filter_f_p_chance.setter
    def cassandra_table_bloom_filter_f_p_chance(
        self, cassandra_table_bloom_filter_f_p_chance: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_bloom_filter_f_p_chance = (
            cassandra_table_bloom_filter_f_p_chance
        )

    @property
    def cassandra_table_caching(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.cassandra_table_caching
        )

    @cassandra_table_caching.setter
    def cassandra_table_caching(
        self, cassandra_table_caching: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_caching = cassandra_table_caching

    @property
    def cassandra_table_comment(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_table_comment
        )

    @cassandra_table_comment.setter
    def cassandra_table_comment(self, cassandra_table_comment: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_comment = cassandra_table_comment

    @property
    def cassandra_table_compaction(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_compaction
        )

    @cassandra_table_compaction.setter
    def cassandra_table_compaction(
        self, cassandra_table_compaction: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_compaction = cassandra_table_compaction

    @property
    def cassandra_table_compression(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_compression
        )

    @cassandra_table_compression.setter
    def cassandra_table_compression(
        self, cassandra_table_compression: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_compression = cassandra_table_compression

    @property
    def cassandra_table_c_r_c_check_chance(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_c_r_c_check_chance
        )

    @cassandra_table_c_r_c_check_chance.setter
    def cassandra_table_c_r_c_check_chance(
        self, cassandra_table_c_r_c_check_chance: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_c_r_c_check_chance = (
            cassandra_table_c_r_c_check_chance
        )

    @property
    def cassandra_table_d_c_local_read_repair_chance(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_d_c_local_read_repair_chance
        )

    @cassandra_table_d_c_local_read_repair_chance.setter
    def cassandra_table_d_c_local_read_repair_chance(
        self, cassandra_table_d_c_local_read_repair_chance: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_d_c_local_read_repair_chance = (
            cassandra_table_d_c_local_read_repair_chance
        )

    @property
    def cassandra_table_default_t_t_l(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_default_t_t_l
        )

    @cassandra_table_default_t_t_l.setter
    def cassandra_table_default_t_t_l(
        self, cassandra_table_default_t_t_l: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_default_t_t_l = cassandra_table_default_t_t_l

    @property
    def cassandra_table_flags(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.cassandra_table_flags
        )

    @cassandra_table_flags.setter
    def cassandra_table_flags(self, cassandra_table_flags: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_flags = cassandra_table_flags

    @property
    def cassandra_table_g_c_grace_seconds(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_g_c_grace_seconds
        )

    @cassandra_table_g_c_grace_seconds.setter
    def cassandra_table_g_c_grace_seconds(
        self, cassandra_table_g_c_grace_seconds: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_g_c_grace_seconds = (
            cassandra_table_g_c_grace_seconds
        )

    @property
    def cassandra_table_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cassandra_table_id

    @cassandra_table_id.setter
    def cassandra_table_id(self, cassandra_table_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_id = cassandra_table_id

    @property
    def cassandra_table_max_index_interval(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_max_index_interval
        )

    @cassandra_table_max_index_interval.setter
    def cassandra_table_max_index_interval(
        self, cassandra_table_max_index_interval: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_max_index_interval = (
            cassandra_table_max_index_interval
        )

    @property
    def cassandra_table_memtable_flush_period_in_ms(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_memtable_flush_period_in_ms
        )

    @cassandra_table_memtable_flush_period_in_ms.setter
    def cassandra_table_memtable_flush_period_in_ms(
        self, cassandra_table_memtable_flush_period_in_ms: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_memtable_flush_period_in_ms = (
            cassandra_table_memtable_flush_period_in_ms
        )

    @property
    def cassandra_table_min_index_interval(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_min_index_interval
        )

    @cassandra_table_min_index_interval.setter
    def cassandra_table_min_index_interval(
        self, cassandra_table_min_index_interval: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_min_index_interval = (
            cassandra_table_min_index_interval
        )

    @property
    def cassandra_table_read_repair_chance(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_read_repair_chance
        )

    @cassandra_table_read_repair_chance.setter
    def cassandra_table_read_repair_chance(
        self, cassandra_table_read_repair_chance: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_read_repair_chance = (
            cassandra_table_read_repair_chance
        )

    @property
    def cassandra_table_speculative_retry(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_speculative_retry
        )

    @cassandra_table_speculative_retry.setter
    def cassandra_table_speculative_retry(
        self, cassandra_table_speculative_retry: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_speculative_retry = (
            cassandra_table_speculative_retry
        )

    @property
    def cassandra_table_virtual(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.cassandra_table_virtual
        )

    @cassandra_table_virtual.setter
    def cassandra_table_virtual(self, cassandra_table_virtual: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_virtual = cassandra_table_virtual

    @property
    def cassandra_table_query(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_table_query
        )

    @cassandra_table_query.setter
    def cassandra_table_query(self, cassandra_table_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_query = cassandra_table_query

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

    @property
    def cassandra_indexes(self) -> Optional[List[CassandraIndex]]:
        return None if self.attributes is None else self.attributes.cassandra_indexes

    @cassandra_indexes.setter
    def cassandra_indexes(self, cassandra_indexes: Optional[List[CassandraIndex]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_indexes = cassandra_indexes

    class Attributes(Cassandra.Attributes):
        cassandra_table_bloom_filter_f_p_chance: Optional[float] = Field(
            default=None, description=""
        )
        cassandra_table_caching: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        cassandra_table_comment: Optional[str] = Field(default=None, description="")
        cassandra_table_compaction: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        cassandra_table_compression: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        cassandra_table_c_r_c_check_chance: Optional[float] = Field(
            default=None, description=""
        )
        cassandra_table_d_c_local_read_repair_chance: Optional[float] = Field(
            default=None, description=""
        )
        cassandra_table_default_t_t_l: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_table_flags: Optional[Set[str]] = Field(default=None, description="")
        cassandra_table_g_c_grace_seconds: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_table_id: Optional[str] = Field(default=None, description="")
        cassandra_table_max_index_interval: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_table_memtable_flush_period_in_ms: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_table_min_index_interval: Optional[int] = Field(
            default=None, description=""
        )
        cassandra_table_read_repair_chance: Optional[float] = Field(
            default=None, description=""
        )
        cassandra_table_speculative_retry: Optional[str] = Field(
            default=None, description=""
        )
        cassandra_table_virtual: Optional[bool] = Field(default=None, description="")
        cassandra_table_query: Optional[str] = Field(default=None, description="")
        cassandra_keyspace: Optional[CassandraKeyspace] = Field(
            default=None, description=""
        )  # relationship
        cassandra_columns: Optional[List[CassandraColumn]] = Field(
            default=None, description=""
        )  # relationship
        cassandra_indexes: Optional[List[CassandraIndex]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CassandraTable.Attributes = Field(
        default_factory=lambda: CassandraTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cassandra_column import CassandraColumn  # noqa: E402, F401
from .cassandra_index import CassandraIndex  # noqa: E402, F401
from .cassandra_keyspace import CassandraKeyspace  # noqa: E402, F401

CassandraTable.Attributes.update_forward_refs()
