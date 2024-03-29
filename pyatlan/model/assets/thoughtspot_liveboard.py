# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .thoughtspot import Thoughtspot


class ThoughtspotLiveboard(Thoughtspot):
    """Description"""

    type_name: str = Field(default="ThoughtspotLiveboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotLiveboard":
            raise ValueError("must be ThoughtspotLiveboard")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotLiveboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_DASHLETS: ClassVar[RelationField] = RelationField("thoughtspotDashlets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "thoughtspot_dashlets",
    ]

    @property
    def thoughtspot_dashlets(self) -> Optional[List[ThoughtspotDashlet]]:
        return None if self.attributes is None else self.attributes.thoughtspot_dashlets

    @thoughtspot_dashlets.setter
    def thoughtspot_dashlets(
        self, thoughtspot_dashlets: Optional[List[ThoughtspotDashlet]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_dashlets = thoughtspot_dashlets

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_dashlets: Optional[List[ThoughtspotDashlet]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ThoughtspotLiveboard.Attributes = Field(
        default_factory=lambda: ThoughtspotLiveboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .thoughtspot_dashlet import ThoughtspotDashlet  # noqa
