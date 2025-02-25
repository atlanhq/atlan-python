# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .quick_sight import QuickSight


class QuickSightDashboardVisual(QuickSight):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        quick_sight_id: str,
        quick_sight_sheet_id: str,
        quick_sight_sheet_name: str,
        quick_sight_dashboard_qualified_name: str,
    ) -> QuickSightDashboardVisual: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        quick_sight_id: str,
        quick_sight_sheet_id: str,
        quick_sight_sheet_name: str,
        quick_sight_dashboard_qualified_name: str,
        connection_qualified_name: str,
    ) -> QuickSightDashboardVisual: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        quick_sight_id: str,
        quick_sight_sheet_id: str,
        quick_sight_sheet_name: str,
        quick_sight_dashboard_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> QuickSightDashboardVisual:
        validate_required_fields(
            [
                "name",
                "quick_sight_id",
                "quick_sight_sheet_id",
                "quick_sight_sheet_name",
                "quick_sight_dashboard_qualified_name",
            ],
            [
                name,
                quick_sight_id,
                quick_sight_sheet_id,
                quick_sight_sheet_name,
                quick_sight_dashboard_qualified_name,
            ],
        )
        attributes = QuickSightDashboardVisual.Attributes.creator(
            name=name,
            quick_sight_id=quick_sight_id,
            quick_sight_sheet_id=quick_sight_sheet_id,
            quick_sight_sheet_name=quick_sight_sheet_name,
            quick_sight_dashboard_qualified_name=quick_sight_dashboard_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

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

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            quick_sight_id: str,
            quick_sight_sheet_id: str,
            quick_sight_sheet_name: str,
            quick_sight_dashboard_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> QuickSightDashboardVisual.Attributes:
            validate_required_fields(
                [
                    "name",
                    "quick_sight_id",
                    "quick_sight_sheet_name",
                    "quick_sight_sheet_id",
                    "quick_sight_dashboard_qualified_name",
                ],
                [
                    name,
                    quick_sight_id,
                    quick_sight_sheet_name,
                    quick_sight_sheet_id,
                    quick_sight_dashboard_qualified_name,
                ],
            )
            assert quick_sight_dashboard_qualified_name
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    quick_sight_dashboard_qualified_name,
                    "quick_sight_dashboard_qualified_name",
                    4,
                )
            connection_qualified_name = connection_qualified_name or connection_qn
            return QuickSightDashboardVisual.Attributes(
                name=name,
                qualified_name=f"{quick_sight_dashboard_qualified_name}/{quick_sight_sheet_id}/{quick_sight_id}",
                quick_sight_id=quick_sight_id,
                quick_sight_sheet_id=quick_sight_sheet_id,
                quick_sight_sheet_name=quick_sight_sheet_name,
                quick_sight_dashboard_qualified_name=quick_sight_dashboard_qualified_name,
                quick_sight_dashboard=QuickSightDashboard.ref_by_qualified_name(
                    quick_sight_dashboard_qualified_name
                ),
                connection_qualified_name=connection_qualified_name,
                connector_name=connector_name,
            )

    attributes: QuickSightDashboardVisual.Attributes = Field(
        default_factory=lambda: QuickSightDashboardVisual.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_dashboard import QuickSightDashboard  # noqa: E402, F401

QuickSightDashboardVisual.Attributes.update_forward_refs()
