# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import APIQueryParamTypeEnum, AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .a_p_i import API


class APIField(API):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str],
        parent_api_query_qualified_name: Optional[str],
    ) -> APIField: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str],
        parent_api_query_qualified_name: Optional[str],
        connection_qualified_name: str,
    ) -> APIField: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str],
        parent_api_query_qualified_name: Optional[str],
        api_query_param_type: APIQueryParamTypeEnum,
    ) -> APIField: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str],
        parent_api_query_qualified_name: Optional[str],
        api_field_type: str,
        api_field_type_secondary: str,
        api_query_param_type: APIQueryParamTypeEnum,
    ) -> APIField: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str],
        parent_api_query_qualified_name: Optional[str],
        api_field_type: str,
        api_field_type_secondary: str,
        is_api_object_reference: bool,
        api_query_param_type: APIQueryParamTypeEnum,
    ) -> APIField: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str],
        parent_api_query_qualified_name: Optional[str],
        api_field_type: str,
        api_field_type_secondary: str,
        is_api_object_reference: bool,
        reference_api_object_qualified_name: str,
        api_query_param_type: APIQueryParamTypeEnum,
    ) -> APIField: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str],
        parent_api_query_qualified_name: Optional[str],
        connection_qualified_name: str,
        api_field_type: str,
        api_field_type_secondary: str,
        is_api_object_reference: bool,
        reference_api_object_qualified_name: str,
        api_query_param_type: APIQueryParamTypeEnum,
    ) -> APIField: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        parent_api_object_qualified_name: Optional[str] = None,
        parent_api_query_qualified_name: Optional[str] = None,
        connection_qualified_name: Optional[str] = None,
        api_field_type: Optional[str] = None,
        api_field_type_secondary: Optional[str] = None,
        is_api_object_reference: Optional[bool] = False,
        reference_api_object_qualified_name: Optional[str] = None,
        api_query_param_type: Optional[APIQueryParamTypeEnum] = None,
    ) -> APIField:
        validate_required_fields(["name"], [name])
        # valid checker - for either to have a value ONLY
        if parent_api_object_qualified_name is None or (
            isinstance(parent_api_object_qualified_name, str)
            and not parent_api_object_qualified_name.strip()
        ):
            if parent_api_query_qualified_name is None or (
                isinstance(parent_api_query_qualified_name, str)
                and not parent_api_query_qualified_name.strip()
            ):
                raise ValueError(
                    (
                        "Either parent_api_object_qualified_name or "
                        "parent_api_query_qualified_name requires a valid value"
                    )
                )
        elif (
            isinstance(parent_api_query_qualified_name, str)
            and parent_api_query_qualified_name.strip()
        ):
            raise ValueError(
                "Both parent_api_object_qualified_name and parent_api_query_qualified_name cannot be valid"
            )

        # is api object reference - checker
        if is_api_object_reference:
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
                    "Set is_api_object_reference to true to set reference_api_object_qualified_name"
                )

        attributes = APIField.Attributes.creator(
            name=name,
            parent_api_object_qualified_name=parent_api_object_qualified_name,
            parent_api_query_qualified_name=parent_api_query_qualified_name,
            connection_qualified_name=connection_qualified_name,
            api_field_type=api_field_type,
            api_field_type_secondary=api_field_type_secondary,
            is_api_object_reference=is_api_object_reference,
            reference_api_object_qualified_name=reference_api_object_qualified_name,
            api_query_param_type=api_query_param_type,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="APIField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "APIField":
            raise ValueError("must be APIField")
        return v

    def __setattr__(self, name, value):
        if name in APIField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    API_FIELD_TYPE: ClassVar[KeywordField] = KeywordField(
        "apiFieldType", "apiFieldType"
    )
    """
    Type of APIField. E.g. STRING, NUMBER etc. It is free text.
    """
    API_FIELD_TYPE_SECONDARY: ClassVar[KeywordField] = KeywordField(
        "apiFieldTypeSecondary", "apiFieldTypeSecondary"
    )
    """
    Secondary Type of APIField. E.g. LIST/STRING, then LIST would be the secondary type.
    """
    API_QUERY_PARAM_TYPE: ClassVar[KeywordField] = KeywordField(
        "apiQueryParamType", "apiQueryParamType"
    )
    """
    If parent relationship type is APIQuery, then this attribute denotes if this is input or output parameter.
    """

    API_QUERY: ClassVar[RelationField] = RelationField("apiQuery")
    """
    TBC
    """
    API_OBJECT: ClassVar[RelationField] = RelationField("apiObject")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "api_field_type",
        "api_field_type_secondary",
        "api_query_param_type",
        "api_query",
        "api_object",
    ]

    @property
    def api_field_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.api_field_type

    @api_field_type.setter
    def api_field_type(self, api_field_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_field_type = api_field_type

    @property
    def api_field_type_secondary(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.api_field_type_secondary
        )

    @api_field_type_secondary.setter
    def api_field_type_secondary(self, api_field_type_secondary: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_field_type_secondary = api_field_type_secondary

    @property
    def api_query_param_type(self) -> Optional[APIQueryParamTypeEnum]:
        return None if self.attributes is None else self.attributes.api_query_param_type

    @api_query_param_type.setter
    def api_query_param_type(
        self, api_query_param_type: Optional[APIQueryParamTypeEnum]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_query_param_type = api_query_param_type

    @property
    def api_query(self) -> Optional[APIQuery]:
        return None if self.attributes is None else self.attributes.api_query

    @api_query.setter
    def api_query(self, api_query: Optional[APIQuery]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_query = api_query

    @property
    def api_object(self) -> Optional[APIObject]:
        return None if self.attributes is None else self.attributes.api_object

    @api_object.setter
    def api_object(self, api_object: Optional[APIObject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.api_object = api_object

    class Attributes(API.Attributes):
        api_field_type: Optional[str] = Field(default=None, description="")
        api_field_type_secondary: Optional[str] = Field(default=None, description="")
        api_query_param_type: Optional[APIQueryParamTypeEnum] = Field(
            default=None, description=""
        )
        api_query: Optional[APIQuery] = Field(
            default=None, description=""
        )  # relationship
        api_object: Optional[APIObject] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            parent_api_object_qualified_name: Optional[str] = None,
            parent_api_query_qualified_name: Optional[str] = None,
            connection_qualified_name: Optional[str] = None,
            api_field_type: Optional[str] = None,
            api_field_type_secondary: Optional[str] = None,
            is_api_object_reference: Optional[bool] = False,
            reference_api_object_qualified_name: Optional[str] = None,
            api_query_param_type: Optional[APIQueryParamTypeEnum] = None,
        ) -> APIField.Attributes:
            validate_required_fields(["name"], [name])
            if parent_api_object_qualified_name is None or (
                isinstance(parent_api_object_qualified_name, str)
                and not parent_api_object_qualified_name.strip()
            ):
                if parent_api_query_qualified_name is None or (
                    isinstance(parent_api_query_qualified_name, str)
                    and not parent_api_query_qualified_name.strip()
                ):
                    raise ValueError(
                        (
                            "Either parent_api_object_qualified_name or "
                            "parent_api_query_qualified_name requires a valid value"
                        )
                    )
            elif (
                isinstance(parent_api_query_qualified_name, str)
                and parent_api_query_qualified_name.strip()
            ):
                raise ValueError(
                    "Both parent_api_object_qualified_name and parent_api_query_qualified_name cannot be valid"
                )

            if is_api_object_reference:
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
                        "Set is_api_object_reference to true to set reference_api_object_qualified_name"
                    )

            # connector-name
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
                connection_qn = connection_qualified_name
            elif parent_api_object_qualified_name:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    parent_api_object_qualified_name,
                    "parent_api_object_qualified_name",
                    4,
                )
            elif parent_api_query_qualified_name:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    parent_api_query_qualified_name,
                    "parent_api_query_qualified_name",
                    4,
                )

            if parent_api_object_qualified_name:
                return APIField.Attributes(
                    name=name,
                    qualified_name=f"{parent_api_object_qualified_name}/{name}",
                    connection_qualified_name=connection_qn,
                    connector_name=connector_name,
                    api_field_type=api_field_type,
                    api_field_type_secondary=api_field_type_secondary,
                    api_is_object_reference=is_api_object_reference,
                    api_object_qualified_name=(
                        reference_api_object_qualified_name
                        if is_api_object_reference
                        else None
                    ),
                    api_object=APIObject.ref_by_qualified_name(
                        str(parent_api_object_qualified_name)
                    ),
                    api_query_param_type=api_query_param_type,
                )
            else:
                return APIField.Attributes(
                    name=name,
                    qualified_name=f"{parent_api_query_qualified_name}/{name}",
                    connection_qualified_name=connection_qn,
                    connector_name=connector_name,
                    api_field_type=api_field_type,
                    api_field_type_secondary=api_field_type_secondary,
                    api_is_object_reference=is_api_object_reference,
                    api_object_qualified_name=(
                        reference_api_object_qualified_name
                        if is_api_object_reference
                        else None
                    ),
                    api_query=APIQuery.ref_by_qualified_name(
                        str(parent_api_query_qualified_name)
                    ),
                    api_query_param_type=api_query_param_type,
                )

    attributes: APIField.Attributes = Field(
        default_factory=lambda: APIField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_p_i_object import APIObject  # noqa
from .a_p_i_query import APIQuery  # noqa

APIField.Attributes.update_forward_refs()
