# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .core.flow import Flow


class FlowFolder(Flow):
    """Description"""

    type_name: str = Field(default="FlowFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FlowFolder":
            raise ValueError("must be FlowFolder")
        return v

    def __setattr__(self, name, value):
        if name in FlowFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FLOW_SUB_FOLDERS: ClassVar[RelationField] = RelationField("flowSubFolders")
    """
    TBC
    """
    FLOW_PARENT_FOLDER: ClassVar[RelationField] = RelationField("flowParentFolder")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "flow_sub_folders",
        "flow_parent_folder",
    ]

    @property
    def flow_sub_folders(self) -> Optional[List[FlowFolder]]:
        return None if self.attributes is None else self.attributes.flow_sub_folders

    @flow_sub_folders.setter
    def flow_sub_folders(self, flow_sub_folders: Optional[List[FlowFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_sub_folders = flow_sub_folders

    @property
    def flow_parent_folder(self) -> Optional[FlowFolder]:
        return None if self.attributes is None else self.attributes.flow_parent_folder

    @flow_parent_folder.setter
    def flow_parent_folder(self, flow_parent_folder: Optional[FlowFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_parent_folder = flow_parent_folder

    class Attributes(Flow.Attributes):
        flow_sub_folders: Optional[List[FlowFolder]] = Field(
            default=None, description=""
        )  # relationship
        flow_parent_folder: Optional[FlowFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: FlowFolder.Attributes = Field(
        default_factory=lambda: FlowFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


FlowFolder.Attributes.update_forward_refs()
