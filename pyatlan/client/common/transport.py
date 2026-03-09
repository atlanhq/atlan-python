# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared transport utilities for sync and async Atlan HTTP transports.

Provides duplicate AuthPolicy detection logic used by both
PyatlanSyncTransport and PyatlanAsyncTransport.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

import httpx

from pyatlan.client.constants import BULK_UPDATE, INDEX_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Term

logger = logging.getLogger(__name__)


def build_policy_search_request(
    policy_name: str, persona_guid: str
) -> IndexSearchRequest:
    """Build an IndexSearchRequest to find an existing AuthPolicy by name and persona."""
    query = Bool(
        filter=[
            Term(field="__typeName.keyword", value="AuthPolicy"),
            Term(field="name.keyword", value=policy_name),
            Term(field="__persona", value=persona_guid),
        ]
    )
    return IndexSearchRequest(
        dsl=DSL(query=query, size=1, from_=0),
        attributes=["name", "qualifiedName"],
    )


def create_mock_response(
    existing_policy: dict, temp_guid: str = "-1"
) -> httpx.Response:
    """Build a mock bulk-entity response containing an already-created policy."""
    response_body = {
        "mutatedEntities": {"CREATE": [existing_policy]},
        "guidAssignments": {temp_guid: existing_policy.get("guid")},
    }
    return httpx.Response(
        status_code=200,
        json=response_body,
        request=httpx.Request("POST", f"http://mock/{BULK_UPDATE.path}"),
    )


def parse_auth_policy_entity(request: httpx.Request) -> Optional[tuple[str, str, str]]:
    """
    Parse the request body and return (policy_name, persona_guid, temp_guid)
    if the request is a bulk POST containing an AuthPolicy, else None.
    """
    if request.method != "POST" or BULK_UPDATE.path not in str(request.url):
        return None
    if not request.content:
        return None

    try:
        body = json.loads(request.content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.debug(
            "parse_auth_policy_entity: failed to decode request body, skipping duplicate check"
        )
        return None

    for entity in body.get("entities", []):
        if entity.get("typeName") != "AuthPolicy":
            continue
        policy_name = entity.get("attributes", {}).get("name")
        access_control = entity.get("attributes", {}).get("accessControl")
        persona_guid = (
            access_control.get("guid") if isinstance(access_control, dict) else None
        )
        if policy_name and persona_guid:
            return policy_name, persona_guid, entity.get("guid", "-1")
    return None


def find_existing_policy(
    client: Any, policy_name: str, persona_guid: str
) -> Optional[dict]:
    """
    Search for an existing AuthPolicy by name and persona GUID (synchronous).

    Raises:
        ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY: if the search call fails.
    """
    try:
        search_request = build_policy_search_request(policy_name, persona_guid)
        raw_json = client._call_api(INDEX_SEARCH, request_obj=search_request)
        if raw_json and raw_json.get("entities"):
            return raw_json["entities"][0]
        return None
    except Exception as e:
        raise ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY.exception_with_parameters(
            policy_name, persona_guid, str(e)
        ) from e


async def find_existing_policy_async(
    client: Any, policy_name: str, persona_guid: str
) -> Optional[dict]:
    """
    Search for an existing AuthPolicy by name and persona GUID (asynchronous).

    Raises:
        ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY: if the search call fails.
    """
    try:
        search_request = build_policy_search_request(policy_name, persona_guid)
        raw_json = await client._call_api(INDEX_SEARCH, request_obj=search_request)
        if raw_json and raw_json.get("entities"):
            return raw_json["entities"][0]
        return None
    except Exception as e:
        raise ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY.exception_with_parameters(
            policy_name, persona_guid, str(e)
        ) from e


def check_for_duplicate_policy(
    client: Any, request: httpx.Request
) -> Optional[httpx.Response]:
    """
    Check whether a bulk POST is creating an AuthPolicy that already exists (synchronous).
    Only called during retry attempts, never on the first request.

    Returns a mock response with the existing policy if a duplicate is found,
    or None to let the retry proceed normally.

    Raises:
        ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY: if the duplicate search fails.
    """
    parsed = parse_auth_policy_entity(request)
    if not parsed:
        return None

    policy_name, persona_guid, temp_guid = parsed
    existing_policy = find_existing_policy(client, policy_name, persona_guid)
    if existing_policy:
        logger.info(
            f"Found existing policy '{policy_name}' with guid "
            f"{existing_policy.get('guid')} during retry check"
        )
        return create_mock_response(existing_policy, temp_guid)
    return None


async def check_for_duplicate_policy_async(
    client: Any, request: httpx.Request
) -> Optional[httpx.Response]:
    """
    Check whether a bulk POST is creating an AuthPolicy that already exists (asynchronous).
    Only called during retry attempts, never on the first request.

    Returns a mock response with the existing policy if a duplicate is found,
    or None to let the retry proceed normally.

    Raises:
        ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY: if the duplicate search fails.
    """
    parsed = parse_auth_policy_entity(request)
    if not parsed:
        return None

    policy_name, persona_guid, temp_guid = parsed
    existing_policy = await find_existing_policy_async(
        client, policy_name, persona_guid
    )
    if existing_policy:
        logger.info(
            f"Found existing policy '{policy_name}' with guid "
            f"{existing_policy.get('guid')} during retry check"
        )
        return create_mock_response(existing_policy, temp_guid)
    return None
