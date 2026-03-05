# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import List, Union

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    TypeDefCreate,
    TypeDefGet,
    TypeDefGetByName,
    TypeDefPurge,
    TypeDefUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import (
    AtlanTagDef,
    CustomMetadataDef,
    EnumDef,
    TypeDef,
    TypeDefResponse,
)


class TypeDefClient:
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

        :returns: TypeDefResponse object that contains  a list of all the type definitions in Atlan
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = TypeDefGet.prepare_request_all()
        raw_json = self._client._call_api(endpoint, query_params)
        return TypeDefGet.process_response(raw_json)

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
        endpoint, query_params = TypeDefGet.prepare_request_by_category(type_category)
        raw_json = self._client._call_api(endpoint, query_params)
        return TypeDefGet.process_response(raw_json)

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
        endpoint, request_obj = TypeDefGetByName.prepare_request(name)
        raw_json = self._client._call_api(endpoint, request_obj)
        return TypeDefGetByName.process_response(raw_json)

    @validate_arguments
    def create(self, typedef: TypeDef) -> TypeDefResponse:
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
        endpoint, request_obj = TypeDefCreate.prepare_request(typedef)
        raw_json = self._client._call_api(
            endpoint, request_obj=request_obj, exclude_unset=True
        )
        self._refresh_caches(typedef)
        return TypeDefCreate.process_response(raw_json)

    @validate_arguments
    def update(self, typedef: TypeDef) -> TypeDefResponse:
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
        endpoint, request_obj = TypeDefUpdate.prepare_request(typedef)
        raw_json = self._client._call_api(
            endpoint, request_obj=request_obj, exclude_unset=True
        )
        self._refresh_caches(typedef)
        return TypeDefUpdate.process_response(raw_json)

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
        endpoint, request_obj = TypeDefPurge.prepare_request(
            name, typedef_type, self._client
        )
        self._client._call_api(endpoint, request_obj)
        TypeDefPurge.refresh_caches(typedef_type, self._client)
