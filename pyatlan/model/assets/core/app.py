# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

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

    APP_APPLICATION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "appApplicationName", "appApplicationName.keyword", "appApplicationName"
    )
    """
    Simple name of the application in which this asset exists, or empty if it is itself an application.
    """
    APP_APPLICATION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "appApplicationQualifiedName", "appApplicationQualifiedName"
    )
    """
    Unique name of the application in which this asset exists, or empty if it is itself an application.
    """
    APP_COMPONENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "appComponentName", "appComponentName.keyword", "appComponentName"
    )
    """
    Simple name of the application component in which this asset exists, or empty if it is itself an application component.
    """  # noqa: E501
    APP_COMPONENT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "appComponentQualifiedName", "appComponentQualifiedName"
    )
    """
    Unique name of the application component in which this asset exists, or empty if it is itself an application component.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "app_application_name",
        "app_application_qualified_name",
        "app_component_name",
        "app_component_qualified_name",
    ]

    @property
    def app_application_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.app_application_name

    @app_application_name.setter
    def app_application_name(self, app_application_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_application_name = app_application_name

    @property
    def app_application_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_application_qualified_name
        )

    @app_application_qualified_name.setter
    def app_application_qualified_name(
        self, app_application_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_application_qualified_name = app_application_qualified_name

    @property
    def app_component_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.app_component_name

    @app_component_name.setter
    def app_component_name(self, app_component_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_component_name = app_component_name

    @property
    def app_component_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_component_qualified_name
        )

    @app_component_qualified_name.setter
    def app_component_qualified_name(self, app_component_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_component_qualified_name = app_component_qualified_name

    class Attributes(Catalog.Attributes):
        app_application_name: Optional[str] = Field(default=None, description="")
        app_application_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        app_component_name: Optional[str] = Field(default=None, description="")
        app_component_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: App.Attributes = Field(
        default_factory=lambda: App.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
