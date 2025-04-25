# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.b_i import BI


class Looker(BI):
    """Description"""

    type_name: str = Field(default="Looker", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Looker":
            raise ValueError("must be Looker")
        return v

    def __setattr__(self, name, value):
        if name in Looker._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    LOOKER_SLUG: ClassVar[KeywordField] = KeywordField("lookerSlug", "lookerSlug")
    """
    An alpha-numeric slug for the underlying Looker asset that can be used to uniquely identify it
    """

    _convenience_properties: ClassVar[List[str]] = [
        "looker_slug",
    ]

    @property
    def looker_slug(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.looker_slug

    @looker_slug.setter
    def looker_slug(self, looker_slug: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_slug = looker_slug

    class Attributes(BI.Attributes):
        looker_slug: Optional[str] = Field(default=None, description="")

    attributes: Looker.Attributes = Field(
        default_factory=lambda: Looker.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Looker.Attributes.update_forward_refs()
