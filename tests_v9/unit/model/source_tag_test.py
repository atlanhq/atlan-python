# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SourceTag model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-bridge-app emits today
(``{partnerConnectionQN}/source-tag/{tagId}``, FND-3838 census), so a creator
change that would re-key existing source tags fails here.
"""

import pytest

from pyatlan_v9.model import SourceTag

CONNECTION_QUALIFIED_NAME = "default/bigid/1700000000"
CONNECTOR_NAME = "bigid"
TAG_NAME = "PII"
TAG_ID = "tag-42"
TAG_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/source-tag/{TAG_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-bridge-app's build_raw_tag_records inputs and output."""
    sut = SourceTag.creator(
        name="Sensitive",
        tag_id="tag-1",
        connection_qualified_name="default/bigid/1700000099",
    )

    assert sut.qualified_name == "default/bigid/1700000099/source-tag/tag-1"
    assert sut.tag_id == "tag-1"
    assert sut.connector_name == "bigid"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, tag_id, connection_qualified_name, message",
    [
        (None, TAG_ID, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", TAG_ID, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (TAG_NAME, None, CONNECTION_QUALIFIED_NAME, "tag_id is required"),
        (TAG_NAME, " ", CONNECTION_QUALIFIED_NAME, "tag_id cannot be blank"),
        (TAG_NAME, TAG_ID, None, "connection_qualified_name is required"),
        (TAG_NAME, TAG_ID, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, tag_id: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SourceTag.creator(
            name=name,
            tag_id=tag_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the tag id and connection attributes."""
    sut = SourceTag.creator(
        name=TAG_NAME,
        tag_id=TAG_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == TAG_NAME
    assert sut.tag_id == TAG_ID
    assert sut.qualified_name == TAG_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    sut.validate(for_creation=True)


def test_validate_rejects_qualified_name_without_source_tag_segment():
    """Test validate enforces the source-tag qualifiedName pattern."""
    sut = SourceTag(name=TAG_NAME, qualified_name=f"{CONNECTION_QUALIFIED_NAME}/x")

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, TAG_NAME, "qualified_name is required"),
        (TAG_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SourceTag.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a SourceTag for modification."""
    sut = SourceTag.updater(qualified_name=TAG_QUALIFIED_NAME, name=TAG_NAME)

    assert sut.qualified_name == TAG_QUALIFIED_NAME
    assert sut.name == TAG_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SourceTag.updater(
        qualified_name=TAG_QUALIFIED_NAME, name=TAG_NAME
    ).trim_to_required()

    assert sut.qualified_name == TAG_QUALIFIED_NAME
    assert sut.name == TAG_NAME
