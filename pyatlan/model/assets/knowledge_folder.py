# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import KnowledgeFolderType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .knowledge import Knowledge


class KnowledgeFolder(Knowledge):
    """Description"""

    type_name: str = Field(default="KnowledgeFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KnowledgeFolder":
            raise ValueError("must be KnowledgeFolder")
        return v

    def __setattr__(self, name, value):
        if name in KnowledgeFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    KNOWLEDGE_FOLDER_TYPE: ClassVar[KeywordField] = KeywordField(
        "knowledgeFolderType", "knowledgeFolderType"
    )
    """
    Type of this folder based on how it was created and how it is managed.
    """

    KNOWLEDGE_FILES: ClassVar[RelationField] = RelationField("knowledgeFiles")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "knowledge_folder_type",
        "knowledge_files",
    ]

    @property
    def knowledge_folder_type(self) -> Optional[KnowledgeFolderType]:
        return (
            None if self.attributes is None else self.attributes.knowledge_folder_type
        )

    @knowledge_folder_type.setter
    def knowledge_folder_type(
        self, knowledge_folder_type: Optional[KnowledgeFolderType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.knowledge_folder_type = knowledge_folder_type

    @property
    def knowledge_files(self) -> Optional[List[KnowledgeFile]]:
        return None if self.attributes is None else self.attributes.knowledge_files

    @knowledge_files.setter
    def knowledge_files(self, knowledge_files: Optional[List[KnowledgeFile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.knowledge_files = knowledge_files

    class Attributes(Knowledge.Attributes):
        knowledge_folder_type: Optional[KnowledgeFolderType] = Field(
            default=None, description=""
        )
        knowledge_files: Optional[List[KnowledgeFile]] = Field(
            default=None, description=""
        )  # relationship

    attributes: KnowledgeFolder.Attributes = Field(
        default_factory=lambda: KnowledgeFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .knowledge_file import KnowledgeFile  # noqa: E402, F401

KnowledgeFolder.Attributes.update_forward_refs()
