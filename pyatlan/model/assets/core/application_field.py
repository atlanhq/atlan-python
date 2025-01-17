# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .app import App


class ApplicationField(App):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        application_qualified_name: str,
    ) -> ApplicationField: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        application_qualified_name: str,
        connection_qualified_name: str,
    ) -> ApplicationField: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        application_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> ApplicationField:
        validate_required_fields(
            ["name", "application_qualified_name"], [name, application_qualified_name]
        )
        attributes = ApplicationField.Attributes.create(
            name=name,
            application_qualified_name=application_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="ApplicationField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ApplicationField":
            raise ValueError("must be ApplicationField")
        return v

    def __setattr__(self, name, value):
        if name in ApplicationField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARENT_APPLICATION: ClassVar[RelationField] = RelationField("parentApplication")
    """
    TBC
    """
    APPLICATION_FIELD_OWNED_ASSETS: ClassVar[RelationField] = RelationField(
        "applicationFieldOwnedAssets"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "parent_application",
        "application_field_owned_assets",
    ]

    @property
    def parent_application(self) -> Optional[Application]:
        return None if self.attributes is None else self.attributes.parent_application

    @parent_application.setter
    def parent_application(self, parent_application: Optional[Application]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_application = parent_application

    @property
    def application_field_owned_assets(self) -> Optional[List[Asset]]:
        return (
            None
            if self.attributes is None
            else self.attributes.application_field_owned_assets
        )

    @application_field_owned_assets.setter
    def application_field_owned_assets(
        self, application_field_owned_assets: Optional[List[Asset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.application_field_owned_assets = application_field_owned_assets

    class Attributes(App.Attributes):
        parent_application: Optional[Application] = Field(
            default=None, description=""
        )  # relationship
        application_field_owned_assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            application_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> ApplicationField.Attributes:
            validate_required_fields(
                ["name", "application_qualified_name"],
                [name, application_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    application_qualified_name, "application_qualified_name", 4
                )

            return ApplicationField.Attributes(
                name=name,
                qualified_name=f"{application_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name or connection_qn,
                connector_name=connector_name,
                parent_application=Application.ref_by_qualified_name(
                    application_qualified_name
                ),
            )

    attributes: ApplicationField.Attributes = Field(
        default_factory=lambda: ApplicationField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .application import Application  # noqa
from .asset import Asset  # noqa
