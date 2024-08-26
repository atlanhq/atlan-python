# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordTextStemmedField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .superset import Superset


class SupersetDashboard(Superset):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> SupersetDashboard:
        validate_required_fields(
            ["name", "connection_qualified_name"],
            [name, connection_qualified_name],
        )
        attributes = SupersetDashboard.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> SupersetDashboard:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )

    type_name: str = Field(default="SupersetDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SupersetDashboard":
            raise ValueError("must be SupersetDashboard")
        return v

    def __setattr__(self, name, value):
        if name in SupersetDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SUPERSET_DASHBOARD_CHANGED_BY_NAME: ClassVar[KeywordTextStemmedField] = (
        KeywordTextStemmedField(
            "supersetDashboardChangedByName",
            "supersetDashboardChangedByName.keyword",
            "supersetDashboardChangedByName",
            "supersetDashboardChangedByName.stemmed",
        )
    )
    """
    Name of the user who changed the dashboard.
    """
    SUPERSET_DASHBOARD_CHANGED_BY_URL: ClassVar[TextField] = TextField(
        "supersetDashboardChangedByURL", "supersetDashboardChangedByURL"
    )
    """
    URL of the user profile that changed the dashboard
    """
    SUPERSET_DASHBOARD_IS_MANAGED_EXTERNALLY: ClassVar[BooleanField] = BooleanField(
        "supersetDashboardIsManagedExternally", "supersetDashboardIsManagedExternally"
    )
    """
    Whether the dashboard is manager externally (true) or not (false).
    """
    SUPERSET_DASHBOARD_IS_PUBLISHED: ClassVar[BooleanField] = BooleanField(
        "supersetDashboardIsPublished", "supersetDashboardIsPublished"
    )
    """
    Whether the dashboard is published (true) or not (false).
    """
    SUPERSET_DASHBOARD_THUMBNAIL_URL: ClassVar[TextField] = TextField(
        "supersetDashboardThumbnailURL", "supersetDashboardThumbnailURL"
    )
    """
    URL for the dashboard thumbnail image in superset.
    """
    SUPERSET_DASHBOARD_CHART_COUNT: ClassVar[NumericField] = NumericField(
        "supersetDashboardChartCount", "supersetDashboardChartCount"
    )
    """
    Count of charts present in the dashboard.
    """

    SUPERSET_DATASETS: ClassVar[RelationField] = RelationField("supersetDatasets")
    """
    TBC
    """
    SUPERSET_CHARTS: ClassVar[RelationField] = RelationField("supersetCharts")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "superset_dashboard_changed_by_name",
        "superset_dashboard_changed_by_url",
        "superset_dashboard_is_managed_externally",
        "superset_dashboard_is_published",
        "superset_dashboard_thumbnail_url",
        "superset_dashboard_chart_count",
        "superset_datasets",
        "superset_charts",
    ]

    @property
    def superset_dashboard_changed_by_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dashboard_changed_by_name
        )

    @superset_dashboard_changed_by_name.setter
    def superset_dashboard_changed_by_name(
        self, superset_dashboard_changed_by_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_changed_by_name = (
            superset_dashboard_changed_by_name
        )

    @property
    def superset_dashboard_changed_by_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dashboard_changed_by_url
        )

    @superset_dashboard_changed_by_url.setter
    def superset_dashboard_changed_by_url(
        self, superset_dashboard_changed_by_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_changed_by_url = (
            superset_dashboard_changed_by_url
        )

    @property
    def superset_dashboard_is_managed_externally(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dashboard_is_managed_externally
        )

    @superset_dashboard_is_managed_externally.setter
    def superset_dashboard_is_managed_externally(
        self, superset_dashboard_is_managed_externally: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_is_managed_externally = (
            superset_dashboard_is_managed_externally
        )

    @property
    def superset_dashboard_is_published(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dashboard_is_published
        )

    @superset_dashboard_is_published.setter
    def superset_dashboard_is_published(
        self, superset_dashboard_is_published: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_is_published = (
            superset_dashboard_is_published
        )

    @property
    def superset_dashboard_thumbnail_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dashboard_thumbnail_url
        )

    @superset_dashboard_thumbnail_url.setter
    def superset_dashboard_thumbnail_url(
        self, superset_dashboard_thumbnail_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_thumbnail_url = (
            superset_dashboard_thumbnail_url
        )

    @property
    def superset_dashboard_chart_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.superset_dashboard_chart_count
        )

    @superset_dashboard_chart_count.setter
    def superset_dashboard_chart_count(
        self, superset_dashboard_chart_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_dashboard_chart_count = superset_dashboard_chart_count

    @property
    def superset_datasets(self) -> Optional[List[SupersetDataset]]:
        return None if self.attributes is None else self.attributes.superset_datasets

    @superset_datasets.setter
    def superset_datasets(self, superset_datasets: Optional[List[SupersetDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_datasets = superset_datasets

    @property
    def superset_charts(self) -> Optional[List[SupersetChart]]:
        return None if self.attributes is None else self.attributes.superset_charts

    @superset_charts.setter
    def superset_charts(self, superset_charts: Optional[List[SupersetChart]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.superset_charts = superset_charts

    class Attributes(Superset.Attributes):
        superset_dashboard_changed_by_name: Optional[str] = Field(
            default=None, description=""
        )
        superset_dashboard_changed_by_url: Optional[str] = Field(
            default=None, description=""
        )
        superset_dashboard_is_managed_externally: Optional[bool] = Field(
            default=None, description=""
        )
        superset_dashboard_is_published: Optional[bool] = Field(
            default=None, description=""
        )
        superset_dashboard_thumbnail_url: Optional[str] = Field(
            default=None, description=""
        )
        superset_dashboard_chart_count: Optional[int] = Field(
            default=None, description=""
        )
        superset_datasets: Optional[List[SupersetDataset]] = Field(
            default=None, description=""
        )  # relationship
        superset_charts: Optional[List[SupersetChart]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> SupersetDashboard.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"],
                [name, connection_qualified_name],
            )
            return SupersetDashboard.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: SupersetDashboard.Attributes = Field(
        default_factory=lambda: SupersetDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .superset_chart import SupersetChart  # noqa
from .superset_dataset import SupersetDataset  # noqa

SupersetDashboard.Attributes.update_forward_refs()
