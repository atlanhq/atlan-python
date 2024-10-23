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

from .fivetran import Fivetran


class FivetranConnector(Fivetran):
    """Description"""

    type_name: str = Field(default="FivetranConnector", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FivetranConnector":
            raise ValueError("must be FivetranConnector")
        return v

    def __setattr__(self, name, value):
        if name in FivetranConnector._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FIVETRAN_CONNECTOR_LAST_SYNC_ID: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorLastSyncId", "fivetranConnectorLastSyncId"
    )
    """
    ID of the latest sync
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_STARTED_AT: ClassVar[NumericField] = NumericField(
        "fivetranConnectorLastSyncStartedAt", "fivetranConnectorLastSyncStartedAt"
    )
    """
    Timestamp (epoch) when the latest sync started on Fivetran, in milliseconds
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_FINISHED_AT: ClassVar[NumericField] = NumericField(
        "fivetranConnectorLastSyncFinishedAt", "fivetranConnectorLastSyncFinishedAt"
    )
    """
    Timestamp (epoch) when the latest sync finished on Fivetran, in milliseconds
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_REASON: ClassVar[KeywordTextField] = KeywordTextField(
        "fivetranConnectorLastSyncReason",
        "fivetranConnectorLastSyncReason.keyword",
        "fivetranConnectorLastSyncReason",
    )
    """
    Failure reason for the latest sync on Fivetran. If status is FAILURE, this is the description of the reason why the sync failed. If status is FAILURE_WITH_TASK, this is the description of the Error. If status is RESCHEDULED, this is the description of the reason why the sync is rescheduled.
    """  # noqa: E501
    FIVETRAN_CONNECTOR_LAST_SYNC_TASK_TYPE: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorLastSyncTaskType", "fivetranConnectorLastSyncTaskType"
    )
    """
    Failure task type for the latest sync on Fivetran. If status is FAILURE_WITH_TASK or RESCHEDULED, this field displays the type of the Error that caused the failure or rescheduling, respectively, e.g., reconnect, update_service_account, etc.
    """  # noqa: E501
    FIVETRAN_CONNECTOR_LAST_SYNC_RESCHEDULED_AT: ClassVar[NumericField] = NumericField(
        "fivetranConnectorLastSyncRescheduledAt",
        "fivetranConnectorLastSyncRescheduledAt",
    )
    """
    Timestamp (epoch) at which the latest sync is rescheduled at on Fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_TABLES_SYNCED: ClassVar[NumericField] = NumericField(
        "fivetranConnectorLastSyncTablesSynced", "fivetranConnectorLastSyncTablesSynced"
    )
    """
    Number of tables synced in the latest sync on Fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_EXTRACT_TIME_SECONDS: ClassVar[NumericField] = (
        NumericField(
            "fivetranConnectorLastSyncExtractTimeSeconds",
            "fivetranConnectorLastSyncExtractTimeSeconds",
        )
    )
    """
    Extract time in seconds in the latest sync on fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_EXTRACT_VOLUME_MEGABYTES: ClassVar[NumericField] = (
        NumericField(
            "fivetranConnectorLastSyncExtractVolumeMegabytes",
            "fivetranConnectorLastSyncExtractVolumeMegabytes",
        )
    )
    """
    Extracted data volume in metabytes in the latest sync on Fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_LOAD_TIME_SECONDS: ClassVar[NumericField] = (
        NumericField(
            "fivetranConnectorLastSyncLoadTimeSeconds",
            "fivetranConnectorLastSyncLoadTimeSeconds",
        )
    )
    """
    Load time in seconds in the latest sync on Fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_LOAD_VOLUME_MEGABYTES: ClassVar[NumericField] = (
        NumericField(
            "fivetranConnectorLastSyncLoadVolumeMegabytes",
            "fivetranConnectorLastSyncLoadVolumeMegabytes",
        )
    )
    """
    Loaded data volume in metabytes in the latest sync on Fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_PROCESS_TIME_SECONDS: ClassVar[NumericField] = (
        NumericField(
            "fivetranConnectorLastSyncProcessTimeSeconds",
            "fivetranConnectorLastSyncProcessTimeSeconds",
        )
    )
    """
    Process time in seconds in the latest sync on Fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_PROCESS_VOLUME_MEGABYTES: ClassVar[NumericField] = (
        NumericField(
            "fivetranConnectorLastSyncProcessVolumeMegabytes",
            "fivetranConnectorLastSyncProcessVolumeMegabytes",
        )
    )
    """
    Process volume in metabytes in the latest sync on Fivetran
    """
    FIVETRAN_CONNECTOR_LAST_SYNC_TOTAL_TIME_SECONDS: ClassVar[NumericField] = (
        NumericField(
            "fivetranConnectorLastSyncTotalTimeSeconds",
            "fivetranConnectorLastSyncTotalTimeSeconds",
        )
    )
    """
    Total sync time in seconds in the latest sync on Fivetran
    """
    FIVETRAN_CONNECTOR_NAME: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorName", "fivetranConnectorName"
    )
    """
    Connector name added by the user on Fivetran
    """
    FIVETRAN_CONNECTOR_TYPE: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorType", "fivetranConnectorType"
    )
    """
    Type of connector on Fivetran. Eg: snowflake, google_analytics, notion etc.
    """
    FIVETRAN_CONNECTOR_URL: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorURL", "fivetranConnectorURL"
    )
    """
    URL to open the connector details on Fivetran
    """
    FIVETRAN_CONNECTOR_DESTINATION_NAME: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorDestinationName", "fivetranConnectorDestinationName"
    )
    """
    Destination name added by the user on Fivetran
    """
    FIVETRAN_CONNECTOR_DESTINATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorDestinationType", "fivetranConnectorDestinationType"
    )
    """
    Type of destination on Fivetran. Eg: redshift, bigquery etc.
    """
    FIVETRAN_CONNECTOR_DESTINATION_URL: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorDestinationURL", "fivetranConnectorDestinationURL"
    )
    """
    URL to open the destination details on Fivetran
    """
    FIVETRAN_CONNECTOR_SYNC_SETUP_ON: ClassVar[NumericField] = NumericField(
        "fivetranConnectorSyncSetupOn", "fivetranConnectorSyncSetupOn"
    )
    """
    Timestamp (epoch) on which the connector was setup on Fivetran, in milliseconds
    """
    FIVETRAN_CONNECTOR_SYNC_FREQUENCY: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorSyncFrequency", "fivetranConnectorSyncFrequency"
    )
    """
    Sync frequency for the connector in number of hours. Eg: Every 6 hours
    """
    FIVETRAN_CONNECTOR_SYNC_PAUSED: ClassVar[BooleanField] = BooleanField(
        "fivetranConnectorSyncPaused", "fivetranConnectorSyncPaused"
    )
    """
    Boolean to indicate whether the sync for this connector is paused or not
    """
    FIVETRAN_CONNECTOR_SYNC_SETUP_USER_FULL_NAME: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorSyncSetupUserFullName",
        "fivetranConnectorSyncSetupUserFullName",
    )
    """
    Full name of the user who setup the connector on Fivetran
    """
    FIVETRAN_CONNECTOR_SYNC_SETUP_USER_EMAIL: ClassVar[KeywordField] = KeywordField(
        "fivetranConnectorSyncSetupUserEmail", "fivetranConnectorSyncSetupUserEmail"
    )
    """
    Email ID of the user who setpu the connector on Fivetran
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_FREE: ClassVar[NumericField] = NumericField(
        "fivetranConnectorMonthlyActiveRowsFree",
        "fivetranConnectorMonthlyActiveRowsFree",
    )
    """
    Free Monthly Active Rows used by the connector in the past month
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_PAID: ClassVar[NumericField] = NumericField(
        "fivetranConnectorMonthlyActiveRowsPaid",
        "fivetranConnectorMonthlyActiveRowsPaid",
    )
    """
    Paid Monthly Active Rows used by the connector in the past month
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_TOTAL: ClassVar[NumericField] = NumericField(
        "fivetranConnectorMonthlyActiveRowsTotal",
        "fivetranConnectorMonthlyActiveRowsTotal",
    )
    """
    Total Monthly Active Rows used by the connector in the past month
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_CHANGE_PERCENTAGE_FREE: ClassVar[
        NumericField
    ] = NumericField(
        "fivetranConnectorMonthlyActiveRowsChangePercentageFree",
        "fivetranConnectorMonthlyActiveRowsChangePercentageFree",
    )
    """
    Increase in the percentage of free MAR compared to the previous month
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_CHANGE_PERCENTAGE_PAID: ClassVar[
        NumericField
    ] = NumericField(
        "fivetranConnectorMonthlyActiveRowsChangePercentagePaid",
        "fivetranConnectorMonthlyActiveRowsChangePercentagePaid",
    )
    """
    Increase in the percentage of paid MAR compared to the previous month
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_CHANGE_PERCENTAGE_TOTAL: ClassVar[
        NumericField
    ] = NumericField(
        "fivetranConnectorMonthlyActiveRowsChangePercentageTotal",
        "fivetranConnectorMonthlyActiveRowsChangePercentageTotal",
    )
    """
    Increase in the percentage of total MAR compared to the previous month
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_FREE_PERCENTAGE_OF_ACCOUNT: ClassVar[
        NumericField
    ] = NumericField(
        "fivetranConnectorMonthlyActiveRowsFreePercentageOfAccount",
        "fivetranConnectorMonthlyActiveRowsFreePercentageOfAccount",
    )
    """
    Percentage of the account's total free MAR used by this connector
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_PAID_PERCENTAGE_OF_ACCOUNT: ClassVar[
        NumericField
    ] = NumericField(
        "fivetranConnectorMonthlyActiveRowsPaidPercentageOfAccount",
        "fivetranConnectorMonthlyActiveRowsPaidPercentageOfAccount",
    )
    """
    Percentage of the account's total paid MAR used by this connector
    """
    FIVETRAN_CONNECTOR_MONTHLY_ACTIVE_ROWS_TOTAL_PERCENTAGE_OF_ACCOUNT: ClassVar[
        NumericField
    ] = NumericField(
        "fivetranConnectorMonthlyActiveRowsTotalPercentageOfAccount",
        "fivetranConnectorMonthlyActiveRowsTotalPercentageOfAccount",
    )
    """
    Percentage of the account's total MAR used by this connector
    """
    FIVETRAN_CONNECTOR_TOTAL_TABLES_SYNCED: ClassVar[NumericField] = NumericField(
        "fivetranConnectorTotalTablesSynced", "fivetranConnectorTotalTablesSynced"
    )
    """
    Total number of tables synced by this connector
    """
    FIVETRAN_CONNECTOR_TOP_TABLES_BY_MAR: ClassVar[TextField] = TextField(
        "fivetranConnectorTopTablesByMAR", "fivetranConnectorTopTablesByMAR"
    )
    """
    Total five tables sorted by MAR synced by this connector
    """
    FIVETRAN_CONNECTOR_USAGE_COST: ClassVar[NumericField] = NumericField(
        "fivetranConnectorUsageCost", "fivetranConnectorUsageCost"
    )
    """
    Total usage cost by this destination
    """
    FIVETRAN_CONNECTOR_CREDITS_USED: ClassVar[NumericField] = NumericField(
        "fivetranConnectorCreditsUsed", "fivetranConnectorCreditsUsed"
    )
    """
    Total credits used by this destination
    """

    PROCESSES: ClassVar[RelationField] = RelationField("processes")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fivetran_connector_last_sync_id",
        "fivetran_connector_last_sync_started_at",
        "fivetran_connector_last_sync_finished_at",
        "fivetran_connector_last_sync_reason",
        "fivetran_connector_last_sync_task_type",
        "fivetran_connector_last_sync_rescheduled_at",
        "fivetran_connector_last_sync_tables_synced",
        "fivetran_connector_last_sync_extract_time_seconds",
        "fivetran_connector_last_sync_extract_volume_megabytes",
        "fivetran_connector_last_sync_load_time_seconds",
        "fivetran_connector_last_sync_load_volume_megabytes",
        "fivetran_connector_last_sync_process_time_seconds",
        "fivetran_connector_last_sync_process_volume_megabytes",
        "fivetran_connector_last_sync_total_time_seconds",
        "fivetran_connector_name",
        "fivetran_connector_type",
        "fivetran_connector_url",
        "fivetran_connector_destination_name",
        "fivetran_connector_destination_type",
        "fivetran_connector_destination_url",
        "fivetran_connector_sync_setup_on",
        "fivetran_connector_sync_frequency",
        "fivetran_connector_sync_paused",
        "fivetran_connector_sync_setup_user_full_name",
        "fivetran_connector_sync_setup_user_email",
        "fivetran_connector_monthly_active_rows_free",
        "fivetran_connector_monthly_active_rows_paid",
        "fivetran_connector_monthly_active_rows_total",
        "fivetran_connector_monthly_active_rows_change_percentage_free",
        "fivetran_connector_monthly_active_rows_change_percentage_paid",
        "fivetran_connector_monthly_active_rows_change_percentage_total",
        "fivetran_connector_monthly_active_rows_free_percentage_of_account",
        "fivetran_connector_monthly_active_rows_paid_percentage_of_account",
        "fivetran_connector_monthly_active_rows_total_percentage_of_account",
        "fivetran_connector_total_tables_synced",
        "fivetran_connector_top_tables_by_m_a_r",
        "fivetran_connector_usage_cost",
        "fivetran_connector_credits_used",
        "processes",
    ]

    @property
    def fivetran_connector_last_sync_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_id
        )

    @fivetran_connector_last_sync_id.setter
    def fivetran_connector_last_sync_id(
        self, fivetran_connector_last_sync_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_id = (
            fivetran_connector_last_sync_id
        )

    @property
    def fivetran_connector_last_sync_started_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_started_at
        )

    @fivetran_connector_last_sync_started_at.setter
    def fivetran_connector_last_sync_started_at(
        self, fivetran_connector_last_sync_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_started_at = (
            fivetran_connector_last_sync_started_at
        )

    @property
    def fivetran_connector_last_sync_finished_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_finished_at
        )

    @fivetran_connector_last_sync_finished_at.setter
    def fivetran_connector_last_sync_finished_at(
        self, fivetran_connector_last_sync_finished_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_finished_at = (
            fivetran_connector_last_sync_finished_at
        )

    @property
    def fivetran_connector_last_sync_reason(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_reason
        )

    @fivetran_connector_last_sync_reason.setter
    def fivetran_connector_last_sync_reason(
        self, fivetran_connector_last_sync_reason: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_reason = (
            fivetran_connector_last_sync_reason
        )

    @property
    def fivetran_connector_last_sync_task_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_task_type
        )

    @fivetran_connector_last_sync_task_type.setter
    def fivetran_connector_last_sync_task_type(
        self, fivetran_connector_last_sync_task_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_task_type = (
            fivetran_connector_last_sync_task_type
        )

    @property
    def fivetran_connector_last_sync_rescheduled_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_rescheduled_at
        )

    @fivetran_connector_last_sync_rescheduled_at.setter
    def fivetran_connector_last_sync_rescheduled_at(
        self, fivetran_connector_last_sync_rescheduled_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_rescheduled_at = (
            fivetran_connector_last_sync_rescheduled_at
        )

    @property
    def fivetran_connector_last_sync_tables_synced(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_tables_synced
        )

    @fivetran_connector_last_sync_tables_synced.setter
    def fivetran_connector_last_sync_tables_synced(
        self, fivetran_connector_last_sync_tables_synced: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_tables_synced = (
            fivetran_connector_last_sync_tables_synced
        )

    @property
    def fivetran_connector_last_sync_extract_time_seconds(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_extract_time_seconds
        )

    @fivetran_connector_last_sync_extract_time_seconds.setter
    def fivetran_connector_last_sync_extract_time_seconds(
        self, fivetran_connector_last_sync_extract_time_seconds: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_extract_time_seconds = (
            fivetran_connector_last_sync_extract_time_seconds
        )

    @property
    def fivetran_connector_last_sync_extract_volume_megabytes(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_extract_volume_megabytes
        )

    @fivetran_connector_last_sync_extract_volume_megabytes.setter
    def fivetran_connector_last_sync_extract_volume_megabytes(
        self, fivetran_connector_last_sync_extract_volume_megabytes: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_extract_volume_megabytes = (
            fivetran_connector_last_sync_extract_volume_megabytes
        )

    @property
    def fivetran_connector_last_sync_load_time_seconds(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_load_time_seconds
        )

    @fivetran_connector_last_sync_load_time_seconds.setter
    def fivetran_connector_last_sync_load_time_seconds(
        self, fivetran_connector_last_sync_load_time_seconds: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_load_time_seconds = (
            fivetran_connector_last_sync_load_time_seconds
        )

    @property
    def fivetran_connector_last_sync_load_volume_megabytes(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_load_volume_megabytes
        )

    @fivetran_connector_last_sync_load_volume_megabytes.setter
    def fivetran_connector_last_sync_load_volume_megabytes(
        self, fivetran_connector_last_sync_load_volume_megabytes: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_load_volume_megabytes = (
            fivetran_connector_last_sync_load_volume_megabytes
        )

    @property
    def fivetran_connector_last_sync_process_time_seconds(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_process_time_seconds
        )

    @fivetran_connector_last_sync_process_time_seconds.setter
    def fivetran_connector_last_sync_process_time_seconds(
        self, fivetran_connector_last_sync_process_time_seconds: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_process_time_seconds = (
            fivetran_connector_last_sync_process_time_seconds
        )

    @property
    def fivetran_connector_last_sync_process_volume_megabytes(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_process_volume_megabytes
        )

    @fivetran_connector_last_sync_process_volume_megabytes.setter
    def fivetran_connector_last_sync_process_volume_megabytes(
        self, fivetran_connector_last_sync_process_volume_megabytes: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_process_volume_megabytes = (
            fivetran_connector_last_sync_process_volume_megabytes
        )

    @property
    def fivetran_connector_last_sync_total_time_seconds(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_last_sync_total_time_seconds
        )

    @fivetran_connector_last_sync_total_time_seconds.setter
    def fivetran_connector_last_sync_total_time_seconds(
        self, fivetran_connector_last_sync_total_time_seconds: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_last_sync_total_time_seconds = (
            fivetran_connector_last_sync_total_time_seconds
        )

    @property
    def fivetran_connector_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.fivetran_connector_name
        )

    @fivetran_connector_name.setter
    def fivetran_connector_name(self, fivetran_connector_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_name = fivetran_connector_name

    @property
    def fivetran_connector_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.fivetran_connector_type
        )

    @fivetran_connector_type.setter
    def fivetran_connector_type(self, fivetran_connector_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_type = fivetran_connector_type

    @property
    def fivetran_connector_url(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.fivetran_connector_url
        )

    @fivetran_connector_url.setter
    def fivetran_connector_url(self, fivetran_connector_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_url = fivetran_connector_url

    @property
    def fivetran_connector_destination_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_destination_name
        )

    @fivetran_connector_destination_name.setter
    def fivetran_connector_destination_name(
        self, fivetran_connector_destination_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_destination_name = (
            fivetran_connector_destination_name
        )

    @property
    def fivetran_connector_destination_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_destination_type
        )

    @fivetran_connector_destination_type.setter
    def fivetran_connector_destination_type(
        self, fivetran_connector_destination_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_destination_type = (
            fivetran_connector_destination_type
        )

    @property
    def fivetran_connector_destination_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_destination_url
        )

    @fivetran_connector_destination_url.setter
    def fivetran_connector_destination_url(
        self, fivetran_connector_destination_url: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_destination_url = (
            fivetran_connector_destination_url
        )

    @property
    def fivetran_connector_sync_setup_on(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_sync_setup_on
        )

    @fivetran_connector_sync_setup_on.setter
    def fivetran_connector_sync_setup_on(
        self, fivetran_connector_sync_setup_on: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_sync_setup_on = (
            fivetran_connector_sync_setup_on
        )

    @property
    def fivetran_connector_sync_frequency(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_sync_frequency
        )

    @fivetran_connector_sync_frequency.setter
    def fivetran_connector_sync_frequency(
        self, fivetran_connector_sync_frequency: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_sync_frequency = (
            fivetran_connector_sync_frequency
        )

    @property
    def fivetran_connector_sync_paused(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_sync_paused
        )

    @fivetran_connector_sync_paused.setter
    def fivetran_connector_sync_paused(
        self, fivetran_connector_sync_paused: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_sync_paused = fivetran_connector_sync_paused

    @property
    def fivetran_connector_sync_setup_user_full_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_sync_setup_user_full_name
        )

    @fivetran_connector_sync_setup_user_full_name.setter
    def fivetran_connector_sync_setup_user_full_name(
        self, fivetran_connector_sync_setup_user_full_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_sync_setup_user_full_name = (
            fivetran_connector_sync_setup_user_full_name
        )

    @property
    def fivetran_connector_sync_setup_user_email(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_sync_setup_user_email
        )

    @fivetran_connector_sync_setup_user_email.setter
    def fivetran_connector_sync_setup_user_email(
        self, fivetran_connector_sync_setup_user_email: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_sync_setup_user_email = (
            fivetran_connector_sync_setup_user_email
        )

    @property
    def fivetran_connector_monthly_active_rows_free(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_free
        )

    @fivetran_connector_monthly_active_rows_free.setter
    def fivetran_connector_monthly_active_rows_free(
        self, fivetran_connector_monthly_active_rows_free: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_free = (
            fivetran_connector_monthly_active_rows_free
        )

    @property
    def fivetran_connector_monthly_active_rows_paid(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_paid
        )

    @fivetran_connector_monthly_active_rows_paid.setter
    def fivetran_connector_monthly_active_rows_paid(
        self, fivetran_connector_monthly_active_rows_paid: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_paid = (
            fivetran_connector_monthly_active_rows_paid
        )

    @property
    def fivetran_connector_monthly_active_rows_total(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_total
        )

    @fivetran_connector_monthly_active_rows_total.setter
    def fivetran_connector_monthly_active_rows_total(
        self, fivetran_connector_monthly_active_rows_total: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_total = (
            fivetran_connector_monthly_active_rows_total
        )

    @property
    def fivetran_connector_monthly_active_rows_change_percentage_free(
        self,
    ) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_change_percentage_free
        )

    @fivetran_connector_monthly_active_rows_change_percentage_free.setter
    def fivetran_connector_monthly_active_rows_change_percentage_free(
        self,
        fivetran_connector_monthly_active_rows_change_percentage_free: Optional[float],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_change_percentage_free = (
            fivetran_connector_monthly_active_rows_change_percentage_free
        )

    @property
    def fivetran_connector_monthly_active_rows_change_percentage_paid(
        self,
    ) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_change_percentage_paid
        )

    @fivetran_connector_monthly_active_rows_change_percentage_paid.setter
    def fivetran_connector_monthly_active_rows_change_percentage_paid(
        self,
        fivetran_connector_monthly_active_rows_change_percentage_paid: Optional[float],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_change_percentage_paid = (
            fivetran_connector_monthly_active_rows_change_percentage_paid
        )

    @property
    def fivetran_connector_monthly_active_rows_change_percentage_total(
        self,
    ) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_change_percentage_total
        )

    @fivetran_connector_monthly_active_rows_change_percentage_total.setter
    def fivetran_connector_monthly_active_rows_change_percentage_total(
        self,
        fivetran_connector_monthly_active_rows_change_percentage_total: Optional[float],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_change_percentage_total = (
            fivetran_connector_monthly_active_rows_change_percentage_total
        )

    @property
    def fivetran_connector_monthly_active_rows_free_percentage_of_account(
        self,
    ) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_free_percentage_of_account
        )

    @fivetran_connector_monthly_active_rows_free_percentage_of_account.setter
    def fivetran_connector_monthly_active_rows_free_percentage_of_account(
        self,
        fivetran_connector_monthly_active_rows_free_percentage_of_account: Optional[
            float
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_free_percentage_of_account = (
            fivetran_connector_monthly_active_rows_free_percentage_of_account
        )

    @property
    def fivetran_connector_monthly_active_rows_paid_percentage_of_account(
        self,
    ) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_paid_percentage_of_account
        )

    @fivetran_connector_monthly_active_rows_paid_percentage_of_account.setter
    def fivetran_connector_monthly_active_rows_paid_percentage_of_account(
        self,
        fivetran_connector_monthly_active_rows_paid_percentage_of_account: Optional[
            float
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_paid_percentage_of_account = (
            fivetran_connector_monthly_active_rows_paid_percentage_of_account
        )

    @property
    def fivetran_connector_monthly_active_rows_total_percentage_of_account(
        self,
    ) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_monthly_active_rows_total_percentage_of_account
        )

    @fivetran_connector_monthly_active_rows_total_percentage_of_account.setter
    def fivetran_connector_monthly_active_rows_total_percentage_of_account(
        self,
        fivetran_connector_monthly_active_rows_total_percentage_of_account: Optional[
            float
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_monthly_active_rows_total_percentage_of_account = (
            fivetran_connector_monthly_active_rows_total_percentage_of_account
        )

    @property
    def fivetran_connector_total_tables_synced(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_total_tables_synced
        )

    @fivetran_connector_total_tables_synced.setter
    def fivetran_connector_total_tables_synced(
        self, fivetran_connector_total_tables_synced: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_total_tables_synced = (
            fivetran_connector_total_tables_synced
        )

    @property
    def fivetran_connector_top_tables_by_m_a_r(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_top_tables_by_m_a_r
        )

    @fivetran_connector_top_tables_by_m_a_r.setter
    def fivetran_connector_top_tables_by_m_a_r(
        self, fivetran_connector_top_tables_by_m_a_r: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_top_tables_by_m_a_r = (
            fivetran_connector_top_tables_by_m_a_r
        )

    @property
    def fivetran_connector_usage_cost(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_usage_cost
        )

    @fivetran_connector_usage_cost.setter
    def fivetran_connector_usage_cost(
        self, fivetran_connector_usage_cost: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_usage_cost = fivetran_connector_usage_cost

    @property
    def fivetran_connector_credits_used(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.fivetran_connector_credits_used
        )

    @fivetran_connector_credits_used.setter
    def fivetran_connector_credits_used(
        self, fivetran_connector_credits_used: Optional[float]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector_credits_used = (
            fivetran_connector_credits_used
        )

    @property
    def processes(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.processes

    @processes.setter
    def processes(self, processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.processes = processes

    class Attributes(Fivetran.Attributes):
        fivetran_connector_last_sync_id: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_finished_at: Optional[datetime] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_reason: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_task_type: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_rescheduled_at: Optional[datetime] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_tables_synced: Optional[int] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_extract_time_seconds: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_extract_volume_megabytes: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_load_time_seconds: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_load_volume_megabytes: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_process_time_seconds: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_process_volume_megabytes: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_last_sync_total_time_seconds: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_name: Optional[str] = Field(default=None, description="")
        fivetran_connector_type: Optional[str] = Field(default=None, description="")
        fivetran_connector_url: Optional[str] = Field(default=None, description="")
        fivetran_connector_destination_name: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_destination_type: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_destination_url: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_sync_setup_on: Optional[datetime] = Field(
            default=None, description=""
        )
        fivetran_connector_sync_frequency: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_sync_paused: Optional[bool] = Field(
            default=None, description=""
        )
        fivetran_connector_sync_setup_user_full_name: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_sync_setup_user_email: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_monthly_active_rows_free: Optional[int] = Field(
            default=None, description=""
        )
        fivetran_connector_monthly_active_rows_paid: Optional[int] = Field(
            default=None, description=""
        )
        fivetran_connector_monthly_active_rows_total: Optional[int] = Field(
            default=None, description=""
        )
        fivetran_connector_monthly_active_rows_change_percentage_free: Optional[
            float
        ] = Field(default=None, description="")
        fivetran_connector_monthly_active_rows_change_percentage_paid: Optional[
            float
        ] = Field(default=None, description="")
        fivetran_connector_monthly_active_rows_change_percentage_total: Optional[
            float
        ] = Field(default=None, description="")
        fivetran_connector_monthly_active_rows_free_percentage_of_account: Optional[
            float
        ] = Field(default=None, description="")
        fivetran_connector_monthly_active_rows_paid_percentage_of_account: Optional[
            float
        ] = Field(default=None, description="")
        fivetran_connector_monthly_active_rows_total_percentage_of_account: Optional[
            float
        ] = Field(default=None, description="")
        fivetran_connector_total_tables_synced: Optional[int] = Field(
            default=None, description=""
        )
        fivetran_connector_top_tables_by_m_a_r: Optional[str] = Field(
            default=None, description=""
        )
        fivetran_connector_usage_cost: Optional[float] = Field(
            default=None, description=""
        )
        fivetran_connector_credits_used: Optional[float] = Field(
            default=None, description=""
        )
        processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: FivetranConnector.Attributes = Field(
        default_factory=lambda: FivetranConnector.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .process import Process  # noqa
