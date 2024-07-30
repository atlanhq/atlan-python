# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField

from .catalog import Catalog


class Resource(Catalog):
    """Description"""

    type_name: str = Field(default="Resource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Resource":
            raise ValueError("must be Resource")
        return v

    def __setattr__(self, name, value):
        if name in Resource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    LINK: ClassVar[KeywordField] = KeywordField("link", "link")
    """
    URL to the resource.
    """
    IS_GLOBAL: ClassVar[BooleanField] = BooleanField("isGlobal", "isGlobal")
    """
    Whether the resource is global (true) or not (false).
    """
    REFERENCE: ClassVar[KeywordField] = KeywordField("reference", "reference")
    """
    Reference to the resource.
    """
    RESOURCE_METADATA: ClassVar[KeywordField] = KeywordField(
        "resourceMetadata", "resourceMetadata"
    )
    """
    Metadata of the resource.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "link",
        "is_global",
        "reference",
        "resource_metadata",
    ]

    @property
    def link(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.link

    @link.setter
    def link(self, link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.link = link

    @property
    def is_global(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_global

    @is_global.setter
    def is_global(self, is_global: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_global = is_global

    @property
    def reference(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.reference

    @reference.setter
    def reference(self, reference: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reference = reference

    @property
    def resource_metadata(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.resource_metadata

    @resource_metadata.setter
    def resource_metadata(self, resource_metadata: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.resource_metadata = resource_metadata

    class Attributes(Catalog.Attributes):
        link: Optional[str] = Field(default=None, description="")
        is_global: Optional[bool] = Field(default=None, description="")
        reference: Optional[str] = Field(default=None, description="")
        resource_metadata: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )

    attributes: Resource.Attributes = Field(
        default_factory=lambda: Resource.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
