# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""
V9 relationship attribute models (msgspec.Struct).

These classes replace the legacy Pydantic-based relationship models from
``pyatlan.model.assets.relations``.  Each class:

* holds the relationship-specific attributes (description, status, …),
* provides builder methods that return ``Related{Type}`` references with
  ``relationship_type`` and ``relationship_attributes`` populated.
"""

from pyatlan_v9.model.assets.relations.relationship_attributes import (
    AtlasGlossaryIsARelationship,
    AtlasGlossaryPreferredTerm,
    AtlasGlossaryRelatedTerm,
    AtlasGlossaryReplacementTerm,
    AtlasGlossarySemanticAssignment,
    AtlasGlossarySynonym,
    AtlasGlossaryTermCategorization,
    AtlasGlossaryTranslation,
    AtlasGlossaryValidValue,
    CustomRelatedFromEntitiesCustomRelatedToEntities,
    IndistinctRelationship,
    RelationshipAttributes,
    UserDefRelationship,
)

__all__ = [
    "RelationshipAttributes",
    "IndistinctRelationship",
    "AtlasGlossaryTermCategorization",
    "AtlasGlossaryIsARelationship",
    "AtlasGlossaryValidValue",
    "AtlasGlossaryPreferredTerm",
    "AtlasGlossaryReplacementTerm",
    "AtlasGlossaryTranslation",
    "AtlasGlossaryRelatedTerm",
    "AtlasGlossarySynonym",
    "AtlasGlossarySemanticAssignment",
    "UserDefRelationship",
    "CustomRelatedFromEntitiesCustomRelatedToEntities",
]
