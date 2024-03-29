# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    RelationField,
    TextField,
)

from .power_b_i import PowerBI


class PowerBIMeasure(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIMeasure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIMeasure":
            raise ValueError("must be PowerBIMeasure")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIMeasure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this measure exists.
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    Unique name of the dataset in which this measure exists.
    """
    POWER_BI_MEASURE_EXPRESSION: ClassVar[TextField] = TextField(
        "powerBIMeasureExpression", "powerBIMeasureExpression"
    )
    """
    DAX expression for this measure.
    """
    POWER_BI_IS_EXTERNAL_MEASURE: ClassVar[BooleanField] = BooleanField(
        "powerBIIsExternalMeasure", "powerBIIsExternalMeasure"
    )
    """
    Whether this measure is external (true) or internal (false).
    """

    TABLE: ClassVar[RelationField] = RelationField("table")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_measure_expression",
        "power_b_i_is_external_measure",
        "table",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dataset_qualified_name
        )

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_measure_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_measure_expression
        )

    @power_b_i_measure_expression.setter
    def power_b_i_measure_expression(self, power_b_i_measure_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_measure_expression = power_b_i_measure_expression

    @property
    def power_b_i_is_external_measure(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_is_external_measure
        )

    @power_b_i_is_external_measure.setter
    def power_b_i_is_external_measure(
        self, power_b_i_is_external_measure: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_is_external_measure = power_b_i_is_external_measure

    @property
    def table(self) -> Optional[PowerBITable]:
        return None if self.attributes is None else self.attributes.table

    @table.setter
    def table(self, table: Optional[PowerBITable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table = table

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        dataset_qualified_name: Optional[str] = Field(default=None, description="")
        power_b_i_measure_expression: Optional[str] = Field(
            default=None, description=""
        )
        power_b_i_is_external_measure: Optional[bool] = Field(
            default=None, description=""
        )
        table: Optional[PowerBITable] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIMeasure.Attributes = Field(
        default_factory=lambda: PowerBIMeasure.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_table import PowerBITable  # noqa
