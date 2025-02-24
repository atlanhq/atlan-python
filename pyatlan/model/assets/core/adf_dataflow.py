# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField, TextField

from .a_d_f import ADF


class AdfDataflow(ADF):
    """Description"""

    type_name: str = Field(default="AdfDataflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AdfDataflow":
            raise ValueError("must be AdfDataflow")
        return v

    def __setattr__(self, name, value):
        if name in AdfDataflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADF_DATAFLOW_SOURCES: ClassVar[TextField] = TextField(
        "adfDataflowSources", "adfDataflowSources"
    )
    """
    The list of names of sources for this dataflow.
    """
    ADF_DATAFLOW_SINKS: ClassVar[TextField] = TextField(
        "adfDataflowSinks", "adfDataflowSinks"
    )
    """
    The list of names of sinks for this dataflow.
    """
    ADF_DATAFLOW_SCRIPT: ClassVar[TextField] = TextField(
        "adfDataflowScript", "adfDataflowScript"
    )
    """
    The gererated script for the dataflow.
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
    ADF_PIPELINES: ClassVar[RelationField] = RelationField("adfPipelines")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adf_dataflow_sources",
        "adf_dataflow_sinks",
        "adf_dataflow_script",
        "adf_linkedservices",
        "adf_datasets",
        "adf_activities",
        "adf_pipelines",
    ]

    @property
    def adf_dataflow_sources(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.adf_dataflow_sources

    @adf_dataflow_sources.setter
    def adf_dataflow_sources(self, adf_dataflow_sources: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataflow_sources = adf_dataflow_sources

    @property
    def adf_dataflow_sinks(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.adf_dataflow_sinks

    @adf_dataflow_sinks.setter
    def adf_dataflow_sinks(self, adf_dataflow_sinks: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataflow_sinks = adf_dataflow_sinks

    @property
    def adf_dataflow_script(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adf_dataflow_script

    @adf_dataflow_script.setter
    def adf_dataflow_script(self, adf_dataflow_script: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataflow_script = adf_dataflow_script

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
    def adf_pipelines(self) -> Optional[List[AdfPipeline]]:
        return None if self.attributes is None else self.attributes.adf_pipelines

    @adf_pipelines.setter
    def adf_pipelines(self, adf_pipelines: Optional[List[AdfPipeline]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipelines = adf_pipelines

    class Attributes(ADF.Attributes):
        adf_dataflow_sources: Optional[Set[str]] = Field(default=None, description="")
        adf_dataflow_sinks: Optional[Set[str]] = Field(default=None, description="")
        adf_dataflow_script: Optional[str] = Field(default=None, description="")
        adf_linkedservices: Optional[List[AdfLinkedservice]] = Field(
            default=None, description=""
        )  # relationship
        adf_datasets: Optional[List[AdfDataset]] = Field(
            default=None, description=""
        )  # relationship
        adf_activities: Optional[List[AdfActivity]] = Field(
            default=None, description=""
        )  # relationship
        adf_pipelines: Optional[List[AdfPipeline]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AdfDataflow.Attributes = Field(
        default_factory=lambda: AdfDataflow.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .adf_activity import AdfActivity  # noqa
from .adf_dataset import AdfDataset  # noqa
from .adf_linkedservice import AdfLinkedservice  # noqa
from .adf_pipeline import AdfPipeline  # noqa
