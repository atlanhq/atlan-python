# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .domo import Domo


class DomoDataset(Domo):
    """Description"""

    type_name: str = Field(default="DomoDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DomoDataset":
            raise ValueError("must be DomoDataset")
        return v

    def __setattr__(self, name, value):
        if name in DomoDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DOMO_DATASET_ROW_COUNT: ClassVar[NumericField] = NumericField(
        "domoDatasetRowCount", "domoDatasetRowCount"
    )
    """
    Number of rows in the Domo dataset.
    """
    DOMO_DATASET_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "domoDatasetColumnCount", "domoDatasetColumnCount"
    )
    """
    Number of columns in the Domo dataset.
    """
    DOMO_DATASET_CARD_COUNT: ClassVar[NumericField] = NumericField(
        "domoDatasetCardCount", "domoDatasetCardCount"
    )
    """
    Number of cards linked to the Domo dataset.
    """
    DOMO_DATASET_LAST_RUN: ClassVar[KeywordField] = KeywordField(
        "domoDatasetLastRun", "domoDatasetLastRun"
    )
    """
    An ISO-8601 representation of the time the DataSet was last run.
    """

    DOMO_DATASET_COLUMNS: ClassVar[RelationField] = RelationField("domoDatasetColumns")
    """
    TBC
    """
    DOMO_CARDS: ClassVar[RelationField] = RelationField("domoCards")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "domo_dataset_row_count",
        "domo_dataset_column_count",
        "domo_dataset_card_count",
        "domo_dataset_last_run",
        "domo_dataset_columns",
        "domo_cards",
    ]

    @property
    def domo_dataset_row_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.domo_dataset_row_count
        )

    @domo_dataset_row_count.setter
    def domo_dataset_row_count(self, domo_dataset_row_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_row_count = domo_dataset_row_count

    @property
    def domo_dataset_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dataset_column_count
        )

    @domo_dataset_column_count.setter
    def domo_dataset_column_count(self, domo_dataset_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_column_count = domo_dataset_column_count

    @property
    def domo_dataset_card_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.domo_dataset_card_count
        )

    @domo_dataset_card_count.setter
    def domo_dataset_card_count(self, domo_dataset_card_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_card_count = domo_dataset_card_count

    @property
    def domo_dataset_last_run(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.domo_dataset_last_run
        )

    @domo_dataset_last_run.setter
    def domo_dataset_last_run(self, domo_dataset_last_run: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_last_run = domo_dataset_last_run

    @property
    def domo_dataset_columns(self) -> Optional[List[DomoDatasetColumn]]:
        return None if self.attributes is None else self.attributes.domo_dataset_columns

    @domo_dataset_columns.setter
    def domo_dataset_columns(
        self, domo_dataset_columns: Optional[List[DomoDatasetColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_columns = domo_dataset_columns

    @property
    def domo_cards(self) -> Optional[List[DomoCard]]:
        return None if self.attributes is None else self.attributes.domo_cards

    @domo_cards.setter
    def domo_cards(self, domo_cards: Optional[List[DomoCard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_cards = domo_cards

    class Attributes(Domo.Attributes):
        domo_dataset_row_count: Optional[int] = Field(default=None, description="")
        domo_dataset_column_count: Optional[int] = Field(default=None, description="")
        domo_dataset_card_count: Optional[int] = Field(default=None, description="")
        domo_dataset_last_run: Optional[str] = Field(default=None, description="")
        domo_dataset_columns: Optional[List[DomoDatasetColumn]] = Field(
            default=None, description=""
        )  # relationship
        domo_cards: Optional[List[DomoCard]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DomoDataset.Attributes = Field(
        default_factory=lambda: DomoDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .domo_card import DomoCard  # noqa
from .domo_dataset_column import DomoDatasetColumn  # noqa
