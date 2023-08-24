# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .asset49 import Salesforce


class SalesforceObject(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceObject":
            raise ValueError("must be SalesforceObject")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    IS_CUSTOM: ClassVar[BooleanField] = BooleanField("isCustom", "isCustom")
    """
    isCustom captures whether the object is a custom object or not
    """
    IS_MERGABLE: ClassVar[BooleanField] = BooleanField("isMergable", "isMergable")
    """
    TBC
    """
    IS_QUERYABLE: ClassVar[BooleanField] = BooleanField("isQueryable", "isQueryable")
    """
    TBC
    """
    FIELD_COUNT: ClassVar[NumericField] = NumericField("fieldCount", "fieldCount")
    """
    fieldCount is the number of fields in the object entity
    """

    LOOKUP_FIELDS: ClassVar[RelationField] = RelationField("lookupFields")
    """
    TBC
    """
    ORGANIZATION: ClassVar[RelationField] = RelationField("organization")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "is_custom",
        "is_mergable",
        "is_queryable",
        "field_count",
        "lookup_fields",
        "organization",
        "fields",
    ]

    @property
    def is_custom(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_custom

    @is_custom.setter
    def is_custom(self, is_custom: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_custom = is_custom

    @property
    def is_mergable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_mergable

    @is_mergable.setter
    def is_mergable(self, is_mergable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_mergable = is_mergable

    @property
    def is_queryable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_queryable

    @is_queryable.setter
    def is_queryable(self, is_queryable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_queryable = is_queryable

    @property
    def field_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.field_count

    @field_count.setter
    def field_count(self, field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.field_count = field_count

    @property
    def lookup_fields(self) -> Optional[list[SalesforceField]]:
        return None if self.attributes is None else self.attributes.lookup_fields

    @lookup_fields.setter
    def lookup_fields(self, lookup_fields: Optional[list[SalesforceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.lookup_fields = lookup_fields

    @property
    def organization(self) -> Optional[SalesforceOrganization]:
        return None if self.attributes is None else self.attributes.organization

    @organization.setter
    def organization(self, organization: Optional[SalesforceOrganization]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization = organization

    @property
    def fields(self) -> Optional[list[SalesforceField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[SalesforceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Salesforce.Attributes):
        is_custom: Optional[bool] = Field(None, description="", alias="isCustom")
        is_mergable: Optional[bool] = Field(None, description="", alias="isMergable")
        is_queryable: Optional[bool] = Field(None, description="", alias="isQueryable")
        field_count: Optional[int] = Field(None, description="", alias="fieldCount")
        lookup_fields: Optional[list[SalesforceField]] = Field(
            None, description="", alias="lookupFields"
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
        )  # relationship
        fields: Optional[list[SalesforceField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "SalesforceObject.Attributes" = Field(
        default_factory=lambda: SalesforceObject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceField(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceField":
            raise ValueError("must be SalesforceField")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "dataType", "dataType", "dataType.text"
    )
    """
    data type of the field
    """
    OBJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "objectQualifiedName", "objectQualifiedName"
    )
    """
    TBC
    """
    ORDER: ClassVar[NumericField] = NumericField("order", "order")
    """
    TBC
    """
    INLINE_HELP_TEXT: ClassVar[TextField] = TextField(
        "inlineHelpText", "inlineHelpText.text"
    )
    """
    TBC
    """
    IS_CALCULATED: ClassVar[BooleanField] = BooleanField("isCalculated", "isCalculated")
    """
    TBC
    """
    FORMULA: ClassVar[KeywordField] = KeywordField("formula", "formula")
    """
    TBC
    """
    IS_CASE_SENSITIVE: ClassVar[BooleanField] = BooleanField(
        "isCaseSensitive", "isCaseSensitive"
    )
    """
    TBC
    """
    IS_ENCRYPTED: ClassVar[BooleanField] = BooleanField("isEncrypted", "isEncrypted")
    """
    TBC
    """
    MAX_LENGTH: ClassVar[NumericField] = NumericField("maxLength", "maxLength")
    """
    TBC
    """
    IS_NULLABLE: ClassVar[BooleanField] = BooleanField("isNullable", "isNullable")
    """
    TBC
    """
    PRECISION: ClassVar[NumericField] = NumericField("precision", "precision")
    """
    Total number of digits allowed
    """
    NUMERIC_SCALE: ClassVar[NumericField] = NumericField("numericScale", "numericScale")
    """
    TBC
    """
    IS_UNIQUE: ClassVar[BooleanField] = BooleanField("isUnique", "isUnique")
    """
    TBC
    """
    PICKLIST_VALUES: ClassVar[KeywordField] = KeywordField(
        "picklistValues", "picklistValues"
    )
    """
    picklistValues is a list of values from which a user can pick from while adding a record
    """
    IS_POLYMORPHIC_FOREIGN_KEY: ClassVar[BooleanField] = BooleanField(
        "isPolymorphicForeignKey", "isPolymorphicForeignKey"
    )
    """
    isPolymorphicForeignKey captures whether the field references to record of multiple objects
    """
    DEFAULT_VALUE_FORMULA: ClassVar[KeywordField] = KeywordField(
        "defaultValueFormula", "defaultValueFormula"
    )
    """
    TBC
    """

    LOOKUP_OBJECTS: ClassVar[RelationField] = RelationField("lookupObjects")
    """
    TBC
    """
    OBJECT: ClassVar[RelationField] = RelationField("object")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "data_type",
        "object_qualified_name",
        "order",
        "inline_help_text",
        "is_calculated",
        "formula",
        "is_case_sensitive",
        "is_encrypted",
        "max_length",
        "is_nullable",
        "precision",
        "numeric_scale",
        "is_unique",
        "picklist_values",
        "is_polymorphic_foreign_key",
        "default_value_formula",
        "lookup_objects",
        "object",
    ]

    @property
    def data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_type

    @data_type.setter
    def data_type(self, data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_type = data_type

    @property
    def object_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.object_qualified_name
        )

    @object_qualified_name.setter
    def object_qualified_name(self, object_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object_qualified_name = object_qualified_name

    @property
    def order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.order

    @order.setter
    def order(self, order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.order = order

    @property
    def inline_help_text(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.inline_help_text

    @inline_help_text.setter
    def inline_help_text(self, inline_help_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inline_help_text = inline_help_text

    @property
    def is_calculated(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_calculated

    @is_calculated.setter
    def is_calculated(self, is_calculated: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_calculated = is_calculated

    @property
    def formula(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.formula

    @formula.setter
    def formula(self, formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.formula = formula

    @property
    def is_case_sensitive(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_case_sensitive

    @is_case_sensitive.setter
    def is_case_sensitive(self, is_case_sensitive: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_case_sensitive = is_case_sensitive

    @property
    def is_encrypted(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_encrypted

    @is_encrypted.setter
    def is_encrypted(self, is_encrypted: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_encrypted = is_encrypted

    @property
    def max_length(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.max_length

    @max_length.setter
    def max_length(self, max_length: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.max_length = max_length

    @property
    def is_nullable(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_nullable

    @is_nullable.setter
    def is_nullable(self, is_nullable: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_nullable = is_nullable

    @property
    def precision(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.precision

    @precision.setter
    def precision(self, precision: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.precision = precision

    @property
    def numeric_scale(self) -> Optional[float]:
        return None if self.attributes is None else self.attributes.numeric_scale

    @numeric_scale.setter
    def numeric_scale(self, numeric_scale: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.numeric_scale = numeric_scale

    @property
    def is_unique(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_unique

    @is_unique.setter
    def is_unique(self, is_unique: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_unique = is_unique

    @property
    def picklist_values(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.picklist_values

    @picklist_values.setter
    def picklist_values(self, picklist_values: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.picklist_values = picklist_values

    @property
    def is_polymorphic_foreign_key(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_polymorphic_foreign_key
        )

    @is_polymorphic_foreign_key.setter
    def is_polymorphic_foreign_key(self, is_polymorphic_foreign_key: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_polymorphic_foreign_key = is_polymorphic_foreign_key

    @property
    def default_value_formula(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.default_value_formula
        )

    @default_value_formula.setter
    def default_value_formula(self, default_value_formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.default_value_formula = default_value_formula

    @property
    def lookup_objects(self) -> Optional[list[SalesforceObject]]:
        return None if self.attributes is None else self.attributes.lookup_objects

    @lookup_objects.setter
    def lookup_objects(self, lookup_objects: Optional[list[SalesforceObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.lookup_objects = lookup_objects

    @property
    def object(self) -> Optional[SalesforceObject]:
        return None if self.attributes is None else self.attributes.object

    @object.setter
    def object(self, object: Optional[SalesforceObject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object = object

    class Attributes(Salesforce.Attributes):
        data_type: Optional[str] = Field(None, description="", alias="dataType")
        object_qualified_name: Optional[str] = Field(
            None, description="", alias="objectQualifiedName"
        )
        order: Optional[int] = Field(None, description="", alias="order")
        inline_help_text: Optional[str] = Field(
            None, description="", alias="inlineHelpText"
        )
        is_calculated: Optional[bool] = Field(
            None, description="", alias="isCalculated"
        )
        formula: Optional[str] = Field(None, description="", alias="formula")
        is_case_sensitive: Optional[bool] = Field(
            None, description="", alias="isCaseSensitive"
        )
        is_encrypted: Optional[bool] = Field(None, description="", alias="isEncrypted")
        max_length: Optional[int] = Field(None, description="", alias="maxLength")
        is_nullable: Optional[bool] = Field(None, description="", alias="isNullable")
        precision: Optional[int] = Field(None, description="", alias="precision")
        numeric_scale: Optional[float] = Field(
            None, description="", alias="numericScale"
        )
        is_unique: Optional[bool] = Field(None, description="", alias="isUnique")
        picklist_values: Optional[set[str]] = Field(
            None, description="", alias="picklistValues"
        )
        is_polymorphic_foreign_key: Optional[bool] = Field(
            None, description="", alias="isPolymorphicForeignKey"
        )
        default_value_formula: Optional[str] = Field(
            None, description="", alias="defaultValueFormula"
        )
        lookup_objects: Optional[list[SalesforceObject]] = Field(
            None, description="", alias="lookupObjects"
        )  # relationship
        object: Optional[SalesforceObject] = Field(
            None, description="", alias="object"
        )  # relationship

    attributes: "SalesforceField.Attributes" = Field(
        default_factory=lambda: SalesforceField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceOrganization(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceOrganization", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceOrganization":
            raise ValueError("must be SalesforceOrganization")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceOrganization._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_ID: ClassVar[KeywordField] = KeywordField("sourceId", "sourceId")
    """
    sourceId is the Id of the organization entity on salesforce
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    OBJECTS: ClassVar[RelationField] = RelationField("objects")
    """
    TBC
    """
    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "source_id",
        "reports",
        "objects",
        "dashboards",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def reports(self) -> Optional[list[SalesforceReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[SalesforceReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def objects(self) -> Optional[list[SalesforceObject]]:
        return None if self.attributes is None else self.attributes.objects

    @objects.setter
    def objects(self, objects: Optional[list[SalesforceObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.objects = objects

    @property
    def dashboards(self) -> Optional[list[SalesforceDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[SalesforceDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        reports: Optional[list[SalesforceReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        objects: Optional[list[SalesforceObject]] = Field(
            None, description="", alias="objects"
        )  # relationship
        dashboards: Optional[list[SalesforceDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship

    attributes: "SalesforceOrganization.Attributes" = Field(
        default_factory=lambda: SalesforceOrganization.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceDashboard(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceDashboard":
            raise ValueError("must be SalesforceDashboard")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_ID: ClassVar[KeywordField] = KeywordField("sourceId", "sourceId")
    """
    sourceId is the Id of the dashboard entity on salesforce
    """
    DASHBOARD_TYPE: ClassVar[KeywordField] = KeywordField(
        "dashboardType", "dashboardType"
    )
    """
    dashboardType is the type of dashboard in salesforce
    """
    REPORT_COUNT: ClassVar[NumericField] = NumericField("reportCount", "reportCount")
    """
    reportCount is the number of reports linked to the dashboard entity on salesforce
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    ORGANIZATION: ClassVar[RelationField] = RelationField("organization")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "source_id",
        "dashboard_type",
        "report_count",
        "reports",
        "organization",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def dashboard_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dashboard_type

    @dashboard_type.setter
    def dashboard_type(self, dashboard_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_type = dashboard_type

    @property
    def report_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def reports(self) -> Optional[list[SalesforceReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[SalesforceReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def organization(self) -> Optional[SalesforceOrganization]:
        return None if self.attributes is None else self.attributes.organization

    @organization.setter
    def organization(self, organization: Optional[SalesforceOrganization]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization = organization

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        dashboard_type: Optional[str] = Field(
            None, description="", alias="dashboardType"
        )
        report_count: Optional[int] = Field(None, description="", alias="reportCount")
        reports: Optional[list[SalesforceReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
        )  # relationship

    attributes: "SalesforceDashboard.Attributes" = Field(
        default_factory=lambda: SalesforceDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SalesforceReport(Salesforce):
    """Description"""

    type_name: str = Field("SalesforceReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SalesforceReport":
            raise ValueError("must be SalesforceReport")
        return v

    def __setattr__(self, name, value):
        if name in SalesforceReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SOURCE_ID: ClassVar[KeywordField] = KeywordField("sourceId", "sourceId")
    """
    sourceId is the Id of the report entity on salesforce
    """
    REPORT_TYPE: ClassVar[KeywordField] = KeywordField("reportType", "reportType")
    """
    reportType is the type of report in salesforce
    """
    DETAIL_COLUMNS: ClassVar[KeywordField] = KeywordField(
        "detailColumns", "detailColumns"
    )
    """
    detailColumns is a list of column names on the report
    """

    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """
    ORGANIZATION: ClassVar[RelationField] = RelationField("organization")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "source_id",
        "report_type",
        "detail_columns",
        "dashboards",
        "organization",
    ]

    @property
    def source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_id

    @source_id.setter
    def source_id(self, source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_id = source_id

    @property
    def report_type(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.report_type

    @report_type.setter
    def report_type(self, report_type: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_type = report_type

    @property
    def detail_columns(self) -> Optional[set[str]]:
        return None if self.attributes is None else self.attributes.detail_columns

    @detail_columns.setter
    def detail_columns(self, detail_columns: Optional[set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.detail_columns = detail_columns

    @property
    def dashboards(self) -> Optional[list[SalesforceDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[SalesforceDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def organization(self) -> Optional[SalesforceOrganization]:
        return None if self.attributes is None else self.attributes.organization

    @organization.setter
    def organization(self, organization: Optional[SalesforceOrganization]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.organization = organization

    class Attributes(Salesforce.Attributes):
        source_id: Optional[str] = Field(None, description="", alias="sourceId")
        report_type: Optional[dict[str, str]] = Field(
            None, description="", alias="reportType"
        )
        detail_columns: Optional[set[str]] = Field(
            None, description="", alias="detailColumns"
        )
        dashboards: Optional[list[SalesforceDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            None, description="", alias="organization"
        )  # relationship

    attributes: "SalesforceReport.Attributes" = Field(
        default_factory=lambda: SalesforceReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


SalesforceObject.Attributes.update_forward_refs()


SalesforceField.Attributes.update_forward_refs()


SalesforceOrganization.Attributes.update_forward_refs()


SalesforceDashboard.Attributes.update_forward_refs()


SalesforceReport.Attributes.update_forward_refs()
