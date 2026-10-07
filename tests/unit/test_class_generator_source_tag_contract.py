from pyatlan.generator.class_generator import (
    add_source_tag_contract_attributes,
    get_search_type,
)
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import EntityDef

CONTRACT_FIELDS = {
    "objectQualifiedName": "KeywordField",
    "objectTypeName": "KeywordField",
    "sourceTagQualifiedName": "KeywordField",
    "sourceTagDisplayName": "KeywordField",
    "sourceTagTypeName": "KeywordField",
    "valueType": "KeywordField",
    "value": "KeywordField",
    "propagate": "BooleanField",
}


def _entity_def(name: str) -> EntityDef:
    return EntityDef(
        category=AtlanTypeCategory.ENTITY,
        name=name,
        attribute_defs=[
            {"name": "tagQualifiedName", "typeName": "string"},
            {"name": "tagAttachmentStringValue", "typeName": "string"},
        ],
        relationship_attribute_defs=[],
        super_types=["Asset"],
    )


def test_adds_contract_attributes_to_tag_attachment():
    tag_attachment = _entity_def("TagAttachment")

    add_source_tag_contract_attributes([tag_attachment])

    names = [attribute_def["name"] for attribute_def in tag_attachment.attribute_defs]
    assert names == ["tagQualifiedName", "tagAttachmentStringValue", *CONTRACT_FIELDS]
    search_types = {
        attribute_def["name"]: get_search_type(attribute_def).name
        for attribute_def in tag_attachment.attribute_defs[2:]
    }
    assert search_types == CONTRACT_FIELDS


def test_leaves_other_entity_defs_alone():
    other = _entity_def("SnowflakeTag")

    add_source_tag_contract_attributes([other])

    assert len(other.attribute_defs) == 2


def test_does_not_duplicate_attributes_already_in_the_typedef():
    tag_attachment = _entity_def("TagAttachment")
    tag_attachment.attribute_defs.append({"name": "value", "typeName": "string"})

    add_source_tag_contract_attributes([tag_attachment])

    names = [attribute_def["name"] for attribute_def in tag_attachment.attribute_defs]
    assert names.count("value") == 1
