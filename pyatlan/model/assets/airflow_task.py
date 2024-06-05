# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .airflow import Airflow


class AirflowTask(Airflow):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        airflow_dag_qualified_name: str,
    ) -> AirflowTask: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        airflow_dag_qualified_name: str,
        connection_qualified_name: str,
    ) -> AirflowTask: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        airflow_dag_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> AirflowTask:
        validate_required_fields(
            ["name", "airflow_dag_qualified_name"],
            [name, airflow_dag_qualified_name],
        )
        attributes = AirflowTask.Attributes.creator(
            name=name,
            airflow_dag_qualified_name=airflow_dag_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="AirflowTask", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AirflowTask":
            raise ValueError("must be AirflowTask")
        return v

    def __setattr__(self, name, value):
        if name in AirflowTask._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AIRFLOW_TASK_OPERATOR_CLASS: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowTaskOperatorClass",
        "airflowTaskOperatorClass.keyword",
        "airflowTaskOperatorClass",
    )
    """
    Class name for the operator this task uses.
    """
    AIRFLOW_DAG_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowDagName", "airflowDagName.keyword", "airflowDagName"
    )
    """
    Simple name of the DAG this task is contained within.
    """
    AIRFLOW_DAG_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "airflowDagQualifiedName", "airflowDagQualifiedName"
    )
    """
    Unique name of the DAG this task is contained within.
    """
    AIRFLOW_TASK_CONNECTION_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "airflowTaskConnectionId",
        "airflowTaskConnectionId.keyword",
        "airflowTaskConnectionId",
    )
    """
    Identifier for the connection this task accesses.
    """
    AIRFLOW_TASK_SQL: ClassVar[KeywordField] = KeywordField(
        "airflowTaskSql", "airflowTaskSql"
    )
    """
    SQL code that executes through this task.
    """
    AIRFLOW_TASK_RETRY_NUMBER: ClassVar[NumericField] = NumericField(
        "airflowTaskRetryNumber", "airflowTaskRetryNumber"
    )
    """
    Retry count for this task running.
    """
    AIRFLOW_TASK_POOL: ClassVar[KeywordField] = KeywordField(
        "airflowTaskPool", "airflowTaskPool"
    )
    """
    Pool on which this run happened.
    """
    AIRFLOW_TASK_POOL_SLOTS: ClassVar[NumericField] = NumericField(
        "airflowTaskPoolSlots", "airflowTaskPoolSlots"
    )
    """
    Pool slots used for the run.
    """
    AIRFLOW_TASK_QUEUE: ClassVar[KeywordField] = KeywordField(
        "airflowTaskQueue", "airflowTaskQueue"
    )
    """
    Queue on which this run happened.
    """
    AIRFLOW_TASK_PRIORITY_WEIGHT: ClassVar[NumericField] = NumericField(
        "airflowTaskPriorityWeight", "airflowTaskPriorityWeight"
    )
    """
    Priority of the run.
    """
    AIRFLOW_TASK_TRIGGER_RULE: ClassVar[KeywordField] = KeywordField(
        "airflowTaskTriggerRule", "airflowTaskTriggerRule"
    )
    """
    Trigger for the run.
    """

    OUTPUTS: ClassVar[RelationField] = RelationField("outputs")
    """
    TBC
    """
    PROCESS: ClassVar[RelationField] = RelationField("process")
    """
    TBC
    """
    INPUTS: ClassVar[RelationField] = RelationField("inputs")
    """
    TBC
    """
    AIRFLOW_DAG: ClassVar[RelationField] = RelationField("airflowDag")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "airflow_task_operator_class",
        "airflow_dag_name",
        "airflow_dag_qualified_name",
        "airflow_task_connection_id",
        "airflow_task_sql",
        "airflow_task_retry_number",
        "airflow_task_pool",
        "airflow_task_pool_slots",
        "airflow_task_queue",
        "airflow_task_priority_weight",
        "airflow_task_trigger_rule",
        "outputs",
        "process",
        "inputs",
        "airflow_dag",
    ]

    @property
    def airflow_task_operator_class(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_operator_class
        )

    @airflow_task_operator_class.setter
    def airflow_task_operator_class(self, airflow_task_operator_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_operator_class = airflow_task_operator_class

    @property
    def airflow_dag_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_dag_name

    @airflow_dag_name.setter
    def airflow_dag_name(self, airflow_dag_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_name = airflow_dag_name

    @property
    def airflow_dag_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_dag_qualified_name
        )

    @airflow_dag_qualified_name.setter
    def airflow_dag_qualified_name(self, airflow_dag_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag_qualified_name = airflow_dag_qualified_name

    @property
    def airflow_task_connection_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_connection_id
        )

    @airflow_task_connection_id.setter
    def airflow_task_connection_id(self, airflow_task_connection_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_connection_id = airflow_task_connection_id

    @property
    def airflow_task_sql(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_task_sql

    @airflow_task_sql.setter
    def airflow_task_sql(self, airflow_task_sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_sql = airflow_task_sql

    @property
    def airflow_task_retry_number(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_retry_number
        )

    @airflow_task_retry_number.setter
    def airflow_task_retry_number(self, airflow_task_retry_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_retry_number = airflow_task_retry_number

    @property
    def airflow_task_pool(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_task_pool

    @airflow_task_pool.setter
    def airflow_task_pool(self, airflow_task_pool: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_pool = airflow_task_pool

    @property
    def airflow_task_pool_slots(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.airflow_task_pool_slots
        )

    @airflow_task_pool_slots.setter
    def airflow_task_pool_slots(self, airflow_task_pool_slots: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_pool_slots = airflow_task_pool_slots

    @property
    def airflow_task_queue(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.airflow_task_queue

    @airflow_task_queue.setter
    def airflow_task_queue(self, airflow_task_queue: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_queue = airflow_task_queue

    @property
    def airflow_task_priority_weight(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_priority_weight
        )

    @airflow_task_priority_weight.setter
    def airflow_task_priority_weight(self, airflow_task_priority_weight: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_priority_weight = airflow_task_priority_weight

    @property
    def airflow_task_trigger_rule(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.airflow_task_trigger_rule
        )

    @airflow_task_trigger_rule.setter
    def airflow_task_trigger_rule(self, airflow_task_trigger_rule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_task_trigger_rule = airflow_task_trigger_rule

    @property
    def outputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.process

    @process.setter
    def process(self, process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.process = process

    @property
    def inputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def airflow_dag(self) -> Optional[AirflowDag]:
        return None if self.attributes is None else self.attributes.airflow_dag

    @airflow_dag.setter
    def airflow_dag(self, airflow_dag: Optional[AirflowDag]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_dag = airflow_dag

    class Attributes(Airflow.Attributes):
        airflow_task_operator_class: Optional[str] = Field(default=None, description="")
        airflow_dag_name: Optional[str] = Field(default=None, description="")
        airflow_dag_qualified_name: Optional[str] = Field(default=None, description="")
        airflow_task_connection_id: Optional[str] = Field(default=None, description="")
        airflow_task_sql: Optional[str] = Field(default=None, description="")
        airflow_task_retry_number: Optional[int] = Field(default=None, description="")
        airflow_task_pool: Optional[str] = Field(default=None, description="")
        airflow_task_pool_slots: Optional[int] = Field(default=None, description="")
        airflow_task_queue: Optional[str] = Field(default=None, description="")
        airflow_task_priority_weight: Optional[int] = Field(
            default=None, description=""
        )
        airflow_task_trigger_rule: Optional[str] = Field(default=None, description="")
        outputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        process: Optional[Process] = Field(default=None, description="")  # relationship
        inputs: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        airflow_dag: Optional[AirflowDag] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            airflow_dag_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> AirflowTask.Attributes:
            validate_required_fields(
                ["name", "airflow_dag_qualified_name"],
                [name, airflow_dag_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    airflow_dag_qualified_name, "airflow_dag_qualified_name", 4
                )

            return AirflowTask.Attributes(
                name=name,
                airflow_dag_qualified_name=airflow_dag_qualified_name,
                connection_qualified_name=connection_qualified_name or connection_qn,
                qualified_name=f"{airflow_dag_qualified_name}/{name}",
                connector_name=connector_name,
                airflow_dag=AirflowDag.ref_by_qualified_name(
                    airflow_dag_qualified_name
                ),
            )

    attributes: AirflowTask.Attributes = Field(
        default_factory=lambda: AirflowTask.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .airflow_dag import AirflowDag  # noqa
from .catalog import Catalog  # noqa
from .process import Process  # noqa
