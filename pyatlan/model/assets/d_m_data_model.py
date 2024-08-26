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

    D_M_VERSION_COUNT: ClassVar[NumericField] = NumericField(
        "dMVersionCount", "dMVersionCount"
    )
    """
    Number of versions of the data model.
    """
    D_M_TYPE: ClassVar[KeywordField] = KeywordField("dMType", "dMType")
    """
    Type of the data model.
    """
    D_M_TOOL: ClassVar[KeywordField] = KeywordField("dMTool", "dMTool")
    """
    Tool used to create this data model.
    """

    D_M_VERSIONS: ClassVar[RelationField] = RelationField("dMVersions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "d_m_version_count",
        "d_m_type",
        "d_m_tool",
        "d_m_versions",
    ]

    @property
    def d_m_version_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.d_m_version_count

    @d_m_version_count.setter
    def d_m_version_count(self, d_m_version_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_version_count = d_m_version_count

    @property
    def d_m_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_type

    @d_m_type.setter
    def d_m_type(self, d_m_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_type = d_m_type

    @property
    def d_m_tool(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_tool

    @d_m_tool.setter
    def d_m_tool(self, d_m_tool: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_tool = d_m_tool

    @property
    def d_m_versions(self) -> Optional[List[DMVersion]]:
        return None if self.attributes is None else self.attributes.d_m_versions

    @d_m_versions.setter
    def d_m_versions(self, d_m_versions: Optional[List[DMVersion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_versions = d_m_versions

    class Attributes(DM.Attributes):
        d_m_version_count: Optional[int] = Field(default=None, description="")
        d_m_type: Optional[str] = Field(default=None, description="")
        d_m_tool: Optional[str] = Field(default=None, description="")
        d_m_versions: Optional[List[DMVersion]] = Field(
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
