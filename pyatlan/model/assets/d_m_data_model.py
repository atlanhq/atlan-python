# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .d_m import DM


class DMDataModel(DM):
    """Description"""

    type_name: str = Field(default="DMDataModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DMDataModel":
            raise ValueError("must be DMDataModel")
        return v

    def __setattr__(self, name, value):
        if name in DMDataModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DM_VERSION_COUNT: ClassVar[NumericField] = NumericField(
        "dmVersionCount", "dmVersionCount"
    )
    """
    Number of versions of the data model.
    """
    DM_DATA_MODEL_TYPE: ClassVar[KeywordField] = KeywordField(
        "dmDataModelType", "dmDataModelType"
    )
    """
    Type of the data model.
    """
    DM_TOOL: ClassVar[KeywordField] = KeywordField("dmTool", "dmTool")
    """
    Tool used to create this data model.
    """

    DM_VERSIONS: ClassVar[RelationField] = RelationField("dmVersions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dm_version_count",
        "dm_data_model_type",
        "dm_tool",
        "dm_versions",
    ]

    @property
    def dm_version_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dm_version_count

    @dm_version_count.setter
    def dm_version_count(self, dm_version_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_version_count = dm_version_count

    @property
    def dm_data_model_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_data_model_type

    @dm_data_model_type.setter
    def dm_data_model_type(self, dm_data_model_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_data_model_type = dm_data_model_type

    @property
    def dm_tool(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_tool

    @dm_tool.setter
    def dm_tool(self, dm_tool: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_tool = dm_tool

    @property
    def dm_versions(self) -> Optional[List[DMVersion]]:
        return None if self.attributes is None else self.attributes.dm_versions

    @dm_versions.setter
    def dm_versions(self, dm_versions: Optional[List[DMVersion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_versions = dm_versions

    class Attributes(DM.Attributes):
        dm_version_count: Optional[int] = Field(default=None, description="")
        dm_data_model_type: Optional[str] = Field(default=None, description="")
        dm_tool: Optional[str] = Field(default=None, description="")
        dm_versions: Optional[List[DMVersion]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DMDataModel.Attributes = Field(
        default_factory=lambda: DMDataModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .d_m_version import DMVersion  # noqa

DMDataModel.Attributes.update_forward_refs()
