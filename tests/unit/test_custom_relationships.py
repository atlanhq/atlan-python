import json
import os
from unittest.mock import patch

import pytest

from pyatlan.model.assets import (
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    CustomEntity,
    Table,
)
from pyatlan.model.assets.relations import (
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
    UserDefRelationship,
)


@pytest.fixture()
def mock_asset_guid():
    with patch("pyatlan.utils.random") as mock_random:
        mock_random.random.return_value = 123456789
        yield mock_random


def _load_test_data(filename):
    """Load test data from JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data", "custom_relationships")
    file_path = os.path.join(data_dir, filename)

    with open(file_path, "r") as f:
        return json.load(f)


def _assert_relationship(relationship, expected_type_name):
    """Helper function to assert relationship structure."""
    assert relationship
    assert relationship.guid
    assert relationship.type_name
    assert relationship.attributes
    assert relationship.attributes.relationship_attributes
    assert relationship.attributes.relationship_attributes.attributes
    assert (
        relationship.attributes.relationship_attributes.type_name == expected_type_name
    )


def test_atlas_glossary_term_categorization_deserialization():
    """Test deserialization of AtlasGlossaryTermCategorization relationship (both ends)."""
    raw_json = _load_test_data(
        "atlas_glossary_term_categorization_deserialization.json"
    )
    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.categories) == 2

    # Test categories relationship (term -> category)
    category_relation = term.categories[0]
    _assert_relationship(category_relation, "AtlasGlossaryTermCategorization")

    # Test specific attributes
    attrs = category_relation.attributes.relationship_attributes.attributes
    assert attrs.description == "Customer term is categorized under business concepts"
    assert attrs.status.value == "ACTIVE"

    # Test the nested terms relationship (category -> terms) in the second category
    second_category = term.categories[1]
    assert hasattr(second_category.attributes, "terms")
    assert len(second_category.attributes.terms) == 2

    nested_term_relation = second_category.attributes.terms[0]
    _assert_relationship(nested_term_relation, "AtlasGlossaryTermCategorization")

    nested_attrs = nested_term_relation.attributes.relationship_attributes.attributes
    assert nested_attrs.description == "Terms organized within this category"
    assert nested_attrs.status.value == "ACTIVE"


def test_atlas_glossary_term_categorization_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossaryTermCategorization relationship."""
    expected_json = _load_test_data(
        "atlas_glossary_term_categorization_serialization.json"
    )

    category = AtlasGlossaryCategory.updater(
        qualified_name="business-category@business-glossary",
        name="business-category",
        glossary_guid="business-glossary-guid",
    )

    term = AtlasGlossaryTerm.ref_by_guid("term-guid-1")

    categorization = AtlasGlossaryTermCategorization(
        description="Customer related terms", status="ACTIVE"
    )

    category.terms = [categorization.terms(term)]

    assert category.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_is_a_relationship_deserialization():
    """Test deserialization of AtlasGlossaryIsARelationship relationship."""
    raw_json = _load_test_data("atlas_glossary_is_a_relationship_deserialization.json")
    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.classifies) == 1
    assert len(term.is_a) == 1

    classifies_relation = term.classifies[0]
    is_a_relation = term.is_a[0]

    _assert_relationship(classifies_relation, "AtlasGlossaryIsARelationship")
    _assert_relationship(is_a_relation, "AtlasGlossaryIsARelationship")

    # Test specific attributes
    attrs = classifies_relation.attributes.relationship_attributes.attributes
    assert attrs.description == "Animal is a more general concept"
    assert attrs.expression == "taxonomic classification"
    assert attrs.status.value == "ACTIVE"
    assert attrs.steward == "taxonomy-expert"
    assert attrs.source == "domain-expert"


