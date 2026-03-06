# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .app import App


class AtlanApp(App):
    """Description"""

    type_name: str = Field(default="AtlanApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlanApp":
            raise ValueError("must be AtlanApp")
        return v

    def __setattr__(self, name, value):
        if name in AtlanApp._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ATLAN_APP_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "atlanAppQualifiedName", "atlanAppQualifiedName"
    )
    """
    Qualified name of the Atlan application this asset belongs to.
    """
    ATLAN_APP_NAME: ClassVar[KeywordField] = KeywordField(
        "atlanAppName", "atlanAppName"
    )
    """
    Name of the Atlan application this asset belongs to.
    """
    ATLAN_APP_METADATA: ClassVar[TextField] = TextField(
        "atlanAppMetadata", "atlanAppMetadata"
    )
    """
    Metadata for the Atlan application (escaped JSON string).
    """

    ATLAN_APP_TOOLS: ClassVar[RelationField] = RelationField("atlanAppTools")
    """
    TBC
    """
    ATLAN_APP_WORKFLOWS: ClassVar[RelationField] = RelationField("atlanAppWorkflows")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "atlan_app_qualified_name",
        "atlan_app_name",
        "atlan_app_metadata",
        "atlan_app_tools",
        "atlan_app_workflows",
    ]

    @property
    def atlan_app_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_qualified_name
        )

    @atlan_app_qualified_name.setter
    def atlan_app_qualified_name(self, atlan_app_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_qualified_name = atlan_app_qualified_name

    @property
    def atlan_app_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.atlan_app_name

    @atlan_app_name.setter
    def atlan_app_name(self, atlan_app_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_name = atlan_app_name

    @property
    def atlan_app_metadata(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.atlan_app_metadata

    @atlan_app_metadata.setter
    def atlan_app_metadata(self, atlan_app_metadata: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_metadata = atlan_app_metadata

    @property
    def atlan_app_tools(self) -> Optional[List[AtlanAppTool]]:
        return None if self.attributes is None else self.attributes.atlan_app_tools

    @atlan_app_tools.setter
    def atlan_app_tools(self, atlan_app_tools: Optional[List[AtlanAppTool]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_tools = atlan_app_tools

    @property
    def atlan_app_workflows(self) -> Optional[List[AtlanAppWorkflow]]:
        return None if self.attributes is None else self.attributes.atlan_app_workflows

    @atlan_app_workflows.setter
    def atlan_app_workflows(
        self, atlan_app_workflows: Optional[List[AtlanAppWorkflow]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflows = atlan_app_workflows

    class Attributes(App.Attributes):
        atlan_app_qualified_name: Optional[str] = Field(default=None, description="")
        atlan_app_name: Optional[str] = Field(default=None, description="")
        atlan_app_metadata: Optional[str] = Field(default=None, description="")
        atlan_app_tools: Optional[List[AtlanAppTool]] = Field(
            default=None, description=""
        )  # relationship
        atlan_app_workflows: Optional[List[AtlanAppWorkflow]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AtlanApp.Attributes = Field(
        default_factory=lambda: AtlanApp.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlan_app_tool import AtlanAppTool  # noqa: E402, F401
from .atlan_app_workflow import AtlanAppWorkflow  # noqa: E402, F401
