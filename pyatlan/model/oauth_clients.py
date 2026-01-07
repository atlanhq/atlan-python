# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import List, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class OAuthClientRequest(AtlanObject):
    """Request object for creating an OAuth client."""

    display_name: str = Field(
        description="Human-readable name for the OAuth client.",
    )
    description: Optional[str] = Field(
        default=None,
        description="Explanation of the OAuth client.",
    )
    role: str = Field(
        description="Role assigned to the OAuth client (e.g., '$admin', '$member').",
    )
    persona_qns: Optional[List[str]] = Field(
        default=None,
        description="Qualified names of personas to associate with the OAuth client.",
    )


class OAuthClientCreateResponse(AtlanObject):
    """Response object returned when creating an OAuth client (includes client secret)."""

    id: Optional[str] = Field(
        default=None,
        description="Unique identifier (GUID) of the OAuth client.",
    )
    client_id: Optional[str] = Field(
        default=None,
        description="Unique client identifier of the OAuth client.",
        alias="clientId",
    )
    client_secret: Optional[str] = Field(
        default=None,
        description="Client secret for the OAuth client (only returned on creation).",
        alias="clientSecret",
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Human-readable name provided when creating the OAuth client.",
        alias="displayName",
    )
    description: Optional[str] = Field(
        default=None,
        description="Explanation of the OAuth client.",
    )
    token_expiry_seconds: Optional[int] = Field(
        default=None,
        description="Time in seconds after which the token will expire.",
        alias="tokenExpirySeconds",
    )
    created_at: Optional[str] = Field(
        default=None,
        description="Epoch time, in milliseconds, at which the OAuth client was created.",
        alias="createdAt",
    )
    created_by: Optional[str] = Field(
        default=None,
        description="User who created the OAuth client.",
        alias="createdBy",
    )


class OAuthClient(AtlanObject):
    """Represents an OAuth client credential in Atlan."""

    id: Optional[str] = Field(
        default=None,
        description="Unique identifier (GUID) of the OAuth client.",
    )
    client_id: Optional[str] = Field(
        default=None,
        description="Unique client identifier of the OAuth client.",
        alias="clientId",
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Human-readable name provided when creating the OAuth client.",
        alias="displayName",
    )
    description: Optional[str] = Field(
        default=None,
        description="Explanation of the OAuth client.",
    )
    role: Optional[str] = Field(
        default=None,
        description="Role assigned to the OAuth client (e.g., '$admin').",
    )
    persona_qns: Optional[List[str]] = Field(
        default=None,
        description="Qualified names of personas associated with the OAuth client.",
        alias="personaQNs",
    )
    token_expiry_seconds: Optional[int] = Field(
        default=None,
        description="Time in seconds after which the token will expire.",
        alias="tokenExpirySeconds",
    )
    created_at: Optional[str] = Field(
        default=None,
        description="Epoch time, in milliseconds, at which the OAuth client was created.",
        alias="createdAt",
    )
    created_by: Optional[str] = Field(
        default=None,
        description="User who created the OAuth client.",
        alias="createdBy",
    )
    updated_at: Optional[str] = Field(
        default=None,
        description="Epoch time, in milliseconds, at which the OAuth client was last updated.",
        alias="updatedAt",
    )
    updated_by: Optional[str] = Field(
        default=None,
        description="User who last updated the OAuth client.",
        alias="updatedBy",
    )


class OAuthClientResponse(AtlanObject):
    """Response object containing a list of OAuth clients with pagination info."""

    total_record: Optional[int] = Field(
        default=None,
        description="Total number of OAuth clients.",
        alias="totalRecord",
    )
    filter_record: Optional[int] = Field(
        default=None,
        description="Number of OAuth clients that matched the specified filters.",
        alias="filterRecord",
    )
    records: Optional[List[OAuthClient]] = Field(
        default=None,
        description="List of OAuth clients.",
    )
