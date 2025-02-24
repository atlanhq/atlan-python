# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .thoughtspot import Thoughtspot


class ThoughtspotWorksheet(Thoughtspot):
    """Description"""

    type_name: str = Field(default="ThoughtspotWorksheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ThoughtspotWorksheet":
            raise ValueError("must be ThoughtspotWorksheet")
        return v

    def __setattr__(self, name, value):
        if name in ThoughtspotWorksheet._convenience_properties:
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

    attributes: ThoughtspotWorksheet.Attributes = Field(
        default_factory=lambda: ThoughtspotWorksheet.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .thoughtspot_column import ThoughtspotColumn  # noqa

ThoughtspotWorksheet.Attributes.update_forward_refs()
