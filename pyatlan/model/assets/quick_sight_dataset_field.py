# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import QuickSightDatasetFieldType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .quick_sight import QuickSight


class QuickSightDatasetField(QuickSight):
    """Description"""

    type_name: str = Field(default="QuickSightDatasetField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDatasetField":
            raise ValueError("must be QuickSightDatasetField")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDatasetField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DATASET_FIELD_TYPE: ClassVar[KeywordField] = KeywordField(
        "quickSightDatasetFieldType", "quickSightDatasetFieldType"
    )
    """
    Datatype of this field, for example: STRING, INTEGER, etc.
    """
    QUICK_SIGHT_DATASET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "quickSightDatasetQualifiedName",
        "quickSightDatasetQualifiedName",
        "quickSightDatasetQualifiedName.text",
    )
    """
    Unique name of the dataset in which this field exists.
    """

    QUICK_SIGHT_DATASET: ClassVar[RelationField] = RelationField("quickSightDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "quick_sight_dataset_field_type",
        "quick_sight_dataset_qualified_name",
        "quick_sight_dataset",
    ]

    @property
    def quick_sight_dataset_field_type(self) -> Optional[QuickSightDatasetFieldType]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_field_type
        )

    @quick_sight_dataset_field_type.setter
    def quick_sight_dataset_field_type(
        self, quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_field_type = quick_sight_dataset_field_type

    @property
    def quick_sight_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_qualified_name
        )

    @quick_sight_dataset_qualified_name.setter
    def quick_sight_dataset_qualified_name(
        self, quick_sight_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_qualified_name = (
            quick_sight_dataset_qualified_name
        )

    @property
    def quick_sight_dataset(self) -> Optional[QuickSightDataset]:
        return None if self.attributes is None else self.attributes.quick_sight_dataset

    @quick_sight_dataset.setter
    def quick_sight_dataset(self, quick_sight_dataset: Optional[QuickSightDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset = quick_sight_dataset

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_field_type: Optional[QuickSightDatasetFieldType] = Field(
            default=None, description=""
        )
        quick_sight_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        quick_sight_dataset: Optional[QuickSightDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: QuickSightDatasetField.Attributes = Field(
        default_factory=lambda: QuickSightDatasetField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_dataset import QuickSightDataset  # noqa
