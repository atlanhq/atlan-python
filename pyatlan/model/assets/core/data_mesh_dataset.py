# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DataMeshDatasetType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .data_mesh import DataMesh


class DataMeshDataset(DataMesh):
    """Description"""

    type_name: str = Field(default="DataMeshDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataMeshDataset":
            raise ValueError("must be DataMeshDataset")
        return v

    def __setattr__(self, name, value):
        if name in DataMeshDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_MESH_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "dataMeshDatasetType", "dataMeshDatasetType"
    )
    """
    Type classification of this dataset (Raw, Refined, or Aggregated).
    """

    DATA_MESH_DATA_PRODUCTS: ClassVar[RelationField] = RelationField(
        "dataMeshDataProducts"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_mesh_dataset_type",
        "data_mesh_data_products",
    ]

    @property
    def data_mesh_dataset_type(self) -> Optional[DataMeshDatasetType]:
        return (
            None if self.attributes is None else self.attributes.data_mesh_dataset_type
        )

    @data_mesh_dataset_type.setter
    def data_mesh_dataset_type(
        self, data_mesh_dataset_type: Optional[DataMeshDatasetType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_mesh_dataset_type = data_mesh_dataset_type

    @property
    def data_mesh_data_products(self) -> Optional[List[DataProduct]]:
        return (
            None if self.attributes is None else self.attributes.data_mesh_data_products
        )

    @data_mesh_data_products.setter
    def data_mesh_data_products(
        self, data_mesh_data_products: Optional[List[DataProduct]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_mesh_data_products = data_mesh_data_products

    class Attributes(DataMesh.Attributes):
        data_mesh_dataset_type: Optional[DataMeshDatasetType] = Field(
            default=None, description=""
        )
        data_mesh_data_products: Optional[List[DataProduct]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DataMeshDataset.Attributes = Field(
        default_factory=lambda: DataMeshDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .data_product import DataProduct  # noqa: E402, F401
