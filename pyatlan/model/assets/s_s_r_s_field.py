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


class SSRSField(SSRS):
    """Description"""

    type_name: str = Field(default="SSRSField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SSRSField":
            raise ValueError("must be SSRSField")
        return v

    def __setattr__(self, name, value):
        if name in SSRSField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SSRS_FIELD_DATATYPE: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldDatatype", "ssrsFieldDatatype"
    )
    """
    Data type of the field.
    """
    SSRS_FIELD_FUNCTION: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldFunction", "ssrsFieldFunction"
    )
    """
    Function applied to the field.
    """
    SSRS_FIELD_CALCULATED_FIELD: ClassVar[BooleanField] = BooleanField(
        "ssrsFieldCalculatedField", "ssrsFieldCalculatedField"
    )
    """
    Whether the field is calculated.
    """
    SSRS_FIELD_DATABASE_FIELD: ClassVar[BooleanField] = BooleanField(
        "ssrsFieldDatabaseField", "ssrsFieldDatabaseField"
    )
    """
    Whether the field is a database field.
    """
    SSRS_FIELD_REFERENCED_COLUMN_NAMES: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldReferencedColumnNames", "ssrsFieldReferencedColumnNames"
    )
    """
    Referenced column names for the field.
    """
    SSRS_FIELD_SQL_TRANSFORM_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldSqlTransformExpression", "ssrsFieldSqlTransformExpression"
    )
    """
    SQL transform expression for the field.
    """
    SSRS_FIELD_ORDINAL_POSITION: ClassVar[NumericField] = NumericField(
        "ssrsFieldOrdinalPosition", "ssrsFieldOrdinalPosition"
    )
    """
    Ordinal position of the field.
    """
    SSRS_FIELD_LOG_MESSAGES: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldLogMessages", "ssrsFieldLogMessages"
    )
    """
    Log messages for the field.
    """
    SSRS_FIELD_ERROR_CODE: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldErrorCode", "ssrsFieldErrorCode"
    )
    """
    Error code for the field.
    """
    SSRS_FIELD_REPORT_SOURCE: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldReportSource", "ssrsFieldReportSource"
    )
    """
    Report source for the field.
    """
    SSRS_FIELD_DATA_GROUP: ClassVar[KeywordField] = KeywordField(
        "ssrsFieldDataGroup", "ssrsFieldDataGroup"
    )
    """
    Data group for the field.
    """
    SSRS_FIELD_CONNECTED: ClassVar[BooleanField] = BooleanField(
        "ssrsFieldConnected", "ssrsFieldConnected"
    )
    """
    Whether the field is connected.
    """

    SSRS_DATA_SET: ClassVar[RelationField] = RelationField("ssrsDataSet")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ssrs_field_datatype",
        "ssrs_field_function",
        "ssrs_field_calculated_field",
        "ssrs_field_database_field",
        "ssrs_field_referenced_column_names",
        "ssrs_field_sql_transform_expression",
        "ssrs_field_ordinal_position",
        "ssrs_field_log_messages",
        "ssrs_field_error_code",
        "ssrs_field_report_source",
        "ssrs_field_data_group",
        "ssrs_field_connected",
        "ssrs_data_set",
    ]

    @property
    def ssrs_field_datatype(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_field_datatype

    @ssrs_field_datatype.setter
    def ssrs_field_datatype(self, ssrs_field_datatype: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_datatype = ssrs_field_datatype

    @property
    def ssrs_field_function(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ssrs_field_function

    @ssrs_field_function.setter
    def ssrs_field_function(self, ssrs_field_function: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_function = ssrs_field_function

    @property
    def ssrs_field_calculated_field(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_field_calculated_field
        )

    @ssrs_field_calculated_field.setter
    def ssrs_field_calculated_field(self, ssrs_field_calculated_field: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_calculated_field = ssrs_field_calculated_field

    @property
    def ssrs_field_database_field(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_field_database_field
        )

    @ssrs_field_database_field.setter
    def ssrs_field_database_field(self, ssrs_field_database_field: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_database_field = ssrs_field_database_field

    @property
    def ssrs_field_referenced_column_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_field_referenced_column_names
        )

    @ssrs_field_referenced_column_names.setter
    def ssrs_field_referenced_column_names(
        self, ssrs_field_referenced_column_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_referenced_column_names = (
            ssrs_field_referenced_column_names
        )

    @property
    def ssrs_field_sql_transform_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_field_sql_transform_expression
        )

    @ssrs_field_sql_transform_expression.setter
    def ssrs_field_sql_transform_expression(
        self, ssrs_field_sql_transform_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_sql_transform_expression = (
            ssrs_field_sql_transform_expression
        )

    @property
    def ssrs_field_ordinal_position(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_field_ordinal_position
        )

    @ssrs_field_ordinal_position.setter
    def ssrs_field_ordinal_position(self, ssrs_field_ordinal_position: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_ordinal_position = ssrs_field_ordinal_position

    @property
    def ssrs_field_log_messages(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ssrs_field_log_messages
        )

    @ssrs_field_log_messages.setter
    def ssrs_field_log_messages(self, ssrs_field_log_messages: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_log_messages = ssrs_field_log_messages

    @property
    def ssrs_field_error_code(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ssrs_field_error_code
        )

    @ssrs_field_error_code.setter
    def ssrs_field_error_code(self, ssrs_field_error_code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_error_code = ssrs_field_error_code

    @property
    def ssrs_field_report_source(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.ssrs_field_report_source
        )

    @ssrs_field_report_source.setter
    def ssrs_field_report_source(self, ssrs_field_report_source: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_report_source = ssrs_field_report_source

    @property
    def ssrs_field_data_group(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ssrs_field_data_group
        )

    @ssrs_field_data_group.setter
    def ssrs_field_data_group(self, ssrs_field_data_group: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_data_group = ssrs_field_data_group

    @property
    def ssrs_field_connected(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.ssrs_field_connected

    @ssrs_field_connected.setter
    def ssrs_field_connected(self, ssrs_field_connected: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_field_connected = ssrs_field_connected

    @property
    def ssrs_data_set(self) -> Optional[SSRSDataSet]:
        return None if self.attributes is None else self.attributes.ssrs_data_set

    @ssrs_data_set.setter
    def ssrs_data_set(self, ssrs_data_set: Optional[SSRSDataSet]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ssrs_data_set = ssrs_data_set

    class Attributes(SSRS.Attributes):
        ssrs_field_datatype: Optional[str] = Field(default=None, description="")
        ssrs_field_function: Optional[str] = Field(default=None, description="")
        ssrs_field_calculated_field: Optional[bool] = Field(
            default=None, description=""
        )
        ssrs_field_database_field: Optional[bool] = Field(default=None, description="")
        ssrs_field_referenced_column_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        ssrs_field_sql_transform_expression: Optional[str] = Field(
            default=None, description=""
        )
        ssrs_field_ordinal_position: Optional[int] = Field(default=None, description="")
        ssrs_field_log_messages: Optional[str] = Field(default=None, description="")
        ssrs_field_error_code: Optional[str] = Field(default=None, description="")
        ssrs_field_report_source: Optional[str] = Field(default=None, description="")
        ssrs_field_data_group: Optional[str] = Field(default=None, description="")
        ssrs_field_connected: Optional[bool] = Field(default=None, description="")
        ssrs_data_set: Optional[SSRSDataSet] = Field(
            default=None, description=""
        )  # relationship

    attributes: SSRSField.Attributes = Field(
        default_factory=lambda: SSRSField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .s_s_r_s_data_set import SSRSDataSet  # noqa: E402, F401

SSRSField.Attributes.update_forward_refs()
