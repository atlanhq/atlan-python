# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .preset import Preset


class PresetWorkspace(Preset):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> PresetWorkspace:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = PresetWorkspace.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> PresetWorkspace:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )

    type_name: str = Field(default="PresetWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetWorkspace":
            raise ValueError("must be PresetWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in PresetWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_WORKSPACE_PUBLIC_DASHBOARDS_ALLOWED: ClassVar[BooleanField] = BooleanField(
        "presetWorkspacePublicDashboardsAllowed",
        "presetWorkspacePublicDashboardsAllowed",
    )
    """

    """
    PRESET_WORKSPACE_CLUSTER_ID: ClassVar[NumericField] = NumericField(
        "presetWorkspaceClusterId", "presetWorkspaceClusterId"
    )
    """

    """
    PRESET_WORKSPACE_HOSTNAME: ClassVar[KeywordTextField] = KeywordTextField(
        "presetWorkspaceHostname",
        "presetWorkspaceHostname",
        "presetWorkspaceHostname.text",
    )
    """

    """
    PRESET_WORKSPACE_IS_IN_MAINTENANCE_MODE: ClassVar[BooleanField] = BooleanField(
        "presetWorkspaceIsInMaintenanceMode", "presetWorkspaceIsInMaintenanceMode"
    )
    """

    """
    PRESET_WORKSPACE_REGION: ClassVar[KeywordTextField] = KeywordTextField(
        "presetWorkspaceRegion", "presetWorkspaceRegion", "presetWorkspaceRegion.text"
    )
    """

    """
    PRESET_WORKSPACE_STATUS: ClassVar[KeywordField] = KeywordField(
        "presetWorkspaceStatus", "presetWorkspaceStatus"
    )
    """

    """
    PRESET_WORKSPACE_DEPLOYMENT_ID: ClassVar[NumericField] = NumericField(
        "presetWorkspaceDeploymentId", "presetWorkspaceDeploymentId"
    )
    """

    """
    PRESET_WORKSPACE_DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "presetWorkspaceDashboardCount", "presetWorkspaceDashboardCount"
    )
    """

    """
    PRESET_WORKSPACE_DATASET_COUNT: ClassVar[NumericField] = NumericField(
        "presetWorkspaceDatasetCount", "presetWorkspaceDatasetCount"
    )
    """

    """

    PRESET_DASHBOARDS: ClassVar[RelationField] = RelationField("presetDashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "preset_workspace_public_dashboards_allowed",
        "preset_workspace_cluster_id",
        "preset_workspace_hostname",
        "preset_workspace_is_in_maintenance_mode",
        "preset_workspace_region",
        "preset_workspace_status",
        "preset_workspace_deployment_id",
        "preset_workspace_dashboard_count",
        "preset_workspace_dataset_count",
        "preset_dashboards",
    ]

    @property
    def preset_workspace_public_dashboards_allowed(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_public_dashboards_allowed
        )

    @preset_workspace_public_dashboards_allowed.setter
    def preset_workspace_public_dashboards_allowed(
        self, preset_workspace_public_dashboards_allowed: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_public_dashboards_allowed = (
            preset_workspace_public_dashboards_allowed
        )

    @property
    def preset_workspace_cluster_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_cluster_id
        )

    @preset_workspace_cluster_id.setter
    def preset_workspace_cluster_id(self, preset_workspace_cluster_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_cluster_id = preset_workspace_cluster_id

    @property
    def preset_workspace_hostname(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_hostname
        )

    @preset_workspace_hostname.setter
    def preset_workspace_hostname(self, preset_workspace_hostname: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_hostname = preset_workspace_hostname

    @property
    def preset_workspace_is_in_maintenance_mode(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_is_in_maintenance_mode
        )

    @preset_workspace_is_in_maintenance_mode.setter
    def preset_workspace_is_in_maintenance_mode(
        self, preset_workspace_is_in_maintenance_mode: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_is_in_maintenance_mode = (
            preset_workspace_is_in_maintenance_mode
        )

    @property
    def preset_workspace_region(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.preset_workspace_region
        )

    @preset_workspace_region.setter
    def preset_workspace_region(self, preset_workspace_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_region = preset_workspace_region

    @property
    def preset_workspace_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.preset_workspace_status
        )

    @preset_workspace_status.setter
    def preset_workspace_status(self, preset_workspace_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_status = preset_workspace_status

    @property
    def preset_workspace_deployment_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_deployment_id
        )

    @preset_workspace_deployment_id.setter
    def preset_workspace_deployment_id(
        self, preset_workspace_deployment_id: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_deployment_id = preset_workspace_deployment_id

    @property
    def preset_workspace_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_dashboard_count
        )

    @preset_workspace_dashboard_count.setter
    def preset_workspace_dashboard_count(
        self, preset_workspace_dashboard_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_dashboard_count = (
            preset_workspace_dashboard_count
        )

    @property
    def preset_workspace_dataset_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_workspace_dataset_count
        )

    @preset_workspace_dataset_count.setter
    def preset_workspace_dataset_count(
        self, preset_workspace_dataset_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace_dataset_count = preset_workspace_dataset_count

    @property
    def preset_dashboards(self) -> Optional[List[PresetDashboard]]:
        return None if self.attributes is None else self.attributes.preset_dashboards

    @preset_dashboards.setter
    def preset_dashboards(self, preset_dashboards: Optional[List[PresetDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboards = preset_dashboards

    class Attributes(Preset.Attributes):
        preset_workspace_public_dashboards_allowed: Optional[bool] = Field(
            default=None, description=""
        )
        preset_workspace_cluster_id: Optional[int] = Field(default=None, description="")
        preset_workspace_hostname: Optional[str] = Field(default=None, description="")
        preset_workspace_is_in_maintenance_mode: Optional[bool] = Field(
            default=None, description=""
        )
        preset_workspace_region: Optional[str] = Field(default=None, description="")
        preset_workspace_status: Optional[str] = Field(default=None, description="")
        preset_workspace_deployment_id: Optional[int] = Field(
            default=None, description=""
        )
        preset_workspace_dashboard_count: Optional[int] = Field(
            default=None, description=""
        )
        preset_workspace_dataset_count: Optional[int] = Field(
            default=None, description=""
        )
        preset_dashboards: Optional[List[PresetDashboard]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> PresetWorkspace.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return PresetWorkspace.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: PresetWorkspace.Attributes = Field(
        default_factory=lambda: PresetWorkspace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .preset_dashboard import PresetDashboard  # noqa
