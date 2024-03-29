# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .domo import Domo


class DomoDashboard(Domo):
    """Description"""

    type_name: str = Field(default="DomoDashboard", allow_mutation=False)

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

    _convenience_properties: ClassVar[List[str]] = [
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
    def domo_dashboard_children(self) -> Optional[List[DomoDashboard]]:
        return (
            None if self.attributes is None else self.attributes.domo_dashboard_children
        )

    @domo_dashboard_children.setter
    def domo_dashboard_children(
        self, domo_dashboard_children: Optional[List[DomoDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dashboard_children = domo_dashboard_children

    @property
    def domo_cards(self) -> Optional[List[DomoCard]]:
        return None if self.attributes is None else self.attributes.domo_cards

    @domo_cards.setter
    def domo_cards(self, domo_cards: Optional[List[DomoCard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_cards = domo_cards

    class Attributes(Domo.Attributes):
        domo_dashboard_card_count: Optional[int] = Field(default=None, description="")
        domo_dashboard_parent: Optional[DomoDashboard] = Field(
            default=None, description=""
        )  # relationship
        domo_dashboard_children: Optional[List[DomoDashboard]] = Field(
            default=None, description=""
        )  # relationship
        domo_cards: Optional[List[DomoCard]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DomoDashboard.Attributes = Field(
        default_factory=lambda: DomoDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .domo_card import DomoCard  # noqa
