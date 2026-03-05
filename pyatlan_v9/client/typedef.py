# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import List, Union

import msgspec

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    CREATE_TYPE_DEFS,
    DELETE_TYPE_DEF_BY_NAME,
    GET_ALL_TYPE_DEFS,
    GET_TYPE_DEF_BY_NAME,
    UPDATE_TYPE_DEFS,
)
from pyatlan.errors import ErrorCode
from pyatlan_v9.model.enums import AtlanTypeCategory
from pyatlan_v9.model.typedef import (
    AtlanTagDef,
    CustomMetadataDef,
    EntityDef,
    EnumDef,
    RelationshipDef,
    StructDef,
    TypeDef,
    TypeDefResponse,
)
from pyatlan_v9.validate import validate_arguments

_TYPE_DEF_MAP = {
    AtlanTypeCategory.ENUM: EnumDef,
    AtlanTypeCategory.STRUCT: StructDef,
    AtlanTypeCategory.CLASSIFICATION: AtlanTagDef,
    AtlanTypeCategory.ENTITY: EntityDef,
    AtlanTypeCategory.RELATIONSHIP: RelationshipDef,
    AtlanTypeCategory.CUSTOM_METADATA: CustomMetadataDef,
}


def _build_typedef_request(typedef: TypeDef) -> TypeDefResponse:
    """Build a TypeDefResponse request payload from a TypeDef."""
    if isinstance(typedef, AtlanTagDef):
        return TypeDefResponse(atlan_tag_defs=[typedef])
    elif isinstance(typedef, CustomMetadataDef):
        return TypeDefResponse(custom_metadata_defs=[typedef])
    elif isinstance(typedef, EnumDef):
        return TypeDefResponse(enum_defs=[typedef])
    else:
        raise ErrorCode.UNABLE_TO_UPDATE_TYPEDEF_CATEGORY.exception_with_parameters(
            typedef.category.value
        )


def _create_typedef_from_json(raw_json) -> TypeDef:
    """Create a specific TypeDef subclass from raw JSON based on category."""
    try:
        category = raw_json.get("category")
        type_def_cls = category and _TYPE_DEF_MAP.get(category)
        if type_def_cls:
            return msgspec.convert(raw_json, type_def_cls, strict=False)
        raise ErrorCode.JSON_ERROR.exception_with_parameters(
            raw_json, 200, f"Unsupported type definition category: {category}"
        )
    except (msgspec.ValidationError, AttributeError) as err:
        raise ErrorCode.JSON_ERROR.exception_with_parameters(
            raw_json, 200, str(err)
        ) from err


