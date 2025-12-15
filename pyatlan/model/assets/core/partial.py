# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .catalog import Catalog


class Partial(Catalog):
    """Description"""

    type_name: str = Field(default="Partial", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Partial":
            raise ValueError("must be Partial")
        return v

    def __setattr__(self, name, value):
        if name in Partial._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARTIAL_STRUCTURE_JSON: ClassVar[KeywordField] = KeywordField(
        "partialStructureJSON", "partialStructureJSON"
    )
    """
    Complete JSON structure of this partial asset, as a string.
    """
    PARTIAL_RESOLVED_TYPE_NAME: ClassVar[KeywordField] = KeywordField(
        "partialResolvedTypeName", "partialResolvedTypeName"
    )
    """
    Atlan-mapped type name of this partial asset.
    """
    PARTIAL_UNKNOWN_ATTRIBUTES_HASH_ID: ClassVar[KeywordField] = KeywordField(
        "partialUnknownAttributesHashId", "partialUnknownAttributesHashId"
    )
    """
    Hash ID of the unknown attributes for this partial asset.
    """
    PARTIAL_PARENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "partialParentType", "partialParentType"
    )
    """
    Type of the field's parent asset.
    """
    PARTIAL_PARENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "partialParentQualifiedName", "partialParentQualifiedName"
    )
    """
    Unique name of the field's parent asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "partial_structure_j_s_o_n",
        "partial_resolved_type_name",
        "partial_unknown_attributes_hash_id",
        "partial_parent_type",
        "partial_parent_qualified_name",
    ]

    @property
    def partial_structure_j_s_o_n(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_structure_j_s_o_n
        )

    @partial_structure_j_s_o_n.setter
    def partial_structure_j_s_o_n(self, partial_structure_j_s_o_n: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_structure_j_s_o_n = partial_structure_j_s_o_n

    @property
    def partial_resolved_type_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_resolved_type_name
        )

    @partial_resolved_type_name.setter
    def partial_resolved_type_name(self, partial_resolved_type_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_resolved_type_name = partial_resolved_type_name

    @property
    def partial_unknown_attributes_hash_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_unknown_attributes_hash_id
        )

    @partial_unknown_attributes_hash_id.setter
    def partial_unknown_attributes_hash_id(
        self, partial_unknown_attributes_hash_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_unknown_attributes_hash_id = (
            partial_unknown_attributes_hash_id
        )

    @property
    def partial_parent_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partial_parent_type

    @partial_parent_type.setter
    def partial_parent_type(self, partial_parent_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_parent_type = partial_parent_type

    @property
    def partial_parent_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_parent_qualified_name
        )

    @partial_parent_qualified_name.setter
    def partial_parent_qualified_name(
        self, partial_parent_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_parent_qualified_name = partial_parent_qualified_name

    class Attributes(Catalog.Attributes):
        partial_structure_j_s_o_n: Optional[str] = Field(default=None, description="")
        partial_resolved_type_name: Optional[str] = Field(default=None, description="")
        partial_unknown_attributes_hash_id: Optional[str] = Field(
            default=None, description=""
        )
        partial_parent_type: Optional[str] = Field(default=None, description="")
        partial_parent_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: Partial.Attributes = Field(
        default_factory=lambda: Partial.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
