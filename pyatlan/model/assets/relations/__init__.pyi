# Copyright 2025 Atlan Pte. Ltd.

__all__ = [
    "RelationshipAttributes",
    "IndistinctRelationship",
    "CustomParentEntityCustomChildEntities",
    "AtlasGlossaryAntonym",
    "AtlasGlossarySynonym",
    "AtlasGlossaryReplacementTerm",
    "AtlasGlossarySemanticAssignment",
    "UserDefRelationship",
    "AtlasGlossaryPreferredTerm",
    "AtlasGlossaryRelatedTerm",
    "AtlasGlossaryTermCategorization",
    "AtlasGlossaryTranslation",
    "AtlasGlossaryValidValue",
    "CustomRelatedFromEntitiesCustomRelatedToEntities",
    "AtlasGlossaryIsARelationship",
]

from .atlas_glossary_antonym import AtlasGlossaryAntonym
from .atlas_glossary_is_a_relationship import AtlasGlossaryIsARelationship
from .atlas_glossary_preferred_term import AtlasGlossaryPreferredTerm
from .atlas_glossary_related_term import AtlasGlossaryRelatedTerm
from .atlas_glossary_replacement_term import AtlasGlossaryReplacementTerm
from .atlas_glossary_semantic_assignment import AtlasGlossarySemanticAssignment
from .atlas_glossary_synonym import AtlasGlossarySynonym
from .atlas_glossary_term_categorization import AtlasGlossaryTermCategorization
from .atlas_glossary_translation import AtlasGlossaryTranslation
from .atlas_glossary_valid_value import AtlasGlossaryValidValue
from .custom_parent_entity_custom_child_entities import (
    CustomParentEntityCustomChildEntities,
)
from .custom_related_from_entities_custom_related_to_entities import (
    CustomRelatedFromEntitiesCustomRelatedToEntities,
)
from .indistinct_relationship import IndistinctRelationship
from .relationship_attributes import RelationshipAttributes
from .user_def_relationship import UserDefRelationship
