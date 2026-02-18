# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Core model classes for pyatlan_v9, migrated from pyatlan/model/core.py.

This module provides:
- AtlanTagName: Custom string-like class with sentinel pattern (plain Python class)
- Announcement: Announcement data (msgspec.Struct)
- AtlanTag: Classification/tag assignment with propagation settings (msgspec.Struct)
- Meaning: Glossary term reference (msgspec.Struct)
- AssetResponse: API response wrapper for single assets (msgspec.Struct)
- AssetRequest: API request wrapper for single assets (msgspec.Struct)
- BulkRequest: API request wrapper for bulk asset operations (msgspec.Struct)
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Union

import msgspec

from pyatlan.model.constants import DELETED_, DELETED_SENTINEL
from pyatlan.model.enums import AnnouncementType, EntityStatus
from pyatlan_v9.model.retranslators import AtlanTagRetranslator
from pyatlan_v9.model.structs import SourceTagAttachment
from pyatlan_v9.model.translators import AtlanTagTranslator

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient
    from pyatlan.client.atlan import AtlanClient


# =============================================================================
# ATLAN TAG NAME (plain Python class -- NOT a msgspec.Struct)
# =============================================================================


class AtlanTagName:
    """
    A custom string-like class representing an Atlan tag name.

    Uses a sentinel pattern so that deleted tags are represented by a single
    shared instance, allowing identity comparison.
    """

    _sentinel: Union[AtlanTagName, None] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> AtlanTagName:
        if args and args[0] == DELETED_SENTINEL and cls._sentinel:
            return cls._sentinel
        obj = super().__new__(cls)
        if args and args[0] == DELETED_SENTINEL:
            obj._display_text = DELETED_
            cls._sentinel = obj
        return obj

    def __init__(self, display_text: str) -> None:
        self._display_text = display_text

    @classmethod
    def get_deleted_sentinel(cls) -> AtlanTagName:
        """Return an AtlanTagName that is a sentinel object to represent deleted tags."""
        return cls._sentinel or cls.__new__(
            cls, DELETED_SENTINEL
        )  # Because __new__ is being invoked directly, __init__ won't be called

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_tag_name

    def __str__(self) -> str:
        return self._display_text

    def __repr__(self) -> str:
        return f"AtlanTagName({self._display_text.__repr__()})"

    def __hash__(self) -> int:
        return self._display_text.__hash__()

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, AtlanTagName)
            and self._display_text == other._display_text
        )

    @classmethod
    def _convert_to_tag_name(cls, data: Any) -> AtlanTagName:
        if isinstance(data, AtlanTagName):
            return data
        return AtlanTagName(data) if data else cls.get_deleted_sentinel()


# =============================================================================
# RESPONSE / REQUEST TRANSLATION WRAPPERS
# =============================================================================


class AtlanResponse:
    """
    Wrapper that translates backend-oriented payloads into user-friendly values.
    """

    def __init__(self, raw_json: dict[str, Any], client: Any):
        self.raw_json = raw_json
        self.client = client
        self.translators = [
            AtlanTagTranslator(client),
        ]
        self.translated = self._deep_translate(self.raw_json)

    def _deep_translate(self, data: Any) -> Any:
        if isinstance(data, dict):
            translated = data
            for translator in self.translators:
                if translator.applies_to(translated):
                    translated = translator.translate(translated)
            return {
                key: self._deep_translate(value) for key, value in translated.items()
            }
        if isinstance(data, list):
            return [self._deep_translate(item) for item in data]
        return data

    def to_dict(self) -> Any:
        """Return translated payload as Python builtins."""
        return self.translated


