import json
import os
from unittest.mock import patch

import pytest

from pyatlan.model.assets import AtlasGlossaryTerm
from pyatlan.model.assets.relations import UserDefRelationship


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


def _assert_relationship(relationship):
    assert relationship
    assert relationship.guid
    assert relationship.type_name
    assert relationship.attributes
    assert relationship.attributes.relationship_attributes
    assert relationship.attributes.relationship_attributes.attributes
    assert (
        relationship.attributes.relationship_attributes.type_name
        == "UserDefRelationship"
    )
    assert relationship.attributes.relationship_attributes.attributes.from_type_label
    assert relationship.attributes.relationship_attributes.attributes.from_type_label


def test_user_def_relationship_deserialization():
    raw_json = _load_test_data("user_def_relationship_deserialization.json")
    term = AtlasGlossaryTerm(**raw_json)
    assert term.name and term.guid and term.qualified_name
    to_relation1 = term.user_def_relationship_to[0]
    from_relation1 = term.user_def_relationship_from[0]
    fron_relation2 = term.user_def_relationship_from[1]
    _assert_relationship(to_relation1)
    _assert_relationship(from_relation1)
    _assert_relationship(fron_relation2)


def test_user_def_relationship_serialization(mock_asset_guid):
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
