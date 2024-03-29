# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .sisense import Sisense


class SisenseDatamodelTable(Sisense):
    """Description"""

    type_name: str = Field(default="SisenseDatamodelTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SisenseDatamodelTable":
            raise ValueError("must be SisenseDatamodelTable")
        return v

    def __setattr__(self, name, value):
        if name in SisenseDatamodelTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SISENSE_DATAMODEL_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sisenseDatamodelQualifiedName",
        "sisenseDatamodelQualifiedName",
        "sisenseDatamodelQualifiedName.text",
    )
    """
    Unique name of the datamodel in which this datamodel table exists.
    """
    SISENSE_DATAMODEL_TABLE_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "sisenseDatamodelTableColumnCount", "sisenseDatamodelTableColumnCount"
    )
    """
    Number of columns present in this datamodel table.
    """
    SISENSE_DATAMODEL_TABLE_TYPE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableType", "sisenseDatamodelTableType"
    )
    """
    Type of this datamodel table, for example: 'base' for regular tables, 'custom' for SQL expression-based tables.
    """
    SISENSE_DATAMODEL_TABLE_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableExpression", "sisenseDatamodelTableExpression"
    )
    """
    SQL expression of this datamodel table.
    """
    SISENSE_DATAMODEL_TABLE_IS_MATERIALIZED: ClassVar[BooleanField] = BooleanField(
        "sisenseDatamodelTableIsMaterialized", "sisenseDatamodelTableIsMaterialized"
    )
    """
    Whether this datamodel table is materialised (true) or not (false).
    """
    SISENSE_DATAMODEL_TABLE_IS_HIDDEN: ClassVar[BooleanField] = BooleanField(
        "sisenseDatamodelTableIsHidden", "sisenseDatamodelTableIsHidden"
    )
    """
    Whether this datamodel table is hidden in Sisense (true) or not (false).
    """
    SISENSE_DATAMODEL_TABLE_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableSchedule", "sisenseDatamodelTableSchedule"
    )
    """
    JSON specifying the refresh schedule of this datamodel table.
    """
    SISENSE_DATAMODEL_TABLE_LIVE_QUERY_SETTINGS: ClassVar[KeywordField] = KeywordField(
        "sisenseDatamodelTableLiveQuerySettings",
        "sisenseDatamodelTableLiveQuerySettings",
    )
    """
    JSON specifying the LiveQuery settings of this datamodel table.
    """

    SISENSE_DATAMODEL: ClassVar[RelationField] = RelationField("sisenseDatamodel")
    """
    TBC
    """
    SISENSE_WIDGETS: ClassVar[RelationField] = RelationField("sisenseWidgets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sisense_datamodel_qualified_name",
        "sisense_datamodel_table_column_count",
        "sisense_datamodel_table_type",
        "sisense_datamodel_table_expression",
        "sisense_datamodel_table_is_materialized",
        "sisense_datamodel_table_is_hidden",
        "sisense_datamodel_table_schedule",
        "sisense_datamodel_table_live_query_settings",
        "sisense_datamodel",
        "sisense_widgets",
    ]

    @property
    def sisense_datamodel_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_qualified_name
        )

    @sisense_datamodel_qualified_name.setter
    def sisense_datamodel_qualified_name(
        self, sisense_datamodel_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_qualified_name = (
            sisense_datamodel_qualified_name
        )

    @property
    def sisense_datamodel_table_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_column_count
        )

    @sisense_datamodel_table_column_count.setter
    def sisense_datamodel_table_column_count(
        self, sisense_datamodel_table_column_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_column_count = (
            sisense_datamodel_table_column_count
        )

    @property
    def sisense_datamodel_table_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_type
        )

    @sisense_datamodel_table_type.setter
    def sisense_datamodel_table_type(self, sisense_datamodel_table_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_type = sisense_datamodel_table_type

    @property
    def sisense_datamodel_table_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_expression
        )

    @sisense_datamodel_table_expression.setter
    def sisense_datamodel_table_expression(
        self, sisense_datamodel_table_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_expression = (
            sisense_datamodel_table_expression
        )

    @property
    def sisense_datamodel_table_is_materialized(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_is_materialized
        )

    @sisense_datamodel_table_is_materialized.setter
    def sisense_datamodel_table_is_materialized(
        self, sisense_datamodel_table_is_materialized: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_is_materialized = (
            sisense_datamodel_table_is_materialized
        )

    @property
    def sisense_datamodel_table_is_hidden(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_is_hidden
        )

    @sisense_datamodel_table_is_hidden.setter
    def sisense_datamodel_table_is_hidden(
        self, sisense_datamodel_table_is_hidden: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_is_hidden = (
            sisense_datamodel_table_is_hidden
        )

    @property
    def sisense_datamodel_table_schedule(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_schedule
        )

    @sisense_datamodel_table_schedule.setter
    def sisense_datamodel_table_schedule(
        self, sisense_datamodel_table_schedule: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_schedule = (
            sisense_datamodel_table_schedule
        )

    @property
    def sisense_datamodel_table_live_query_settings(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sisense_datamodel_table_live_query_settings
        )

    @sisense_datamodel_table_live_query_settings.setter
    def sisense_datamodel_table_live_query_settings(
        self, sisense_datamodel_table_live_query_settings: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel_table_live_query_settings = (
            sisense_datamodel_table_live_query_settings
        )

    @property
    def sisense_datamodel(self) -> Optional[SisenseDatamodel]:
        return None if self.attributes is None else self.attributes.sisense_datamodel

    @sisense_datamodel.setter
    def sisense_datamodel(self, sisense_datamodel: Optional[SisenseDatamodel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_datamodel = sisense_datamodel

    @property
    def sisense_widgets(self) -> Optional[List[SisenseWidget]]:
        return None if self.attributes is None else self.attributes.sisense_widgets

    @sisense_widgets.setter
    def sisense_widgets(self, sisense_widgets: Optional[List[SisenseWidget]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sisense_widgets = sisense_widgets

    class Attributes(Sisense.Attributes):
        sisense_datamodel_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sisense_datamodel_table_column_count: Optional[int] = Field(
            default=None, description=""
        )
        sisense_datamodel_table_type: Optional[str] = Field(
            default=None, description=""
        )
        sisense_datamodel_table_expression: Optional[str] = Field(
            default=None, description=""
        )
        sisense_datamodel_table_is_materialized: Optional[bool] = Field(
            default=None, description=""
        )
        sisense_datamodel_table_is_hidden: Optional[bool] = Field(
            default=None, description=""
        )
        sisense_datamodel_table_schedule: Optional[str] = Field(
            default=None, description=""
        )
        sisense_datamodel_table_live_query_settings: Optional[str] = Field(
            default=None, description=""
        )
        sisense_datamodel: Optional[SisenseDatamodel] = Field(
            default=None, description=""
        )  # relationship
        sisense_widgets: Optional[List[SisenseWidget]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SisenseDatamodelTable.Attributes = Field(
        default_factory=lambda: SisenseDatamodelTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sisense_datamodel import SisenseDatamodel  # noqa
from .sisense_widget import SisenseWidget  # noqa
