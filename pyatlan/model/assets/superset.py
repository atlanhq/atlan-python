# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, NumericField

from .core.b_i import BI


class Superset(BI):
    """Description"""

    type_name: str = Field(default="Superset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Superset":
            raise ValueError("must be Superset")
        return v

    def __setattr__(self, name, value):
        if name in Superset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SUPERSET_DASHBOARD_ID: ClassVar[NumericField] = NumericField(
        "supersetDashboardId", "supersetDashboardId"
    )
    """
    Identifier of the dashboard in which this asset exists, in Superset.
    """
    SUPERSET_DASHBOARD_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "supersetDashboardQualifiedName",
        "supersetDashboardQualifiedName",
        "supersetDashboardQualifiedName.text",
    )
    """
    Unique name of the dashboard in which this asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "superset_dashboard_id",
        "superset_dashboard_qualified_name",
    ]

    @property
    def superset_dashboard_id(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.superset_dashboard_id
        )

    @superset_dashboard_id.setter
    def superset_dashboard_id(self, superset_dashboard_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_id = superset_dashboard_id

    @property
    def superset_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dashboard_qualified_name
        )

    @superset_dashboard_qualified_name.setter
    def superset_dashboard_qualified_name(
        self, superset_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_qualified_name = (
            superset_dashboard_qualified_name
        )

    class Attributes(BI.Attributes):
        superset_dashboard_id: Optional[int] = Field(default=None, description="")
        superset_dashboard_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: Superset.Attributes = Field(
        default_factory=lambda: Superset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Superset.Attributes.update_forward_refs()
