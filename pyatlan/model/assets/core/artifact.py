# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import FileType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    RelationField,
    TextField,
)

from .agentic import Agentic


class Artifact(Agentic):
    """Description"""

    type_name: str = Field(default="Artifact", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Artifact":
            raise ValueError("must be Artifact")
        return v

    def __setattr__(self, name, value):
        if name in Artifact._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ARTIFACT_VERSION: ClassVar[KeywordField] = KeywordField(
        "artifactVersion", "artifactVersion"
    )
    """
    Version identifier for this artifact.
    """
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

    _convenience_properties: ClassVar[List[str]] = [
        "artifact_version",
        "catalog_dataset_guid",
        "file_type",
        "file_path",
        "link",
        "is_global",
        "reference",
        "resource_metadata",
        "file_assets",
    ]

    @property
    def artifact_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.artifact_version

    @artifact_version.setter
    def artifact_version(self, artifact_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.artifact_version = artifact_version

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

    class Attributes(Agentic.Attributes):
        artifact_version: Optional[str] = Field(default=None, description="")
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
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

    attributes: Artifact.Attributes = Field(
        default_factory=lambda: Artifact.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa: E402, F401
