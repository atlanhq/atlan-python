# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .sigma import Sigma


class SigmaDataModel(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaDataModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataModel":
            raise ValueError("must be SigmaDataModel")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATA_MODEL_URL_ID: ClassVar[KeywordField] = KeywordField(
        "sigmaDataModelUrlId", "sigmaDataModelUrlId"
    )
    """
    Short (21-22 character) URL-safe identifier of this data model in Sigma, used in deep-link URLs into the Sigma UI.
    """
    SIGMA_DATA_MODEL_DOCUMENT_VERSION: ClassVar[NumericField] = NumericField(
        "sigmaDataModelDocumentVersion", "sigmaDataModelDocumentVersion"
    )
    """
    Current document version of this data model, as reported by the Sigma /spec endpoint. Sigma increments this on each save.
    """  # noqa: E501
    SIGMA_DATA_MODEL_LATEST_DOCUMENT_VERSION: ClassVar[NumericField] = NumericField(
        "sigmaDataModelLatestDocumentVersion", "sigmaDataModelLatestDocumentVersion"
    )
    """
    Latest document version of this data model, as reported by the Sigma /spec endpoint (falls back to the latestVersion field from /dataModels when /spec is unavailable).
    """  # noqa: E501
    SIGMA_DATA_MODEL_SCHEMA_VERSION: ClassVar[NumericField] = NumericField(
        "sigmaDataModelSchemaVersion", "sigmaDataModelSchemaVersion"
    )
    """
    Schema version of this data model, as reported by the Sigma /spec endpoint.
    """
    SIGMA_DATA_MODEL_ELEMENT_COUNT: ClassVar[NumericField] = NumericField(
        "sigmaDataModelElementCount", "sigmaDataModelElementCount"
    )
    """
    Number of elements (warehouse-table, sql, data-model, dataset sources) inside this data model.
    """
    SIGMA_DATA_MODEL_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "sigmaDataModelColumnCount", "sigmaDataModelColumnCount"
    )
    """
    Number of columns defined across all elements of this data model.
    """
    SIGMA_DATA_MODEL_PATH: ClassVar[TextField] = TextField(
        "sigmaDataModelPath", "sigmaDataModelPath"
    )
    """
    Folder path of this data model in Sigma (for example, the root path "/My Documents").
    """

    SIGMA_DATA_MODEL_COLUMNS: ClassVar[RelationField] = RelationField(
        "sigmaDataModelColumns"
    )
    """
    TBC
    """
    DATA_MODEL_ELEMENTS: ClassVar[RelationField] = RelationField("dataModelElements")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "sigma_data_model_url_id",
        "sigma_data_model_document_version",
        "sigma_data_model_latest_document_version",
        "sigma_data_model_schema_version",
        "sigma_data_model_element_count",
        "sigma_data_model_column_count",
        "sigma_data_model_path",
        "sigma_data_model_columns",
        "data_model_elements",
    ]

    @property
    def sigma_data_model_url_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sigma_data_model_url_id
        )

    @sigma_data_model_url_id.setter
    def sigma_data_model_url_id(self, sigma_data_model_url_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_url_id = sigma_data_model_url_id

    @property
    def sigma_data_model_document_version(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_document_version
        )

    @sigma_data_model_document_version.setter
    def sigma_data_model_document_version(
        self, sigma_data_model_document_version: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_document_version = (
            sigma_data_model_document_version
        )

    @property
    def sigma_data_model_latest_document_version(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_latest_document_version
        )

    @sigma_data_model_latest_document_version.setter
    def sigma_data_model_latest_document_version(
        self, sigma_data_model_latest_document_version: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_latest_document_version = (
            sigma_data_model_latest_document_version
        )

    @property
    def sigma_data_model_schema_version(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_schema_version
        )

    @sigma_data_model_schema_version.setter
    def sigma_data_model_schema_version(
        self, sigma_data_model_schema_version: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_schema_version = (
            sigma_data_model_schema_version
        )

    @property
    def sigma_data_model_element_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_element_count
        )

    @sigma_data_model_element_count.setter
    def sigma_data_model_element_count(
        self, sigma_data_model_element_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_element_count = sigma_data_model_element_count

    @property
    def sigma_data_model_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_column_count
        )

    @sigma_data_model_column_count.setter
    def sigma_data_model_column_count(
        self, sigma_data_model_column_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_column_count = sigma_data_model_column_count

    @property
    def sigma_data_model_path(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.sigma_data_model_path
        )

    @sigma_data_model_path.setter
    def sigma_data_model_path(self, sigma_data_model_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_path = sigma_data_model_path

    @property
    def sigma_data_model_columns(self) -> Optional[List[SigmaDataModelColumn]]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_data_model_columns
        )

    @sigma_data_model_columns.setter
    def sigma_data_model_columns(
        self, sigma_data_model_columns: Optional[List[SigmaDataModelColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_data_model_columns = sigma_data_model_columns

    @property
    def data_model_elements(self) -> Optional[List[SigmaDataModelElement]]:
        return None if self.attributes is None else self.attributes.data_model_elements

    @data_model_elements.setter
    def data_model_elements(
        self, data_model_elements: Optional[List[SigmaDataModelElement]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_elements = data_model_elements

    class Attributes(Sigma.Attributes):
        sigma_data_model_url_id: Optional[str] = Field(default=None, description="")
        sigma_data_model_document_version: Optional[int] = Field(
            default=None, description=""
        )
        sigma_data_model_latest_document_version: Optional[int] = Field(
            default=None, description=""
        )
        sigma_data_model_schema_version: Optional[int] = Field(
            default=None, description=""
        )
        sigma_data_model_element_count: Optional[int] = Field(
            default=None, description=""
        )
        sigma_data_model_column_count: Optional[int] = Field(
            default=None, description=""
        )
        sigma_data_model_path: Optional[str] = Field(default=None, description="")
        sigma_data_model_columns: Optional[List[SigmaDataModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        data_model_elements: Optional[List[SigmaDataModelElement]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaDataModel.Attributes = Field(
        default_factory=lambda: SigmaDataModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_data_model_column import SigmaDataModelColumn  # noqa: E402, F401
from .sigma_data_model_element import SigmaDataModelElement  # noqa: E402, F401

SigmaDataModel.Attributes.update_forward_refs()
