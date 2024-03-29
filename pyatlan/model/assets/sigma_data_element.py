# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .sigma import Sigma


class SigmaDataElement(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaDataElement", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataElement":
            raise ValueError("must be SigmaDataElement")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataElement._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATA_ELEMENT_QUERY: ClassVar[KeywordField] = KeywordField(
        "sigmaDataElementQuery", "sigmaDataElementQuery"
    )
    """

    """
    SIGMA_DATA_ELEMENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "sigmaDataElementType", "sigmaDataElementType"
    )
    """

    """
    SIGMA_DATA_ELEMENT_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "sigmaDataElementFieldCount", "sigmaDataElementFieldCount"
    )
    """
    Number of fields in this data element.
    """

    SIGMA_PAGE: ClassVar[RelationField] = RelationField("sigmaPage")
    """
    TBC
    """
    SIGMA_DATA_ELEMENT_FIELDS: ClassVar[RelationField] = RelationField(
        "sigmaDataElementFields"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sigma_data_element_query",
        "sigma_data_element_type",
        "sigma_data_element_field_count",
        "sigma_page",
        "sigma_data_element_fields",
    ]

    @property
    def sigma_data_element_query(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_query
        )

    @sigma_data_element_query.setter
    def sigma_data_element_query(self, sigma_data_element_query: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_query = sigma_data_element_query

    @property
    def sigma_data_element_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sigma_data_element_type
        )

    @sigma_data_element_type.setter
    def sigma_data_element_type(self, sigma_data_element_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_type = sigma_data_element_type

    @property
    def sigma_data_element_field_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_field_count
        )

    @sigma_data_element_field_count.setter
    def sigma_data_element_field_count(
        self, sigma_data_element_field_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_field_count = sigma_data_element_field_count

    @property
    def sigma_page(self) -> Optional[SigmaPage]:
        return None if self.attributes is None else self.attributes.sigma_page

    @sigma_page.setter
    def sigma_page(self, sigma_page: Optional[SigmaPage]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page = sigma_page

    @property
    def sigma_data_element_fields(self) -> Optional[List[SigmaDataElementField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_fields
        )

    @sigma_data_element_fields.setter
    def sigma_data_element_fields(
        self, sigma_data_element_fields: Optional[List[SigmaDataElementField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_fields = sigma_data_element_fields

    class Attributes(Sigma.Attributes):
        sigma_data_element_query: Optional[str] = Field(default=None, description="")
        sigma_data_element_type: Optional[str] = Field(default=None, description="")
        sigma_data_element_field_count: Optional[int] = Field(
            default=None, description=""
        )
        sigma_page: Optional[SigmaPage] = Field(
            default=None, description=""
        )  # relationship
        sigma_data_element_fields: Optional[List[SigmaDataElementField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaDataElement.Attributes = Field(
        default_factory=lambda: SigmaDataElement.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_data_element_field import SigmaDataElementField  # noqa
from .sigma_page import SigmaPage  # noqa
