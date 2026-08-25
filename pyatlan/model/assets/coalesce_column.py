# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, TextField

from .coalesce import Coalesce


class CoalesceColumn(Coalesce):
    """Description"""

    type_name: str = Field(default="CoalesceColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CoalesceColumn":
            raise ValueError("must be CoalesceColumn")
        return v

    def __setattr__(self, name, value):
        if name in CoalesceColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_NODE_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "coalesceNodeQualifiedName", "coalesceNodeQualifiedName"
    )
    """
    TBC
    """
    DATA_TYPE: ClassVar[TextField] = TextField("dataType", "dataType")
    """
    TBC
    """
    IS_NULLABLE: ClassVar[BooleanField] = BooleanField("isNullable", "isNullable")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_node_qualified_name",
        "data_type",
        "is_nullable",
    ]

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
    def data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_type

    @data_type.setter
    def data_type(self, data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_type = data_type

    @property
    def is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_nullable

    @is_nullable.setter
    def is_nullable(self, is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_nullable = is_nullable

    class Attributes(Coalesce.Attributes):
        coalesce_node_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        data_type: Optional[str] = Field(default=None, description="")
        is_nullable: Optional[bool] = Field(default=None, description="")

    attributes: CoalesceColumn.Attributes = Field(
        default_factory=lambda: CoalesceColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


CoalesceColumn.Attributes.update_forward_refs()