def test_atlas_glossary_is_a_relationship_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossaryIsARelationship relationship."""
    expected_json = _load_test_data(
        "atlas_glossary_is_a_relationship_serialization.json"
    )

    term = AtlasGlossaryTerm.updater(
        qualified_name="mammal@taxonomy-glossary",
        name="mammal",
        glossary_guid="taxonomy-glossary-guid",
    )

    general_term = AtlasGlossaryTerm.ref_by_guid("general-term-guid")

    is_a_relationship = AtlasGlossaryIsARelationship(
        description="Animal is a more general concept",
        expression="taxonomic classification",
        status="ACTIVE",
        steward="taxonomy-expert",
        source="domain-expert",
    )

    term.classifies = [is_a_relationship.classifies(general_term)]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_valid_value_deserialization():
    """Test deserialization of AtlasGlossaryValidValue relationship (both ends)."""
    raw_json = _load_test_data("atlas_glossary_valid_value_deserialization.json")
    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.valid_values) == 2
    assert len(term.valid_values_for) == 1

    # Test valid_values relationship (term -> valid values)
    valid_value_relation = term.valid_values[0]
    _assert_relationship(valid_value_relation, "AtlasGlossaryValidValue")

    # Test specific attributes
    attrs = valid_value_relation.attributes.relationship_attributes.attributes
    assert attrs.description == "Red is a valid color value"
    assert attrs.expression == "enumeration value"
    assert attrs.status.value == "ACTIVE"
    assert attrs.steward == "data-modeler"
    assert attrs.source == "business-rules"

    # Test valid_values_for relationship (term -> parent terms)
    valid_values_for_relation = term.valid_values_for[0]
    _assert_relationship(valid_values_for_relation, "AtlasGlossaryValidValue")

    # Test specific attributes for the reverse relationship
    reverse_attrs = (
        valid_values_for_relation.attributes.relationship_attributes.attributes
    )
    assert reverse_attrs.description == "Color is a valid value for parent concept"
    assert reverse_attrs.expression == "enumeration constraint"
    assert reverse_attrs.status.value == "ACTIVE"
    assert reverse_attrs.steward == "data-modeler"
    assert reverse_attrs.source == "domain-rules"


def test_atlas_glossary_valid_value_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossaryValidValue relationship."""
    expected_json = _load_test_data("atlas_glossary_valid_value_serialization.json")

    term = AtlasGlossaryTerm.updater(
        qualified_name="color@business-glossary",
        name="color",
        glossary_guid="business-glossary-guid",
    )

    red_value = AtlasGlossaryTerm.ref_by_guid("red-value-guid")

    valid_value_relationship = AtlasGlossaryValidValue(
        description="Red color value",
        expression="manual assignment",
        status="ACTIVE",
        steward="data-modeler",
        source="business-analysis",
    )

    term.valid_values = [valid_value_relationship.valid_values(red_value)]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_preferred_term_deserialization():
    """Test deserialization of AtlasGlossaryPreferredTerm relationship."""
    raw_json = _load_test_data("atlas_glossary_preferred_term_deserialization.json")
    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.preferred_terms) == 1
    assert len(term.preferred_to_terms) == 1

    preferred_relation = term.preferred_terms[0]
    preferred_to_relation = term.preferred_to_terms[0]

    _assert_relationship(preferred_relation, "AtlasGlossaryPreferredTerm")
    _assert_relationship(preferred_to_relation, "AtlasGlossaryPreferredTerm")

    # Test specific attributes
    attrs = preferred_relation.attributes.relationship_attributes.attributes
    assert attrs.description == "Customer is the preferred term over client"
    assert attrs.expression == "business standardization"
    assert attrs.status.value == "ACTIVE"
    assert attrs.steward == "business-analyst"
    assert attrs.source == "governance-committee"


