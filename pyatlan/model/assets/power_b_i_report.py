# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .power_b_i import PowerBI


class PowerBIReport(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIReport":
            raise ValueError("must be PowerBIReport")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this report exists.
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    Unique name of the dataset used to build this report.
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    Deprecated. See 'sourceUrl' instead.
    """
    PAGE_COUNT: ClassVar[NumericField] = NumericField("pageCount", "pageCount")
    """
    Number of pages in this report.
    """

    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """
    PAGES: ClassVar[RelationField] = RelationField("pages")
    """
    TBC
    """
    DATASET: ClassVar[RelationField] = RelationField("dataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "web_url",
        "page_count",
        "workspace",
        "tiles",
        "pages",
        "dataset",
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
    def dataset_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dataset_qualified_name
        )

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def page_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.page_count

    @page_count.setter
    def page_count(self, page_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.page_count = page_count

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
    def pages(self) -> Optional[List[PowerBIPage]]:
        return None if self.attributes is None else self.attributes.pages

    @pages.setter
    def pages(self, pages: Optional[List[PowerBIPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pages = pages

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        dataset_qualified_name: Optional[str] = Field(default=None, description="")
        web_url: Optional[str] = Field(default=None, description="")
        page_count: Optional[int] = Field(default=None, description="")
        workspace: Optional[PowerBIWorkspace] = Field(
            default=None, description=""
        )  # relationship
        tiles: Optional[List[PowerBITile]] = Field(
            default=None, description=""
        )  # relationship
        pages: Optional[List[PowerBIPage]] = Field(
            default=None, description=""
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIReport.Attributes = Field(
        default_factory=lambda: PowerBIReport.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dataset import PowerBIDataset  # noqa
from .power_b_i_page import PowerBIPage  # noqa
from .power_b_i_tile import PowerBITile  # noqa
from .power_b_i_workspace import PowerBIWorkspace  # noqa
