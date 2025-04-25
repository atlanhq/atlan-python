# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .cassandra import Cassandra


class CassandraIndex(Cassandra):
    """Description"""

    type_name: str = Field(default="CassandraIndex", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CassandraIndex":
            raise ValueError("must be CassandraIndex")
        return v

    def __setattr__(self, name, value):
        if name in CassandraIndex._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CASSANDRA_INDEX_KIND: ClassVar[KeywordField] = KeywordField(
        "cassandraIndexKind", "cassandraIndexKind"
    )
    """
    Kind of index (e.g. COMPOSITES).
    """
    CASSANDRA_INDEX_OPTIONS: ClassVar[KeywordField] = KeywordField(
        "cassandraIndexOptions", "cassandraIndexOptions"
    )
    """
    Options for the index.
    """
    CASSANDRA_INDEX_QUERY: ClassVar[KeywordField] = KeywordField(
        "cassandraIndexQuery", "cassandraIndexQuery"
    )
    """
    Query used to create the index.
    """

    CASSANDRA_TABLE: ClassVar[RelationField] = RelationField("cassandraTable")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cassandra_index_kind",
        "cassandra_index_options",
        "cassandra_index_query",
        "cassandra_table",
    ]

    @property
    def cassandra_index_kind(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cassandra_index_kind

    @cassandra_index_kind.setter
    def cassandra_index_kind(self, cassandra_index_kind: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_index_kind = cassandra_index_kind

    @property
    def cassandra_index_options(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.cassandra_index_options
        )

    @cassandra_index_options.setter
    def cassandra_index_options(
        self, cassandra_index_options: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_index_options = cassandra_index_options

    @property
    def cassandra_index_query(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_index_query
        )

    @cassandra_index_query.setter
    def cassandra_index_query(self, cassandra_index_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_index_query = cassandra_index_query

    @property
    def cassandra_table(self) -> Optional[CassandraTable]:
        return None if self.attributes is None else self.attributes.cassandra_table

    @cassandra_table.setter
    def cassandra_table(self, cassandra_table: Optional[CassandraTable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table = cassandra_table

    class Attributes(Cassandra.Attributes):
        cassandra_index_kind: Optional[str] = Field(default=None, description="")
        cassandra_index_options: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        cassandra_index_query: Optional[str] = Field(default=None, description="")
        cassandra_table: Optional[CassandraTable] = Field(
            default=None, description=""
        )  # relationship

    attributes: CassandraIndex.Attributes = Field(
        default_factory=lambda: CassandraIndex.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cassandra_table import CassandraTable  # noqa: E402, F401

CassandraIndex.Attributes.update_forward_refs()
