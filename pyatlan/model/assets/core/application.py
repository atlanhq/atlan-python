# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .catalog import Catalog


class Application(Catalog):
    """Description"""

    type_name: str = Field(default="Application", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Application":
            raise ValueError("must be Application")
        return v

    def __setattr__(self, name, value):
        if name in Application._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    APPLICATION_ID: ClassVar[KeywordField] = KeywordField(
        "applicationId", "applicationId"
    )
    """
    Unique identifier for the Application asset from the source system.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "application_id",
    ]

    @property
    def application_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.application_id

    @application_id.setter
    def application_id(self, application_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.application_id = application_id

    class Attributes(Catalog.Attributes):
        application_id: Optional[str] = Field(default=None, description="")

    attributes: Application.Attributes = Field(
        default_factory=lambda: Application.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
