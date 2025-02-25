# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .catalog import Catalog


class App(Catalog):
    """Description"""

    type_name: str = Field(default="App", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "App":
            raise ValueError("must be App")
        return v

    def __setattr__(self, name, value):
        if name in App._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    APP_ID: ClassVar[KeywordField] = KeywordField("appId", "appId")
    """
    Unique identifier for the App asset from the source system.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "app_id",
    ]

    @property
    def app_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.app_id

    @app_id.setter
    def app_id(self, app_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_id = app_id

    class Attributes(Catalog.Attributes):
        app_id: Optional[str] = Field(default=None, description="")

    attributes: App.Attributes = Field(
        default_factory=lambda: App.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
