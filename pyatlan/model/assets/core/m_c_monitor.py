# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import MCRuleComparison, MCRuleSchedule

from .monte_carlo import MonteCarlo


class MCMonitor(MonteCarlo):
    """Description"""

    type_name: str = Field(default="MCMonitor", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MCMonitor":
            raise ValueError("must be MCMonitor")
        return v

    def __setattr__(self, name, value):
        if name in MCMonitor._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MC_MONITOR_ID: ClassVar[KeywordField] = KeywordField("mcMonitorId", "mcMonitorId")
    """
    Unique identifier for this monitor, from Monte Carlo.
    """
    MC_MONITOR_STATUS: ClassVar[KeywordField] = KeywordField(
        "mcMonitorStatus", "mcMonitorStatus"
    )
    """
    Status of this monitor.
    """
    MC_MONITOR_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorType", "mcMonitorType"
    )
    """
    Type of this monitor, for example: field health (stats) or dimension tracking (categories).
    """
    MC_MONITOR_WAREHOUSE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorWarehouse", "mcMonitorWarehouse"
    )
    """
    Name of the warehouse for this monitor.
    """
    MC_MONITOR_SCHEDULE_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorScheduleType", "mcMonitorScheduleType"
    )
    """
    Type of schedule for this monitor, for example: fixed or dynamic.
    """
    MC_MONITOR_NAMESPACE: ClassVar[KeywordTextField] = KeywordTextField(
        "mcMonitorNamespace", "mcMonitorNamespace.keyword", "mcMonitorNamespace"
    )
    """
    Namespace of this monitor.
    """
    MC_MONITOR_RULE_TYPE: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleType", "mcMonitorRuleType"
    )
    """
    Type of rule for this monitor.
    """
    MC_MONITOR_RULE_CUSTOM_SQL: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleCustomSql", "mcMonitorRuleCustomSql"
    )
    """
    SQL code for custom SQL rules.
    """
    MC_MONITOR_RULE_SCHEDULE_CONFIG: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleScheduleConfig", "mcMonitorRuleScheduleConfig"
    )
    """
    Schedule details for the rule.
    """
    MC_MONITOR_RULE_SCHEDULE_CONFIG_HUMANIZED: ClassVar[TextField] = TextField(
        "mcMonitorRuleScheduleConfigHumanized", "mcMonitorRuleScheduleConfigHumanized"
    )
    """
    Readable description of the schedule for the rule.
    """
    MC_MONITOR_ALERT_CONDITION: ClassVar[TextField] = TextField(
        "mcMonitorAlertCondition", "mcMonitorAlertCondition"
    )
    """
    Condition on which the monitor produces an alert.
    """
    MC_MONITOR_RULE_NEXT_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "mcMonitorRuleNextExecutionTime", "mcMonitorRuleNextExecutionTime"
    )
    """
    Time at which the next execution of the rule should occur.
    """
    MC_MONITOR_RULE_PREVIOUS_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "mcMonitorRulePreviousExecutionTime", "mcMonitorRulePreviousExecutionTime"
    )
    """
    Time at which the previous execution of the rule occurred.
    """
    MC_MONITOR_RULE_COMPARISONS: ClassVar[KeywordField] = KeywordField(
        "mcMonitorRuleComparisons", "mcMonitorRuleComparisons"
    )
    """
    Comparison logic used for the rule.
    """
    MC_MONITOR_RULE_IS_SNOOZED: ClassVar[BooleanField] = BooleanField(
        "mcMonitorRuleIsSnoozed", "mcMonitorRuleIsSnoozed"
    )
    """
    Whether the rule is currently snoozed (true) or not (false).
    """
    MC_MONITOR_BREACH_RATE: ClassVar[NumericField] = NumericField(
        "mcMonitorBreachRate", "mcMonitorBreachRate"
    )
    """
    Rate at which this monitor is breached.
    """
    MC_MONITOR_INCIDENT_COUNT: ClassVar[NumericField] = NumericField(
        "mcMonitorIncidentCount", "mcMonitorIncidentCount"
    )
    """
    Number of incidents associated with this monitor.
    """

    MC_MONITOR_ASSETS: ClassVar[RelationField] = RelationField("mcMonitorAssets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "mc_monitor_id",
        "mc_monitor_status",
        "mc_monitor_type",
        "mc_monitor_warehouse",
        "mc_monitor_schedule_type",
        "mc_monitor_namespace",
        "mc_monitor_rule_type",
        "mc_monitor_rule_custom_sql",
        "mc_monitor_rule_schedule_config",
        "mc_monitor_rule_schedule_config_humanized",
        "mc_monitor_alert_condition",
        "mc_monitor_rule_next_execution_time",
        "mc_monitor_rule_previous_execution_time",
        "mc_monitor_rule_comparisons",
        "mc_monitor_rule_is_snoozed",
        "mc_monitor_breach_rate",
        "mc_monitor_incident_count",
        "mc_monitor_assets",
    ]

    @property
    def mc_monitor_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_id

    @mc_monitor_id.setter
    def mc_monitor_id(self, mc_monitor_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_id = mc_monitor_id

    @property
    def mc_monitor_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_status

    @mc_monitor_status.setter
    def mc_monitor_status(self, mc_monitor_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_status = mc_monitor_status

    @property
    def mc_monitor_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_type

    @mc_monitor_type.setter
    def mc_monitor_type(self, mc_monitor_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_type = mc_monitor_type

    @property
    def mc_monitor_warehouse(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_warehouse

    @mc_monitor_warehouse.setter
    def mc_monitor_warehouse(self, mc_monitor_warehouse: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_warehouse = mc_monitor_warehouse

    @property
    def mc_monitor_schedule_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_schedule_type
        )

    @mc_monitor_schedule_type.setter
    def mc_monitor_schedule_type(self, mc_monitor_schedule_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_schedule_type = mc_monitor_schedule_type

    @property
    def mc_monitor_namespace(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_namespace

    @mc_monitor_namespace.setter
    def mc_monitor_namespace(self, mc_monitor_namespace: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_namespace = mc_monitor_namespace

    @property
    def mc_monitor_rule_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.mc_monitor_rule_type

    @mc_monitor_rule_type.setter
    def mc_monitor_rule_type(self, mc_monitor_rule_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_type = mc_monitor_rule_type

    @property
    def mc_monitor_rule_custom_sql(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_custom_sql
        )

    @mc_monitor_rule_custom_sql.setter
    def mc_monitor_rule_custom_sql(self, mc_monitor_rule_custom_sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_custom_sql = mc_monitor_rule_custom_sql

    @property
    def mc_monitor_rule_schedule_config(self) -> Optional[MCRuleSchedule]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_schedule_config
        )

    @mc_monitor_rule_schedule_config.setter
    def mc_monitor_rule_schedule_config(
        self, mc_monitor_rule_schedule_config: Optional[MCRuleSchedule]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_schedule_config = (
            mc_monitor_rule_schedule_config
        )

    @property
    def mc_monitor_rule_schedule_config_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_schedule_config_humanized
        )

    @mc_monitor_rule_schedule_config_humanized.setter
    def mc_monitor_rule_schedule_config_humanized(
        self, mc_monitor_rule_schedule_config_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_schedule_config_humanized = (
            mc_monitor_rule_schedule_config_humanized
        )

    @property
    def mc_monitor_alert_condition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_alert_condition
        )

    @mc_monitor_alert_condition.setter
    def mc_monitor_alert_condition(self, mc_monitor_alert_condition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_alert_condition = mc_monitor_alert_condition

    @property
    def mc_monitor_rule_next_execution_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_next_execution_time
        )

    @mc_monitor_rule_next_execution_time.setter
    def mc_monitor_rule_next_execution_time(
        self, mc_monitor_rule_next_execution_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_next_execution_time = (
            mc_monitor_rule_next_execution_time
        )

    @property
    def mc_monitor_rule_previous_execution_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_previous_execution_time
        )

    @mc_monitor_rule_previous_execution_time.setter
    def mc_monitor_rule_previous_execution_time(
        self, mc_monitor_rule_previous_execution_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_previous_execution_time = (
            mc_monitor_rule_previous_execution_time
        )

    @property
    def mc_monitor_rule_comparisons(self) -> Optional[List[MCRuleComparison]]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_comparisons
        )

    @mc_monitor_rule_comparisons.setter
    def mc_monitor_rule_comparisons(
        self, mc_monitor_rule_comparisons: Optional[List[MCRuleComparison]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_comparisons = mc_monitor_rule_comparisons

    @property
    def mc_monitor_rule_is_snoozed(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_rule_is_snoozed
        )

    @mc_monitor_rule_is_snoozed.setter
    def mc_monitor_rule_is_snoozed(self, mc_monitor_rule_is_snoozed: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_rule_is_snoozed = mc_monitor_rule_is_snoozed

    @property
    def mc_monitor_breach_rate(self) -> Optional[float]:
        return (
            None if self.attributes is None else self.attributes.mc_monitor_breach_rate
        )

    @mc_monitor_breach_rate.setter
    def mc_monitor_breach_rate(self, mc_monitor_breach_rate: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_breach_rate = mc_monitor_breach_rate

    @property
    def mc_monitor_incident_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_monitor_incident_count
        )

    @mc_monitor_incident_count.setter
    def mc_monitor_incident_count(self, mc_monitor_incident_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_incident_count = mc_monitor_incident_count

    @property
    def mc_monitor_assets(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.mc_monitor_assets

    @mc_monitor_assets.setter
    def mc_monitor_assets(self, mc_monitor_assets: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_monitor_assets = mc_monitor_assets

    class Attributes(MonteCarlo.Attributes):
        mc_monitor_id: Optional[str] = Field(default=None, description="")
        mc_monitor_status: Optional[str] = Field(default=None, description="")
        mc_monitor_type: Optional[str] = Field(default=None, description="")
        mc_monitor_warehouse: Optional[str] = Field(default=None, description="")
        mc_monitor_schedule_type: Optional[str] = Field(default=None, description="")
        mc_monitor_namespace: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_type: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_custom_sql: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_schedule_config: Optional[MCRuleSchedule] = Field(
            default=None, description=""
        )
        mc_monitor_rule_schedule_config_humanized: Optional[str] = Field(
            default=None, description=""
        )
        mc_monitor_alert_condition: Optional[str] = Field(default=None, description="")
        mc_monitor_rule_next_execution_time: Optional[datetime] = Field(
            default=None, description=""
        )
        mc_monitor_rule_previous_execution_time: Optional[datetime] = Field(
            default=None, description=""
        )
        mc_monitor_rule_comparisons: Optional[List[MCRuleComparison]] = Field(
            default=None, description=""
        )
        mc_monitor_rule_is_snoozed: Optional[bool] = Field(default=None, description="")
        mc_monitor_breach_rate: Optional[float] = Field(default=None, description="")
        mc_monitor_incident_count: Optional[int] = Field(default=None, description="")
        mc_monitor_assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MCMonitor.Attributes = Field(
        default_factory=lambda: MCMonitor.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
