# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import  ClassVar, List, Optional, overload
from warnings import warn


from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    AtlanConnectorType,
)
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    RelationField,
)

from pyatlan.utils import (
    init_guid,
    validate_required_fields,
)


from .cognite import Cognite


class CogniteSequence(Cognite):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> CogniteSequence:
        validate_required_fields(
            ["name", "connection_qualified_name"],
            [name, connection_qualified_name],
        )
        attributes = CogniteSequence.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> CogniteSequence:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )

    type_name: str = Field(default="CogniteSequence", allow_mutation=False)

    @validator('type_name')
    def validate_type_name(cls, v):
        if v != "CogniteSequence":
            raise ValueError('must be CogniteSequence')
        return v

    def __setattr__(self, name, value):
        if name in CogniteSequence._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    EXTERNAL_ID: ClassVar[KeywordField] = KeywordField("externalId", "externalId")
    """

    """

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "external_id",
        "cognite_asset", ]

    @property
    def external_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.external_id

    @external_id.setter
    def external_id(self, external_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.external_id = external_id

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        external_id: Optional[str] = Field(default=None, description='')
        cognite_asset: Optional[CogniteAsset] = Field(default=None, description='')  # relationship

        @classmethod
        @init_guid
        def create(
                cls, *, name: str, connection_qualified_name: str
        ) -> CogniteSequence.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"],
                [name, connection_qualified_name],
            )
            return CogniteSequence.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: CogniteSequence.Attributes = Field(
        default_factory=lambda: CogniteSequence.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognite_asset import CogniteAsset  # noqa

CogniteSequence.Attributes.update_forward_refs()
