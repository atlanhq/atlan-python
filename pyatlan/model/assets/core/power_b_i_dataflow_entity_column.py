# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .power_b_i import PowerBI


class PowerBIDataflowEntityColumn(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIDataflowEntityColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataflowEntityColumn":
            raise ValueError("must be PowerBIDataflowEntityColumn")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataflowEntityColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    POWER_BI_DATAFLOW_ENTITY_NAME: ClassVar[TextField] = TextField(
        "powerBIDataflowEntityName", "powerBIDataflowEntityName"
    )
    """
    Unique name of the dataflow entity in which this dataflow entity column exists.
    """
    POWER_BI_WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "powerBIWorkspaceQualifiedName", "powerBIWorkspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this dataflow entity column exists.
    """
    POWER_BI_DATAFLOW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "powerBIDataflowQualifiedName", "powerBIDataflowQualifiedName"
    )
    """
    Unique name of the dataflow in which this dataflow entity column exists.
    """
    POWER_BI_DATAFLOW_ENTITY_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "powerBIDataflowEntityColumnDataType", "powerBIDataflowEntityColumnDataType"
    )
    """
    Data type of this dataflow entity column.
    """

    POWER_BI_DATAFLOW: ClassVar[RelationField] = RelationField("powerBIDataflow")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "power_b_i_dataflow_entity_name",
        "power_b_i_workspace_qualified_name",
        "power_b_i_dataflow_qualified_name",
        "power_b_i_dataflow_entity_column_data_type",
        "power_b_i_dataflow",
    ]

    @property
    def power_b_i_dataflow_entity_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_entity_name
        )

    @power_b_i_dataflow_entity_name.setter
    def power_b_i_dataflow_entity_name(
        self, power_b_i_dataflow_entity_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_entity_name = power_b_i_dataflow_entity_name

    @property
    def power_b_i_workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_workspace_qualified_name
        )

    @power_b_i_workspace_qualified_name.setter
    def power_b_i_workspace_qualified_name(
        self, power_b_i_workspace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_workspace_qualified_name = (
            power_b_i_workspace_qualified_name
        )

    @property
    def power_b_i_dataflow_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_qualified_name
        )

    @power_b_i_dataflow_qualified_name.setter
    def power_b_i_dataflow_qualified_name(
        self, power_b_i_dataflow_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_qualified_name = (
            power_b_i_dataflow_qualified_name
        )

    @property
    def power_b_i_dataflow_entity_column_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_entity_column_data_type
        )

    @power_b_i_dataflow_entity_column_data_type.setter
    def power_b_i_dataflow_entity_column_data_type(
        self, power_b_i_dataflow_entity_column_data_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_entity_column_data_type = (
            power_b_i_dataflow_entity_column_data_type
        )

    @property
    def power_b_i_dataflow(self) -> Optional[PowerBIDataflow]:
        return None if self.attributes is None else self.attributes.power_b_i_dataflow

    @power_b_i_dataflow.setter
    def power_b_i_dataflow(self, power_b_i_dataflow: Optional[PowerBIDataflow]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow = power_b_i_dataflow

    class Attributes(PowerBI.Attributes):
        power_b_i_dataflow_entity_name: Optional[str] = Field(
            default=None, description=""
        )
        power_b_i_workspace_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        power_b_i_dataflow_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        power_b_i_dataflow_entity_column_data_type: Optional[str] = Field(
            default=None, description=""
        )
        power_b_i_dataflow: Optional[PowerBIDataflow] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIDataflowEntityColumn.Attributes = Field(
        default_factory=lambda: PowerBIDataflowEntityColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dataflow import PowerBIDataflow  # noqa: E402, F401
