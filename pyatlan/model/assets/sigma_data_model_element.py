# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .sigma import Sigma


class SigmaDataModelElement(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaDataModelElement", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataModelElement":
            raise ValueError("must be SigmaDataModelElement")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataModelElement._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATA_MODEL_ELEMENT_KIND: ClassVar[KeywordField] = KeywordField(
        "sigmaDataModelElementKind", "sigmaDataModelElementKind"
    )
    """
    Kind of data model element, for example 'table' or 'view'.
    """
    SIGMA_DATA_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sigmaDataModelQualifiedName", "sigmaDataModelQualifiedName"
    )
    """
    Unique name of the data model in which this element exists.
    """
    SIGMA_DATA_MODEL_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDataModelName", "sigmaDataModelName.keyword", "sigmaDataModelName"
    )
    """
    Simple name of the data model in which this element exists.
    """

    DATA_MODEL_ELEMENT_COLUMNS: ClassVar[RelationField] = RelationField(
        "dataModelElementColumns"
    )
    """
    TBC
    """
    SIGMA_DATA_MODEL: ClassVar[RelationField] = RelationField("sigmaDataModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sigma_data_model_element_kind",
        "sigma_data_model_qualified_name",
        "sigma_data_model_name",
        "data_model_element_columns",
        "sigma_data_model",
    ]

    @property
    def sigma_data_model_element_kind(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_element_kind
        )

    @sigma_data_model_element_kind.setter
    def sigma_data_model_element_kind(
        self, sigma_data_model_element_kind: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_element_kind = sigma_data_model_element_kind

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
    def data_model_element_columns(self) -> Optional[List[SigmaDataModelColumn]]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_model_element_columns
        )

    @data_model_element_columns.setter
    def data_model_element_columns(
        self, data_model_element_columns: Optional[List[SigmaDataModelColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_element_columns = data_model_element_columns

    @property
    def sigma_data_model(self) -> Optional[SigmaDataModel]:
        return None if self.attributes is None else self.attributes.sigma_data_model

    @sigma_data_model.setter
    def sigma_data_model(self, sigma_data_model: Optional[SigmaDataModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model = sigma_data_model

    class Attributes(Sigma.Attributes):
        sigma_data_model_element_kind: Optional[str] = Field(
            default=None, description=""
        )
        sigma_data_model_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        sigma_data_model_name: Optional[str] = Field(default=None, description="")
        data_model_element_columns: Optional[List[SigmaDataModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        sigma_data_model: Optional[SigmaDataModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaDataModelElement.Attributes = Field(
        default_factory=lambda: SigmaDataModelElement.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_data_model import SigmaDataModel  # noqa: E402, F401
from .sigma_data_model_column import SigmaDataModelColumn  # noqa: E402, F401

SigmaDataModelElement.Attributes.update_forward_refs()
