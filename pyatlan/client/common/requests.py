# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Dict, Optional

from pyatlan.client.constants import (
    ACTION_REQUEST,
    CREATE_REQUEST,
    GET_ACTIONABLE_REQUESTS,
    GET_REQUEST_BY_ID,
    GET_REQUESTS,
)
from pyatlan.model.atlan_request import (
    AtlanRequest,
    AtlanRequestAction,
    AtlanRequestResponse,
)


def _list_query_params(
    post_filter: Optional[str],
    sort: Optional[str],
    count: bool,
    offset: int,
    limit: int,
) -> Dict[str, str]:
    query_params: Dict[str, str] = {
        "count": str(count),
        "offset": str(offset),
        "limit": str(limit),
    }
    if post_filter is not None:
        query_params["filter"] = post_filter
    if sort is not None:
        query_params["sort"] = sort
    return query_params


class RequestsList:
    """Shared logic for listing requests (Metadata Inbox)."""

    @staticmethod
    def prepare_request(
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple:
        return GET_REQUESTS.format_path_with_params(), _list_query_params(
            post_filter, sort, count, offset, limit
        )

    @staticmethod
    def process_response(raw_json: Dict) -> AtlanRequestResponse:
        return AtlanRequestResponse(**raw_json)


class RequestsListActionable:
    """Shared logic for listing requests actionable by the current identity."""

    @staticmethod
    def prepare_request(
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple:
        return GET_ACTIONABLE_REQUESTS.format_path_with_params(), _list_query_params(
            post_filter, sort, count, offset, limit
        )

    @staticmethod
    def process_response(raw_json: Dict) -> AtlanRequestResponse:
        return AtlanRequestResponse(**raw_json)


class RequestsGetById:
    """Shared logic for retrieving a single request by its GUID."""

    @staticmethod
    def prepare_request(guid: str):
        return GET_REQUEST_BY_ID.format_path({"request_id": guid})

    @staticmethod
    def process_response(raw_json) -> Optional[AtlanRequest]:
        # The endpoint may return the request object directly or a
        # single-element list wrapping it.
        if isinstance(raw_json, list):
            raw_json = raw_json[0] if raw_json else None
        return AtlanRequest(**raw_json) if raw_json else None


class RequestsCreate:
    """Shared logic for creating (raising) a request."""

    @staticmethod
    def prepare_request(request: AtlanRequest) -> tuple:
        return CREATE_REQUEST.format_path_with_params(), request

    @staticmethod
    def process_response(raw_json) -> Optional[AtlanRequest]:
        return AtlanRequest(**raw_json) if isinstance(raw_json, dict) else None


class RequestsAction:
    """Shared logic for approving or rejecting a request."""

    @staticmethod
    def prepare_request(guid: str, action: str, message: Optional[str] = None) -> tuple:
        body = AtlanRequestAction(action=action, message=message or "")
        return ACTION_REQUEST.format_path({"request_id": guid}), body

    @staticmethod
    def process_response(raw_json) -> bool:
        return raw_json == "success"
