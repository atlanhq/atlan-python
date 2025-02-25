# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional
from uuid import uuid4

from pydantic.v1 import Field, validator

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.enums import IconType
from pyatlan.model.fields.atlan_fields import KeywordField, TextField
from pyatlan.utils import init_guid, validate_required_fields

from .core.namespace import Namespace


class Collection(Namespace):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, client: AtlanClient, name: str) -> Collection:
        validate_required_fields(["client", "name"], [client, name])
        return cls(attributes=Collection.Attributes.creator(client=client, name=name))

    @classmethod
    def _generate_qualified_name(cls, client: AtlanClient):
        """
        Generate a unique Collection name.

        :param client: connectivity to the Atlan tenant
        as the user who will own the Collection
        :returns: a unique name for the Collection
        """
        try:
            username = client.user.get_current().username
            return f"default/collection/{username}/{uuid4()}"
        except AtlanError as e:
            raise ErrorCode.UNABLE_TO_GENERATE_QN.exception_with_parameters(
                cls.__name__, e
            ) from e

    type_name: str = Field(default="Collection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Collection":
            raise ValueError("must be Collection")
        return v

    def __setattr__(self, name, value):
        if name in Collection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ICON: ClassVar[TextField] = TextField("icon", "icon")
    """
    Image used to represent this collection.
    """
    ICON_TYPE: ClassVar[KeywordField] = KeywordField("iconType", "iconType")
    """
    Type of image used to represent the collection (for example, an emoji).
    """

    _convenience_properties: ClassVar[List[str]] = [
        "icon",
        "icon_type",
    ]

    @property
    def icon(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.icon

    @icon.setter
    def icon(self, icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon = icon

    @property
    def icon_type(self) -> Optional[IconType]:
        return None if self.attributes is None else self.attributes.icon_type

    @icon_type.setter
    def icon_type(self, icon_type: Optional[IconType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon_type = icon_type

    class Attributes(Namespace.Attributes):
        icon: Optional[str] = Field(default=None, description="")
        icon_type: Optional[IconType] = Field(default=None, description="")

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            client: AtlanClient,
            name: str,
        ) -> Collection.Attributes:
            validate_required_fields(["name"], [name])
            return Collection.Attributes(
                name=name,
                qualified_name=Collection._generate_qualified_name(client),
            )

    attributes: Collection.Attributes = Field(
        default_factory=lambda: Collection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Collection.Attributes.update_forward_refs()
