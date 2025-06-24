from unittest.mock import patch

import pytest

from pyatlan.model.assets import AtlasGlossaryTerm
from pyatlan.model.assets.relations import UserDefRelationship


@pytest.fixture()
def mock_asset_guid():
    with patch("pyatlan.utils.random") as mock_random:
        mock_random.random.return_value = 123456789
        yield mock_random


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
    raw_json = {
        "typeName": "AtlasGlossaryTerm",
        "attributes": {
            "userDefRelationshipTo": [
                {
                    "guid": "90a43be2-f700-4f78-8512-4a38f129a901",
                    "typeName": "AtlasGlossaryTerm",
                    "attributes": {
                        "relationshipAttributes": {
                            "typeName": "UserDefRelationship",
                            "attributes": {
                                "fromTypeLabel": "test0-from-label",
                                "toTypeLabel": "test0-to-label",
                            },
                        },
                        "name": "test-term0",
                    },
                    "uniqueAttributes": {
                        "qualifiedName": "Orpt6s3r9CNLFXftuvVpZ@KhgDjmb3kdRvft9TEzv5W"
                    },
                },
            ],
            "qualifiedName": "i9QXU6yl19Grdk8d6yVYT@KhgDjmb3kdRvft9TEzv9W",
            "userDefRelationshipFrom": [
                {
                    "guid": "90a43be2-f700-4f78-8512-4a38f121a901",
                    "typeName": "AtlasGlossaryTerm",
                    "attributes": {
                        "relationshipAttributes": {
                            "typeName": "UserDefRelationship",
                            "attributes": {
                                "fromTypeLabel": "test1-from-label",
                                "toTypeLabel": "test1-to-label",
                            },
                        },
                        "name": "test-term1",
                    },
                    "uniqueAttributes": {
                        "qualifiedName": "Orpt6s3r9CNLFXftuvVpZ@KhgDjmb3kdRvft9TEzv5W"
                    },
                },
                {
                    "guid": "90a43be2-f700-4f78-8512-4a38f121a911",
                    "typeName": "AtlasGlossaryTerm",
                    "attributes": {
                        "relationshipAttributes": {
                            "typeName": "UserDefRelationship",
                            "attributes": {
                                "fromTypeLabel": "test3-from-label",
                                "toTypeLabel": "test3-to-label",
                            },
                        },
                        "name": "test-term3",
                    },
                    "uniqueAttributes": {
                        "qualifiedName": "Orpt6s3r9CNLFXftuvVpZ@KhgDjmb3kdRvft9TEzv5W"
                    },
                },
            ],
            "name": "test-term2",
        },
        "guid": "977b55f9-084c-460f-bf3b-cea5fa740e20",
        "status": "ACTIVE",
        "displayText": "test-term2",
        "classificationNames": [],
        "classifications": [],
        "meaningNames": [],
        "meanings": [],
        "isIncomplete": False,
        "labels": [],
        "createdBy": "test-user",
        "updatedBy": "service-account-apikey",
        "createTime": 1750078015371,
        "updateTime": 1750156224299,
    }
    term = AtlasGlossaryTerm(**raw_json)
    assert term.name and term.guid and term.qualified_name
    to_relation1 = term.user_def_relationship_to[0]
    from_relation1 = term.user_def_relationship_from[0]
    fron_relation2 = term.user_def_relationship_from[1]
    _assert_relationship(to_relation1)
    _assert_relationship(from_relation1)
    _assert_relationship(fron_relation2)


def test_user_def_relationship_serialization(mock_asset_guid):
    expected_json = {
        "typeName": "AtlasGlossaryTerm",
        "attributes": {
            "qualifiedName": "test-term-qn",
            "userDefRelationshipTo": [
                {
                    "typeName": "AtlasGlossaryTerm",
                    "guid": "test-term2-guid",
                    "relationshipAttributes": {
                        "typeName": "UserDefRelationship",
                        "attributes": {
                            "fromTypeLabel": "test1-from-label",
                            "toTypeLabel": "test1-to-label",
                        },
                    },
                    "relationshipType": "UserDefRelationship",
                },
                {
                    "typeName": "AtlasGlossaryTerm",
                    "guid": "test-term3-guid",
                    "relationshipAttributes": {
                        "typeName": "UserDefRelationship",
                        "attributes": {
                            "fromTypeLabel": "test2-from-label",
                            "toTypeLabel": "test2-to-label",
                        },
                    },
                    "relationshipType": "UserDefRelationship",
                },
            ],
            "userDefRelationshipFrom": [
                {
                    "typeName": "AtlasGlossaryTerm",
                    "guid": "test-term0-guid",
                    "relationshipAttributes": {
                        "typeName": "UserDefRelationship",
                        "attributes": {
                            "fromTypeLabel": "test0-from-label",
                            "toTypeLabel": "test0-to-label",
                        },
                    },
                    "relationshipType": "UserDefRelationship",
                }
            ],
            "name": "test-term",
            "anchor": {
                "typeName": "AtlasGlossary",
                "attributes": {"qualifiedName": "test-glossary-guid"},
                "guid": "test-glossary-guid",
            },
        },
        "guid": "-1234567890000000000000000",
    }

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
