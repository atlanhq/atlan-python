# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AgenticSource, FileType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .knowledge import Knowledge


class KnowledgeFile(Knowledge):
    """Description"""

    type_name: str = Field(default="KnowledgeFile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KnowledgeFile":
            raise ValueError("must be KnowledgeFile")
        return v

    def __setattr__(self, name, value):
        if name in KnowledgeFile._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    KNOWLEDGE_CONTENT_HASH: ClassVar[KeywordField] = KeywordField(
        "knowledgeContentHash", "knowledgeContentHash"
    )
    """
    SHA-256 hex digest of file content, used for deduplication.
    """
    KNOWLEDGE_FOLDER_NAMES: ClassVar[KeywordField] = KeywordField(
        "knowledgeFolderNames", "knowledgeFolderNames"
    )
    """
    Display names of the knowledge folders containing this file.
    """
    KNOWLEDGE_CONTENT_VERSION_ID: ClassVar[KeywordField] = KeywordField(
        "knowledgeContentVersionId", "knowledgeContentVersionId"
    )
    """
    Provider-specific version identifier for the active file content (e.g., S3 VersionId, GCS generation number). Use with filePath to retrieve exact bytes at a point in time.
    """  # noqa: E501
    AGENTIC_VERSION: ClassVar[NumericField] = NumericField(
        "agenticVersion", "agenticVersion"
    )
    """
    Version of this agentic asset as an epoch-millisecond timestamp. One Atlan entity per (slug, version) tuple.
    """
    AGENTIC_SOURCE: ClassVar[KeywordField] = KeywordField(
        "agenticSource", "agenticSource"
    )
    """
    Product surface this agentic asset was created from, so agents and skills can be attributed to their originating surface without slug pattern matching (AUT-1074). Mirrors AtlanAppWorkflow.source, which does the same for workflows (AUT-1028).
    """  # noqa: E501
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
    """
    FILE_TYPE: ClassVar[KeywordField] = KeywordField("fileType", "fileType")
    """
    Type (extension) of the file.
    """
    FILE_PATH: ClassVar[TextField] = TextField("filePath", "filePath")
    """
    URL giving the online location where the file can be accessed.
    """
    RESOURCE_FILE_SIZE: ClassVar[NumericField] = NumericField(
        "resourceFileSize", "resourceFileSize"
    )
    """
    Size of the file in bytes.
    """
    LINK: ClassVar[TextField] = TextField("link", "link")
    """
    URL to the resource.
    """
    IS_GLOBAL: ClassVar[BooleanField] = BooleanField("isGlobal", "isGlobal")
    """
    Whether the resource is global (true) or not (false).
    """
    REFERENCE: ClassVar[TextField] = TextField("reference", "reference")
    """
    Reference to the resource.
    """
    RESOURCE_METADATA: ClassVar[KeywordField] = KeywordField(
        "resourceMetadata", "resourceMetadata"
    )
    """
    Metadata of the resource.
    """

    FILE_ASSETS: ClassVar[RelationField] = RelationField("fileAssets")
    """
    TBC
    """
    KNOWLEDGE_FOLDERS: ClassVar[RelationField] = RelationField("knowledgeFolders")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "knowledge_content_hash",
        "knowledge_folder_names",
        "knowledge_content_version_id",
        "agentic_version",
        "agentic_source",
        "catalog_dataset_guid",
        "file_type",
        "file_path",
        "resource_file_size",
        "link",
        "is_global",
        "reference",
        "resource_metadata",
        "file_assets",
        "knowledge_folders",
    ]

    @property
    def knowledge_content_hash(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.knowledge_content_hash
        )

    @knowledge_content_hash.setter
    def knowledge_content_hash(self, knowledge_content_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.knowledge_content_hash = knowledge_content_hash

    @property
    def knowledge_folder_names(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.knowledge_folder_names
        )

    @knowledge_folder_names.setter
    def knowledge_folder_names(self, knowledge_folder_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.knowledge_folder_names = knowledge_folder_names

    @property
    def knowledge_content_version_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.knowledge_content_version_id
        )

    @knowledge_content_version_id.setter
    def knowledge_content_version_id(self, knowledge_content_version_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.knowledge_content_version_id = knowledge_content_version_id

    @property
    def agentic_version(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.agentic_version

    @agentic_version.setter
    def agentic_version(self, agentic_version: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agentic_version = agentic_version

    @property
    def agentic_source(self) -> Optional[AgenticSource]:
        return None if self.attributes is None else self.attributes.agentic_source

    @agentic_source.setter
    def agentic_source(self, agentic_source: Optional[AgenticSource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agentic_source = agentic_source

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

    @property
    def file_type(self) -> Optional[FileType]:
        return None if self.attributes is None else self.attributes.file_type

    @file_type.setter
    def file_type(self, file_type: Optional[FileType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_type = file_type

    @property
    def file_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.file_path

    @file_path.setter
    def file_path(self, file_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_path = file_path

    @property
    def resource_file_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.resource_file_size

    @resource_file_size.setter
    def resource_file_size(self, resource_file_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.resource_file_size = resource_file_size

    @property
    def link(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.link

    @link.setter
    def link(self, link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.link = link

    @property
    def is_global(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_global

    @is_global.setter
    def is_global(self, is_global: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_global = is_global

    @property
    def reference(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.reference

    @reference.setter
    def reference(self, reference: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reference = reference

    @property
    def resource_metadata(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.resource_metadata

    @resource_metadata.setter
    def resource_metadata(self, resource_metadata: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.resource_metadata = resource_metadata

    @property
    def file_assets(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.file_assets

    @file_assets.setter
    def file_assets(self, file_assets: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.file_assets = file_assets

    @property
    def knowledge_folders(self) -> Optional[List[KnowledgeFolder]]:
        return None if self.attributes is None else self.attributes.knowledge_folders

    @knowledge_folders.setter
    def knowledge_folders(self, knowledge_folders: Optional[List[KnowledgeFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.knowledge_folders = knowledge_folders

    class Attributes(Knowledge.Attributes):
        knowledge_content_hash: Optional[str] = Field(default=None, description="")
        knowledge_folder_names: Optional[Set[str]] = Field(default=None, description="")
        knowledge_content_version_id: Optional[str] = Field(
            default=None, description=""
        )
        agentic_version: Optional[int] = Field(default=None, description="")
        agentic_source: Optional[AgenticSource] = Field(default=None, description="")
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
        file_type: Optional[FileType] = Field(default=None, description="")
        file_path: Optional[str] = Field(default=None, description="")
        resource_file_size: Optional[int] = Field(default=None, description="")
        link: Optional[str] = Field(default=None, description="")
        is_global: Optional[bool] = Field(default=None, description="")
        reference: Optional[str] = Field(default=None, description="")
        resource_metadata: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        file_assets: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        knowledge_folders: Optional[List[KnowledgeFolder]] = Field(
            default=None, description=""
        )  # relationship

    attributes: KnowledgeFile.Attributes = Field(
        default_factory=lambda: KnowledgeFile.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.asset import Asset  # noqa: E402, F401
from .knowledge_folder import KnowledgeFolder  # noqa: E402, F401

KnowledgeFile.Attributes.update_forward_refs()
