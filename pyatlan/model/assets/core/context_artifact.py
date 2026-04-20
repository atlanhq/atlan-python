# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from nanoid import generate as generate_nanoid  # type: ignore
from pydantic.v1 import Field, validator

from pyatlan.model.enums import FileType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .context import Context


class ContextArtifact(Context):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        context_repository_qualified_name: str,
        file_type: FileType,
    ) -> ContextArtifact:
        validate_required_fields(
            ["name", "context_repository_qualified_name", "file_type"],
            [name, context_repository_qualified_name, file_type],
        )
        return ContextArtifact(
            attributes=ContextArtifact.Attributes.creator(
                name=name,
                context_repository_qualified_name=context_repository_qualified_name,
                file_type=file_type,
            )
        )

    type_name: str = Field(default="ContextArtifact", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextArtifact":
            raise ValueError("must be ContextArtifact")
        return v

    def __setattr__(self, name, value):
        if name in ContextArtifact._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONTEXT_REPOSITORY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "contextRepositoryQualifiedName", "contextRepositoryQualifiedName"
    )
    """
    Qualified name of the context repository to which this asset belongs.
    """
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
    """
    ARTIFACT_VERSION: ClassVar[KeywordField] = KeywordField(
        "artifactVersion", "artifactVersion"
    )
    """
    Version identifier for this artifact.
    """
    FILE_TYPE: ClassVar[KeywordField] = KeywordField("fileType", "fileType")
    """
    Type (extension) of the file.
    """
    FILE_PATH: ClassVar[TextField] = TextField("filePath", "filePath")
    """
    URL giving the online location where the file can be accessed.
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
    CONTEXT_REPOSITORY: ClassVar[RelationField] = RelationField("contextRepository")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "context_repository_qualified_name",
        "catalog_dataset_guid",
        "artifact_version",
        "file_type",
        "file_path",
        "link",
        "is_global",
        "reference",
        "resource_metadata",
        "file_assets",
        "context_repository",
    ]

    @property
    def context_repository_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_repository_qualified_name
        )

    @context_repository_qualified_name.setter
    def context_repository_qualified_name(
        self, context_repository_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository_qualified_name = (
            context_repository_qualified_name
        )

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

    @property
    def artifact_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.artifact_version

    @artifact_version.setter
    def artifact_version(self, artifact_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.artifact_version = artifact_version

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
    def context_repository(self) -> Optional[ContextRepository]:
        return None if self.attributes is None else self.attributes.context_repository

    @context_repository.setter
    def context_repository(self, context_repository: Optional[ContextRepository]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository = context_repository

    class Attributes(Context.Attributes):
        context_repository_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
        artifact_version: Optional[str] = Field(default=None, description="")
        file_type: Optional[FileType] = Field(default=None, description="")
        file_path: Optional[str] = Field(default=None, description="")
        link: Optional[str] = Field(default=None, description="")
        is_global: Optional[bool] = Field(default=None, description="")
        reference: Optional[str] = Field(default=None, description="")
        resource_metadata: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        file_assets: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        context_repository: Optional[ContextRepository] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            context_repository_qualified_name: str,
            file_type: FileType,
        ) -> ContextArtifact.Attributes:
            validate_required_fields(
                ["name", "context_repository_qualified_name", "file_type"],
                [name, context_repository_qualified_name, file_type],
            )
            return ContextArtifact.Attributes(
                name=name,
                qualified_name=(
                    f"{context_repository_qualified_name}/artifact/"
                    f"{file_type.value}/{generate_nanoid()}"
                ),
                file_type=file_type,
                context_repository_qualified_name=context_repository_qualified_name,
                context_repository=ContextRepository.ref_by_qualified_name(
                    context_repository_qualified_name
                ),
            )

    attributes: ContextArtifact.Attributes = Field(
        default_factory=lambda: ContextArtifact.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa: E402, F401
from .context_repository import ContextRepository  # noqa: E402, F401
