# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .cognos import Cognos


class CognosFolder(Cognos):
    """Description"""

    type_name: str = Field(default="CognosFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CognosFolder":
            raise ValueError("must be CognosFolder")
        return v

    def __setattr__(self, name, value):
        if name in CognosFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNOS_FOLDER_SUB_FOLDER_COUNT: ClassVar[NumericField] = NumericField(
        "cognosFolderSubFolderCount", "cognosFolderSubFolderCount"
    )
    """
    Number of sub-folders in the folder.
    """
    COGNOS_FOLDER_CHILD_OBJECTS_COUNT: ClassVar[NumericField] = NumericField(
        "cognosFolderChildObjectsCount", "cognosFolderChildObjectsCount"
    )
    """
    Number of children in the folder (excluding subfolders).
    """

    COGNOS_PACKAGES: ClassVar[RelationField] = RelationField("cognosPackages")
    """
    TBC
    """
    COGNOS_REPORTS: ClassVar[RelationField] = RelationField("cognosReports")
    """
    TBC
    """
    COGNOS_DASHBOARDS: ClassVar[RelationField] = RelationField("cognosDashboards")
    """
    TBC
    """
    COGNOS_SUB_FOLDERS: ClassVar[RelationField] = RelationField("cognosSubFolders")
    """
    TBC
    """
    COGNOS_FOLDER: ClassVar[RelationField] = RelationField("cognosFolder")
    """
    TBC
    """
    COGNOS_MODULES: ClassVar[RelationField] = RelationField("cognosModules")
    """
    TBC
    """
    COGNOS_FILES: ClassVar[RelationField] = RelationField("cognosFiles")
    """
    TBC
    """
    COGNOS_EXPLORATIONS: ClassVar[RelationField] = RelationField("cognosExplorations")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cognos_folder_sub_folder_count",
        "cognos_folder_child_objects_count",
        "cognos_packages",
        "cognos_reports",
        "cognos_dashboards",
        "cognos_sub_folders",
        "cognos_folder",
        "cognos_modules",
        "cognos_files",
        "cognos_explorations",
    ]

    @property
    def cognos_folder_sub_folder_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cognos_folder_sub_folder_count
        )

    @cognos_folder_sub_folder_count.setter
    def cognos_folder_sub_folder_count(
        self, cognos_folder_sub_folder_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_folder_sub_folder_count = cognos_folder_sub_folder_count

    @property
    def cognos_folder_child_objects_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.cognos_folder_child_objects_count
        )

    @cognos_folder_child_objects_count.setter
    def cognos_folder_child_objects_count(
        self, cognos_folder_child_objects_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_folder_child_objects_count = (
            cognos_folder_child_objects_count
        )

    @property
    def cognos_packages(self) -> Optional[List[CognosPackage]]:
        return None if self.attributes is None else self.attributes.cognos_packages

    @cognos_packages.setter
    def cognos_packages(self, cognos_packages: Optional[List[CognosPackage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_packages = cognos_packages

    @property
    def cognos_reports(self) -> Optional[List[CognosReport]]:
        return None if self.attributes is None else self.attributes.cognos_reports

    @cognos_reports.setter
    def cognos_reports(self, cognos_reports: Optional[List[CognosReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_reports = cognos_reports

    @property
    def cognos_dashboards(self) -> Optional[List[CognosDashboard]]:
        return None if self.attributes is None else self.attributes.cognos_dashboards

    @cognos_dashboards.setter
    def cognos_dashboards(self, cognos_dashboards: Optional[List[CognosDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_dashboards = cognos_dashboards

    @property
    def cognos_sub_folders(self) -> Optional[List[CognosFolder]]:
        return None if self.attributes is None else self.attributes.cognos_sub_folders

    @cognos_sub_folders.setter
    def cognos_sub_folders(self, cognos_sub_folders: Optional[List[CognosFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_sub_folders = cognos_sub_folders

    @property
    def cognos_folder(self) -> Optional[CognosFolder]:
        return None if self.attributes is None else self.attributes.cognos_folder

    @cognos_folder.setter
    def cognos_folder(self, cognos_folder: Optional[CognosFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_folder = cognos_folder

    @property
    def cognos_modules(self) -> Optional[List[CognosModule]]:
        return None if self.attributes is None else self.attributes.cognos_modules

    @cognos_modules.setter
    def cognos_modules(self, cognos_modules: Optional[List[CognosModule]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_modules = cognos_modules

    @property
    def cognos_files(self) -> Optional[List[CognosFile]]:
        return None if self.attributes is None else self.attributes.cognos_files

    @cognos_files.setter
    def cognos_files(self, cognos_files: Optional[List[CognosFile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_files = cognos_files

    @property
    def cognos_explorations(self) -> Optional[List[CognosExploration]]:
        return None if self.attributes is None else self.attributes.cognos_explorations

    @cognos_explorations.setter
    def cognos_explorations(
        self, cognos_explorations: Optional[List[CognosExploration]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognos_explorations = cognos_explorations

    class Attributes(Cognos.Attributes):
        cognos_folder_sub_folder_count: Optional[int] = Field(
            default=None, description=""
        )
        cognos_folder_child_objects_count: Optional[int] = Field(
            default=None, description=""
        )
        cognos_packages: Optional[List[CognosPackage]] = Field(
            default=None, description=""
        )  # relationship
        cognos_reports: Optional[List[CognosReport]] = Field(
            default=None, description=""
        )  # relationship
        cognos_dashboards: Optional[List[CognosDashboard]] = Field(
            default=None, description=""
        )  # relationship
        cognos_sub_folders: Optional[List[CognosFolder]] = Field(
            default=None, description=""
        )  # relationship
        cognos_folder: Optional[CognosFolder] = Field(
            default=None, description=""
        )  # relationship
        cognos_modules: Optional[List[CognosModule]] = Field(
            default=None, description=""
        )  # relationship
        cognos_files: Optional[List[CognosFile]] = Field(
            default=None, description=""
        )  # relationship
        cognos_explorations: Optional[List[CognosExploration]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CognosFolder.Attributes = Field(
        default_factory=lambda: CognosFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognos_dashboard import CognosDashboard  # noqa
from .cognos_exploration import CognosExploration  # noqa
from .cognos_file import CognosFile  # noqa
from .cognos_module import CognosModule  # noqa
from .cognos_package import CognosPackage  # noqa
from .cognos_report import CognosReport  # noqa
