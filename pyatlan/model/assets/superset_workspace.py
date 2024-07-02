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

from .superset import Superset


class SupersetWorkspace(Superset):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> SupersetWorkspace:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = SupersetWorkspace.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> SupersetWorkspace:
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

    type_name: str = Field(default="SupersetWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SupersetWorkspace":
            raise ValueError("must be SupersetWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in SupersetWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SUPERSET_WORKSPACE_PUBLIC_DASHBOARDS_ALLOWED: ClassVar[BooleanField] = BooleanField(
        "supersetWorkspacePublicDashboardsAllowed",
        "supersetWorkspacePublicDashboardsAllowed",
    )
    """

    """
    SUPERSET_WORKSPACE_CLUSTER_ID: ClassVar[NumericField] = NumericField(
        "supersetWorkspaceClusterId", "supersetWorkspaceClusterId"
    )
    """

    """
    SUPERSET_WORKSPACE_DEPLOYMENT_ID: ClassVar[NumericField] = NumericField(
        "supersetWorkspaceDeploymentId", "supersetWorkspaceDeploymentId"
    )
    """

    """
    SUPERSET_WORKSPACE_HOSTNAME: ClassVar[KeywordTextField] = KeywordTextField(
        "supersetWorkspaceHostname",
        "supersetWorkspaceHostname",
        "supersetWorkspaceHostname.text",
    )
    """

    """
    SUPERSET_WORKSPACE_IS_IN_MAINTENANCE_MODE: ClassVar[BooleanField] = BooleanField(
        "supersetWorkspaceIsInMaintenanceMode", "supersetWorkspaceIsInMaintenanceMode"
    )
    """

    """
    SUPERSET_WORKSPACE_REGION: ClassVar[KeywordTextField] = KeywordTextField(
        "supersetWorkspaceRegion",
        "supersetWorkspaceRegion",
        "supersetWorkspaceRegion.text",
    )
    """

    """
    SUPERSET_WORKSPACE_STATUS: ClassVar[KeywordField] = KeywordField(
        "supersetWorkspaceStatus", "supersetWorkspaceStatus"
    )
    """

    """
    SUPERSET_WORKSPACE_DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "supersetWorkspaceDashboardCount", "supersetWorkspaceDashboardCount"
    )
    """

    """
    SUPERSET_WORKSPACE_DATASET_COUNT: ClassVar[NumericField] = NumericField(
        "supersetWorkspaceDatasetCount", "supersetWorkspaceDatasetCount"
    )
    """

    """

    SUPERSET_DASHBOARDS: ClassVar[RelationField] = RelationField("supersetDashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "superset_workspace_public_dashboards_allowed",
        "superset_workspace_cluster_id",
        "superset_workspace_deployment_id",
        "superset_workspace_hostname",
        "superset_workspace_is_in_maintenance_mode",
        "superset_workspace_region",
        "superset_workspace_status",
        "superset_workspace_dashboard_count",
        "superset_workspace_dataset_count",
        "superset_dashboards",
    ]

    @property
    def superset_workspace_public_dashboards_allowed(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_public_dashboards_allowed
        )

    @superset_workspace_public_dashboards_allowed.setter
    def superset_workspace_public_dashboards_allowed(
        self, superset_workspace_public_dashboards_allowed: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_public_dashboards_allowed = (
            superset_workspace_public_dashboards_allowed
        )

    @property
    def superset_workspace_cluster_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_cluster_id
        )

    @superset_workspace_cluster_id.setter
    def superset_workspace_cluster_id(
        self, superset_workspace_cluster_id: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_cluster_id = superset_workspace_cluster_id

    @property
    def superset_workspace_deployment_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_deployment_id
        )

    @superset_workspace_deployment_id.setter
    def superset_workspace_deployment_id(
        self, superset_workspace_deployment_id: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_deployment_id = (
            superset_workspace_deployment_id
        )

    @property
    def superset_workspace_hostname(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_hostname
        )

    @superset_workspace_hostname.setter
    def superset_workspace_hostname(self, superset_workspace_hostname: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_hostname = superset_workspace_hostname

    @property
    def superset_workspace_is_in_maintenance_mode(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_is_in_maintenance_mode
        )

    @superset_workspace_is_in_maintenance_mode.setter
    def superset_workspace_is_in_maintenance_mode(
        self, superset_workspace_is_in_maintenance_mode: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_is_in_maintenance_mode = (
            superset_workspace_is_in_maintenance_mode
        )

    @property
    def superset_workspace_region(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_region
        )

    @superset_workspace_region.setter
    def superset_workspace_region(self, superset_workspace_region: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_region = superset_workspace_region

    @property
    def superset_workspace_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_status
        )

    @superset_workspace_status.setter
    def superset_workspace_status(self, superset_workspace_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_status = superset_workspace_status

    @property
    def superset_workspace_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_dashboard_count
        )

    @superset_workspace_dashboard_count.setter
    def superset_workspace_dashboard_count(
        self, superset_workspace_dashboard_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_dashboard_count = (
            superset_workspace_dashboard_count
        )

    @property
    def superset_workspace_dataset_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_workspace_dataset_count
        )

    @superset_workspace_dataset_count.setter
    def superset_workspace_dataset_count(
        self, superset_workspace_dataset_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_workspace_dataset_count = (
            superset_workspace_dataset_count
        )

    @property
    def superset_dashboards(self) -> Optional[List[SupersetDashboard]]:
        return None if self.attributes is None else self.attributes.superset_dashboards

    @superset_dashboards.setter
    def superset_dashboards(
        self, superset_dashboards: Optional[List[SupersetDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboards = superset_dashboards

    class Attributes(Superset.Attributes):
        superset_workspace_public_dashboards_allowed: Optional[bool] = Field(
            default=None, description=""
        )
        superset_workspace_cluster_id: Optional[int] = Field(
            default=None, description=""
        )
        superset_workspace_deployment_id: Optional[int] = Field(
            default=None, description=""
        )
        superset_workspace_hostname: Optional[str] = Field(default=None, description="")
        superset_workspace_is_in_maintenance_mode: Optional[bool] = Field(
            default=None, description=""
        )
        superset_workspace_region: Optional[str] = Field(default=None, description="")
        superset_workspace_status: Optional[str] = Field(default=None, description="")
        superset_workspace_dashboard_count: Optional[int] = Field(
            default=None, description=""
        )
        superset_workspace_dataset_count: Optional[int] = Field(
            default=None, description=""
        )
        superset_dashboards: Optional[List[SupersetDashboard]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> SupersetWorkspace.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return SupersetWorkspace.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: SupersetWorkspace.Attributes = Field(
        default_factory=lambda: SupersetWorkspace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .superset_dashboard import SupersetDashboard  # noqa
