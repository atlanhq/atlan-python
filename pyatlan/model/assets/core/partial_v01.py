# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, TextField

from .catalog import Catalog


class PartialV01(Catalog):
    """Description"""

    type_name: str = Field(default="PartialV01", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PartialV01":
            raise ValueError("must be PartialV01")
        return v

    def __setattr__(self, name, value):
        if name in PartialV01._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARTIAL_V01STRUCTURE_JSON: ClassVar[TextField] = TextField(
        "partialV01StructureJSON", "partialV01StructureJSON"
    )
    """
    Complete JSON structure of this partial asset in string.
    """
    PARTIAL_V01RESOLVED_TYPE_NAME: ClassVar[KeywordField] = KeywordField(
        "partialV01ResolvedTypeName", "partialV01ResolvedTypeName"
    )
    """
    Atlan-mapped type name of this partial asset.
    """
    PARTIAL_V01UNKNOWN_ATTRIBUTES_HASH_ID: ClassVar[KeywordField] = KeywordField(
        "partialV01UnknownAttributesHashId", "partialV01UnknownAttributesHashId"
    )
    """
    Hash ID of the unknown attributes for this partial asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "partial_v01_structure_j_s_o_n",
        "partial_v01_resolved_type_name",
        "partial_v01_unknown_attributes_hash_id",
    ]

    @property
    def partial_v01_structure_j_s_o_n(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v01_structure_j_s_o_n
        )

    @partial_v01_structure_j_s_o_n.setter
    def partial_v01_structure_j_s_o_n(
        self, partial_v01_structure_j_s_o_n: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v01_structure_j_s_o_n = partial_v01_structure_j_s_o_n

    @property
    def partial_v01_resolved_type_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v01_resolved_type_name
        )

    @partial_v01_resolved_type_name.setter
    def partial_v01_resolved_type_name(
        self, partial_v01_resolved_type_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v01_resolved_type_name = partial_v01_resolved_type_name

    @property
    def partial_v01_unknown_attributes_hash_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v01_unknown_attributes_hash_id
        )

    @partial_v01_unknown_attributes_hash_id.setter
    def partial_v01_unknown_attributes_hash_id(
        self, partial_v01_unknown_attributes_hash_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v01_unknown_attributes_hash_id = (
            partial_v01_unknown_attributes_hash_id
        )

    class Attributes(Catalog.Attributes):
        partial_v01_structure_j_s_o_n: Optional[str] = Field(
            default=None, description=""
        )
        partial_v01_resolved_type_name: Optional[str] = Field(
            default=None, description=""
        )
        partial_v01_unknown_attributes_hash_id: Optional[str] = Field(
            default=None, description=""
        )

    attributes: PartialV01.Attributes = Field(
        default_factory=lambda: PartialV01.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
