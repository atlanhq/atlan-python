# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .flow import Flow


class FlowReusableUnit(Flow):
    """Description"""

    type_name: str = Field(default="FlowReusableUnit", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FlowReusableUnit":
            raise ValueError("must be FlowReusableUnit")
        return v

    def __setattr__(self, name, value):
        if name in FlowReusableUnit._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FLOW_DATASET_COUNT: ClassVar[NumericField] = NumericField(
        "flowDatasetCount", "flowDatasetCount"
    )
    """
    Count of the number of ephemeral datasets contained within this reusable unit.
    """
    FLOW_CONTROL_OPERATION_COUNT: ClassVar[NumericField] = NumericField(
        "flowControlOperationCount", "flowControlOperationCount"
    )
    """
    Count of the number of control flow operations that execute this reusable unit.
    """

    FLOW_DATA_FLOWS: ClassVar[RelationField] = RelationField("flowDataFlows")
    """
    TBC
    """
    FLOW_ABSTRACTS: ClassVar[RelationField] = RelationField("flowAbstracts")
    """
    TBC
    """
    FLOW_DATASETS: ClassVar[RelationField] = RelationField("flowDatasets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "flow_dataset_count",
        "flow_control_operation_count",
        "flow_data_flows",
        "flow_abstracts",
        "flow_datasets",
    ]

    @property
    def flow_dataset_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.flow_dataset_count

    @flow_dataset_count.setter
    def flow_dataset_count(self, flow_dataset_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_dataset_count = flow_dataset_count

    @property
    def flow_control_operation_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.flow_control_operation_count
        )

    @flow_control_operation_count.setter
    def flow_control_operation_count(self, flow_control_operation_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_control_operation_count = flow_control_operation_count

    @property
    def flow_data_flows(self) -> Optional[List[FlowDatasetOperation]]:
        return None if self.attributes is None else self.attributes.flow_data_flows

    @flow_data_flows.setter
    def flow_data_flows(self, flow_data_flows: Optional[List[FlowDatasetOperation]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_data_flows = flow_data_flows

    @property
    def flow_abstracts(self) -> Optional[List[FlowDataset]]:
        return None if self.attributes is None else self.attributes.flow_abstracts

    @flow_abstracts.setter
    def flow_abstracts(self, flow_abstracts: Optional[List[FlowDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_abstracts = flow_abstracts

    @property
    def flow_datasets(self) -> Optional[List[FlowDataset]]:
        return None if self.attributes is None else self.attributes.flow_datasets

    @flow_datasets.setter
    def flow_datasets(self, flow_datasets: Optional[List[FlowDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_datasets = flow_datasets

    class Attributes(Flow.Attributes):
        flow_dataset_count: Optional[int] = Field(default=None, description="")
        flow_control_operation_count: Optional[int] = Field(
            default=None, description=""
        )
        flow_data_flows: Optional[List[FlowDatasetOperation]] = Field(
            default=None, description=""
        )  # relationship
        flow_abstracts: Optional[List[FlowDataset]] = Field(
            default=None, description=""
        )  # relationship
        flow_datasets: Optional[List[FlowDataset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: FlowReusableUnit.Attributes = Field(
        default_factory=lambda: FlowReusableUnit.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .flow_dataset import FlowDataset  # noqa: E402, F401
from .flow_dataset_operation import FlowDatasetOperation  # noqa: E402, F401
