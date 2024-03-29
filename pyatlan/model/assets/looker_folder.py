# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .looker import Looker


class LookerFolder(Looker):
    """Description"""

    type_name: str = Field(default="LookerFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerFolder":
            raise ValueError("must be LookerFolder")
        return v

    def __setattr__(self, name, value):
        if name in LookerFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_CONTENT_METADATA_ID: ClassVar[NumericField] = NumericField(
        "sourceContentMetadataId", "sourceContentMetadataId"
    )
    """
    Identifier for the folder's content metadata in Looker.
    """
    SOURCE_CREATOR_ID: ClassVar[NumericField] = NumericField(
        "sourceCreatorId", "sourceCreatorId"
    )
    """
    Identifier of the user who created the folder, from Looker.
    """
    SOURCE_CHILD_COUNT: ClassVar[NumericField] = NumericField(
        "sourceChildCount", "sourceChildCount"
    )
    """
    Number of subfolders in this folder.
    """
    SOURCE_PARENT_ID: ClassVar[NumericField] = NumericField(
        "sourceParentID", "sourceParentID"
    )
    """
    Identifier of the parent folder of this folder, from Looker.
    """

    LOOKER_SUB_FOLDERS: ClassVar[RelationField] = RelationField("lookerSubFolders")
    """
    TBC
    """
    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """
    LOOKS: ClassVar[RelationField] = RelationField("looks")
    """
    TBC
    """
    LOOKER_PARENT_FOLDER: ClassVar[RelationField] = RelationField("lookerParentFolder")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "source_content_metadata_id",
        "source_creator_id",
        "source_child_count",
        "source_parent_i_d",
        "looker_sub_folders",
        "dashboards",
        "looks",
        "looker_parent_folder",
    ]

    @property
    def source_content_metadata_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_content_metadata_id
        )

    @source_content_metadata_id.setter
    def source_content_metadata_id(self, source_content_metadata_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_content_metadata_id = source_content_metadata_id

    @property
    def source_creator_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_creator_id

    @source_creator_id.setter
    def source_creator_id(self, source_creator_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_creator_id = source_creator_id

    @property
    def source_child_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_child_count

    @source_child_count.setter
    def source_child_count(self, source_child_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_child_count = source_child_count

    @property
    def source_parent_i_d(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.source_parent_i_d

    @source_parent_i_d.setter
    def source_parent_i_d(self, source_parent_i_d: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_parent_i_d = source_parent_i_d

    @property
    def looker_sub_folders(self) -> Optional[List[LookerFolder]]:
        return None if self.attributes is None else self.attributes.looker_sub_folders

    @looker_sub_folders.setter
    def looker_sub_folders(self, looker_sub_folders: Optional[List[LookerFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_sub_folders = looker_sub_folders

    @property
    def dashboards(self) -> Optional[List[LookerDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[List[LookerDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def looks(self) -> Optional[List[LookerLook]]:
        return None if self.attributes is None else self.attributes.looks

    @looks.setter
    def looks(self, looks: Optional[List[LookerLook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looks = looks

    @property
    def looker_parent_folder(self) -> Optional[LookerFolder]:
        return None if self.attributes is None else self.attributes.looker_parent_folder

    @looker_parent_folder.setter
    def looker_parent_folder(self, looker_parent_folder: Optional[LookerFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_parent_folder = looker_parent_folder

    class Attributes(Looker.Attributes):
        source_content_metadata_id: Optional[int] = Field(default=None, description="")
        source_creator_id: Optional[int] = Field(default=None, description="")
        source_child_count: Optional[int] = Field(default=None, description="")
        source_parent_i_d: Optional[int] = Field(default=None, description="")
        looker_sub_folders: Optional[List[LookerFolder]] = Field(
            default=None, description=""
        )  # relationship
        dashboards: Optional[List[LookerDashboard]] = Field(
            default=None, description=""
        )  # relationship
        looks: Optional[List[LookerLook]] = Field(
            default=None, description=""
        )  # relationship
        looker_parent_folder: Optional[LookerFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerFolder.Attributes = Field(
        default_factory=lambda: LookerFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_dashboard import LookerDashboard  # noqa
from .looker_look import LookerLook  # noqa
