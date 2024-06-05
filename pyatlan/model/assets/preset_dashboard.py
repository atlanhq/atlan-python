# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextStemmedField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .preset import Preset


class PresetDashboard(Preset):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        preset_workspace_qualified_name: str,
    ) -> PresetDashboard: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        preset_workspace_qualified_name: str,
        connection_qualified_name: str,
    ) -> PresetDashboard: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        preset_workspace_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> PresetDashboard:
        validate_required_fields(
            ["name", "preset_workspace_qualified_name"],
            [name, preset_workspace_qualified_name],
        )
        attributes = PresetDashboard.Attributes.create(
            name=name,
            preset_workspace_qualified_name=preset_workspace_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(
        cls, *, name: str, preset_workspace_qualified_name: str
    ) -> PresetDashboard:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, preset_workspace_qualified_name=preset_workspace_qualified_name
        )

    type_name: str = Field(default="PresetDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PresetDashboard":
            raise ValueError("must be PresetDashboard")
        return v

    def __setattr__(self, name, value):
        if name in PresetDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PRESET_DASHBOARD_CHANGED_BY_NAME: ClassVar[KeywordTextStemmedField] = (
        KeywordTextStemmedField(
            "presetDashboardChangedByName",
            "presetDashboardChangedByName.keyword",
            "presetDashboardChangedByName",
            "presetDashboardChangedByName.stemmed",
        )
    )
    """

    """
    PRESET_DASHBOARD_CHANGED_BY_URL: ClassVar[KeywordField] = KeywordField(
        "presetDashboardChangedByURL", "presetDashboardChangedByURL"
    )
    """

    """
    PRESET_DASHBOARD_IS_MANAGED_EXTERNALLY: ClassVar[BooleanField] = BooleanField(
        "presetDashboardIsManagedExternally", "presetDashboardIsManagedExternally"
    )
    """

    """
    PRESET_DASHBOARD_IS_PUBLISHED: ClassVar[BooleanField] = BooleanField(
        "presetDashboardIsPublished", "presetDashboardIsPublished"
    )
    """

    """
    PRESET_DASHBOARD_THUMBNAIL_URL: ClassVar[KeywordField] = KeywordField(
        "presetDashboardThumbnailURL", "presetDashboardThumbnailURL"
    )
    """

    """
    PRESET_DASHBOARD_CHART_COUNT: ClassVar[NumericField] = NumericField(
        "presetDashboardChartCount", "presetDashboardChartCount"
    )
    """

    """

    PRESET_DATASETS: ClassVar[RelationField] = RelationField("presetDatasets")
    """
    TBC
    """
    PRESET_CHARTS: ClassVar[RelationField] = RelationField("presetCharts")
    """
    TBC
    """
    PRESET_WORKSPACE: ClassVar[RelationField] = RelationField("presetWorkspace")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "preset_dashboard_changed_by_name",
        "preset_dashboard_changed_by_url",
        "preset_dashboard_is_managed_externally",
        "preset_dashboard_is_published",
        "preset_dashboard_thumbnail_url",
        "preset_dashboard_chart_count",
        "preset_datasets",
        "preset_charts",
        "preset_workspace",
    ]

    @property
    def preset_dashboard_changed_by_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_changed_by_name
        )

    @preset_dashboard_changed_by_name.setter
    def preset_dashboard_changed_by_name(
        self, preset_dashboard_changed_by_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_changed_by_name = (
            preset_dashboard_changed_by_name
        )

    @property
    def preset_dashboard_changed_by_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_changed_by_url
        )

    @preset_dashboard_changed_by_url.setter
    def preset_dashboard_changed_by_url(
        self, preset_dashboard_changed_by_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_changed_by_url = (
            preset_dashboard_changed_by_url
        )

    @property
    def preset_dashboard_is_managed_externally(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_is_managed_externally
        )

    @preset_dashboard_is_managed_externally.setter
    def preset_dashboard_is_managed_externally(
        self, preset_dashboard_is_managed_externally: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_is_managed_externally = (
            preset_dashboard_is_managed_externally
        )

    @property
    def preset_dashboard_is_published(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_is_published
        )

    @preset_dashboard_is_published.setter
    def preset_dashboard_is_published(
        self, preset_dashboard_is_published: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_is_published = preset_dashboard_is_published

    @property
    def preset_dashboard_thumbnail_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_thumbnail_url
        )

    @preset_dashboard_thumbnail_url.setter
    def preset_dashboard_thumbnail_url(
        self, preset_dashboard_thumbnail_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_thumbnail_url = preset_dashboard_thumbnail_url

    @property
    def preset_dashboard_chart_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.preset_dashboard_chart_count
        )

    @preset_dashboard_chart_count.setter
    def preset_dashboard_chart_count(self, preset_dashboard_chart_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_dashboard_chart_count = preset_dashboard_chart_count

    @property
    def preset_datasets(self) -> Optional[List[PresetDataset]]:
        return None if self.attributes is None else self.attributes.preset_datasets

    @preset_datasets.setter
    def preset_datasets(self, preset_datasets: Optional[List[PresetDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_datasets = preset_datasets

    @property
    def preset_charts(self) -> Optional[List[PresetChart]]:
        return None if self.attributes is None else self.attributes.preset_charts

    @preset_charts.setter
    def preset_charts(self, preset_charts: Optional[List[PresetChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_charts = preset_charts

    @property
    def preset_workspace(self) -> Optional[PresetWorkspace]:
        return None if self.attributes is None else self.attributes.preset_workspace

    @preset_workspace.setter
    def preset_workspace(self, preset_workspace: Optional[PresetWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.preset_workspace = preset_workspace

    class Attributes(Preset.Attributes):
        preset_dashboard_changed_by_name: Optional[str] = Field(
            default=None, description=""
        )
        preset_dashboard_changed_by_url: Optional[str] = Field(
            default=None, description=""
        )
        preset_dashboard_is_managed_externally: Optional[bool] = Field(
            default=None, description=""
        )
        preset_dashboard_is_published: Optional[bool] = Field(
            default=None, description=""
        )
        preset_dashboard_thumbnail_url: Optional[str] = Field(
            default=None, description=""
        )
        preset_dashboard_chart_count: Optional[int] = Field(
            default=None, description=""
        )
        preset_datasets: Optional[List[PresetDataset]] = Field(
            default=None, description=""
        )  # relationship
        preset_charts: Optional[List[PresetChart]] = Field(
            default=None, description=""
        )  # relationship
        preset_workspace: Optional[PresetWorkspace] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            preset_workspace_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> PresetDashboard.Attributes:
            validate_required_fields(
                ["name", "preset_workspace_qualified_name"],
                [name, preset_workspace_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    preset_workspace_qualified_name,
                    "preset_workspace_qualified_name",
                    4,
                )

            return PresetDashboard.Attributes(
                name=name,
                preset_workspace_qualified_name=preset_workspace_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{preset_workspace_qualified_name}/{name}",
                connector_name=connector_name,
                preset_workspace=PresetWorkspace.ref_by_qualified_name(
                    preset_workspace_qualified_name
                ),
            )

    attributes: PresetDashboard.Attributes = Field(
        default_factory=lambda: PresetDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .preset_chart import PresetChart  # noqa
from .preset_dataset import PresetDataset  # noqa
from .preset_workspace import PresetWorkspace  # noqa
