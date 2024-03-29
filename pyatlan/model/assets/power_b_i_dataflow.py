# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .power_b_i import PowerBI


class PowerBIDataflow(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIDataflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataflow":
            raise ValueError("must be PowerBIDataflow")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this dataflow exists.
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    Deprecated. See 'sourceUrl' instead.
    """

    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    DATASETS: ClassVar[RelationField] = RelationField("datasets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "web_url",
        "workspace",
        "datasets",
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
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def datasets(self) -> Optional[List[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[List[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        web_url: Optional[str] = Field(default=None, description="")
        workspace: Optional[PowerBIWorkspace] = Field(
            default=None, description=""
        )  # relationship
        datasets: Optional[List[PowerBIDataset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIDataflow.Attributes = Field(
        default_factory=lambda: PowerBIDataflow.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dataset import PowerBIDataset  # noqa
from .power_b_i_workspace import PowerBIWorkspace  # noqa
