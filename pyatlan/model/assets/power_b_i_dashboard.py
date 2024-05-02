# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .power_b_i import PowerBI


class PowerBIDashboard(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDashboard":
            raise ValueError("must be PowerBIDashboard")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this dashboard exists.
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    Deprecated. See 'sourceUrl' instead.
    """
    TILE_COUNT: ClassVar[NumericField] = NumericField("tileCount", "tileCount")
    """
    Number of tiles in this table.
    """

    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "web_url",
        "tile_count",
        "workspace",
        "tiles",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def tile_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.tile_count

    @tile_count.setter
    def tile_count(self, tile_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tile_count = tile_count

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def tiles(self) -> Optional[List[PowerBITile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[List[PowerBITile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        web_url: Optional[str] = Field(default=None, description="")
        tile_count: Optional[int] = Field(default=None, description="")
        workspace: Optional[PowerBIWorkspace] = Field(
            default=None, description=""
        )  # relationship
        tiles: Optional[List[PowerBITile]] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIDashboard.Attributes = Field(
        default_factory=lambda: PowerBIDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_tile import PowerBITile  # noqa
from .power_b_i_workspace import PowerBIWorkspace  # noqa
