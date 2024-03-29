# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .sigma import Sigma


class SigmaDataset(Sigma):
    """Description"""

    type_name: str = Field(default="SigmaDataset", allow_mutation=False)

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
    Number of columns in this dataset.
    """

    SIGMA_DATASET_COLUMNS: ClassVar[RelationField] = RelationField(
        "sigmaDatasetColumns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def sigma_dataset_columns(self) -> Optional[List[SigmaDatasetColumn]]:
        return (
            None if self.attributes is None else self.attributes.sigma_dataset_columns
        )

    @sigma_dataset_columns.setter
    def sigma_dataset_columns(
        self, sigma_dataset_columns: Optional[List[SigmaDatasetColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sigma_dataset_columns = sigma_dataset_columns

    class Attributes(Sigma.Attributes):
        sigma_dataset_column_count: Optional[int] = Field(default=None, description="")
        sigma_dataset_columns: Optional[List[SigmaDatasetColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SigmaDataset.Attributes = Field(
        default_factory=lambda: SigmaDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sigma_dataset_column import SigmaDatasetColumn  # noqa
