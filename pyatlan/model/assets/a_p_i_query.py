# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .a_p_i import API


class APIQuery(API):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
    ) -> APIQuery: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        api_input_field_count: int,
    ) -> APIQuery: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        api_input_field_count: int,
        api_query_output_type: str,
        api_query_output_type_secondary: str,
    ) -> APIQuery: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        api_input_field_count: int,
        api_query_output_type: str,
        api_query_output_type_secondary: str,
        is_object_reference: bool,
        reference_api_object_qualified_name: str,
    ) -> APIQuery: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        api_input_field_count: Optional[int] = None,
        api_query_output_type: Optional[str] = None,
        api_query_output_type_secondary: Optional[str] = None,
        is_object_reference: Optional[bool] = False,
        reference_api_object_qualified_name: Optional[str] = None,
    ) -> APIQuery:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        # is api object reference - checker
        if is_object_reference:
            if not reference_api_object_qualified_name or (
                isinstance(reference_api_object_qualified_name, str)
                and not reference_api_object_qualified_name.strip()
            ):
                raise ValueError(
                    "Set valid qualified name for reference_api_object_qualified_name when is_object_reference is true"
                )
        else:
            if (
                reference_api_object_qualified_name
                and isinstance(reference_api_object_qualified_name, str)
                and reference_api_object_qualified_name.strip()
            ):
                raise ValueError(
                    "Set is_object_reference to true to set reference_api_object_qualified_name"
                )

        attributes = APIQuery.Attributes.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            api_input_field_count=api_input_field_count,
            api_query_output_type=api_query_output_type,
            api_query_output_type_secondary=api_query_output_type_secondary,
            is_object_reference=is_object_reference,
            reference_api_object_qualified_name=reference_api_object_qualified_name,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="APIQuery", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APIQuery":
            raise ValueError("must be APIQuery")
        return v

    def __setattr__(self, name, value):
        if name in APIQuery._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    API_INPUT_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "apiInputFieldCount", "apiInputFieldCount"
    )
    """
    Count of the APIField of this query that are input to it.
    """
    API_QUERY_OUTPUT_TYPE: ClassVar[KeywordField] = KeywordField(
        "apiQueryOutputType", "apiQueryOutputType"
    )
    """
    Type of APIQueryOutput. E.g. STRING, NUMBER etc. It is free text.
    """
    API_QUERY_OUTPUT_TYPE_SECONDARY: ClassVar[KeywordField] = KeywordField(
        "apiQueryOutputTypeSecondary", "apiQueryOutputTypeSecondary"
    )
    """
    Secondary Type of APIQueryOutput. E.g. LIST/STRING then LIST would be the secondary type.
    """

    API_FIELDS: ClassVar[RelationField] = RelationField("apiFields")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "api_input_field_count",
        "api_query_output_type",
        "api_query_output_type_secondary",
        "api_fields",
    ]

    @property
    def api_input_field_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.api_input_field_count
        )

    @api_input_field_count.setter
    def api_input_field_count(self, api_input_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_input_field_count = api_input_field_count

    @property
    def api_query_output_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.api_query_output_type
        )

    @api_query_output_type.setter
    def api_query_output_type(self, api_query_output_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_query_output_type = api_query_output_type

    @property
    def api_query_output_type_secondary(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_query_output_type_secondary
        )

    @api_query_output_type_secondary.setter
    def api_query_output_type_secondary(
        self, api_query_output_type_secondary: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_query_output_type_secondary = (
            api_query_output_type_secondary
        )

    @property
    def api_fields(self) -> Optional[List[APIField]]:
        return None if self.attributes is None else self.attributes.api_fields

    @api_fields.setter
    def api_fields(self, api_fields: Optional[List[APIField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_fields = api_fields

    class Attributes(API.Attributes):
        api_input_field_count: Optional[int] = Field(default=None, description="")
        api_query_output_type: Optional[str] = Field(default=None, description="")
        api_query_output_type_secondary: Optional[str] = Field(
            default=None, description=""
        )
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
            api_input_field_count: Optional[int] = None,
            api_query_output_type: Optional[str] = None,
            api_query_output_type_secondary: Optional[str] = None,
            is_object_reference: Optional[bool] = False,
            reference_api_object_qualified_name: Optional[str] = None,
        ) -> APIQuery.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            # is api object reference - checker
            if is_object_reference:
                if not reference_api_object_qualified_name or (
                    isinstance(reference_api_object_qualified_name, str)
                    and not reference_api_object_qualified_name.strip()
                ):
                    raise ValueError(
                        "Set valid qualified name for reference_api_object_qualified_name"
                    )
            else:
                if (
                    reference_api_object_qualified_name
                    and isinstance(reference_api_object_qualified_name, str)
                    and reference_api_object_qualified_name.strip()
                ):
                    raise ValueError(
                        "Set is_object_reference to true to set reference_api_object_qualified_name"
                    )

            return APIQuery.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
                api_input_field_count=api_input_field_count,
                api_query_output_type=api_query_output_type,
                api_query_output_type_secondary=api_query_output_type_secondary,
                api_is_object_reference=is_object_reference,
                api_object_qualified_name=(
                    reference_api_object_qualified_name if is_object_reference else None
                ),
            )

    attributes: APIQuery.Attributes = Field(
        default_factory=lambda: APIQuery.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_p_i_field import APIField  # noqa

APIQuery.Attributes.update_forward_refs()
