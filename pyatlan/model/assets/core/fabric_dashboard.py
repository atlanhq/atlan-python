# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .fabric import Fabric


class FabricDashboard(Fabric):
    """Description"""

    type_name: str = Field(default="FabricDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricDashboard":
            raise ValueError("must be FabricDashboard")
        return v

    def __setattr__(self, name, value):
        if name in FabricDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_WORKSPACE: ClassVar[RelationField] = RelationField("fabricWorkspace")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_workspace",
    ]

    @property
    def fabric_workspace(self) -> Optional[FabricWorkspace]:
        return None if self.attributes is None else self.attributes.fabric_workspace

    @fabric_workspace.setter
    def fabric_workspace(self, fabric_workspace: Optional[FabricWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_workspace = fabric_workspace

    class Attributes(Fabric.Attributes):
        fabric_workspace: Optional[FabricWorkspace] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricDashboard.Attributes = Field(
        default_factory=lambda: FabricDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_workspace import FabricWorkspace  # noqa: E402, F401