class AtlanRequest:
    """
    Wrapper that retranslates user-friendly payloads into backend format.
    """

    def __init__(self, instance: Any, client: Any):
        self.instance = instance
        self.client = client
        self.retranslators = [
            AtlanTagRetranslator(client),
        ]

        if isinstance(instance, (dict, list)):
            raw_json = instance
        elif hasattr(instance, "to_json") and callable(instance.to_json):
            raw_json = json.loads(instance.to_json(nested=True))
        else:
            raw_json = msgspec.to_builtins(instance)
        self.translated = self._deep_retranslate(raw_json)

    def _deep_retranslate(self, data: Any) -> Any:
        if isinstance(data, dict):
            translated = data
            for retranslator in self.retranslators:
                if retranslator.applies_to(translated):
                    translated = retranslator.retranslate(translated)
            return {
                key: self._deep_retranslate(value) for key, value in translated.items()
            }
        if isinstance(data, list):
            return [self._deep_retranslate(item) for item in data]
        return data

    def json(self, **kwargs: Any) -> str:
        """Return retranslated payload as JSON text."""
        return json.dumps(self.translated, **kwargs)


# =============================================================================
# ANNOUNCEMENT
# =============================================================================


class Announcement(msgspec.Struct, kw_only=True):
    """
    Data class representing an announcement that can be attached to an asset.
    """

    announcement_title: str
    """Title of the announcement."""

    announcement_type: AnnouncementType
    """Type of the announcement (INFORMATION, WARNING, or ISSUE)."""

    announcement_message: Union[str, None] = None
    """Optional detailed message for the announcement."""


# =============================================================================
# ATLAN TAG
# =============================================================================


class AtlanTag(msgspec.Struct, kw_only=True, rename="camel"):
    """
    Represents an Atlan classification/tag assignment on an entity.

    Includes propagation settings that control how the tag spreads
    through lineage and hierarchy relationships.
    """

    type_name: Union[str, AtlanTagName, None] = None
    """Name of the type definition that defines this instance."""

    entity_guid: Union[str, None] = None
    """Unique identifier of the entity instance."""

    entity_status: Union[EntityStatus, None] = None
    """Status of the entity (ACTIVE or DELETED)."""

    propagate: Union[bool, None] = False
    """Whether to propagate the Atlan tag (True) or not (False)."""

    remove_propagations_on_entity_delete: Union[bool, None] = True
    """Whether to remove propagated Atlan tags when the tag is removed from this asset."""

    restrict_propagation_through_lineage: Union[bool, None] = False
    """Whether to avoid propagating through lineage (True) or propagate through lineage (False)."""

    restrict_propagation_through_hierarchy: Union[bool, None] = False
    """Whether to prevent this Atlan tag from propagating through hierarchy (True) or allow it (False)."""

    validity_periods: Union[list[str], None] = None
    """Time periods during which this tag assignment is valid."""

    attributes: Union[dict[str, Any], None] = None
    """Custom attributes for this tag assignment (e.g., source tag attachments)."""

    source_tag_attachments: list[SourceTagAttachment] = msgspec.field(
        default_factory=list
    )
    """Source tag attachments extracted from classification attributes."""

    @classmethod
    def of(
        cls,
        atlan_tag_name: AtlanTagName,
        entity_guid: Union[str, None] = None,
        source_tag_attachment: Union[SourceTagAttachment, None] = None,
        client: Union[AtlanClient, None] = None,
    ) -> AtlanTag:
        """
        Construct an Atlan tag assignment for a specific entity.

        :param atlan_tag_name: human-readable name of the Atlan tag
        :param entity_guid: unique identifier (GUID) of the entity to tag
        :param source_tag_attachment: (optional) source-specific details for the tag
        :param client: (optional) client instance used for translating source-specific details
        :returns: an Atlan tag assignment with default settings for propagation
        :raises InvalidRequestError: if client is not provided and source_tag_attachment is specified
        """
        from pyatlan.errors import ErrorCode

        tag = AtlanTag(type_name=atlan_tag_name)
        if entity_guid:
            tag.entity_guid = entity_guid
            tag.entity_status = EntityStatus.ACTIVE
        if source_tag_attachment:
            if not client:
                raise ErrorCode.NO_ATLAN_CLIENT.exception_with_parameters()
            tag_id = client.atlan_tag_cache.get_id_for_name(str(atlan_tag_name))
            source_tag_attr_id = client.atlan_tag_cache.get_source_tags_attr_id(
                tag_id or ""
            )
            tag.attributes = {source_tag_attr_id: [source_tag_attachment]}  # type: ignore[dict-item]
            tag.source_tag_attachments.append(source_tag_attachment)
        return tag

    @classmethod
    async def of_async(
        cls,
        atlan_tag_name: AtlanTagName,
        entity_guid: Union[str, None] = None,
        source_tag_attachment: Union[SourceTagAttachment, None] = None,
        client: Union[AsyncAtlanClient, None] = None,
    ) -> AtlanTag:
        """
        Async version of AtlanTag.of() for use with AsyncAtlanClient.

        Construct an Atlan tag assignment for a specific entity.

        :param atlan_tag_name: human-readable name of the Atlan tag
        :param entity_guid: unique identifier (GUID) of the entity to tag
        :param source_tag_attachment: (optional) source-specific details for the tag
        :param client: (optional) async client instance used for translating source-specific details
        :returns: an Atlan tag assignment with default settings for propagation
        :raises InvalidRequestError: if client is not provided and source_tag_attachment is specified
        """
        from pyatlan.errors import ErrorCode

        tag = AtlanTag(type_name=atlan_tag_name)
        if entity_guid:
            tag.entity_guid = entity_guid
            tag.entity_status = EntityStatus.ACTIVE
        if source_tag_attachment:
            if not client:
                raise ErrorCode.NO_ATLAN_CLIENT.exception_with_parameters()
            tag_id = await client.atlan_tag_cache.get_id_for_name(str(atlan_tag_name))
            source_tag_attr_id = await client.atlan_tag_cache.get_source_tags_attr_id(
                tag_id or ""
            )
            tag.attributes = {source_tag_attr_id: [source_tag_attachment]}  # type: ignore[dict-item]
            tag.source_tag_attachments.append(source_tag_attachment)
        return tag