def test_atlas_glossary_preferred_term_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossaryPreferredTerm relationship."""
    expected_json = _load_test_data("atlas_glossary_preferred_term_serialization.json")

    term = AtlasGlossaryTerm.updater(
        qualified_name="business-entity@business-glossary",
        name="business-entity",
        glossary_guid="business-glossary-guid",
    )

    preferred_term = AtlasGlossaryTerm.ref_by_guid("customer-preferred-guid")

    preferred_relationship = AtlasGlossaryPreferredTerm(
        description="Customer is the preferred term",
        expression="governance decision",
        status="ACTIVE",
        steward="business-analyst",
        source="manual",
    )

    term.preferred_terms = [preferred_relationship.preferred_terms(preferred_term)]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_replacement_term_deserialization():
    """Test deserialization of AtlasGlossaryReplacementTerm relationship."""
    raw_json = _load_test_data("atlas_glossary_replacement_term_deserialization.json")
    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.replacement_terms) == 1
    assert len(term.replaced_by) == 1

    replacement_relation = term.replacement_terms[0]
    replaced_by_relation = term.replaced_by[0]

    _assert_relationship(replacement_relation, "AtlasGlossaryReplacementTerm")
    _assert_relationship(replaced_by_relation, "AtlasGlossaryReplacementTerm")

    # Test specific attributes
    attrs = replacement_relation.attributes.relationship_attributes.attributes
    assert attrs.description == "Customer record replaces the deprecated client record"
    assert attrs.expression == "system migration"
    assert attrs.status.value == "ACTIVE"
    assert attrs.steward == "data-architect"
    assert attrs.source == "system-modernization"


def test_atlas_glossary_replacement_term_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossaryReplacementTerm relationship."""
    expected_json = _load_test_data(
        "atlas_glossary_replacement_term_serialization.json"
    )

    term = AtlasGlossaryTerm.updater(
        qualified_name="legacy-term@old-glossary",
        name="legacy-term",
        glossary_guid="old-glossary-guid",
    )

    replacement_term = AtlasGlossaryTerm.ref_by_guid("new-term-guid")

    replacement_relationship = AtlasGlossaryReplacementTerm(
        description="New term replaces legacy term",
        expression="system upgrade",
        status="ACTIVE",
        steward="data-architect",
        source="manual",
    )

    term.replacement_terms = [
        replacement_relationship.replacement_terms(replacement_term)
    ]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_translation_deserialization():
    """Test deserialization of AtlasGlossaryTranslation relationship."""
    raw_json = _load_test_data("atlas_glossary_translation_deserialization.json")
    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.translated_terms) == 2
    assert len(term.translation_terms) == 1

    translated_relation = term.translated_terms[0]
    translation_relation = term.translation_terms[0]

    _assert_relationship(translated_relation, "AtlasGlossaryTranslation")
    _assert_relationship(translation_relation, "AtlasGlossaryTranslation")

    # Test specific attributes
    attrs = translated_relation.attributes.relationship_attributes.attributes
    assert attrs.description == "Spanish translation of customer"
    assert attrs.expression == "language localization"
    assert attrs.status.value == "ACTIVE"
    assert attrs.steward == "translation-team"
    assert attrs.source == "professional-translation"


def test_atlas_glossary_translation_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossaryTranslation relationship."""
    expected_json = _load_test_data("atlas_glossary_translation_serialization.json")

    term = AtlasGlossaryTerm.updater(
        qualified_name="customer@english-glossary",
        name="customer",
        glossary_guid="english-glossary-guid",
    )

    spanish_term = AtlasGlossaryTerm.ref_by_guid("cliente-spanish-guid")

    translation_relationship = AtlasGlossaryTranslation(
        description="Spanish translation",
        expression="localization",
        status="ACTIVE",
        steward="translation-team",
        source="manual",
    )

    term.translated_terms = [translation_relationship.translated_terms(spanish_term)]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_user_def_relationship_deserialization():
    """Test deserialization of UserDefRelationship relationship."""
    raw_json = _load_test_data("user_def_relationship_deserialization.json")
    term = AtlasGlossaryTerm(**raw_json)
    assert term.name and term.guid and term.qualified_name
    to_relation1 = term.user_def_relationship_to[0]
    from_relation1 = term.user_def_relationship_from[0]
    from_relation2 = term.user_def_relationship_from[1]
    _assert_relationship(to_relation1, "UserDefRelationship")
    _assert_relationship(from_relation1, "UserDefRelationship")
    _assert_relationship(from_relation2, "UserDefRelationship")


def test_user_def_relationship_serialization(mock_asset_guid):
    """Test serialization of UserDefRelationship relationship."""
    expected_json = _load_test_data("user_def_relationship_serialization.json")

    term1 = AtlasGlossaryTerm.updater(
        qualified_name="test-term-qn",
        name="test-term",
        glossary_guid="test-glossary-guid",
    )

    term0 = AtlasGlossaryTerm.ref_by_guid("test-term0-guid")
    term2 = AtlasGlossaryTerm.ref_by_guid("test-term2-guid")
    term3 = AtlasGlossaryTerm.ref_by_guid("test-term3-guid")

    udr_from0 = UserDefRelationship(
        from_type_label="test0-from-label", to_type_label="test0-to-label"
    )
    udr_to1 = UserDefRelationship(
        from_type_label="test1-from-label", to_type_label="test1-to-label"
    )
    udr_to2 = UserDefRelationship(
        from_type_label="test2-from-label", to_type_label="test2-to-label"
    )

    term1.user_def_relationship_from = [udr_from0.user_def_relationship_from(term0)]
    term1.user_def_relationship_to = [
        udr_to1.user_def_relationship_to(term2),
        udr_to2.user_def_relationship_to(term3),
    ]

    assert term1.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_semantic_assignment_deserialization():
    """Test deserialization of AtlasGlossarySemanticAssignment relationship (both ends)."""
    raw_json = _load_test_data(
        "atlas_glossary_semantic_assignment_deserialization.json"
    )
    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.assigned_entities) == 2

    # Test assigned_entities relationship (term -> entities)
    table_assignment = term.assigned_entities[0]
    _assert_relationship(table_assignment, "AtlasGlossarySemanticAssignment")

    # Test specific attributes
    attrs = table_assignment.attributes.relationship_attributes.attributes
    assert (
        attrs.description == "Customer table semantically represents customer concept"
    )
    assert attrs.expression == "business metadata mapping"
    assert attrs.status.value == "ACTIVE"
    assert attrs.confidence == 95
    assert attrs.created_by == "data-analyst"
    assert attrs.steward == "data-governance-team"
    assert attrs.source == "automated-discovery"

    # Test second assignment (Column)
    column_assignment = term.assigned_entities[1]
    _assert_relationship(column_assignment, "AtlasGlossarySemanticAssignment")

    column_attrs = column_assignment.attributes.relationship_attributes.attributes
    assert (
        column_attrs.description == "Customer ID column represents customer identifier"
    )
    assert column_attrs.confidence == 98
    assert column_attrs.source == "manual-assignment"

    # Note: The reverse relationship (meanings) would be tested from the asset side (Table/Column)
    # since AtlasGlossarySemanticAssignment.meanings() is used from asset -> term direction
    # ie: test_atlas_glossary_semantic_assignment_meanings_perspective_*


def test_atlas_glossary_semantic_assignment_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossarySemanticAssignment relationship."""
    expected_json = _load_test_data(
        "atlas_glossary_semantic_assignment_serialization.json"
    )

    term = AtlasGlossaryTerm.updater(
        qualified_name="customer@business-glossary",
        name="Customer",
        glossary_guid="business-glossary-guid",
    )

    table = Table.ref_by_guid("customer-table-guid")

    semantic_assignment = AtlasGlossarySemanticAssignment(
        description="Customer term semantically represents customer data",
        expression="business metadata mapping",
        status="ACTIVE",
        confidence=95,
        created_by="data-analyst",
        steward="data-governance-team",
        source="automated-discovery",
    )

    term.assigned_entities = [semantic_assignment.assigned_entities(table)]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_semantic_assignment_meanings_perspective_deserialization():
    """Test deserialization of AtlasGlossarySemanticAssignment from meanings perspective."""
    raw_json = _load_test_data(
        "atlas_glossary_semantic_assignment_meanings_perspective_deserialization.json"
    )

    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.assigned_terms) == 1

    # Test assigned_entities relationship (term -> assets)
    assigned_term = term.assigned_terms[0]
    _assert_relationship(assigned_term, "AtlasGlossarySemanticAssignment")

    # Test specific attributes
    attrs = assigned_term.attributes.relationship_attributes.attributes
    assert attrs.description == "Customer data is assigned this business term"
    assert attrs.expression == "manual assignment"
    assert attrs.status.value == "ACTIVE"
    assert attrs.confidence == 95
    assert attrs.created_by == "data-analyst"
    assert attrs.steward == "business-analyst"
    assert attrs.source == "business-glossary"

    # Test that the assigned entity has the expected structure
    assert assigned_term.type_name == "Table"
    assert assigned_term.guid == "customer-table-guid"


def test_atlas_glossary_related_term_deserialization():
    """Test deserialization of AtlasGlossaryRelatedTerm relationship."""
    raw_json = _load_test_data("atlas_glossary_related_term_deserialization.json")

    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.see_also) == 1

    # Test see_also relationship
    related_term = term.see_also[0]
    _assert_relationship(related_term, "AtlasGlossaryRelatedTerm")

    # Test specific attributes
    attrs = related_term.attributes.relationship_attributes.attributes

    assert attrs.description == "Related term for reference"
    assert attrs.expression == "see-also-expression"
    assert attrs.status.value == "ACTIVE"
    assert attrs.steward == "data-steward"
    assert attrs.source == "manual"


