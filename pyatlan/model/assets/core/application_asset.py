# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .application import Application


class ApplicationAsset(Application):
    """Description"""

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

    attributes: ApplicationAsset.Attributes = Field(
        default_factory=lambda: ApplicationAsset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa
