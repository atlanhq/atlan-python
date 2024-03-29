# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .b_i import BI


class Domo(BI):
    """Description"""

    type_name: str = Field(default="Domo", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Domo":
            raise ValueError("must be Domo")
        return v

    def __setattr__(self, name, value):
        if name in Domo._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DOMO_ID: ClassVar[KeywordField] = KeywordField("domoId", "domoId")
    """
    Id of the Domo dataset.
    """
    DOMO_OWNER_ID: ClassVar[KeywordField] = KeywordField("domoOwnerId", "domoOwnerId")
    """
    Id of the owner of the Domo dataset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "domo_id",
        "domo_owner_id",
    ]

    @property
    def domo_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.domo_id

    @domo_id.setter
    def domo_id(self, domo_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_id = domo_id

    @property
    def domo_owner_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.domo_owner_id

    @domo_owner_id.setter
    def domo_owner_id(self, domo_owner_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_owner_id = domo_owner_id

    class Attributes(BI.Attributes):
        domo_id: Optional[str] = Field(default=None, description="")
        domo_owner_id: Optional[str] = Field(default=None, description="")

    attributes: Domo.Attributes = Field(
        default_factory=lambda: Domo.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
