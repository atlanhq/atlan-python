# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .app import App


class AppApplication(App):
    """Description"""

    type_name: str = Field(default="AppApplication", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AppApplication":
            raise ValueError("must be AppApplication")
        return v

    def __setattr__(self, name, value):
        if name in AppApplication._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    APP_COMPONENT_COUNT: ClassVar[NumericField] = NumericField(
        "appComponentCount", "appComponentCount"
    )
    """
    Number of components in the application.
    """

    APP_COMPONENTS: ClassVar[RelationField] = RelationField("appComponents")
    """
    TBC
    """
    APP_IMPLEMENTED_BY_ASSETS: ClassVar[RelationField] = RelationField(
        "appImplementedByAssets"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "app_component_count",
        "app_components",
        "app_implemented_by_assets",
    ]

    @property
    def app_component_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.app_component_count

    @app_component_count.setter
    def app_component_count(self, app_component_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_component_count = app_component_count

    @property
    def app_components(self) -> Optional[List[AppComponent]]:
        return None if self.attributes is None else self.attributes.app_components

    @app_components.setter
    def app_components(self, app_components: Optional[List[AppComponent]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_components = app_components

    @property
    def app_implemented_by_assets(self) -> Optional[List[Catalog]]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_implemented_by_assets
        )

    @app_implemented_by_assets.setter
    def app_implemented_by_assets(
        self, app_implemented_by_assets: Optional[List[Catalog]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_implemented_by_assets = app_implemented_by_assets

    class Attributes(App.Attributes):
        app_component_count: Optional[int] = Field(default=None, description="")
        app_components: Optional[List[AppComponent]] = Field(
            default=None, description=""
        )  # relationship
        app_implemented_by_assets: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AppApplication.Attributes = Field(
        default_factory=lambda: AppApplication.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .app_component import AppComponent  # noqa
from .catalog import Catalog  # noqa
