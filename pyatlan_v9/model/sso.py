# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

import json
from typing import Union

import msgspec


class SSOMapperConfig(msgspec.Struct, kw_only=True, rename="camel", omit_defaults=True):
    """Configuration for an SSO mapper."""

    sync_mode: Union[str, None] = None
    attributes: Union[str, None] = None
    group_name: Union[str, None] = msgspec.field(default=None, name="group")
    """Group name for the mapper."""
    attribute_name: Union[str, None] = msgspec.field(
        default=None, name="attribute.name"
    )
    attribute_value: Union[str, None] = msgspec.field(
        default=None, name="attribute.value"
    )
    attribute_friendly_name: Union[str, None] = msgspec.field(
        default=None, name="attribute.friendly.name"
    )
    attribute_values_regex: Union[str, None] = msgspec.field(
        default=None, name="are.attribute.values.regex"
    )


class SSOMapper(msgspec.Struct, kw_only=True, rename="camel", omit_defaults=True):
    """SSO identity provider mapper."""

    id: Union[str, None] = None
    name: Union[str, None] = None
    identity_provider_mapper: str
    identity_provider_alias: str
    config: SSOMapperConfig

    def to_dict(self) -> dict:
        """Serialize to dict, excluding fields with None/default values."""
        return json.loads(msgspec.json.encode(self))


class SSOProvider(msgspec.Struct, kw_only=True, rename="camel", omit_defaults=True):
    """
    A tenant's SSO identity provider configuration (Keycloak identity
    provider representation), as returned by `GET /api/service/idp`.

    The nested `config` is an untyped mapping so that every key returned
    by the API is sent back verbatim on update - the backend treats
    updates as full replacements, and omitted keys may be reset.

    Note: unlike the pydantic model, msgspec cannot capture unknown
    top-level fields; if the API adds new top-level fields they must be
    added here to survive a get-then-update round-trip.
    """

    alias: Union[str, None] = None
    internal_id: Union[str, None] = None
    display_name: Union[str, None] = None
    provider_id: Union[str, None] = None
    enabled: Union[bool, None] = None
    trust_email: Union[bool, None] = None
    store_token: Union[bool, None] = None
    link_only: Union[bool, None] = None
    add_read_token_role_on_create: Union[bool, None] = None
    first_broker_login_flow_alias: Union[str, None] = None
    post_broker_login_flow_alias: Union[str, None] = None
    authenticate_by_default: Union[bool, None] = None
    update_profile_first_login_mode: Union[str, None] = None
    hide_on_login: Union[bool, None] = None
    organization_id: Union[str, None] = None
    config: Union[dict, None] = None

    def to_dict(self) -> dict:
        """Serialize to dict, excluding fields with None/default values."""
        return json.loads(msgspec.json.encode(self))
