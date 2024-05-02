# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField

from .quick_sight import QuickSight


class QuickSightDashboardVisual(QuickSight):
    """Description"""

    type_name: str = Field(default="QuickSightDashboardVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboardVisual":
            raise ValueError("must be QuickSightDashboardVisual")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDashboardVisual._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DASHBOARD_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "quickSightDashboardQualifiedName",
        "quickSightDashboardQualifiedName",
        "quickSightDashboardQualifiedName.text",
    )
    """
    Unique name of the dashboard in which this visual exists.
    """

    QUICK_SIGHT_DASHBOARD: ClassVar[RelationField] = RelationField(
        "quickSightDashboard"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "quick_sight_dashboard_qualified_name",
        "quick_sight_dashboard",
    ]

    @property
    def quick_sight_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_qualified_name
        )

    @quick_sight_dashboard_qualified_name.setter
    def quick_sight_dashboard_qualified_name(
        self, quick_sight_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_qualified_name = (
            quick_sight_dashboard_qualified_name
        )

    @property
    def quick_sight_dashboard(self) -> Optional[QuickSightDashboard]:
        return (
            None if self.attributes is None else self.attributes.quick_sight_dashboard
        )

    @quick_sight_dashboard.setter
    def quick_sight_dashboard(
        self, quick_sight_dashboard: Optional[QuickSightDashboard]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard = quick_sight_dashboard

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        quick_sight_dashboard: Optional[QuickSightDashboard] = Field(
            default=None, description=""
        )  # relationship

    attributes: QuickSightDashboardVisual.Attributes = Field(
        default_factory=lambda: QuickSightDashboardVisual.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_dashboard import QuickSightDashboard  # noqa
