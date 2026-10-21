# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for ModeQuery model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-mode-app emits today
(``{reportQN}/queries/{token}``, FND-3838 census), so a creator change that
would re-key existing queries fails here.
"""

import pytest

from pyatlan_v9.model import ModeQuery
from tests_v9.unit.model.constants import (
    MODE_CONNECTION_QUALIFIED_NAME,
    MODE_CONNECTOR_TYPE,
    MODE_NAME,
    MODE_QUERY_QUALIFIED_NAME,
    MODE_QUERY_TOKEN,
    MODE_REPORT_NAME,
    MODE_REPORT_QUALIFIED_NAME,
    MODE_WORKSPACE_NAME,
    MODE_WORKSPACE_QUALIFIED_NAME,
)


def test_creator_matches_app_qualified_name():
    """Mirror atlan-mode-app's transform_query inputs and output."""
    sut = ModeQuery.creator(
        name="Daily Orders",
        mode_token="3c4d5e6f7a8b",
        mode_report_qualified_name=(
            "default/mode/1712345678/workspaces/a1b2c3d4e5f6/reports/9a8b7c6d5e4f"
        ),
        mode_report_name="Revenue Overview",
        mode_workspace_name="Acme Analytics",
    )

    assert sut.qualified_name == (
        "default/mode/1712345678/workspaces/a1b2c3d4e5f6"
        "/reports/9a8b7c6d5e4f/queries/3c4d5e6f7a8b"
    )
    assert (
        sut.mode_workspace_qualified_name
        == "default/mode/1712345678/workspaces/a1b2c3d4e5f6"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, mode_token, report_qualified_name, report_name, workspace_name, message",
    [
        (
            None,
            MODE_QUERY_TOKEN,
            MODE_REPORT_QUALIFIED_NAME,
            MODE_REPORT_NAME,
            MODE_WORKSPACE_NAME,
            "name is required",
        ),
        (
            " ",
            MODE_QUERY_TOKEN,
            MODE_REPORT_QUALIFIED_NAME,
            MODE_REPORT_NAME,
            MODE_WORKSPACE_NAME,
            "name cannot be blank",
        ),
        (
            MODE_NAME,
            None,
            MODE_REPORT_QUALIFIED_NAME,
            MODE_REPORT_NAME,
            MODE_WORKSPACE_NAME,
            "mode_token is required",
        ),
        (
            MODE_NAME,
            MODE_QUERY_TOKEN,
            None,
            MODE_REPORT_NAME,
            MODE_WORKSPACE_NAME,
            "mode_report_qualified_name is required",
        ),
        (
            MODE_NAME,
            MODE_QUERY_TOKEN,
            MODE_REPORT_QUALIFIED_NAME,
            None,
            MODE_WORKSPACE_NAME,
            "mode_report_name is required",
        ),
        (
            MODE_NAME,
            MODE_QUERY_TOKEN,
            MODE_REPORT_QUALIFIED_NAME,
            MODE_REPORT_NAME,
            None,
            "mode_workspace_name is required",
        ),
        (
            MODE_NAME,
            MODE_QUERY_TOKEN,
            MODE_REPORT_QUALIFIED_NAME,
            MODE_REPORT_NAME,
            " ",
            "mode_workspace_name cannot be blank",
        ),
        (
            MODE_NAME,
            MODE_QUERY_TOKEN,
            MODE_WORKSPACE_QUALIFIED_NAME,
            MODE_REPORT_NAME,
            MODE_WORKSPACE_NAME,
            "mode_report_qualified_name is invalid",
        ),
        (
            MODE_NAME,
            MODE_QUERY_TOKEN,
            MODE_QUERY_QUALIFIED_NAME,
            MODE_REPORT_NAME,
            MODE_WORKSPACE_NAME,
            "mode_report_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    mode_token: str,
    report_qualified_name: str,
    report_name: str,
    workspace_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ModeQuery.creator(
            name=name,
            mode_token=mode_token,
            mode_report_qualified_name=report_qualified_name,
            mode_report_name=report_name,
            mode_workspace_name=workspace_name,
        )


def test_creator():
    """Test creator derives the workspace and connection from the report."""
    sut = ModeQuery.creator(
        name=MODE_NAME,
        mode_token=MODE_QUERY_TOKEN,
        mode_report_qualified_name=MODE_REPORT_QUALIFIED_NAME,
        mode_report_name=MODE_REPORT_NAME,
        mode_workspace_name=MODE_WORKSPACE_NAME,
    )

    assert sut.name == MODE_NAME
    assert sut.mode_token == MODE_QUERY_TOKEN
    assert sut.qualified_name == MODE_QUERY_QUALIFIED_NAME
    assert sut.mode_report_qualified_name == MODE_REPORT_QUALIFIED_NAME
    assert sut.mode_report_name == MODE_REPORT_NAME
    assert sut.mode_workspace_qualified_name == MODE_WORKSPACE_QUALIFIED_NAME
    assert sut.mode_workspace_name == MODE_WORKSPACE_NAME
    assert sut.connection_qualified_name == MODE_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == MODE_CONNECTOR_TYPE
    assert sut.mode_report.unique_attributes == {
        "qualifiedName": MODE_REPORT_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts explicit workspace and connection qualified names."""
    sut = ModeQuery.creator(
        name=MODE_NAME,
        mode_token=MODE_QUERY_TOKEN,
        mode_report_qualified_name=MODE_REPORT_QUALIFIED_NAME,
        mode_report_name=MODE_REPORT_NAME,
        mode_workspace_name=MODE_WORKSPACE_NAME,
        mode_workspace_qualified_name=MODE_WORKSPACE_QUALIFIED_NAME,
        connection_qualified_name=MODE_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == MODE_QUERY_QUALIFIED_NAME
    assert sut.mode_workspace_qualified_name == MODE_WORKSPACE_QUALIFIED_NAME
    assert sut.connection_qualified_name == MODE_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == MODE_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, MODE_NAME, "qualified_name is required"),
        (MODE_QUERY_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ModeQuery.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a ModeQuery for modification."""
    sut = ModeQuery.updater(qualified_name=MODE_QUERY_QUALIFIED_NAME, name=MODE_NAME)

    assert sut.qualified_name == MODE_QUERY_QUALIFIED_NAME
    assert sut.name == MODE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = ModeQuery.updater(
        qualified_name=MODE_QUERY_QUALIFIED_NAME, name=MODE_NAME
    ).trim_to_required()

    assert sut.qualified_name == MODE_QUERY_QUALIFIED_NAME
    assert sut.name == MODE_NAME
