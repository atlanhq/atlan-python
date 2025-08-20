# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIDatasetType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    TextField,
)

from .column_process import ColumnProcess


class FlowFieldOperation(ColumnProcess):
    """Description"""

    type_name: str = Field(default="FlowFieldOperation", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FlowFieldOperation":
            raise ValueError("must be FlowFieldOperation")
        return v

    def __setattr__(self, name, value):
        if name in FlowFieldOperation._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CODE: ClassVar[TextField] = TextField("code", "code")
    """
    Code that ran within the process.
    """
    SQL: ClassVar[TextField] = TextField("sql", "sql")
    """
    SQL query that ran to produce the outputs.
    """
    PARENT_CONNECTION_PROCESS_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "parentConnectionProcessQualifiedName", "parentConnectionProcessQualifiedName"
    )
    """

    """
    AST: ClassVar[TextField] = TextField("ast", "ast")
    """
    Parsed AST of the code or SQL statements that describe the logic of this process.
    """
    ADDITIONAL_ETL_CONTEXT: ClassVar[TextField] = TextField(
        "additionalEtlContext", "additionalEtlContext"
    )
    """
    Additional Context of the ETL pipeline/notebook which creates the process.
    """
    AI_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "aiDatasetType", "aiDatasetType"
    )
    """
    Dataset type for AI Model - dataset process.
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

    _convenience_properties: ClassVar[List[str]] = [
        "inputs",
        "outputs",
        "code",
        "sql",
        "parent_connection_process_qualified_name",
        "ast",
        "additional_etl_context",
        "ai_dataset_type",
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
    ]

    @property
    def inputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def code(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.code

    @code.setter
    def code(self, code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.code = code

    @property
    def sql(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql

    @sql.setter
    def sql(self, sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql = sql

    @property
    def parent_connection_process_qualified_name(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.parent_connection_process_qualified_name
        )

    @parent_connection_process_qualified_name.setter
    def parent_connection_process_qualified_name(
        self, parent_connection_process_qualified_name: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_connection_process_qualified_name = (
            parent_connection_process_qualified_name
        )

    @property
    def ast(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ast

    @ast.setter
    def ast(self, ast: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ast = ast

    @property
    def additional_etl_context(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.additional_etl_context
        )

    @additional_etl_context.setter
    def additional_etl_context(self, additional_etl_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_etl_context = additional_etl_context

    @property
    def ai_dataset_type(self) -> Optional[AIDatasetType]:
        return None if self.attributes is None else self.attributes.ai_dataset_type

    @ai_dataset_type.setter
    def ai_dataset_type(self, ai_dataset_type: Optional[AIDatasetType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_dataset_type = ai_dataset_type

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

    class Attributes(ColumnProcess.Attributes):
        inputs: Optional[List[Catalog]] = Field(default=None, description="")
        outputs: Optional[List[Catalog]] = Field(default=None, description="")
        code: Optional[str] = Field(default=None, description="")
        sql: Optional[str] = Field(default=None, description="")
        parent_connection_process_qualified_name: Optional[Set[str]] = Field(
            default=None, description=""
        )
        ast: Optional[str] = Field(default=None, description="")
        additional_etl_context: Optional[str] = Field(default=None, description="")
        ai_dataset_type: Optional[AIDatasetType] = Field(default=None, description="")
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

    attributes: FlowFieldOperation.Attributes = Field(
        default_factory=lambda: FlowFieldOperation.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa: E402, F401
