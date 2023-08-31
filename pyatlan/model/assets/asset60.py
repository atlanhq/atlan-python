# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordTextField,
    NumericField,
    RelationField,
)

from .asset38 import Sigma


class SigmaDatasetColumn(Sigma):
    """Description"""

    type_name: str = Field("SigmaDatasetColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDatasetColumn":
            raise ValueError("must be SigmaDatasetColumn")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDatasetColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATASET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDatasetQualifiedName",
        "sigmaDatasetQualifiedName",
        "sigmaDatasetQualifiedName.text",
    )
    """
    TBC
    """
    SIGMA_DATASET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDatasetName", "sigmaDatasetName.keyword", "sigmaDatasetName"
    )
    """
    TBC
    """

    SIGMA_DATASET: ClassVar[RelationField] = RelationField("sigmaDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sigma_dataset_qualified_name",
        "sigma_dataset_name",
        "sigma_dataset",
    ]

    @property
    def sigma_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_dataset_qualified_name
        )

    @sigma_dataset_qualified_name.setter
    def sigma_dataset_qualified_name(self, sigma_dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_qualified_name = sigma_dataset_qualified_name

    @property
    def sigma_dataset_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sigma_dataset_name

    @sigma_dataset_name.setter
    def sigma_dataset_name(self, sigma_dataset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_name = sigma_dataset_name

    @property
    def sigma_dataset(self) -> Optional[SigmaDataset]:
        return None if self.attributes is None else self.attributes.sigma_dataset

    @sigma_dataset.setter
    def sigma_dataset(self, sigma_dataset: Optional[SigmaDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset = sigma_dataset

    class Attributes(Sigma.Attributes):
        sigma_dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="sigmaDatasetQualifiedName"
        )
        sigma_dataset_name: Optional[str] = Field(
            None, description="", alias="sigmaDatasetName"
        )
        sigma_dataset: Optional[SigmaDataset] = Field(
            None, description="", alias="sigmaDataset"
        )  # relationship

    attributes: "SigmaDatasetColumn.Attributes" = Field(
        default_factory=lambda: SigmaDatasetColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class SigmaDataset(Sigma):
    """Description"""

    type_name: str = Field("SigmaDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SigmaDataset":
            raise ValueError("must be SigmaDataset")
        return v

    def __setattr__(self, name, value):
        if name in SigmaDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SIGMA_DATASET_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "sigmaDatasetColumnCount", "sigmaDatasetColumnCount"
    )
    """
    TBC
    """

    SIGMA_DATASET_COLUMNS: ClassVar[RelationField] = RelationField(
        "sigmaDatasetColumns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "sigma_dataset_column_count",
        "sigma_dataset_columns",
    ]

    @property
    def sigma_dataset_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.sigma_dataset_column_count
        )

    @sigma_dataset_column_count.setter
    def sigma_dataset_column_count(self, sigma_dataset_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_column_count = sigma_dataset_column_count

    @property
    def sigma_dataset_columns(self) -> Optional[list[SigmaDatasetColumn]]:
        return (
            None if self.attributes is None else self.attributes.sigma_dataset_columns
        )

    @sigma_dataset_columns.setter
    def sigma_dataset_columns(
        self, sigma_dataset_columns: Optional[list[SigmaDatasetColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_columns = sigma_dataset_columns

    class Attributes(Sigma.Attributes):
        sigma_dataset_column_count: Optional[int] = Field(
            None, description="", alias="sigmaDatasetColumnCount"
        )
        sigma_dataset_columns: Optional[list[SigmaDatasetColumn]] = Field(
            None, description="", alias="sigmaDatasetColumns"
        )  # relationship

    attributes: "SigmaDataset.Attributes" = Field(
        default_factory=lambda: SigmaDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


SigmaDatasetColumn.Attributes.update_forward_refs()


SigmaDataset.Attributes.update_forward_refs()
