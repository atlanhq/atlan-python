# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .core.dremio import Dremio


class DremioSpace(Dremio):
    """Description"""

    type_name: str = Field(default="DremioSpace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DremioSpace":
            raise ValueError("must be DremioSpace")
        return v

    def __setattr__(self, name, value):
        if name in DremioSpace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DREMIO_VIRTUAL_DATASETS: ClassVar[RelationField] = RelationField(
        "dremioVirtualDatasets"
    )
    """
    TBC
    """
    DREMIO_FOLDERS: ClassVar[RelationField] = RelationField("dremioFolders")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dremio_virtual_datasets",
        "dremio_folders",
    ]

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

    @property
    def dremio_folders(self) -> Optional[List[DremioFolder]]:
        return None if self.attributes is None else self.attributes.dremio_folders

    @dremio_folders.setter
    def dremio_folders(self, dremio_folders: Optional[List[DremioFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_folders = dremio_folders

    class Attributes(Dremio.Attributes):
        dremio_virtual_datasets: Optional[List[DremioVirtualDataset]] = Field(
            default=None, description=""
        )  # relationship
        dremio_folders: Optional[List[DremioFolder]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DremioSpace.Attributes = Field(
        default_factory=lambda: DremioSpace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dremio_folder import DremioFolder  # noqa: E402, F401
from .dremio_virtual_dataset import DremioVirtualDataset  # noqa: E402, F401

DremioSpace.Attributes.update_forward_refs()
