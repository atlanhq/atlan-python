# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .application import Application


class ApplicationAsset(Application):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> ApplicationAsset: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        application_id: str,
    ) -> ApplicationAsset: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        application_id: str,
        application_catalog_list: List[Catalog],
    ) -> ApplicationAsset: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        application_id: Optional[str] = None,
        application_catalog_list: Optional[List[Catalog]] = None,
    ) -> ApplicationAsset:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = ApplicationAsset.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            application_id=application_id,
            application_catalog_list=application_catalog_list,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="ApplicationAsset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ApplicationAsset":
            raise ValueError("must be ApplicationAsset")
        return v

    def __setattr__(self, name, value):
        if name in ApplicationAsset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    APPLICATION_CATALOG: ClassVar[RelationField] = RelationField("applicationCatalog")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "application_catalog",
    ]

    @property
    def application_catalog(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.application_catalog

    @application_catalog.setter
    def application_catalog(self, application_catalog: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.application_catalog = application_catalog

    class Attributes(Application.Attributes):
        application_catalog: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            application_id: Optional[str] = None,
            application_catalog_list: Optional[List[Catalog]] = None,
        ) -> ApplicationAsset.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return ApplicationAsset.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
                application_id=application_id,
                application_catalog=application_catalog_list,
            )

    attributes: ApplicationAsset.Attributes = Field(
        default_factory=lambda: ApplicationAsset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa
