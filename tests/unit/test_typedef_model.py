# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
from pathlib import Path

import pytest

from pyatlan.model.core import to_camel_case, to_snake_case
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import (
    ClassificationDef,
    CustomMetadataDef,
    EntityDef,
    EnumDef,
    RelationshipDef,
    StructDef,
    TypeDef,
    TypeDefResponse,
)

PARENT_DIR = Path(__file__).parent
TYPEDEFS_JSON = PARENT_DIR / "data" / "typedefs.json"

ENUM_DEF = {
    "category": "ENUM",
    "guid": "f2e6763b-a29d-4fb5-8447-10ba9da14259",
    "createdBy": "service-account-atlan-argo",
    "updatedBy": "service-account-atlan-argo",
    "createTime": 1646710766297,
    "updateTime": 1657756889921,
    "version": 95,
    "name": "AtlasGlossaryTermRelationshipStatus",
    "description": "TermRelationshipStatus defines how reliable the relationship is between two glossary terms",
    "typeVersion": "1.0",
    "serviceType": "atlas_core",
    "elementDefs": [
        {
            "value": "DRAFT",
            "description": "DRAFT means the relationship is under development.",
            "ordinal": 0,
        },
        {
            "value": "ACTIVE",
            "description": "ACTIVE means the relationship is validated and in use.",
            "ordinal": 1,
        },
        {
            "value": "DEPRECATED",
            "description": "DEPRECATED means the the relationship is being phased out.",
            "ordinal": 2,
        },
        {
            "value": "OBSOLETE",
            "description": "OBSOLETE means that the relationship should not be used anymore.",
            "ordinal": 3,
        },
        {
            "value": "OTHER",
            "description": "OTHER means that there is another status.",
            "ordinal": 99,
        },
    ],
}
STRUCT_DEF = {
    "category": "STRUCT",
    "guid": "8afb807f-26f7-4787-b15f-7872d00220ea",
    "createdBy": "service-account-atlan-argo",
    "updatedBy": "service-account-atlan-argo",
    "createTime": 1652745663724,
    "updateTime": 1657756890174,
    "version": 59,
    "name": "AwsTag",
    "description": "Atlas Type representing a tag/value pair associated with an AWS object, eg S3 bucket",
    "typeVersion": "1.0",
    "serviceType": "aws",
    "attributeDefs": [
        {
            "name": "awsTagKey",
            "typeName": "string",
            "isOptional": False,
            "cardinality": "SINGLE",
            "valuesMinCount": 1,
            "valuesMaxCount": 1,
            "isUnique": False,
            "isIndexable": True,
            "includeInNotification": False,
            "skipScrubbing": False,
            "searchWeight": -1,
            "indexType": "STRING",
        },
        {
            "name": "awsTagValue",
            "typeName": "string",
            "isOptional": False,
            "cardinality": "SINGLE",
            "valuesMinCount": 1,
            "valuesMaxCount": 1,
            "isUnique": False,
            "isIndexable": False,
            "includeInNotification": False,
            "skipScrubbing": False,
            "searchWeight": -1,
            "indexType": "STRING",
        },
    ],
}
CLASSIFICATION_DEF = {
    "category": "CLASSIFICATION",
    "guid": "a73d2a3d-984f-4117-b05b-cf8b88dcb559",
    "createdBy": "markpavletich",
    "updatedBy": "markpavletich",
    "createTime": 1646881735887,
    "updateTime": 1660047587203,
    "version": 4,
    "name": "wqDf0vVAF3uL8FXjIyk6St",
    "description": "",
    "typeVersion": "1.0",
    "options": {"color": "Red"},
    "attributeDefs": [],
    "superTypes": [],
    "entityTypes": [],
    "displayName": "Name",
    "subTypes": [],
}


@pytest.fixture()
def type_defs():
    with TYPEDEFS_JSON.open() as input_file:
        return json.load(input_file)


def test_create_element_def():
    element_def = EnumDef.ElementDef(**(ENUM_DEF["elementDefs"][0]))
    assert element_def.description == ENUM_DEF["elementDefs"][0]["description"]
    assert element_def.value == ENUM_DEF["elementDefs"][0]["value"]
    assert element_def.ordinal == ENUM_DEF["elementDefs"][0]["ordinal"]


def check_type_def_properties(type_def: TypeDef, source: dict):
    def check_property(property_name: str):
        key = to_camel_case(property_name)
        value = getattr(type_def, property_name)
        if key in source:
            assert value == source[key]
        else:
            assert value is None

    check_property("create_time")
    check_property("created_by")
    check_property("description")
    check_property("guid")
    check_property("name")
    check_property("type_version")
    check_property("update_time")
    check_property("updated_by")
    check_property("version")


def test_create_enum_def():
    enum_def = EnumDef(**ENUM_DEF)
    assert enum_def.category == AtlanTypeCategory.ENUM
    assert len(enum_def.element_defs) == 5
    check_type_def_properties(enum_def, ENUM_DEF)


def test_enum_defs(type_defs):
    for enum_def_json in type_defs["enumDefs"]:
        enum_def = EnumDef(**enum_def_json)
        assert enum_def.category == AtlanTypeCategory.ENUM
        check_type_def_properties(enum_def, enum_def_json)


def check_attribute(model: object, attribute_name: str, source: dict):
    key = to_camel_case(attribute_name)
    attribute = getattr(model, attribute_name)
    if key in source:
        value = source[key]
        value = type(attribute)(value)
        assert attribute == value
    else:
        assert getattr(model, attribute_name) is None


def test_struct_defs(type_defs):
    for struct_def_json in type_defs["structDefs"]:
        struct_def = StructDef(**struct_def_json)
        assert struct_def.category == AtlanTypeCategory.STRUCT
        check_type_def_properties(struct_def, struct_def_json)
        for index, attribute_def in enumerate(struct_def.attribute_defs):
            attribute_defs = struct_def_json["attributeDefs"][index]
            for key in attribute_def.__dict__.keys():
                check_attribute(attribute_def, key, attribute_defs)
        check_has_attributes(struct_def, struct_def_json)


def test_create_struct_def():
    struct_def = StructDef(**STRUCT_DEF)
    assert struct_def.category == AtlanTypeCategory.STRUCT
    check_type_def_properties(struct_def, STRUCT_DEF)
    for index, attribute_def in enumerate(struct_def.attribute_defs):
        attribute_defs = STRUCT_DEF["attributeDefs"][index]
        for key in attribute_def.__dict__.keys():
            check_attribute(attribute_def, key, attribute_defs)


def test_classification_def(type_defs):
    for classification_def_json in type_defs["classificationDefs"]:
        classification_def = ClassificationDef(**classification_def_json)
        assert classification_def.category == AtlanTypeCategory.CLASSIFICATION
        check_type_def_properties(classification_def, classification_def_json)
        check_has_attributes(classification_def, classification_def_json)


def check_has_attributes(type_def: TypeDef, type_def_json: dict):
    for key in type_def_json:
        attribute_name = to_snake_case(key)
        assert hasattr(type_def, attribute_name)


def test_entity_def(type_defs):
    for entity_def_json in type_defs["entityDefs"]:
        entity_def = EntityDef(**entity_def_json)
        assert entity_def.category == AtlanTypeCategory.ENTITY
        check_type_def_properties(entity_def, entity_def_json)
        check_has_attributes(entity_def, entity_def_json)


def test_relationship_def(type_defs):
    for relationship_def_json in type_defs["relationshipDefs"]:
        relationship_def = RelationshipDef(**relationship_def_json)
        assert relationship_def.category == AtlanTypeCategory.RELATIONSHIP
        check_type_def_properties(relationship_def, relationship_def_json)
        check_has_attributes(relationship_def, relationship_def_json)


def test_business_metadata_def(type_defs):
    for business_metadata_def_json in type_defs["businessMetadataDefs"]:
        business_metadata_def = CustomMetadataDef(**business_metadata_def_json)
        assert business_metadata_def.category == AtlanTypeCategory.CUSTOM_METADATA
        check_type_def_properties(business_metadata_def, business_metadata_def_json)
        check_has_attributes(business_metadata_def, business_metadata_def_json)


def test_type_def_response(type_defs):
    type_def_response = TypeDefResponse(**type_defs)
    assert isinstance(type_def_response, TypeDefResponse)