class V9TypeDefClient:
    """
    This class can be used to retrieve information pertaining to TypeDefs. This class does not need to be instantiated
    directly but can be obtained through the typedef property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def _refresh_caches(self, typedef: TypeDef) -> None:
        """Refresh appropriate caches after creating or updating a type definition."""
        if isinstance(typedef, AtlanTagDef):
            self._client.atlan_tag_cache.refresh_cache()  # type: ignore[attr-defined]
        if isinstance(typedef, CustomMetadataDef):
            self._client.custom_metadata_cache.refresh_cache()  # type: ignore[attr-defined]
        if isinstance(typedef, EnumDef):
            self._client.enum_cache.refresh_cache()  # type: ignore[attr-defined]

    def get_all(self) -> TypeDefResponse:
        """
        Retrieves a TypeDefResponse object that contains a list of all the type definitions in Atlan.

        :returns: TypeDefResponse object that contains a list of all the type definitions in Atlan
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(GET_ALL_TYPE_DEFS, None)
        return msgspec.convert(raw_json, TypeDefResponse, strict=False)

    @validate_arguments
    def get(
        self, type_category: Union[AtlanTypeCategory, List[AtlanTypeCategory]]
    ) -> TypeDefResponse:
        """
        Retrieves a TypeDefResponse object that contain a list of the specified category type definitions in Atlan.

        :param type_category: category of type definitions to retrieve
        :returns: TypeDefResponse object that contain a list that contains the requested list of type definitions
        :raises AtlanError: on any API communication issue
        """
        categories: List[str] = []
        if isinstance(type_category, list):
            categories.extend(map(lambda x: x.value, type_category))
        else:
            categories.append(type_category.value)
        query_params = {"type": categories}
        raw_json = self._client._call_api(
            GET_ALL_TYPE_DEFS.format_path_with_params(), query_params
        )
        return msgspec.convert(raw_json, TypeDefResponse, strict=False)

    @validate_arguments
    def get_by_name(self, name: str) -> TypeDef:
        """
        Retrieves a specific type definition from Atlan.

        :name: internal (hashed-string, if used) name of the type definition
        :returns: details of that specific type definition
        :raises ApiError: on receiving an unsupported type definition
        category or when unable to produce a valid response
        :raises AtlanError: on any API communication issue
        """
        endpoint = GET_TYPE_DEF_BY_NAME.format_path_with_params(name)
        raw_json = self._client._call_api(endpoint, None)
        return _create_typedef_from_json(raw_json)

    @validate_arguments
    def creator(self, typedef: TypeDef) -> TypeDefResponse:
        """
        Create a new type definition in Atlan.
        Note: only custom metadata, enumerations (options), and Atlan tag type
        definitions are currently supported. Furthermore, if any of these are
        created their respective cache will be force-refreshed.

        :param typedef: type definition to create
        :returns: the resulting type definition that was created
        :raises InvalidRequestError: if the typedef you are
        trying to create is not one of the allowed types
        :raises AtlanError: on any API communication issue
        """
        payload = _build_typedef_request(typedef)
        raw_json = self._client._call_api(CREATE_TYPE_DEFS, request_obj=payload)
        self._refresh_caches(typedef)
        return msgspec.convert(raw_json, TypeDefResponse, strict=False)

    @validate_arguments
    def updater(self, typedef: TypeDef) -> TypeDefResponse:
        """
        Update an existing type definition in Atlan.
        Note: only custom metadata, enumerations (options), and Atlan tag type
        definitions are currently supported. Furthermore, if any of these are
        updated their respective cache will be force-refreshed.

        :param typedef: type definition to update
        :returns: the resulting type definition that was updated
        :raises InvalidRequestError: if the typedef you are
        trying to update is not one of the allowed types
        :raises AtlanError: on any API communication issue
        """
        payload = _build_typedef_request(typedef)
        raw_json = self._client._call_api(UPDATE_TYPE_DEFS, request_obj=payload)
        self._refresh_caches(typedef)
        return msgspec.convert(raw_json, TypeDefResponse, strict=False)

    @validate_arguments
    def purge(self, name: str, typedef_type: type) -> None:
        """
        Delete the type definition.
        Furthermore, if an Atlan tag, enumeration or custom metadata is deleted their
        respective cache will be force-refreshed.

        :param name: internal hashed-string name of the type definition
        :param typedef_type: type of the type definition that is being deleted
        :raises InvalidRequestError: if the typedef you are trying to delete is not one of the allowed types
        :raises NotFoundError: if the typedef you are trying to delete cannot be found
        :raises AtlanError: on any API communication issue
        """
        if typedef_type == CustomMetadataDef:
            internal_name = self._client.custom_metadata_cache.get_id_for_name(name)  # type: ignore[attr-defined]
        elif typedef_type == EnumDef:
            internal_name = name
        elif typedef_type == AtlanTagDef:
            internal_name = str(self._client.atlan_tag_cache.get_id_for_name(name))  # type: ignore[attr-defined]
        else:
            raise ErrorCode.UNABLE_TO_PURGE_TYPEDEF_OF_TYPE.exception_with_parameters(
                typedef_type
            )
        if internal_name:
            endpoint = DELETE_TYPE_DEF_BY_NAME.format_path_with_params(internal_name)
            self._client._call_api(endpoint, None)
        else:
            raise ErrorCode.TYPEDEF_NOT_FOUND_BY_NAME.exception_with_parameters(name)

        if typedef_type == CustomMetadataDef:
            self._client.custom_metadata_cache.refresh_cache()  # type: ignore[attr-defined]
        elif typedef_type == EnumDef:
            self._client.enum_cache.refresh_cache()  # type: ignore[attr-defined]
        elif typedef_type == AtlanTagDef:
            self._client.atlan_tag_cache.refresh_cache()  # type: ignore[attr-defined]
