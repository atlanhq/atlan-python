# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)

from .sigma import Sigma


class SigmaDataModelColumn(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaDataModelColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataModelColumn":
            raise ValueError("must be SigmaDataModelColumn")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataModelColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATA_MODEL_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDataModelQualifiedName",
        "sigmaDataModelQualifiedName.keyword",
        "sigmaDataModelQualifiedName",
    )
    """
    Unique name of the Sigma data model in which this column exists.
    """
    SIGMA_DATA_MODEL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDataModelName", "sigmaDataModelName.keyword", "sigmaDataModelName"
    )
    """
    Simple name of the Sigma data model in which this column exists.
    """
    SIGMA_DATA_MODEL_COLUMN_FORMULA: ClassVar[TextField] = TextField(
        "sigmaDataModelColumnFormula", "sigmaDataModelColumnFormula"
    )
    """
    Formula expression that defines this column (Sigma's formula language). Truncated to 100,000 characters by the connector for parity with sigmaDataElementFieldFormula.
    """  # noqa: E501
    SIGMA_DATA_MODEL_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "sigmaDataModelColumnDataType", "sigmaDataModelColumnDataType"
    )
    """
    Data type of this column as reported by Sigma (vocabulary: datetime, integer, number, text, variant). Flattened by the connector from the API's nested type.type field.
    """  # noqa: E501

    SIGMA_DATA_MODEL_ELEMENT: ClassVar[RelationField] = RelationField(
        "sigmaDataModelElement"
    )
    """
    TBC
    """
    SIGMA_DATA_MODEL: ClassVar[RelationField] = RelationField("sigmaDataModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sigma_data_model_qualified_name",
        "sigma_data_model_name",
        "sigma_data_model_column_formula",
        "sigma_data_model_column_data_type",
        "sigma_data_model_element",
        "sigma_data_model",
    ]

    @property
    def sigma_data_model_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_qualified_name
        )

    @sigma_data_model_qualified_name.setter
    def sigma_data_model_qualified_name(
        self, sigma_data_model_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_qualified_name = (
            sigma_data_model_qualified_name
        )

    @property
    def sigma_data_model_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sigma_data_model_name
        )

    @sigma_data_model_name.setter
    def sigma_data_model_name(self, sigma_data_model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_name = sigma_data_model_name

    @property
    def sigma_data_model_column_formula(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_column_formula
        )

    @sigma_data_model_column_formula.setter
    def sigma_data_model_column_formula(
        self, sigma_data_model_column_formula: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_column_formula = (
            sigma_data_model_column_formula
        )

    @property
    def sigma_data_model_column_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_column_data_type
        )

    @sigma_data_model_column_data_type.setter
    def sigma_data_model_column_data_type(
        self, sigma_data_model_column_data_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_column_data_type = (
            sigma_data_model_column_data_type
        )

    @property
    def sigma_data_model_element(self) -> Optional[SigmaDataModelElement]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_element
        )

    @sigma_data_model_element.setter
    def sigma_data_model_element(
        self, sigma_data_model_element: Optional[SigmaDataModelElement]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_element = sigma_data_model_element

    @property
    def sigma_data_model(self) -> Optional[SigmaDataModel]:
        return None if self.attributes is None else self.attributes.sigma_data_model

    @sigma_data_model.setter
    def sigma_data_model(self, sigma_data_model: Optional[SigmaDataModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model = sigma_data_model

    class Attributes(Sigma.Attributes):
        sigma_data_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sigma_data_model_name: Optional[str] = Field(default=None, description="")
        sigma_data_model_column_formula: Optional[str] = Field(
            default=None, description=""
        )
        sigma_data_model_column_data_type: Optional[str] = Field(
            default=None, description=""
        )
        sigma_data_model_element: Optional[SigmaDataModelElement] = Field(
            default=None, description=""
        )  # relationship
        sigma_data_model: Optional[SigmaDataModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaDataModelColumn.Attributes = Field(
        default_factory=lambda: SigmaDataModelColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_data_model import SigmaDataModel  # noqa: E402, F401
from .sigma_data_model_element import SigmaDataModelElement  # noqa: E402, F401

SigmaDataModelColumn.Attributes.update_forward_refs()