def test_atlas_glossary_related_term_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossaryRelatedTerm relationship."""
    expected_json = _load_test_data("atlas_glossary_related_term_serialization.json")

    term = AtlasGlossaryTerm.updater(
        qualified_name="main-term@default",
        name="Main Term",
        glossary_guid="business-glossary-guid",
    )

    related_term = AtlasGlossaryTerm.ref_by_guid("related-term-guid")

    related_term_rel = AtlasGlossaryRelatedTerm(
        description="Related term for reference",
        expression="see-also-expression",
        status="ACTIVE",
        steward="data-steward",
        source="manual",
    )

    term.see_also = [related_term_rel.see_also(related_term)]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_atlas_glossary_synonym_deserialization():
    """Test deserialization of AtlasGlossarySynonym relationship."""
    raw_json = _load_test_data("atlas_glossary_synonym_deserialization.json")

    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.synonyms) == 1

    # Test synonyms relationship
    synonym_term = term.synonyms[0]
    _assert_relationship(synonym_term, "AtlasGlossarySynonym")

    # Test specific attributes
    attrs = synonym_term.attributes.relationship_attributes.attributes
    assert attrs.description == "Synonym relationship"
    assert attrs.expression == "synonym-expression"
    assert attrs.status.value == "ACTIVE"
    assert attrs.steward == "data-steward"
    assert attrs.source == "manual"


def test_atlas_glossary_synonym_serialization(mock_asset_guid):
    """Test serialization of AtlasGlossarySynonym relationship."""
    expected_json = _load_test_data("atlas_glossary_synonym_serialization.json")

    term = AtlasGlossaryTerm.updater(
        qualified_name="main-term@default",
        name="Main Term",
        glossary_guid="business-glossary-guid",
    )

    synonym_term = AtlasGlossaryTerm.ref_by_guid("synonym-term-guid")

    synonym_rel = AtlasGlossarySynonym(
        description="Synonym relationship",
        expression="synonym-expression",
        status="ACTIVE",
        steward="data-steward",
        source="manual",
    )

    term.synonyms = [synonym_rel.synonyms(synonym_term)]

    assert term.dict(by_alias=True, exclude_unset=True) == expected_json


def test_custom_related_from_entities_custom_related_to_entities_deserialization():
    """Test deserialization of CustomRelatedFromEntitiesCustomRelatedToEntities relationship."""
    raw_json = _load_test_data(
        "custom_related_from_entities_custom_related_to_entities_deserialization.json"
    )

    entity = CustomEntity(**raw_json)

    assert entity.name and entity.guid and entity.qualified_name
    assert len(entity.custom_related_to_entities) == 1
    assert len(entity.custom_related_from_entities) == 1

    # Test custom_related_to_entities relationship
    to_entity = entity.custom_related_to_entities[0]
    _assert_relationship(
        to_entity, "custom_related_from_entities_custom_related_to_entities"
    )

    # Test specific attributes
    to_attrs = to_entity.attributes.relationship_attributes.attributes
    assert to_attrs.custom_entity_to_label == "relates to"
    assert to_attrs.custom_entity_from_label == "relates from"

    # Test custom_related_from_entities relationship
    from_entity = entity.custom_related_from_entities[0]
    _assert_relationship(
        from_entity, "custom_related_from_entities_custom_related_to_entities"
    )

    # Test specific attributes
    from_attrs = from_entity.attributes.relationship_attributes.attributes
    assert from_attrs.custom_entity_to_label == "relates to"
    assert from_attrs.custom_entity_from_label == "relates from"


def test_custom_related_from_entities_custom_related_to_entities_serialization(
    mock_asset_guid,
):
    """Test serialization of CustomRelatedFromEntitiesCustomRelatedToEntities relationship."""
    expected_json = _load_test_data(
        "custom_related_from_entities_custom_related_to_entities_serialization.json"
    )

    entity = CustomEntity.updater(
        qualified_name="main-entity@default", name="Main Entity"
    )

    target_entity = CustomEntity.ref_by_guid("target-entity-guid")
    source_entity = CustomEntity.ref_by_guid("source-entity-guid")

    custom_rel = CustomRelatedFromEntitiesCustomRelatedToEntities(
        custom_entity_to_label="relates to", custom_entity_from_label="relates from"
    )

    entity.custom_related_to_entities = [
        custom_rel.custom_related_to_entities(target_entity)
    ]
    entity.custom_related_from_entities = [
        custom_rel.custom_related_from_entities(source_entity)
    ]

    assert entity.dict(by_alias=True, exclude_unset=True) == expected_json


def test_combined_multiple_relationships_on_single_asset(mock_asset_guid):
    """Test combining multiple different relationship types on a single glossary term."""
    # Create a glossary term with multiple relationship types
    term = AtlasGlossaryTerm.updater(
        qualified_name="customer@business-glossary",
        name="Customer",
        glossary_guid="business-glossary-guid",
    )

    # 1. Add categorization relationship
    category = AtlasGlossaryCategory.ref_by_guid("business-category-guid")
    categorization = AtlasGlossaryTermCategorization(
        description="Customer is categorized under business concepts", status="ACTIVE"
    )
    term.categories = [categorization.categories(category)]

    # 2. Add is-a relationship (hierarchical)
    parent_term = AtlasGlossaryTerm.ref_by_guid("person-term-guid")
    is_a_rel = AtlasGlossaryIsARelationship(
        description="Customer is a type of Person",
        expression="business hierarchy",
        status="ACTIVE",
        steward="business-analyst",
        source="domain-expert",
    )
    term.classifies = [is_a_rel.classifies(parent_term)]

    # 3. Add valid values relationship
    status_value = AtlasGlossaryTerm.ref_by_guid("active-status-guid")
    valid_value_rel = AtlasGlossaryValidValue(
        description="Active is a valid status for Customer",
        expression="enumeration value",
        status="ACTIVE",
        steward="data-modeler",
        source="business-rules",
    )
    term.valid_values = [valid_value_rel.valid_values(status_value)]

    # 4. Add preferred term relationship
    preferred_term = AtlasGlossaryTerm.ref_by_guid("client-term-guid")
    preferred_rel = AtlasGlossaryPreferredTerm(
        description="Customer is preferred over Client",
        expression="business preference",
        status="ACTIVE",
        steward="business-analyst",
        source="style-guide",
    )
    term.preferred_to_terms = [preferred_rel.preferred_to_terms(preferred_term)]

    # 5. Add synonym relationship
    synonym_term = AtlasGlossaryTerm.ref_by_guid("buyer-term-guid")
    synonym_rel = AtlasGlossarySynonym(
        description="Customer and Buyer are synonymous",
        expression="business synonym",
        status="ACTIVE",
        steward="business-analyst",
        source="domain-expert",
    )
    term.synonyms = [synonym_rel.synonyms(synonym_term)]

    # 6. Add user-defined relationship
    related_term = AtlasGlossaryTerm.ref_by_guid("account-term-guid")
    user_def_rel = UserDefRelationship(
        from_type_label="has account", to_type_label="belongs to customer"
    )
    term.user_def_relationship_to = [
        user_def_rel.user_def_relationship_to(related_term)
    ]

    # Serialize and verify structure
    result = term.dict(by_alias=True, exclude_unset=True)

    # Verify the term has all expected relationship types
    attributes = result["attributes"]
    assert "categories" in attributes
    assert "classifies" in attributes
    assert "validValues" in attributes
    assert "preferredToTerms" in attributes
    assert "synonyms" in attributes
    assert "userDefRelationshipTo" in attributes

    # Verify each relationship has the correct structure
    assert len(attributes["categories"]) == 1
    assert len(attributes["classifies"]) == 1
    assert len(attributes["validValues"]) == 1
    assert len(attributes["preferredToTerms"]) == 1
    assert len(attributes["synonyms"]) == 1
    assert len(attributes["userDefRelationshipTo"]) == 1

    # Verify relationship types
    assert (
        attributes["categories"][0]["relationshipType"]
        == "AtlasGlossaryTermCategorization"
    )
    assert (
        attributes["classifies"][0]["relationshipType"]
        == "AtlasGlossaryIsARelationship"
    )
    assert attributes["validValues"][0]["relationshipType"] == "AtlasGlossaryValidValue"
    assert (
        attributes["preferredToTerms"][0]["relationshipType"]
        == "AtlasGlossaryPreferredTerm"
    )
    assert attributes["synonyms"][0]["relationshipType"] == "AtlasGlossarySynonym"
    assert (
        attributes["userDefRelationshipTo"][0]["relationshipType"]
        == "UserDefRelationship"
    )

    # Verify relationship attributes are present
    for rel_list in [
        attributes["categories"],
        attributes["classifies"],
        attributes["validValues"],
        attributes["preferredToTerms"],
        attributes["synonyms"],
        attributes["userDefRelationshipTo"],
    ]:
        for rel in rel_list:
            assert "relationshipAttributes" in rel
            assert "typeName" in rel["relationshipAttributes"]
            assert "attributes" in rel["relationshipAttributes"]

    # Verify specific relationship attribute values
    assert (
        attributes["categories"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Customer is categorized under business concepts"
    )
    assert (
        attributes["classifies"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Customer is a type of Person"
    )
    assert (
        attributes["validValues"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Active is a valid status for Customer"
    )
    assert (
        attributes["preferredToTerms"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Customer is preferred over Client"
    )
    assert (
        attributes["synonyms"][0]["relationshipAttributes"]["attributes"]["description"]
        == "Customer and Buyer are synonymous"
    )
    assert (
        attributes["userDefRelationshipTo"][0]["relationshipAttributes"]["attributes"][
            "fromTypeLabel"
        ]
        == "has account"
    )


def test_indistinct_relationship_deserialization(mock_asset_guid):
    """Test deserialization of IndistinctRelationship relationship."""
    raw_json = _load_test_data("indistinct_relationship_deserialization.json")

    term = AtlasGlossaryTerm(**raw_json)

    assert term.name and term.guid and term.qualified_name
    assert len(term.valid_values) == 2
    assert len(term.valid_values_for) == 1

    # Test valid_values relationship (term -> valid values)
    valid_value_relation = term.valid_values[0]
    _assert_relationship(valid_value_relation, "UnknownRelationship1")
    assert isinstance(
        valid_value_relation.attributes.relationship_attributes, IndistinctRelationship
    )

    # Test specific attributes
    attrs = valid_value_relation.attributes.relationship_attributes.attributes
    assert attrs["description"] == "test description 11"
    assert attrs["expression"] == "test expression 11"
    assert attrs["status"] == "ACTIVE"

    # Test valid_values_for relationship (term -> parent terms)
    valid_values_for_relation = term.valid_values_for[0]
    _assert_relationship(valid_values_for_relation, "UnknownRelationship2")
    assert isinstance(
        valid_values_for_relation.attributes.relationship_attributes,
        IndistinctRelationship,
    )

    # Test specific attributes for the reverse relationship
    reverse_attrs = (
        valid_values_for_relation.attributes.relationship_attributes.attributes
    )
    assert reverse_attrs["description"] == "test description 21"
    assert reverse_attrs["alias"] == "test alias 21"
    assert reverse_attrs["status"] == "ACTIVE"


def test_relationship_attrs_no_typename_fallback_dict_deserialization(mock_asset_guid):
    """Test deserialization of Relationship attributes when typeName is absent."""
    raw_json = _load_test_data("relationship_attributes_dict_when_no_typename.json")

    term = AtlasGlossaryTerm(**raw_json)

    # Fallback to dict when typeName is absent (cannot determine specific Relationship model type)
    assert term.relationship_attributes
    assert isinstance(term.relationship_attributes, dict)
    assert term.relationship_attributes["attributes"]["description"]

    assert term.attributes.relationship_attributes
    assert isinstance(term.attributes.relationship_attributes, dict)
    assert term.relationship_attributes["attributes"]["description"]

    assert term.name and term.guid and term.qualified_name
    assert len(term.valid_values) == 2
    assert len(term.valid_values_for) == 1

    valid_value_relation = term.valid_values[0]
    assert valid_value_relation.attributes
    assert valid_value_relation.attributes.relationship_attributes
    assert valid_value_relation.attributes.relationship_attributes["attributes"][
        "description"
    ]

    valid_value_for_relation = term.valid_values_for[0]
    assert valid_value_for_relation.attributes
    assert valid_value_for_relation.attributes.relationship_attributes
    assert valid_value_for_relation.attributes.relationship_attributes["attributes"][
        "description"
    ]
