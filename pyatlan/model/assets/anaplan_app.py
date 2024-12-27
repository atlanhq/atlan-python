# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .anaplan import Anaplan


class AnaplanApp(Anaplan):
    """Description"""

    type_name: str = Field(default="AnaplanApp", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanApp":
            raise ValueError("must be AnaplanApp")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanApp._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_PAGES: ClassVar[RelationField] = RelationField("anaplanPages")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_pages",
    ]

    @property
    def anaplan_pages(self) -> Optional[List[AnaplanPage]]:
        return None if self.attributes is None else self.attributes.anaplan_pages

    @anaplan_pages.setter
    def anaplan_pages(self, anaplan_pages: Optional[List[AnaplanPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_pages = anaplan_pages

    class Attributes(Anaplan.Attributes):
        anaplan_pages: Optional[List[AnaplanPage]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AnaplanApp.Attributes = Field(
        default_factory=lambda: AnaplanApp.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_page import AnaplanPage  # noqa

AnaplanApp.Attributes.update_forward_refs()
