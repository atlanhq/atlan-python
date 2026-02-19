# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)

from __future__ import annotations

from typing import Type, TypeVar, Union

import msgspec

from pyatlan.model.assets import Asset

A = TypeVar("A", bound=Asset)


class MutatedEntities(msgspec.Struct, kw_only=True):
    """Entities that were mutated during an API operation."""

    CREATE: Union[list[Asset], None] = msgspec.field(default=None, name="CREATE")
    """Assets that were created."""

    UPDATE: Union[list[Asset], None] = msgspec.field(default=None, name="UPDATE")
    """Assets that were updated."""

    DELETE: Union[list[Asset], None] = msgspec.field(default=None, name="DELETE")
    """Assets that were deleted."""

    PARTIAL_UPDATE: Union[list[Asset], None] = msgspec.field(
        default=None, name="PARTIAL_UPDATE"
    )
    """Assets that were partially updated."""


class AssetMutationResponse(msgspec.Struct, kw_only=True):
    """Response from an asset mutation operation."""

    guid_assignments: Union[dict[str, str], None] = None
    """Map of assigned unique identifiers for the changed assets."""

    mutated_entities: Union[MutatedEntities, None] = None
    """Assets that were changed."""

    partial_updated_entities: Union[list[Asset], None] = None
    """Assets that were partially updated."""

    def assets_created(self, asset_type: Type[A]) -> list[A]:
        """Return created assets matching the given type."""
        if self.mutated_entities and self.mutated_entities.CREATE:
            return [
                asset
                for asset in self.mutated_entities.CREATE
                if isinstance(asset, asset_type)
            ]
        return []

    def assets_updated(self, asset_type: Type[A]) -> list[A]:
        """Return updated assets matching the given type."""
        if self.mutated_entities and self.mutated_entities.UPDATE:
            return [
                asset
                for asset in self.mutated_entities.UPDATE
                if isinstance(asset, asset_type)
            ]
        return []

    def assets_deleted(self, asset_type: Type[A]) -> list[A]:
        """Return deleted assets matching the given type."""
        if self.mutated_entities and self.mutated_entities.DELETE:
            return [
                asset
                for asset in self.mutated_entities.DELETE
                if isinstance(asset, asset_type)
            ]
        return []

    def assets_partially_updated(self, asset_type: Type[A]) -> list[A]:
        """Return partially updated assets matching the given type."""
        if self.mutated_entities and self.mutated_entities.PARTIAL_UPDATE:
            return [
                asset
                for asset in self.mutated_entities.PARTIAL_UPDATE
                if isinstance(asset, asset_type)
            ]
        return []


class AccessTokenResponse(msgspec.Struct, kw_only=True):
    """Response from an OAuth token request."""

    access_token: str
    """The access token."""

    expires_in: Union[int, None] = None
    """Token expiry time in seconds."""

    refresh_expires_in: Union[int, None] = None
    """Refresh token expiry time in seconds."""

    refresh_token: Union[str, None] = None
    """The refresh token."""

    token_type: Union[str, None] = None
    """Type of the token (e.g. 'Bearer')."""

    not_before_policy: Union[int, None] = None

    session_state: Union[str, None] = None

    scope: Union[str, None] = None
    """Scope of the token."""
