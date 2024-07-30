# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField
from pyatlan.utils import init_guid, validate_required_fields

from .superset import Superset


class SupersetChart(Superset):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
    ) -> SupersetChart: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
        connection_qualified_name: str,
    ) -> SupersetChart: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        superset_dashboard_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> SupersetChart:
        validate_required_fields(
            ["name", "superset_dashboard_qualified_name"],
            [name, superset_dashboard_qualified_name],
        )
        attributes = SupersetChart.Attributes.create(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
        cls, *, name: str, superset_dashboard_qualified_name: str
    ) -> SupersetChart:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
        )

    type_name: str = Field(default="SupersetChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SupersetChart":
            raise ValueError("must be SupersetChart")
        return v

    def __setattr__(self, name, value):
        if name in SupersetChart._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SUPERSET_CHART_DESCRIPTION_MARKDOWN: ClassVar[TextField] = TextField(
        "supersetChartDescriptionMarkdown", "supersetChartDescriptionMarkdown"
    )
    """
    Description markdown of the chart.
    """
    SUPERSET_CHART_FORM_DATA: ClassVar[KeywordField] = KeywordField(
        "supersetChartFormData", "supersetChartFormData"
    )
    """
    Data stored for the chart in key value pairs.
    """

    SUPERSET_DASHBOARD: ClassVar[RelationField] = RelationField("supersetDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "superset_chart_description_markdown",
        "superset_chart_form_data",
        "superset_dashboard",
    ]

    @property
    def superset_chart_description_markdown(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_chart_description_markdown
        )

    @superset_chart_description_markdown.setter
    def superset_chart_description_markdown(
        self, superset_chart_description_markdown: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_chart_description_markdown = (
            superset_chart_description_markdown
        )

    @property
    def superset_chart_form_data(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_chart_form_data
        )

    @superset_chart_form_data.setter
    def superset_chart_form_data(
        self, superset_chart_form_data: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_chart_form_data = superset_chart_form_data

    @property
    def superset_dashboard(self) -> Optional[SupersetDashboard]:
        return None if self.attributes is None else self.attributes.superset_dashboard

    @superset_dashboard.setter
    def superset_dashboard(self, superset_dashboard: Optional[SupersetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard = superset_dashboard

    class Attributes(Superset.Attributes):
        superset_chart_description_markdown: Optional[str] = Field(
            default=None, description=""
        )
        superset_chart_form_data: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        superset_dashboard: Optional[SupersetDashboard] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            superset_dashboard_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> SupersetChart.Attributes:
            validate_required_fields(
                ["name", "superset_dashboard_qualified_name"],
                [name, superset_dashboard_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    superset_dashboard_qualified_name,
                    "superset_dashboard_qualified_name",
                    4,
                )

            return SupersetChart.Attributes(
                name=name,
                superset_dashboard_qualified_name=superset_dashboard_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{superset_dashboard_qualified_name}/{name}",
                connector_name=connector_name,
                superset_dashboard=SupersetDashboard.ref_by_qualified_name(
                    superset_dashboard_qualified_name
                ),
            )

    attributes: SupersetChart.Attributes = Field(
        default_factory=lambda: SupersetChart.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .superset_dashboard import SupersetDashboard  # noqa

SupersetChart.Attributes.update_forward_refs()
