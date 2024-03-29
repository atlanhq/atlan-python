# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField

from .sigma import Sigma


class SigmaDatasetColumn(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaDatasetColumn", allow_mutation=False)

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
    Unique name of the dataset in which this column exists.
    """
    SIGMA_DATASET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "sigmaDatasetName", "sigmaDatasetName.keyword", "sigmaDatasetName"
    )
    """
    Simple name of the dataset in which this column exists.
    """

    SIGMA_DATASET: ClassVar[RelationField] = RelationField("sigmaDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
            default=None, description=""
        )
        sigma_dataset_name: Optional[str] = Field(default=None, description="")
        sigma_dataset: Optional[SigmaDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaDatasetColumn.Attributes = Field(
        default_factory=lambda: SigmaDatasetColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_dataset import SigmaDataset  # noqa
