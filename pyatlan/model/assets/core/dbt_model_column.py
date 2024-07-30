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

from .dbt import Dbt


class DbtModelColumn(Dbt):
    """Description"""

    type_name: str = Field(default="DbtModelColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtModelColumn":
            raise ValueError("must be DbtModelColumn")
        return v

    def __setattr__(self, name, value):
        if name in DbtModelColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_MODEL_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtModelQualifiedName", "dbtModelQualifiedName", "dbtModelQualifiedName.text"
    )
    """

    """
    DBT_MODEL_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "dbtModelColumnDataType", "dbtModelColumnDataType"
    )
    """

    """
    DBT_MODEL_COLUMN_ORDER: ClassVar[NumericField] = NumericField(
        "dbtModelColumnOrder", "dbtModelColumnOrder"
    )
    """

    """

    SQL_COLUMN: ClassVar[RelationField] = RelationField("sqlColumn")
    """
    TBC
    """
    DBT_MODEL: ClassVar[RelationField] = RelationField("dbtModel")
    """
    TBC
    """
    DBT_MODEL_COLUMN_SQL_COLUMNS: ClassVar[RelationField] = RelationField(
        "dbtModelColumnSqlColumns"
    )
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dbt_model_qualified_name",
        "dbt_model_column_data_type",
        "dbt_model_column_order",
        "sql_column",
        "dbt_model",
        "dbt_model_column_sql_columns",
        "dbt_tests",
    ]

    @property
    def dbt_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_qualified_name
        )

    @dbt_model_qualified_name.setter
    def dbt_model_qualified_name(self, dbt_model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_qualified_name = dbt_model_qualified_name

    @property
    def dbt_model_column_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_column_data_type
        )

    @dbt_model_column_data_type.setter
    def dbt_model_column_data_type(self, dbt_model_column_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_data_type = dbt_model_column_data_type

    @property
    def dbt_model_column_order(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.dbt_model_column_order
        )

    @dbt_model_column_order.setter
    def dbt_model_column_order(self, dbt_model_column_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_order = dbt_model_column_order

    @property
    def sql_column(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.sql_column

    @sql_column.setter
    def sql_column(self, sql_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_column = sql_column

    @property
    def dbt_model(self) -> Optional[DbtModel]:
        return None if self.attributes is None else self.attributes.dbt_model

    @dbt_model.setter
    def dbt_model(self, dbt_model: Optional[DbtModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model = dbt_model

    @property
    def dbt_model_column_sql_columns(self) -> Optional[List[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_column_sql_columns
        )

    @dbt_model_column_sql_columns.setter
    def dbt_model_column_sql_columns(
        self, dbt_model_column_sql_columns: Optional[List[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_column_sql_columns = dbt_model_column_sql_columns

    @property
    def dbt_tests(self) -> Optional[List[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[List[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    class Attributes(Dbt.Attributes):
        dbt_model_qualified_name: Optional[str] = Field(default=None, description="")
        dbt_model_column_data_type: Optional[str] = Field(default=None, description="")
        dbt_model_column_order: Optional[int] = Field(default=None, description="")
        sql_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_column_sql_columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[List[DbtTest]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DbtModelColumn.Attributes = Field(
        default_factory=lambda: DbtModelColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .column import Column  # noqa
from .dbt_model import DbtModel  # noqa
from .dbt_test import DbtTest  # noqa
