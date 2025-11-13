# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import BigqueryRoutineType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .procedure import Procedure


class BigqueryRoutine(Procedure):
    """Description"""

    type_name: str = Field(default="BigqueryRoutine", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "BigqueryRoutine":
            raise ValueError("must be BigqueryRoutine")
        return v

    def __setattr__(self, name, value):
        if name in BigqueryRoutine._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    BIGQUERY_ROUTINE_TYPE: ClassVar[KeywordField] = KeywordField(
        "bigqueryRoutineType", "bigqueryRoutineType"
    )
    """
    Type of bigquery routine (sp, udf, or tvf).
    """
    BIGQUERY_ROUTINE_ARGUMENTS: ClassVar[KeywordField] = KeywordField(
        "bigqueryRoutineArguments", "bigqueryRoutineArguments"
    )
    """
    Arguments that are passed in to the routine.
    """
    BIGQUERY_ROUTINE_RETURN_TYPE: ClassVar[KeywordField] = KeywordField(
        "bigqueryRoutineReturnType", "bigqueryRoutineReturnType"
    )
    """
    Return data type of the bigquery routine (null for stored procedures).
    """
    BIGQUERY_ROUTINE_SECURITY_TYPE: ClassVar[KeywordField] = KeywordField(
        "bigqueryRoutineSecurityType", "bigqueryRoutineSecurityType"
    )
    """
    Security type of the routine, always null.
    """
    BIGQUERY_ROUTINE_DDL: ClassVar[KeywordField] = KeywordField(
        "bigqueryRoutineDdl", "bigqueryRoutineDdl"
    )
    """
    The ddl statement used to create the bigquery routine.
    """

    BIGQUERY_ATLAN_SCHEMA: ClassVar[RelationField] = RelationField(
        "bigqueryAtlanSchema"
    )
    """
    TBC
    """
    BIGQUERY_PROCESSES: ClassVar[RelationField] = RelationField("bigqueryProcesses")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "bigquery_routine_type",
        "bigquery_routine_arguments",
        "bigquery_routine_return_type",
        "bigquery_routine_security_type",
        "bigquery_routine_ddl",
        "bigquery_atlan_schema",
        "bigquery_processes",
    ]

    @property
    def bigquery_routine_type(self) -> Optional[BigqueryRoutineType]:
        return (
            None if self.attributes is None else self.attributes.bigquery_routine_type
        )

    @bigquery_routine_type.setter
    def bigquery_routine_type(
        self, bigquery_routine_type: Optional[BigqueryRoutineType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_routine_type = bigquery_routine_type

    @property
    def bigquery_routine_arguments(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.bigquery_routine_arguments
        )

    @bigquery_routine_arguments.setter
    def bigquery_routine_arguments(
        self, bigquery_routine_arguments: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_routine_arguments = bigquery_routine_arguments

    @property
    def bigquery_routine_return_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.bigquery_routine_return_type
        )

    @bigquery_routine_return_type.setter
    def bigquery_routine_return_type(self, bigquery_routine_return_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_routine_return_type = bigquery_routine_return_type

    @property
    def bigquery_routine_security_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.bigquery_routine_security_type
        )

    @bigquery_routine_security_type.setter
    def bigquery_routine_security_type(
        self, bigquery_routine_security_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_routine_security_type = bigquery_routine_security_type

    @property
    def bigquery_routine_ddl(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.bigquery_routine_ddl

    @bigquery_routine_ddl.setter
    def bigquery_routine_ddl(self, bigquery_routine_ddl: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_routine_ddl = bigquery_routine_ddl

    @property
    def bigquery_atlan_schema(self) -> Optional[Schema]:
        return (
            None if self.attributes is None else self.attributes.bigquery_atlan_schema
        )

    @bigquery_atlan_schema.setter
    def bigquery_atlan_schema(self, bigquery_atlan_schema: Optional[Schema]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_atlan_schema = bigquery_atlan_schema

    @property
    def bigquery_processes(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.bigquery_processes

    @bigquery_processes.setter
    def bigquery_processes(self, bigquery_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_processes = bigquery_processes

    class Attributes(Procedure.Attributes):
        bigquery_routine_type: Optional[BigqueryRoutineType] = Field(
            default=None, description=""
        )
        bigquery_routine_arguments: Optional[Set[str]] = Field(
            default=None, description=""
        )
        bigquery_routine_return_type: Optional[str] = Field(
            default=None, description=""
        )
        bigquery_routine_security_type: Optional[str] = Field(
            default=None, description=""
        )
        bigquery_routine_ddl: Optional[str] = Field(default=None, description="")
        bigquery_atlan_schema: Optional[Schema] = Field(
            default=None, description=""
        )  # relationship
        bigquery_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: BigqueryRoutine.Attributes = Field(
        default_factory=lambda: BigqueryRoutine.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .process import Process  # noqa: E402, F401
from .schema import Schema  # noqa: E402, F401
