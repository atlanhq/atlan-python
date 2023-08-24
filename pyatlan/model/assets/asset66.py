# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .asset41 import Redash


class RedashQuery(Redash):
    """Description"""

    type_name: str = Field("RedashQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashQuery":
            raise ValueError("must be RedashQuery")
        return v

    def __setattr__(self, name, value):
        if name in RedashQuery._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    REDASH_QUERY_SQL: ClassVar[KeywordField] = KeywordField(
        "redashQuerySQL", "redashQuerySQL"
    )
    """
    SQL code of Redash Query
    """
    REDASH_QUERY_PARAMETERS: ClassVar[KeywordField] = KeywordField(
        "redashQueryParameters", "redashQueryParameters"
    )
    """
    Parameters of Redash Query
    """
    REDASH_QUERY_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "redashQuerySchedule", "redashQuerySchedule"
    )
    """
    Schedule of Redash Query
    """
    REDASH_QUERY_LAST_EXECUTION_RUNTIME: ClassVar[NumericField] = NumericField(
        "redashQueryLastExecutionRuntime", "redashQueryLastExecutionRuntime"
    )
    """
    Runtime of Redash Query
    """
    REDASH_QUERY_LAST_EXECUTED_AT: ClassVar[NumericField] = NumericField(
        "redashQueryLastExecutedAt", "redashQueryLastExecutedAt"
    )
    """
    Time when the Redash Query was last executed
    """
    REDASH_QUERY_SCHEDULE_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "redashQueryScheduleHumanized",
        "redashQueryScheduleHumanized",
        "redashQueryScheduleHumanized.text",
    )
    """
    Query schedule for overview tab and filtering.
    """

    REDASH_VISUALIZATIONS: ClassVar[RelationField] = RelationField(
        "redashVisualizations"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "redash_query_s_q_l",
        "redash_query_parameters",
        "redash_query_schedule",
        "redash_query_last_execution_runtime",
        "redash_query_last_executed_at",
        "redash_query_schedule_humanized",
        "redash_visualizations",
    ]

    @property
    def redash_query_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.redash_query_s_q_l

    @redash_query_s_q_l.setter
    def redash_query_s_q_l(self, redash_query_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_s_q_l = redash_query_s_q_l

    @property
    def redash_query_parameters(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.redash_query_parameters
        )

    @redash_query_parameters.setter
    def redash_query_parameters(self, redash_query_parameters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_parameters = redash_query_parameters

    @property
    def redash_query_schedule(self) -> Optional[dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.redash_query_schedule
        )

    @redash_query_schedule.setter
    def redash_query_schedule(self, redash_query_schedule: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_schedule = redash_query_schedule

    @property
    def redash_query_last_execution_runtime(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_last_execution_runtime
        )

    @redash_query_last_execution_runtime.setter
    def redash_query_last_execution_runtime(
        self, redash_query_last_execution_runtime: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_last_execution_runtime = (
            redash_query_last_execution_runtime
        )

    @property
    def redash_query_last_executed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_last_executed_at
        )

    @redash_query_last_executed_at.setter
    def redash_query_last_executed_at(
        self, redash_query_last_executed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_last_executed_at = redash_query_last_executed_at

    @property
    def redash_query_schedule_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_schedule_humanized
        )

    @redash_query_schedule_humanized.setter
    def redash_query_schedule_humanized(
        self, redash_query_schedule_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_schedule_humanized = (
            redash_query_schedule_humanized
        )

    @property
    def redash_visualizations(self) -> Optional[list[RedashVisualization]]:
        return (
            None if self.attributes is None else self.attributes.redash_visualizations
        )

    @redash_visualizations.setter
    def redash_visualizations(
        self, redash_visualizations: Optional[list[RedashVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_visualizations = redash_visualizations

    class Attributes(Redash.Attributes):
        redash_query_s_q_l: Optional[str] = Field(
            None, description="", alias="redashQuerySQL"
        )
        redash_query_parameters: Optional[str] = Field(
            None, description="", alias="redashQueryParameters"
        )
        redash_query_schedule: Optional[dict[str, str]] = Field(
            None, description="", alias="redashQuerySchedule"
        )
        redash_query_last_execution_runtime: Optional[float] = Field(
            None, description="", alias="redashQueryLastExecutionRuntime"
        )
        redash_query_last_executed_at: Optional[datetime] = Field(
            None, description="", alias="redashQueryLastExecutedAt"
        )
        redash_query_schedule_humanized: Optional[str] = Field(
            None, description="", alias="redashQueryScheduleHumanized"
        )
        redash_visualizations: Optional[list[RedashVisualization]] = Field(
            None, description="", alias="redashVisualizations"
        )  # relationship

    attributes: "RedashQuery.Attributes" = Field(
        default_factory=lambda: RedashQuery.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class RedashVisualization(Redash):
    """Description"""

    type_name: str = Field("RedashVisualization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "RedashVisualization":
            raise ValueError("must be RedashVisualization")
        return v

    def __setattr__(self, name, value):
        if name in RedashVisualization._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    REDASH_VISUALIZATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "redashVisualizationType", "redashVisualizationType"
    )
    """
    Redash Visualization Type
    """
    REDASH_QUERY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "redashQueryName", "redashQueryName.keyword", "redashQueryName"
    )
    """
    Redash Query from which visualization is created
    """
    REDASH_QUERY_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "redashQueryQualifiedName",
        "redashQueryQualifiedName",
        "redashQueryQualifiedName.text",
    )
    """
    Qualified name of the Redash Query from which visualization is created
    """

    REDASH_QUERY: ClassVar[RelationField] = RelationField("redashQuery")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "redash_visualization_type",
        "redash_query_name",
        "redash_query_qualified_name",
        "redash_query",
    ]

    @property
    def redash_visualization_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_visualization_type
        )

    @redash_visualization_type.setter
    def redash_visualization_type(self, redash_visualization_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_visualization_type = redash_visualization_type

    @property
    def redash_query_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.redash_query_name

    @redash_query_name.setter
    def redash_query_name(self, redash_query_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_name = redash_query_name

    @property
    def redash_query_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.redash_query_qualified_name
        )

    @redash_query_qualified_name.setter
    def redash_query_qualified_name(self, redash_query_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query_qualified_name = redash_query_qualified_name

    @property
    def redash_query(self) -> Optional[RedashQuery]:
        return None if self.attributes is None else self.attributes.redash_query

    @redash_query.setter
    def redash_query(self, redash_query: Optional[RedashQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_query = redash_query

    class Attributes(Redash.Attributes):
        redash_visualization_type: Optional[str] = Field(
            None, description="", alias="redashVisualizationType"
        )
        redash_query_name: Optional[str] = Field(
            None, description="", alias="redashQueryName"
        )
        redash_query_qualified_name: Optional[str] = Field(
            None, description="", alias="redashQueryQualifiedName"
        )
        redash_query: Optional[RedashQuery] = Field(
            None, description="", alias="redashQuery"
        )  # relationship

    attributes: "RedashVisualization.Attributes" = Field(
        default_factory=lambda: RedashVisualization.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


RedashQuery.Attributes.update_forward_refs()


RedashVisualization.Attributes.update_forward_refs()
