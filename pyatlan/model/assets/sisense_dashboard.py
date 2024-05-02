# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordTextField,
    NumericField,
    RelationField,
)

from .sisense import Sisense


class SisenseDashboard(Sisense):
    """Description"""

    type_name: str = Field(default="SisenseDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseDashboard":
            raise ValueError("must be SisenseDashboard")
        return v

    def __setattr__(self, name, value):
        if name in SisenseDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_DASHBOARD_FOLDER_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "sisenseDashboardFolderQualifiedName",
            "sisenseDashboardFolderQualifiedName",
            "sisenseDashboardFolderQualifiedName.text",
        )
    )
    """
    Unique name of the folder in which this dashboard exists.
    """
    SISENSE_DASHBOARD_WIDGET_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseDashboardWidgetCount", "sisenseDashboardWidgetCount"
    )
    """
    Number of widgets in this dashboard.
    """

    SISENSE_DATAMODELS: ClassVar[RelationField] = RelationField("sisenseDatamodels")
    """
    TBC
    """
    SISENSE_WIDGETS: ClassVar[RelationField] = RelationField("sisenseWidgets")
    """
    TBC
    """
    SISENSE_FOLDER: ClassVar[RelationField] = RelationField("sisenseFolder")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sisense_dashboard_folder_qualified_name",
        "sisense_dashboard_widget_count",
        "sisense_datamodels",
        "sisense_widgets",
        "sisense_folder",
    ]

    @property
    def sisense_dashboard_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_dashboard_folder_qualified_name
        )

    @sisense_dashboard_folder_qualified_name.setter
    def sisense_dashboard_folder_qualified_name(
        self, sisense_dashboard_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboard_folder_qualified_name = (
            sisense_dashboard_folder_qualified_name
        )

    @property
    def sisense_dashboard_widget_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_dashboard_widget_count
        )

    @sisense_dashboard_widget_count.setter
    def sisense_dashboard_widget_count(
        self, sisense_dashboard_widget_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboard_widget_count = sisense_dashboard_widget_count

    @property
    def sisense_datamodels(self) -> Optional[List[SisenseDatamodel]]:
        return None if self.attributes is None else self.attributes.sisense_datamodels

    @sisense_datamodels.setter
    def sisense_datamodels(self, sisense_datamodels: Optional[List[SisenseDatamodel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodels = sisense_datamodels

    @property
    def sisense_widgets(self) -> Optional[List[SisenseWidget]]:
        return None if self.attributes is None else self.attributes.sisense_widgets

    @sisense_widgets.setter
    def sisense_widgets(self, sisense_widgets: Optional[List[SisenseWidget]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widgets = sisense_widgets

    @property
    def sisense_folder(self) -> Optional[SisenseFolder]:
        return None if self.attributes is None else self.attributes.sisense_folder

    @sisense_folder.setter
    def sisense_folder(self, sisense_folder: Optional[SisenseFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_folder = sisense_folder

    class Attributes(Sisense.Attributes):
        sisense_dashboard_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sisense_dashboard_widget_count: Optional[int] = Field(
            default=None, description=""
        )
        sisense_datamodels: Optional[List[SisenseDatamodel]] = Field(
            default=None, description=""
        )  # relationship
        sisense_widgets: Optional[List[SisenseWidget]] = Field(
            default=None, description=""
        )  # relationship
        sisense_folder: Optional[SisenseFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: SisenseDashboard.Attributes = Field(
        default_factory=lambda: SisenseDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sisense_datamodel import SisenseDatamodel  # noqa
from .sisense_folder import SisenseFolder  # noqa
from .sisense_widget import SisenseWidget  # noqa
