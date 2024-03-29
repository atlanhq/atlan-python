# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField

from .b_i import BI


class Sigma(BI):
    """Description"""

    type_name: str = Field(default="Sigma", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Sigma":
            raise ValueError("must be Sigma")
        return v

    def __setattr__(self, name, value):
        if name in Sigma._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaWorkbookQualifiedName",
        "sigmaWorkbookQualifiedName",
        "sigmaWorkbookQualifiedName.text",
    )
    """
    Unique name of the workbook in which this asset exists.
    """
    SIGMA_WORKBOOK_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaWorkbookName", "sigmaWorkbookName.keyword", "sigmaWorkbookName"
    )
    """
    Simple name of the workbook in which this asset exists.
    """
    SIGMA_PAGE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaPageQualifiedName",
        "sigmaPageQualifiedName",
        "sigmaPageQualifiedName.text",
    )
    """
    Unique name of the page on which this asset exists.
    """
    SIGMA_PAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaPageName", "sigmaPageName.keyword", "sigmaPageName"
    )
    """
    Simple name of the page on which this asset exists.
    """
    SIGMA_DATA_ELEMENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDataElementQualifiedName",
        "sigmaDataElementQualifiedName",
        "sigmaDataElementQualifiedName.text",
    )
    """
    Unique name of the data element in which this asset exists.
    """
    SIGMA_DATA_ELEMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDataElementName", "sigmaDataElementName.keyword", "sigmaDataElementName"
    )
    """
    Simple name of the data element in which this asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sigma_workbook_qualified_name",
        "sigma_workbook_name",
        "sigma_page_qualified_name",
        "sigma_page_name",
        "sigma_data_element_qualified_name",
        "sigma_data_element_name",
    ]

    @property
    def sigma_workbook_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_workbook_qualified_name
        )

    @sigma_workbook_qualified_name.setter
    def sigma_workbook_qualified_name(
        self, sigma_workbook_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_qualified_name = sigma_workbook_qualified_name

    @property
    def sigma_workbook_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_workbook_name

    @sigma_workbook_name.setter
    def sigma_workbook_name(self, sigma_workbook_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_workbook_name = sigma_workbook_name

    @property
    def sigma_page_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_page_qualified_name
        )

    @sigma_page_qualified_name.setter
    def sigma_page_qualified_name(self, sigma_page_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_qualified_name = sigma_page_qualified_name

    @property
    def sigma_page_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_page_name

    @sigma_page_name.setter
    def sigma_page_name(self, sigma_page_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_page_name = sigma_page_name

    @property
    def sigma_data_element_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_element_qualified_name
        )

    @sigma_data_element_qualified_name.setter
    def sigma_data_element_qualified_name(
        self, sigma_data_element_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_qualified_name = (
            sigma_data_element_qualified_name
        )

    @property
    def sigma_data_element_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sigma_data_element_name
        )

    @sigma_data_element_name.setter
    def sigma_data_element_name(self, sigma_data_element_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_element_name = sigma_data_element_name

    class Attributes(BI.Attributes):
        sigma_workbook_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sigma_workbook_name: Optional[str] = Field(default=None, description="")
        sigma_page_qualified_name: Optional[str] = Field(default=None, description="")
        sigma_page_name: Optional[str] = Field(default=None, description="")
        sigma_data_element_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sigma_data_element_name: Optional[str] = Field(default=None, description="")

    attributes: Sigma.Attributes = Field(
        default_factory=lambda: Sigma.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
