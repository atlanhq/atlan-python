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

from .s_a_p import SAP


class SapDatasphereReplicationFlow(SAP):
    """Description"""

    type_name: str = Field(default="SapDatasphereReplicationFlow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapDatasphereReplicationFlow":
            raise ValueError("must be SapDatasphereReplicationFlow")
        return v

    def __setattr__(self, name, value):
        if name in SapDatasphereReplicationFlow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_DATASPHERE_REPLICATION_FLOW_SPACE_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "sapDatasphereReplicationFlowSpaceName",
            "sapDatasphereReplicationFlowSpaceName.keyword",
            "sapDatasphereReplicationFlowSpaceName",
        )
    )
    """
    Simple name of the Datasphere space in which this replication flow runs and creates its target tables.
    """
    SAP_DATASPHERE_REPLICATION_FLOW_SPACE_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "sapDatasphereReplicationFlowSpaceQualifiedName",
            "sapDatasphereReplicationFlowSpaceQualifiedName",
        )
    )
    """
    Unique name of the Datasphere space in which this replication flow runs and creates its target tables.
    """
    SAP_DATASPHERE_REPLICATION_FLOW_SOURCE_CONNECTION: ClassVar[KeywordField] = (
        KeywordField(
            "sapDatasphereReplicationFlowSourceConnection",
            "sapDatasphereReplicationFlowSourceConnection",
        )
    )
    """
    Name of the source connection from which this replication flow reads data, such as an S/4HANA, SAP ECC, SAP BW, or S3 connection outside Datasphere.
    """  # noqa: E501
    SAP_DATASPHERE_REPLICATION_FLOW_TARGET_CONNECTION: ClassVar[KeywordField] = (
        KeywordField(
            "sapDatasphereReplicationFlowTargetConnection",
            "sapDatasphereReplicationFlowTargetConnection",
        )
    )
    """
    Name of the target connection into which this replication flow writes data, such as the local Datasphere repository.
    """
    SAP_DATASPHERE_REPLICATION_FLOW_LOAD_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapDatasphereReplicationFlowLoadType", "sapDatasphereReplicationFlowLoadType"
    )
    """
    Type of load performed by this replication flow, such as INITIAL or INITIAL_AND_DELTA.
    """
    SAP_DATASPHERE_REPLICATION_FLOW_DATASET_COUNT: ClassVar[NumericField] = (
        NumericField(
            "sapDatasphereReplicationFlowDatasetCount",
            "sapDatasphereReplicationFlowDatasetCount",
        )
    )
    """
    Number of datasets moved by this replication flow.
    """
    SAP_TECHNICAL_NAME: ClassVar[KeywordField] = KeywordField(
        "sapTechnicalName", "sapTechnicalName"
    )
    """
    Technical identifier for SAP data objects, used for integration and internal reference.
    """
    SAP_LOGICAL_NAME: ClassVar[KeywordField] = KeywordField(
        "sapLogicalName", "sapLogicalName"
    )
    """
    Logical, business-friendly identifier for SAP data objects, aligned with business terminology and concepts.
    """
    SAP_PACKAGE_NAME: ClassVar[KeywordField] = KeywordField(
        "sapPackageName", "sapPackageName"
    )
    """
    Name of the SAP package, representing a logical grouping of related SAP data objects.
    """
    SAP_COMPONENT_NAME: ClassVar[KeywordField] = KeywordField(
        "sapComponentName", "sapComponentName"
    )
    """
    Name of the SAP component, representing a specific functional area in SAP.
    """
    SAP_DATA_TYPE: ClassVar[KeywordField] = KeywordField("sapDataType", "sapDataType")
    """
    SAP-specific data types.
    """
    SAP_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "sapFieldCount", "sapFieldCount"
    )
    """
    Represents the total number of fields, columns, or child assets present in a given SAP asset.
    """
    SAP_FIELD_ORDER: ClassVar[NumericField] = NumericField(
        "sapFieldOrder", "sapFieldOrder"
    )
    """
    Indicates the sequential position of a field, column, or child asset within its parent SAP asset, starting from 1.
    """
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
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

    SAP_DATASPHERE_SCHEMA: ClassVar[RelationField] = RelationField(
        "sapDatasphereSchema"
    )
    """
    TBC
    """
    FLOW_SUCCESSORS: ClassVar[RelationField] = RelationField("flowSuccessors")
    """
    TBC
    """
    FLOW_PREDECESSORS: ClassVar[RelationField] = RelationField("flowPredecessors")
    """
    TBC
    """
    FLOW_CONTROLLED_BY: ClassVar[RelationField] = RelationField("flowControlledBy")
    """
    TBC
    """
    FLOW_CONTROLLED_OPERATIONS: ClassVar[RelationField] = RelationField(
        "flowControlledOperations"
    )
    """
    TBC
    """
    FLOW_DATA_RESULTS: ClassVar[RelationField] = RelationField("flowDataResults")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_datasphere_replication_flow_space_name",
        "sap_datasphere_replication_flow_space_qualified_name",
        "sap_datasphere_replication_flow_source_connection",
        "sap_datasphere_replication_flow_target_connection",
        "sap_datasphere_replication_flow_load_type",
        "sap_datasphere_replication_flow_dataset_count",
        "sap_technical_name",
        "sap_logical_name",
        "sap_package_name",
        "sap_component_name",
        "sap_data_type",
        "sap_field_count",
        "sap_field_order",
        "catalog_dataset_guid",
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
        "sap_datasphere_schema",
        "flow_successors",
        "flow_predecessors",
        "flow_controlled_by",
        "flow_controlled_operations",
        "flow_data_results",
    ]

    @property
    def sap_datasphere_replication_flow_space_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_datasphere_replication_flow_space_name
        )

    @sap_datasphere_replication_flow_space_name.setter
    def sap_datasphere_replication_flow_space_name(
        self, sap_datasphere_replication_flow_space_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_datasphere_replication_flow_space_name = (
            sap_datasphere_replication_flow_space_name
        )

    @property
    def sap_datasphere_replication_flow_space_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_datasphere_replication_flow_space_qualified_name
        )

    @sap_datasphere_replication_flow_space_qualified_name.setter
    def sap_datasphere_replication_flow_space_qualified_name(
        self, sap_datasphere_replication_flow_space_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_datasphere_replication_flow_space_qualified_name = (
            sap_datasphere_replication_flow_space_qualified_name
        )

    @property
    def sap_datasphere_replication_flow_source_connection(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_datasphere_replication_flow_source_connection
        )

    @sap_datasphere_replication_flow_source_connection.setter
    def sap_datasphere_replication_flow_source_connection(
        self, sap_datasphere_replication_flow_source_connection: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_datasphere_replication_flow_source_connection = (
            sap_datasphere_replication_flow_source_connection
        )

    @property
    def sap_datasphere_replication_flow_target_connection(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_datasphere_replication_flow_target_connection
        )

    @sap_datasphere_replication_flow_target_connection.setter
    def sap_datasphere_replication_flow_target_connection(
        self, sap_datasphere_replication_flow_target_connection: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_datasphere_replication_flow_target_connection = (
            sap_datasphere_replication_flow_target_connection
        )

    @property
    def sap_datasphere_replication_flow_load_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_datasphere_replication_flow_load_type
        )

    @sap_datasphere_replication_flow_load_type.setter
    def sap_datasphere_replication_flow_load_type(
        self, sap_datasphere_replication_flow_load_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_datasphere_replication_flow_load_type = (
            sap_datasphere_replication_flow_load_type
        )

    @property
    def sap_datasphere_replication_flow_dataset_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_datasphere_replication_flow_dataset_count
        )

    @sap_datasphere_replication_flow_dataset_count.setter
    def sap_datasphere_replication_flow_dataset_count(
        self, sap_datasphere_replication_flow_dataset_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_datasphere_replication_flow_dataset_count = (
            sap_datasphere_replication_flow_dataset_count
        )

    @property
    def sap_technical_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_technical_name

    @sap_technical_name.setter
    def sap_technical_name(self, sap_technical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_technical_name = sap_technical_name

    @property
    def sap_logical_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_logical_name

    @sap_logical_name.setter
    def sap_logical_name(self, sap_logical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_logical_name = sap_logical_name

    @property
    def sap_package_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_package_name

    @sap_package_name.setter
    def sap_package_name(self, sap_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_package_name = sap_package_name

    @property
    def sap_component_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_component_name

    @sap_component_name.setter
    def sap_component_name(self, sap_component_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_component_name = sap_component_name

    @property
    def sap_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_data_type

    @sap_data_type.setter
    def sap_data_type(self, sap_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_data_type = sap_data_type

    @property
    def sap_field_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.sap_field_count

    @sap_field_count.setter
    def sap_field_count(self, sap_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_field_count = sap_field_count

    @property
    def sap_field_order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.sap_field_order

    @sap_field_order.setter
    def sap_field_order(self, sap_field_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_field_order = sap_field_order

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

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
    def sap_datasphere_schema(self) -> Optional[Schema]:
        return (
            None if self.attributes is None else self.attributes.sap_datasphere_schema
        )

    @sap_datasphere_schema.setter
    def sap_datasphere_schema(self, sap_datasphere_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_datasphere_schema = sap_datasphere_schema

    @property
    def flow_successors(self) -> Optional[List[FlowControlOperation]]:
        return None if self.attributes is None else self.attributes.flow_successors

    @flow_successors.setter
    def flow_successors(self, flow_successors: Optional[List[FlowControlOperation]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_successors = flow_successors

    @property
    def flow_predecessors(self) -> Optional[List[FlowControlOperation]]:
        return None if self.attributes is None else self.attributes.flow_predecessors

    @flow_predecessors.setter
    def flow_predecessors(
        self, flow_predecessors: Optional[List[FlowControlOperation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_predecessors = flow_predecessors

    @property
    def flow_controlled_by(self) -> Optional[FlowControlOperation]:
        return None if self.attributes is None else self.attributes.flow_controlled_by

    @flow_controlled_by.setter
    def flow_controlled_by(self, flow_controlled_by: Optional[FlowControlOperation]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_controlled_by = flow_controlled_by

    @property
    def flow_controlled_operations(self) -> Optional[List[FlowControlOperation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.flow_controlled_operations
        )

    @flow_controlled_operations.setter
    def flow_controlled_operations(
        self, flow_controlled_operations: Optional[List[FlowControlOperation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_controlled_operations = flow_controlled_operations

    @property
    def flow_data_results(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.flow_data_results

    @flow_data_results.setter
    def flow_data_results(self, flow_data_results: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_data_results = flow_data_results

    class Attributes(SAP.Attributes):
        sap_datasphere_replication_flow_space_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_datasphere_replication_flow_space_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_datasphere_replication_flow_source_connection: Optional[str] = Field(
            default=None, description=""
        )
        sap_datasphere_replication_flow_target_connection: Optional[str] = Field(
            default=None, description=""
        )
        sap_datasphere_replication_flow_load_type: Optional[str] = Field(
            default=None, description=""
        )
        sap_datasphere_replication_flow_dataset_count: Optional[int] = Field(
            default=None, description=""
        )
        sap_technical_name: Optional[str] = Field(default=None, description="")
        sap_logical_name: Optional[str] = Field(default=None, description="")
        sap_package_name: Optional[str] = Field(default=None, description="")
        sap_component_name: Optional[str] = Field(default=None, description="")
        sap_data_type: Optional[str] = Field(default=None, description="")
        sap_field_count: Optional[int] = Field(default=None, description="")
        sap_field_order: Optional[int] = Field(default=None, description="")
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
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
        sap_datasphere_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        flow_successors: Optional[List[FlowControlOperation]] = Field(
            default=None, description=""
        )  # relationship
        flow_predecessors: Optional[List[FlowControlOperation]] = Field(
            default=None, description=""
        )  # relationship
        flow_controlled_by: Optional[FlowControlOperation] = Field(
            default=None, description=""
        )  # relationship
        flow_controlled_operations: Optional[List[FlowControlOperation]] = Field(
            default=None, description=""
        )  # relationship
        flow_data_results: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapDatasphereReplicationFlow.Attributes = Field(
        default_factory=lambda: SapDatasphereReplicationFlow.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .flow_control_operation import FlowControlOperation  # noqa: E402, F401
from .process import Process  # noqa: E402, F401
from .schema import Schema  # noqa: E402, F401
