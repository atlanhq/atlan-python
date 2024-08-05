# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import IncidentSeverity
from pyatlan.model.fields.atlan_fields import KeywordField

from .core.asset import Asset


class Incident(Asset, type_name="Incident"):
    """Description"""

    type_name: str = Field(default="Incident", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Incident":
            raise ValueError("must be Incident")
        return v

    def __setattr__(self, name, value):
        if name in Incident._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    INCIDENT_SEVERITY: ClassVar[KeywordField] = KeywordField(
        "incidentSeverity", "incidentSeverity"
    )
    """
    Status of this asset's severity.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "incident_severity",
    ]

    @property
    def incident_severity(self) -> Optional[IncidentSeverity]:
        return None if self.attributes is None else self.attributes.incident_severity

    @incident_severity.setter
    def incident_severity(self, incident_severity: Optional[IncidentSeverity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.incident_severity = incident_severity

    class Attributes(Asset.Attributes):
        incident_severity: Optional[IncidentSeverity] = Field(
            default=None, description=""
        )

    attributes: Incident.Attributes = Field(
        default_factory=lambda: Incident.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Incident.Attributes.update_forward_refs()
