# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .a_p_i import API


class APIObject(API):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> APIObject: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        api_field_count: int,
    ) -> APIObject: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        api_field_count: Optional[int] = None,
    ) -> APIObject:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = APIObject.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            api_field_count=api_field_count,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="APIObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APIObject":
            raise ValueError("must be APIObject")
        return v

    def __setattr__(self, name, value):
        if name in APIObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    API_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "apiFieldCount", "apiFieldCount"
    )
    """
    Count of the APIField of this object.
    """

    API_FIELDS: ClassVar[RelationField] = RelationField("apiFields")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "api_field_count",
        "api_fields",
    ]

    @property
    def api_field_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.api_field_count

    @api_field_count.setter
    def api_field_count(self, api_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_field_count = api_field_count

    @property
    def api_fields(self) -> Optional[List[APIField]]:
        return None if self.attributes is None else self.attributes.api_fields

    @api_fields.setter
    def api_fields(self, api_fields: Optional[List[APIField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_fields = api_fields

    class Attributes(API.Attributes):
        api_field_count: Optional[int] = Field(default=None, description="")
        api_fields: Optional[List[APIField]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            api_field_count: Optional[int] = None,
        ) -> APIObject.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return APIObject.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
                api_field_count=api_field_count,
            )

    attributes: APIObject.Attributes = Field(
        default_factory=lambda: APIObject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_p_i_field import APIField  # noqa

APIObject.Attributes.update_forward_refs()
