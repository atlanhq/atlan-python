# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Atlan API client for interacting with Atlan.

This module provides both synchronous (AtlanClient) and asynchronous (AsyncAtlanClient)
clients for HTTP communication with the Atlan API.

Example (sync):
    >>> with AtlanClient("https://tenant.atlan.com", api_key="...") as client:
    ...     entity = client.asset.get_by_guid("...")
    ...     client.asset.save([entity])

Example (async):
    >>> async with AsyncAtlanClient("https://tenant.atlan.com", api_key="...") as client:
    ...     entity = await client.asset.get_by_guid("...")
    ...     await client.asset.save([entity])
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, cast

import httpx
import msgspec

from pyatlan_v9.admin import (
    AtlanGroup,
    AtlanUser,
    CreateGroupResponse,
    GroupResponse,
    UserResponse,
)
from pyatlan_v9.models.asset import Asset
from pyatlan_v9.transform import from_atlas_format, from_atlas_json, to_bulk_payload

# =============================================================================
# Shared Data Types
# =============================================================================


@dataclass
class EntityMutation:
    """Represents a single entity mutation result from the API."""

    guid: str
    type_name: str
    qualified_name: Optional[str] = None


@dataclass
class BulkResponse:
    """Response from a bulk entity operation.

    Attributes:
        created: List of entities that were newly created.
        updated: List of entities that were updated.
        deleted: List of entities that were deleted.
    """

    created: list[EntityMutation]
    updated: list[EntityMutation]
    deleted: list[EntityMutation]


class DeleteType:
    """Deletion type for asset deletion operations.

    Attributes:
        SOFT: Archive the asset (can be restored later).
        HARD: Hard delete (same as PURGE).
        PURGE: Permanently delete the asset.
    """

    SOFT = "SOFT"
    HARD = "HARD"
    PURGE = "PURGE"


@dataclass
class SearchInput:
    """Input for search operations."""

    query: dict[
        str, Any
    ]  # Raw ES query (e.g., {"term": {"__typeName.keyword": "Table"}})
    page_size: int = 20
    offset: int = 0
    attributes: list[str] | None = None  # Attributes to include in response
    sort: list[dict[str, Any]] | None = None  # ES sort specification
    include_archived: bool = (
        False  # If True, include archived/deleted assets (skip __state filter)
    )


@dataclass
class SearchResponse:
    """Response from search operations."""

    assets: list[Asset]
    total_count: int
    has_more: bool


# =============================================================================
# Exceptions
# =============================================================================


class AtlanClientError(Exception):
    """Base exception for Atlan client errors."""

    pass


class AtlanAPIError(AtlanClientError):
    """Exception raised when the Atlan API returns an error response."""

    def __init__(self, status_code: int, message: str, response_body: str = ""):
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"HTTP {status_code}: {message}")


# =============================================================================
# Shared Endpoints
# =============================================================================


class Endpoints:
    """API endpoint paths."""

    # Asset/Entity endpoints
    ENTITY_BULK = "/api/meta/entity/bulk"
    ENTITY_GUID = "/api/meta/entity/guid/{guid}"
    ENTITY_UNIQUE = "/api/meta/entity/uniqueAttribute/type/{type_name}"
    SEARCH = "/api/meta/search/indexsearch"

    # User endpoints (Heracles)
    USERS = "/api/service/users"
    USER_BY_ID = "/api/service/users/{id}"
    USER_CURRENT = "/api/service/users/current"
    USER_GROUPS = "/api/service/users/{id}/groups"
    USER_CHANGE_ROLE = "/api/service/users/{id}/roles/update"

    # Group endpoints (Heracles)
    GROUPS = "/api/service/groups"
    GROUP_BY_ID = "/api/service/groups/{id}"
    GROUP_MEMBERS = "/api/service/groups/{id}/members"
    GROUP_REMOVE_MEMBERS = "/api/service/groups/{id}/members/remove"
    GROUP_DELETE = "/api/service/groups/{id}/delete"


# =============================================================================
# Shared Parsing/Building Logic
# =============================================================================


