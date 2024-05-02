# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, NumericField

from .b_i import BI


class Preset(BI):
    """Description"""

    type_name: str = Field(default="Preset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Preset":
            raise ValueError("must be Preset")
        return v

    def __setattr__(self, name, value):
        if name in Preset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_WORKSPACE_ID: ClassVar[NumericField] = NumericField(
        "presetWorkspaceId", "presetWorkspaceId"
    )
    """
    Identifier of the workspace in which this asset exists, in Preset.
    """
    PRESET_WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "presetWorkspaceQualifiedName",
        "presetWorkspaceQualifiedName",
        "presetWorkspaceQualifiedName.text",
    )
    """
    Unique name of the workspace in which this asset exists.
    """
    PRESET_DASHBOARD_ID: ClassVar[NumericField] = NumericField(
        "presetDashboardId", "presetDashboardId"
    )
    """
    Identifier of the dashboard in which this asset exists, in Preset.
    """
    PRESET_DASHBOARD_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "presetDashboardQualifiedName",
        "presetDashboardQualifiedName",
        "presetDashboardQualifiedName.text",
    )
    """
    Unique name of the dashboard in which this asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "preset_workspace_id",
        "preset_workspace_qualified_name",
        "preset_dashboard_id",
        "preset_dashboard_qualified_name",
    ]

    @property
    def preset_workspace_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.preset_workspace_id

    @preset_workspace_id.setter
    def preset_workspace_id(self, preset_workspace_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_id = preset_workspace_id

    @property
    def preset_workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_qualified_name
        )

    @preset_workspace_qualified_name.setter
    def preset_workspace_qualified_name(
        self, preset_workspace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_qualified_name = (
            preset_workspace_qualified_name
        )

    @property
    def preset_dashboard_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.preset_dashboard_id

    @preset_dashboard_id.setter
    def preset_dashboard_id(self, preset_dashboard_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_id = preset_dashboard_id

    @property
    def preset_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_qualified_name
        )

    @preset_dashboard_qualified_name.setter
    def preset_dashboard_qualified_name(
        self, preset_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_qualified_name = (
            preset_dashboard_qualified_name
        )

    class Attributes(BI.Attributes):
        preset_workspace_id: Optional[int] = Field(default=None, description="")
        preset_workspace_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        preset_dashboard_id: Optional[int] = Field(default=None, description="")
        preset_dashboard_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: Preset.Attributes = Field(
        default_factory=lambda: Preset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
