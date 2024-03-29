# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .salesforce import Salesforce


class SalesforceField(Salesforce):
    """Description"""

    type_name: str = Field(default="SalesforceField", allow_mutation=False)

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
    Data type of values in this field.
    """
    OBJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "objectQualifiedName", "objectQualifiedName"
    )
    """
    Unique name of the object in which this field exists.
    """
    ORDER: ClassVar[NumericField] = NumericField("order", "order")
    """
    Order (position) of this field within the object.
    """
    INLINE_HELP_TEXT: ClassVar[TextField] = TextField(
        "inlineHelpText", "inlineHelpText.text"
    )
    """
    Help text for this field.
    """
    IS_CALCULATED: ClassVar[BooleanField] = BooleanField("isCalculated", "isCalculated")
    """
    Whether this field is calculated (true) or not (false).
    """
    FORMULA: ClassVar[KeywordField] = KeywordField("formula", "formula")
    """
    Formula for this field, if it is a calculated field.
    """
    IS_CASE_SENSITIVE: ClassVar[BooleanField] = BooleanField(
        "isCaseSensitive", "isCaseSensitive"
    )
    """
    Whether this field is case sensitive (true) or in-sensitive (false).
    """
    IS_ENCRYPTED: ClassVar[BooleanField] = BooleanField("isEncrypted", "isEncrypted")
    """
    Whether this field is encrypted (true) or not (false).
    """
    MAX_LENGTH: ClassVar[NumericField] = NumericField("maxLength", "maxLength")
    """
    Maximum length of this field.
    """
    IS_NULLABLE: ClassVar[BooleanField] = BooleanField("isNullable", "isNullable")
    """
    Whether this field allows null values (true) or not (false).
    """
    PRECISION: ClassVar[NumericField] = NumericField("precision", "precision")
    """
    Total number of digits allowed
    """
    NUMERIC_SCALE: ClassVar[NumericField] = NumericField("numericScale", "numericScale")
    """
    Number of digits allowed to the right of the decimal point.
    """
    IS_UNIQUE: ClassVar[BooleanField] = BooleanField("isUnique", "isUnique")
    """
    Whether this field must have unique values (true) or not (false).
    """
    PICKLIST_VALUES: ClassVar[KeywordField] = KeywordField(
        "picklistValues", "picklistValues"
    )
    """
    List of values from which a user can pick while adding a record.
    """
    IS_POLYMORPHIC_FOREIGN_KEY: ClassVar[BooleanField] = BooleanField(
        "isPolymorphicForeignKey", "isPolymorphicForeignKey"
    )
    """
    Whether this field references a record of multiple objects (true) or not (false).
    """
    DEFAULT_VALUE_FORMULA: ClassVar[KeywordField] = KeywordField(
        "defaultValueFormula", "defaultValueFormula"
    )
    """
    Formula for the default value for this field.
    """

    LOOKUP_OBJECTS: ClassVar[RelationField] = RelationField("lookupObjects")
    """
    TBC
    """
    OBJECT: ClassVar[RelationField] = RelationField("object")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def picklist_values(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.picklist_values

    @picklist_values.setter
    def picklist_values(self, picklist_values: Optional[Set[str]]):
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
    def lookup_objects(self) -> Optional[List[SalesforceObject]]:
        return None if self.attributes is None else self.attributes.lookup_objects

    @lookup_objects.setter
    def lookup_objects(self, lookup_objects: Optional[List[SalesforceObject]]):
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
        data_type: Optional[str] = Field(default=None, description="")
        object_qualified_name: Optional[str] = Field(default=None, description="")
        order: Optional[int] = Field(default=None, description="")
        inline_help_text: Optional[str] = Field(default=None, description="")
        is_calculated: Optional[bool] = Field(default=None, description="")
        formula: Optional[str] = Field(default=None, description="")
        is_case_sensitive: Optional[bool] = Field(default=None, description="")
        is_encrypted: Optional[bool] = Field(default=None, description="")
        max_length: Optional[int] = Field(default=None, description="")
        is_nullable: Optional[bool] = Field(default=None, description="")
        precision: Optional[int] = Field(default=None, description="")
        numeric_scale: Optional[float] = Field(default=None, description="")
        is_unique: Optional[bool] = Field(default=None, description="")
        picklist_values: Optional[Set[str]] = Field(default=None, description="")
        is_polymorphic_foreign_key: Optional[bool] = Field(default=None, description="")
        default_value_formula: Optional[str] = Field(default=None, description="")
        lookup_objects: Optional[List[SalesforceObject]] = Field(
            default=None, description=""
        )  # relationship
        object: Optional[SalesforceObject] = Field(
            default=None, description=""
        )  # relationship

    attributes: SalesforceField.Attributes = Field(
        default_factory=lambda: SalesforceField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .salesforce_object import SalesforceObject  # noqa
