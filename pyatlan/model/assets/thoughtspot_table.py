# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .thoughtspot import Thoughtspot


class ThoughtspotTable(Thoughtspot):
    """Description"""

    type_name: str = Field(default="ThoughtspotTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotTable":
            raise ValueError("must be ThoughtspotTable")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_COLUMNS: ClassVar[RelationField] = RelationField("thoughtspotColumns")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "thoughtspot_columns",
    ]

    @property
    def thoughtspot_columns(self) -> Optional[List[ThoughtspotColumn]]:
        return None if self.attributes is None else self.attributes.thoughtspot_columns

    @thoughtspot_columns.setter
    def thoughtspot_columns(
        self, thoughtspot_columns: Optional[List[ThoughtspotColumn]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_columns = thoughtspot_columns

    class Attributes(Thoughtspot.Attributes):
        thoughtspot_columns: Optional[List[ThoughtspotColumn]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ThoughtspotTable.Attributes = Field(
        default_factory=lambda: ThoughtspotTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .thoughtspot_column import ThoughtspotColumn  # noqa
