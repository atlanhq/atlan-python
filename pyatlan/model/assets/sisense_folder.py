# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField

from .sisense import Sisense


class SisenseFolder(Sisense):
    """Description"""

    type_name: str = Field(default="SisenseFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseFolder":
            raise ValueError("must be SisenseFolder")
        return v

    def __setattr__(self, name, value):
        if name in SisenseFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_FOLDER_PARENT_FOLDER_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "sisenseFolderParentFolderQualifiedName",
            "sisenseFolderParentFolderQualifiedName",
            "sisenseFolderParentFolderQualifiedName.text",
        )
    )
    """
    Unique name of the parent folder in which this folder exists.
    """

    SISENSE_CHILD_FOLDERS: ClassVar[RelationField] = RelationField(
        "sisenseChildFolders"
    )
    """
    TBC
    """
    SISENSE_WIDGETS: ClassVar[RelationField] = RelationField("sisenseWidgets")
    """
    TBC
    """
    SISENSE_DASHBOARDS: ClassVar[RelationField] = RelationField("sisenseDashboards")
    """
    TBC
    """
    SISENSE_PARENT_FOLDER: ClassVar[RelationField] = RelationField(
        "sisenseParentFolder"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sisense_folder_parent_folder_qualified_name",
        "sisense_child_folders",
        "sisense_widgets",
        "sisense_dashboards",
        "sisense_parent_folder",
    ]

    @property
    def sisense_folder_parent_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_folder_parent_folder_qualified_name
        )

    @sisense_folder_parent_folder_qualified_name.setter
    def sisense_folder_parent_folder_qualified_name(
        self, sisense_folder_parent_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_folder_parent_folder_qualified_name = (
            sisense_folder_parent_folder_qualified_name
        )

    @property
    def sisense_child_folders(self) -> Optional[List[SisenseFolder]]:
        return (
            None if self.attributes is None else self.attributes.sisense_child_folders
        )

    @sisense_child_folders.setter
    def sisense_child_folders(
        self, sisense_child_folders: Optional[List[SisenseFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_child_folders = sisense_child_folders

    @property
    def sisense_widgets(self) -> Optional[List[SisenseWidget]]:
        return None if self.attributes is None else self.attributes.sisense_widgets

    @sisense_widgets.setter
    def sisense_widgets(self, sisense_widgets: Optional[List[SisenseWidget]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widgets = sisense_widgets

    @property
    def sisense_dashboards(self) -> Optional[List[SisenseDashboard]]:
        return None if self.attributes is None else self.attributes.sisense_dashboards

    @sisense_dashboards.setter
    def sisense_dashboards(self, sisense_dashboards: Optional[List[SisenseDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboards = sisense_dashboards

    @property
    def sisense_parent_folder(self) -> Optional[SisenseFolder]:
        return (
            None if self.attributes is None else self.attributes.sisense_parent_folder
        )

    @sisense_parent_folder.setter
    def sisense_parent_folder(self, sisense_parent_folder: Optional[SisenseFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_parent_folder = sisense_parent_folder

    class Attributes(Sisense.Attributes):
        sisense_folder_parent_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sisense_child_folders: Optional[List[SisenseFolder]] = Field(
            default=None, description=""
        )  # relationship
        sisense_widgets: Optional[List[SisenseWidget]] = Field(
            default=None, description=""
        )  # relationship
        sisense_dashboards: Optional[List[SisenseDashboard]] = Field(
            default=None, description=""
        )  # relationship
        sisense_parent_folder: Optional[SisenseFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: SisenseFolder.Attributes = Field(
        default_factory=lambda: SisenseFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sisense_dashboard import SisenseDashboard  # noqa
from .sisense_widget import SisenseWidget  # noqa
