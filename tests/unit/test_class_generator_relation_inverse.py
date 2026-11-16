"""RelationField carries the attribute at the other end of the relationship.

Atlas stores every relationship on both ends, so walking a relationship graph
means folding an edge seen from both ends into one. The pairing comes from each
relationship typedef's endDef1/endDef2, so it follows the metastore rather than
a hand-written map.
"""

import json
from pathlib import Path

import pytest

from pyatlan.generator.class_generator import (
    RELATIONSHIP_ENDS,
    get_relation_field_args,
    record_relationship_ends,
)
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.model.typedef import TypeDefResponse

TYPEDEFS = Path(__file__).parent / "data" / "typedefs.json"


@pytest.fixture(scope="module", autouse=True)
def _ends():
    """Index the fixture's relationship typedefs once for the module."""
    before = dict(RELATIONSHIP_ENDS)
    type_defs = TypeDefResponse(**json.loads(TYPEDEFS.read_text()))
    record_relationship_ends(type_defs.relationship_defs)
    yield
    RELATIONSHIP_ENDS.clear()
    RELATIONSHIP_ENDS.update(before)


@pytest.fixture(scope="module")
def term_attrs():
    type_defs = TypeDefResponse(**json.loads(TYPEDEFS.read_text()))
    term = next(e for e in type_defs.entity_defs if e.name == "AtlasGlossaryTerm")
    return {a["name"]: a for a in term.relationship_attribute_defs}


@pytest.mark.parametrize(
    ("attribute", "inverse"),
    [
        ("preferredTerms", "preferredToTerms"),
        ("preferredToTerms", "preferredTerms"),
        ("replacedBy", "replacementTerms"),
        ("replacementTerms", "replacedBy"),
        ("translatedTerms", "translationTerms"),
        ("translationTerms", "translatedTerms"),
        ("validValues", "validValuesFor"),
        ("validValuesFor", "validValues"),
        ("isA", "classifies"),
        ("classifies", "isA"),
        # not glossary-specific: the pairing works for any relationship
        ("meanings", "assignedEntities"),
    ],
)
def test_asymmetric_relation_names_its_other_end(term_attrs, attribute, inverse):
    """Each end names the other, so an edge found from either side folds to one."""
    args = get_relation_field_args(term_attrs[attribute])

    assert args == f'"{attribute}", inverse="{inverse}"'


@pytest.mark.parametrize("attribute", ["seeAlso", "synonyms", "antonyms"])
def test_symmetric_relation_is_flagged(term_attrs, attribute):
    """Both ends carry the same name, so the two directions are one edge."""
    args = get_relation_field_args(term_attrs[attribute])

    assert args == f'"{attribute}", inverse="{attribute}", is_symmetric=True'


def test_unknown_relationship_type_still_generates():
    """An unresolvable relationship must generate with the name alone — a wrong
    inverse would be worse than no inverse."""
    args = get_relation_field_args(
        {"name": "somethingNew", "relationshipTypeName": "NotInTheTypedefs"}
    )

    assert args == '"somethingNew"'


def test_relation_field_defaults_keep_the_old_constructor_working():
    """Existing callers pass only the name."""
    field = RelationField("seeAlso")

    assert field.atlan_field_name == "seeAlso"
    assert field.inverse is None
    assert field.is_symmetric is False


def test_relation_field_records_what_it_was_given():
    field = RelationField("preferredTerms", inverse="preferredToTerms")
    symmetric = RelationField("seeAlso", inverse="seeAlso", is_symmetric=True)

    assert field.inverse == "preferredToTerms" and field.is_symmetric is False
    assert symmetric.inverse == "seeAlso" and symmetric.is_symmetric is True
