# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .cassandra import Cassandra


class CassandraColumn(Cassandra):
    """Description"""

    type_name: str = Field(default="CassandraColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CassandraColumn":
            raise ValueError("must be CassandraColumn")
        return v

    def __setattr__(self, name, value):
        if name in CassandraColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CASSANDRA_COLUMN_CLUSTERING_ORDER: ClassVar[KeywordField] = KeywordField(
        "cassandraColumnClusteringOrder", "cassandraColumnClusteringOrder"
    )
    """
    Clustering order of the CassandraColumn.
    """
    CASSANDRA_COLUMN_IS_PARTITION_KEY: ClassVar[BooleanField] = BooleanField(
        "cassandraColumnIsPartitionKey", "cassandraColumnIsPartitionKey"
    )
    """
    Is the CassandraColumn partition key.
    """
    CASSANDRA_COLUMN_IS_CLUSTERING_KEY: ClassVar[BooleanField] = BooleanField(
        "cassandraColumnIsClusteringKey", "cassandraColumnIsClusteringKey"
    )
    """
    Is the CassandraColumn clustering key.
    """
    CASSANDRA_COLUMN_KIND: ClassVar[KeywordField] = KeywordField(
        "cassandraColumnKind", "cassandraColumnKind"
    )
    """
    Kind of CassandraColumn (e.g. partition key, clustering column, etc).
    """
    CASSANDRA_COLUMN_POSITION: ClassVar[NumericField] = NumericField(
        "cassandraColumnPosition", "cassandraColumnPosition"
    )
    """
    Position of the CassandraColumn.
    """
    CASSANDRA_COLUMN_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "cassandraColumnType", "cassandraColumnType.keyword", "cassandraColumnType"
    )
    """
    Type of the CassandraColumn.
    """
    CASSANDRA_COLUMN_IS_STATIC: ClassVar[BooleanField] = BooleanField(
        "cassandraColumnIsStatic", "cassandraColumnIsStatic"
    )
    """
    Indicates whether the CassandraColumn is static.
    """

    CASSANDRA_VIEW: ClassVar[RelationField] = RelationField("cassandraView")
    """
    TBC
    """
    CASSANDRA_TABLE: ClassVar[RelationField] = RelationField("cassandraTable")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cassandra_column_clustering_order",
        "cassandra_column_is_partition_key",
        "cassandra_column_is_clustering_key",
        "cassandra_column_kind",
        "cassandra_column_position",
        "cassandra_column_type",
        "cassandra_column_is_static",
        "cassandra_view",
        "cassandra_table",
    ]

    @property
    def cassandra_column_clustering_order(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_column_clustering_order
        )

    @cassandra_column_clustering_order.setter
    def cassandra_column_clustering_order(
        self, cassandra_column_clustering_order: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_column_clustering_order = (
            cassandra_column_clustering_order
        )

    @property
    def cassandra_column_is_partition_key(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_column_is_partition_key
        )

    @cassandra_column_is_partition_key.setter
    def cassandra_column_is_partition_key(
        self, cassandra_column_is_partition_key: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_column_is_partition_key = (
            cassandra_column_is_partition_key
        )

    @property
    def cassandra_column_is_clustering_key(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_column_is_clustering_key
        )

    @cassandra_column_is_clustering_key.setter
    def cassandra_column_is_clustering_key(
        self, cassandra_column_is_clustering_key: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_column_is_clustering_key = (
            cassandra_column_is_clustering_key
        )

    @property
    def cassandra_column_kind(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_column_kind
        )

    @cassandra_column_kind.setter
    def cassandra_column_kind(self, cassandra_column_kind: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_column_kind = cassandra_column_kind

    @property
    def cassandra_column_position(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_column_position
        )

    @cassandra_column_position.setter
    def cassandra_column_position(self, cassandra_column_position: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_column_position = cassandra_column_position

    @property
    def cassandra_column_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cassandra_column_type
        )

    @cassandra_column_type.setter
    def cassandra_column_type(self, cassandra_column_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_column_type = cassandra_column_type

    @property
    def cassandra_column_is_static(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.cassandra_column_is_static
        )

    @cassandra_column_is_static.setter
    def cassandra_column_is_static(self, cassandra_column_is_static: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_column_is_static = cassandra_column_is_static

    @property
    def cassandra_view(self) -> Optional[CassandraView]:
        return None if self.attributes is None else self.attributes.cassandra_view

    @cassandra_view.setter
    def cassandra_view(self, cassandra_view: Optional[CassandraView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_view = cassandra_view

    @property
    def cassandra_table(self) -> Optional[CassandraTable]:
        return None if self.attributes is None else self.attributes.cassandra_table

    @cassandra_table.setter
    def cassandra_table(self, cassandra_table: Optional[CassandraTable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cassandra_table = cassandra_table

    class Attributes(Cassandra.Attributes):
        cassandra_column_clustering_order: Optional[str] = Field(
            default=None, description=""
        )
        cassandra_column_is_partition_key: Optional[bool] = Field(
            default=None, description=""
        )
        cassandra_column_is_clustering_key: Optional[bool] = Field(
            default=None, description=""
        )
        cassandra_column_kind: Optional[str] = Field(default=None, description="")
        cassandra_column_position: Optional[int] = Field(default=None, description="")
        cassandra_column_type: Optional[str] = Field(default=None, description="")
        cassandra_column_is_static: Optional[bool] = Field(default=None, description="")
        cassandra_view: Optional[CassandraView] = Field(
            default=None, description=""
        )  # relationship
        cassandra_table: Optional[CassandraTable] = Field(
            default=None, description=""
        )  # relationship

    attributes: CassandraColumn.Attributes = Field(
        default_factory=lambda: CassandraColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cassandra_table import CassandraTable  # noqa: E402, F401
from .cassandra_view import CassandraView  # noqa: E402, F401

CassandraColumn.Attributes.update_forward_refs()