# =============================================================================
# MEANING
# =============================================================================


class Meaning(msgspec.Struct, kw_only=True, rename="camel"):
    """
    Represents a reference to a glossary term assigned to an entity.
    """

    term_guid: Union[str, None] = None
    """Unique identifier (GUID) of the related term."""

    relation_guid: Union[str, None] = None
    """Unique identifier (GUID) of the relationship itself."""

    display_text: Union[str, None] = None
    """Human-readable display name of the related term."""

    confidence: Union[int, None] = None
    """Confidence score for the term assignment."""


# =============================================================================
# API REQUEST / RESPONSE WRAPPERS
# =============================================================================


class AssetResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """
    Wrapper for single-asset API responses.

    Wraps the entity returned by the Atlan API along with any referred entities.
    """

    entity: Any
    """The primary asset entity returned by the API."""

    referred_entities: Union[dict[str, Any], None] = None
    """Map of related entities keyed by GUID."""


class AssetRequest(msgspec.Struct, kw_only=True, rename="camel"):
    """
    Wrapper for single-asset API requests.
    """

    entity: Any
    """The asset entity to send to the API."""


class BulkRequest(msgspec.Struct, kw_only=True, rename="camel"):
    """
    Wrapper for bulk asset API requests.

    In v9, relationship categorization (replace/append/remove semantics) is
    handled by each entity's ``to_json(nested=True)`` conversion, which calls
    ``categorize_relationships()`` under the hood.
    """

    entities: list[Any]
    """List of asset entities to send to the API in bulk."""

    def to_dict(self) -> dict:
        """
        Convert to a dict in the API nested format.

        Each entity is converted to its nested representation (with
        ``attributes``, ``relationshipAttributes``,
        ``appendRelationshipAttributes``, ``removeRelationshipAttributes``).

        Returns:
            Dict suitable for JSON serialization and API submission.
        """
        entity_dicts = []
        for entity in self.entities:
            if hasattr(entity, "to_json"):
                entity_dicts.append(json.loads(entity.to_json(nested=True)))
            else:
                entity_dicts.append(msgspec.to_builtins(entity))
        return {"entities": entity_dicts}
