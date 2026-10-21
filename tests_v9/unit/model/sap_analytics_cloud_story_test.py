# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SapAnalyticsCloudStory model in pyatlan_v9.

The parity tests use the exact qualifiedNames atlan-sapanalyticscloud-app emits
(``app/processing/qualified_names.story_path``, golden ``tests/golden/sac-ref``):
``{parentFolder}/{resourceId}``, or ``{connection}/{resourceId}`` for a story
outside any folder.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SapAnalyticsCloudStory

CONNECTION_QUALIFIED_NAME = "default/sapanalyticscloud/1700000000"
CONNECTOR_NAME = "sapanalyticscloud"
STORY_NAME = "SAP_SMPL_DSP_FI_Sample_Report"
RESOURCE_ID = "40A9F68194993DCE5E1E0BB887BAB28A"
PARENT_FOLDER_QUALIFIED_NAME = (
    "default/sapanalyticscloud/1700000000/PUBLIC"
    "/B9F8280354E43C4BBDF03A9A31710EFC/AAB0B033247EE9FA56BE4555C787EAA"
)
STORY_QUALIFIED_NAME = f"{PARENT_FOLDER_QUALIFIED_NAME}/{RESOURCE_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror the app's story in a folder, with its parent folder fields."""
    sut = SapAnalyticsCloudStory.creator(
        name="SAP_SMPL_DSP_FI_Sample_Report",
        resource_id="40A9F68194993DCE5E1E0BB887BAB28A",
        parent_folder_qualified_name=(
            "default/sapanalyticscloud/1700000000/PUBLIC"
            "/B9F8280354E43C4BBDF03A9A31710EFC/AAB0B033247EE9FA56BE4555C787EAA"
        ),
        parent_folder_name="SAP_DSP_SAMPLES",
    )

    assert sut.qualified_name == (
        "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
        "/AAB0B033247EE9FA56BE4555C787EAA/40A9F68194993DCE5E1E0BB887BAB28A"
    )
    assert sut.sap_analytics_cloud_parent_folder_name == "SAP_DSP_SAMPLES"
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_without_folder():
    """A story under one of SAC's synthetic roots has no folder at all."""
    sut = SapAnalyticsCloudStory.creator(
        name="Private story",
        resource_id="A1B2C3D4E5F6",
        connection_qualified_name="default/sapanalyticscloud/1700000000",
    )

    assert sut.qualified_name == "default/sapanalyticscloud/1700000000/A1B2C3D4E5F6"
    assert sut.sap_analytics_cloud_folder is UNSET
    assert sut.sap_analytics_cloud_parent_folder_qualified_name is UNSET
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, resource_id, connection_qualified_name, parent_folder_qualified_name, message",
    [
        (None, RESOURCE_ID, CONNECTION_QUALIFIED_NAME, None, "name is required"),
        (" ", RESOURCE_ID, CONNECTION_QUALIFIED_NAME, None, "name cannot be blank"),
        (STORY_NAME, None, CONNECTION_QUALIFIED_NAME, None, "resource_id is required"),
        (
            STORY_NAME,
            " ",
            CONNECTION_QUALIFIED_NAME,
            None,
            "resource_id cannot be blank",
        ),
        (
            STORY_NAME,
            RESOURCE_ID,
            None,
            None,
            "connection_qualified_name is required",
        ),
        (
            STORY_NAME,
            RESOURCE_ID,
            None,
            CONNECTION_QUALIFIED_NAME,
            "parent_folder_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    resource_id: str,
    connection_qualified_name: str,
    parent_folder_qualified_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapAnalyticsCloudStory.creator(
            name=name,
            resource_id=resource_id,
            connection_qualified_name=connection_qualified_name,
            parent_folder_qualified_name=parent_folder_qualified_name,
        )


def test_creator_derives_connection_from_parent_folder():
    """Test creator derives the connection and relates the folder."""
    sut = SapAnalyticsCloudStory.creator(
        name=STORY_NAME,
        resource_id=RESOURCE_ID,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.name == STORY_NAME
    assert sut.qualified_name == STORY_QUALIFIED_NAME
    assert sut.sap_analytics_cloud_resource_id == RESOURCE_ID
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert (
        sut.sap_analytics_cloud_parent_folder_qualified_name
        == PARENT_FOLDER_QUALIFIED_NAME
    )
    assert sut.sap_analytics_cloud_folder.unique_attributes == {
        "qualifiedName": PARENT_FOLDER_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection():
    """Test an explicit connection qualified name is kept as given."""
    sut = SapAnalyticsCloudStory.creator(
        name=STORY_NAME,
        resource_id=RESOURCE_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.qualified_name == STORY_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, STORY_NAME, "qualified_name is required"),
        (STORY_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapAnalyticsCloudStory.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a minimal instance for modification."""
    sut = SapAnalyticsCloudStory.updater(
        qualified_name=STORY_QUALIFIED_NAME, name=STORY_NAME
    )

    assert sut.qualified_name == STORY_QUALIFIED_NAME
    assert sut.name == STORY_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only the fields needed for update."""
    sut = SapAnalyticsCloudStory.creator(
        name=STORY_NAME,
        resource_id=RESOURCE_ID,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == STORY_QUALIFIED_NAME
    assert sut.name == STORY_NAME
