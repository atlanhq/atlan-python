# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .monte_carlo import MonteCarlo


class MCIncident(MonteCarlo):
    """Description"""

    type_name: str = Field(default="MCIncident", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MCIncident":
            raise ValueError("must be MCIncident")
        return v

    def __setattr__(self, name, value):
        if name in MCIncident._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MC_INCIDENT_ID: ClassVar[KeywordField] = KeywordField(
        "mcIncidentId", "mcIncidentId"
    )
    """
    Identifier of this incident, from Monte Carlo.
    """
    MC_INCIDENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentType", "mcIncidentType"
    )
    """
    Type of this incident.
    """
    MC_INCIDENT_SUB_TYPES: ClassVar[KeywordField] = KeywordField(
        "mcIncidentSubTypes", "mcIncidentSubTypes"
    )
    """
    Subtypes of this incident.
    """
    MC_INCIDENT_SEVERITY: ClassVar[KeywordField] = KeywordField(
        "mcIncidentSeverity", "mcIncidentSeverity"
    )
    """
    Severity of this incident.
    """
    MC_INCIDENT_STATE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentState", "mcIncidentState"
    )
    """
    State of this incident.
    """
    MC_INCIDENT_WAREHOUSE: ClassVar[KeywordField] = KeywordField(
        "mcIncidentWarehouse", "mcIncidentWarehouse"
    )
    """
    Name of this incident's warehouse.
    """

    MC_MONITOR: ClassVar[RelationField] = RelationField("mcMonitor")
    """
    TBC
    """
    MC_INCIDENT_ASSETS: ClassVar[RelationField] = RelationField("mcIncidentAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "mc_incident_id",
        "mc_incident_type",
        "mc_incident_sub_types",
        "mc_incident_severity",
        "mc_incident_state",
        "mc_incident_warehouse",
        "mc_monitor",
        "mc_incident_assets",
    ]

    @property
    def mc_incident_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_id

    @mc_incident_id.setter
    def mc_incident_id(self, mc_incident_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_id = mc_incident_id

    @property
    def mc_incident_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_type

    @mc_incident_type.setter
    def mc_incident_type(self, mc_incident_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_type = mc_incident_type

    @property
    def mc_incident_sub_types(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.mc_incident_sub_types
        )

    @mc_incident_sub_types.setter
    def mc_incident_sub_types(self, mc_incident_sub_types: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_sub_types = mc_incident_sub_types

    @property
    def mc_incident_severity(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_severity

    @mc_incident_severity.setter
    def mc_incident_severity(self, mc_incident_severity: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_severity = mc_incident_severity

    @property
    def mc_incident_state(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_incident_state

    @mc_incident_state.setter
    def mc_incident_state(self, mc_incident_state: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_state = mc_incident_state

    @property
    def mc_incident_warehouse(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.mc_incident_warehouse
        )

    @mc_incident_warehouse.setter
    def mc_incident_warehouse(self, mc_incident_warehouse: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_warehouse = mc_incident_warehouse

    @property
    def mc_monitor(self) -> Optional[MCMonitor]:
        return None if self.attributes is None else self.attributes.mc_monitor

    @mc_monitor.setter
    def mc_monitor(self, mc_monitor: Optional[MCMonitor]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor = mc_monitor

    @property
    def mc_incident_assets(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.mc_incident_assets

    @mc_incident_assets.setter
    def mc_incident_assets(self, mc_incident_assets: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_incident_assets = mc_incident_assets

    class Attributes(MonteCarlo.Attributes):
        mc_incident_id: Optional[str] = Field(default=None, description="")
        mc_incident_type: Optional[str] = Field(default=None, description="")
        mc_incident_sub_types: Optional[Set[str]] = Field(default=None, description="")
        mc_incident_severity: Optional[str] = Field(default=None, description="")
        mc_incident_state: Optional[str] = Field(default=None, description="")
        mc_incident_warehouse: Optional[str] = Field(default=None, description="")
        mc_monitor: Optional[MCMonitor] = Field(
            default=None, description=""
        )  # relationship
        mc_incident_assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MCIncident.Attributes = Field(
        default_factory=lambda: MCIncident.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
from .m_c_monitor import MCMonitor  # noqa
