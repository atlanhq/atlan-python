# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .namespace import Namespace


class Folder(Namespace):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        collection_qualified_name: str,
    ) -> Folder: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_folder_qualified_name: str,
    ) -> Folder: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        collection_qualified_name: Optional[str] = None,
        parent_folder_qualified_name: Optional[str] = None,
    ) -> Folder:
        validate_required_fields(["name"], [name])
        return Folder(
            attributes=Folder.Attributes.creator(
                name=name,
                collection_qualified_name=collection_qualified_name,
                parent_folder_qualified_name=parent_folder_qualified_name,
            )
        )

    type_name: str = Field(default="Folder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Folder":
            raise ValueError("must be Folder")
        return v

    def __setattr__(self, name, value):
        if name in Folder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "parentQualifiedName", "parentQualifiedName", "parentQualifiedName.text"
    )
    """
    Unique name of the parent folder or collection in which this folder exists.
    """
    COLLECTION_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "collectionQualifiedName",
        "collectionQualifiedName",
        "collectionQualifiedName.text",
    )
    """
    Unique name of the collection in which this folder exists.
    """

    PARENT: ClassVar[RelationField] = RelationField("parent")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "parent_qualified_name",
        "collection_qualified_name",
        "parent",
    ]

    @property
    def parent_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.parent_qualified_name
        )

    @parent_qualified_name.setter
    def parent_qualified_name(self, parent_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_qualified_name = parent_qualified_name

    @property
    def collection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.collection_qualified_name
        )

    @collection_qualified_name.setter
    def collection_qualified_name(self, collection_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.collection_qualified_name = collection_qualified_name

    @property
    def parent(self) -> Optional[Namespace]:
        return None if self.attributes is None else self.attributes.parent

    @parent.setter
    def parent(self, parent: Optional[Namespace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent = parent

    class Attributes(Namespace.Attributes):
        parent_qualified_name: Optional[str] = Field(default=None, description="")
        collection_qualified_name: Optional[str] = Field(default=None, description="")
        parent: Optional[Namespace] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            collection_qualified_name: Optional[str] = None,
            parent_folder_qualified_name: Optional[str] = None,
        ) -> Folder.Attributes:
            from pyatlan.model.assets import Collection

            validate_required_fields(["name"], [name])

            if not (parent_folder_qualified_name or collection_qualified_name):
                raise ValueError(
                    "Either 'collection_qualified_name' or 'parent_folder_qualified_name' to be specified."
                )

            if not parent_folder_qualified_name:
                qualified_name = f"{collection_qualified_name}/{name}"
                parent_qn = collection_qualified_name
                parent = Collection.ref_by_qualified_name(
                    collection_qualified_name or ""
                )

            else:
                tokens = parent_folder_qualified_name.split("/")
                if len(tokens) < 4:
                    raise ValueError("Invalid collection_qualified_name")
                collection_qualified_name = (
                    f"{tokens[0]}/{tokens[1]}/{tokens[2]}/{tokens[3]}"
                )
                qualified_name = f"{parent_folder_qualified_name}/{name}"
                parent_qn = parent_folder_qualified_name
                parent = Folder.ref_by_qualified_name(parent_folder_qualified_name)  # type: ignore[assignment]

            return Folder.Attributes(
                name=name,
                qualified_name=qualified_name,
                collection_qualified_name=collection_qualified_name,
                parent=parent,
                parent_qualified_name=parent_qn,
            )

    attributes: Folder.Attributes = Field(
        default_factory=lambda: Folder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .namespace import Namespace  # noqa: E402, F401
