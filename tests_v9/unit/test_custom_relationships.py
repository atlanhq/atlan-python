"""Tests for v9 custom relationship models.

These tests verify:
- Relationship attribute builder methods produce correct RelatedEntity refs
- Serialization of models with relationship attributes (to_json)
- Round-trip serialization → deserialization preserves relationship data
- Combined multiple relationship types on a single asset
- IndistinctRelationship fallback for unknown relationship types
"""

import json
from unittest.mock import patch

import pytest
from msgspec import UNSET

from pyatlan_v9.model.assets import (
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    CustomEntity,
    Table,
)
from pyatlan_v9.model.assets.gtc_related import RelatedAtlasGlossaryTerm
from pyatlan_v9.model.assets.related_entity import RelatedEntity
from pyatlan_v9.model.assets.relations import (
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
    with patch("pyatlan_v9.utils.random") as mock_random:
        mock_random.random.return_value = 123456789
        yield mock_random


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _assert_related_entity(related, expected_relationship_type):
    """Helper to assert a RelatedEntity has the expected relationship structure."""
    assert isinstance(related, RelatedEntity)
    assert related.relationship_type == expected_relationship_type
    assert related.relationship_attributes is not UNSET
    assert related.relationship_attributes is not None
    assert related.relationship_attributes["typeName"] == expected_relationship_type
    assert "attributes" in related.relationship_attributes


def _get_serialized_rel_attrs(term_json, rel_field_name, index=0):
    """Extract serialized relationship attributes from nested JSON output.

    In v9 nested format, relationship fields are under 'relationshipAttributes'.
    """
    rel_attrs = term_json.get("relationshipAttributes", {})
    items = rel_attrs.get(rel_field_name, [])
    if isinstance(items, list):
        return items[index] if index < len(items) else None
    return items


# ---------------------------------------------------------------------------
# AtlasGlossaryTermCategorization
# ---------------------------------------------------------------------------


def test_atlas_glossary_term_categorization_builder():
    """Test AtlasGlossaryTermCategorization builder methods."""
    categorization = AtlasGlossaryTermCategorization(
        description="Customer related terms", status="ACTIVE"
    )
    term = AtlasGlossaryTerm.ref_by_guid("term-guid-1")
    category = AtlasGlossaryCategory.ref_by_guid("category-guid-1")

    # Test terms() builder
    terms_ref = categorization.terms(term)
    _assert_related_entity(terms_ref, "AtlasGlossaryTermCategorization")
    assert terms_ref.guid == "term-guid-1"
    attrs = terms_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "Customer related terms"
    assert attrs["status"] == "ACTIVE"

    # Test categories() builder
    categories_ref = categorization.categories(category)
    _assert_related_entity(categories_ref, "AtlasGlossaryTermCategorization")
    assert categories_ref.guid == "category-guid-1"


def test_atlas_glossary_term_categorization_serialization():
    """Test serialization of AtlasGlossaryTermCategorization relationship."""
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

    result = json.loads(category.to_json())

    # Verify the terms relationship is in relationshipAttributes
    terms_item = _get_serialized_rel_attrs(result, "terms", 0)
    assert terms_item is not None
    assert terms_item["guid"] == "term-guid-1"
    assert terms_item["relationshipType"] == "AtlasGlossaryTermCategorization"
    assert (
        terms_item["relationshipAttributes"]["typeName"]
        == "AtlasGlossaryTermCategorization"
    )
    assert (
        terms_item["relationshipAttributes"]["attributes"]["description"]
        == "Customer related terms"
    )
    assert terms_item["relationshipAttributes"]["attributes"]["status"] == "ACTIVE"


def test_atlas_glossary_term_categorization_roundtrip():
    """Test round-trip serialization/deserialization of categorization relationship."""
    category = AtlasGlossaryCategory.updater(
        qualified_name="business-category@business-glossary",
        name="business-category",
        glossary_guid="business-glossary-guid",
    )

    categorization = AtlasGlossaryTermCategorization(
        description="Customer related terms", status="ACTIVE"
    )
    term_ref = AtlasGlossaryTerm.ref_by_guid("term-guid-1")
    category.terms = [categorization.terms(term_ref)]

    # Serialize → deserialize
    json_str = category.to_json()
    restored = AtlasGlossaryCategory.from_json(json_str)

    assert restored.name == "business-category"
    assert restored.qualified_name == "business-category@business-glossary"
    assert restored.terms is not UNSET and restored.terms is not None
    assert len(restored.terms) == 1

    restored_term = restored.terms[0]
    assert restored_term.guid == "term-guid-1"
    assert restored_term.relationship_type == "AtlasGlossaryTermCategorization"
    assert (
        restored_term.relationship_attributes["typeName"]
        == "AtlasGlossaryTermCategorization"
    )
    assert (
        restored_term.relationship_attributes["attributes"]["description"]
        == "Customer related terms"
    )


# ---------------------------------------------------------------------------
# AtlasGlossaryIsARelationship
# ---------------------------------------------------------------------------


def test_atlas_glossary_is_a_relationship_builder():
    """Test AtlasGlossaryIsARelationship builder methods."""
    is_a_rel = AtlasGlossaryIsARelationship(
        description="Animal is a more general concept",
        expression="taxonomic classification",
        status="ACTIVE",
        steward="taxonomy-expert",
        source="domain-expert",
    )

    general_term = AtlasGlossaryTerm.ref_by_guid("general-term-guid")

    classifies_ref = is_a_rel.classifies(general_term)
    _assert_related_entity(classifies_ref, "AtlasGlossaryIsARelationship")
    assert classifies_ref.guid == "general-term-guid"
    attrs = classifies_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "Animal is a more general concept"
    assert attrs["expression"] == "taxonomic classification"
    assert attrs["status"] == "ACTIVE"
    assert attrs["steward"] == "taxonomy-expert"
    assert attrs["source"] == "domain-expert"

    is_a_ref = is_a_rel.is_a(general_term)
    _assert_related_entity(is_a_ref, "AtlasGlossaryIsARelationship")


def test_atlas_glossary_is_a_relationship_serialization():
    """Test serialization of AtlasGlossaryIsARelationship relationship."""
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

    result = json.loads(term.to_json())

    classifies_item = _get_serialized_rel_attrs(result, "classifies", 0)
    assert classifies_item is not None
    assert classifies_item["guid"] == "general-term-guid"
    assert classifies_item["relationshipType"] == "AtlasGlossaryIsARelationship"
    rel_attrs = classifies_item["relationshipAttributes"]
    assert rel_attrs["typeName"] == "AtlasGlossaryIsARelationship"
    assert rel_attrs["attributes"]["description"] == "Animal is a more general concept"
    assert rel_attrs["attributes"]["expression"] == "taxonomic classification"
    assert rel_attrs["attributes"]["status"] == "ACTIVE"
    assert rel_attrs["attributes"]["steward"] == "taxonomy-expert"
    assert rel_attrs["attributes"]["source"] == "domain-expert"


def test_atlas_glossary_is_a_relationship_roundtrip():
    """Test round-trip for AtlasGlossaryIsARelationship."""
    term = AtlasGlossaryTerm.updater(
        qualified_name="mammal@taxonomy-glossary",
        name="mammal",
        glossary_guid="taxonomy-glossary-guid",
    )

    is_a_rel = AtlasGlossaryIsARelationship(
        description="Animal is a more general concept",
        expression="taxonomic classification",
        status="ACTIVE",
        steward="taxonomy-expert",
        source="domain-expert",
    )

    general_term = AtlasGlossaryTerm.ref_by_guid("general-term-guid")
    term.classifies = [is_a_rel.classifies(general_term)]

    restored = AtlasGlossaryTerm.from_json(term.to_json())

    assert restored.classifies is not UNSET and restored.classifies is not None
    assert len(restored.classifies) == 1
    c = restored.classifies[0]
    assert c.guid == "general-term-guid"
    assert c.relationship_attributes["typeName"] == "AtlasGlossaryIsARelationship"
    assert (
        c.relationship_attributes["attributes"]["description"]
        == "Animal is a more general concept"
    )


# ---------------------------------------------------------------------------
# AtlasGlossaryValidValue
# ---------------------------------------------------------------------------


def test_atlas_glossary_valid_value_builder():
    """Test AtlasGlossaryValidValue builder methods."""
    vv_rel = AtlasGlossaryValidValue(
        description="Red is a valid color value",
        expression="enumeration value",
        status="ACTIVE",
        steward="data-modeler",
        source="business-rules",
    )

    red_value = AtlasGlossaryTerm.ref_by_guid("red-value-guid")

    vv_ref = vv_rel.valid_values(red_value)
    _assert_related_entity(vv_ref, "AtlasGlossaryValidValue")
    assert vv_ref.guid == "red-value-guid"
    attrs = vv_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "Red is a valid color value"
    assert attrs["expression"] == "enumeration value"
    assert attrs["status"] == "ACTIVE"
    assert attrs["steward"] == "data-modeler"
    assert attrs["source"] == "business-rules"

    vvf_ref = vv_rel.valid_values_for(red_value)
    _assert_related_entity(vvf_ref, "AtlasGlossaryValidValue")


def test_atlas_glossary_valid_value_serialization():
    """Test serialization of AtlasGlossaryValidValue relationship."""
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

    result = json.loads(term.to_json())

    vv_item = _get_serialized_rel_attrs(result, "validValues", 0)
    assert vv_item is not None
    assert vv_item["guid"] == "red-value-guid"
    assert vv_item["relationshipType"] == "AtlasGlossaryValidValue"
    assert vv_item["relationshipAttributes"]["typeName"] == "AtlasGlossaryValidValue"
    assert (
        vv_item["relationshipAttributes"]["attributes"]["description"]
        == "Red color value"
    )


def test_atlas_glossary_valid_value_roundtrip():
    """Test round-trip for AtlasGlossaryValidValue."""
    term = AtlasGlossaryTerm.updater(
        qualified_name="color@business-glossary",
        name="color",
        glossary_guid="business-glossary-guid",
    )

    vv_rel = AtlasGlossaryValidValue(
        description="Red color value",
        expression="manual assignment",
        status="ACTIVE",
        steward="data-modeler",
        source="business-analysis",
    )
    term.valid_values = [vv_rel.valid_values(AtlasGlossaryTerm.ref_by_guid("red-guid"))]

    restored = AtlasGlossaryTerm.from_json(term.to_json())
    assert restored.valid_values is not UNSET
    assert len(restored.valid_values) == 1
    vv = restored.valid_values[0]
    assert vv.guid == "red-guid"
    assert vv.relationship_attributes["typeName"] == "AtlasGlossaryValidValue"


# ---------------------------------------------------------------------------
# AtlasGlossaryPreferredTerm
# ---------------------------------------------------------------------------


def test_atlas_glossary_preferred_term_builder():
    """Test AtlasGlossaryPreferredTerm builder methods."""
    pref_rel = AtlasGlossaryPreferredTerm(
        description="Customer is the preferred term over client",
        expression="business standardization",
        status="ACTIVE",
        steward="business-analyst",
        source="governance-committee",
    )

    preferred = AtlasGlossaryTerm.ref_by_guid("customer-preferred-guid")

    pt_ref = pref_rel.preferred_terms(preferred)
    _assert_related_entity(pt_ref, "AtlasGlossaryPreferredTerm")
    assert pt_ref.guid == "customer-preferred-guid"
    attrs = pt_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "Customer is the preferred term over client"
    assert attrs["expression"] == "business standardization"
    assert attrs["status"] == "ACTIVE"
    assert attrs["steward"] == "business-analyst"
    assert attrs["source"] == "governance-committee"

    ptt_ref = pref_rel.preferred_to_terms(preferred)
    _assert_related_entity(ptt_ref, "AtlasGlossaryPreferredTerm")


def test_atlas_glossary_preferred_term_serialization():
    """Test serialization of AtlasGlossaryPreferredTerm relationship."""
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

    result = json.loads(term.to_json())

    pt_item = _get_serialized_rel_attrs(result, "preferredTerms", 0)
    assert pt_item is not None
    assert pt_item["guid"] == "customer-preferred-guid"
    assert pt_item["relationshipType"] == "AtlasGlossaryPreferredTerm"
    assert pt_item["relationshipAttributes"]["typeName"] == "AtlasGlossaryPreferredTerm"
    assert (
        pt_item["relationshipAttributes"]["attributes"]["description"]
        == "Customer is the preferred term"
    )


# ---------------------------------------------------------------------------
# AtlasGlossaryReplacementTerm
# ---------------------------------------------------------------------------


def test_atlas_glossary_replacement_term_builder():
    """Test AtlasGlossaryReplacementTerm builder methods."""
    repl_rel = AtlasGlossaryReplacementTerm(
        description="New term replaces legacy term",
        expression="system upgrade",
        status="ACTIVE",
        steward="data-architect",
        source="manual",
    )

    new_term = AtlasGlossaryTerm.ref_by_guid("new-term-guid")

    rt_ref = repl_rel.replacement_terms(new_term)
    _assert_related_entity(rt_ref, "AtlasGlossaryReplacementTerm")
    assert rt_ref.guid == "new-term-guid"
    attrs = rt_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "New term replaces legacy term"

    rb_ref = repl_rel.replaced_by(new_term)
    _assert_related_entity(rb_ref, "AtlasGlossaryReplacementTerm")


def test_atlas_glossary_replacement_term_serialization():
    """Test serialization of AtlasGlossaryReplacementTerm relationship."""
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

    result = json.loads(term.to_json())

    rt_item = _get_serialized_rel_attrs(result, "replacementTerms", 0)
    assert rt_item is not None
    assert rt_item["guid"] == "new-term-guid"
    assert rt_item["relationshipType"] == "AtlasGlossaryReplacementTerm"
    assert (
        rt_item["relationshipAttributes"]["typeName"] == "AtlasGlossaryReplacementTerm"
    )


# ---------------------------------------------------------------------------
# AtlasGlossaryTranslation
# ---------------------------------------------------------------------------


def test_atlas_glossary_translation_builder():
    """Test AtlasGlossaryTranslation builder methods."""
    trans_rel = AtlasGlossaryTranslation(
        description="Spanish translation",
        expression="localization",
        status="ACTIVE",
        steward="translation-team",
        source="manual",
    )

    spanish_term = AtlasGlossaryTerm.ref_by_guid("cliente-spanish-guid")

    tt_ref = trans_rel.translated_terms(spanish_term)
    _assert_related_entity(tt_ref, "AtlasGlossaryTranslation")
    assert tt_ref.guid == "cliente-spanish-guid"
    attrs = tt_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "Spanish translation"

    tlt_ref = trans_rel.translation_terms(spanish_term)
    _assert_related_entity(tlt_ref, "AtlasGlossaryTranslation")


def test_atlas_glossary_translation_serialization():
    """Test serialization of AtlasGlossaryTranslation relationship."""
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

    result = json.loads(term.to_json())

    tt_item = _get_serialized_rel_attrs(result, "translatedTerms", 0)
    assert tt_item is not None
    assert tt_item["guid"] == "cliente-spanish-guid"
    assert tt_item["relationshipType"] == "AtlasGlossaryTranslation"
    assert tt_item["relationshipAttributes"]["typeName"] == "AtlasGlossaryTranslation"


# ---------------------------------------------------------------------------
# AtlasGlossaryRelatedTerm
# ---------------------------------------------------------------------------


def test_atlas_glossary_related_term_builder():
    """Test AtlasGlossaryRelatedTerm builder methods."""
    related_rel = AtlasGlossaryRelatedTerm(
        description="Related term for reference",
        expression="see-also-expression",
        status="ACTIVE",
        steward="data-steward",
        source="manual",
    )

    related = AtlasGlossaryTerm.ref_by_guid("related-term-guid")

    sa_ref = related_rel.see_also(related)
    _assert_related_entity(sa_ref, "AtlasGlossaryRelatedTerm")
    assert sa_ref.guid == "related-term-guid"
    attrs = sa_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "Related term for reference"
    assert attrs["expression"] == "see-also-expression"
    assert attrs["status"] == "ACTIVE"
    assert attrs["steward"] == "data-steward"
    assert attrs["source"] == "manual"


def test_atlas_glossary_related_term_serialization():
    """Test serialization of AtlasGlossaryRelatedTerm relationship."""
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

    result = json.loads(term.to_json())

    sa_item = _get_serialized_rel_attrs(result, "seeAlso", 0)
    assert sa_item is not None
    assert sa_item["guid"] == "related-term-guid"
    assert sa_item["relationshipType"] == "AtlasGlossaryRelatedTerm"
    assert sa_item["relationshipAttributes"]["typeName"] == "AtlasGlossaryRelatedTerm"
    assert (
        sa_item["relationshipAttributes"]["attributes"]["description"]
        == "Related term for reference"
    )


def test_atlas_glossary_related_term_roundtrip():
    """Test round-trip for AtlasGlossaryRelatedTerm."""
    term = AtlasGlossaryTerm.updater(
        qualified_name="main-term@default",
        name="Main Term",
        glossary_guid="business-glossary-guid",
    )

    related_term_rel = AtlasGlossaryRelatedTerm(
        description="Related term for reference",
        expression="see-also-expression",
        status="ACTIVE",
        steward="data-steward",
        source="manual",
    )
    term.see_also = [
        related_term_rel.see_also(AtlasGlossaryTerm.ref_by_guid("related-term-guid"))
    ]

    restored = AtlasGlossaryTerm.from_json(term.to_json())
    assert restored.see_also is not UNSET
    assert len(restored.see_also) == 1
    sa = restored.see_also[0]
    assert sa.guid == "related-term-guid"
    assert sa.relationship_attributes["typeName"] == "AtlasGlossaryRelatedTerm"


# ---------------------------------------------------------------------------
# AtlasGlossarySynonym
# ---------------------------------------------------------------------------


def test_atlas_glossary_synonym_builder():
    """Test AtlasGlossarySynonym builder methods."""
    syn_rel = AtlasGlossarySynonym(
        description="Synonym relationship",
        expression="synonym-expression",
        status="ACTIVE",
        steward="data-steward",
        source="manual",
    )

    synonym_term = AtlasGlossaryTerm.ref_by_guid("synonym-term-guid")

    syn_ref = syn_rel.synonyms(synonym_term)
    _assert_related_entity(syn_ref, "AtlasGlossarySynonym")
    assert syn_ref.guid == "synonym-term-guid"
    attrs = syn_ref.relationship_attributes["attributes"]
    assert attrs["description"] == "Synonym relationship"
    assert attrs["expression"] == "synonym-expression"


def test_atlas_glossary_synonym_serialization():
    """Test serialization of AtlasGlossarySynonym relationship."""
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

    result = json.loads(term.to_json())

    syn_item = _get_serialized_rel_attrs(result, "synonyms", 0)
    assert syn_item is not None
    assert syn_item["guid"] == "synonym-term-guid"
    assert syn_item["relationshipType"] == "AtlasGlossarySynonym"
    assert syn_item["relationshipAttributes"]["typeName"] == "AtlasGlossarySynonym"


# ---------------------------------------------------------------------------
# AtlasGlossarySemanticAssignment
# ---------------------------------------------------------------------------


def test_atlas_glossary_semantic_assignment_builder():
    """Test AtlasGlossarySemanticAssignment builder methods."""
    sem_rel = AtlasGlossarySemanticAssignment(
        description="Customer table semantically represents customer concept",
        expression="business metadata mapping",
        status="ACTIVE",
        confidence=95,
        created_by="data-analyst",
        steward="data-governance-team",
        source="automated-discovery",
    )

    table = Table.ref_by_guid("customer-table-guid")

    ae_ref = sem_rel.assigned_entities(table)
    _assert_related_entity(ae_ref, "AtlasGlossarySemanticAssignment")
    assert ae_ref.guid == "customer-table-guid"
    attrs = ae_ref.relationship_attributes["attributes"]
    assert (
        attrs["description"]
        == "Customer table semantically represents customer concept"
    )
    assert attrs["expression"] == "business metadata mapping"
    assert attrs["status"] == "ACTIVE"
    assert attrs["confidence"] == 95
    assert attrs["createdBy"] == "data-analyst"
    assert attrs["steward"] == "data-governance-team"
    assert attrs["source"] == "automated-discovery"


def test_atlas_glossary_semantic_assignment_serialization():
    """Test serialization of AtlasGlossarySemanticAssignment relationship."""
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

    result = json.loads(term.to_json())

    ae_item = _get_serialized_rel_attrs(result, "assignedEntities", 0)
    assert ae_item is not None
    assert ae_item["guid"] == "customer-table-guid"
    assert ae_item["relationshipType"] == "AtlasGlossarySemanticAssignment"
    assert (
        ae_item["relationshipAttributes"]["typeName"]
        == "AtlasGlossarySemanticAssignment"
    )
    assert (
        ae_item["relationshipAttributes"]["attributes"]["description"]
        == "Customer term semantically represents customer data"
    )
    assert ae_item["relationshipAttributes"]["attributes"]["confidence"] == 95


def test_atlas_glossary_semantic_assignment_meanings_builder():
    """Test meanings() builder on AtlasGlossarySemanticAssignment."""
    sem_rel = AtlasGlossarySemanticAssignment(
        description="Customer data is assigned this business term",
        expression="manual assignment",
        status="ACTIVE",
        confidence=95,
        created_by="data-analyst",
        steward="business-analyst",
        source="business-glossary",
    )

    term = AtlasGlossaryTerm.ref_by_guid("customer-term-guid")

    meanings_ref = sem_rel.meanings(term)
    _assert_related_entity(meanings_ref, "AtlasGlossarySemanticAssignment")
    assert meanings_ref.guid == "customer-term-guid"
    assert isinstance(meanings_ref, RelatedAtlasGlossaryTerm)


# ---------------------------------------------------------------------------
# UserDefRelationship
# ---------------------------------------------------------------------------


def test_user_def_relationship_builder():
    """Test UserDefRelationship builder methods."""
    udr = UserDefRelationship(
        from_type_label="test-from-label", to_type_label="test-to-label"
    )

    target = AtlasGlossaryTerm.ref_by_guid("target-term-guid")

    to_ref = udr.user_def_relationship_to(target)
    _assert_related_entity(to_ref, "UserDefRelationship")
    assert to_ref.guid == "target-term-guid"
    attrs = to_ref.relationship_attributes["attributes"]
    assert attrs["fromTypeLabel"] == "test-from-label"
    assert attrs["toTypeLabel"] == "test-to-label"

    from_ref = udr.user_def_relationship_from(target)
    _assert_related_entity(from_ref, "UserDefRelationship")


def test_user_def_relationship_serialization():
    """Test serialization of UserDefRelationship relationship."""
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

    result = json.loads(term1.to_json())

    # Check userDefRelationshipFrom
    from_item = _get_serialized_rel_attrs(result, "userDefRelationshipFrom", 0)
    assert from_item is not None
    assert from_item["guid"] == "test-term0-guid"
    assert from_item["relationshipType"] == "UserDefRelationship"
    assert (
        from_item["relationshipAttributes"]["attributes"]["fromTypeLabel"]
        == "test0-from-label"
    )
    assert (
        from_item["relationshipAttributes"]["attributes"]["toTypeLabel"]
        == "test0-to-label"
    )

    # Check userDefRelationshipTo - first item
    to_item1 = _get_serialized_rel_attrs(result, "userDefRelationshipTo", 0)
    assert to_item1 is not None
    assert to_item1["guid"] == "test-term2-guid"
    assert (
        to_item1["relationshipAttributes"]["attributes"]["fromTypeLabel"]
        == "test1-from-label"
    )

    # Check userDefRelationshipTo - second item
    to_item2 = _get_serialized_rel_attrs(result, "userDefRelationshipTo", 1)
    assert to_item2 is not None
    assert to_item2["guid"] == "test-term3-guid"
    assert (
        to_item2["relationshipAttributes"]["attributes"]["fromTypeLabel"]
        == "test2-from-label"
    )


# ---------------------------------------------------------------------------
# CustomRelatedFromEntitiesCustomRelatedToEntities
# ---------------------------------------------------------------------------


def test_custom_related_entities_builder():
    """Test CustomRelatedFromEntitiesCustomRelatedToEntities builder methods."""
    custom_rel = CustomRelatedFromEntitiesCustomRelatedToEntities(
        custom_entity_to_label="relates to",
        custom_entity_from_label="relates from",
    )

    target = CustomEntity.ref_by_guid("target-entity-guid")

    to_ref = custom_rel.custom_related_to_entities(target)
    _assert_related_entity(
        to_ref, "custom_related_from_entities_custom_related_to_entities"
    )
    assert to_ref.guid == "target-entity-guid"
    attrs = to_ref.relationship_attributes["attributes"]
    assert attrs["customEntityToLabel"] == "relates to"
    assert attrs["customEntityFromLabel"] == "relates from"

    from_ref = custom_rel.custom_related_from_entities(target)
    _assert_related_entity(
        from_ref, "custom_related_from_entities_custom_related_to_entities"
    )


def test_custom_related_entities_serialization():
    """Test serialization of CustomRelatedFromEntitiesCustomRelatedToEntities."""
    entity = CustomEntity(qualified_name="main-entity@default", name="Main Entity")

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

    result = json.loads(entity.to_json())

    # Check customRelatedToEntities
    to_item = _get_serialized_rel_attrs(result, "customRelatedToEntities", 0)
    assert to_item is not None
    assert to_item["guid"] == "target-entity-guid"
    assert (
        to_item["relationshipType"]
        == "custom_related_from_entities_custom_related_to_entities"
    )
    assert (
        to_item["relationshipAttributes"]["attributes"]["customEntityToLabel"]
        == "relates to"
    )
    assert (
        to_item["relationshipAttributes"]["attributes"]["customEntityFromLabel"]
        == "relates from"
    )

    # Check customRelatedFromEntities
    from_item = _get_serialized_rel_attrs(result, "customRelatedFromEntities", 0)
    assert from_item is not None
    assert from_item["guid"] == "source-entity-guid"


def test_custom_related_entities_roundtrip():
    """Test round-trip for CustomRelatedFromEntitiesCustomRelatedToEntities."""
    entity = CustomEntity(qualified_name="main-entity@default", name="Main Entity")

    custom_rel = CustomRelatedFromEntitiesCustomRelatedToEntities(
        custom_entity_to_label="relates to", custom_entity_from_label="relates from"
    )

    entity.custom_related_to_entities = [
        custom_rel.custom_related_to_entities(CustomEntity.ref_by_guid("target-guid"))
    ]

    restored = CustomEntity.from_json(entity.to_json())
    assert restored.custom_related_to_entities is not UNSET
    assert len(restored.custom_related_to_entities) == 1
    to_entity = restored.custom_related_to_entities[0]
    assert to_entity.guid == "target-guid"
    assert (
        to_entity.relationship_attributes["typeName"]
        == "custom_related_from_entities_custom_related_to_entities"
    )


# ---------------------------------------------------------------------------
# Combined multiple relationships on a single asset
# ---------------------------------------------------------------------------


def test_combined_multiple_relationships_on_single_asset():
    """Test combining multiple different relationship types on a single glossary term."""
    term = AtlasGlossaryTerm.updater(
        qualified_name="customer@business-glossary",
        name="Customer",
        glossary_guid="business-glossary-guid",
    )

    # 1. Add categorization relationship
    categorization = AtlasGlossaryTermCategorization(
        description="Customer is categorized under business concepts", status="ACTIVE"
    )
    term.categories = [
        categorization.categories(
            AtlasGlossaryCategory.ref_by_guid("business-category-guid")
        )
    ]

    # 2. Add is-a relationship (hierarchical)
    is_a_rel = AtlasGlossaryIsARelationship(
        description="Customer is a type of Person",
        expression="business hierarchy",
        status="ACTIVE",
        steward="business-analyst",
        source="domain-expert",
    )
    term.classifies = [
        is_a_rel.classifies(AtlasGlossaryTerm.ref_by_guid("person-term-guid"))
    ]

    # 3. Add valid values relationship
    valid_value_rel = AtlasGlossaryValidValue(
        description="Active is a valid status for Customer",
        expression="enumeration value",
        status="ACTIVE",
        steward="data-modeler",
        source="business-rules",
    )
    term.valid_values = [
        valid_value_rel.valid_values(
            AtlasGlossaryTerm.ref_by_guid("active-status-guid")
        )
    ]

    # 4. Add preferred term relationship
    preferred_rel = AtlasGlossaryPreferredTerm(
        description="Customer is preferred over Client",
        expression="business preference",
        status="ACTIVE",
        steward="business-analyst",
        source="style-guide",
    )
    term.preferred_to_terms = [
        preferred_rel.preferred_to_terms(
            AtlasGlossaryTerm.ref_by_guid("client-term-guid")
        )
    ]

    # 5. Add synonym relationship
    synonym_rel = AtlasGlossarySynonym(
        description="Customer and Buyer are synonymous",
        expression="business synonym",
        status="ACTIVE",
        steward="business-analyst",
        source="domain-expert",
    )
    term.synonyms = [
        synonym_rel.synonyms(AtlasGlossaryTerm.ref_by_guid("buyer-term-guid"))
    ]

    # 6. Add user-defined relationship
    user_def_rel = UserDefRelationship(
        from_type_label="has account", to_type_label="belongs to customer"
    )
    term.user_def_relationship_to = [
        user_def_rel.user_def_relationship_to(
            AtlasGlossaryTerm.ref_by_guid("account-term-guid")
        )
    ]

    # Serialize and verify structure
    result = json.loads(term.to_json())

    rel_attrs = result.get("relationshipAttributes", {})

    # Verify each relationship type is present
    assert "categories" in rel_attrs
    assert "classifies" in rel_attrs
    assert "validValues" in rel_attrs
    assert "preferredToTerms" in rel_attrs
    assert "synonyms" in rel_attrs
    assert "userDefRelationshipTo" in rel_attrs

    # Verify each has exactly one entry
    assert len(rel_attrs["categories"]) == 1
    assert len(rel_attrs["classifies"]) == 1
    assert len(rel_attrs["validValues"]) == 1
    assert len(rel_attrs["preferredToTerms"]) == 1
    assert len(rel_attrs["synonyms"]) == 1
    assert len(rel_attrs["userDefRelationshipTo"]) == 1

    # Verify relationship types
    assert (
        rel_attrs["categories"][0]["relationshipType"]
        == "AtlasGlossaryTermCategorization"
    )
    assert (
        rel_attrs["classifies"][0]["relationshipType"] == "AtlasGlossaryIsARelationship"
    )
    assert rel_attrs["validValues"][0]["relationshipType"] == "AtlasGlossaryValidValue"
    assert (
        rel_attrs["preferredToTerms"][0]["relationshipType"]
        == "AtlasGlossaryPreferredTerm"
    )
    assert rel_attrs["synonyms"][0]["relationshipType"] == "AtlasGlossarySynonym"
    assert (
        rel_attrs["userDefRelationshipTo"][0]["relationshipType"]
        == "UserDefRelationship"
    )

    # Verify relationship attributes are present in each
    for rel_field in [
        "categories",
        "classifies",
        "validValues",
        "preferredToTerms",
        "synonyms",
        "userDefRelationshipTo",
    ]:
        for rel in rel_attrs[rel_field]:
            assert "relationshipAttributes" in rel
            assert "typeName" in rel["relationshipAttributes"]
            assert "attributes" in rel["relationshipAttributes"]

    # Verify specific relationship attribute values
    assert (
        rel_attrs["categories"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Customer is categorized under business concepts"
    )
    assert (
        rel_attrs["classifies"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Customer is a type of Person"
    )
    assert (
        rel_attrs["validValues"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Active is a valid status for Customer"
    )
    assert (
        rel_attrs["preferredToTerms"][0]["relationshipAttributes"]["attributes"][
            "description"
        ]
        == "Customer is preferred over Client"
    )
    assert (
        rel_attrs["synonyms"][0]["relationshipAttributes"]["attributes"]["description"]
        == "Customer and Buyer are synonymous"
    )
    assert (
        rel_attrs["userDefRelationshipTo"][0]["relationshipAttributes"]["attributes"][
            "fromTypeLabel"
        ]
        == "has account"
    )


# ---------------------------------------------------------------------------
# IndistinctRelationship
# ---------------------------------------------------------------------------


def test_indistinct_relationship():
    """Test IndistinctRelationship as a fallback for unknown relationship types."""
    indistinct = IndistinctRelationship(
        type_name="SomeUnknownRelationship",
        attributes={"custom_field": "custom_value", "status": "ACTIVE"},
    )

    assert indistinct.type_name == "SomeUnknownRelationship"
    assert indistinct.attributes["custom_field"] == "custom_value"
    assert indistinct.attributes["status"] == "ACTIVE"

    attrs_dict = indistinct._attrs_dict()
    assert attrs_dict["custom_field"] == "custom_value"
    assert attrs_dict["status"] == "ACTIVE"


# ---------------------------------------------------------------------------
# Builder with qualified_name (no GUID)
# ---------------------------------------------------------------------------


def test_builder_with_qualified_name_ref():
    """Test relationship builder when related entity uses qualifiedName instead of GUID."""
    categorization = AtlasGlossaryTermCategorization(
        description="Test categorization", status="ACTIVE"
    )

    # Create a term referenced by qualified_name
    term = AtlasGlossaryTerm(
        qualified_name="some-term@some-glossary",
        name="some-term",
    )

    ref = categorization.terms(term)
    _assert_related_entity(ref, "AtlasGlossaryTermCategorization")
    # When guid is not set, unique_attributes should be populated
    assert ref.unique_attributes is not UNSET
    assert ref.unique_attributes["qualifiedName"] == "some-term@some-glossary"
