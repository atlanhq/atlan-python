# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .catalog import Catalog


class FlowField(Catalog):
    """Description"""

    type_name: str = Field(default="FlowField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FlowField":
            raise ValueError("must be FlowField")
        return v

    def __setattr__(self, name, value):
        if name in FlowField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FLOW_DATASET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "flowDatasetName", "flowDatasetName.keyword", "flowDatasetName"
    )
    """
    Simple name of the ephemeral dataset in which this field is contained.
    """
    FLOW_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "flowDatasetQualifiedName", "flowDatasetQualifiedName"
    )
    """
    Unique name of the ephemeral dataset in which this field is contained.
    """
    FLOW_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "flowDataType", "flowDataType"
    )
    """
    Type of the data captured in this field.
    """
    FLOW_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "flowExpression", "flowExpression"
    )
    """
    Logic that is applied, injected or otherwise used as part of producing this ephemeral field of data.
    """
    FLOW_STARTED_AT: ClassVar[NumericField] = NumericField(
        "flowStartedAt", "flowStartedAt"
    )
    """
    Date and time at which this point in the data processing or orchestration started.
    """
    FLOW_FINISHED_AT: ClassVar[NumericField] = NumericField(
        "flowFinishedAt", "flowFinishedAt"
    )
    """
    Date and time at which this point in the data processing or orchestration finished.
    """
    FLOW_STATUS: ClassVar[KeywordField] = KeywordField("flowStatus", "flowStatus")
    """
    Overall status of this point in the data processing or orchestration.
    """
    FLOW_SCHEDULE: ClassVar[KeywordField] = KeywordField("flowSchedule", "flowSchedule")
    """
    Schedule for this point in the data processing or orchestration.
    """
    FLOW_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "flowProjectName", "flowProjectName.keyword", "flowProjectName"
    )
    """
    Simple name of the project in which this asset is contained.
    """
    FLOW_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "flowProjectQualifiedName", "flowProjectQualifiedName"
    )
    """
    Unique name of the project in which this asset is contained.
    """
    FLOW_FOLDER_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "flowFolderName", "flowFolderName.keyword", "flowFolderName"
    )
    """
    Simple name of the folder in which this asset is contained.
    """
    FLOW_FOLDER_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "flowFolderQualifiedName", "flowFolderQualifiedName"
    )
    """
    Unique name of the folder in which this asset is contained.
    """
    FLOW_REUSABLE_UNIT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "flowReusableUnitName", "flowReusableUnitName.keyword", "flowReusableUnitName"
    )
    """
    Simple name of the reusable grouping of operations in which this ephemeral data is contained.
    """
    FLOW_REUSABLE_UNIT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "flowReusableUnitQualifiedName", "flowReusableUnitQualifiedName"
    )
    """
    Unique name of the reusable grouping of operations in which this ephemeral data is contained.
    """
    FLOW_ID: ClassVar[KeywordField] = KeywordField("flowId", "flowId")
    """
    Unique ID for this flow asset, which will remain constant throughout the lifecycle of the asset.
    """
    FLOW_RUN_ID: ClassVar[KeywordField] = KeywordField("flowRunId", "flowRunId")
    """
    Unique ID of the flow run, which could change on subsequent runs of the same flow.
    """
    FLOW_ERROR_MESSAGE: ClassVar[KeywordField] = KeywordField(
        "flowErrorMessage", "flowErrorMessage"
    )
    """
    Optional error message of the flow run.
    """
    FLOW_INPUT_PARAMETERS: ClassVar[KeywordField] = KeywordField(
        "flowInputParameters", "flowInputParameters"
    )
    """
    Input parameters for the flow run.
    """

    FLOW_DATASET: ClassVar[RelationField] = RelationField("flowDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "flow_dataset_name",
        "flow_dataset_qualified_name",
        "flow_data_type",
        "flow_expression",
        "flow_started_at",
        "flow_finished_at",
        "flow_status",
        "flow_schedule",
        "flow_project_name",
        "flow_project_qualified_name",
        "flow_folder_name",
        "flow_folder_qualified_name",
        "flow_reusable_unit_name",
        "flow_reusable_unit_qualified_name",
        "flow_id",
        "flow_run_id",
        "flow_error_message",
        "flow_input_parameters",
        "flow_dataset",
    ]

    @property
    def flow_dataset_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_dataset_name

    @flow_dataset_name.setter
    def flow_dataset_name(self, flow_dataset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_dataset_name = flow_dataset_name

    @property
    def flow_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.flow_dataset_qualified_name
        )

    @flow_dataset_qualified_name.setter
    def flow_dataset_qualified_name(self, flow_dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_dataset_qualified_name = flow_dataset_qualified_name

    @property
    def flow_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_data_type

    @flow_data_type.setter
    def flow_data_type(self, flow_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_data_type = flow_data_type

    @property
    def flow_expression(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_expression

    @flow_expression.setter
    def flow_expression(self, flow_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_expression = flow_expression

    @property
    def flow_started_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.flow_started_at

    @flow_started_at.setter
    def flow_started_at(self, flow_started_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_started_at = flow_started_at

    @property
    def flow_finished_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.flow_finished_at

    @flow_finished_at.setter
    def flow_finished_at(self, flow_finished_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_finished_at = flow_finished_at

    @property
    def flow_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_status

    @flow_status.setter
    def flow_status(self, flow_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_status = flow_status

    @property
    def flow_schedule(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_schedule

    @flow_schedule.setter
    def flow_schedule(self, flow_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_schedule = flow_schedule

    @property
    def flow_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_project_name

    @flow_project_name.setter
    def flow_project_name(self, flow_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_project_name = flow_project_name

    @property
    def flow_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.flow_project_qualified_name
        )

    @flow_project_qualified_name.setter
    def flow_project_qualified_name(self, flow_project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_project_qualified_name = flow_project_qualified_name

    @property
    def flow_folder_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_folder_name

    @flow_folder_name.setter
    def flow_folder_name(self, flow_folder_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_folder_name = flow_folder_name

    @property
    def flow_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.flow_folder_qualified_name
        )

    @flow_folder_qualified_name.setter
    def flow_folder_qualified_name(self, flow_folder_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_folder_qualified_name = flow_folder_qualified_name

    @property
    def flow_reusable_unit_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.flow_reusable_unit_name
        )

    @flow_reusable_unit_name.setter
    def flow_reusable_unit_name(self, flow_reusable_unit_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_reusable_unit_name = flow_reusable_unit_name

    @property
    def flow_reusable_unit_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.flow_reusable_unit_qualified_name
        )

    @flow_reusable_unit_qualified_name.setter
    def flow_reusable_unit_qualified_name(
        self, flow_reusable_unit_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_reusable_unit_qualified_name = (
            flow_reusable_unit_qualified_name
        )

    @property
    def flow_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_id

    @flow_id.setter
    def flow_id(self, flow_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_id = flow_id

    @property
    def flow_run_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_run_id

    @flow_run_id.setter
    def flow_run_id(self, flow_run_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_run_id = flow_run_id

    @property
    def flow_error_message(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.flow_error_message

    @flow_error_message.setter
    def flow_error_message(self, flow_error_message: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_error_message = flow_error_message

    @property
    def flow_input_parameters(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.flow_input_parameters
        )

    @flow_input_parameters.setter
    def flow_input_parameters(self, flow_input_parameters: Optional[Dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_input_parameters = flow_input_parameters

    @property
    def flow_dataset(self) -> Optional[FlowDataset]:
        return None if self.attributes is None else self.attributes.flow_dataset

    @flow_dataset.setter
    def flow_dataset(self, flow_dataset: Optional[FlowDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_dataset = flow_dataset

    class Attributes(Catalog.Attributes):
        flow_dataset_name: Optional[str] = Field(default=None, description="")
        flow_dataset_qualified_name: Optional[str] = Field(default=None, description="")
        flow_data_type: Optional[str] = Field(default=None, description="")
        flow_expression: Optional[str] = Field(default=None, description="")
        flow_started_at: Optional[datetime] = Field(default=None, description="")
        flow_finished_at: Optional[datetime] = Field(default=None, description="")
        flow_status: Optional[str] = Field(default=None, description="")
        flow_schedule: Optional[str] = Field(default=None, description="")
        flow_project_name: Optional[str] = Field(default=None, description="")
        flow_project_qualified_name: Optional[str] = Field(default=None, description="")
        flow_folder_name: Optional[str] = Field(default=None, description="")
        flow_folder_qualified_name: Optional[str] = Field(default=None, description="")
        flow_reusable_unit_name: Optional[str] = Field(default=None, description="")
        flow_reusable_unit_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        flow_id: Optional[str] = Field(default=None, description="")
        flow_run_id: Optional[str] = Field(default=None, description="")
        flow_error_message: Optional[str] = Field(default=None, description="")
        flow_input_parameters: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        flow_dataset: Optional[FlowDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: FlowField.Attributes = Field(
        default_factory=lambda: FlowField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .flow_dataset import FlowDataset  # noqa: E402, F401
