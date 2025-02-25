# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.b_i import BI


class Anaplan(BI):
    """Description"""

    type_name: str = Field(default="Anaplan", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Anaplan":
            raise ValueError("must be Anaplan")
        return v

    def __setattr__(self, name, value):
        if name in Anaplan._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanWorkspaceQualifiedName", "anaplanWorkspaceQualifiedName"
    )
    """
    Unique name of the AnaplanWorkspace asset that contains this asset(AnaplanModel and everthing under it's hierarchy).
    """
    ANAPLAN_WORKSPACE_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanWorkspaceName", "anaplanWorkspaceName"
    )
    """
    Simple name of the AnaplanWorkspace asset that contains this asset(AnaplanModel and everthing under it's hierarchy).
    """
    ANAPLAN_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanModelQualifiedName", "anaplanModelQualifiedName"
    )
    """
    Unique name of the AnaplanModel asset that contains this asset(AnaplanModule and everthing under it's hierarchy).
    """
    ANAPLAN_MODEL_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanModelName", "anaplanModelName"
    )
    """
    Simple name of the AnaplanModel asset that contains this asset(AnaplanModule and everthing under it's hierarchy).
    """
    ANAPLAN_MODULE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanModuleQualifiedName", "anaplanModuleQualifiedName"
    )
    """
    Unique name of the AnaplanModule asset that contains this asset(AnaplanLineItem, AnaplanList, AnaplanView and everthing under their hierarchy).
    """  # noqa: E501
    ANAPLAN_MODULE_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanModuleName", "anaplanModuleName"
    )
    """
    Simple name of the AnaplanModule asset that contains this asset(AnaplanLineItem, AnaplanList, AnaplanView and everthing under their hierarchy).
    """  # noqa: E501
    ANAPLAN_SOURCE_ID: ClassVar[KeywordField] = KeywordField(
        "anaplanSourceId", "anaplanSourceId"
    )
    """
    Id/Guid of the Anaplan asset in the source system.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_workspace_qualified_name",
        "anaplan_workspace_name",
        "anaplan_model_qualified_name",
        "anaplan_model_name",
        "anaplan_module_qualified_name",
        "anaplan_module_name",
        "anaplan_source_id",
    ]

    @property
    def anaplan_workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_workspace_qualified_name
        )

    @anaplan_workspace_qualified_name.setter
    def anaplan_workspace_qualified_name(
        self, anaplan_workspace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_workspace_qualified_name = (
            anaplan_workspace_qualified_name
        )

    @property
    def anaplan_workspace_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.anaplan_workspace_name
        )

    @anaplan_workspace_name.setter
    def anaplan_workspace_name(self, anaplan_workspace_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_workspace_name = anaplan_workspace_name

    @property
    def anaplan_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_model_qualified_name
        )

    @anaplan_model_qualified_name.setter
    def anaplan_model_qualified_name(self, anaplan_model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_model_qualified_name = anaplan_model_qualified_name

    @property
    def anaplan_model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.anaplan_model_name

    @anaplan_model_name.setter
    def anaplan_model_name(self, anaplan_model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_model_name = anaplan_model_name

    @property
    def anaplan_module_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_module_qualified_name
        )

    @anaplan_module_qualified_name.setter
    def anaplan_module_qualified_name(
        self, anaplan_module_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_module_qualified_name = anaplan_module_qualified_name

    @property
    def anaplan_module_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.anaplan_module_name

    @anaplan_module_name.setter
    def anaplan_module_name(self, anaplan_module_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_module_name = anaplan_module_name

    @property
    def anaplan_source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.anaplan_source_id

    @anaplan_source_id.setter
    def anaplan_source_id(self, anaplan_source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_source_id = anaplan_source_id

    class Attributes(BI.Attributes):
        anaplan_workspace_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        anaplan_workspace_name: Optional[str] = Field(default=None, description="")
        anaplan_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        anaplan_model_name: Optional[str] = Field(default=None, description="")
        anaplan_module_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        anaplan_module_name: Optional[str] = Field(default=None, description="")
        anaplan_source_id: Optional[str] = Field(default=None, description="")

    attributes: Anaplan.Attributes = Field(
        default_factory=lambda: Anaplan.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Anaplan.Attributes.update_forward_refs()
