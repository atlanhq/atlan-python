# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .v1_coalesce import V1Coalesce


class V1CoalesceNode(V1Coalesce):
    """Description"""

    type_name: str = Field(default="V1CoalesceNode", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "V1CoalesceNode":
            raise ValueError("must be V1CoalesceNode")
        return v

    def __setattr__(self, name, value):
        if name in V1CoalesceNode._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_NODE_ID: ClassVar[KeywordField] = KeywordField(
        "coalesceNodeId", "coalesceNodeId"
    )
    """
    Unique identifier of this Coalesce node.
    """
    COALESCE_NODE_TYPE: ClassVar[KeywordField] = KeywordField(
        "coalesceNodeType", "coalesceNodeType"
    )
    """
    Type of this Coalesce node (e.g. source, target, stage).
    """
    COALESCE_ENVIRONMENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceEnvironmentQualifiedName",
        "coalesceEnvironmentQualifiedName.keyword",
        "coalesceEnvironmentQualifiedName",
    )
    """
    Qualified name of the Coalesce environment in which this node exists.
    """
    COALESCE_SNOWFLAKE_TABLE_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "coalesceSnowflakeTableQualifiedName",
            "coalesceSnowflakeTableQualifiedName.keyword",
            "coalesceSnowflakeTableQualifiedName",
        )
    )
    """
    Qualified name of the Snowflake table that this Coalesce node materializes into.
    """

    V1COALESCE_ENVIRONMENT: ClassVar[RelationField] = RelationField(
        "v1CoalesceEnvironment"
    )
    """
    TBC
    """
    V1COALESCE_COLUMNS: ClassVar[RelationField] = RelationField("v1CoalesceColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_node_id",
        "coalesce_node_type",
        "coalesce_environment_qualified_name",
        "coalesce_snowflake_table_qualified_name",
        "v1_coalesce_environment",
        "v1_coalesce_columns",
    ]

    @property
    def coalesce_node_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.coalesce_node_id

    @coalesce_node_id.setter
    def coalesce_node_id(self, coalesce_node_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_node_id = coalesce_node_id

    @property
    def coalesce_node_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.coalesce_node_type

    @coalesce_node_type.setter
    def coalesce_node_type(self, coalesce_node_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_node_type = coalesce_node_type

    @property
    def coalesce_environment_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.coalesce_environment_qualified_name
        )

    @coalesce_environment_qualified_name.setter
    def coalesce_environment_qualified_name(
        self, coalesce_environment_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_environment_qualified_name = (
            coalesce_environment_qualified_name
        )

    @property
    def coalesce_snowflake_table_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.coalesce_snowflake_table_qualified_name
        )

    @coalesce_snowflake_table_qualified_name.setter
    def coalesce_snowflake_table_qualified_name(
        self, coalesce_snowflake_table_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_snowflake_table_qualified_name = (
            coalesce_snowflake_table_qualified_name
        )

    @property
    def v1_coalesce_environment(self) -> Optional[V1CoalesceEnvironment]:
        return (
            None if self.attributes is None else self.attributes.v1_coalesce_environment
        )

    @v1_coalesce_environment.setter
    def v1_coalesce_environment(
        self, v1_coalesce_environment: Optional[V1CoalesceEnvironment]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.v1_coalesce_environment = v1_coalesce_environment

    @property
    def v1_coalesce_columns(self) -> Optional[List[V1CoalesceColumn]]:
        return None if self.attributes is None else self.attributes.v1_coalesce_columns

    @v1_coalesce_columns.setter
    def v1_coalesce_columns(
        self, v1_coalesce_columns: Optional[List[V1CoalesceColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.v1_coalesce_columns = v1_coalesce_columns

    class Attributes(V1Coalesce.Attributes):
        coalesce_node_id: Optional[str] = Field(default=None, description="")
        coalesce_node_type: Optional[str] = Field(default=None, description="")
        coalesce_environment_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        coalesce_snowflake_table_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        v1_coalesce_environment: Optional[V1CoalesceEnvironment] = Field(
            default=None, description=""
        )  # relationship
        v1_coalesce_columns: Optional[List[V1CoalesceColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: V1CoalesceNode.Attributes = Field(
        default_factory=lambda: V1CoalesceNode.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .v1_coalesce_column import V1CoalesceColumn  # noqa: E402, F401
from .v1_coalesce_environment import V1CoalesceEnvironment  # noqa: E402, F401

V1CoalesceNode.Attributes.update_forward_refs()
