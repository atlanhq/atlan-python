# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Dict, List, Union

from pydantic.v1 import ValidationError

from pyatlan.client.constants import (
    CREATE_TYPE_DEFS,
    DELETE_TYPE_DEF_BY_NAME,
    GET_ALL_TYPE_DEFS,
    GET_TYPE_DEF_BY_NAME,
    UPDATE_TYPE_DEFS,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import (
    AtlanTagDef,
    CustomMetadataDef,
    EntityDef,
    EnumDef,
    RelationshipDef,
    StructDef,
    TypeDef,
    TypeDefResponse,
)


def _build_typedef_request(typedef: TypeDef) -> TypeDefResponse:
    """
    Build a TypeDefResponse request payload from a TypeDef.

    :param typedef: type definition to build request for
    :returns: TypeDefResponse request payload
    :raises InvalidRequestError: if the typedef category is not supported
    """
    if isinstance(typedef, AtlanTagDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[typedef],
            enum_defs=[],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[],
        )  # type: ignore[call-arg]
    elif isinstance(typedef, CustomMetadataDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[],
            enum_defs=[],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[typedef],
        )  # type: ignore[call-arg]
    elif isinstance(typedef, EnumDef):
        # Set up the request payload...
        payload = TypeDefResponse(
            atlan_tag_defs=[],
            enum_defs=[typedef],
            struct_defs=[],
            entity_defs=[],
            relationship_defs=[],
            custom_metadata_defs=[],
        )  # type: ignore[call-arg]
    else:
        raise ErrorCode.UNABLE_TO_UPDATE_TYPEDEF_CATEGORY.exception_with_parameters(
            typedef.category.value
        )
    return payload


class TypeDefFactory:
    """Factory for creating specific type definition objects."""

    @staticmethod
    def create(raw_json: dict) -> TypeDef:
        """
        Creates a specific type definition object based on the provided raw JSON.

        :param raw_json: raw JSON data representing the type definition
        :returns: type definition object
        :raises ApiError: on receiving an unsupported type definition category
        """
        TYPE_DEF_MAP = {
            AtlanTypeCategory.ENUM: EnumDef,
            AtlanTypeCategory.STRUCT: StructDef,
            AtlanTypeCategory.CLASSIFICATION: AtlanTagDef,
            AtlanTypeCategory.ENTITY: EntityDef,
            AtlanTypeCategory.RELATIONSHIP: RelationshipDef,
            AtlanTypeCategory.CUSTOM_METADATA: CustomMetadataDef,
        }
        category = raw_json.get("category")
        type_def_model = category and TYPE_DEF_MAP.get(category)
        if type_def_model:
            return type_def_model(**raw_json)
        else:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, f"Unsupported type definition category: {category}"
            )


class TypeDefGet:
    """Shared logic for retrieving type definitions."""

    @staticmethod
    def prepare_request_all() -> tuple:
        """
        Prepare the request for getting all type definitions.

        :returns: tuple of (endpoint, query_params)
        """
        return GET_ALL_TYPE_DEFS, None

    @staticmethod
    def prepare_request_by_category(
        type_category: Union[AtlanTypeCategory, List[AtlanTypeCategory]],
    ) -> tuple:
        """
        Prepare the request for getting type definitions by category.

        :param type_category: category of type definitions to retrieve
        :returns: tuple of (endpoint, query_params)
        """
        categories: List[str] = []
        if isinstance(type_category, list):
            categories.extend(map(lambda x: x.value, type_category))
        else:
            categories.append(type_category.value)
        query_params = {"type": categories}
        return GET_ALL_TYPE_DEFS.format_path_with_params(), query_params

    @staticmethod
    def process_response(raw_json: Dict) -> TypeDefResponse:
        """
        Process the API response into a TypeDefResponse.

        :param raw_json: raw response from the API
        :returns: TypeDefResponse object
        """
        return TypeDefResponse(**raw_json)


class TypeDefGetByName:
    """Shared logic for getting type definition by name."""

    @staticmethod
    def prepare_request(name: str) -> tuple:
        """
        Prepare the request for getting type definition by name.

        :param name: internal (hashed-string, if used) name of the type definition
        :returns: tuple of (endpoint, request_obj)
        """
        endpoint = GET_TYPE_DEF_BY_NAME.format_path_with_params(name)
        return endpoint, None

    @staticmethod
    def process_response(raw_json: Dict) -> TypeDef:
        """
        Process the API response into a TypeDef.

        :param raw_json: raw response from the API
        :returns: TypeDef object
        :raises ApiError: on receiving an unsupported type definition
        category or when unable to produce a valid response
        """
        try:
            return TypeDefFactory.create(raw_json)
        except (ValidationError, AttributeError) as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err


class TypeDefCreate:
    """Shared logic for creating type definitions."""

    @staticmethod
    def prepare_request(typedef: TypeDef) -> tuple:
        """
        Prepare the request for creating a type definition.

        :param typedef: type definition to create
        :returns: tuple of (endpoint, request_obj)
        :raises InvalidRequestError: if the typedef you are
        trying to create is not one of the allowed types
        """
        payload = _build_typedef_request(typedef)
        return CREATE_TYPE_DEFS, payload

    @staticmethod
    def process_response(raw_json: Dict) -> TypeDefResponse:
        """
        Process the API response into a TypeDefResponse.

        :param raw_json: raw response from the API
        :returns: TypeDefResponse object
        """
        return TypeDefResponse(**raw_json)


