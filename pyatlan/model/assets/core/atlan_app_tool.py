# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .atlan_app import AtlanApp


class AtlanAppTool(AtlanApp):
    """Description"""

    type_name: str = Field(default="AtlanAppTool", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlanAppTool":
            raise ValueError("must be AtlanAppTool")
        return v

    def __setattr__(self, name, value):
        if name in AtlanAppTool._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ATLAN_APP_TOOL_INPUT_SCHEMA: ClassVar[TextField] = TextField(
        "atlanAppToolInputSchema", "atlanAppToolInputSchema"
    )
    """
    Input schema for the Atlan application tool (escaped JSON string of JSONSchema).
    """
    ATLAN_APP_TOOL_OUTPUT_SCHEMA: ClassVar[TextField] = TextField(
        "atlanAppToolOutputSchema", "atlanAppToolOutputSchema"
    )
    """
    Output schema for the Atlan application tool (escaped JSON string of JSONSchema).
    """
    ATLAN_APP_TOOL_TASK_QUEUE: ClassVar[KeywordField] = KeywordField(
        "atlanAppToolTaskQueue", "atlanAppToolTaskQueue"
    )
    """
    Name of the Temporal task queue for the Atlan application tool.
    """
    ATLAN_APP_TOOL_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "atlanAppToolCategory", "atlanAppToolCategory"
    )
    """
    Category of the tool.
    """

    ATLAN_APP: ClassVar[RelationField] = RelationField("atlanApp")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "atlan_app_tool_input_schema",
        "atlan_app_tool_output_schema",
        "atlan_app_tool_task_queue",
        "atlan_app_tool_category",
        "atlan_app",
    ]

    @property
    def atlan_app_tool_input_schema(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_tool_input_schema
        )

    @atlan_app_tool_input_schema.setter
    def atlan_app_tool_input_schema(self, atlan_app_tool_input_schema: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_tool_input_schema = atlan_app_tool_input_schema

    @property
    def atlan_app_tool_output_schema(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_tool_output_schema
        )

    @atlan_app_tool_output_schema.setter
    def atlan_app_tool_output_schema(self, atlan_app_tool_output_schema: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_tool_output_schema = atlan_app_tool_output_schema

    @property
    def atlan_app_tool_task_queue(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_tool_task_queue
        )

    @atlan_app_tool_task_queue.setter
    def atlan_app_tool_task_queue(self, atlan_app_tool_task_queue: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_tool_task_queue = atlan_app_tool_task_queue

    @property
    def atlan_app_tool_category(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.atlan_app_tool_category
        )

    @atlan_app_tool_category.setter
    def atlan_app_tool_category(self, atlan_app_tool_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_tool_category = atlan_app_tool_category

    @property
    def atlan_app(self) -> Optional[AtlanApp]:
        return None if self.attributes is None else self.attributes.atlan_app

    @atlan_app.setter
    def atlan_app(self, atlan_app: Optional[AtlanApp]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app = atlan_app

    class Attributes(AtlanApp.Attributes):
        atlan_app_tool_input_schema: Optional[str] = Field(default=None, description="")
        atlan_app_tool_output_schema: Optional[str] = Field(
            default=None, description=""
        )
        atlan_app_tool_task_queue: Optional[str] = Field(default=None, description="")
        atlan_app_tool_category: Optional[str] = Field(default=None, description="")
        atlan_app: Optional[AtlanApp] = Field(
            default=None, description=""
        )  # relationship

    attributes: AtlanAppTool.Attributes = Field(
        default_factory=lambda: AtlanAppTool.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlan_app import AtlanApp  # noqa: E402, F401
