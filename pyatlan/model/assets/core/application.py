# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .app import App


class Application(App):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> Application:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = Application.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

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

    APPLICATION_OWNED_ASSETS: ClassVar[RelationField] = RelationField(
        "applicationOwnedAssets"
    )
    """
    TBC
    """
    APPLICATION_CHILD_FIELDS: ClassVar[RelationField] = RelationField(
        "applicationChildFields"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "application_owned_assets",
        "application_child_fields",
    ]

    @property
    def application_owned_assets(self) -> Optional[List[Asset]]:
        return (
            None
            if self.attributes is None
            else self.attributes.application_owned_assets
        )

    @application_owned_assets.setter
    def application_owned_assets(self, application_owned_assets: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.application_owned_assets = application_owned_assets

    @property
    def application_child_fields(self) -> Optional[List[ApplicationField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.application_child_fields
        )

    @application_child_fields.setter
    def application_child_fields(
        self, application_child_fields: Optional[List[ApplicationField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.application_child_fields = application_child_fields

    class Attributes(App.Attributes):
        application_owned_assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship
        application_child_fields: Optional[List[ApplicationField]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
        ) -> Application.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return Application.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: Application.Attributes = Field(
        default_factory=lambda: Application.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .application_field import ApplicationField  # noqa: E402, F401
from .asset import Asset  # noqa: E402, F401
