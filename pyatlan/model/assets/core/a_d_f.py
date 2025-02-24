# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import TextField

from .catalog import Catalog


class ADF(Catalog):
    """Description"""

    type_name: str = Field(default="ADF", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADF":
            raise ValueError("must be ADF")
        return v

    def __setattr__(self, name, value):
        if name in ADF._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADF_FACTORY_NAME: ClassVar[TextField] = TextField(
        "adfFactoryName", "adfFactoryName"
    )
    """
    Defines the name of the factory in which this asset exists.
    """
    ADF_ASSET_FOLDER_PATH: ClassVar[TextField] = TextField(
        "adfAssetFolderPath", "adfAssetFolderPath"
    )
    """
    Defines the folder path in which this ADF asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adf_factory_name",
        "adf_asset_folder_path",
    ]

    @property
    def adf_factory_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adf_factory_name

    @adf_factory_name.setter
    def adf_factory_name(self, adf_factory_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_factory_name = adf_factory_name

    @property
    def adf_asset_folder_path(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adf_asset_folder_path
        )

    @adf_asset_folder_path.setter
    def adf_asset_folder_path(self, adf_asset_folder_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_asset_folder_path = adf_asset_folder_path

    class Attributes(Catalog.Attributes):
        adf_factory_name: Optional[str] = Field(default=None, description="")
        adf_asset_folder_path: Optional[str] = Field(default=None, description="")

    attributes: ADF.Attributes = Field(
        default_factory=lambda: ADF.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
