# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Dict, Optional, Set

from pyatlan.client.constants import DELETE_API_TOKEN, GET_API_TOKENS, UPSERT_API_TOKEN
from pyatlan.model.api_tokens import ApiToken, ApiTokenRequest, ApiTokenResponse
from pyatlan.model.constants import SERVICE_ACCOUNT_


class TokenGet:
    """Shared logic for getting API tokens with various filters."""

    @staticmethod
    def prepare_request(
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> tuple:
        """
        Prepare the request for getting API tokens.

        :param limit: maximum number of results to be returned
        :param post_filter: which API tokens to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: tuple of (endpoint, query_params)
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

        return GET_API_TOKENS.format_path_with_params(), query_params

    @staticmethod
    def process_response(raw_json: Dict) -> ApiTokenResponse:
        """
        Process the API response into an ApiTokenResponse.

        :param raw_json: raw response from the API
        :returns: parsed ApiTokenResponse
        """
        return ApiTokenResponse(**raw_json)


class TokenGetByName:
    """Shared logic for getting API token by display name."""

    @staticmethod
    def prepare_request(display_name: str) -> tuple:
        """
        Prepare the request for getting API token by name.

        :param display_name: name (as it appears in the UI) by which to retrieve the API token
        :returns: tuple of (endpoint, query_params)
        """
        query_params: Dict[str, str] = {
            "count": "True",
            "offset": "0",
            "limit": "5",
            "filter": f'{{"displayName":"{display_name}"}}',
        }
        return GET_API_TOKENS.format_path_with_params(), query_params

    @staticmethod
    def process_response(raw_json: Dict) -> Optional[ApiToken]:
        """
        Process the API response and extract the first matching token.

        :param raw_json: raw response from the API
        :returns: the first API token found, or None if none found
        """
        response = ApiTokenResponse(**raw_json)
        if response.records and len(response.records) >= 1:
            return response.records[0]
        return None


class TokenGetById:
    """Shared logic for getting API token by client ID."""

    @staticmethod
    def prepare_request(client_id: str) -> tuple:
        """
        Prepare the request for getting API token by client ID.

        :param client_id: unique client identifier by which to retrieve the API token
        :returns: tuple of (endpoint, query_params)
        """
        # Strip SERVICE_ACCOUNT_ prefix if present
        if client_id and client_id.startswith(SERVICE_ACCOUNT_):
            client_id = client_id[len(SERVICE_ACCOUNT_) :]

        query_params: Dict[str, str] = {
            "count": "True",
            "offset": "0",
            "limit": "5",
            "filter": f'{{"clientId":"{client_id}"}}',
        }
        return GET_API_TOKENS.format_path_with_params(), query_params

    @staticmethod
    def process_response(raw_json: Dict) -> Optional[ApiToken]:
        """
        Process the API response and extract the first matching token.

        :param raw_json: raw response from the API
        :returns: the first API token found, or None if none found
        """
        response = ApiTokenResponse(**raw_json)
        if response.records and len(response.records) >= 1:
            return response.records[0]
        return None


class TokenGetByGuid:
    """Shared logic for getting API token by GUID."""

    @staticmethod
    def prepare_request(guid: str) -> tuple:
        """
        Prepare the request for getting API token by GUID.

        :param guid: unique identifier by which to retrieve the API token
        :returns: tuple of (endpoint, query_params)
        """
        query_params: Dict[str, str] = {
            "count": "True",
            "offset": "0",
            "limit": "5",
            "filter": f'{{"id":"{guid}"}}',
            "sort": "createdAt",
        }
        return GET_API_TOKENS.format_path_with_params(), query_params

    @staticmethod
    def process_response(raw_json: Dict) -> Optional[ApiToken]:
        """
        Process the API response and extract the first matching token.

        :param raw_json: raw response from the API
        :returns: the first API token found, or None if none found
        """
        response = ApiTokenResponse(**raw_json)
        if response.records and len(response.records) >= 1:
            return response.records[0]
        return None


class TokenCreate:
    """Shared logic for creating API tokens."""

    @staticmethod
    def prepare_request(
        display_name: str,
        description: str = "",
        personas: Optional[Set[str]] = None,
        validity_seconds: int = -1,
    ) -> tuple:
        """
        Prepare the request for creating an API token.

        :param display_name: human-readable name for the API token
        :param description: optional explanation of the API token
        :param personas: qualified_names of personas that should be linked to the token
        :param validity_seconds: time in seconds after which the token should expire
        :returns: tuple of (endpoint, request_obj)
        """
        request = ApiTokenRequest(
            display_name=display_name,
            description=description,
            persona_qualified_names=personas or set(),
            validity_seconds=validity_seconds,
        )
        return UPSERT_API_TOKEN, request

    @staticmethod
    def process_response(raw_json: Dict) -> ApiToken:
        """
        Process the API response into an ApiToken.

        :param raw_json: raw response from the API
        :returns: the created ApiToken
        """
        return ApiToken(**raw_json)


class TokenUpdate:
    """Shared logic for updating API tokens."""

    @staticmethod
    def prepare_request(
        guid: str,
        display_name: str,
        description: str = "",
        personas: Optional[Set[str]] = None,
    ) -> tuple:
        """
        Prepare the request for updating an API token.

        :param guid: unique identifier (GUID) of the API token
        :param display_name: human-readable name for the API token
        :param description: optional explanation of the API token
        :param personas: qualified_names of personas that should be linked to the token
        :returns: tuple of (endpoint, request_obj)
        """
        request = ApiTokenRequest(
            display_name=display_name,
            description=description,
            persona_qualified_names=personas or set(),
        )
        endpoint = UPSERT_API_TOKEN.format_path_with_params(guid)
        return endpoint, request

    @staticmethod
    def process_response(raw_json: Dict) -> ApiToken:
        """
        Process the API response into an ApiToken.

        :param raw_json: raw response from the API
        :returns: the updated ApiToken
        """
        return ApiToken(**raw_json)


class TokenPurge:
    """Shared logic for purging API tokens."""

    @staticmethod
    def prepare_request(guid: str) -> tuple:
        """
        Prepare the request for purging an API token.

        :param guid: unique identifier (GUID) of the API token to delete
        :returns: tuple of (endpoint, None)
        """
        endpoint = DELETE_API_TOKEN.format_path_with_params(guid)
        return endpoint, None
