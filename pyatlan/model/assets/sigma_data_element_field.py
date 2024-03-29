# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, RelationField, TextField

from .sigma import Sigma


class SigmaDataElementField(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaDataElementField", allow_mutation=False)

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
    Whether this field is hidden (true) or not (false).
    """
    SIGMA_DATA_ELEMENT_FIELD_FORMULA: ClassVar[TextField] = TextField(
        "sigmaDataElementFieldFormula", "sigmaDataElementFieldFormula"
    )
    """

    """

    SIGMA_DATA_ELEMENT: ClassVar[RelationField] = RelationField("sigmaDataElement")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
            default=None, description=""
        )
        sigma_data_element_field_formula: Optional[str] = Field(
            default=None, description=""
        )
        sigma_data_element: Optional[SigmaDataElement] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaDataElementField.Attributes = Field(
        default_factory=lambda: SigmaDataElementField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_data_element import SigmaDataElement  # noqa
