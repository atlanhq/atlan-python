# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .anaplan import Anaplan


class AnaplanModel(Anaplan):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        workspace_qualified_name: str,
    ) -> AnaplanModel: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        workspace_qualified_name: str,
        connection_qualified_name: str,
    ) -> AnaplanModel: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        workspace_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> AnaplanModel:
        validate_required_fields(
            ["name", "workspace_qualified_name"], [name, workspace_qualified_name]
        )
        attributes = AnaplanModel.Attributes.create(
            name=name,
            workspace_qualified_name=workspace_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="AnaplanModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanModel":
            raise ValueError("must be AnaplanModel")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_WORKSPACE: ClassVar[RelationField] = RelationField("anaplanWorkspace")
    """
    TBC
    """
    ANAPLAN_MODULES: ClassVar[RelationField] = RelationField("anaplanModules")
    """
    TBC
    """
    ANAPLAN_PAGES: ClassVar[RelationField] = RelationField("anaplanPages")
    """
    TBC
    """
    ANAPLAN_LISTS: ClassVar[RelationField] = RelationField("anaplanLists")
    """
    TBC
    """
    ANAPLAN_DIMENSIONS: ClassVar[RelationField] = RelationField("anaplanDimensions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_workspace",
        "anaplan_modules",
        "anaplan_pages",
        "anaplan_lists",
        "anaplan_dimensions",
    ]

    @property
    def anaplan_workspace(self) -> Optional[AnaplanWorkspace]:
        return None if self.attributes is None else self.attributes.anaplan_workspace

    @anaplan_workspace.setter
    def anaplan_workspace(self, anaplan_workspace: Optional[AnaplanWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_workspace = anaplan_workspace

    @property
    def anaplan_modules(self) -> Optional[List[AnaplanModule]]:
        return None if self.attributes is None else self.attributes.anaplan_modules

    @anaplan_modules.setter
    def anaplan_modules(self, anaplan_modules: Optional[List[AnaplanModule]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_modules = anaplan_modules

    @property
    def anaplan_pages(self) -> Optional[List[AnaplanPage]]:
        return None if self.attributes is None else self.attributes.anaplan_pages

    @anaplan_pages.setter
    def anaplan_pages(self, anaplan_pages: Optional[List[AnaplanPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_pages = anaplan_pages

    @property
    def anaplan_lists(self) -> Optional[List[AnaplanList]]:
        return None if self.attributes is None else self.attributes.anaplan_lists

    @anaplan_lists.setter
    def anaplan_lists(self, anaplan_lists: Optional[List[AnaplanList]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_lists = anaplan_lists

    @property
    def anaplan_dimensions(self) -> Optional[List[AnaplanDimension]]:
        return None if self.attributes is None else self.attributes.anaplan_dimensions

    @anaplan_dimensions.setter
    def anaplan_dimensions(self, anaplan_dimensions: Optional[List[AnaplanDimension]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_dimensions = anaplan_dimensions

    class Attributes(Anaplan.Attributes):
        anaplan_workspace: Optional[AnaplanWorkspace] = Field(
            default=None, description=""
        )  # relationship
        anaplan_modules: Optional[List[AnaplanModule]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_pages: Optional[List[AnaplanPage]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_lists: Optional[List[AnaplanList]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_dimensions: Optional[List[AnaplanDimension]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            workspace_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> AnaplanModel.Attributes:
            validate_required_fields(
                ["name", "workspace_qualified_name"],
                [name, workspace_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    workspace_qualified_name, "workspace_qualified_name", 4
                )

            workspace_name = workspace_qualified_name.split("/")[3]

            return AnaplanModel.Attributes(
                name=name,
                qualified_name=f"{workspace_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name or connection_qn,
                connector_name=connector_name,
                anaplan_workspace_qualified_name=workspace_qualified_name,
                anaplan_workspace_name=workspace_name,
                anaplan_workspace=AnaplanWorkspace.ref_by_qualified_name(
                    workspace_qualified_name
                ),
            )

    attributes: AnaplanModel.Attributes = Field(
        default_factory=lambda: AnaplanModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_dimension import AnaplanDimension  # noqa: E402, F401
from .anaplan_list import AnaplanList  # noqa: E402, F401
from .anaplan_module import AnaplanModule  # noqa: E402, F401
from .anaplan_page import AnaplanPage  # noqa: E402, F401
from .anaplan_workspace import AnaplanWorkspace  # noqa: E402, F401

AnaplanModel.Attributes.update_forward_refs()
