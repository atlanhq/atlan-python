# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .sigma import Sigma


class SigmaWorkbook(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaWorkbook", allow_mutation=False)

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
    Number of pages in this workbook.
    """

    SIGMA_PAGES: ClassVar[RelationField] = RelationField("sigmaPages")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def sigma_pages(self) -> Optional[List[SigmaPage]]:
        return None if self.attributes is None else self.attributes.sigma_pages

    @sigma_pages.setter
    def sigma_pages(self, sigma_pages: Optional[List[SigmaPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_pages = sigma_pages

    class Attributes(Sigma.Attributes):
        sigma_page_count: Optional[int] = Field(default=None, description="")
        sigma_pages: Optional[List[SigmaPage]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaWorkbook.Attributes = Field(
        default_factory=lambda: SigmaWorkbook.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_page import SigmaPage  # noqa
