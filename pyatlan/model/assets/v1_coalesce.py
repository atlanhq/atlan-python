# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField

from .core.catalog import Catalog


class V1Coalesce(Catalog):
    """Description"""

    type_name: str = Field(default="V1Coalesce", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "V1Coalesce":
            raise ValueError("must be V1Coalesce")
        return v

    def __setattr__(self, name, value):
        if name in V1Coalesce._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceProjectId", "coalesceProjectId.keyword", "coalesceProjectId"
    )
    """
    Unique identifier of the project in which this Coalesce asset exists.
    """
    COALESCE_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceProjectName", "coalesceProjectName.keyword", "coalesceProjectName"
    )
    """
    Name of the project in which this Coalesce asset exists.
    """
    COALESCE_WORKSPACE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceWorkspaceId", "coalesceWorkspaceId.keyword", "coalesceWorkspaceId"
    )
    """
    Unique identifier of the workspace in which this Coalesce asset exists.
    """
    COALESCE_WORKSPACE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceWorkspaceName",
        "coalesceWorkspaceName.keyword",
        "coalesceWorkspaceName",
    )
    """
    Name of the workspace in which this Coalesce asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_project_id",
        "coalesce_project_name",
        "coalesce_workspace_id",
        "coalesce_workspace_name",
    ]

    @property
    def coalesce_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.coalesce_project_id

    @coalesce_project_id.setter
    def coalesce_project_id(self, coalesce_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_project_id = coalesce_project_id

    @property
    def coalesce_project_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_project_name
        )

    @coalesce_project_name.setter
    def coalesce_project_name(self, coalesce_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_project_name = coalesce_project_name

    @property
    def coalesce_workspace_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_workspace_id
        )

    @coalesce_workspace_id.setter
    def coalesce_workspace_id(self, coalesce_workspace_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_workspace_id = coalesce_workspace_id

    @property
    def coalesce_workspace_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_workspace_name
        )

    @coalesce_workspace_name.setter
    def coalesce_workspace_name(self, coalesce_workspace_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_workspace_name = coalesce_workspace_name

    class Attributes(Catalog.Attributes):
        coalesce_project_id: Optional[str] = Field(default=None, description="")
        coalesce_project_name: Optional[str] = Field(default=None, description="")
        coalesce_workspace_id: Optional[str] = Field(default=None, description="")
        coalesce_workspace_name: Optional[str] = Field(default=None, description="")

    attributes: V1Coalesce.Attributes = Field(
        default_factory=lambda: V1Coalesce.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


V1Coalesce.Attributes.update_forward_refs()
