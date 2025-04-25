# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .cassandra import Cassandra


class CassandraKeyspace(Cassandra):
    """Description"""

    type_name: str = Field(default="CassandraKeyspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CassandraKeyspace":
            raise ValueError("must be CassandraKeyspace")
        return v

    def __setattr__(self, name, value):
        if name in CassandraKeyspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CASSANDRA_KEYSPACE_DURABLE_WRITES: ClassVar[BooleanField] = BooleanField(
        "cassandraKeyspaceDurableWrites", "cassandraKeyspaceDurableWrites"
    )
    """
    Indicates whether durable writes are enabled for the CassandraKeyspace.
    """
    CASSANDRA_KEYSPACE_REPLICATION: ClassVar[KeywordField] = KeywordField(
        "cassandraKeyspaceReplication", "cassandraKeyspaceReplication"
    )
    """
    Replication class for the CassandraKeyspace.
    """
    CASSANDRA_KEYSPACE_VIRTUAL: ClassVar[BooleanField] = BooleanField(
        "cassandraKeyspaceVirtual", "cassandraKeyspaceVirtual"
    )
    """
    Indicates whether the CassandraKeyspace is virtual.
    """
    CASSANDRA_KEYSPACE_QUERY: ClassVar[KeywordField] = KeywordField(
        "cassandraKeyspaceQuery", "cassandraKeyspaceQuery"
    )
    """
    Query associated with the CassandraKeyspace.
    """

    CASSANDRA_TABLES: ClassVar[RelationField] = RelationField("cassandraTables")
    """
    TBC
    """
    CASSANDRA_VIEWS: ClassVar[RelationField] = RelationField("cassandraViews")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cassandra_keyspace_durable_writes",
        "cassandra_keyspace_replication",
        "cassandra_keyspace_virtual",
        "cassandra_keyspace_query",
        "cassandra_tables",
        "cassandra_views",
    ]

    @property
    def cassandra_keyspace_durable_writes(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_keyspace_durable_writes
        )

    @cassandra_keyspace_durable_writes.setter
    def cassandra_keyspace_durable_writes(
        self, cassandra_keyspace_durable_writes: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_keyspace_durable_writes = (
            cassandra_keyspace_durable_writes
        )

    @property
    def cassandra_keyspace_replication(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_keyspace_replication
        )

    @cassandra_keyspace_replication.setter
    def cassandra_keyspace_replication(
        self, cassandra_keyspace_replication: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_keyspace_replication = cassandra_keyspace_replication

    @property
    def cassandra_keyspace_virtual(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_keyspace_virtual
        )

    @cassandra_keyspace_virtual.setter
    def cassandra_keyspace_virtual(self, cassandra_keyspace_virtual: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_keyspace_virtual = cassandra_keyspace_virtual

    @property
    def cassandra_keyspace_query(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_keyspace_query
        )

    @cassandra_keyspace_query.setter
    def cassandra_keyspace_query(self, cassandra_keyspace_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_keyspace_query = cassandra_keyspace_query

    @property
    def cassandra_tables(self) -> Optional[List[CassandraTable]]:
        return None if self.attributes is None else self.attributes.cassandra_tables

    @cassandra_tables.setter
    def cassandra_tables(self, cassandra_tables: Optional[List[CassandraTable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_tables = cassandra_tables

    @property
    def cassandra_views(self) -> Optional[List[CassandraView]]:
        return None if self.attributes is None else self.attributes.cassandra_views

    @cassandra_views.setter
    def cassandra_views(self, cassandra_views: Optional[List[CassandraView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_views = cassandra_views

    class Attributes(Cassandra.Attributes):
        cassandra_keyspace_durable_writes: Optional[bool] = Field(
            default=None, description=""
        )
        cassandra_keyspace_replication: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        cassandra_keyspace_virtual: Optional[bool] = Field(default=None, description="")
        cassandra_keyspace_query: Optional[str] = Field(default=None, description="")
        cassandra_tables: Optional[List[CassandraTable]] = Field(
            default=None, description=""
        )  # relationship
        cassandra_views: Optional[List[CassandraView]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CassandraKeyspace.Attributes = Field(
        default_factory=lambda: CassandraKeyspace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cassandra_table import CassandraTable  # noqa: E402, F401
from .cassandra_view import CassandraView  # noqa: E402, F401

CassandraKeyspace.Attributes.update_forward_refs()
