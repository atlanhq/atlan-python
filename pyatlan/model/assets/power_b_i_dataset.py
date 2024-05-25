# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .power_b_i import PowerBI


class PowerBIDataset(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataset":
            raise ValueError("must be PowerBIDataset")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this dataset exists.
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    Deprecated. See 'sourceUrl' instead.
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """
    TABLES: ClassVar[RelationField] = RelationField("tables")
    """
    TBC
    """
    DATAFLOWS: ClassVar[RelationField] = RelationField("dataflows")
    """
    TBC
    """
    DATASOURCES: ClassVar[RelationField] = RelationField("datasources")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "web_url",
        "reports",
        "workspace",
        "tiles",
        "tables",
        "dataflows",
        "datasources",
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
    def reports(self) -> Optional[List[PowerBIReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[List[PowerBIReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

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

    @property
    def tables(self) -> Optional[List[PowerBITable]]:
        return None if self.attributes is None else self.attributes.tables

    @tables.setter
    def tables(self, tables: Optional[List[PowerBITable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tables = tables

    @property
    def dataflows(self) -> Optional[List[PowerBIDataflow]]:
        return None if self.attributes is None else self.attributes.dataflows

    @dataflows.setter
    def dataflows(self, dataflows: Optional[List[PowerBIDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflows = dataflows

    @property
    def datasources(self) -> Optional[List[PowerBIDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[List[PowerBIDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        web_url: Optional[str] = Field(default=None, description="")
        reports: Optional[List[PowerBIReport]] = Field(
            default=None, description=""
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            default=None, description=""
        )  # relationship
        tiles: Optional[List[PowerBITile]] = Field(
            default=None, description=""
        )  # relationship
        tables: Optional[List[PowerBITable]] = Field(
            default=None, description=""
        )  # relationship
        dataflows: Optional[List[PowerBIDataflow]] = Field(
            default=None, description=""
        )  # relationship
        datasources: Optional[List[PowerBIDatasource]] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIDataset.Attributes = Field(
        default_factory=lambda: PowerBIDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dataflow import PowerBIDataflow  # noqa
from .power_b_i_datasource import PowerBIDatasource  # noqa
from .power_b_i_report import PowerBIReport  # noqa
from .power_b_i_table import PowerBITable  # noqa
from .power_b_i_tile import PowerBITile  # noqa
from .power_b_i_workspace import PowerBIWorkspace  # noqa
