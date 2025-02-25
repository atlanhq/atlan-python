# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .a_d_f import ADF


class AdfPipeline(ADF):
    """Description"""

    type_name: str = Field(default="AdfPipeline", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AdfPipeline":
            raise ValueError("must be AdfPipeline")
        return v

    def __setattr__(self, name, value):
        if name in AdfPipeline._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADF_PIPELINE_ACTIVITY_COUNT: ClassVar[NumericField] = NumericField(
        "adfPipelineActivityCount", "adfPipelineActivityCount"
    )
    """
    Defines the count of activities in the pipline.
    """
    ADF_PIPELINE_RUNS: ClassVar[KeywordField] = KeywordField(
        "adfPipelineRuns", "adfPipelineRuns"
    )
    """
    List of objects of pipeline runs for a particular pipeline.
    """
    ADF_PIPELINE_ANNOTATIONS: ClassVar[TextField] = TextField(
        "adfPipelineAnnotations", "adfPipelineAnnotations"
    )
    """
    The list of annotation assigned to a pipeline.
    """

    ADF_LINKEDSERVICES: ClassVar[RelationField] = RelationField("adfLinkedservices")
    """
    TBC
    """
    ADF_DATASETS: ClassVar[RelationField] = RelationField("adfDatasets")
    """
    TBC
    """
    ADF_ACTIVITIES: ClassVar[RelationField] = RelationField("adfActivities")
    """
    TBC
    """
    ADF_DATAFLOWS: ClassVar[RelationField] = RelationField("adfDataflows")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adf_pipeline_activity_count",
        "adf_pipeline_runs",
        "adf_pipeline_annotations",
        "adf_linkedservices",
        "adf_datasets",
        "adf_activities",
        "adf_dataflows",
    ]

    @property
    def adf_pipeline_activity_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_pipeline_activity_count
        )

    @adf_pipeline_activity_count.setter
    def adf_pipeline_activity_count(self, adf_pipeline_activity_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipeline_activity_count = adf_pipeline_activity_count

    @property
    def adf_pipeline_runs(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.adf_pipeline_runs

    @adf_pipeline_runs.setter
    def adf_pipeline_runs(self, adf_pipeline_runs: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipeline_runs = adf_pipeline_runs

    @property
    def adf_pipeline_annotations(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_pipeline_annotations
        )

    @adf_pipeline_annotations.setter
    def adf_pipeline_annotations(self, adf_pipeline_annotations: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipeline_annotations = adf_pipeline_annotations

    @property
    def adf_linkedservices(self) -> Optional[List[AdfLinkedservice]]:
        return None if self.attributes is None else self.attributes.adf_linkedservices

    @adf_linkedservices.setter
    def adf_linkedservices(self, adf_linkedservices: Optional[List[AdfLinkedservice]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservices = adf_linkedservices

    @property
    def adf_datasets(self) -> Optional[List[AdfDataset]]:
        return None if self.attributes is None else self.attributes.adf_datasets

    @adf_datasets.setter
    def adf_datasets(self, adf_datasets: Optional[List[AdfDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_datasets = adf_datasets

    @property
    def adf_activities(self) -> Optional[List[AdfActivity]]:
        return None if self.attributes is None else self.attributes.adf_activities

    @adf_activities.setter
    def adf_activities(self, adf_activities: Optional[List[AdfActivity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activities = adf_activities

    @property
    def adf_dataflows(self) -> Optional[List[AdfDataflow]]:
        return None if self.attributes is None else self.attributes.adf_dataflows

    @adf_dataflows.setter
    def adf_dataflows(self, adf_dataflows: Optional[List[AdfDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataflows = adf_dataflows

    class Attributes(ADF.Attributes):
        adf_pipeline_activity_count: Optional[int] = Field(default=None, description="")
        adf_pipeline_runs: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        adf_pipeline_annotations: Optional[Set[str]] = Field(
            default=None, description=""
        )
        adf_linkedservices: Optional[List[AdfLinkedservice]] = Field(
            default=None, description=""
        )  # relationship
        adf_datasets: Optional[List[AdfDataset]] = Field(
            default=None, description=""
        )  # relationship
        adf_activities: Optional[List[AdfActivity]] = Field(
            default=None, description=""
        )  # relationship
        adf_dataflows: Optional[List[AdfDataflow]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AdfPipeline.Attributes = Field(
        default_factory=lambda: AdfPipeline.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .adf_activity import AdfActivity  # noqa: E402, F401
from .adf_dataflow import AdfDataflow  # noqa: E402, F401
from .adf_dataset import AdfDataset  # noqa: E402, F401
from .adf_linkedservice import AdfLinkedservice  # noqa: E402, F401
