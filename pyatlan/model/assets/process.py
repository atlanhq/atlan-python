# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
from io import StringIO
from typing import ClassVar, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .asset import Asset


class Process(Asset, type_name="Process"):
    """Description"""

    @classmethod
    @init_guid
    def create(
        cls,
        name: str,
        connection_qualified_name: str,
        inputs: list["Catalog"],
        outputs: list["Catalog"],
        process_id: Optional[str] = None,
        parent: Optional[Process] = None,
    ) -> Process:
        return Process(
            attributes=Process.Attributes.create(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
        )

    type_name: str = Field(default="Process", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Process":
            raise ValueError("must be Process")
        return v

    def __setattr__(self, name, value):
        if name in Process._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CODE: ClassVar[KeywordField] = KeywordField("code", "code")
    """
    Code that ran within the process.
    """
    SQL: ClassVar[KeywordField] = KeywordField("sql", "sql")
    """
    SQL query that ran to produce the outputs.
    """
    AST: ClassVar[KeywordField] = KeywordField("ast", "ast")
    """
    Parsed AST of the code or SQL statements that describe the logic of this process.
    """

    MATILLION_COMPONENT: ClassVar[RelationField] = RelationField("matillionComponent")
    """
    TBC
    """
    AIRFLOW_TASKS: ClassVar[RelationField] = RelationField("airflowTasks")
    """
    TBC
    """
    COLUMN_PROCESSES: ClassVar[RelationField] = RelationField("columnProcesses")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "inputs",
        "outputs",
        "code",
        "sql",
        "ast",
        "matillion_component",
        "airflow_tasks",
        "column_processes",
    ]

    @property
    def inputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[list[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[list[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[list[Catalog]]):
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
    def ast(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ast

    @ast.setter
    def ast(self, ast: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ast = ast

    @property
    def matillion_component(self) -> Optional[MatillionComponent]:
        return None if self.attributes is None else self.attributes.matillion_component

    @matillion_component.setter
    def matillion_component(self, matillion_component: Optional[MatillionComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component = matillion_component

    @property
    def airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return None if self.attributes is None else self.attributes.airflow_tasks

    @airflow_tasks.setter
    def airflow_tasks(self, airflow_tasks: Optional[list[AirflowTask]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_tasks = airflow_tasks

    @property
    def column_processes(self) -> Optional[list[ColumnProcess]]:
        return None if self.attributes is None else self.attributes.column_processes

    @column_processes.setter
    def column_processes(self, column_processes: Optional[list[ColumnProcess]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_processes = column_processes

    class Attributes(Asset.Attributes):
        inputs: Optional[list[Catalog]] = Field(default=None, description="")
        outputs: Optional[list[Catalog]] = Field(default=None, description="")
        code: Optional[str] = Field(default=None, description="")
        sql: Optional[str] = Field(default=None, description="")
        ast: Optional[str] = Field(default=None, description="")
        matillion_component: Optional[MatillionComponent] = Field(
            default=None, description=""
        )  # relationship
        airflow_tasks: Optional[list[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        column_processes: Optional[list[ColumnProcess]] = Field(
            default=None, description=""
        )  # relationship

        @staticmethod
        def generate_qualified_name(
            name: str,
            connection_qualified_name: str,
            inputs: list["Catalog"],
            outputs: list["Catalog"],
            parent: Optional["Process"] = None,
            process_id: Optional[str] = None,
        ) -> str:
            def append_relationship(output: StringIO, relationship: Asset):
                if relationship.guid:
                    output.write(relationship.guid)

            def append_relationships(output: StringIO, relationships: list["Catalog"]):
                for catalog in relationships:
                    append_relationship(output, catalog)

            validate_required_fields(
                ["name", "connection_qualified_name", "inputs", "outputs"],
                [name, connection_qualified_name, inputs, outputs],
            )
            if process_id and process_id.strip():
                return f"{connection_qualified_name}/{process_id}"
            buffer = StringIO()
            buffer.write(name)
            buffer.write(connection_qualified_name)
            if parent:
                append_relationship(buffer, parent)
            append_relationships(buffer, inputs)
            append_relationships(buffer, outputs)
            ret_value = hashlib.md5(
                buffer.getvalue().encode(), usedforsecurity=False
            ).hexdigest()
            buffer.close()
            return ret_value

        @classmethod
        @init_guid
        def create(
            cls,
            name: str,
            connection_qualified_name: str,
            inputs: list["Catalog"],
            outputs: list["Catalog"],
            process_id: Optional[str] = None,
            parent: Optional[Process] = None,
        ) -> Process.Attributes:
            qualified_name = Process.Attributes.generate_qualified_name(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
            connector_name = connection_qualified_name.split("/")[1]
            return Process.Attributes(
                name=name,
                qualified_name=qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
                inputs=inputs,
                outputs=outputs,
            )

    attributes: "Process.Attributes" = Field(
        default_factory=lambda: Process.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


from .airflow_task import AirflowTask  # noqa: E402
from .catalog import Catalog  # noqa: E402
from .column_process import ColumnProcess  # noqa: E402
from .matillion_component import MatillionComponent  # noqa: E402