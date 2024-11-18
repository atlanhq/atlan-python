# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .application import Application


class ApplicationContainer(Application):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> ApplicationContainer:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = ApplicationContainer.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="ApplicationContainer", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ApplicationContainer":
            raise ValueError("must be ApplicationContainer")
        return v

    def __setattr__(self, name, value):
        if name in ApplicationContainer._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    APPLICATION_OWNED_ASSETS: ClassVar[RelationField] = RelationField(
        "applicationOwnedAssets"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "application_owned_assets",
    ]

    @property
    def application_owned_assets(self) -> Optional[List[Catalog]]:
        return (
            None
            if self.attributes is None
            else self.attributes.application_owned_assets
        )

    @application_owned_assets.setter
    def application_owned_assets(
        self, application_owned_assets: Optional[List[Catalog]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.application_owned_assets = application_owned_assets

    class Attributes(Application.Attributes):
        application_owned_assets: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
        ) -> ApplicationContainer.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return ApplicationContainer.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: ApplicationContainer.Attributes = Field(
        default_factory=lambda: ApplicationContainer.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa
