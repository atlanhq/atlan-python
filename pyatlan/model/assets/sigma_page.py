# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .sigma import Sigma


class SigmaPage(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaPage", allow_mutation=False)

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
    Number of data elements on this page.
    """

    SIGMA_DATA_ELEMENTS: ClassVar[RelationField] = RelationField("sigmaDataElements")
    """
    TBC
    """
    SIGMA_WORKBOOK: ClassVar[RelationField] = RelationField("sigmaWorkbook")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def sigma_data_elements(self) -> Optional[List[SigmaDataElement]]:
        return None if self.attributes is None else self.attributes.sigma_data_elements

    @sigma_data_elements.setter
    def sigma_data_elements(
        self, sigma_data_elements: Optional[List[SigmaDataElement]]
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
        sigma_data_element_count: Optional[int] = Field(default=None, description="")
        sigma_data_elements: Optional[List[SigmaDataElement]] = Field(
            default=None, description=""
        )  # relationship
        sigma_workbook: Optional[SigmaWorkbook] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaPage.Attributes = Field(
        default_factory=lambda: SigmaPage.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_data_element import SigmaDataElement  # noqa
from .sigma_workbook import SigmaWorkbook  # noqa
