# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField

from .b_i import BI


class Metabase(BI):
    """Description"""

    type_name: str = Field(default="Metabase", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Metabase":
            raise ValueError("must be Metabase")
        return v

    def __setattr__(self, name, value):
        if name in Metabase._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    METABASE_COLLECTION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseCollectionName",
        "metabaseCollectionName.keyword",
        "metabaseCollectionName",
    )
    """
    Simple name of the Metabase collection in which this asset exists.
    """
    METABASE_COLLECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "metabaseCollectionQualifiedName",
        "metabaseCollectionQualifiedName",
        "metabaseCollectionQualifiedName.text",
    )
    """
    Unique name of the Metabase collection in which this asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "metabase_collection_name",
        "metabase_collection_qualified_name",
    ]

    @property
    def metabase_collection_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_collection_name
        )

    @metabase_collection_name.setter
    def metabase_collection_name(self, metabase_collection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_name = metabase_collection_name

    @property
    def metabase_collection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.metabase_collection_qualified_name
        )

    @metabase_collection_qualified_name.setter
    def metabase_collection_qualified_name(
        self, metabase_collection_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metabase_collection_qualified_name = (
            metabase_collection_qualified_name
        )

    class Attributes(BI.Attributes):
        metabase_collection_name: Optional[str] = Field(default=None, description="")
        metabase_collection_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: Metabase.Attributes = Field(
        default_factory=lambda: Metabase.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
