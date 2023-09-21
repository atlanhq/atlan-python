# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField

from .asset43 import Redash


class RedashDashboard(Redash):
    """Description"""

    type_name: str = Field("RedashDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashDashboard":
            raise ValueError("must be RedashDashboard")
        return v

    def __setattr__(self, name, value):
        if name in RedashDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    REDASH_DASHBOARD_WIDGET_COUNT: ClassVar[NumericField] = NumericField(
        "redashDashboardWidgetCount", "redashDashboardWidgetCount"
    )
    """
    Number of widgets in the Redash Dashboard
    """

    _convenience_properties: ClassVar[list[str]] = [
        "redash_dashboard_widget_count",
    ]

    @property
    def redash_dashboard_widget_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_dashboard_widget_count
        )

    @redash_dashboard_widget_count.setter
    def redash_dashboard_widget_count(
        self, redash_dashboard_widget_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_dashboard_widget_count = redash_dashboard_widget_count

    class Attributes(Redash.Attributes):
        redash_dashboard_widget_count: Optional[int] = Field(
            None, description="", alias="redashDashboardWidgetCount"
        )

    attributes: "RedashDashboard.Attributes" = Field(
        default_factory=lambda: RedashDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


RedashDashboard.Attributes.update_forward_refs()
