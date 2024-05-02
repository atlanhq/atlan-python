# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import QuickSightDatasetImportMode
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .quick_sight import QuickSight


class QuickSightDataset(QuickSight):
    """Description"""

    type_name: str = Field(default="QuickSightDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "QuickSightDataset":
            raise ValueError("must be QuickSightDataset")
        return v

    def __setattr__(self, name, value):
        if name in QuickSightDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    QUICK_SIGHT_DATASET_IMPORT_MODE: ClassVar[KeywordField] = KeywordField(
        "quickSightDatasetImportMode", "quickSightDatasetImportMode"
    )
    """
    Import mode for this dataset, for example: SPICE or DIRECT_QUERY.
    """
    QUICK_SIGHT_DATASET_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "quickSightDatasetColumnCount", "quickSightDatasetColumnCount"
    )
    """
    Number of columns present in this dataset.
    """

    QUICK_SIGHT_DATASET_FOLDERS: ClassVar[RelationField] = RelationField(
        "quickSightDatasetFolders"
    )
    """
    TBC
    """
    QUICK_SIGHT_DATASET_FIELDS: ClassVar[RelationField] = RelationField(
        "quickSightDatasetFields"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "quick_sight_dataset_import_mode",
        "quick_sight_dataset_column_count",
        "quick_sight_dataset_folders",
        "quick_sight_dataset_fields",
    ]

    @property
    def quick_sight_dataset_import_mode(self) -> Optional[QuickSightDatasetImportMode]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_import_mode
        )

    @quick_sight_dataset_import_mode.setter
    def quick_sight_dataset_import_mode(
        self, quick_sight_dataset_import_mode: Optional[QuickSightDatasetImportMode]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_import_mode = (
            quick_sight_dataset_import_mode
        )

    @property
    def quick_sight_dataset_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_column_count
        )

    @quick_sight_dataset_column_count.setter
    def quick_sight_dataset_column_count(
        self, quick_sight_dataset_column_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_column_count = (
            quick_sight_dataset_column_count
        )

    @property
    def quick_sight_dataset_folders(self) -> Optional[List[QuickSightFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_folders
        )

    @quick_sight_dataset_folders.setter
    def quick_sight_dataset_folders(
        self, quick_sight_dataset_folders: Optional[List[QuickSightFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_folders = quick_sight_dataset_folders

    @property
    def quick_sight_dataset_fields(self) -> Optional[List[QuickSightDatasetField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.quick_sight_dataset_fields
        )

    @quick_sight_dataset_fields.setter
    def quick_sight_dataset_fields(
        self, quick_sight_dataset_fields: Optional[List[QuickSightDatasetField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.quick_sight_dataset_fields = quick_sight_dataset_fields

    class Attributes(QuickSight.Attributes):
        quick_sight_dataset_import_mode: Optional[QuickSightDatasetImportMode] = Field(
            default=None, description=""
        )
        quick_sight_dataset_column_count: Optional[int] = Field(
            default=None, description=""
        )
        quick_sight_dataset_folders: Optional[List[QuickSightFolder]] = Field(
            default=None, description=""
        )  # relationship
        quick_sight_dataset_fields: Optional[List[QuickSightDatasetField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: QuickSightDataset.Attributes = Field(
        default_factory=lambda: QuickSightDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .quick_sight_dataset_field import QuickSightDatasetField  # noqa
from .quick_sight_folder import QuickSightFolder  # noqa
