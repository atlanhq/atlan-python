# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField

from .asset18 import BI


class Redash(BI):
    """Description"""

    type_name: str = Field("Redash", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Redash":
            raise ValueError("must be Redash")
        return v

    def __setattr__(self, name, value):
        if name in Redash._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    REDASH_IS_PUBLISHED: ClassVar[BooleanField] = BooleanField(
        "redashIsPublished", "redashIsPublished"
    )
    """
    Status whether the asset is published or not on source
    """

    _convenience_properties: ClassVar[list[str]] = [
        "redash_is_published",
    ]

    @property
    def redash_is_published(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.redash_is_published

    @redash_is_published.setter
    def redash_is_published(self, redash_is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.redash_is_published = redash_is_published

    class Attributes(BI.Attributes):
        redash_is_published: Optional[bool] = Field(
            None, description="", alias="redashIsPublished"
        )

    attributes: "Redash.Attributes" = Field(
        default_factory=lambda: Redash.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Redash.Attributes.update_forward_refs()
