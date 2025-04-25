# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.no_s_q_l import NoSQL


class Cassandra(NoSQL):
    """Description"""

    type_name: str = Field(default="Cassandra", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Cassandra":
            raise ValueError("must be Cassandra")
        return v

    def __setattr__(self, name, value):
        if name in Cassandra._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CASSANDRA_KEYSPACE_NAME: ClassVar[KeywordField] = KeywordField(
        "cassandraKeyspaceName", "cassandraKeyspaceName"
    )
    """
    Name of the keyspace for the Cassandra asset.
    """
    CASSANDRA_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "cassandraTableName", "cassandraTableName"
    )
    """
    Name of the table for the Cassandra asset.
    """
    CASSANDRA_VIEW_NAME: ClassVar[KeywordField] = KeywordField(
        "cassandraViewName", "cassandraViewName"
    )
    """
    Name of view for Cassandra asset
    """
    CASSANDRA_TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "cassandraTableQualifiedName", "cassandraTableQualifiedName"
    )
    """
    Unique name of table for Cassandra asset
    """
    CASSANDRA_VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "cassandraViewQualifiedName", "cassandraViewQualifiedName"
    )
    """
    Unique name of view for Cassandra asset
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cassandra_keyspace_name",
        "cassandra_table_name",
        "cassandra_view_name",
        "cassandra_table_qualified_name",
        "cassandra_view_qualified_name",
    ]

    @property
    def cassandra_keyspace_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_keyspace_name
        )

    @cassandra_keyspace_name.setter
    def cassandra_keyspace_name(self, cassandra_keyspace_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_keyspace_name = cassandra_keyspace_name

    @property
    def cassandra_table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cassandra_table_name

    @cassandra_table_name.setter
    def cassandra_table_name(self, cassandra_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_name = cassandra_table_name

    @property
    def cassandra_view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cassandra_view_name

    @cassandra_view_name.setter
    def cassandra_view_name(self, cassandra_view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_name = cassandra_view_name

    @property
    def cassandra_table_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_table_qualified_name
        )

    @cassandra_table_qualified_name.setter
    def cassandra_table_qualified_name(
        self, cassandra_table_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table_qualified_name = cassandra_table_qualified_name

    @property
    def cassandra_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_view_qualified_name
        )

    @cassandra_view_qualified_name.setter
    def cassandra_view_qualified_name(
        self, cassandra_view_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view_qualified_name = cassandra_view_qualified_name

    class Attributes(NoSQL.Attributes):
        cassandra_keyspace_name: Optional[str] = Field(default=None, description="")
        cassandra_table_name: Optional[str] = Field(default=None, description="")
        cassandra_view_name: Optional[str] = Field(default=None, description="")
        cassandra_table_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        cassandra_view_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: Cassandra.Attributes = Field(
        default_factory=lambda: Cassandra.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Cassandra.Attributes.update_forward_refs()
