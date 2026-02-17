# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.

from __future__ import annotations

import json
from typing import Any, Union

import msgspec

from pyatlan.model.constants import SERVICE_ACCOUNT_


class ApiTokenPersona(msgspec.Struct, kw_only=True, frozen=True):
    """Persona linked to an API token."""

    guid: Union[str, None] = msgspec.field(default=None, name="id")
    """Unique identifier (GUID) of the linked persona."""

    persona: Union[str, None] = None
    """Unique name of the linked persona."""

    persona_qualified_name: Union[str, None] = None
    """Unique qualified_name of the persona."""


class ApiTokenAttributes(msgspec.Struct, kw_only=True):
    """Detailed characteristics of an API token."""

    access_token_lifespan: Union[int, None] = msgspec.field(
        default=None, name="access.token.lifespan"
    )
    """Time, in seconds, from created_at after which the token will expire."""

    access_token: Union[str, None] = None
    """The actual API token that can be used as a bearer token."""

    client_id: Union[str, None] = None
    """Unique client identifier (GUID) of the API token."""

    created_at: Union[int, None] = None
    """Epoch time, in milliseconds, at which the API token was created."""

    created_by: Union[str, None] = None
    """User who created the API token."""

    description: Union[str, None] = None
    """Explanation of the API token."""

    display_name: Union[str, None] = None
    """Human-readable name provided when creating the token."""

    personas: Union[list[Any], None] = msgspec.field(default_factory=list)
    """Deprecated (now unused): personas associated with the API token."""

    persona_qualified_name: Union[set[ApiTokenPersona], None] = msgspec.field(
        default_factory=set
    )
    """Personas associated with the API token."""

    purposes: Union[Any, None] = None
    """Possible future placeholder for purposes associated with the token."""

    workspace_permissions: Union[set[str], None] = msgspec.field(default_factory=set)
    """Detailed permissions given to the API token."""

    def __post_init__(self) -> None:
        """Handle JSON string values for embedded objects."""
        if isinstance(self.workspace_permissions, str):
            self.workspace_permissions = set(json.loads(self.workspace_permissions))
        if isinstance(self.personas, str):
            self.personas = json.loads(self.personas)
        if isinstance(self.persona_qualified_name, str):
            persona_qns = json.loads(self.persona_qualified_name)
            self.persona_qualified_name = {
                ApiTokenPersona(persona_qualified_name=qn) for qn in persona_qns
            }


class ApiToken(msgspec.Struct, kw_only=True):
    """Representation of an API token in Atlan."""

    guid: Union[str, None] = msgspec.field(default=None, name="id")
    """Unique identifier (GUID) of the API token."""

    client_id: Union[str, None] = msgspec.field(default=None, name="clientId")
    """Unique client identifier (GUID) of the API token."""

    display_name: Union[str, None] = msgspec.field(default=None, name="displayName")
    """Human-readable name provided when creating the token."""

    attributes: Union[ApiTokenAttributes, None] = None
    """Detailed characteristics of the API token."""

    def __post_init__(self) -> None:
        """Copy values from attributes to top-level fields."""
        if self.attributes:
            if self.attributes.display_name and not self.display_name:
                self.display_name = self.attributes.display_name
            if self.attributes.client_id and not self.client_id:
                self.client_id = self.attributes.client_id

    @property
    def username(self) -> str:
        """Username for the API token (service account format)."""
        cid = self.client_id or (self.attributes.client_id if self.attributes else None)
        return SERVICE_ACCOUNT_ + cid if cid else ""


class ApiTokenRequest(msgspec.Struct, kw_only=True):
    """Request to create an API token."""

    # 5 years in seconds (reverted from 13 years due to Keycloak overflow)
    _MAX_VALIDITY: int = 157680000

    display_name: Union[str, None] = None
    """Human-readable name provided when creating the token."""

    description: str = ""
    """Explanation of the token."""

    personas: Union[set[str], None] = None
    """Deprecated (now unused): GUIDs of personas associated with the token."""

    persona_qualified_names: Union[set[str], None] = None
    """Unique qualified_names of personas associated with the token."""

    validity_seconds: Union[int, None] = None
    """Length of time, in seconds, after which the token will expire."""

    def __post_init__(self) -> None:
        """Validate and clamp validity_seconds."""
        if self.validity_seconds is not None:
            if self.validity_seconds < 0:
                self.validity_seconds = self._MAX_VALIDITY
            else:
                self.validity_seconds = min(self.validity_seconds, self._MAX_VALIDITY)
        if self.personas is not None and not self.personas:
            self.personas = set()


class ApiTokenResponse(msgspec.Struct, kw_only=True):
    """Response containing API token information."""

    total_record: Union[int, None] = None
    """Total number of API tokens."""

    filter_record: Union[int, None] = None
    """Number of API records that matched the specified filters."""

    records: Union[list[ApiToken], None] = None
    """Actual API tokens that matched the specified filters."""
