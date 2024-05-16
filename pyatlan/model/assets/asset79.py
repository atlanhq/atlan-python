# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.enums import DomoCardType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .asset47 import Domo


class DomoDataset(Domo):
    """Description"""

    type_name: str = Field("DomoDataset", allow_mutation=False)

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

    _convenience_properties: ClassVar[list[str]] = [
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
    def domo_dataset_columns(self) -> Optional[list[DomoDatasetColumn]]:
        return None if self.attributes is None else self.attributes.domo_dataset_columns

    @domo_dataset_columns.setter
    def domo_dataset_columns(
        self, domo_dataset_columns: Optional[list[DomoDatasetColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_columns = domo_dataset_columns

    @property
    def domo_cards(self) -> Optional[list[DomoCard]]:
        return None if self.attributes is None else self.attributes.domo_cards

    @domo_cards.setter
    def domo_cards(self, domo_cards: Optional[list[DomoCard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_cards = domo_cards

    class Attributes(Domo.Attributes):
        domo_dataset_row_count: Optional[int] = Field(
            None, description="", alias="domoDatasetRowCount"
        )
        domo_dataset_column_count: Optional[int] = Field(
            None, description="", alias="domoDatasetColumnCount"
        )
        domo_dataset_card_count: Optional[int] = Field(
            None, description="", alias="domoDatasetCardCount"
        )
        domo_dataset_last_run: Optional[str] = Field(
            None, description="", alias="domoDatasetLastRun"
        )
        domo_dataset_columns: Optional[list[DomoDatasetColumn]] = Field(
            None, description="", alias="domoDatasetColumns"
        )  # relationship
        domo_cards: Optional[list[DomoCard]] = Field(
            None, description="", alias="domoCards"
        )  # relationship

    attributes: "DomoDataset.Attributes" = Field(
        default_factory=lambda: DomoDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DomoCard(Domo):
    """Description"""

    type_name: str = Field("DomoCard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DomoCard":
            raise ValueError("must be DomoCard")
        return v

    def __setattr__(self, name, value):
        if name in DomoCard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DOMO_CARD_TYPE: ClassVar[KeywordField] = KeywordField(
        "domoCardType", "domoCardType"
    )
    """
    Type of the Domo Card.
    """
    DOMO_CARD_TYPE_VALUE: ClassVar[KeywordField] = KeywordField(
        "domoCardTypeValue", "domoCardTypeValue"
    )
    """
    Type of the Domo Card.
    """
    DOMO_CARD_DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "domoCardDashboardCount", "domoCardDashboardCount"
    )
    """
    Number of dashboards linked to this card.
    """

    DOMO_DASHBOARDS: ClassVar[RelationField] = RelationField("domoDashboards")
    """
    TBC
    """
    DOMO_DATASET: ClassVar[RelationField] = RelationField("domoDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "domo_card_type",
        "domo_card_type_value",
        "domo_card_dashboard_count",
        "domo_dashboards",
        "domo_dataset",
    ]

    @property
    def domo_card_type(self) -> Optional[DomoCardType]:
        return None if self.attributes is None else self.attributes.domo_card_type

    @domo_card_type.setter
    def domo_card_type(self, domo_card_type: Optional[DomoCardType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_card_type = domo_card_type

    @property
    def domo_card_type_value(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.domo_card_type_value

    @domo_card_type_value.setter
    def domo_card_type_value(self, domo_card_type_value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_card_type_value = domo_card_type_value

    @property
    def domo_card_dashboard_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_card_dashboard_count
        )

    @domo_card_dashboard_count.setter
    def domo_card_dashboard_count(self, domo_card_dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_card_dashboard_count = domo_card_dashboard_count

    @property
    def domo_dashboards(self) -> Optional[list[DomoDashboard]]:
        return None if self.attributes is None else self.attributes.domo_dashboards

    @domo_dashboards.setter
    def domo_dashboards(self, domo_dashboards: Optional[list[DomoDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dashboards = domo_dashboards

    @property
    def domo_dataset(self) -> Optional[DomoDataset]:
        return None if self.attributes is None else self.attributes.domo_dataset

    @domo_dataset.setter
    def domo_dataset(self, domo_dataset: Optional[DomoDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset = domo_dataset

    class Attributes(Domo.Attributes):
        domo_card_type: Optional[DomoCardType] = Field(
            None, description="", alias="domoCardType"
        )
        domo_card_type_value: Optional[str] = Field(
            None, description="", alias="domoCardTypeValue"
        )
        domo_card_dashboard_count: Optional[int] = Field(
            None, description="", alias="domoCardDashboardCount"
        )
        domo_dashboards: Optional[list[DomoDashboard]] = Field(
            None, description="", alias="domoDashboards"
        )  # relationship
        domo_dataset: Optional[DomoDataset] = Field(
            None, description="", alias="domoDataset"
        )  # relationship

    attributes: "DomoCard.Attributes" = Field(
        default_factory=lambda: DomoCard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DomoDatasetColumn(Domo):
    """Description"""

    type_name: str = Field("DomoDatasetColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DomoDatasetColumn":
            raise ValueError("must be DomoDatasetColumn")
        return v

    def __setattr__(self, name, value):
        if name in DomoDatasetColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DOMO_DATASET_COLUMN_TYPE: ClassVar[KeywordField] = KeywordField(
        "domoDatasetColumnType", "domoDatasetColumnType"
    )
    """
    Type of Domo Dataset Column.
    """
    DOMO_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "domoDatasetQualifiedName", "domoDatasetQualifiedName"
    )
    """
    Qualified name of domo dataset of this column.
    """

    DOMO_DATASET: ClassVar[RelationField] = RelationField("domoDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "domo_dataset_column_type",
        "domo_dataset_qualified_name",
        "domo_dataset",
    ]

    @property
    def domo_dataset_column_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dataset_column_type
        )

    @domo_dataset_column_type.setter
    def domo_dataset_column_type(self, domo_dataset_column_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_column_type = domo_dataset_column_type

    @property
    def domo_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dataset_qualified_name
        )

    @domo_dataset_qualified_name.setter
    def domo_dataset_qualified_name(self, domo_dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_qualified_name = domo_dataset_qualified_name

    @property
    def domo_dataset(self) -> Optional[DomoDataset]:
        return None if self.attributes is None else self.attributes.domo_dataset

    @domo_dataset.setter
    def domo_dataset(self, domo_dataset: Optional[DomoDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset = domo_dataset

    class Attributes(Domo.Attributes):
        domo_dataset_column_type: Optional[str] = Field(
            None, description="", alias="domoDatasetColumnType"
        )
        domo_dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="domoDatasetQualifiedName"
        )
        domo_dataset: Optional[DomoDataset] = Field(
            None, description="", alias="domoDataset"
        )  # relationship

    attributes: "DomoDatasetColumn.Attributes" = Field(
        default_factory=lambda: DomoDatasetColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class DomoDashboard(Domo):
    """Description"""

    type_name: str = Field("DomoDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DomoDashboard":
            raise ValueError("must be DomoDashboard")
        return v

    def __setattr__(self, name, value):
        if name in DomoDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DOMO_DASHBOARD_CARD_COUNT: ClassVar[NumericField] = NumericField(
        "domoDashboardCardCount", "domoDashboardCardCount"
    )
    """
    Number of cards linked to this dashboard.
    """

    DOMO_DASHBOARD_PARENT: ClassVar[RelationField] = RelationField(
        "domoDashboardParent"
    )
    """
    TBC
    """
    DOMO_DASHBOARD_CHILDREN: ClassVar[RelationField] = RelationField(
        "domoDashboardChildren"
    )
    """
    TBC
    """
    DOMO_CARDS: ClassVar[RelationField] = RelationField("domoCards")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "domo_dashboard_card_count",
        "domo_dashboard_parent",
        "domo_dashboard_children",
        "domo_cards",
    ]

    @property
    def domo_dashboard_card_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dashboard_card_count
        )

    @domo_dashboard_card_count.setter
    def domo_dashboard_card_count(self, domo_dashboard_card_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dashboard_card_count = domo_dashboard_card_count

    @property
    def domo_dashboard_parent(self) -> Optional[DomoDashboard]:
        return (
            None if self.attributes is None else self.attributes.domo_dashboard_parent
        )

    @domo_dashboard_parent.setter
    def domo_dashboard_parent(self, domo_dashboard_parent: Optional[DomoDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dashboard_parent = domo_dashboard_parent

    @property
    def domo_dashboard_children(self) -> Optional[list[DomoDashboard]]:
        return (
            None if self.attributes is None else self.attributes.domo_dashboard_children
        )

    @domo_dashboard_children.setter
    def domo_dashboard_children(
        self, domo_dashboard_children: Optional[list[DomoDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dashboard_children = domo_dashboard_children

    @property
    def domo_cards(self) -> Optional[list[DomoCard]]:
        return None if self.attributes is None else self.attributes.domo_cards

    @domo_cards.setter
    def domo_cards(self, domo_cards: Optional[list[DomoCard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_cards = domo_cards

    class Attributes(Domo.Attributes):
        domo_dashboard_card_count: Optional[int] = Field(
            None, description="", alias="domoDashboardCardCount"
        )
        domo_dashboard_parent: Optional[DomoDashboard] = Field(
            None, description="", alias="domoDashboardParent"
        )  # relationship
        domo_dashboard_children: Optional[list[DomoDashboard]] = Field(
            None, description="", alias="domoDashboardChildren"
        )  # relationship
        domo_cards: Optional[list[DomoCard]] = Field(
            None, description="", alias="domoCards"
        )  # relationship

    attributes: "DomoDashboard.Attributes" = Field(
        default_factory=lambda: DomoDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


DomoDataset.Attributes.update_forward_refs()


DomoCard.Attributes.update_forward_refs()


DomoDatasetColumn.Attributes.update_forward_refs()


DomoDashboard.Attributes.update_forward_refs()
