# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

import json
from typing import Union

import msgspec


class SSOMapperConfig(
    msgspec.Struct, kw_only=True, rename="camel", omit_defaults=True
):
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
