import json

from pyatlan.model.assets import Asset, GlueTag, TagAttachment
from pyatlan.model.enums import GlueTagType

CONNECTION_QN = "default/glue/1700000000"
TAG_QN = f"{CONNECTION_QN}/tag/property/OwningTeam"
COLUMN_QN = f"{CONNECTION_QN}/AwsDataCatalog/curated_db/dim_teams/team_name"

GLUE_TAG_ATTRIBUTES = {
    "name": "OwningTeam",
    "qualifiedName": TAG_QN,
    "connectorName": "glue",
    "connectionQualifiedName": CONNECTION_QN,
    "glueTagType": "lf_tag",
    "tagAllowedValues": ["platform"],
}

TAG_ATTACHMENT_ATTRIBUTES = {
    "name": "OwningTeam",
    "qualifiedName": f"{TAG_QN}/{COLUMN_QN}",
    "connectorName": "glue",
    "connectionQualifiedName": CONNECTION_QN,
    "objectQualifiedName": COLUMN_QN,
    "objectTypeName": "Column",
    "tagQualifiedName": TAG_QN,
    "sourceTagQualifiedName": TAG_QN,
    "sourceTagDisplayName": "OwningTeam",
    "sourceTagTypeName": "GlueTag",
    "valueType": "STRING",
    "value": "platform",
    "tagAttachmentStringValue": "platform",
    "propagate": False,
}


def _attributes(asset: Asset) -> dict:
    return json.loads(asset.json(by_alias=True, exclude_unset=True))["attributes"]


def test_glue_tag_serializes_to_atlas_shape():
    tag = GlueTag()
    tag.name = "OwningTeam"
    tag.qualified_name = TAG_QN
    tag.connector_name = "glue"
    tag.connection_qualified_name = CONNECTION_QN
    tag.glue_tag_type = GlueTagType.LF_TAG
    tag.tag_allowed_values = {"platform"}

    assert tag.type_name == "GlueTag"
    assert _attributes(tag) == GLUE_TAG_ATTRIBUTES


def test_glue_tag_decodes_from_atlas_json():
    tag = Asset._convert_to_real_type_(
        {"typeName": "GlueTag", "attributes": GLUE_TAG_ATTRIBUTES}
    )

    assert isinstance(tag, GlueTag)
    assert tag.glue_tag_type == GlueTagType.LF_TAG
    assert tag.tag_allowed_values == {"platform"}


def test_tag_attachment_serializes_publish_contract_fields():
    attachment = TagAttachment()
    attachment.name = "OwningTeam"
    attachment.qualified_name = f"{TAG_QN}/{COLUMN_QN}"
    attachment.connector_name = "glue"
    attachment.connection_qualified_name = CONNECTION_QN
    attachment.object_qualified_name = COLUMN_QN
    attachment.object_type_name = "Column"
    attachment.tag_qualified_name = TAG_QN
    attachment.source_tag_qualified_name = TAG_QN
    attachment.source_tag_display_name = "OwningTeam"
    attachment.source_tag_type_name = "GlueTag"
    attachment.value_type = "STRING"
    attachment.value = "platform"
    attachment.tag_attachment_string_value = "platform"
    attachment.propagate = False

    assert _attributes(attachment) == TAG_ATTACHMENT_ATTRIBUTES


def test_tag_attachment_decodes_from_atlas_json():
    attachment = Asset._convert_to_real_type_(
        {"typeName": "TagAttachment", "attributes": TAG_ATTACHMENT_ATTRIBUTES}
    )

    assert isinstance(attachment, TagAttachment)
    assert attachment.object_qualified_name == COLUMN_QN
    assert attachment.source_tag_type_name == "GlueTag"
    assert attachment.propagate is False
