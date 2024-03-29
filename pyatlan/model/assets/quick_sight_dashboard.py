# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .quick_sight import QuickSight


class QuickSightDashboard(QuickSight):
    """Description"""

    type_name: str = Field(default="QuickSightDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDashboard":
            raise ValueError("must be QuickSightDashboard")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DASHBOARD_PUBLISHED_VERSION_NUMBER: ClassVar[NumericField] = (
        NumericField(
            "quickSightDashboardPublishedVersionNumber",
            "quickSightDashboardPublishedVersionNumber",
        )
    )
    """
    Version number of the published dashboard.
    """
    QUICK_SIGHT_DASHBOARD_LAST_PUBLISHED_TIME: ClassVar[NumericField] = NumericField(
        "quickSightDashboardLastPublishedTime", "quickSightDashboardLastPublishedTime"
    )
    """
    Time (epoch) at which this dashboard was last published, in milliseconds.
    """

    QUICK_SIGHT_DASHBOARD_FOLDERS: ClassVar[RelationField] = RelationField(
        "quickSightDashboardFolders"
    )
    """
    TBC
    """
    QUICK_SIGHT_DASHBOARD_VISUALS: ClassVar[RelationField] = RelationField(
        "quickSightDashboardVisuals"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "quick_sight_dashboard_published_version_number",
        "quick_sight_dashboard_last_published_time",
        "quick_sight_dashboard_folders",
        "quick_sight_dashboard_visuals",
    ]

    @property
    def quick_sight_dashboard_published_version_number(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_published_version_number
        )

    @quick_sight_dashboard_published_version_number.setter
    def quick_sight_dashboard_published_version_number(
        self, quick_sight_dashboard_published_version_number: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_published_version_number = (
            quick_sight_dashboard_published_version_number
        )

    @property
    def quick_sight_dashboard_last_published_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_last_published_time
        )

    @quick_sight_dashboard_last_published_time.setter
    def quick_sight_dashboard_last_published_time(
        self, quick_sight_dashboard_last_published_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_last_published_time = (
            quick_sight_dashboard_last_published_time
        )

    @property
    def quick_sight_dashboard_folders(self) -> Optional[List[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_folders
        )

    @quick_sight_dashboard_folders.setter
    def quick_sight_dashboard_folders(
        self, quick_sight_dashboard_folders: Optional[List[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_folders = quick_sight_dashboard_folders

    @property
    def quick_sight_dashboard_visuals(
        self,
    ) -> Optional[List[QuickSightDashboardVisual]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dashboard_visuals
        )

    @quick_sight_dashboard_visuals.setter
    def quick_sight_dashboard_visuals(
        self, quick_sight_dashboard_visuals: Optional[List[QuickSightDashboardVisual]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dashboard_visuals = quick_sight_dashboard_visuals

    class Attributes(QuickSight.Attributes):
        quick_sight_dashboard_published_version_number: Optional[int] = Field(
            default=None, description=""
        )
        quick_sight_dashboard_last_published_time: Optional[datetime] = Field(
            default=None, description=""
        )
        quick_sight_dashboard_folders: Optional[List[QuickSightFolder]] = Field(
            default=None, description=""
        )  # relationship
        quick_sight_dashboard_visuals: Optional[List[QuickSightDashboardVisual]] = (
            Field(default=None, description="")
        )  # relationship

    attributes: QuickSightDashboard.Attributes = Field(
        default_factory=lambda: QuickSightDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_dashboard_visual import QuickSightDashboardVisual  # noqa
from .quick_sight_folder import QuickSightFolder  # noqa
