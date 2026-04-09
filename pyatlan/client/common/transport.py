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
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Prefix, Term

logger = logging.getLogger(__name__)


def build_policy_search_request(
    policy_name: str, persona_qualified_name: str
) -> IndexSearchRequest:
    """
    Build an IndexSearchRequest to find an existing AuthPolicy by name and persona.
    Using persona GUID directly returns associated assets, not policies.
    Policies require a hierarchical (prefix) match to be correctly retrieved.
    """
    query = Bool(
        filter=[
            Term(field="__state", value="ACTIVE"),
            Term(field="__typeName.keyword", value="AuthPolicy"),
            Term(field="policyCategory", value="persona"),
            Term(field="name.keyword", value=policy_name),
            Prefix(field="qualifiedName", value=persona_qualified_name),
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
    if the request is a bulk POST containing a NEW AuthPolicy creation, else None.

    Only matches policy CREATES (temp GUIDs starting with "-"), not UPDATES
    (real GUIDs), to prevent suppressing legitimate policy modifications.
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

        entity_guid = entity.get("guid", "-1")
        # Only match policy CREATES (temp GUIDs like "-1", "-2", etc.)
        # Skip policy UPDATES (real GUIDs) to avoid suppressing modifications
        if not isinstance(entity_guid, str) or not entity_guid.startswith("-"):
            logger.debug(
                "parse_auth_policy_entity: skipping duplicate check for policy with GUID %s (likely an update or invalid type)",
                entity_guid,
            )
            continue

        policy_name = entity.get("attributes", {}).get("name")
        access_control = entity.get("attributes", {}).get("accessControl")
        persona_guid = (
            access_control.get("guid") if isinstance(access_control, dict) else None
        )
        if policy_name and persona_guid:
            return policy_name, persona_guid, entity_guid
    return None


def get_persona_qualified_name(client: Any, persona_guid: str) -> Optional[str]:
    """
    Fetch the qualifiedName of a Persona by its GUID via IndexSearch (synchronous).
    """
    try:
        query = Bool(
            filter=[
                Term(field="__typeName.keyword", value="Persona"),
                Term(field="__guid", value=persona_guid),
            ]
        )
        search = IndexSearchRequest(
            dsl=DSL(query=query, size=1, from_=0),
            attributes=["qualifiedName"],
        )
        raw_json = client._call_api(INDEX_SEARCH, request_obj=search)
        if raw_json and raw_json.get("entities"):
            return raw_json["entities"][0].get("attributes", {}).get("qualifiedName")
        return None
    except Exception as e:
        logger.debug(
            "get_persona_qualified_name: could not fetch qualifiedName for persona %s: %s",
            persona_guid,
            e,
        )
        return None


async def get_persona_qualified_name_async(
    client: Any, persona_guid: str
) -> Optional[str]:
    """
    Fetch the qualifiedName of a Persona by its GUID via IndexSearch (asynchronous).
    """
    try:
        query = Bool(
            filter=[
                Term(field="__typeName.keyword", value="Persona"),
                Term(field="__guid", value=persona_guid),
            ]
        )
        search = IndexSearchRequest(
            dsl=DSL(query=query, size=1, from_=0),
            attributes=["qualifiedName"],
        )
        raw_json = await client._call_api(INDEX_SEARCH, request_obj=search)
        if raw_json and raw_json.get("entities"):
            return raw_json["entities"][0].get("attributes", {}).get("qualifiedName")
        return None
    except Exception as e:
        logger.debug(
            "get_persona_qualified_name_async: could not fetch qualifiedName for persona %s: %s",
            persona_guid,
            e,
        )
        return None


def find_existing_policy(
    client: Any, policy_name: str, persona_guid: str
) -> Optional[dict]:
    """
    Search for an existing AuthPolicy by name and persona GUID (synchronous).

    First resolves the persona GUID to its qualifiedName, then uses a qualifiedName
    prefix query to scope the search to that persona.

    Raises:
        ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY: if the policy search call fails.
    """
    persona_qualified_name = get_persona_qualified_name(client, persona_guid)
    if not persona_qualified_name:
        raise ErrorCode.UNABLE_TO_RESOLVE_PERSONA_QUALIFIED_NAME.exception_with_parameters(
            persona_guid
        )

    try:
        search_request = build_policy_search_request(
            policy_name, persona_qualified_name
        )
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

    First resolves the persona GUID to its qualifiedName, then uses a qualifiedName
    prefix query to scope the search to that persona.

    Raises:
        ErrorCode.UNABLE_TO_SEARCH_EXISTING_POLICY: if the policy search call fails.
    """
    persona_qualified_name = await get_persona_qualified_name_async(
        client, persona_guid
    )
    if not persona_qualified_name:
        raise ErrorCode.UNABLE_TO_RESOLVE_PERSONA_QUALIFIED_NAME.exception_with_parameters(
            persona_guid
        )

    try:
        search_request = build_policy_search_request(
            policy_name, persona_qualified_name
        )
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
    Called before every attempt — including the first — so that repeated automation
    runs that don't pre-check for an existing policy are handled transparently.

    Returns a mock response with the existing policy if a duplicate is found,
    or None to let the request proceed normally.

    Never raises: search failures are logged and treated as "not found" so that
    a degraded index cannot block policy creation entirely.
    """
    parsed = parse_auth_policy_entity(request)
    if not parsed:
        return None

    policy_name, persona_guid, temp_guid = parsed
    try:
        existing_policy = find_existing_policy(client, policy_name, persona_guid)
    except Exception as e:
        logger.warning(
            "Duplicate policy search failed for '%s' (persona %s): %s. "
            "Proceeding with request.",
            policy_name,
            persona_guid,
            str(e),
        )
        return None
    if existing_policy:
        logger.info(
            "Found existing policy '%s' with guid %s — returning it instead of creating a duplicate.",
            policy_name,
            existing_policy.get("guid"),
        )
        return create_mock_response(existing_policy, temp_guid)
    return None


async def check_for_duplicate_policy_async(
    client: Any, request: httpx.Request
) -> Optional[httpx.Response]:
    """
    Check whether a bulk POST is creating an AuthPolicy that already exists (asynchronous).
    Called before every attempt — including the first — so that repeated automation
    runs that don't pre-check for an existing policy are handled transparently.

    Returns a mock response with the existing policy if a duplicate is found,
    or None to let the request proceed normally.

    Never raises: search failures are logged and treated as "not found" so that
    a degraded index cannot block policy creation entirely.
    """
    parsed = parse_auth_policy_entity(request)
    if not parsed:
        return None

    policy_name, persona_guid, temp_guid = parsed
    try:
        existing_policy = await find_existing_policy_async(
            client, policy_name, persona_guid
        )
    except Exception as e:
        logger.warning(
            "Duplicate policy search failed for '%s' (persona %s): %s. "
            "Proceeding with request.",
            policy_name,
            persona_guid,
            str(e),
        )
        return None
    if existing_policy:
        logger.info(
            "Found existing policy '%s' with guid %s — returning it instead of creating a duplicate.",
            policy_name,
            existing_policy.get("guid"),
        )
        return create_mock_response(existing_policy, temp_guid)
    return None
