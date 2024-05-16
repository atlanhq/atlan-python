# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .asset53 import Thoughtspot


class ThoughtspotWorksheet(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotWorksheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotWorksheet":
            raise ValueError("must be ThoughtspotWorksheet")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotWorksheet._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_COLUMNS: ClassVar[RelationField] = RelationField("thoughtspotColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "thoughtspot_columns",
    ]

    @property
    def thoughtspot_columns(self) -> Optional[list[ThoughtspotColumn]]:
        return None if self.attributes is None else self.attributes.thoughtspot_columns

    @thoughtspot_columns.setter
    def thoughtspot_columns(
        self, thoughtspot_columns: Optional[list[ThoughtspotColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_columns = thoughtspot_columns

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_columns: Optional[list[ThoughtspotColumn]] = Field(
            None, description="", alias="thoughtspotColumns"
        )  # relationship

    attributes: "ThoughtspotWorksheet.Attributes" = Field(
        default_factory=lambda: ThoughtspotWorksheet.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotTable(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotTable":
            raise ValueError("must be ThoughtspotTable")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_COLUMNS: ClassVar[RelationField] = RelationField("thoughtspotColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "thoughtspot_columns",
    ]

    @property
    def thoughtspot_columns(self) -> Optional[list[ThoughtspotColumn]]:
        return None if self.attributes is None else self.attributes.thoughtspot_columns

    @thoughtspot_columns.setter
    def thoughtspot_columns(
        self, thoughtspot_columns: Optional[list[ThoughtspotColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_columns = thoughtspot_columns

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_columns: Optional[list[ThoughtspotColumn]] = Field(
            None, description="", alias="thoughtspotColumns"
        )  # relationship

    attributes: "ThoughtspotTable.Attributes" = Field(
        default_factory=lambda: ThoughtspotTable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotColumn(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotColumn", allow_mutation=False)

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

    _convenience_properties: ClassVar[list[str]] = [
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
            None, description="", alias="thoughtspotTableQualifiedName"
        )
        thoughtspot_view_qualified_name: Optional[str] = Field(
            None, description="", alias="thoughtspotViewQualifiedName"
        )
        thoughtspot_worksheet_qualified_name: Optional[str] = Field(
            None, description="", alias="thoughtspotWorksheetQualifiedName"
        )
        thoughtspot_column_data_type: Optional[str] = Field(
            None, description="", alias="thoughtspotColumnDataType"
        )
        thoughtspot_column_type: Optional[str] = Field(
            None, description="", alias="thoughtspotColumnType"
        )
        thoughtspot_table: Optional[ThoughtspotTable] = Field(
            None, description="", alias="thoughtspotTable"
        )  # relationship
        thoughtspot_view: Optional[ThoughtspotView] = Field(
            None, description="", alias="thoughtspotView"
        )  # relationship
        thoughtspot_worksheet: Optional[ThoughtspotWorksheet] = Field(
            None, description="", alias="thoughtspotWorksheet"
        )  # relationship

    attributes: "ThoughtspotColumn.Attributes" = Field(
        default_factory=lambda: ThoughtspotColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class ThoughtspotView(Thoughtspot):
    """Description"""

    type_name: str = Field("ThoughtspotView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotView":
            raise ValueError("must be ThoughtspotView")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_COLUMNS: ClassVar[RelationField] = RelationField("thoughtspotColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "thoughtspot_columns",
    ]

    @property
    def thoughtspot_columns(self) -> Optional[list[ThoughtspotColumn]]:
        return None if self.attributes is None else self.attributes.thoughtspot_columns

    @thoughtspot_columns.setter
    def thoughtspot_columns(
        self, thoughtspot_columns: Optional[list[ThoughtspotColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_columns = thoughtspot_columns

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_columns: Optional[list[ThoughtspotColumn]] = Field(
            None, description="", alias="thoughtspotColumns"
        )  # relationship

    attributes: "ThoughtspotView.Attributes" = Field(
        default_factory=lambda: ThoughtspotView.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


ThoughtspotWorksheet.Attributes.update_forward_refs()


ThoughtspotTable.Attributes.update_forward_refs()


ThoughtspotColumn.Attributes.update_forward_refs()


ThoughtspotView.Attributes.update_forward_refs()