def _parse_bulk_response(data: dict[str, Any]) -> BulkResponse:
    """Parse a bulk API response into a BulkResponse object."""
    mutation_response = data.get("mutatedEntities", {})

    def parse_mutations(mutations: list[dict[str, Any]]) -> list[EntityMutation]:
        return [
            EntityMutation(
                guid=m.get("guid", ""),
                type_name=m.get("typeName", ""),
                qualified_name=m.get("attributes", {}).get("qualifiedName"),
            )
            for m in mutations
        ]

    return BulkResponse(
        created=parse_mutations(mutation_response.get("CREATE", [])),
        updated=parse_mutations(mutation_response.get("UPDATE", [])),
        deleted=parse_mutations(mutation_response.get("DELETE", [])),
    )


def _build_headers(api_key: Optional[str]) -> dict[str, str]:
    """Build HTTP headers for API requests."""
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _check_response(response: httpx.Response) -> None:
    """Check response status and raise AtlanAPIError if needed."""
    if response.status_code >= 400:
        raise AtlanAPIError(
            status_code=response.status_code,
            message=response.reason_phrase,
            response_body=response.text,
        )


def _build_search_payload(input: SearchInput) -> dict[str, Any]:
    """Build the search API request payload."""
    # Build filter list - always include the query
    filters: list[dict[str, Any]] = [input.query]

    # By default, only return ACTIVE assets; skip this filter if include_archived=True
    if not input.include_archived:
        filters.append({"term": {"__state": "ACTIVE"}})

    dsl: dict[str, Any] = {
        "from": input.offset,
        "size": input.page_size,
        "track_total_hits": True,
        "query": {"bool": {"filter": filters}},
    }
    if input.sort:
        dsl["sort"] = input.sort
    payload: dict[str, Any] = {
        "dsl": dsl,
        "suppressLogs": True,
    }
    if input.attributes:
        payload["attributes"] = input.attributes
    return payload


def _parse_search_response(data: dict[str, Any], input: SearchInput) -> SearchResponse:
    """Parse search API response."""
    raw_entities = data.get("entities", [])
    assets = [from_atlas_format(entity) for entity in raw_entities]
    total_count = data.get("approximateCount", len(assets))
    has_more = (input.offset + len(raw_entities)) < total_count
    return SearchResponse(assets=assets, total_count=total_count, has_more=has_more)


# Msgspec decoders for admin types (reuse for performance)
_user_response_decoder = msgspec.json.Decoder(UserResponse)
_group_response_decoder = msgspec.json.Decoder(GroupResponse)
_create_group_response_decoder = msgspec.json.Decoder(CreateGroupResponse)


def _decode_user_response(content: bytes) -> UserResponse:
    """Decode user list response from JSON bytes using msgspec."""
    return _user_response_decoder.decode(content)


def _decode_group_response(content: bytes) -> GroupResponse:
    """Decode group list response from JSON bytes using msgspec."""
    return _group_response_decoder.decode(content)


def _decode_create_group_response(content: bytes) -> CreateGroupResponse:
    """Decode create group response from JSON bytes using msgspec."""
    return _create_group_response_decoder.decode(content)


# =============================================================================
# Synchronous Resource Classes
# =============================================================================