class TypeDefUpdate:
    """Shared logic for updating type definitions."""

    @staticmethod
    def prepare_request(typedef: TypeDef) -> tuple:
        """
        Prepare the request for updating a type definition.

        :param typedef: type definition to update
        :returns: tuple of (endpoint, request_obj)
        :raises InvalidRequestError: if the typedef you are
        trying to update is not one of the allowed types
        """
        payload = _build_typedef_request(typedef)
        return UPDATE_TYPE_DEFS, payload

    @staticmethod
    def process_response(raw_json: Dict) -> TypeDefResponse:
        """
        Process the API response into a TypeDefResponse.

        :param raw_json: raw response from the API
        :returns: TypeDefResponse object
        """
        return TypeDefResponse(**raw_json)


class TypeDefPurge:
    """Shared logic for purging type definitions."""

    @staticmethod
    def prepare_request(name: str, typedef_type: type, client) -> tuple:
        """
        Prepare the request for purging a type definition.

        :param name: internal hashed-string name of the type definition
        :param typedef_type: type of the type definition that is being deleted
        :param client: client instance to access caches
        :returns: tuple of (endpoint, request_obj)
        :raises InvalidRequestError: if the typedef you are trying to delete is not one of the allowed types
        :raises NotFoundError: if the typedef you are trying to delete cannot be found
        """
        if typedef_type == CustomMetadataDef:
            internal_name = client.custom_metadata_cache.get_id_for_name(name)
        elif typedef_type == EnumDef:
            internal_name = name
        elif typedef_type == AtlanTagDef:
            internal_name = str(client.atlan_tag_cache.get_id_for_name(name))
        else:
            raise ErrorCode.UNABLE_TO_PURGE_TYPEDEF_OF_TYPE.exception_with_parameters(
                typedef_type
            )

        if internal_name:
            endpoint = DELETE_TYPE_DEF_BY_NAME.format_path_with_params(internal_name)
            return endpoint, None
        else:
            raise ErrorCode.TYPEDEF_NOT_FOUND_BY_NAME.exception_with_parameters(name)

    @staticmethod
    def refresh_caches(typedef_type: type, client) -> None:
        """
        Refresh appropriate caches after purging a type definition.

        :param typedef_type: type of the type definition that was deleted
        :param client: client instance to access caches
        """
        if typedef_type == CustomMetadataDef:
            client.custom_metadata_cache.refresh_cache()
        elif typedef_type == EnumDef:
            client.enum_cache.refresh_cache()
        elif typedef_type == AtlanTagDef:
            client.atlan_tag_cache.refresh_cache()

    @staticmethod
    async def prepare_request_async(name: str, typedef_type: type, client) -> tuple:
        """
        Async version of prepare_request that properly awaits cache calls.

        :param name: internal hashed-string name of the type definition
        :param typedef_type: type of the type definition that is being deleted
        :param client: AsyncAtlanClient instance
        :returns: tuple of (endpoint, request_obj)
        :raises InvalidRequestError: if the typedef you are trying to delete is not one of the allowed types
        :raises NotFoundError: if the typedef you are trying to delete cannot be found
        """
        from pyatlan.client.common.typedef import DELETE_TYPE_DEF_BY_NAME
        from pyatlan.errors import ErrorCode
        from pyatlan.model.typedef import AtlanTagDef, CustomMetadataDef, EnumDef

        if typedef_type == CustomMetadataDef:
            internal_name = await client.custom_metadata_cache.get_id_for_name(name)
        elif typedef_type == EnumDef:
            internal_name = name
        elif typedef_type == AtlanTagDef:
            internal_name = str(await client.atlan_tag_cache.get_id_for_name(name))
        else:
            raise ErrorCode.UNABLE_TO_PURGE_TYPEDEF_OF_TYPE.exception_with_parameters(
                typedef_type
            )

        if internal_name:
            endpoint = DELETE_TYPE_DEF_BY_NAME.format_path_with_params(internal_name)
            return endpoint, None
        else:
            raise ErrorCode.TYPEDEF_NOT_FOUND_BY_NAME.exception_with_parameters(name)

    @staticmethod
    async def refresh_caches_async(typedef_type: type, client) -> None:
        """
        Async version of refresh_caches that properly awaits cache calls.

        :param typedef_type: type of the type definition that was deleted
        :param client: AsyncAtlanClient instance
        """
        from pyatlan.model.typedef import AtlanTagDef, CustomMetadataDef, EnumDef

        if typedef_type == CustomMetadataDef:
            await client.custom_metadata_cache.refresh_cache()
        elif typedef_type == EnumDef:
            await client.enum_cache.refresh_cache()
        elif typedef_type == AtlanTagDef:
            await client.atlan_tag_cache.refresh_cache()
