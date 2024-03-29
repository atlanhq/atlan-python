# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .redash import Redash


class RedashQuery(Redash):
    """Description"""

    type_name: str = Field(default="RedashQuery", allow_mutation=False)

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
    SQL code of this query.
    """
    REDASH_QUERY_PARAMETERS: ClassVar[KeywordField] = KeywordField(
        "redashQueryParameters", "redashQueryParameters"
    )
    """
    Parameters of this query.
    """
    REDASH_QUERY_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "redashQuerySchedule", "redashQuerySchedule"
    )
    """
    Schedule for this query.
    """
    REDASH_QUERY_LAST_EXECUTION_RUNTIME: ClassVar[NumericField] = NumericField(
        "redashQueryLastExecutionRuntime", "redashQueryLastExecutionRuntime"
    )
    """
    Elapsed time of the last execution of this query.
    """
    REDASH_QUERY_LAST_EXECUTED_AT: ClassVar[NumericField] = NumericField(
        "redashQueryLastExecutedAt", "redashQueryLastExecutedAt"
    )
    """
    Time (epoch) when this query was last executed, in milliseconds.
    """
    REDASH_QUERY_SCHEDULE_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "redashQueryScheduleHumanized",
        "redashQueryScheduleHumanized",
        "redashQueryScheduleHumanized.text",
    )
    """
    Schdule for this query in readable text for overview tab and filtering.
    """

    REDASH_VISUALIZATIONS: ClassVar[RelationField] = RelationField(
        "redashVisualizations"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def redash_query_schedule(self) -> Optional[Dict[str, str]]:
        return (
            None if self.attributes is None else self.attributes.redash_query_schedule
        )

    @redash_query_schedule.setter
    def redash_query_schedule(self, redash_query_schedule: Optional[Dict[str, str]]):
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
    def redash_visualizations(self) -> Optional[List[RedashVisualization]]:
        return (
            None if self.attributes is None else self.attributes.redash_visualizations
        )

    @redash_visualizations.setter
    def redash_visualizations(
        self, redash_visualizations: Optional[List[RedashVisualization]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_visualizations = redash_visualizations

    class Attributes(Redash.Attributes):
        redash_query_s_q_l: Optional[str] = Field(default=None, description="")
        redash_query_parameters: Optional[str] = Field(default=None, description="")
        redash_query_schedule: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        redash_query_last_execution_runtime: Optional[float] = Field(
            default=None, description=""
        )
        redash_query_last_executed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        redash_query_schedule_humanized: Optional[str] = Field(
            default=None, description=""
        )
        redash_visualizations: Optional[List[RedashVisualization]] = Field(
            default=None, description=""
        )  # relationship

    attributes: RedashQuery.Attributes = Field(
        default_factory=lambda: RedashQuery.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .redash_visualization import RedashVisualization  # noqa