class AssetResource:
    """Synchronous resource for asset operations.

    Access via `client.asset`.
    """

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def save(self, entities: list[Asset]) -> BulkResponse:
        """Create or update entities via the bulk API.

        This method handles both creation (guid="-1" or negative) and updates
        (existing guid) transparently.

        Args:
            entities: List of Asset instances to save.

        Returns:
            BulkResponse containing the created, updated, and deleted entities.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        payload = to_bulk_payload(entities)
        response = self._http.post(Endpoints.ENTITY_BULK, json=payload)
        _check_response(response)
        return _parse_bulk_response(response.json())

    def get_by_guid(self, guid: str, include_relationships: bool = False) -> Asset:
        """Retrieve an entity by its GUID.

        Args:
            guid: The unique identifier of the entity.
            include_relationships: Whether to include relationship attributes.

        Returns:
            The Asset instance for the entity.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        params = {"ignoreRelationships": str(not include_relationships).lower()}
        url = Endpoints.ENTITY_GUID.format(guid=guid)
        response = self._http.get(url, params=params)
        _check_response(response)
        return from_atlas_json(response.content)

    def get_by_qualified_name(self, type_name: str, qualified_name: str) -> Asset:
        """Retrieve an entity by its type and qualified name.

        Args:
            type_name: The Atlas type name (e.g., "Table").
            qualified_name: The unique qualified name of the entity.

        Returns:
            The Asset instance for the entity.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.ENTITY_UNIQUE.format(type_name=type_name)
        response = self._http.get(url, params={"attr:qualifiedName": qualified_name})
        _check_response(response)
        return from_atlas_json(response.content)

    def delete(
        self,
        guids: list[str],
        delete_type: str = DeleteType.SOFT,
    ) -> BulkResponse:
        """Delete entities by their GUIDs.

        Args:
            guids: List of unique identifiers of entities to delete.
            delete_type: Type of deletion - DeleteType.SOFT (archive, default),
                DeleteType.HARD, or DeleteType.PURGE (permanent).

        Returns:
            BulkResponse containing the deleted entities.

        Raises:
            AtlanAPIError: If the API returns an error response.
            ValueError: If guids list is empty.
        """
        if not guids:
            raise ValueError("guids list cannot be empty")

        # Build query string with multiple guid parameters
        guid_params = "&".join(f"guid={guid}" for guid in guids)
        url = f"{Endpoints.ENTITY_BULK}?{guid_params}&deleteType={delete_type}"
        response = self._http.delete(url)
        _check_response(response)
        return _parse_bulk_response(response.json())

    def delete_by_guid(
        self, guid: str, delete_type: str = DeleteType.SOFT
    ) -> BulkResponse:
        """Delete an entity by its GUID.

        Convenience method that calls delete() with a single GUID.

        Args:
            guid: The unique identifier of the entity to delete.
            delete_type: Type of deletion - DeleteType.SOFT (archive, default),
                DeleteType.HARD, or DeleteType.PURGE (permanent).

        Returns:
            BulkResponse containing the deleted entity.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        return self.delete([guid], delete_type)

    def search(self, input: SearchInput) -> SearchResponse:
        """Search for assets using an ElasticSearch query.

        Args:
            input: SearchInput containing the ES query and pagination options.

        Returns:
            SearchResponse containing the matching assets.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        payload = _build_search_payload(input)
        response = self._http.post(Endpoints.SEARCH, json=payload)
        _check_response(response)
        return _parse_search_response(response.json(), input)


class UserResource:
    """Synchronous resource for user operations.

    Access via `client.users`.
    """

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def list(
        self,
        query_filter: Optional[str] = None,
        sort: str = "username",
        limit: int = 20,
        offset: int = 0,
    ) -> UserResponse:
        """List users in Atlan.

        Args:
            query_filter: RQL filter string (e.g., '{"email":{"$ilike":"%@example.com%"}}').
            sort: Property to sort by (default: "username").
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            UserResponse containing the list of users.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        params: dict[str, Any] = {
            "sort": sort,
            "limit": limit,
            "offset": offset,
            "count": "true",
        }
        if query_filter:
            params["filter"] = query_filter

        response = self._http.get(Endpoints.USERS, params=params)
        _check_response(response)
        return _decode_user_response(response.content)

    def get_by_email(self, email: str) -> List[AtlanUser]:
        """Get users by email address (partial match).

        Args:
            email: Email address or partial email to search for.

        Returns:
            List of users whose email contains the provided string.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"email":{{"$ilike":"%{email}%"}}}}'
        response = self.list(query_filter=rql_filter)
        return response.records

    def get_by_username(self, username: str) -> Optional[AtlanUser]:
        """Get a user by exact username.

        Args:
            username: The exact username to search for.

        Returns:
            The user with that username, or None if not found.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"username":"{username}"}}'
        response = self.list(query_filter=rql_filter)
        return response.records[0] if response.records else None

    def get_by_guid(self, guid: str) -> Optional[AtlanUser]:
        """Get a user by GUID.

        Args:
            guid: The unique identifier of the user.

        Returns:
            The user with that GUID, or None if not found.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"id":"{guid}"}}'
        response = self.list(query_filter=rql_filter)
        return response.records[0] if response.records else None

    def create(self, email: str, role_name: str, role_id: str) -> None:
        """Create a new user.

        Args:
            email: Email address for the new user.
            role_name: Name of the role to assign (e.g., "Admin", "Member").
            role_id: GUID of the role to assign.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        payload = {
            "users": [
                {
                    "email": email,
                    "roleName": role_name,
                    "roleId": role_id,
                }
            ]
        }
        response = self._http.post(Endpoints.USERS, json=payload)
        _check_response(response)

    def update(self, id: str, user: AtlanUser) -> dict[str, Any]:
        """Update a user.

        Note: You can only update users that have already signed up to Atlan.
        Users that are only invited (but have not yet logged in) cannot be updated.

        Args:
            id: GUID of the user to update.
            user: AtlanUser with the updated fields.

        Returns:
            Basic details about the updated user.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_BY_ID.format(id=id)
        payload = {
            "firstName": user.first_name,
            "lastName": user.last_name,
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        response = self._http.post(url, json=payload)
        _check_response(response)
        return cast(Dict[str, Any], response.json())

    def list_groups(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> GroupResponse:
        """List groups a user belongs to.

        Args:
            user_id: GUID of the user.
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            GroupResponse containing the list of groups.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_GROUPS.format(id=user_id)
        params = {"limit": limit, "offset": offset}
        response = self._http.get(url, params=params)
        _check_response(response)
        return _decode_group_response(response.content)

    def add_to_groups(self, user_id: str, group_ids: List[str]) -> None:
        """Add a user to one or more groups.

        Args:
            user_id: GUID of the user to add.
            group_ids: List of group GUIDs to add the user to.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_GROUPS.format(id=user_id)
        payload = {"groups": group_ids}
        response = self._http.post(url, json=payload)
        _check_response(response)

    def change_role(self, user_id: str, role_id: str) -> None:
        """Change the role of a user.

        Args:
            user_id: GUID of the user.
            role_id: GUID of the new role.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_CHANGE_ROLE.format(id=user_id)
        payload = {"roleId": role_id}
        response = self._http.post(url, json=payload)
        _check_response(response)

    def get_current_user(self) -> dict[str, Any]:
        """Get the current user (representing the API token).

        Returns:
            Minimal details about the current user.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        response = self._http.get(Endpoints.USER_CURRENT)
        _check_response(response)
        return cast(Dict[str, Any], response.json())


class GroupResource:
    """Synchronous resource for group operations.

    Access via `client.groups`.
    """

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    def list(
        self,
        query_filter: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> GroupResponse:
        """List groups in Atlan.

        Args:
            query_filter: RQL filter string.
            sort: Property to sort by.
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            GroupResponse containing the list of groups.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "count": "true",
        }
        if query_filter:
            params["filter"] = query_filter
        if sort:
            params["sort"] = sort

        response = self._http.get(Endpoints.GROUPS, params=params)
        _check_response(response)
        return _decode_group_response(response.content)

    def get(self, alias: str) -> List[AtlanGroup]:
        """Get groups by name (partial match on alias).

        Args:
            alias: Name of the group (as shown in UI) to search for.

        Returns:
            List of groups whose alias contains the provided string.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"$and":[{{"alias":{{"$ilike":"%{alias}%"}}}}]}}'
        response = self.list(query_filter=rql_filter)
        return response.records

    def create(
        self,
        alias: str,
        description: Optional[str] = None,
        user_ids: Optional[List[str]] = None,
    ) -> CreateGroupResponse:
        """Create a new group.

        Args:
            alias: Human-readable name for the group (as shown in UI).
            description: Optional description for the group.
            user_ids: Optional list of user GUIDs to add to the group.

        Returns:
            CreateGroupResponse with the GUID of the created group.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        group_data: dict[str, Any] = {"alias": alias}
        if description:
            group_data["description"] = description

        payload: dict[str, Any] = {"group": group_data}
        if user_ids:
            payload["users"] = user_ids

        response = self._http.post(Endpoints.GROUPS, json=payload)
        _check_response(response)
        return _decode_create_group_response(response.content)

    def update(self, id: str, group: AtlanGroup) -> None:
        """Update a group.

        Args:
            id: GUID of the group to update.
            group: AtlanGroup with the updated fields.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_BY_ID.format(id=id)
        payload: dict[str, Any] = {}
        if group.alias:
            payload["alias"] = group.alias
        if group.description:
            payload["description"] = group.description

        response = self._http.post(url, json=payload)
        _check_response(response)

    def list_members(
        self,
        group_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> UserResponse:
        """List members (users) of a group.

        Args:
            group_id: GUID of the group.
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            UserResponse containing the list of users.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_MEMBERS.format(id=group_id)
        params = {"limit": limit, "offset": offset}
        response = self._http.get(url, params=params)
        _check_response(response)
        return _decode_user_response(response.content)

    def remove_members(self, group_id: str, user_ids: List[str]) -> None:
        """Remove users from a group.

        Args:
            group_id: GUID of the group.
            user_ids: List of user GUIDs to remove.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_REMOVE_MEMBERS.format(id=group_id)
        payload = {"users": user_ids}
        response = self._http.post(url, json=payload)
        _check_response(response)

    def delete(self, id: str) -> None:
        """Delete a group.

        Args:
            id: GUID of the group to delete.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_DELETE.format(id=id)
        response = self._http.post(url, json="")
        _check_response(response)


