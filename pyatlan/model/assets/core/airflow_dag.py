# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .airflow import Airflow


class AirflowDag(Airflow):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> AirflowDag:
        validate_required_fields(
            ["name", "connection_qualified_name"],
            [name, connection_qualified_name],
        )
        attributes = AirflowDag.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="AirflowDag", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AirflowDag":
            raise ValueError("must be AirflowDag")
        return v

    def __setattr__(self, name, value):
        if name in AirflowDag._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AIRFLOW_DAG_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "airflowDagSchedule", "airflowDagSchedule"
    )
    """
    Schedule for the DAG.
    """
    AIRFLOW_DAG_SCHEDULE_DELTA: ClassVar[NumericField] = NumericField(
        "airflowDagScheduleDelta", "airflowDagScheduleDelta"
    )
    """
    Duration between scheduled runs, in seconds.
    """

    AIRFLOW_TASKS: ClassVar[RelationField] = RelationField("airflowTasks")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "airflow_dag_schedule",
        "airflow_dag_schedule_delta",
        "airflow_tasks",
    ]

    @property
    def airflow_dag_schedule(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_dag_schedule

    @airflow_dag_schedule.setter
    def airflow_dag_schedule(self, airflow_dag_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_schedule = airflow_dag_schedule

    @property
    def airflow_dag_schedule_delta(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_dag_schedule_delta
        )

    @airflow_dag_schedule_delta.setter
    def airflow_dag_schedule_delta(self, airflow_dag_schedule_delta: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_schedule_delta = airflow_dag_schedule_delta

    @property
    def airflow_tasks(self) -> Optional[List[AirflowTask]]:
        return None if self.attributes is None else self.attributes.airflow_tasks

    @airflow_tasks.setter
    def airflow_tasks(self, airflow_tasks: Optional[List[AirflowTask]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_tasks = airflow_tasks

    class Attributes(Airflow.Attributes):
        airflow_dag_schedule: Optional[str] = Field(default=None, description="")
        airflow_dag_schedule_delta: Optional[int] = Field(default=None, description="")
        airflow_tasks: Optional[List[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
        ) -> AirflowDag.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return AirflowDag.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: AirflowDag.Attributes = Field(
        default_factory=lambda: AirflowDag.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .airflow_task import AirflowTask  # noqa
