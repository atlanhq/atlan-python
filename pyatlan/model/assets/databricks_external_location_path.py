# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .core.databricks import Databricks


class DatabricksExternalLocationPath(Databricks):
    """Description"""

    type_name: str = Field(
        default="DatabricksExternalLocationPath", allow_mutation=False
    )

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DatabricksExternalLocationPath":
            raise ValueError("must be DatabricksExternalLocationPath")
        return v

    def __setattr__(self, name, value):
        if name in DatabricksExternalLocationPath._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATABRICKS_PATH: ClassVar[KeywordField] = KeywordField(
        "databricksPath", "databricksPath"
    )
    """
    Path of data at the external location.
    """
    DATABRICKS_PARENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databricksParentQualifiedName", "databricksParentQualifiedName"
    )
    """
    Qualified name of the parent external location.
    """
    DATABRICKS_PARENT_NAME: ClassVar[KeywordField] = KeywordField(
        "databricksParentName", "databricksParentName"
    )
    """
    Name of the parent external location.
    """

    DATABRICKS_EXTERNAL_LOCATION: ClassVar[RelationField] = RelationField(
        "databricksExternalLocation"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "databricks_path",
        "databricks_parent_qualified_name",
        "databricks_parent_name",
        "databricks_external_location",
    ]

    @property
    def databricks_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.databricks_path

    @databricks_path.setter
    def databricks_path(self, databricks_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_path = databricks_path

    @property
    def databricks_parent_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_parent_qualified_name
        )

    @databricks_parent_qualified_name.setter
    def databricks_parent_qualified_name(
        self, databricks_parent_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_parent_qualified_name = (
            databricks_parent_qualified_name
        )

    @property
    def databricks_parent_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.databricks_parent_name
        )

    @databricks_parent_name.setter
    def databricks_parent_name(self, databricks_parent_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_parent_name = databricks_parent_name

    @property
    def databricks_external_location(self) -> Optional[DatabricksExternalLocation]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_external_location
        )

    @databricks_external_location.setter
    def databricks_external_location(
        self, databricks_external_location: Optional[DatabricksExternalLocation]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_external_location = databricks_external_location

    class Attributes(Databricks.Attributes):
        databricks_path: Optional[str] = Field(default=None, description="")
        databricks_parent_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        databricks_parent_name: Optional[str] = Field(default=None, description="")
        databricks_external_location: Optional[DatabricksExternalLocation] = Field(
            default=None, description=""
        )  # relationship

    attributes: DatabricksExternalLocationPath.Attributes = Field(
        default_factory=lambda: DatabricksExternalLocationPath.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .databricks_external_location import DatabricksExternalLocation  # noqa: E402, F401

DatabricksExternalLocationPath.Attributes.update_forward_refs()
