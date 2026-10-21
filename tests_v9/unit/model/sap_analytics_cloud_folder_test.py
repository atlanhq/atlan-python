# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SapAnalyticsCloudFolder model in pyatlan_v9.

The parity tests use the exact qualifiedNames atlan-sapanalyticscloud-app emits
(``app/processing/qualified_names.folder_path``, golden
``tests/golden/sac-ref``): a root folder is ``{connection}/{resourceId}`` and a
nested folder is ``{parentFolder}/{resourceId}``, at any depth.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SapAnalyticsCloudFolder

CONNECTION_QUALIFIED_NAME = "default/sapanalyticscloud/1700000000"
CONNECTOR_NAME = "sapanalyticscloud"
FOLDER_NAME = "SAC_MOBILE"
RESOURCE_ID = "4FC97AEB76E79EBF42933EFF9496DFB9"
PARENT_FOLDER_QUALIFIED_NAME = (
    "default/sapanalyticscloud/1700000000/PUBLIC"
    "/B9F8280354E43C4BBDF03A9A31710EFC/A5BA1AEB2E2B576DAF1DB51B809BEA6A"
)
FOLDER_QUALIFIED_NAME = f"{PARENT_FOLDER_QUALIFIED_NAME}/{RESOURCE_ID}"


def test_creator_matches_app_qualified_name_for_root_folder():
    """Mirror the app's root folder: no parent, directly under the connection."""
    sut = SapAnalyticsCloudFolder.creator(
        name="SYSTEM",
        resource_id="1784555149097_SYSTEM",
        connection_qualified_name="default/sapanalyticscloud/1700000000",
    )

    assert (
        sut.qualified_name
        == "default/sapanalyticscloud/1700000000/1784555149097_SYSTEM"
    )
    assert sut.sap_analytics_cloud_resource_id == "1784555149097_SYSTEM"
    assert sut.sap_analytics_cloud_parent_folder is UNSET
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_for_nested_folder():
    """Mirror the app's deepest folder (four levels) and its parent fields."""
    sut = SapAnalyticsCloudFolder.creator(
        name="SAP_BestRun_ Bikes_ Mobile",
        resource_id="4FC97AEB76E79EBF42933EFF9496DFB9",
        parent_folder_qualified_name=(
            "default/sapanalyticscloud/1700000000/PUBLIC"
            "/B9F8280354E43C4BBDF03A9A31710EFC/A5BA1AEB2E2B576DAF1DB51B809BEA6A"
        ),
        parent_folder_name="SAC_MOBILE",
    )

    assert sut.qualified_name == (
        "default/sapanalyticscloud/1700000000/PUBLIC/B9F8280354E43C4BBDF03A9A31710EFC"
        "/A5BA1AEB2E2B576DAF1DB51B809BEA6A/4FC97AEB76E79EBF42933EFF9496DFB9"
    )
    assert sut.sap_analytics_cloud_parent_folder_name == "SAC_MOBILE"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, resource_id, connection_qualified_name, parent_folder_qualified_name, message",
    [
        (None, RESOURCE_ID, CONNECTION_QUALIFIED_NAME, None, "name is required"),
        (" ", RESOURCE_ID, CONNECTION_QUALIFIED_NAME, None, "name cannot be blank"),
        (FOLDER_NAME, None, CONNECTION_QUALIFIED_NAME, None, "resource_id is required"),
        (
            FOLDER_NAME,
            " ",
            CONNECTION_QUALIFIED_NAME,
            None,
            "resource_id cannot be blank",
        ),
        (
            FOLDER_NAME,
            RESOURCE_ID,
            None,
            None,
            "connection_qualified_name is required",
        ),
        (
            FOLDER_NAME,
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
        SapAnalyticsCloudFolder.creator(
            name=name,
            resource_id=resource_id,
            connection_qualified_name=connection_qualified_name,
            parent_folder_qualified_name=parent_folder_qualified_name,
        )


def test_creator_derives_connection_from_parent_folder():
    """Test creator derives the connection and relates the parent folder."""
    sut = SapAnalyticsCloudFolder.creator(
        name=FOLDER_NAME,
        resource_id=RESOURCE_ID,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.name == FOLDER_NAME
    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert (
        sut.sap_analytics_cloud_parent_folder_qualified_name
        == PARENT_FOLDER_QUALIFIED_NAME
    )
    assert sut.sap_analytics_cloud_parent_folder.unique_attributes == {
        "qualifiedName": PARENT_FOLDER_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection():
    """Test an explicit connection qualified name is kept as given."""
    sut = SapAnalyticsCloudFolder.creator(
        name=FOLDER_NAME,
        resource_id=RESOURCE_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FOLDER_NAME, "qualified_name is required"),
        (FOLDER_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapAnalyticsCloudFolder.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a minimal instance for modification."""
    sut = SapAnalyticsCloudFolder.updater(
        qualified_name=FOLDER_QUALIFIED_NAME, name=FOLDER_NAME
    )

    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.name == FOLDER_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only the fields needed for update."""
    sut = SapAnalyticsCloudFolder.creator(
        name=FOLDER_NAME,
        resource_id=RESOURCE_ID,
        parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.name == FOLDER_NAME
