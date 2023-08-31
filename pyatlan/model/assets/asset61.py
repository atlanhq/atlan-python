# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .asset38 import Sigma


class SigmaWorkbook(Sigma):
    """Description"""

    type_name: str = Field("SigmaWorkbook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaWorkbook":
            raise ValueError("must be SigmaWorkbook")
        return v

    def __setattr__(self, name, value):
        if name in SigmaWorkbook._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_PAGE_COUNT: ClassVar[NumericField] = NumericField(
        "sigmaPageCount", "sigmaPageCount"
    )
    """
    TBC
    """

    SIGMA_PAGES: ClassVar[RelationField] = RelationField("sigmaPages")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sigma_page_count",
        "sigma_pages",
    ]

    @property
    def sigma_page_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.sigma_page_count

    @sigma_page_count.setter
    def sigma_page_count(self, sigma_page_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_count = sigma_page_count

    @property
    def sigma_pages(self) -> Optional[list[SigmaPage]]:
        return None if self.attributes is None else self.attributes.sigma_pages

    @sigma_pages.setter
    def sigma_pages(self, sigma_pages: Optional[list[SigmaPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_pages = sigma_pages

    class Attributes(Sigma.Attributes):
        sigma_page_count: Optional[int] = Field(
            None, description="", alias="sigmaPageCount"
        )
        sigma_pages: Optional[list[SigmaPage]] = Field(
            None, description="", alias="sigmaPages"
        )  # relationship

    attributes: "SigmaWorkbook.Attributes" = Field(
        default_factory=lambda: SigmaWorkbook.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataElementField(Sigma):
    """Description"""

    type_name: str = Field("SigmaDataElementField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataElementField":
            raise ValueError("must be SigmaDataElementField")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataElementField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATA_ELEMENT_FIELD_IS_HIDDEN: ClassVar[BooleanField] = BooleanField(
        "sigmaDataElementFieldIsHidden", "sigmaDataElementFieldIsHidden"
    )
    """
    TBC
    """
    SIGMA_DATA_ELEMENT_FIELD_FORMULA: ClassVar[TextField] = TextField(
        "sigmaDataElementFieldFormula", "sigmaDataElementFieldFormula"
    )
    """
    TBC
    """

    SIGMA_DATA_ELEMENT: ClassVar[RelationField] = RelationField("sigmaDataElement")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sigma_data_element_field_is_hidden",
        "sigma_data_element_field_formula",
        "sigma_data_element",
    ]

    @property
    def sigma_data_element_field_is_hidden(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_field_is_hidden
        )

    @sigma_data_element_field_is_hidden.setter
    def sigma_data_element_field_is_hidden(
        self, sigma_data_element_field_is_hidden: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_field_is_hidden = (
            sigma_data_element_field_is_hidden
        )

    @property
    def sigma_data_element_field_formula(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_field_formula
        )

    @sigma_data_element_field_formula.setter
    def sigma_data_element_field_formula(
        self, sigma_data_element_field_formula: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_field_formula = (
            sigma_data_element_field_formula
        )

    @property
    def sigma_data_element(self) -> Optional[SigmaDataElement]:
        return None if self.attributes is None else self.attributes.sigma_data_element

    @sigma_data_element.setter
    def sigma_data_element(self, sigma_data_element: Optional[SigmaDataElement]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element = sigma_data_element

    class Attributes(Sigma.Attributes):
        sigma_data_element_field_is_hidden: Optional[bool] = Field(
            None, description="", alias="sigmaDataElementFieldIsHidden"
        )
        sigma_data_element_field_formula: Optional[str] = Field(
            None, description="", alias="sigmaDataElementFieldFormula"
        )
        sigma_data_element: Optional[SigmaDataElement] = Field(
            None, description="", alias="sigmaDataElement"
        )  # relationship

    attributes: "SigmaDataElementField.Attributes" = Field(
        default_factory=lambda: SigmaDataElementField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaPage(Sigma):
    """Description"""

    type_name: str = Field("SigmaPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaPage":
            raise ValueError("must be SigmaPage")
        return v

    def __setattr__(self, name, value):
        if name in SigmaPage._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATA_ELEMENT_COUNT: ClassVar[NumericField] = NumericField(
        "sigmaDataElementCount", "sigmaDataElementCount"
    )
    """
    TBC
    """

    SIGMA_DATA_ELEMENTS: ClassVar[RelationField] = RelationField("sigmaDataElements")
    """
    TBC
    """
    SIGMA_WORKBOOK: ClassVar[RelationField] = RelationField("sigmaWorkbook")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sigma_data_element_count",
        "sigma_data_elements",
        "sigma_workbook",
    ]

    @property
    def sigma_data_element_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_count
        )

    @sigma_data_element_count.setter
    def sigma_data_element_count(self, sigma_data_element_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_count = sigma_data_element_count

    @property
    def sigma_data_elements(self) -> Optional[list[SigmaDataElement]]:
        return None if self.attributes is None else self.attributes.sigma_data_elements

    @sigma_data_elements.setter
    def sigma_data_elements(
        self, sigma_data_elements: Optional[list[SigmaDataElement]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_elements = sigma_data_elements

    @property
    def sigma_workbook(self) -> Optional[SigmaWorkbook]:
        return None if self.attributes is None else self.attributes.sigma_workbook

    @sigma_workbook.setter
    def sigma_workbook(self, sigma_workbook: Optional[SigmaWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook = sigma_workbook

    class Attributes(Sigma.Attributes):
        sigma_data_element_count: Optional[int] = Field(
            None, description="", alias="sigmaDataElementCount"
        )
        sigma_data_elements: Optional[list[SigmaDataElement]] = Field(
            None, description="", alias="sigmaDataElements"
        )  # relationship
        sigma_workbook: Optional[SigmaWorkbook] = Field(
            None, description="", alias="sigmaWorkbook"
        )  # relationship

    attributes: "SigmaPage.Attributes" = Field(
        default_factory=lambda: SigmaPage.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataElement(Sigma):
    """Description"""

    type_name: str = Field("SigmaDataElement", allow_mutation=False)

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
    TBC
    """
    SIGMA_DATA_ELEMENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "sigmaDataElementType", "sigmaDataElementType"
    )
    """
    TBC
    """
    SIGMA_DATA_ELEMENT_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "sigmaDataElementFieldCount", "sigmaDataElementFieldCount"
    )
    """
    TBC
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

    _convenience_properties: ClassVar[list[str]] = [
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
    def sigma_data_element_fields(self) -> Optional[list[SigmaDataElementField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_fields
        )

    @sigma_data_element_fields.setter
    def sigma_data_element_fields(
        self, sigma_data_element_fields: Optional[list[SigmaDataElementField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_fields = sigma_data_element_fields

    class Attributes(Sigma.Attributes):
        sigma_data_element_query: Optional[str] = Field(
            None, description="", alias="sigmaDataElementQuery"
        )
        sigma_data_element_type: Optional[str] = Field(
            None, description="", alias="sigmaDataElementType"
        )
        sigma_data_element_field_count: Optional[int] = Field(
            None, description="", alias="sigmaDataElementFieldCount"
        )
        sigma_page: Optional[SigmaPage] = Field(
            None, description="", alias="sigmaPage"
        )  # relationship
        sigma_data_element_fields: Optional[list[SigmaDataElementField]] = Field(
            None, description="", alias="sigmaDataElementFields"
        )  # relationship

    attributes: "SigmaDataElement.Attributes" = Field(
        default_factory=lambda: SigmaDataElement.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


SigmaWorkbook.Attributes.update_forward_refs()


SigmaDataElementField.Attributes.update_forward_refs()


SigmaPage.Attributes.update_forward_refs()


SigmaDataElement.Attributes.update_forward_refs()
