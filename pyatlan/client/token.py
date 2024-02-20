# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Dict, Optional, Set

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import DELETE_API_TOKEN, GET_API_TOKENS, UPSERT_API_TOKEN
from pyatlan.errors import ErrorCode
from pyatlan.model.api_tokens import ApiToken, ApiTokenRequest, ApiTokenResponse

SERVICE_ACCOUNT_ = "service-account-"


class TokenClient:
    """
    This class can be used to retrieve information pertaining to API tokens. This class does not need to be instantiated
    directly but can be obtained through the token property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def get(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> ApiTokenResponse:
        """
        Retrieves an ApiTokenResponse which contains a list of API tokens defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which API tokens to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: an ApiTokenResponse which contains a list of API tokens that match the provided criteria
        :raises AtlanError: on any API communication issue
        """
        query_params: Dict[str, str] = {
            "count": str(count),
            "offset": str(offset),
        }
        if limit is not None:
            query_params["limit"] = str(limit)
        if post_filter is not None:
            query_params["filter"] = post_filter
        if sort is not None:
            query_params["sort"] = sort
        raw_json = self._client._call_api(
            GET_API_TOKENS.format_path_with_params(), query_params
        )
        return ApiTokenResponse(**raw_json)

    @validate_arguments
    def get_by_name(self, display_name: str) -> Optional[ApiToken]:
        """
        Retrieves the API token with a name that exactly matches the provided string.

        :param display_name: name (as it appears in the UI) by which to retrieve the API token
        :returns: the API token whose name (in the UI) matches the provided string, or None if there is none
        """
        if response := self.get(
            offset=0,
            limit=5,
            post_filter='{"displayName":"' + display_name + '"}',
        ):
            if response.records and len(response.records) >= 1:
                return response.records[0]
        return None

    @validate_arguments
    def get_by_id(self, client_id: str) -> Optional[ApiToken]:
        """
        Retrieves the API token with a client ID that exactly matches the provided string.

        :param client_id: unique client identifier by which to retrieve the API token
        :returns: the API token whose clientId matches the provided string, or None if there is none
        """
        if client_id and client_id.startswith(SERVICE_ACCOUNT_):
            client_id = client_id[len(SERVICE_ACCOUNT_) :]  # noqa: E203
        if response := self.get(
            offset=0,
            limit=5,
            post_filter='{"clientId":"' + client_id + '"}',
        ):
            if response.records and len(response.records) >= 1:
                return response.records[0]
        return None

    @validate_arguments
    def get_by_guid(self, guid: str) -> Optional[ApiToken]:
        """
        Retrieves the API token with a unique ID (GUID) that exactly matches the provided string.

        :param guid: unique identifier by which to retrieve the API token
        :returns: the API token whose clientId matches the provided string, or None if there is none
        """
        if response := self.get(
            offset=0, limit=5, post_filter='{"id":"' + guid + '"}', sort="createdAt"
        ):
            if response.records and len(response.records) >= 1:
                return response.records[0]
        return None

    @validate_arguments
    def create(
        self,
        display_name: str,
        description: str = "",
        personas: Optional[Set[str]] = None,
        validity_seconds: int = -1,
    ) -> ApiToken:
        """
        Create a new API token with the provided settings.

        :param display_name: human-readable name for the API token
        :param description: optional explanation of the API token
        :param personas: qualified_names of personas that should  be linked to the token
        :param validity_seconds: time in seconds after which the token should expire (negative numbers are treated as
                                 infinite)
        :returns: the created API token
        :raises AtlanError: on any API communication issue
        """
        request = ApiTokenRequest(
            display_name=display_name,
            description=description,
            persona_qualified_names=personas or set(),
            validity_seconds=validity_seconds,
        )
        raw_json = self._client._call_api(UPSERT_API_TOKEN, request_obj=request)
        return ApiToken(**raw_json)

    @validate_arguments
    def update(
        self,
        guid: str,
        display_name: str,
        description: str = "",
        personas: Optional[Set[str]] = None,
    ) -> ApiToken:
        """
        Update an existing API token with the provided settings.

        :param guid: unique identifier (GUID) of the API token
        :param display_name: human-readable name for the API token
        :param description: optional explanation of the API token
        :param personas: qualified_names of personas that should  be linked to the token, note that you MUST
                         provide the complete list on any update (any not included in the list will be removed,
                         so if you do not specify any personas then ALL personas will be unlinked from the API token)
        :returns: the created API token
        :raises AtlanError: on any API communication issue
        """
        request = ApiTokenRequest(
            display_name=display_name,
            description=description,
            persona_qualified_names=personas or set(),
        )
        raw_json = self._client._call_api(
            UPSERT_API_TOKEN.format_path_with_params(guid), request_obj=request
        )
        return ApiToken(**raw_json)

    @validate_arguments
    def purge(self, guid: str) -> None:
        """
        Delete (purge) the specified API token.

        :param guid: unique identifier (GUID) of the API token to delete
        :raises AtlanError: on any API communication issue
        """
        self._client._call_api(DELETE_API_TOKEN.format_path_with_params(guid))
