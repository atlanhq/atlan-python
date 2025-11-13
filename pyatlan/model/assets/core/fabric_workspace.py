# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .fabric import Fabric


class FabricWorkspace(Fabric):
    """Description"""

    type_name: str = Field(default="FabricWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricWorkspace":
            raise ValueError("must be FabricWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in FabricWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_DATA_PIPELINES: ClassVar[RelationField] = RelationField(
        "fabricDataPipelines"
    )
    """
    TBC
    """
    FABRIC_SEMANTIC_MODELS: ClassVar[RelationField] = RelationField(
        "fabricSemanticModels"
    )
    """
    TBC
    """
    FABRIC_DASHBOARDS: ClassVar[RelationField] = RelationField("fabricDashboards")
    """
    TBC
    """
    FABRIC_DATAFLOWS: ClassVar[RelationField] = RelationField("fabricDataflows")
    """
    TBC
    """
    FABRIC_DATABASES: ClassVar[RelationField] = RelationField("fabricDatabases")
    """
    TBC
    """
    FABRIC_REPORTS: ClassVar[RelationField] = RelationField("fabricReports")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_data_pipelines",
        "fabric_semantic_models",
        "fabric_dashboards",
        "fabric_dataflows",
        "fabric_databases",
        "fabric_reports",
    ]

    @property
    def fabric_data_pipelines(self) -> Optional[List[FabricDataPipeline]]:
        return (
            None if self.attributes is None else self.attributes.fabric_data_pipelines
        )

    @fabric_data_pipelines.setter
    def fabric_data_pipelines(
        self, fabric_data_pipelines: Optional[List[FabricDataPipeline]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_data_pipelines = fabric_data_pipelines

    @property
    def fabric_semantic_models(self) -> Optional[List[FabricSemanticModel]]:
        return (
            None if self.attributes is None else self.attributes.fabric_semantic_models
        )

    @fabric_semantic_models.setter
    def fabric_semantic_models(
        self, fabric_semantic_models: Optional[List[FabricSemanticModel]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_semantic_models = fabric_semantic_models

    @property
    def fabric_dashboards(self) -> Optional[List[FabricDashboard]]:
        return None if self.attributes is None else self.attributes.fabric_dashboards

    @fabric_dashboards.setter
    def fabric_dashboards(self, fabric_dashboards: Optional[List[FabricDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_dashboards = fabric_dashboards

    @property
    def fabric_dataflows(self) -> Optional[List[FabricDataflow]]:
        return None if self.attributes is None else self.attributes.fabric_dataflows

    @fabric_dataflows.setter
    def fabric_dataflows(self, fabric_dataflows: Optional[List[FabricDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_dataflows = fabric_dataflows

    @property
    def fabric_databases(self) -> Optional[List[Database]]:
        return None if self.attributes is None else self.attributes.fabric_databases

    @fabric_databases.setter
    def fabric_databases(self, fabric_databases: Optional[List[Database]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_databases = fabric_databases

    @property
    def fabric_reports(self) -> Optional[List[FabricReport]]:
        return None if self.attributes is None else self.attributes.fabric_reports

    @fabric_reports.setter
    def fabric_reports(self, fabric_reports: Optional[List[FabricReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_reports = fabric_reports

    class Attributes(Fabric.Attributes):
        fabric_data_pipelines: Optional[List[FabricDataPipeline]] = Field(
            default=None, description=""
        )  # relationship
        fabric_semantic_models: Optional[List[FabricSemanticModel]] = Field(
            default=None, description=""
        )  # relationship
        fabric_dashboards: Optional[List[FabricDashboard]] = Field(
            default=None, description=""
        )  # relationship
        fabric_dataflows: Optional[List[FabricDataflow]] = Field(
            default=None, description=""
        )  # relationship
        fabric_databases: Optional[List[Database]] = Field(
            default=None, description=""
        )  # relationship
        fabric_reports: Optional[List[FabricReport]] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricWorkspace.Attributes = Field(
        default_factory=lambda: FabricWorkspace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .database import Database  # noqa: E402, F401
from .fabric_dashboard import FabricDashboard  # noqa: E402, F401
from .fabric_data_pipeline import FabricDataPipeline  # noqa: E402, F401
from .fabric_dataflow import FabricDataflow  # noqa: E402, F401
from .fabric_report import FabricReport  # noqa: E402, F401
from .fabric_semantic_model import FabricSemanticModel  # noqa: E402, F401
