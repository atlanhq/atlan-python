# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .app import App


class AppComponent(App):
    """Description"""

    type_name: str = Field(default="AppComponent", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AppComponent":
            raise ValueError("must be AppComponent")
        return v

    def __setattr__(self, name, value):
        if name in AppComponent._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    APP_APPLICATION: ClassVar[RelationField] = RelationField("appApplication")
    """
    TBC
    """
    APP_COMPONENT_IMPLEMENTED_BY_ASSET: ClassVar[RelationField] = RelationField(
        "appComponentImplementedByAsset"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "app_application",
        "app_component_implemented_by_asset",
    ]

    @property
    def app_application(self) -> Optional[AppApplication]:
        return None if self.attributes is None else self.attributes.app_application

    @app_application.setter
    def app_application(self, app_application: Optional[AppApplication]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_application = app_application

    @property
    def app_component_implemented_by_asset(self) -> Optional[Catalog]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_component_implemented_by_asset
        )

    @app_component_implemented_by_asset.setter
    def app_component_implemented_by_asset(
        self, app_component_implemented_by_asset: Optional[Catalog]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_component_implemented_by_asset = (
            app_component_implemented_by_asset
        )

    class Attributes(App.Attributes):
        app_application: Optional[AppApplication] = Field(
            default=None, description=""
        )  # relationship
        app_component_implemented_by_asset: Optional[Catalog] = Field(
            default=None, description=""
        )  # relationship

    attributes: AppComponent.Attributes = Field(
        default_factory=lambda: AppComponent.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .app_application import AppApplication  # noqa
from .catalog import Catalog  # noqa
