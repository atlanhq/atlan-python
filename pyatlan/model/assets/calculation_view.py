# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .s_q_l import SQL


class CalculationView(SQL):
    """Description"""

    type_name: str = Field(default="CalculationView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CalculationView":
            raise ValueError("must be CalculationView")
        return v

    def __setattr__(self, name, value):
        if name in CalculationView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COLUMN_COUNT: ClassVar[NumericField] = NumericField("columnCount", "columnCount")
    """
    Number of columns in this calculation view.
    """
    CALCULATION_VIEW_VERSION_ID: ClassVar[NumericField] = NumericField(
        "calculationViewVersionId", "calculationViewVersionId"
    )
    """
    The version ID of this calculation view.
    """
    CALCULATION_VIEW_ACTIVATED_BY: ClassVar[KeywordField] = KeywordField(
        "calculationViewActivatedBy", "calculationViewActivatedBy"
    )
    """
    The owner who activated the calculation view
    """
    CALCULATION_VIEW_ACTIVATED_AT: ClassVar[NumericField] = NumericField(
        "calculationViewActivatedAt", "calculationViewActivatedAt"
    )
    """
    Time at which this calculation view was activated at
    """

    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    ATLAN_SCHEMA: ClassVar[RelationField] = RelationField("atlanSchema")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "column_count",
        "calculation_view_version_id",
        "calculation_view_activated_by",
        "calculation_view_activated_at",
        "columns",
        "atlan_schema",
    ]

    @property
    def column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.column_count

    @column_count.setter
    def column_count(self, column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_count = column_count

    @property
    def calculation_view_version_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.calculation_view_version_id
        )

    @calculation_view_version_id.setter
    def calculation_view_version_id(self, calculation_view_version_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_version_id = calculation_view_version_id

    @property
    def calculation_view_activated_by(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.calculation_view_activated_by
        )

    @calculation_view_activated_by.setter
    def calculation_view_activated_by(
        self, calculation_view_activated_by: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_activated_by = calculation_view_activated_by

    @property
    def calculation_view_activated_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.calculation_view_activated_at
        )

    @calculation_view_activated_at.setter
    def calculation_view_activated_at(
        self, calculation_view_activated_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_activated_at = calculation_view_activated_at

    @property
    def columns(self) -> Optional[List[Column]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[List[Column]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def atlan_schema(self) -> Optional[Schema]:
        return None if self.attributes is None else self.attributes.atlan_schema

    @atlan_schema.setter
    def atlan_schema(self, atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_schema = atlan_schema

    class Attributes(SQL.Attributes):
        column_count: Optional[int] = Field(default=None, description="")
        calculation_view_version_id: Optional[int] = Field(default=None, description="")
        calculation_view_activated_by: Optional[str] = Field(
            default=None, description=""
        )
        calculation_view_activated_at: Optional[datetime] = Field(
            default=None, description=""
        )
        columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship

    attributes: CalculationView.Attributes = Field(
        default_factory=lambda: CalculationView.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .column import Column  # noqa
from .schema import Schema  # noqa
