# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DomoCardType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .domo import Domo


class DomoCard(Domo):
    """Description"""

    type_name: str = Field(default="DomoCard", allow_mutation=False)

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

    _convenience_properties: ClassVar[List[str]] = [
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
    def domo_dashboards(self) -> Optional[List[DomoDashboard]]:
        return None if self.attributes is None else self.attributes.domo_dashboards

    @domo_dashboards.setter
    def domo_dashboards(self, domo_dashboards: Optional[List[DomoDashboard]]):
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
        domo_card_type: Optional[DomoCardType] = Field(default=None, description="")
        domo_card_type_value: Optional[str] = Field(default=None, description="")
        domo_card_dashboard_count: Optional[int] = Field(default=None, description="")
        domo_dashboards: Optional[List[DomoDashboard]] = Field(
            default=None, description=""
        )  # relationship
        domo_dataset: Optional[DomoDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: DomoCard.Attributes = Field(
        default_factory=lambda: DomoCard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .domo_dashboard import DomoDashboard  # noqa
from .domo_dataset import DomoDataset  # noqa
