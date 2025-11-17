# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DremioParentAssetType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .dremio import Dremio


class DremioFolder(Dremio):
    """Description"""

    type_name: str = Field(default="DremioFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DremioFolder":
            raise ValueError("must be DremioFolder")
        return v

    def __setattr__(self, name, value):
        if name in DremioFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DREMIO_PARENT_ASSET_TYPE: ClassVar[KeywordField] = KeywordField(
        "dremioParentAssetType", "dremioParentAssetType"
    )
    """
    Type of top level asset that contains this folder.
    """

    DREMIO_SPACE: ClassVar[RelationField] = RelationField("dremioSpace")
    """
    TBC
    """
    DREMIO_PHYSICAL_DATASETS: ClassVar[RelationField] = RelationField(
        "dremioPhysicalDatasets"
    )
    """
    TBC
    """
    DREMIO_PARENT_FOLDER: ClassVar[RelationField] = RelationField("dremioParentFolder")
    """
    TBC
    """
    DREMIO_SUB_FOLDERS: ClassVar[RelationField] = RelationField("dremioSubFolders")
    """
    TBC
    """
    DREMIO_SOURCE: ClassVar[RelationField] = RelationField("dremioSource")
    """
    TBC
    """
    DREMIO_VIRTUAL_DATASETS: ClassVar[RelationField] = RelationField(
        "dremioVirtualDatasets"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dremio_parent_asset_type",
        "dremio_space",
        "dremio_physical_datasets",
        "dremio_parent_folder",
        "dremio_sub_folders",
        "dremio_source",
        "dremio_virtual_datasets",
    ]

    @property
    def dremio_parent_asset_type(self) -> Optional[DremioParentAssetType]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_parent_asset_type
        )

    @dremio_parent_asset_type.setter
    def dremio_parent_asset_type(
        self, dremio_parent_asset_type: Optional[DremioParentAssetType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_parent_asset_type = dremio_parent_asset_type

    @property
    def dremio_space(self) -> Optional[DremioSpace]:
        return None if self.attributes is None else self.attributes.dremio_space

    @dremio_space.setter
    def dremio_space(self, dremio_space: Optional[DremioSpace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_space = dremio_space

    @property
    def dremio_physical_datasets(self) -> Optional[List[DremioPhysicalDataset]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_physical_datasets
        )

    @dremio_physical_datasets.setter
    def dremio_physical_datasets(
        self, dremio_physical_datasets: Optional[List[DremioPhysicalDataset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_physical_datasets = dremio_physical_datasets

    @property
    def dremio_parent_folder(self) -> Optional[DremioFolder]:
        return None if self.attributes is None else self.attributes.dremio_parent_folder

    @dremio_parent_folder.setter
    def dremio_parent_folder(self, dremio_parent_folder: Optional[DremioFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_parent_folder = dremio_parent_folder

    @property
    def dremio_sub_folders(self) -> Optional[List[DremioFolder]]:
        return None if self.attributes is None else self.attributes.dremio_sub_folders

    @dremio_sub_folders.setter
    def dremio_sub_folders(self, dremio_sub_folders: Optional[List[DremioFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_sub_folders = dremio_sub_folders

    @property
    def dremio_source(self) -> Optional[DremioSource]:
        return None if self.attributes is None else self.attributes.dremio_source

    @dremio_source.setter
    def dremio_source(self, dremio_source: Optional[DremioSource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source = dremio_source

    @property
    def dremio_virtual_datasets(self) -> Optional[List[DremioVirtualDataset]]:
        return (
            None if self.attributes is None else self.attributes.dremio_virtual_datasets
        )

    @dremio_virtual_datasets.setter
    def dremio_virtual_datasets(
        self, dremio_virtual_datasets: Optional[List[DremioVirtualDataset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_virtual_datasets = dremio_virtual_datasets

    class Attributes(Dremio.Attributes):
        dremio_parent_asset_type: Optional[DremioParentAssetType] = Field(
            default=None, description=""
        )
        dremio_space: Optional[DremioSpace] = Field(
            default=None, description=""
        )  # relationship
        dremio_physical_datasets: Optional[List[DremioPhysicalDataset]] = Field(
            default=None, description=""
        )  # relationship
        dremio_parent_folder: Optional[DremioFolder] = Field(
            default=None, description=""
        )  # relationship
        dremio_sub_folders: Optional[List[DremioFolder]] = Field(
            default=None, description=""
        )  # relationship
        dremio_source: Optional[DremioSource] = Field(
            default=None, description=""
        )  # relationship
        dremio_virtual_datasets: Optional[List[DremioVirtualDataset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DremioFolder.Attributes = Field(
        default_factory=lambda: DremioFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dremio_physical_dataset import DremioPhysicalDataset  # noqa: E402, F401
from .dremio_source import DremioSource  # noqa: E402, F401
from .dremio_space import DremioSpace  # noqa: E402, F401
from .dremio_virtual_dataset import DremioVirtualDataset  # noqa: E402, F401

DremioFolder.Attributes.update_forward_refs()
