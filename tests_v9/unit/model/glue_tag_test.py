# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for GlueTag and TagAttachment models in pyatlan_v9."""

import json

from pyatlan_v9.model import GlueTag, TagAttachment
from pyatlan_v9.model.enums import GlueTagType
from pyatlan_v9.model.transform import from_atlas_json

CONNECTION_QN = "default/glue/1700000000"
TAG_QN = f"{CONNECTION_QN}/tag/property/OwningTeam"
COLUMN_QN = f"{CONNECTION_QN}/AwsDataCatalog/curated_db/dim_teams/team_name"

GLUE_TAG_ATTRIBUTES = {
    "name": "OwningTeam",
    "qualifiedName": TAG_QN,
    "connectorName": "glue",
    "connectionQualifiedName": CONNECTION_QN,
    "glueTagType": "lf_tag",
    "tagAllowedValues": ["platform", "finance"],
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


def test_glue_tag_type_values():
    assert [member.value for member in GlueTagType] == [
        "property",
        "resource_tag",
        "lf_tag",
    ]


def test_glue_tag_serializes_to_atlas_shape():
    tag = GlueTag(
        name="OwningTeam",
        qualified_name=TAG_QN,
        connector_name="glue",
        connection_qualified_name=CONNECTION_QN,
        glue_tag_type=GlueTagType.LF_TAG.value,
        tag_allowed_values=["platform", "finance"],
    )

    data = json.loads(tag.to_nested_bytes())

    assert data["typeName"] == "GlueTag"
    assert data["attributes"] == GLUE_TAG_ATTRIBUTES


def test_glue_tag_decodes_from_atlas_json():
    payload = {"typeName": "GlueTag", "attributes": GLUE_TAG_ATTRIBUTES}

    tag = from_atlas_json(json.dumps(payload).encode())

    assert isinstance(tag, GlueTag)
    assert tag.glue_tag_type == "lf_tag"
    assert tag.tag_allowed_values == ["platform", "finance"]
    assert tag.qualified_name == TAG_QN


def test_tag_attachment_serializes_publish_contract_fields():
    attachment = TagAttachment(
        name="OwningTeam",
        qualified_name=f"{TAG_QN}/{COLUMN_QN}",
        connector_name="glue",
        connection_qualified_name=CONNECTION_QN,
        object_qualified_name=COLUMN_QN,
        object_type_name="Column",
        tag_qualified_name=TAG_QN,
        source_tag_qualified_name=TAG_QN,
        source_tag_display_name="OwningTeam",
        source_tag_type_name="GlueTag",
        value_type="STRING",
        value="platform",
        tag_attachment_string_value="platform",
        propagate=False,
    )

    data = json.loads(attachment.to_nested_bytes())

    assert data["typeName"] == "TagAttachment"
    assert data["attributes"] == TAG_ATTACHMENT_ATTRIBUTES


def test_tag_attachment_decodes_from_atlas_json():
    payload = {"typeName": "TagAttachment", "attributes": TAG_ATTACHMENT_ATTRIBUTES}

    attachment = from_atlas_json(json.dumps(payload).encode())

    assert isinstance(attachment, TagAttachment)
    assert attachment.object_qualified_name == COLUMN_QN
    assert attachment.source_tag_type_name == "GlueTag"
    assert attachment.value == "platform"
    assert attachment.propagate is False
