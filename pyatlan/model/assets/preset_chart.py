# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField
from pyatlan.utils import init_guid, validate_required_fields

from .preset import Preset


class PresetChart(Preset):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        preset_dashboard_qualified_name: str,
    ) -> PresetChart: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        preset_dashboard_qualified_name: str,
        connection_qualified_name: str,
    ) -> PresetChart: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        preset_dashboard_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> PresetChart:
        validate_required_fields(
            ["name", "preset_dashboard_qualified_name"],
            [name, preset_dashboard_qualified_name],
        )
        attributes = PresetChart.Attributes.create(
            name=name,
            preset_dashboard_qualified_name=preset_dashboard_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, preset_dashboard_qualified_name: str) -> PresetChart:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, preset_dashboard_qualified_name=preset_dashboard_qualified_name
        )

    type_name: str = Field(default="PresetChart", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetChart":
            raise ValueError("must be PresetChart")
        return v

    def __setattr__(self, name, value):
        if name in PresetChart._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_CHART_DESCRIPTION_MARKDOWN: ClassVar[TextField] = TextField(
        "presetChartDescriptionMarkdown", "presetChartDescriptionMarkdown"
    )
    """

    """
    PRESET_CHART_FORM_DATA: ClassVar[KeywordField] = KeywordField(
        "presetChartFormData", "presetChartFormData"
    )
    """

    """

    PRESET_DASHBOARD: ClassVar[RelationField] = RelationField("presetDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "preset_chart_description_markdown",
        "preset_chart_form_data",
        "preset_dashboard",
    ]

    @property
    def preset_chart_description_markdown(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_chart_description_markdown
        )

    @preset_chart_description_markdown.setter
    def preset_chart_description_markdown(
        self, preset_chart_description_markdown: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_chart_description_markdown = (
            preset_chart_description_markdown
        )

    @property
    def preset_chart_form_data(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.preset_chart_form_data
        )

    @preset_chart_form_data.setter
    def preset_chart_form_data(self, preset_chart_form_data: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_chart_form_data = preset_chart_form_data

    @property
    def preset_dashboard(self) -> Optional[PresetDashboard]:
        return None if self.attributes is None else self.attributes.preset_dashboard

    @preset_dashboard.setter
    def preset_dashboard(self, preset_dashboard: Optional[PresetDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard = preset_dashboard

    class Attributes(Preset.Attributes):
        preset_chart_description_markdown: Optional[str] = Field(
            default=None, description=""
        )
        preset_chart_form_data: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        preset_dashboard: Optional[PresetDashboard] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            preset_dashboard_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> PresetChart.Attributes:
            validate_required_fields(
                ["name", "preset_dashboard_qualified_name"],
                [name, preset_dashboard_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    preset_dashboard_qualified_name,
                    "preset_dashboard_qualified_name",
                    5,
                )

            return PresetChart.Attributes(
                name=name,
                preset_dashboard_qualified_name=preset_dashboard_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{preset_dashboard_qualified_name}/{name}",
                connector_name=connector_name,
                preset_dashboard=PresetDashboard.ref_by_qualified_name(
                    preset_dashboard_qualified_name
                ),
            )

    attributes: PresetChart.Attributes = Field(
        default_factory=lambda: PresetChart.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .preset_dashboard import PresetDashboard  # noqa
