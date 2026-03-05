# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Union

import msgspec


class Credential(msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"):
    """Credential used for connectivity to external systems."""

    id: Union[str, None] = None
    """Unique identifier (GUID) of the credential."""

    name: Union[str, None] = None
    """Name of the credential."""

    description: Union[str, None] = None
    """Description of the credential."""

    host: Union[str, None] = None
    """Hostname for which connectivity is defined by the credential."""

    port: Union[int, None] = None
    """Port number on which connectivity should be done."""

    auth_type: Union[str, None] = None
    """Authentication mechanism represented by the credential."""

    connector_type: Union[str, None] = None
    """Type of connector used by the credential."""

    username: Union[str, None] = None
    """Less sensitive portion of the credential (e.g. username or client ID)."""

    password: Union[str, None] = None
    """More sensitive portion of the credential (e.g. password or client secret)."""

    extras: Union[dict[str, Any], None] = msgspec.field(default=None, name="extra")
    """Additional details about the credential (e.g. database, role, warehouse)."""

    connector_config_name: Union[str, None] = None
    """Name of the connector configuration responsible for managing the credential."""

    metadata: Union[dict[str, Any], None] = None

    level: Union[dict[str, Any], str, None] = None

    connector: Union[str, None] = None
    """Name of the connector used by the credential."""


class CredentialResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """Response from a credential lookup."""

    id: Union[str, None] = None
    version: Union[str, None] = None
    is_active: Union[bool, None] = None
    created_at: Union[int, None] = None
    updated_at: Union[int, None] = None
    created_by: Union[str, None] = None
    tenant_id: Union[str, None] = None
    name: Union[str, None] = None
    description: Union[str, None] = None
    connector_config_name: Union[str, None] = None
    connector: Union[str, None] = None
    connector_type: Union[str, None] = None
    auth_type: Union[str, None] = None
    host: Union[str, None] = None
    port: Union[int, None] = None
    metadata: Union[dict[str, Any], None] = None
    level: Union[dict[str, Any], str, None] = None
    connection: Union[dict[str, Any], str, None] = None
    username: Union[str, None] = None
    extras: Union[dict[str, Any], None] = msgspec.field(default=None, name="extra")

    def to_credential(self) -> Credential:
        """
        Convert this response into a credential instance.

        Note: The password field must still be populated manually,
        as it will never be returned by a credential lookup for security reasons.
        """
        return Credential(
            id=self.id,
            name=self.name,
            host=self.host,
            port=self.port,
            auth_type=self.auth_type,
            connector_type=self.connector_type,
            connector_config_name=self.connector_config_name,
            username=self.username,
            extras=self.extras,
        )


class CredentialListResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """Response containing a list of CredentialResponse objects."""

    records: list[CredentialResponse] = msgspec.field(default_factory=list)
    """List of credential records returned."""


class CredentialTestResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """Response from testing a credential's connectivity."""

    code: Union[int, None] = None
    error: Union[str, None] = None
    info: Union[object, None] = None
    message: str
    request_id: Union[str, None] = None

    @property
    def is_successful(self) -> bool:
        """Whether the test was successful (True) or failed (False)."""
        return self.message == "successful"
