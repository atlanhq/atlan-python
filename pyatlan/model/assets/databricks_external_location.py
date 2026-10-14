# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .core.databricks import Databricks


class DatabricksExternalLocation(Databricks):
    """Description"""

    type_name: str = Field(default="DatabricksExternalLocation", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DatabricksExternalLocation":
            raise ValueError("must be DatabricksExternalLocation")
        return v

    def __setattr__(self, name, value):
        if name in DatabricksExternalLocation._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATABRICKS_URL: ClassVar[KeywordField] = KeywordField(
        "databricksUrl", "databricksUrl"
    )
    """
    URL of the external location.
    """
    DATABRICKS_OWNER: ClassVar[KeywordField] = KeywordField(
        "databricksOwner", "databricksOwner"
    )
    """
    User or group (principal) currently owning the external location.
    """

    DATABRICKS_EXTERNAL_LOCATION_PATHS: ClassVar[RelationField] = RelationField(
        "databricksExternalLocationPaths"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "databricks_url",
        "databricks_owner",
        "databricks_external_location_paths",
    ]

    @property
    def databricks_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.databricks_url

    @databricks_url.setter
    def databricks_url(self, databricks_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_url = databricks_url

    @property
    def databricks_owner(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.databricks_owner

    @databricks_owner.setter
    def databricks_owner(self, databricks_owner: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_owner = databricks_owner

    @property
    def databricks_external_location_paths(
        self,
    ) -> Optional[List[DatabricksExternalLocationPath]]:
        return (
            None
            if self.attributes is None
            else self.attributes.databricks_external_location_paths
        )

    @databricks_external_location_paths.setter
    def databricks_external_location_paths(
        self,
        databricks_external_location_paths: Optional[
            List[DatabricksExternalLocationPath]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.databricks_external_location_paths = (
            databricks_external_location_paths
        )

    class Attributes(Databricks.Attributes):
        databricks_url: Optional[str] = Field(default=None, description="")
        databricks_owner: Optional[str] = Field(default=None, description="")
        databricks_external_location_paths: Optional[
            List[DatabricksExternalLocationPath]
        ] = Field(default=None, description="")  # relationship

    attributes: DatabricksExternalLocation.Attributes = Field(
        default_factory=lambda: DatabricksExternalLocation.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .databricks_external_location_path import (
    DatabricksExternalLocationPath,  # noqa: E402, F401
)

DatabricksExternalLocation.Attributes.update_forward_refs()
