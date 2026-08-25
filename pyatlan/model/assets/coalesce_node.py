# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import TextField

from .coalesce import Coalesce


class CoalesceNode(Coalesce):
    """Description"""

    type_name: str = Field(default="CoalesceNode", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CoalesceNode":
            raise ValueError("must be CoalesceNode")
        return v

    def __setattr__(self, name, value):
        if name in CoalesceNode._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_NODE_TYPE: ClassVar[TextField] = TextField(
        "coalesceNodeType", "coalesceNodeType"
    )
    """
    TBC
    """
    COALESCE_ENVIRONMENT_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "coalesceEnvironmentQualifiedName", "coalesceEnvironmentQualifiedName"
    )
    """
    TBC
    """
    COALESCE_LOCATION_NAME: ClassVar[TextField] = TextField(
        "coalesceLocationName", "coalesceLocationName"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_node_type",
        "coalesce_environment_qualified_name",
        "coalesce_location_name",
    ]

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
    def coalesce_location_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_location_name
        )

    @coalesce_location_name.setter
    def coalesce_location_name(self, coalesce_location_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_location_name = coalesce_location_name

    class Attributes(Coalesce.Attributes):
        coalesce_node_type: Optional[str] = Field(default=None, description="")
        coalesce_environment_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        coalesce_location_name: Optional[str] = Field(default=None, description="")

    attributes: CoalesceNode.Attributes = Field(
        default_factory=lambda: CoalesceNode.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


CoalesceNode.Attributes.update_forward_refs()
