# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .databricks import Databricks


class DatabricksVolumePath(Databricks):
    """Description"""

    type_name: str = Field(default="DatabricksVolumePath", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DatabricksVolumePath":
            raise ValueError("must be DatabricksVolumePath")
        return v

    def __setattr__(self, name, value):
        if name in DatabricksVolumePath._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATABRICKS_VOLUME_PATH_PATH: ClassVar[KeywordField] = KeywordField(
        "databricksVolumePathPath", "databricksVolumePathPath"
    )
    """
    Path of data on the volume.
    """
    DATABRICKS_VOLUME_PATH_VOLUME_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databricksVolumePathVolumeQualifiedName",
        "databricksVolumePathVolumeQualifiedName",
    )
    """
    Qualified name of the parent volume.
    """
    DATABRICKS_VOLUME_PATH_VOLUME_NAME: ClassVar[KeywordField] = KeywordField(
        "databricksVolumePathVolumeName", "databricksVolumePathVolumeName"
    )
    """
    Name of the parent volume.
    """

    DATABRICKS_VOLUME: ClassVar[RelationField] = RelationField("databricksVolume")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "databricks_volume_path_path",
        "databricks_volume_path_volume_qualified_name",
        "databricks_volume_path_volume_name",
        "databricks_volume",
    ]

    @property
    def databricks_volume_path_path(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_volume_path_path
        )

    @databricks_volume_path_path.setter
    def databricks_volume_path_path(self, databricks_volume_path_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_path_path = databricks_volume_path_path

    @property
    def databricks_volume_path_volume_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_volume_path_volume_qualified_name
        )

    @databricks_volume_path_volume_qualified_name.setter
    def databricks_volume_path_volume_qualified_name(
        self, databricks_volume_path_volume_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_path_volume_qualified_name = (
            databricks_volume_path_volume_qualified_name
        )

    @property
    def databricks_volume_path_volume_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_volume_path_volume_name
        )

    @databricks_volume_path_volume_name.setter
    def databricks_volume_path_volume_name(
        self, databricks_volume_path_volume_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_path_volume_name = (
            databricks_volume_path_volume_name
        )

    @property
    def databricks_volume(self) -> Optional[DatabricksVolume]:
        return None if self.attributes is None else self.attributes.databricks_volume

    @databricks_volume.setter
    def databricks_volume(self, databricks_volume: Optional[DatabricksVolume]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume = databricks_volume

    class Attributes(Databricks.Attributes):
        databricks_volume_path_path: Optional[str] = Field(default=None, description="")
        databricks_volume_path_volume_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        databricks_volume_path_volume_name: Optional[str] = Field(
            default=None, description=""
        )
        databricks_volume: Optional[DatabricksVolume] = Field(
            default=None, description=""
        )  # relationship

    attributes: DatabricksVolumePath.Attributes = Field(
        default_factory=lambda: DatabricksVolumePath.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .databricks_volume import DatabricksVolume  # noqa: E402, F401
