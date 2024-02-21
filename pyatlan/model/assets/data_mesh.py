# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField

from .catalog import Catalog


class DataMesh(Catalog):
    """Description"""

    type_name: str = Field(default="DataMesh", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataMesh":
            raise ValueError("must be DataMesh")
        return v

    def __setattr__(self, name, value):
        if name in DataMesh._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARENT_DOMAIN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentDomainQualifiedName",
        "parentDomainQualifiedName",
        "parentDomainQualifiedName.text",
    )
    """
    Unique name of the parent domain in which this asset exists.
    """
    SUPER_DOMAIN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "superDomainQualifiedName",
        "superDomainQualifiedName",
        "superDomainQualifiedName.text",
    )
    """
    Unique name of the top-level domain in which this asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "parent_domain_qualified_name",
        "super_domain_qualified_name",
    ]

    @property
    def parent_domain_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.parent_domain_qualified_name
        )

    @parent_domain_qualified_name.setter
    def parent_domain_qualified_name(self, parent_domain_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_domain_qualified_name = parent_domain_qualified_name

    @property
    def super_domain_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.super_domain_qualified_name
        )

    @super_domain_qualified_name.setter
    def super_domain_qualified_name(self, super_domain_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.super_domain_qualified_name = super_domain_qualified_name

    class Attributes(Catalog.Attributes):
        parent_domain_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        super_domain_qualified_name: Optional[str] = Field(default=None, description="")

    attributes: "DataMesh.Attributes" = Field(
        default_factory=lambda: DataMesh.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )
