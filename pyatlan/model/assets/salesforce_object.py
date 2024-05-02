# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, NumericField, RelationField

from .salesforce import Salesforce


class SalesforceObject(Salesforce):
    """Description"""

    type_name: str = Field(default="SalesforceObject", allow_mutation=False)

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
    Whether this object is a custom object (true) or not (false).
    """
    IS_MERGABLE: ClassVar[BooleanField] = BooleanField("isMergable", "isMergable")
    """
    Whether this object is mergable (true) or not (false).
    """
    IS_QUERYABLE: ClassVar[BooleanField] = BooleanField("isQueryable", "isQueryable")
    """
    Whether this object is queryable (true) or not (false).
    """
    FIELD_COUNT: ClassVar[NumericField] = NumericField("fieldCount", "fieldCount")
    """
    Number of fields in this object.
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

    _convenience_properties: ClassVar[List[str]] = [
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
    def lookup_fields(self) -> Optional[List[SalesforceField]]:
        return None if self.attributes is None else self.attributes.lookup_fields

    @lookup_fields.setter
    def lookup_fields(self, lookup_fields: Optional[List[SalesforceField]]):
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
    def fields(self) -> Optional[List[SalesforceField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[List[SalesforceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Salesforce.Attributes):
        is_custom: Optional[bool] = Field(default=None, description="")
        is_mergable: Optional[bool] = Field(default=None, description="")
        is_queryable: Optional[bool] = Field(default=None, description="")
        field_count: Optional[int] = Field(default=None, description="")
        lookup_fields: Optional[List[SalesforceField]] = Field(
            default=None, description=""
        )  # relationship
        organization: Optional[SalesforceOrganization] = Field(
            default=None, description=""
        )  # relationship
        fields: Optional[List[SalesforceField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SalesforceObject.Attributes = Field(
        default_factory=lambda: SalesforceObject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .salesforce_field import SalesforceField  # noqa
from .salesforce_organization import SalesforceOrganization  # noqa
