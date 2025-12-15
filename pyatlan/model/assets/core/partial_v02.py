# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .catalog import Catalog


class PartialV02(Catalog):
    """Description"""

    type_name: str = Field(default="PartialV02", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PartialV02":
            raise ValueError("must be PartialV02")
        return v

    def __setattr__(self, name, value):
        if name in PartialV02._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARTIAL_V02STRUCTURE_JSON: ClassVar[KeywordField] = KeywordField(
        "partialV02StructureJSON", "partialV02StructureJSON"
    )
    """
    Complete JSON structure of this partial asset, as a string.
    """
    PARTIAL_V02RESOLVED_TYPE_NAME: ClassVar[KeywordField] = KeywordField(
        "partialV02ResolvedTypeName", "partialV02ResolvedTypeName"
    )
    """
    Atlan-mapped type name of this partial asset.
    """
    PARTIAL_V02UNKNOWN_ATTRIBUTES_HASH_ID: ClassVar[KeywordField] = KeywordField(
        "partialV02UnknownAttributesHashId", "partialV02UnknownAttributesHashId"
    )
    """
    Hash ID of the unknown attributes for this partial asset.
    """
    PARTIAL_V02PARENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "partialV02ParentType", "partialV02ParentType"
    )
    """
    Type of the field's parent asset.
    """
    PARTIAL_V02PARENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "partialV02ParentQualifiedName", "partialV02ParentQualifiedName"
    )
    """
    Unique name of the field's parent asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "partial_v02_structure_j_s_o_n",
        "partial_v02_resolved_type_name",
        "partial_v02_unknown_attributes_hash_id",
        "partial_v02_parent_type",
        "partial_v02_parent_qualified_name",
    ]

    @property
    def partial_v02_structure_j_s_o_n(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v02_structure_j_s_o_n
        )

    @partial_v02_structure_j_s_o_n.setter
    def partial_v02_structure_j_s_o_n(
        self, partial_v02_structure_j_s_o_n: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v02_structure_j_s_o_n = partial_v02_structure_j_s_o_n

    @property
    def partial_v02_resolved_type_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v02_resolved_type_name
        )

    @partial_v02_resolved_type_name.setter
    def partial_v02_resolved_type_name(
        self, partial_v02_resolved_type_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v02_resolved_type_name = partial_v02_resolved_type_name

    @property
    def partial_v02_unknown_attributes_hash_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v02_unknown_attributes_hash_id
        )

    @partial_v02_unknown_attributes_hash_id.setter
    def partial_v02_unknown_attributes_hash_id(
        self, partial_v02_unknown_attributes_hash_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v02_unknown_attributes_hash_id = (
            partial_v02_unknown_attributes_hash_id
        )

    @property
    def partial_v02_parent_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.partial_v02_parent_type
        )

    @partial_v02_parent_type.setter
    def partial_v02_parent_type(self, partial_v02_parent_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v02_parent_type = partial_v02_parent_type

    @property
    def partial_v02_parent_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v02_parent_qualified_name
        )

    @partial_v02_parent_qualified_name.setter
    def partial_v02_parent_qualified_name(
        self, partial_v02_parent_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v02_parent_qualified_name = (
            partial_v02_parent_qualified_name
        )

    class Attributes(Catalog.Attributes):
        partial_v02_structure_j_s_o_n: Optional[str] = Field(
            default=None, description=""
        )
        partial_v02_resolved_type_name: Optional[str] = Field(
            default=None, description=""
        )
        partial_v02_unknown_attributes_hash_id: Optional[str] = Field(
            default=None, description=""
        )
        partial_v02_parent_type: Optional[str] = Field(default=None, description="")
        partial_v02_parent_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: PartialV02.Attributes = Field(
        default_factory=lambda: PartialV02.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
