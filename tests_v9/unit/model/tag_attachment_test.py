# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for TagAttachment.creator in pyatlan_v9."""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import TagAttachment

DATABRICKS_CONN = "default/databricks/1700000000"
DBT_CONN = "default/dbt/1700000000"
BRIDGE_CONN = "default/example-provider/1700000000"


def _create(**kwargs) -> TagAttachment:
    params = {
        "name": "pii",
        "connection_qualified_name": DATABRICKS_CONN,
        "tag_qualified_name": f"{DATABRICKS_CONN}/tag/pii",
        "object_qualified_name": f"{DATABRICKS_CONN}/cat/sch/tbl",
        **kwargs,
    }
    return TagAttachment.creator(**params)


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"name": None}, "name is required"),
        ({"name": " "}, "name cannot be blank"),
        ({"connection_qualified_name": None}, "connection_qualified_name is required"),
        ({"tag_qualified_name": ""}, "tag_qualified_name cannot be blank"),
        ({"object_qualified_name": None}, "object_qualified_name is required"),
        ({"connection_qualified_name": "default/dbt"}, "Invalid connection"),
        ({"qn_style": "unknown"}, "qn_style must be one of"),
    ],
)
def test_creator_with_invalid_parameters_raises_value_error(kwargs, message):
    with pytest.raises(ValueError, match=message):
        _create(**kwargs)


def test_parity_databricks():
    """atlan-databricks-app: {conn}/tag/{tag_name}/{object_qn} (default style)."""
    tag_qn = f"{DATABRICKS_CONN}/tag/pii"
    obj_qn = f"{DATABRICKS_CONN}/cat/sch/tbl/col"
    sut = _create(
        object_qualified_name=obj_qn,
        object_type_name="Column",
        source_tag_type_name="DatabricksUnityCatalogTag",
        value="high",
    )
    assert sut.qualified_name == f"{tag_qn}/{obj_qn}"
    assert sut.name == "pii"
    assert sut.connector_name == "databricks"
    assert sut.connection_qualified_name == DATABRICKS_CONN
    assert sut.tag_qualified_name == tag_qn
    assert sut.source_tag_qualified_name == tag_qn
    assert sut.object_qualified_name == obj_qn
    assert sut.object_type_name == "Column"
    assert sut.source_tag_type_name == "DatabricksUnityCatalogTag"
    assert sut.value == "high"
    assert sut.value_type == "STRING"
    assert sut.tag_attachment_string_value == "high"
    assert sut.propagate is False
    sut.validate(for_creation=True)


def test_parity_dbt():
    """atlan-dbt-app: {dbt_tag_qn}/attachments/{object_qn}."""
    tag_qn = f"{DBT_CONN}/account/1/project/2/tag/finance"
    obj_qn = f"{DBT_CONN}/account/1/project/2/env/3/model.pkg.orders"
    sut = _create(
        name="finance",
        connection_qualified_name=DBT_CONN,
        tag_qualified_name=tag_qn,
        object_qualified_name=obj_qn,
        qn_style="tag_attachments_object",
        source_tag_type_name="DbtTag",
    )
    assert sut.qualified_name == f"{tag_qn}/attachments/{obj_qn}"
    assert sut.connector_name == "dbt"
    assert sut.value is None
    assert sut.value_type == "NONE"
    assert sut.tag_attachment_string_value is UNSET


def test_parity_bridge():
    """atlan-bridge-app: {object_qn}/{tag_name}."""
    tag_qn = f"{BRIDGE_CONN}/source-tag/42"
    obj_qn = f"{BRIDGE_CONN}/db/sch/tbl"
    sut = _create(
        name="Confidential",
        connection_qualified_name=BRIDGE_CONN,
        tag_qualified_name=tag_qn,
        object_qualified_name=obj_qn,
        qn_style="object_tag",
        source_tag_type_name="SourceTag",
    )
    assert sut.qualified_name == f"{obj_qn}/Confidential"
    assert sut.source_tag_display_name == "Confidential"
    assert sut.connector_name == "example-provider"


def test_round_trip_json():
    sut = _create(value="v")
    restored = TagAttachment.from_json(sut.to_json())
    assert restored.qualified_name == sut.qualified_name
    assert restored.tag_qualified_name == sut.tag_qualified_name
