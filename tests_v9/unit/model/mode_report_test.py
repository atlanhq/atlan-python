# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for ModeReport model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-mode-app emits today
(``{workspaceQN}/reports/{token}``, FND-3838 census), so a creator change
that would re-key existing reports fails here.
"""

import pytest
from msgspec import UNSET


from pyatlan_v9.model import ModeReport
from tests_v9.unit.model.constants import (
    MODE_COLLECTION_QUALIFIED_NAME,
    MODE_CONNECTION_QUALIFIED_NAME,
    MODE_CONNECTOR_TYPE,
    MODE_NAME,
    MODE_REPORT_QUALIFIED_NAME,
    MODE_REPORT_TOKEN,
    MODE_WORKSPACE_NAME,
    MODE_WORKSPACE_QUALIFIED_NAME,
)

OTHER_COLLECTION_QUALIFIED_NAME = (
    f"{MODE_WORKSPACE_QUALIFIED_NAME}/collections/1a2b3c4d5e6f"
)


def test_creator_matches_app_qualified_name():
    """Mirror atlan-mode-app's transform_report inputs and output."""
    sut = ModeReport.creator(
        name="Revenue Overview",
        mode_token="0f1e2d3c4b5a",
        mode_workspace_qualified_name="default/mode/1712345678/workspaces/a1b2c3d4e5f6",
        mode_workspace_name="Acme Analytics",
    )

    assert (
        sut.qualified_name
        == "default/mode/1712345678/workspaces/a1b2c3d4e5f6/reports/0f1e2d3c4b5a"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, mode_token, workspace_qualified_name, workspace_name, message",
    [
        (
            None,
            MODE_REPORT_TOKEN,
            MODE_WORKSPACE_QUALIFIED_NAME,
            MODE_WORKSPACE_NAME,
            "name is required",
        ),
        (
            " ",
            MODE_REPORT_TOKEN,
            MODE_WORKSPACE_QUALIFIED_NAME,
            MODE_WORKSPACE_NAME,
            "name cannot be blank",
        ),
        (
            MODE_NAME,
            None,
            MODE_WORKSPACE_QUALIFIED_NAME,
            MODE_WORKSPACE_NAME,
            "mode_token is required",
        ),
        (
            MODE_NAME,
            MODE_REPORT_TOKEN,
            None,
            MODE_WORKSPACE_NAME,
            "mode_workspace_qualified_name is required",
        ),
        (
            MODE_NAME,
            MODE_REPORT_TOKEN,
            MODE_WORKSPACE_QUALIFIED_NAME,
            None,
            "mode_workspace_name is required",
        ),
        (
            MODE_NAME,
            MODE_REPORT_TOKEN,
            MODE_WORKSPACE_QUALIFIED_NAME,
            " ",
            "mode_workspace_name cannot be blank",
        ),
        (
            MODE_NAME,
            MODE_REPORT_TOKEN,
            MODE_CONNECTION_QUALIFIED_NAME,
            MODE_WORKSPACE_NAME,
            "mode_workspace_qualified_name is invalid",
        ),
        (
            MODE_NAME,
            MODE_REPORT_TOKEN,
            f"{MODE_CONNECTION_QUALIFIED_NAME}/spaces/{MODE_WORKSPACE_NAME}",
            MODE_WORKSPACE_NAME,
            "mode_workspace_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    mode_token: str,
    workspace_qualified_name: str,
    workspace_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ModeReport.creator(
            name=name,
            mode_token=mode_token,
            mode_workspace_qualified_name=workspace_qualified_name,
            mode_workspace_name=workspace_name,
        )


def test_creator():
    """Test creator derives the connection from the workspace."""
    sut = ModeReport.creator(
        name=MODE_NAME,
        mode_token=MODE_REPORT_TOKEN,
        mode_workspace_qualified_name=MODE_WORKSPACE_QUALIFIED_NAME,
        mode_workspace_name=MODE_WORKSPACE_NAME,
    )

    assert sut.name == MODE_NAME
    assert sut.mode_token == MODE_REPORT_TOKEN
    assert sut.qualified_name == MODE_REPORT_QUALIFIED_NAME
    assert sut.mode_workspace_qualified_name == MODE_WORKSPACE_QUALIFIED_NAME
    assert sut.mode_workspace_name == MODE_WORKSPACE_NAME
    assert sut.connection_qualified_name == MODE_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == MODE_CONNECTOR_TYPE
    # The app leaves modeCollections unset when a report has no collection tokens.
    assert sut.mode_collections is UNSET
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = ModeReport.creator(
        name=MODE_NAME,
        mode_token=MODE_REPORT_TOKEN,
        mode_workspace_qualified_name=MODE_WORKSPACE_QUALIFIED_NAME,
        mode_workspace_name=MODE_WORKSPACE_NAME,
        connection_qualified_name=MODE_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == MODE_REPORT_QUALIFIED_NAME
    assert sut.connection_qualified_name == MODE_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == MODE_CONNECTOR_TYPE


def test_creator_with_collections():
    """Test creator relates the report to every collection passed."""
    sut = ModeReport.creator(
        name=MODE_NAME,
        mode_token=MODE_REPORT_TOKEN,
        mode_workspace_qualified_name=MODE_WORKSPACE_QUALIFIED_NAME,
        mode_workspace_name=MODE_WORKSPACE_NAME,
        mode_collection_qualified_names=[
            MODE_COLLECTION_QUALIFIED_NAME,
            OTHER_COLLECTION_QUALIFIED_NAME,
        ],
    )

    assert [c.unique_attributes for c in sut.mode_collections] == [
        {"qualifiedName": MODE_COLLECTION_QUALIFIED_NAME},
        {"qualifiedName": OTHER_COLLECTION_QUALIFIED_NAME},
    ]
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, MODE_NAME, "qualified_name is required"),
        (MODE_REPORT_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ModeReport.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a ModeReport for modification."""
    sut = ModeReport.updater(qualified_name=MODE_REPORT_QUALIFIED_NAME, name=MODE_NAME)

    assert sut.qualified_name == MODE_REPORT_QUALIFIED_NAME
    assert sut.name == MODE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = ModeReport.updater(
        qualified_name=MODE_REPORT_QUALIFIED_NAME, name=MODE_NAME
    ).trim_to_required()

    assert sut.qualified_name == MODE_REPORT_QUALIFIED_NAME
    assert sut.name == MODE_NAME
