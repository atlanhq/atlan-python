# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .s_s_r_s import SSRS


class SSRSFolder(SSRS):
    """Description"""

    type_name: str = Field(default="SSRSFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SSRSFolder":
            raise ValueError("must be SSRSFolder")
        return v

    def __setattr__(self, name, value):
        if name in SSRSFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SSRS_REPORTS: ClassVar[RelationField] = RelationField("ssrsReports")
    """
    TBC
    """
    SSRS_PARENT_FOLDER: ClassVar[RelationField] = RelationField("ssrsParentFolder")
    """
    TBC
    """
    SSRS_SUB_FOLDERS: ClassVar[RelationField] = RelationField("ssrsSubFolders")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ssrs_reports",
        "ssrs_parent_folder",
        "ssrs_sub_folders",
    ]

    @property
    def ssrs_reports(self) -> Optional[List[SSRSReport]]:
        return None if self.attributes is None else self.attributes.ssrs_reports

    @ssrs_reports.setter
    def ssrs_reports(self, ssrs_reports: Optional[List[SSRSReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_reports = ssrs_reports

    @property
    def ssrs_parent_folder(self) -> Optional[SSRSFolder]:
        return None if self.attributes is None else self.attributes.ssrs_parent_folder

    @ssrs_parent_folder.setter
    def ssrs_parent_folder(self, ssrs_parent_folder: Optional[SSRSFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_parent_folder = ssrs_parent_folder

    @property
    def ssrs_sub_folders(self) -> Optional[List[SSRSFolder]]:
        return None if self.attributes is None else self.attributes.ssrs_sub_folders

    @ssrs_sub_folders.setter
    def ssrs_sub_folders(self, ssrs_sub_folders: Optional[List[SSRSFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_sub_folders = ssrs_sub_folders

    class Attributes(SSRS.Attributes):
        ssrs_reports: Optional[List[SSRSReport]] = Field(
            default=None, description=""
        )  # relationship
        ssrs_parent_folder: Optional[SSRSFolder] = Field(
            default=None, description=""
        )  # relationship
        ssrs_sub_folders: Optional[List[SSRSFolder]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SSRSFolder.Attributes = Field(
        default_factory=lambda: SSRSFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_s_r_s_report import SSRSReport  # noqa: E402, F401

SSRSFolder.Attributes.update_forward_refs()
