# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DatabricksVolumeType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .databricks import Databricks


class DatabricksVolume(Databricks):
    """Description"""

    type_name: str = Field(default="DatabricksVolume", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DatabricksVolume":
            raise ValueError("must be DatabricksVolume")
        return v

    def __setattr__(self, name, value):
        if name in DatabricksVolume._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATABRICKS_VOLUME_OWNER: ClassVar[KeywordField] = KeywordField(
        "databricksVolumeOwner", "databricksVolumeOwner"
    )
    """
    User or group (principal) currently owning the volume.
    """
    DATABRICKS_VOLUME_EXTERNAL_LOCATION: ClassVar[KeywordField] = KeywordField(
        "databricksVolumeExternalLocation", "databricksVolumeExternalLocation"
    )
    """
    The storage location where the volume is created.
    """
    DATABRICKS_VOLUME_TYPE: ClassVar[KeywordField] = KeywordField(
        "databricksVolumeType", "databricksVolumeType"
    )
    """
    Type of the volume.
    """

    DATABRICKS_VOLUME_SCHEMA: ClassVar[RelationField] = RelationField(
        "databricksVolumeSchema"
    )
    """
    TBC
    """
    DATABRICKS_VOLUME_PATHS: ClassVar[RelationField] = RelationField(
        "databricksVolumePaths"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "databricks_volume_owner",
        "databricks_volume_external_location",
        "databricks_volume_type",
        "databricks_volume_schema",
        "databricks_volume_paths",
    ]

    @property
    def databricks_volume_owner(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.databricks_volume_owner
        )

    @databricks_volume_owner.setter
    def databricks_volume_owner(self, databricks_volume_owner: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_owner = databricks_volume_owner

    @property
    def databricks_volume_external_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_volume_external_location
        )

    @databricks_volume_external_location.setter
    def databricks_volume_external_location(
        self, databricks_volume_external_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_external_location = (
            databricks_volume_external_location
        )

    @property
    def databricks_volume_type(self) -> Optional[DatabricksVolumeType]:
        return (
            None if self.attributes is None else self.attributes.databricks_volume_type
        )

    @databricks_volume_type.setter
    def databricks_volume_type(
        self, databricks_volume_type: Optional[DatabricksVolumeType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_type = databricks_volume_type

    @property
    def databricks_volume_schema(self) -> Optional[Schema]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_volume_schema
        )

    @databricks_volume_schema.setter
    def databricks_volume_schema(self, databricks_volume_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_schema = databricks_volume_schema

    @property
    def databricks_volume_paths(self) -> Optional[List[DatabricksVolumePath]]:
        return (
            None if self.attributes is None else self.attributes.databricks_volume_paths
        )

    @databricks_volume_paths.setter
    def databricks_volume_paths(
        self, databricks_volume_paths: Optional[List[DatabricksVolumePath]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_volume_paths = databricks_volume_paths

    class Attributes(Databricks.Attributes):
        databricks_volume_owner: Optional[str] = Field(default=None, description="")
        databricks_volume_external_location: Optional[str] = Field(
            default=None, description=""
        )
        databricks_volume_type: Optional[DatabricksVolumeType] = Field(
            default=None, description=""
        )
        databricks_volume_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        databricks_volume_paths: Optional[List[DatabricksVolumePath]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DatabricksVolume.Attributes = Field(
        default_factory=lambda: DatabricksVolume.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .databricks_volume_path import DatabricksVolumePath  # noqa: E402, F401
from .schema import Schema  # noqa: E402, F401