# =============================================================================
# Asynchronous Resource Classes
# =============================================================================


class AsyncAssetResource:
    """Asynchronous resource for asset operations.

    Access via `client.asset`.
    """

    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def save(self, entities: list[Asset]) -> BulkResponse:
        """Create or update entities via the bulk API.

        This method handles both creation (guid="-1" or negative) and updates
        (existing guid) transparently.

        Args:
            entities: List of Asset instances to save.

        Returns:
            BulkResponse containing the created, updated, and deleted entities.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        payload = to_bulk_payload(entities)
        response = await self._http.post(Endpoints.ENTITY_BULK, json=payload)
        _check_response(response)
        return _parse_bulk_response(response.json())

    async def get_by_guid(
        self, guid: str, include_relationships: bool = False
    ) -> Asset:
        """Retrieve an entity by its GUID.

        Args:
            guid: The unique identifier of the entity.
            include_relationships: Whether to include relationship attributes.

        Returns:
            The Asset instance for the entity.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        params = {"ignoreRelationships": str(not include_relationships).lower()}
        url = Endpoints.ENTITY_GUID.format(guid=guid)
        response = await self._http.get(url, params=params)
        _check_response(response)
        return from_atlas_json(response.content)

    async def get_by_qualified_name(self, type_name: str, qualified_name: str) -> Asset:
        """Retrieve an entity by its type and qualified name.

        Args:
            type_name: The Atlas type name (e.g., "Table").
            qualified_name: The unique qualified name of the entity.

        Returns:
            The Asset instance for the entity.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.ENTITY_UNIQUE.format(type_name=type_name)
        response = await self._http.get(
            url, params={"attr:qualifiedName": qualified_name}
        )
        _check_response(response)
        return from_atlas_json(response.content)

    async def delete(
        self,
        guids: list[str],
        delete_type: str = DeleteType.SOFT,
    ) -> BulkResponse:
        """Delete entities by their GUIDs.

        Args:
            guids: List of unique identifiers of entities to delete.
            delete_type: Type of deletion - DeleteType.SOFT (archive, default),
                DeleteType.HARD, or DeleteType.PURGE (permanent).

        Returns:
            BulkResponse containing the deleted entities.

        Raises:
            AtlanAPIError: If the API returns an error response.
            ValueError: If guids list is empty.
        """
        if not guids:
            raise ValueError("guids list cannot be empty")

        # Build query string with multiple guid parameters
        guid_params = "&".join(f"guid={guid}" for guid in guids)
        url = f"{Endpoints.ENTITY_BULK}?{guid_params}&deleteType={delete_type}"
        response = await self._http.delete(url)
        _check_response(response)
        return _parse_bulk_response(response.json())

    async def delete_by_guid(
        self, guid: str, delete_type: str = DeleteType.SOFT
    ) -> BulkResponse:
        """Delete an entity by its GUID.

        Convenience method that calls delete() with a single GUID.

        Args:
            guid: The unique identifier of the entity to delete.
            delete_type: Type of deletion - DeleteType.SOFT (archive, default),
                DeleteType.HARD, or DeleteType.PURGE (permanent).

        Returns:
            BulkResponse containing the deleted entity.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        return await self.delete([guid], delete_type)

    async def search(self, input: SearchInput) -> SearchResponse:
        """Search for assets using an ElasticSearch query.

        Args:
            input: SearchInput containing the ES query and pagination options.

        Returns:
            SearchResponse containing the matching assets.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        payload = _build_search_payload(input)
        response = await self._http.post(Endpoints.SEARCH, json=payload)
        _check_response(response)
        return _parse_search_response(response.json(), input)


class AsyncUserResource:
    """Asynchronous resource for user operations.

    Access via `client.users`.
    """

    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def list(
        self,
        query_filter: Optional[str] = None,
        sort: str = "username",
        limit: int = 20,
        offset: int = 0,
    ) -> UserResponse:
        """List users in Atlan.

        Args:
            query_filter: RQL filter string (e.g., '{"email":{"$ilike":"%@example.com%"}}').
            sort: Property to sort by (default: "username").
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            UserResponse containing the list of users.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        params: dict[str, Any] = {
            "sort": sort,
            "limit": limit,
            "offset": offset,
            "count": "true",
        }
        if query_filter:
            params["filter"] = query_filter

        response = await self._http.get(Endpoints.USERS, params=params)
        _check_response(response)
        return _decode_user_response(response.content)

    async def get_by_email(self, email: str) -> List[AtlanUser]:
        """Get users by email address (partial match).

        Args:
            email: Email address or partial email to search for.

        Returns:
            List of users whose email contains the provided string.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"email":{{"$ilike":"%{email}%"}}}}'
        response = await self.list(query_filter=rql_filter)
        return response.records

    async def get_by_username(self, username: str) -> Optional[AtlanUser]:
        """Get a user by exact username.

        Args:
            username: The exact username to search for.

        Returns:
            The user with that username, or None if not found.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"username":"{username}"}}'
        response = await self.list(query_filter=rql_filter)
        return response.records[0] if response.records else None

    async def get_by_guid(self, guid: str) -> Optional[AtlanUser]:
        """Get a user by GUID.

        Args:
            guid: The unique identifier of the user.

        Returns:
            The user with that GUID, or None if not found.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"id":"{guid}"}}'
        response = await self.list(query_filter=rql_filter)
        return response.records[0] if response.records else None

    async def create(self, email: str, role_name: str, role_id: str) -> None:
        """Create a new user.

        Args:
            email: Email address for the new user.
            role_name: Name of the role to assign (e.g., "Admin", "Member").
            role_id: GUID of the role to assign.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        payload = {
            "users": [
                {
                    "email": email,
                    "roleName": role_name,
                    "roleId": role_id,
                }
            ]
        }
        response = await self._http.post(Endpoints.USERS, json=payload)
        _check_response(response)

    async def update(self, id: str, user: AtlanUser) -> dict[str, Any]:
        """Update a user.

        Note: You can only update users that have already signed up to Atlan.
        Users that are only invited (but have not yet logged in) cannot be updated.

        Args:
            id: GUID of the user to update.
            user: AtlanUser with the updated fields.

        Returns:
            Basic details about the updated user.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_BY_ID.format(id=id)
        payload = {
            "firstName": user.first_name,
            "lastName": user.last_name,
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        response = await self._http.post(url, json=payload)
        _check_response(response)
        return cast(Dict[str, Any], response.json())

    async def list_groups(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> GroupResponse:
        """List groups a user belongs to.

        Args:
            user_id: GUID of the user.
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            GroupResponse containing the list of groups.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_GROUPS.format(id=user_id)
        params = {"limit": limit, "offset": offset}
        response = await self._http.get(url, params=params)
        _check_response(response)
        return _decode_group_response(response.content)

    async def add_to_groups(self, user_id: str, group_ids: List[str]) -> None:
        """Add a user to one or more groups.

        Args:
            user_id: GUID of the user to add.
            group_ids: List of group GUIDs to add the user to.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_GROUPS.format(id=user_id)
        payload = {"groups": group_ids}
        response = await self._http.post(url, json=payload)
        _check_response(response)

    async def change_role(self, user_id: str, role_id: str) -> None:
        """Change the role of a user.

        Args:
            user_id: GUID of the user.
            role_id: GUID of the new role.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.USER_CHANGE_ROLE.format(id=user_id)
        payload = {"roleId": role_id}
        response = await self._http.post(url, json=payload)
        _check_response(response)

    async def get_current_user(self) -> dict[str, Any]:
        """Get the current user (representing the API token).

        Returns:
            Minimal details about the current user.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        response = await self._http.get(Endpoints.USER_CURRENT)
        _check_response(response)
        return cast(Dict[str, Any], response.json())


class AsyncGroupResource:
    """Asynchronous resource for group operations.

    Access via `client.groups`.
    """

    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def list(
        self,
        query_filter: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> GroupResponse:
        """List groups in Atlan.

        Args:
            query_filter: RQL filter string.
            sort: Property to sort by.
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            GroupResponse containing the list of groups.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "count": "true",
        }
        if query_filter:
            params["filter"] = query_filter
        if sort:
            params["sort"] = sort

        response = await self._http.get(Endpoints.GROUPS, params=params)
        _check_response(response)
        return _decode_group_response(response.content)

    async def get(self, alias: str) -> List[AtlanGroup]:
        """Get groups by name (partial match on alias).

        Args:
            alias: Name of the group (as shown in UI) to search for.

        Returns:
            List of groups whose alias contains the provided string.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        rql_filter = f'{{"$and":[{{"alias":{{"$ilike":"%{alias}%"}}}}]}}'
        response = await self.list(query_filter=rql_filter)
        return response.records

    async def create(
        self,
        alias: str,
        description: Optional[str] = None,
        user_ids: Optional[List[str]] = None,
    ) -> CreateGroupResponse:
        """Create a new group.

        Args:
            alias: Human-readable name for the group (as shown in UI).
            description: Optional description for the group.
            user_ids: Optional list of user GUIDs to add to the group.

        Returns:
            CreateGroupResponse with the GUID of the created group.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        group_data: dict[str, Any] = {"alias": alias}
        if description:
            group_data["description"] = description

        payload: dict[str, Any] = {"group": group_data}
        if user_ids:
            payload["users"] = user_ids

        response = await self._http.post(Endpoints.GROUPS, json=payload)
        _check_response(response)
        return _decode_create_group_response(response.content)

    async def update(self, id: str, group: AtlanGroup) -> None:
        """Update a group.

        Args:
            id: GUID of the group to update.
            group: AtlanGroup with the updated fields.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_BY_ID.format(id=id)
        payload: dict[str, Any] = {}
        if group.alias:
            payload["alias"] = group.alias
        if group.description:
            payload["description"] = group.description

        response = await self._http.post(url, json=payload)
        _check_response(response)

    async def list_members(
        self,
        group_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> UserResponse:
        """List members (users) of a group.

        Args:
            group_id: GUID of the group.
            limit: Maximum number of results to return.
            offset: Starting point for results (for paging).

        Returns:
            UserResponse containing the list of users.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_MEMBERS.format(id=group_id)
        params = {"limit": limit, "offset": offset}
        response = await self._http.get(url, params=params)
        _check_response(response)
        return _decode_user_response(response.content)

    async def remove_members(self, group_id: str, user_ids: List[str]) -> None:
        """Remove users from a group.

        Args:
            group_id: GUID of the group.
            user_ids: List of user GUIDs to remove.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_REMOVE_MEMBERS.format(id=group_id)
        payload = {"users": user_ids}
        response = await self._http.post(url, json=payload)
        _check_response(response)

    async def delete(self, id: str) -> None:
        """Delete a group.

        Args:
            id: GUID of the group to delete.

        Raises:
            AtlanAPIError: If the API returns an error response.
        """
        url = Endpoints.GROUP_DELETE.format(id=id)
        response = await self._http.post(url, json="")
        _check_response(response)


# =============================================================================
# Synchronous Client
# =============================================================================


class AtlanClient:
    """Synchronous client for interacting with the Atlan API.

    Resources are accessed via namespaced properties:
    - `client.asset` - Asset operations (save, get_by_guid, search, etc.)
    - `client.users` - User operations (list, create, update, etc.)
    - `client.groups` - Group operations (list, create, update, etc.)

    Example:
        >>> with AtlanClient("https://tenant.atlan.com", api_key="...") as client:
        ...     table = client.asset.get_by_guid("...")
        ...     print(table.name)
        ...     users = client.users.list()
        ...     groups = client.groups.list()
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """Initialize the Atlan client.

        Args:
            base_url: The base URL of the Atlan instance.
            api_key: Optional API key for authentication.
            timeout: Request timeout in seconds (default: 30).
        """
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(
            base_url=self.base_url,
            headers=_build_headers(api_key),
            timeout=timeout,
        )
        # Initialize resource namespaces
        self._asset = AssetResource(self._http)
        self._users = UserResource(self._http)
        self._groups = GroupResource(self._http)
        # Initialize cache placeholders (used by Connection.creator for validation)
        self._role_cache = None
        self._user_cache = None
        self._group_cache = None

    @property
    def asset(self) -> AssetResource:
        """Asset operations (save, get_by_guid, search, delete)."""
        return self._asset

    @property
    def users(self) -> UserResource:
        """User operations (list, get_by_email, get_by_username, create, update, etc.)."""
        return self._users

    @property
    def groups(self) -> GroupResource:
        """Group operations (list, get, create, update, list_members, etc.)."""
        return self._groups

    @property
    def role_cache(self):
        """Cache for role validation."""
        return self._role_cache

    @property
    def user_cache(self):
        """Cache for user validation."""
        return self._user_cache

    @property
    def group_cache(self):
        """Cache for group validation."""
        return self._group_cache

    def __enter__(self) -> "AtlanClient":
        """Enter context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit context manager and close the HTTP client."""
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()


