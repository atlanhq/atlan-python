# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .sisense import Sisense


class SisenseWidget(Sisense):
    """Description"""

    type_name: str = Field(default="SisenseWidget", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseWidget":
            raise ValueError("must be SisenseWidget")
        return v

    def __setattr__(self, name, value):
        if name in SisenseWidget._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_WIDGET_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseWidgetColumnCount", "sisenseWidgetColumnCount"
    )
    """
    Number of columns used in this widget.
    """
    SISENSE_WIDGET_SUB_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseWidgetSubType", "sisenseWidgetSubType"
    )
    """
    Subtype of this widget.
    """
    SISENSE_WIDGET_SIZE: ClassVar[KeywordField] = KeywordField(
        "sisenseWidgetSize", "sisenseWidgetSize"
    )
    """
    Size of this widget.
    """
    SISENSE_WIDGET_DASHBOARD_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "sisenseWidgetDashboardQualifiedName",
            "sisenseWidgetDashboardQualifiedName",
            "sisenseWidgetDashboardQualifiedName.text",
        )
    )
    """
    Unique name of the dashboard in which this widget exists.
    """
    SISENSE_WIDGET_FOLDER_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sisenseWidgetFolderQualifiedName",
        "sisenseWidgetFolderQualifiedName",
        "sisenseWidgetFolderQualifiedName.text",
    )
    """
    Unique name of the folder in which this widget exists.
    """

    SISENSE_DATAMODEL_TABLES: ClassVar[RelationField] = RelationField(
        "sisenseDatamodelTables"
    )
    """
    TBC
    """
    SISENSE_FOLDER: ClassVar[RelationField] = RelationField("sisenseFolder")
    """
    TBC
    """
    SISENSE_DASHBOARD: ClassVar[RelationField] = RelationField("sisenseDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sisense_widget_column_count",
        "sisense_widget_sub_type",
        "sisense_widget_size",
        "sisense_widget_dashboard_qualified_name",
        "sisense_widget_folder_qualified_name",
        "sisense_datamodel_tables",
        "sisense_folder",
        "sisense_dashboard",
    ]

    @property
    def sisense_widget_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_widget_column_count
        )

    @sisense_widget_column_count.setter
    def sisense_widget_column_count(self, sisense_widget_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_column_count = sisense_widget_column_count

    @property
    def sisense_widget_sub_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sisense_widget_sub_type
        )

    @sisense_widget_sub_type.setter
    def sisense_widget_sub_type(self, sisense_widget_sub_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_sub_type = sisense_widget_sub_type

    @property
    def sisense_widget_size(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sisense_widget_size

    @sisense_widget_size.setter
    def sisense_widget_size(self, sisense_widget_size: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_size = sisense_widget_size

    @property
    def sisense_widget_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_widget_dashboard_qualified_name
        )

    @sisense_widget_dashboard_qualified_name.setter
    def sisense_widget_dashboard_qualified_name(
        self, sisense_widget_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_dashboard_qualified_name = (
            sisense_widget_dashboard_qualified_name
        )

    @property
    def sisense_widget_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_widget_folder_qualified_name
        )

    @sisense_widget_folder_qualified_name.setter
    def sisense_widget_folder_qualified_name(
        self, sisense_widget_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widget_folder_qualified_name = (
            sisense_widget_folder_qualified_name
        )

    @property
    def sisense_datamodel_tables(self) -> Optional[List[SisenseDatamodelTable]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_tables
        )

    @sisense_datamodel_tables.setter
    def sisense_datamodel_tables(
        self, sisense_datamodel_tables: Optional[List[SisenseDatamodelTable]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_tables = sisense_datamodel_tables

    @property
    def sisense_folder(self) -> Optional[SisenseFolder]:
        return None if self.attributes is None else self.attributes.sisense_folder

    @sisense_folder.setter
    def sisense_folder(self, sisense_folder: Optional[SisenseFolder]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_folder = sisense_folder

    @property
    def sisense_dashboard(self) -> Optional[SisenseDashboard]:
        return None if self.attributes is None else self.attributes.sisense_dashboard

    @sisense_dashboard.setter
    def sisense_dashboard(self, sisense_dashboard: Optional[SisenseDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_dashboard = sisense_dashboard

    class Attributes(Sisense.Attributes):
        sisense_widget_column_count: Optional[int] = Field(default=None, description="")
        sisense_widget_sub_type: Optional[str] = Field(default=None, description="")
        sisense_widget_size: Optional[str] = Field(default=None, description="")
        sisense_widget_dashboard_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sisense_widget_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sisense_datamodel_tables: Optional[List[SisenseDatamodelTable]] = Field(
            default=None, description=""
        )  # relationship
        sisense_folder: Optional[SisenseFolder] = Field(
            default=None, description=""
        )  # relationship
        sisense_dashboard: Optional[SisenseDashboard] = Field(
            default=None, description=""
        )  # relationship

    attributes: SisenseWidget.Attributes = Field(
        default_factory=lambda: SisenseWidget.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sisense_dashboard import SisenseDashboard  # noqa
from .sisense_datamodel_table import SisenseDatamodelTable  # noqa
from .sisense_folder import SisenseFolder  # noqa
