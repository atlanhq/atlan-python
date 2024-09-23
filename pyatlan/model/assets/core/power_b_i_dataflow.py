# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .power_b_i import PowerBI


class PowerBIDataflow(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIDataflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataflow":
            raise ValueError("must be PowerBIDataflow")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this dataflow exists.
    """
    WEB_URL: ClassVar[TextField] = TextField("webUrl", "webUrl")
    """
    Deprecated. See 'sourceUrl' instead.
    """
    POWER_BI_DATAFLOW_REFRESH_SCHEDULE_FREQUENCY: ClassVar[KeywordField] = KeywordField(
        "powerBIDataflowRefreshScheduleFrequency",
        "powerBIDataflowRefreshScheduleFrequency",
    )
    """
    Refresh Schedule frequency for a PowerBI Dataflow.
    """
    POWER_BI_DATAFLOW_REFRESH_SCHEDULE_TIMES: ClassVar[KeywordField] = KeywordField(
        "powerBIDataflowRefreshScheduleTimes", "powerBIDataflowRefreshScheduleTimes"
    )
    """
    Time for the refresh schedule set for a PowerBI Dataflow.
    """
    POWER_BI_DATAFLOW_REFRESH_SCHEDULE_TIME_ZONE: ClassVar[KeywordField] = KeywordField(
        "powerBIDataflowRefreshScheduleTimeZone",
        "powerBIDataflowRefreshScheduleTimeZone",
    )
    """
    Time zone for the refresh schedule set for a PowerBI Dataflow.
    """

    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    POWER_BI_PROCESSES: ClassVar[RelationField] = RelationField("powerBIProcesses")
    """
    TBC
    """
    DATASETS: ClassVar[RelationField] = RelationField("datasets")
    """
    TBC
    """
    TABLES: ClassVar[RelationField] = RelationField("tables")
    """
    TBC
    """
    POWER_BI_DATAFLOW_CHILDREN: ClassVar[RelationField] = RelationField(
        "powerBIDataflowChildren"
    )
    """
    TBC
    """
    POWER_BI_DATAFLOW_PARENTS: ClassVar[RelationField] = RelationField(
        "powerBIDataflowParents"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "web_url",
        "power_b_i_dataflow_refresh_schedule_frequency",
        "power_b_i_dataflow_refresh_schedule_times",
        "power_b_i_dataflow_refresh_schedule_time_zone",
        "workspace",
        "power_b_i_processes",
        "datasets",
        "tables",
        "power_b_i_dataflow_children",
        "power_b_i_dataflow_parents",
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
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def power_b_i_dataflow_refresh_schedule_frequency(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_refresh_schedule_frequency
        )

    @power_b_i_dataflow_refresh_schedule_frequency.setter
    def power_b_i_dataflow_refresh_schedule_frequency(
        self, power_b_i_dataflow_refresh_schedule_frequency: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_refresh_schedule_frequency = (
            power_b_i_dataflow_refresh_schedule_frequency
        )

    @property
    def power_b_i_dataflow_refresh_schedule_times(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_refresh_schedule_times
        )

    @power_b_i_dataflow_refresh_schedule_times.setter
    def power_b_i_dataflow_refresh_schedule_times(
        self, power_b_i_dataflow_refresh_schedule_times: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_refresh_schedule_times = (
            power_b_i_dataflow_refresh_schedule_times
        )

    @property
    def power_b_i_dataflow_refresh_schedule_time_zone(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_refresh_schedule_time_zone
        )

    @power_b_i_dataflow_refresh_schedule_time_zone.setter
    def power_b_i_dataflow_refresh_schedule_time_zone(
        self, power_b_i_dataflow_refresh_schedule_time_zone: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_refresh_schedule_time_zone = (
            power_b_i_dataflow_refresh_schedule_time_zone
        )

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def power_b_i_processes(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.power_b_i_processes

    @power_b_i_processes.setter
    def power_b_i_processes(self, power_b_i_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_processes = power_b_i_processes

    @property
    def datasets(self) -> Optional[List[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[List[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    @property
    def tables(self) -> Optional[List[PowerBITable]]:
        return None if self.attributes is None else self.attributes.tables

    @tables.setter
    def tables(self, tables: Optional[List[PowerBITable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tables = tables

    @property
    def power_b_i_dataflow_children(self) -> Optional[List[PowerBIDataflow]]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_children
        )

    @power_b_i_dataflow_children.setter
    def power_b_i_dataflow_children(
        self, power_b_i_dataflow_children: Optional[List[PowerBIDataflow]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_children = power_b_i_dataflow_children

    @property
    def power_b_i_dataflow_parents(self) -> Optional[List[PowerBIDataflow]]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_dataflow_parents
        )

    @power_b_i_dataflow_parents.setter
    def power_b_i_dataflow_parents(
        self, power_b_i_dataflow_parents: Optional[List[PowerBIDataflow]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow_parents = power_b_i_dataflow_parents

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        web_url: Optional[str] = Field(default=None, description="")
        power_b_i_dataflow_refresh_schedule_frequency: Optional[str] = Field(
            default=None, description=""
        )
        power_b_i_dataflow_refresh_schedule_times: Optional[Set[str]] = Field(
            default=None, description=""
        )
        power_b_i_dataflow_refresh_schedule_time_zone: Optional[str] = Field(
            default=None, description=""
        )
        workspace: Optional[PowerBIWorkspace] = Field(
            default=None, description=""
        )  # relationship
        power_b_i_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship
        datasets: Optional[List[PowerBIDataset]] = Field(
            default=None, description=""
        )  # relationship
        tables: Optional[List[PowerBITable]] = Field(
            default=None, description=""
        )  # relationship
        power_b_i_dataflow_children: Optional[List[PowerBIDataflow]] = Field(
            default=None, description=""
        )  # relationship
        power_b_i_dataflow_parents: Optional[List[PowerBIDataflow]] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIDataflow.Attributes = Field(
        default_factory=lambda: PowerBIDataflow.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_dataset import PowerBIDataset  # noqa
from .power_b_i_table import PowerBITable  # noqa
from .power_b_i_workspace import PowerBIWorkspace  # noqa
from .process import Process  # noqa
