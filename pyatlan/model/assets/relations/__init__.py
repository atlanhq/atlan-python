# Copyright 2025 Atlan Pte. Ltd.
# isort: skip_file
import lazy_loader as lazy

__PYATLAN_ASSET_RELATIONS__ = {
    "relationship_attributes": ["RelationshipAttributes"],
    "indistinct_relationship": ["IndistinctRelationship"],
    "custom_parent_entity_custom_child_entities": [
        "CustomParentEntityCustomChildEntities"
    ],
    "atlas_glossary_antonym": ["AtlasGlossaryAntonym"],
    "atlas_glossary_synonym": ["AtlasGlossarySynonym"],
    "atlas_glossary_replacement_term": ["AtlasGlossaryReplacementTerm"],
    "atlas_glossary_semantic_assignment": ["AtlasGlossarySemanticAssignment"],
    "user_def_relationship": ["UserDefRelationship"],
    "atlas_glossary_preferred_term": ["AtlasGlossaryPreferredTerm"],
    "atlas_glossary_related_term": ["AtlasGlossaryRelatedTerm"],
    "atlas_glossary_term_categorization": ["AtlasGlossaryTermCategorization"],
    "atlas_glossary_translation": ["AtlasGlossaryTranslation"],
    "atlas_glossary_valid_value": ["AtlasGlossaryValidValue"],
    "custom_related_from_entities_custom_related_to_entities": [
        "CustomRelatedFromEntitiesCustomRelatedToEntities"
    ],
    "atlas_glossary_is_a_relationship": ["AtlasGlossaryIsARelationship"],
}

lazy_loader = lazy.attach(__name__, submod_attrs=__PYATLAN_ASSET_RELATIONS__)
__getattr__, __dir__, __all__ = lazy_loader
