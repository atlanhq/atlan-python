# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.s_q_l import SQL


class Iceberg(SQL):
    """Description"""

    type_name: str = Field(default="Iceberg", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Iceberg":
            raise ValueError("must be Iceberg")
        return v

    def __setattr__(self, name, value):
        if name in Iceberg._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ICEBERG_PARENT_NAMESPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "icebergParentNamespaceQualifiedName", "icebergParentNamespaceQualifiedName"
    )
    """
    Unique name of the immediate parent namespace in which this asset exists.
    """
    ICEBERG_NAMESPACE_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "icebergNamespaceHierarchy", "icebergNamespaceHierarchy"
    )
    """
    Ordered array of namespace assets with qualified name and name representing the complete namespace hierarchy path for this asset, from immediate parent to root namespace.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "iceberg_parent_namespace_qualified_name",
        "iceberg_namespace_hierarchy",
    ]

    @property
    def iceberg_parent_namespace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_parent_namespace_qualified_name
        )

    @iceberg_parent_namespace_qualified_name.setter
    def iceberg_parent_namespace_qualified_name(
        self, iceberg_parent_namespace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_parent_namespace_qualified_name = (
            iceberg_parent_namespace_qualified_name
        )

    @property
    def iceberg_namespace_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.iceberg_namespace_hierarchy
        )

    @iceberg_namespace_hierarchy.setter
    def iceberg_namespace_hierarchy(
        self, iceberg_namespace_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.iceberg_namespace_hierarchy = iceberg_namespace_hierarchy

    class Attributes(SQL.Attributes):
        iceberg_parent_namespace_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        iceberg_namespace_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )

    attributes: Iceberg.Attributes = Field(
        default_factory=lambda: Iceberg.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Iceberg.Attributes.update_forward_refs()
