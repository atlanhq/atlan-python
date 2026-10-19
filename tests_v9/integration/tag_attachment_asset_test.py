# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, TagAttachment
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("TAGATT")
TAG_NAME = f"pii_{MODULE_NAME}"

# (qn_style, object path under the connection, expected qn builder)
STYLES = [
    ("tag_object", "cat/sch/tbl", lambda tag, obj: f"{tag}/{obj}"),
    (
        "tag_attachments_object",
        "cat/sch/view",
        lambda tag, obj: f"{tag}/attachments/{obj}",
    ),
    ("object_tag", "cat/sch/col", lambda tag, obj: f"{obj}/{TAG_NAME}"),
]


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.DATABRICKS
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def attachments(
    client: AtlanClient, connection: Connection
) -> Generator[dict, None, None]:
    conn_qn = connection.qualified_name
    tag_qn = f"{conn_qn}/tag/{TAG_NAME}"
    created = {}
    for qn_style, path, _ in STYLES:
        to_create = TagAttachment.creator(
            name=TAG_NAME,
            connection_qualified_name=conn_qn,
            tag_qualified_name=tag_qn,
            object_qualified_name=f"{conn_qn}/{path}",
            qn_style=qn_style,
            value="high",
        )
        created[qn_style] = client.asset.save(to_create).assets_created(
            asset_type=TagAttachment
        )[0]
    yield created
    for result in created.values():
        delete_asset(client, guid=result.guid, asset_type=TagAttachment)


@pytest.mark.parametrize("qn_style, path, expected", STYLES)
def test_tag_attachment(
    client: AtlanClient,
    connection: Connection,
    attachments: dict,
    qn_style: str,
    path: str,
    expected,
):
    conn_qn = connection.qualified_name
    tag_qn = f"{conn_qn}/tag/{TAG_NAME}"
    created = attachments[qn_style]
    assert created.guid
    assert created.qualified_name == expected(tag_qn, f"{conn_qn}/{path}")

    restored = client.asset.get_by_qualified_name(
        asset_type=TagAttachment, qualified_name=created.qualified_name
    )
    assert restored.guid == created.guid
    assert restored.connection_qualified_name == conn_qn
    assert restored.tag_qualified_name == tag_qn
    assert restored.tag_attachment_string_value == "high"
