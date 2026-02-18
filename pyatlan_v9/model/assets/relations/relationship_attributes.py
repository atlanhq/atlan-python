# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""
Relationship attribute models for v9 (msgspec.Struct).

Each class holds relationship-specific attributes and provides builder methods
that return Related{Type} instances with ``relationship_type`` and
``relationship_attributes`` populated for serialization.
"""

from __future__ import annotations

from typing import Any, Optional, Union

from msgspec import UNSET, UnsetType

from pyatlan_v9.model.assets.related_entity import RelatedEntity, SaveSemantic


# ---------------------------------------------------------------------------
# Helper: build a Related reference from a relationship + related entity
# ---------------------------------------------------------------------------


def _build_related(
    related_cls: type,
    related: Any,
    relationship_type_name: str,
    attrs_dict: dict[str, Any],
    semantic: SaveSemantic,
) -> RelatedEntity:
    """Build a ``Related{Type}`` reference with relationship attributes.

    Parameters
    ----------
    related_cls:
        The ``Related{Type}`` class to instantiate (e.g. ``RelatedAtlasGlossaryTerm``).
        May be ``None``; in that case ``RelatedReferenceable`` is used.
    related:
        The entity being referenced (must have ``guid`` and/or ``qualified_name``).
    relationship_type_name:
        The wire-format relationship type name (e.g. ``"AtlasGlossaryTermCategorization"``).
    attrs_dict:
        The relationship-specific attributes as a plain dict.
    semantic:
        Save semantic for the relationship.
    """
    kwargs: dict[str, Any] = {}

    guid = getattr(related, "guid", UNSET)
    if guid is not UNSET and guid is not None:
        kwargs["guid"] = guid

    qn = getattr(related, "qualified_name", UNSET)
    if qn is not UNSET and qn is not None:
        kwargs["unique_attributes"] = {"qualifiedName": qn}

    # Build the relationship attributes sub-object
    rel_attrs: dict[str, Any] = {
        "typeName": relationship_type_name,
        "attributes": attrs_dict,
    }

    kwargs["relationship_type"] = relationship_type_name
    kwargs["relationship_attributes"] = rel_attrs
    kwargs["semantic"] = semantic

    return related_cls(**kwargs)


def _build_generic_related(
    related: Any,
    relationship_type_name: str,
    attrs_dict: dict[str, Any],
    semantic: SaveSemantic,
) -> RelatedEntity:
    """Build a ``RelatedReferenceable`` reference for generic relationships.

    Used when the related entity type is not known at class-definition time
    (e.g. ``UserDefRelationship``, ``CustomRelated…``).
    """
    from pyatlan_v9.model.assets.referenceable_related import RelatedReferenceable

    kwargs: dict[str, Any] = {}

    guid = getattr(related, "guid", UNSET)
    if guid is not UNSET and guid is not None:
        kwargs["guid"] = guid

    qn = getattr(related, "qualified_name", UNSET)
    if qn is not UNSET and qn is not None:
        kwargs["unique_attributes"] = {"qualifiedName": qn}

    # Preserve the related entity's type_name
    tn = getattr(related, "type_name", UNSET)
    if tn is not UNSET and tn is not None:
        kwargs["type_name"] = tn

    rel_attrs: dict[str, Any] = {
        "typeName": relationship_type_name,
        "attributes": attrs_dict,
    }

    kwargs["relationship_type"] = relationship_type_name
    kwargs["relationship_attributes"] = rel_attrs
    kwargs["semantic"] = semantic

    return RelatedReferenceable(**kwargs)


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------


class RelationshipAttributes:
    """Base class for all v9 relationship attribute models."""

    type_name: str = ""

    def _attrs_dict(self) -> dict[str, Any]:
        """Return the relationship-specific attributes as a plain dict.

        Subclasses should override this.
        """
        return {}


# ---------------------------------------------------------------------------
# IndistinctRelationship (fallback for unknown relationship types)
# ---------------------------------------------------------------------------


class IndistinctRelationship(RelationshipAttributes):
    """Fallback relationship model for relationship types not modelled in the SDK."""

    def __init__(
        self,
        type_name: str = "IndistinctRelationship",
        attributes: Optional[dict[str, Any]] = None,
    ):
        self.type_name = type_name
        self.attributes = attributes or {}

    def _attrs_dict(self) -> dict[str, Any]:
        return dict(self.attributes)


# ---------------------------------------------------------------------------
# Glossary term-to-category relationship
# ---------------------------------------------------------------------------


class AtlasGlossaryTermCategorization(RelationshipAttributes):
    """Relationship: organises terms into categories."""

    type_name = "AtlasGlossaryTermCategorization"

    def __init__(
        self,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ):
        self.description = description
        self.status = status

    def _attrs_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.description is not None:
            d["description"] = self.description
        if self.status is not None:
            d["status"] = self.status
        return d

    # Builder methods -------------------------------------------------------

    def terms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        """Build a reference for the *terms* end of the relationship."""
        from pyatlan_v9.model.assets.gtc_related import RelatedAtlasGlossaryTerm

        return _build_related(
            RelatedAtlasGlossaryTerm,
            related,
            self.type_name,
            self._attrs_dict(),
            semantic,
        )

    def categories(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        """Build a reference for the *categories* end of the relationship."""
        from pyatlan_v9.model.assets.gtc_related import RelatedAtlasGlossaryCategory

        return _build_related(
            RelatedAtlasGlossaryCategory,
            related,
            self.type_name,
            self._attrs_dict(),
            semantic,
        )


# ---------------------------------------------------------------------------
# Common glossary-term relationship base (shared attrs: description, expression,
# status, steward, source)
# ---------------------------------------------------------------------------


class _GlossaryTermRelationship(RelationshipAttributes):
    """Base for glossary term-to-term relationships with the common attribute set."""

    def __init__(
        self,
        description: Optional[str] = None,
        expression: Optional[str] = None,
        status: Optional[str] = None,
        steward: Optional[str] = None,
        source: Optional[str] = None,
    ):
        self.description = description
        self.expression = expression
        self.status = status
        self.steward = steward
        self.source = source

    def _attrs_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.description is not None:
            d["description"] = self.description
        if self.expression is not None:
            d["expression"] = self.expression
        if self.status is not None:
            d["status"] = self.status
        if self.steward is not None:
            d["steward"] = self.steward
        if self.source is not None:
            d["source"] = self.source
        return d

    # Convenience builder for RelatedAtlasGlossaryTerm
    def _term_ref(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        from pyatlan_v9.model.assets.gtc_related import RelatedAtlasGlossaryTerm

        return _build_related(
            RelatedAtlasGlossaryTerm,
            related,
            self.type_name,
            self._attrs_dict(),
            semantic,
        )


# ---------------------------------------------------------------------------
# AtlasGlossaryIsARelationship
# ---------------------------------------------------------------------------


class AtlasGlossaryIsARelationship(_GlossaryTermRelationship):
    """Relationship: ISA (hierarchy) between glossary terms."""

    type_name = "AtlasGlossaryIsARelationship"

    def classifies(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)

    def is_a(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)


# ---------------------------------------------------------------------------
# AtlasGlossaryValidValue
# ---------------------------------------------------------------------------


class AtlasGlossaryValidValue(_GlossaryTermRelationship):
    """Relationship: valid-value constraint between glossary terms."""

    type_name = "AtlasGlossaryValidValue"

    def valid_values(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)

    def valid_values_for(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)


# ---------------------------------------------------------------------------
# AtlasGlossaryPreferredTerm
# ---------------------------------------------------------------------------


class AtlasGlossaryPreferredTerm(_GlossaryTermRelationship):
    """Relationship: preferred-term link between glossary terms."""

    type_name = "AtlasGlossaryPreferredTerm"

    def preferred_terms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)

    def preferred_to_terms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)


# ---------------------------------------------------------------------------
# AtlasGlossaryReplacementTerm
# ---------------------------------------------------------------------------


class AtlasGlossaryReplacementTerm(_GlossaryTermRelationship):
    """Relationship: replacement-term link between glossary terms."""

    type_name = "AtlasGlossaryReplacementTerm"

    def replacement_terms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)

    def replaced_by(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)


# ---------------------------------------------------------------------------
# AtlasGlossaryTranslation
# ---------------------------------------------------------------------------


class AtlasGlossaryTranslation(_GlossaryTermRelationship):
    """Relationship: translation link between glossary terms."""

    type_name = "AtlasGlossaryTranslation"

    def translated_terms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)

    def translation_terms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)


# ---------------------------------------------------------------------------
# AtlasGlossaryRelatedTerm
# ---------------------------------------------------------------------------


class AtlasGlossaryRelatedTerm(_GlossaryTermRelationship):
    """Relationship: see-also link between glossary terms."""

    type_name = "AtlasGlossaryRelatedTerm"

    def see_also(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)


# ---------------------------------------------------------------------------
# AtlasGlossarySynonym
# ---------------------------------------------------------------------------


class AtlasGlossarySynonym(_GlossaryTermRelationship):
    """Relationship: synonym link between glossary terms."""

    type_name = "AtlasGlossarySynonym"

    def synonyms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return self._term_ref(related, semantic)


# ---------------------------------------------------------------------------
# AtlasGlossarySemanticAssignment
# ---------------------------------------------------------------------------


class AtlasGlossarySemanticAssignment(RelationshipAttributes):
    """Relationship: semantic assignment (term <-> asset)."""

    type_name = "AtlasGlossarySemanticAssignment"

    def __init__(
        self,
        description: Optional[str] = None,
        expression: Optional[str] = None,
        status: Optional[str] = None,
        confidence: Optional[int] = None,
        created_by: Optional[str] = None,
        steward: Optional[str] = None,
        source: Optional[str] = None,
    ):
        self.description = description
        self.expression = expression
        self.status = status
        self.confidence = confidence
        self.created_by = created_by
        self.steward = steward
        self.source = source

    def _attrs_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.description is not None:
            d["description"] = self.description
        if self.expression is not None:
            d["expression"] = self.expression
        if self.status is not None:
            d["status"] = self.status
        if self.confidence is not None:
            d["confidence"] = self.confidence
        if self.created_by is not None:
            d["createdBy"] = self.created_by
        if self.steward is not None:
            d["steward"] = self.steward
        if self.source is not None:
            d["source"] = self.source
        return d

    def assigned_entities(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        """Build a reference for the *assigned_entities* end (term → assets)."""
        return _build_generic_related(
            related, self.type_name, self._attrs_dict(), semantic
        )

    def meanings(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        """Build a reference for the *meanings* end (asset → terms)."""
        from pyatlan_v9.model.assets.gtc_related import RelatedAtlasGlossaryTerm

        return _build_related(
            RelatedAtlasGlossaryTerm,
            related,
            self.type_name,
            self._attrs_dict(),
            semantic,
        )

    def assigned_terms(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        """Build a reference for the *assigned_terms* end."""
        return _build_generic_related(
            related, self.type_name, self._attrs_dict(), semantic
        )


# ---------------------------------------------------------------------------
# UserDefRelationship
# ---------------------------------------------------------------------------


class UserDefRelationship(RelationshipAttributes):
    """Relationship: user-defined (generic) relationship between any assets."""

    type_name = "UserDefRelationship"

    def __init__(
        self,
        from_type_label: Optional[str] = None,
        to_type_label: Optional[str] = None,
    ):
        self.from_type_label = from_type_label
        self.to_type_label = to_type_label

    def _attrs_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.to_type_label is not None:
            d["toTypeLabel"] = self.to_type_label
        if self.from_type_label is not None:
            d["fromTypeLabel"] = self.from_type_label
        return d

    def user_def_relationship_to(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return _build_generic_related(
            related, self.type_name, self._attrs_dict(), semantic
        )

    def user_def_relationship_from(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return _build_generic_related(
            related, self.type_name, self._attrs_dict(), semantic
        )


# ---------------------------------------------------------------------------
# CustomRelatedFromEntitiesCustomRelatedToEntities
# ---------------------------------------------------------------------------


class CustomRelatedFromEntitiesCustomRelatedToEntities(RelationshipAttributes):
    """Relationship: custom inter-entity relationship between custom assets."""

    type_name = "custom_related_from_entities_custom_related_to_entities"

    def __init__(
        self,
        custom_entity_to_label: Optional[str] = None,
        custom_entity_from_label: Optional[str] = None,
    ):
        self.custom_entity_to_label = custom_entity_to_label
        self.custom_entity_from_label = custom_entity_from_label

    def _attrs_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.custom_entity_to_label is not None:
            d["customEntityToLabel"] = self.custom_entity_to_label
        if self.custom_entity_from_label is not None:
            d["customEntityFromLabel"] = self.custom_entity_from_label
        return d

    def custom_related_to_entities(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return _build_generic_related(
            related, self.type_name, self._attrs_dict(), semantic
        )

    def custom_related_from_entities(
        self, related: Any, semantic: SaveSemantic = SaveSemantic.REPLACE
    ) -> RelatedEntity:
        return _build_generic_related(
            related, self.type_name, self._attrs_dict(), semantic
        )
