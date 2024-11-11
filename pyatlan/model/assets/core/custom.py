# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .catalog import Catalog


class Custom(Catalog):
    """Description"""

    type_name: str = Field(default="Custom", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Custom":
            raise ValueError("must be Custom")
        return v

    def __setattr__(self, name, value):
        if name in Custom._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUSTOM_SOURCE_ID: ClassVar[KeywordField] = KeywordField(
        "customSourceId", "customSourceId"
    )
    """
    Unique identifier for the Custom asset from the source system.
    """
    CUSTOM_DATASET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "customDatasetName", "customDatasetName.keyword", "customDatasetName"
    )
    """
    Simple name of the dataset in which this asset exists, or empty if it is itself a dataset.
    """
    CUSTOM_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "customDatasetQualifiedName", "customDatasetQualifiedName"
    )
    """
    Unique name of the dataset in which this asset exists, or empty if it is itself a dataset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "custom_source_id",
        "custom_dataset_name",
        "custom_dataset_qualified_name",
    ]

    @property
    def custom_source_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.custom_source_id

    @custom_source_id.setter
    def custom_source_id(self, custom_source_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_source_id = custom_source_id

    @property
    def custom_dataset_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.custom_dataset_name

    @custom_dataset_name.setter
    def custom_dataset_name(self, custom_dataset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_dataset_name = custom_dataset_name

    @property
    def custom_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.custom_dataset_qualified_name
        )

    @custom_dataset_qualified_name.setter
    def custom_dataset_qualified_name(
        self, custom_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_dataset_qualified_name = custom_dataset_qualified_name

    class Attributes(Catalog.Attributes):
        custom_source_id: Optional[str] = Field(default=None, description="")
        custom_dataset_name: Optional[str] = Field(default=None, description="")
        custom_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: Custom.Attributes = Field(
        default_factory=lambda: Custom.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
