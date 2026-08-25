# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .v1_coalesce import V1Coalesce


class V1CoalesceColumn(V1Coalesce):
    """Description"""

    type_name: str = Field(default="V1CoalesceColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "V1CoalesceColumn":
            raise ValueError("must be V1CoalesceColumn")
        return v

    def __setattr__(self, name, value):
        if name in V1CoalesceColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_COLUMN_ID: ClassVar[KeywordField] = KeywordField(
        "coalesceColumnId", "coalesceColumnId"
    )
    """
    Unique identifier of this Coalesce column.
    """
    COALESCE_NODE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceNodeQualifiedName",
        "coalesceNodeQualifiedName.keyword",
        "coalesceNodeQualifiedName",
    )
    """
    Qualified name of the Coalesce node in which this column exists.
    """
    COALESCE_IS_PRIMARY: ClassVar[BooleanField] = BooleanField(
        "coalesceIsPrimary", "coalesceIsPrimary"
    )
    """
    Whether this Coalesce column is a primary key column.
    """
    COALESCE_IS_NULLABLE: ClassVar[BooleanField] = BooleanField(
        "coalesceIsNullable", "coalesceIsNullable"
    )
    """
    Whether this Coalesce column allows null values.
    """

    V1COALESCE_NODE: ClassVar[RelationField] = RelationField("v1CoalesceNode")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_column_id",
        "coalesce_node_qualified_name",
        "coalesce_is_primary",
        "coalesce_is_nullable",
        "v1_coalesce_node",
    ]

    @property
    def coalesce_column_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.coalesce_column_id

    @coalesce_column_id.setter
    def coalesce_column_id(self, coalesce_column_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_column_id = coalesce_column_id

    @property
    def coalesce_node_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.coalesce_node_qualified_name
        )

    @coalesce_node_qualified_name.setter
    def coalesce_node_qualified_name(self, coalesce_node_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_node_qualified_name = coalesce_node_qualified_name

    @property
    def coalesce_is_primary(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.coalesce_is_primary

    @coalesce_is_primary.setter
    def coalesce_is_primary(self, coalesce_is_primary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_is_primary = coalesce_is_primary

    @property
    def coalesce_is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.coalesce_is_nullable

    @coalesce_is_nullable.setter
    def coalesce_is_nullable(self, coalesce_is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_is_nullable = coalesce_is_nullable

    @property
    def v1_coalesce_node(self) -> Optional[V1CoalesceNode]:
        return None if self.attributes is None else self.attributes.v1_coalesce_node

    @v1_coalesce_node.setter
    def v1_coalesce_node(self, v1_coalesce_node: Optional[V1CoalesceNode]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.v1_coalesce_node = v1_coalesce_node

    class Attributes(V1Coalesce.Attributes):
        coalesce_column_id: Optional[str] = Field(default=None, description="")
        coalesce_node_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        coalesce_is_primary: Optional[bool] = Field(default=None, description="")
        coalesce_is_nullable: Optional[bool] = Field(default=None, description="")
        v1_coalesce_node: Optional[V1CoalesceNode] = Field(
            default=None, description=""
        )  # relationship

    attributes: V1CoalesceColumn.Attributes = Field(
        default_factory=lambda: V1CoalesceColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .v1_coalesce_node import V1CoalesceNode  # noqa: E402, F401

V1CoalesceColumn.Attributes.update_forward_refs()