# =============================================================================
# Asynchronous Client
# =============================================================================


class AsyncAtlanClient:
    """Asynchronous client for interacting with the Atlan API.

    Resources are accessed via namespaced properties:
    - `client.asset` - Asset operations (save, get_by_guid, search, etc.)
    - `client.users` - User operations (list, create, update, etc.)
    - `client.groups` - Group operations (list, create, update, etc.)

    Example:
        >>> async with AsyncAtlanClient("https://tenant.atlan.com", api_key="...") as client:
        ...     table = await client.asset.get_by_guid("...")
        ...     print(table.name)
        ...     users = await client.users.list()
        ...     groups = await client.groups.list()
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """Initialize the async Atlan client.

        Args:
            base_url: The base URL of the Atlan instance.
            api_key: Optional API key for authentication.
            timeout: Request timeout in seconds (default: 30).
        """
        self.base_url = base_url.rstrip("/")
        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            headers=_build_headers(api_key),
            timeout=timeout,
        )
        # Initialize resource namespaces
        self._asset = AsyncAssetResource(self._http)
        self._users = AsyncUserResource(self._http)
        self._groups = AsyncGroupResource(self._http)

    @property
    def asset(self) -> AsyncAssetResource:
        """Asset operations (save, get_by_guid, search, delete)."""
        return self._asset

    @property
    def users(self) -> AsyncUserResource:
        """User operations (list, get_by_email, get_by_username, create, update, etc.)."""
        return self._users

    @property
    def groups(self) -> AsyncGroupResource:
        """Group operations (list, get, create, update, list_members, etc.)."""
        return self._groups

    async def __aenter__(self) -> "AsyncAtlanClient":
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit async context manager and close the HTTP client."""
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()
