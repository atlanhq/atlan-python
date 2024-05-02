# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .thoughtspot import Thoughtspot


class ThoughtspotColumn(Thoughtspot):
    """Description"""

    type_name: str = Field(default="ThoughtspotColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotColumn":
            raise ValueError("must be ThoughtspotColumn")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_TABLE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "thoughtspotTableQualifiedName",
        "thoughtspotTableQualifiedName",
        "thoughtspotTableQualifiedName.text",
    )
    """
    Unique name of the table in which this column exists.
    """
    THOUGHTSPOT_VIEW_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "thoughtspotViewQualifiedName",
        "thoughtspotViewQualifiedName",
        "thoughtspotViewQualifiedName.text",
    )
    """
    Unique name of the view in which this column exists.
    """
    THOUGHTSPOT_WORKSHEET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "thoughtspotWorksheetQualifiedName",
        "thoughtspotWorksheetQualifiedName",
        "thoughtspotWorksheetQualifiedName.text",
    )
    """
    Unique name of the worksheet in which this column exists.
    """
    THOUGHTSPOT_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "thoughtspotColumnDataType", "thoughtspotColumnDataType"
    )
    """
    Specifies the technical format of data stored in a column such as integer, float, string, date, boolean etc.
    """
    THOUGHTSPOT_COLUMN_TYPE: ClassVar[KeywordField] = KeywordField(
        "thoughtspotColumnType", "thoughtspotColumnType"
    )
    """
    Defines the analytical role of a column in data analysis categorizing it as a dimension, measure, or attribute.
    """

    THOUGHTSPOT_TABLE: ClassVar[RelationField] = RelationField("thoughtspotTable")
    """
    TBC
    """
    THOUGHTSPOT_VIEW: ClassVar[RelationField] = RelationField("thoughtspotView")
    """
    TBC
    """
    THOUGHTSPOT_WORKSHEET: ClassVar[RelationField] = RelationField(
        "thoughtspotWorksheet"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "thoughtspot_table_qualified_name",
        "thoughtspot_view_qualified_name",
        "thoughtspot_worksheet_qualified_name",
        "thoughtspot_column_data_type",
        "thoughtspot_column_type",
        "thoughtspot_table",
        "thoughtspot_view",
        "thoughtspot_worksheet",
    ]

    @property
    def thoughtspot_table_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_table_qualified_name
        )

    @thoughtspot_table_qualified_name.setter
    def thoughtspot_table_qualified_name(
        self, thoughtspot_table_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_table_qualified_name = (
            thoughtspot_table_qualified_name
        )

    @property
    def thoughtspot_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_view_qualified_name
        )

    @thoughtspot_view_qualified_name.setter
    def thoughtspot_view_qualified_name(
        self, thoughtspot_view_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_view_qualified_name = (
            thoughtspot_view_qualified_name
        )

    @property
    def thoughtspot_worksheet_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_worksheet_qualified_name
        )

    @thoughtspot_worksheet_qualified_name.setter
    def thoughtspot_worksheet_qualified_name(
        self, thoughtspot_worksheet_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_worksheet_qualified_name = (
            thoughtspot_worksheet_qualified_name
        )

    @property
    def thoughtspot_column_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_column_data_type
        )

    @thoughtspot_column_data_type.setter
    def thoughtspot_column_data_type(self, thoughtspot_column_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_column_data_type = thoughtspot_column_data_type

    @property
    def thoughtspot_column_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.thoughtspot_column_type
        )

    @thoughtspot_column_type.setter
    def thoughtspot_column_type(self, thoughtspot_column_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_column_type = thoughtspot_column_type

    @property
    def thoughtspot_table(self) -> Optional[ThoughtspotTable]:
        return None if self.attributes is None else self.attributes.thoughtspot_table

    @thoughtspot_table.setter
    def thoughtspot_table(self, thoughtspot_table: Optional[ThoughtspotTable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_table = thoughtspot_table

    @property
    def thoughtspot_view(self) -> Optional[ThoughtspotView]:
        return None if self.attributes is None else self.attributes.thoughtspot_view

    @thoughtspot_view.setter
    def thoughtspot_view(self, thoughtspot_view: Optional[ThoughtspotView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_view = thoughtspot_view

    @property
    def thoughtspot_worksheet(self) -> Optional[ThoughtspotWorksheet]:
        return (
            None if self.attributes is None else self.attributes.thoughtspot_worksheet
        )

    @thoughtspot_worksheet.setter
    def thoughtspot_worksheet(
        self, thoughtspot_worksheet: Optional[ThoughtspotWorksheet]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_worksheet = thoughtspot_worksheet

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_table_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        thoughtspot_view_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        thoughtspot_worksheet_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        thoughtspot_column_data_type: Optional[str] = Field(
            default=None, description=""
        )
        thoughtspot_column_type: Optional[str] = Field(default=None, description="")
        thoughtspot_table: Optional[ThoughtspotTable] = Field(
            default=None, description=""
        )  # relationship
        thoughtspot_view: Optional[ThoughtspotView] = Field(
            default=None, description=""
        )  # relationship
        thoughtspot_worksheet: Optional[ThoughtspotWorksheet] = Field(
            default=None, description=""
        )  # relationship

    attributes: ThoughtspotColumn.Attributes = Field(
        default_factory=lambda: ThoughtspotColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .thoughtspot_table import ThoughtspotTable  # noqa
from .thoughtspot_view import ThoughtspotView  # noqa
from .thoughtspot_worksheet import ThoughtspotWorksheet  # noqa
