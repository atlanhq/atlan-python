# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.s_q_l import SQL


class Dremio(SQL):
    """Description"""

    type_name: str = Field(default="Dremio", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Dremio":
            raise ValueError("must be Dremio")
        return v

    def __setattr__(self, name, value):
        if name in Dremio._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DREMIO_ID: ClassVar[KeywordField] = KeywordField("dremioId", "dremioId")
    """
    Source ID of this asset in Dremio.
    """
    DREMIO_SPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSpaceQualifiedName", "dremioSpaceQualifiedName"
    )
    """
    Unique qualified name of the Dremio Space containing this asset.
    """
    DREMIO_SPACE_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSpaceName", "dremioSpaceName"
    )
    """
    Simple name of the Dremio Space containing this asset.
    """
    DREMIO_SOURCE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSourceQualifiedName", "dremioSourceQualifiedName"
    )
    """
    Unique qualified name of the Dremio Source containing this asset.
    """
    DREMIO_SOURCE_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioSourceName", "dremioSourceName"
    )
    """
    Simple name of the Dremio Source containing this asset.
    """
    DREMIO_PARENT_FOLDER_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dremioParentFolderQualifiedName", "dremioParentFolderQualifiedName"
    )
    """
    Unique qualified name of the immediate parent folder containing this asset.
    """
    DREMIO_FOLDER_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "dremioFolderHierarchy", "dremioFolderHierarchy"
    )
    """
    Ordered array of folder assets with qualified name and name representing the complete folder hierarchy path for this asset, from immediate parent to root folder.
    """  # noqa: E501
    DREMIO_LABELS: ClassVar[KeywordField] = KeywordField("dremioLabels", "dremioLabels")
    """
    Dremio Labels associated with this asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dremio_id",
        "dremio_space_qualified_name",
        "dremio_space_name",
        "dremio_source_qualified_name",
        "dremio_source_name",
        "dremio_parent_folder_qualified_name",
        "dremio_folder_hierarchy",
        "dremio_labels",
    ]

    @property
    def dremio_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dremio_id

    @dremio_id.setter
    def dremio_id(self, dremio_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_id = dremio_id

    @property
    def dremio_space_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_space_qualified_name
        )

    @dremio_space_qualified_name.setter
    def dremio_space_qualified_name(self, dremio_space_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_space_qualified_name = dremio_space_qualified_name

    @property
    def dremio_space_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dremio_space_name

    @dremio_space_name.setter
    def dremio_space_name(self, dremio_space_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_space_name = dremio_space_name

    @property
    def dremio_source_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_source_qualified_name
        )

    @dremio_source_qualified_name.setter
    def dremio_source_qualified_name(self, dremio_source_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_qualified_name = dremio_source_qualified_name

    @property
    def dremio_source_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dremio_source_name

    @dremio_source_name.setter
    def dremio_source_name(self, dremio_source_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_name = dremio_source_name

    @property
    def dremio_parent_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_parent_folder_qualified_name
        )

    @dremio_parent_folder_qualified_name.setter
    def dremio_parent_folder_qualified_name(
        self, dremio_parent_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_parent_folder_qualified_name = (
            dremio_parent_folder_qualified_name
        )

    @property
    def dremio_folder_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.dremio_folder_hierarchy
        )

    @dremio_folder_hierarchy.setter
    def dremio_folder_hierarchy(
        self, dremio_folder_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_folder_hierarchy = dremio_folder_hierarchy

    @property
    def dremio_labels(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.dremio_labels

    @dremio_labels.setter
    def dremio_labels(self, dremio_labels: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_labels = dremio_labels

    class Attributes(SQL.Attributes):
        dremio_id: Optional[str] = Field(default=None, description="")
        dremio_space_qualified_name: Optional[str] = Field(default=None, description="")
        dremio_space_name: Optional[str] = Field(default=None, description="")
        dremio_source_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dremio_source_name: Optional[str] = Field(default=None, description="")
        dremio_parent_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dremio_folder_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        dremio_labels: Optional[Set[str]] = Field(default=None, description="")

    attributes: Dremio.Attributes = Field(
        default_factory=lambda: Dremio.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Dremio.Attributes.update_forward_refs()
