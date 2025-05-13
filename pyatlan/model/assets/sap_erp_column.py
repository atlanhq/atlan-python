# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .s_a_p import SAP


class SapErpColumn(SAP):
    """Description"""

    type_name: str = Field(default="SapErpColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SapErpColumn":
            raise ValueError("must be SapErpColumn")
        return v

    def __setattr__(self, name, value):
        if name in SapErpColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SAP_ERP_COLUMN_DATA_ELEMENT: ClassVar[KeywordField] = KeywordField(
        "sapErpColumnDataElement", "sapErpColumnDataElement"
    )
    """
    Represents the SAP ERP data element, providing semantic information about the column.
    """
    SAP_ERP_COLUMN_LOGICAL_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "sapErpColumnLogicalDataType", "sapErpColumnLogicalDataType"
    )
    """
    Specifies the logical data type of values in this SAP ERP column
    """
    SAP_ERP_COLUMN_LENGTH: ClassVar[KeywordField] = KeywordField(
        "sapErpColumnLength", "sapErpColumnLength"
    )
    """
    Indicates the maximum length of the values that the SAP ERP column can store.
    """
    SAP_ERP_COLUMN_DECIMALS: ClassVar[KeywordField] = KeywordField(
        "sapErpColumnDecimals", "sapErpColumnDecimals"
    )
    """
    Defines the number of decimal places allowed for numeric values in the SAP ERP column.
    """
    SAP_ERP_COLUMN_IS_PRIMARY: ClassVar[BooleanField] = BooleanField(
        "sapErpColumnIsPrimary", "sapErpColumnIsPrimary"
    )
    """
    When true, this column is the primary key for the SAP ERP table or view.
    """
    SAP_ERP_COLUMN_IS_FOREIGN: ClassVar[BooleanField] = BooleanField(
        "sapErpColumnIsForeign", "sapErpColumnIsForeign"
    )
    """
    When true, this column is the foreign key for the SAP ERP table or view.
    """
    SAP_ERP_COLUMN_IS_MANDATORY: ClassVar[BooleanField] = BooleanField(
        "sapErpColumnIsMandatory", "sapErpColumnIsMandatory"
    )
    """
    When true, the values in this column can be null.
    """
    SAP_ERP_TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sapErpTableName", "sapErpTableName.keyword", "sapErpTableName"
    )
    """
    Simple name of the SAP ERP table in which this column asset exists.
    """
    SAP_ERP_TABLE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sapErpTableQualifiedName",
        "sapErpTableQualifiedName",
        "sapErpTableQualifiedName.text",
    )
    """
    Unique name of the SAP ERP table in which this SQL asset exists.
    """
    SAP_ERP_VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sapErpViewName", "sapErpViewName.keyword", "sapErpViewName"
    )
    """
    Simple name of the SAP ERP view in which this column asset exists.
    """
    SAP_ERP_VIEW_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sapErpViewQualifiedName",
        "sapErpViewQualifiedName",
        "sapErpViewQualifiedName.text",
    )
    """
    Unique name of the SAP ERP view in which this column asset exists.
    """
    SAP_ERP_CDS_VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sapErpCdsViewName", "sapErpCdsViewName.keyword", "sapErpCdsViewName"
    )
    """
    Simple name of the SAP ERP CDS view in which this column asset exists.
    """
    SAP_ERP_CDS_VIEW_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sapErpCdsViewQualifiedName",
        "sapErpCdsViewQualifiedName",
        "sapErpCdsViewQualifiedName.text",
    )
    """
    Unique name of the SAP ERP CDS view in which this column asset exists.
    """
    SAP_TECHNICAL_NAME: ClassVar[KeywordField] = KeywordField(
        "sapTechnicalName", "sapTechnicalName"
    )
    """
    Technical identifier for SAP data objects, used for integration and internal reference.
    """
    SAP_LOGICAL_NAME: ClassVar[KeywordField] = KeywordField(
        "sapLogicalName", "sapLogicalName"
    )
    """
    Logical, business-friendly identifier for SAP data objects, aligned with business terminology and concepts.
    """
    SAP_PACKAGE_NAME: ClassVar[KeywordField] = KeywordField(
        "sapPackageName", "sapPackageName"
    )
    """
    Name of the SAP package, representing a logical grouping of related SAP data objects.
    """
    SAP_COMPONENT_NAME: ClassVar[KeywordField] = KeywordField(
        "sapComponentName", "sapComponentName"
    )
    """
    Name of the SAP component, representing a specific functional area in SAP.
    """
    SAP_DATA_TYPE: ClassVar[KeywordField] = KeywordField("sapDataType", "sapDataType")
    """
    SAP-specific data types
    """
    SAP_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "sapFieldCount", "sapFieldCount"
    )
    """
    Represents the total number of fields, columns, or child assets present in a given SAP asset.
    """
    SAP_FIELD_ORDER: ClassVar[NumericField] = NumericField(
        "sapFieldOrder", "sapFieldOrder"
    )
    """
    Indicates the sequential position of a field, column, or child asset within its parent SAP asset, starting from 1.
    """
    QUERY_COUNT: ClassVar[NumericField] = NumericField("queryCount", "queryCount")
    """
    Number of times this asset has been queried.
    """
    QUERY_USER_COUNT: ClassVar[NumericField] = NumericField(
        "queryUserCount", "queryUserCount"
    )
    """
    Number of unique users who have queried this asset.
    """
    QUERY_USER_MAP: ClassVar[KeywordField] = KeywordField(
        "queryUserMap", "queryUserMap"
    )
    """
    Map of unique users who have queried this asset to the number of times they have queried it.
    """
    QUERY_COUNT_UPDATED_AT: ClassVar[NumericField] = NumericField(
        "queryCountUpdatedAt", "queryCountUpdatedAt"
    )
    """
    Time (epoch) at which the query count was last updated, in milliseconds.
    """
    DATABASE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "databaseName", "databaseName.keyword", "databaseName"
    )
    """
    Simple name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    DATABASE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "databaseQualifiedName", "databaseQualifiedName"
    )
    """
    Unique name of the database in which this SQL asset exists, or empty if it does not exist within a database.
    """
    SCHEMA_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "schemaName", "schemaName.keyword", "schemaName"
    )
    """
    Simple name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    SCHEMA_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaQualifiedName", "schemaQualifiedName"
    )
    """
    Unique name of the schema in which this SQL asset exists, or empty if it does not exist within a schema.
    """
    TABLE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableName", "tableName.keyword", "tableName"
    )
    """
    Simple name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    TABLE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "tableQualifiedName", "tableQualifiedName"
    )
    """
    Unique name of the table in which this SQL asset exists, or empty if it does not exist within a table.
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    Simple name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "viewQualifiedName", "viewQualifiedName"
    )
    """
    Unique name of the view in which this SQL asset exists, or empty if it does not exist within a view.
    """
    CALCULATION_VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "calculationViewName", "calculationViewName.keyword", "calculationViewName"
    )
    """
    Simple name of the calculation view in which this SQL asset exists, or empty if it does not exist within a calculation view.
    """  # noqa: E501
    CALCULATION_VIEW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "calculationViewQualifiedName", "calculationViewQualifiedName"
    )
    """
    Unique name of the calculation view in which this SQL asset exists, or empty if it does not exist within a calculation view.
    """  # noqa: E501
    IS_PROFILED: ClassVar[BooleanField] = BooleanField("isProfiled", "isProfiled")
    """
    Whether this asset has been profiled (true) or not (false).
    """
    LAST_PROFILED_AT: ClassVar[NumericField] = NumericField(
        "lastProfiledAt", "lastProfiledAt"
    )
    """
    Time (epoch) at which this asset was last profiled, in milliseconds.
    """

    DBT_SOURCES: ClassVar[RelationField] = RelationField("dbtSources")
    """
    TBC
    """
    SAP_ERP_TABLE: ClassVar[RelationField] = RelationField("sapErpTable")
    """
    TBC
    """
    SQL_DBT_MODELS: ClassVar[RelationField] = RelationField("sqlDbtModels")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    SQL_DBT_SOURCES: ClassVar[RelationField] = RelationField("sqlDBTSources")
    """
    TBC
    """
    DBT_MODELS: ClassVar[RelationField] = RelationField("dbtModels")
    """
    TBC
    """
    SAP_ERP_CDS_VIEW: ClassVar[RelationField] = RelationField("sapErpCdsView")
    """
    TBC
    """
    SAP_ERP_VIEW: ClassVar[RelationField] = RelationField("sapErpView")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sap_erp_column_data_element",
        "sap_erp_column_logical_data_type",
        "sap_erp_column_length",
        "sap_erp_column_decimals",
        "sap_erp_column_is_primary",
        "sap_erp_column_is_foreign",
        "sap_erp_column_is_mandatory",
        "sap_erp_table_name",
        "sap_erp_table_qualified_name",
        "sap_erp_view_name",
        "sap_erp_view_qualified_name",
        "sap_erp_cds_view_name",
        "sap_erp_cds_view_qualified_name",
        "sap_technical_name",
        "sap_logical_name",
        "sap_package_name",
        "sap_component_name",
        "sap_data_type",
        "sap_field_count",
        "sap_field_order",
        "query_count",
        "query_user_count",
        "query_user_map",
        "query_count_updated_at",
        "database_name",
        "database_qualified_name",
        "schema_name",
        "schema_qualified_name",
        "table_name",
        "table_qualified_name",
        "view_name",
        "view_qualified_name",
        "calculation_view_name",
        "calculation_view_qualified_name",
        "is_profiled",
        "last_profiled_at",
        "dbt_sources",
        "sap_erp_table",
        "sql_dbt_models",
        "dbt_tests",
        "sql_dbt_sources",
        "dbt_models",
        "sap_erp_cds_view",
        "sap_erp_view",
    ]

    @property
    def sap_erp_column_data_element(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_column_data_element
        )

    @sap_erp_column_data_element.setter
    def sap_erp_column_data_element(self, sap_erp_column_data_element: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_column_data_element = sap_erp_column_data_element

    @property
    def sap_erp_column_logical_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_column_logical_data_type
        )

    @sap_erp_column_logical_data_type.setter
    def sap_erp_column_logical_data_type(
        self, sap_erp_column_logical_data_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_column_logical_data_type = (
            sap_erp_column_logical_data_type
        )

    @property
    def sap_erp_column_length(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sap_erp_column_length
        )

    @sap_erp_column_length.setter
    def sap_erp_column_length(self, sap_erp_column_length: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_column_length = sap_erp_column_length

    @property
    def sap_erp_column_decimals(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sap_erp_column_decimals
        )

    @sap_erp_column_decimals.setter
    def sap_erp_column_decimals(self, sap_erp_column_decimals: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_column_decimals = sap_erp_column_decimals

    @property
    def sap_erp_column_is_primary(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_column_is_primary
        )

    @sap_erp_column_is_primary.setter
    def sap_erp_column_is_primary(self, sap_erp_column_is_primary: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_column_is_primary = sap_erp_column_is_primary

    @property
    def sap_erp_column_is_foreign(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_column_is_foreign
        )

    @sap_erp_column_is_foreign.setter
    def sap_erp_column_is_foreign(self, sap_erp_column_is_foreign: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_column_is_foreign = sap_erp_column_is_foreign

    @property
    def sap_erp_column_is_mandatory(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_column_is_mandatory
        )

    @sap_erp_column_is_mandatory.setter
    def sap_erp_column_is_mandatory(self, sap_erp_column_is_mandatory: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_column_is_mandatory = sap_erp_column_is_mandatory

    @property
    def sap_erp_table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_erp_table_name

    @sap_erp_table_name.setter
    def sap_erp_table_name(self, sap_erp_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_table_name = sap_erp_table_name

    @property
    def sap_erp_table_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_table_qualified_name
        )

    @sap_erp_table_qualified_name.setter
    def sap_erp_table_qualified_name(self, sap_erp_table_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_table_qualified_name = sap_erp_table_qualified_name

    @property
    def sap_erp_view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_erp_view_name

    @sap_erp_view_name.setter
    def sap_erp_view_name(self, sap_erp_view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_view_name = sap_erp_view_name

    @property
    def sap_erp_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_view_qualified_name
        )

    @sap_erp_view_qualified_name.setter
    def sap_erp_view_qualified_name(self, sap_erp_view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_view_qualified_name = sap_erp_view_qualified_name

    @property
    def sap_erp_cds_view_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sap_erp_cds_view_name
        )

    @sap_erp_cds_view_name.setter
    def sap_erp_cds_view_name(self, sap_erp_cds_view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_cds_view_name = sap_erp_cds_view_name

    @property
    def sap_erp_cds_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sap_erp_cds_view_qualified_name
        )

    @sap_erp_cds_view_qualified_name.setter
    def sap_erp_cds_view_qualified_name(
        self, sap_erp_cds_view_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_cds_view_qualified_name = (
            sap_erp_cds_view_qualified_name
        )

    @property
    def sap_technical_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_technical_name

    @sap_technical_name.setter
    def sap_technical_name(self, sap_technical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_technical_name = sap_technical_name

    @property
    def sap_logical_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_logical_name

    @sap_logical_name.setter
    def sap_logical_name(self, sap_logical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_logical_name = sap_logical_name

    @property
    def sap_package_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_package_name

    @sap_package_name.setter
    def sap_package_name(self, sap_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_package_name = sap_package_name

    @property
    def sap_component_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_component_name

    @sap_component_name.setter
    def sap_component_name(self, sap_component_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_component_name = sap_component_name

    @property
    def sap_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sap_data_type

    @sap_data_type.setter
    def sap_data_type(self, sap_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_data_type = sap_data_type

    @property
    def sap_field_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.sap_field_count

    @sap_field_count.setter
    def sap_field_count(self, sap_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_field_count = sap_field_count

    @property
    def sap_field_order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.sap_field_order

    @sap_field_order.setter
    def sap_field_order(self, sap_field_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_field_order = sap_field_order

    @property
    def query_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_count

    @query_count.setter
    def query_count(self, query_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count = query_count

    @property
    def query_user_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.query_user_count

    @query_user_count.setter
    def query_user_count(self, query_user_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_count = query_user_count

    @property
    def query_user_map(self) -> Optional[Dict[str, int]]:
        return None if self.attributes is None else self.attributes.query_user_map

    @query_user_map.setter
    def query_user_map(self, query_user_map: Optional[Dict[str, int]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_user_map = query_user_map

    @property
    def query_count_updated_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.query_count_updated_at
        )

    @query_count_updated_at.setter
    def query_count_updated_at(self, query_count_updated_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.query_count_updated_at = query_count_updated_at

    @property
    def database_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.database_name

    @database_name.setter
    def database_name(self, database_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_name = database_name

    @property
    def database_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.database_qualified_name
        )

    @database_qualified_name.setter
    def database_qualified_name(self, database_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.database_qualified_name = database_qualified_name

    @property
    def schema_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.schema_name

    @schema_name.setter
    def schema_name(self, schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_name = schema_name

    @property
    def schema_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.schema_qualified_name
        )

    @schema_qualified_name.setter
    def schema_qualified_name(self, schema_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_qualified_name = schema_qualified_name

    @property
    def table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_name

    @table_name.setter
    def table_name(self, table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_name = table_name

    @property
    def table_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.table_qualified_name

    @table_qualified_name.setter
    def table_qualified_name(self, table_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table_qualified_name = table_qualified_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def view_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_qualified_name

    @view_qualified_name.setter
    def view_qualified_name(self, view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_qualified_name = view_qualified_name

    @property
    def calculation_view_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.calculation_view_name
        )

    @calculation_view_name.setter
    def calculation_view_name(self, calculation_view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_name = calculation_view_name

    @property
    def calculation_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.calculation_view_qualified_name
        )

    @calculation_view_qualified_name.setter
    def calculation_view_qualified_name(
        self, calculation_view_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculation_view_qualified_name = (
            calculation_view_qualified_name
        )

    @property
    def is_profiled(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_profiled

    @is_profiled.setter
    def is_profiled(self, is_profiled: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_profiled = is_profiled

    @property
    def last_profiled_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.last_profiled_at

    @last_profiled_at.setter
    def last_profiled_at(self, last_profiled_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.last_profiled_at = last_profiled_at

    @property
    def dbt_sources(self) -> Optional[List[DbtSource]]:
        return None if self.attributes is None else self.attributes.dbt_sources

    @dbt_sources.setter
    def dbt_sources(self, dbt_sources: Optional[List[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_sources = dbt_sources

    @property
    def sap_erp_table(self) -> Optional[SapErpTable]:
        return None if self.attributes is None else self.attributes.sap_erp_table

    @sap_erp_table.setter
    def sap_erp_table(self, sap_erp_table: Optional[SapErpTable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_table = sap_erp_table

    @property
    def sql_dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.sql_dbt_models

    @sql_dbt_models.setter
    def sql_dbt_models(self, sql_dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_models = sql_dbt_models

    @property
    def dbt_tests(self) -> Optional[List[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[List[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def sql_dbt_sources(self) -> Optional[List[DbtSource]]:
        return None if self.attributes is None else self.attributes.sql_dbt_sources

    @sql_dbt_sources.setter
    def sql_dbt_sources(self, sql_dbt_sources: Optional[List[DbtSource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_dbt_sources = sql_dbt_sources

    @property
    def dbt_models(self) -> Optional[List[DbtModel]]:
        return None if self.attributes is None else self.attributes.dbt_models

    @dbt_models.setter
    def dbt_models(self, dbt_models: Optional[List[DbtModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_models = dbt_models

    @property
    def sap_erp_cds_view(self) -> Optional[SapErpCdsView]:
        return None if self.attributes is None else self.attributes.sap_erp_cds_view

    @sap_erp_cds_view.setter
    def sap_erp_cds_view(self, sap_erp_cds_view: Optional[SapErpCdsView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_cds_view = sap_erp_cds_view

    @property
    def sap_erp_view(self) -> Optional[SapErpView]:
        return None if self.attributes is None else self.attributes.sap_erp_view

    @sap_erp_view.setter
    def sap_erp_view(self, sap_erp_view: Optional[SapErpView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sap_erp_view = sap_erp_view

    class Attributes(SAP.Attributes):
        sap_erp_column_data_element: Optional[str] = Field(default=None, description="")
        sap_erp_column_logical_data_type: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_column_length: Optional[str] = Field(default=None, description="")
        sap_erp_column_decimals: Optional[str] = Field(default=None, description="")
        sap_erp_column_is_primary: Optional[bool] = Field(default=None, description="")
        sap_erp_column_is_foreign: Optional[bool] = Field(default=None, description="")
        sap_erp_column_is_mandatory: Optional[bool] = Field(
            default=None, description=""
        )
        sap_erp_table_name: Optional[str] = Field(default=None, description="")
        sap_erp_table_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_erp_view_name: Optional[str] = Field(default=None, description="")
        sap_erp_view_qualified_name: Optional[str] = Field(default=None, description="")
        sap_erp_cds_view_name: Optional[str] = Field(default=None, description="")
        sap_erp_cds_view_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sap_technical_name: Optional[str] = Field(default=None, description="")
        sap_logical_name: Optional[str] = Field(default=None, description="")
        sap_package_name: Optional[str] = Field(default=None, description="")
        sap_component_name: Optional[str] = Field(default=None, description="")
        sap_data_type: Optional[str] = Field(default=None, description="")
        sap_field_count: Optional[int] = Field(default=None, description="")
        sap_field_order: Optional[int] = Field(default=None, description="")
        query_count: Optional[int] = Field(default=None, description="")
        query_user_count: Optional[int] = Field(default=None, description="")
        query_user_map: Optional[Dict[str, int]] = Field(default=None, description="")
        query_count_updated_at: Optional[datetime] = Field(default=None, description="")
        database_name: Optional[str] = Field(default=None, description="")
        database_qualified_name: Optional[str] = Field(default=None, description="")
        schema_name: Optional[str] = Field(default=None, description="")
        schema_qualified_name: Optional[str] = Field(default=None, description="")
        table_name: Optional[str] = Field(default=None, description="")
        table_qualified_name: Optional[str] = Field(default=None, description="")
        view_name: Optional[str] = Field(default=None, description="")
        view_qualified_name: Optional[str] = Field(default=None, description="")
        calculation_view_name: Optional[str] = Field(default=None, description="")
        calculation_view_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        is_profiled: Optional[bool] = Field(default=None, description="")
        last_profiled_at: Optional[datetime] = Field(default=None, description="")
        dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_table: Optional[SapErpTable] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[List[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        sql_dbt_sources: Optional[List[DbtSource]] = Field(
            default=None, description=""
        )  # relationship
        dbt_models: Optional[List[DbtModel]] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_cds_view: Optional[SapErpCdsView] = Field(
            default=None, description=""
        )  # relationship
        sap_erp_view: Optional[SapErpView] = Field(
            default=None, description=""
        )  # relationship

    attributes: SapErpColumn.Attributes = Field(
        default_factory=lambda: SapErpColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.dbt_model import DbtModel  # noqa: E402, F401
from .core.dbt_source import DbtSource  # noqa: E402, F401
from .core.dbt_test import DbtTest  # noqa: E402, F401
from .sap_erp_cds_view import SapErpCdsView  # noqa: E402, F401
from .sap_erp_table import SapErpTable  # noqa: E402, F401
from .sap_erp_view import SapErpView  # noqa: E402, F401

SapErpColumn.Attributes.update_forward_refs()
