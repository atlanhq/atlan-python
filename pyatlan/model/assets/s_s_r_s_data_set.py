# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)

from .s_s_r_s import SSRS


class SSRSDataSet(SSRS):
    """Description"""

    type_name: str = Field(default="SSRSDataSet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SSRSDataSet":
            raise ValueError("must be SSRSDataSet")
        return v

    def __setattr__(self, name, value):
        if name in SSRSDataSet._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SSRS_DATA_SET_SQL_QUERY: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetSqlQuery", "ssrsDataSetSqlQuery"
    )
    """
    SQL query for the data set.
    """
    SSRS_DATA_SET_IS_SHARED_DATA_SET: ClassVar[BooleanField] = BooleanField(
        "ssrsDataSetIsSharedDataSet", "ssrsDataSetIsSharedDataSet"
    )
    """
    Whether the data set is shared.
    """
    SSRS_DATA_SET_QUERY_PARAMETERS: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetQueryParameters", "ssrsDataSetQueryParameters"
    )
    """
    Query parameters for the data set.
    """
    SSRS_DATA_SET_DATA_SOURCE_CONNECTION_STRING: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetDataSourceConnectionString", "ssrsDataSetDataSourceConnectionString"
    )
    """
    Data source connection string for the data set.
    """
    SSRS_DATA_SET_DATA_SOURCE_REFERENCE: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetDataSourceReference", "ssrsDataSetDataSourceReference"
    )
    """
    Data source reference for the data set.
    """
    SSRS_DATA_SET_EXTENSION: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetExtension", "ssrsDataSetExtension"
    )
    """
    Extension for the data set.
    """
    SSRS_DATA_SET_REFERENCE_TABLE_NAMES: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetReferenceTableNames", "ssrsDataSetReferenceTableNames"
    )
    """
    Reference table names for the data set.
    """
    SSRS_DATA_SET_CUBE_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetCubeName", "ssrsDataSetCubeName"
    )
    """
    Cube name for the data set.
    """
    SSRS_DATA_SET_STORED_PROCEDURE_NAME: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetStoredProcedureName", "ssrsDataSetStoredProcedureName"
    )
    """
    Stored procedure name for the data set.
    """
    SSRS_DATA_SET_PROCESSED_SQL: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetProcessedSql", "ssrsDataSetProcessedSql"
    )
    """
    Processed SQL for the data set.
    """
    SSRS_DATA_SET_LOG_MESSAGES: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetLogMessages", "ssrsDataSetLogMessages"
    )
    """
    Log messages for the data set.
    """
    SSRS_DATA_SET_ERROR_CODE: ClassVar[KeywordField] = KeywordField(
        "ssrsDataSetErrorCode", "ssrsDataSetErrorCode"
    )
    """
    Error code for the data set.
    """
    SSRS_DATA_SET_CONNECTED: ClassVar[BooleanField] = BooleanField(
        "ssrsDataSetConnected", "ssrsDataSetConnected"
    )
    """
    Whether the data set is connected.
    """
    SSRS_DATA_SET_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "ssrsDataSetFieldCount", "ssrsDataSetFieldCount"
    )
    """
    Number of fields in this dataset.
    """

    SSRS_FIELDS: ClassVar[RelationField] = RelationField("ssrsFields")
    """
    TBC
    """
    SSRS_REPORT: ClassVar[RelationField] = RelationField("ssrsReport")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ssrs_data_set_sql_query",
        "ssrs_data_set_is_shared_data_set",
        "ssrs_data_set_query_parameters",
        "ssrs_data_set_data_source_connection_string",
        "ssrs_data_set_data_source_reference",
        "ssrs_data_set_extension",
        "ssrs_data_set_reference_table_names",
        "ssrs_data_set_cube_name",
        "ssrs_data_set_stored_procedure_name",
        "ssrs_data_set_processed_sql",
        "ssrs_data_set_log_messages",
        "ssrs_data_set_error_code",
        "ssrs_data_set_connected",
        "ssrs_data_set_field_count",
        "ssrs_fields",
        "ssrs_report",
    ]

    @property
    def ssrs_data_set_sql_query(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ssrs_data_set_sql_query
        )

    @ssrs_data_set_sql_query.setter
    def ssrs_data_set_sql_query(self, ssrs_data_set_sql_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_sql_query = ssrs_data_set_sql_query

    @property
    def ssrs_data_set_is_shared_data_set(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_is_shared_data_set
        )

    @ssrs_data_set_is_shared_data_set.setter
    def ssrs_data_set_is_shared_data_set(
        self, ssrs_data_set_is_shared_data_set: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_is_shared_data_set = (
            ssrs_data_set_is_shared_data_set
        )

    @property
    def ssrs_data_set_query_parameters(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_query_parameters
        )

    @ssrs_data_set_query_parameters.setter
    def ssrs_data_set_query_parameters(
        self, ssrs_data_set_query_parameters: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_query_parameters = ssrs_data_set_query_parameters

    @property
    def ssrs_data_set_data_source_connection_string(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_data_source_connection_string
        )

    @ssrs_data_set_data_source_connection_string.setter
    def ssrs_data_set_data_source_connection_string(
        self, ssrs_data_set_data_source_connection_string: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_data_source_connection_string = (
            ssrs_data_set_data_source_connection_string
        )

    @property
    def ssrs_data_set_data_source_reference(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_data_source_reference
        )

    @ssrs_data_set_data_source_reference.setter
    def ssrs_data_set_data_source_reference(
        self, ssrs_data_set_data_source_reference: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_data_source_reference = (
            ssrs_data_set_data_source_reference
        )

    @property
    def ssrs_data_set_extension(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ssrs_data_set_extension
        )

    @ssrs_data_set_extension.setter
    def ssrs_data_set_extension(self, ssrs_data_set_extension: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_extension = ssrs_data_set_extension

    @property
    def ssrs_data_set_reference_table_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_reference_table_names
        )

    @ssrs_data_set_reference_table_names.setter
    def ssrs_data_set_reference_table_names(
        self, ssrs_data_set_reference_table_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_reference_table_names = (
            ssrs_data_set_reference_table_names
        )

    @property
    def ssrs_data_set_cube_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ssrs_data_set_cube_name
        )

    @ssrs_data_set_cube_name.setter
    def ssrs_data_set_cube_name(self, ssrs_data_set_cube_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_cube_name = ssrs_data_set_cube_name

    @property
    def ssrs_data_set_stored_procedure_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_stored_procedure_name
        )

    @ssrs_data_set_stored_procedure_name.setter
    def ssrs_data_set_stored_procedure_name(
        self, ssrs_data_set_stored_procedure_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_stored_procedure_name = (
            ssrs_data_set_stored_procedure_name
        )

    @property
    def ssrs_data_set_processed_sql(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_processed_sql
        )

    @ssrs_data_set_processed_sql.setter
    def ssrs_data_set_processed_sql(self, ssrs_data_set_processed_sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_processed_sql = ssrs_data_set_processed_sql

    @property
    def ssrs_data_set_log_messages(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_log_messages
        )

    @ssrs_data_set_log_messages.setter
    def ssrs_data_set_log_messages(self, ssrs_data_set_log_messages: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_log_messages = ssrs_data_set_log_messages

    @property
    def ssrs_data_set_error_code(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_error_code
        )

    @ssrs_data_set_error_code.setter
    def ssrs_data_set_error_code(self, ssrs_data_set_error_code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_error_code = ssrs_data_set_error_code

    @property
    def ssrs_data_set_connected(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.ssrs_data_set_connected
        )

    @ssrs_data_set_connected.setter
    def ssrs_data_set_connected(self, ssrs_data_set_connected: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_connected = ssrs_data_set_connected

    @property
    def ssrs_data_set_field_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_data_set_field_count
        )

    @ssrs_data_set_field_count.setter
    def ssrs_data_set_field_count(self, ssrs_data_set_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set_field_count = ssrs_data_set_field_count

    @property
    def ssrs_fields(self) -> Optional[List[SSRSField]]:
        return None if self.attributes is None else self.attributes.ssrs_fields

    @ssrs_fields.setter
    def ssrs_fields(self, ssrs_fields: Optional[List[SSRSField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_fields = ssrs_fields

    @property
    def ssrs_report(self) -> Optional[SSRSReport]:
        return None if self.attributes is None else self.attributes.ssrs_report

    @ssrs_report.setter
    def ssrs_report(self, ssrs_report: Optional[SSRSReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_report = ssrs_report

    class Attributes(SSRS.Attributes):
        ssrs_data_set_sql_query: Optional[str] = Field(default=None, description="")
        ssrs_data_set_is_shared_data_set: Optional[bool] = Field(
            default=None, description=""
        )
        ssrs_data_set_query_parameters: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_data_set_data_source_connection_string: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_data_set_data_source_reference: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_data_set_extension: Optional[str] = Field(default=None, description="")
        ssrs_data_set_reference_table_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        ssrs_data_set_cube_name: Optional[str] = Field(default=None, description="")
        ssrs_data_set_stored_procedure_name: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_data_set_processed_sql: Optional[str] = Field(default=None, description="")
        ssrs_data_set_log_messages: Optional[str] = Field(default=None, description="")
        ssrs_data_set_error_code: Optional[str] = Field(default=None, description="")
        ssrs_data_set_connected: Optional[bool] = Field(default=None, description="")
        ssrs_data_set_field_count: Optional[int] = Field(default=None, description="")
        ssrs_fields: Optional[List[SSRSField]] = Field(
            default=None, description=""
        )  # relationship
        ssrs_report: Optional[SSRSReport] = Field(
            default=None, description=""
        )  # relationship

    attributes: SSRSDataSet.Attributes = Field(
        default_factory=lambda: SSRSDataSet.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_s_r_s_field import SSRSField  # noqa: E402, F401
from .s_s_r_s_report import SSRSReport  # noqa: E402, F401

SSRSDataSet.Attributes.update_forward_refs()
