# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .core.catalog import Catalog


class SAP(Catalog):
    """Description"""

    type_name: str = Field(default="SAP", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SAP":
            raise ValueError("must be SAP")
        return v

    def __setattr__(self, name, value):
        if name in SAP._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

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

    _convenience_properties: ClassVar[List[str]] = [
        "sap_technical_name",
        "sap_logical_name",
        "sap_package_name",
        "sap_component_name",
        "sap_data_type",
        "sap_field_count",
        "sap_field_order",
    ]

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

    class Attributes(Catalog.Attributes):
        sap_technical_name: Optional[str] = Field(default=None, description="")
        sap_logical_name: Optional[str] = Field(default=None, description="")
        sap_package_name: Optional[str] = Field(default=None, description="")
        sap_component_name: Optional[str] = Field(default=None, description="")
        sap_data_type: Optional[str] = Field(default=None, description="")
        sap_field_count: Optional[int] = Field(default=None, description="")
        sap_field_order: Optional[int] = Field(default=None, description="")

    attributes: SAP.Attributes = Field(
        default_factory=lambda: SAP.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


SAP.Attributes.update_forward_refs()
