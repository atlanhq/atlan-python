# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .catalog import Catalog


class Matillion(Catalog):
    """Description"""

    type_name: str = Field(default="Matillion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Matillion":
            raise ValueError("must be Matillion")
        return v

    def __setattr__(self, name, value):
        if name in Matillion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_VERSION: ClassVar[KeywordField] = KeywordField(
        "matillionVersion", "matillionVersion"
    )
    """
    Current point in time state of a project.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "matillion_version",
    ]

    @property
    def matillion_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.matillion_version

    @matillion_version.setter
    def matillion_version(self, matillion_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_version = matillion_version

    class Attributes(Catalog.Attributes):
        matillion_version: Optional[str] = Field(default=None, description="")

    attributes: Matillion.Attributes = Field(
        default_factory=lambda: Matillion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
