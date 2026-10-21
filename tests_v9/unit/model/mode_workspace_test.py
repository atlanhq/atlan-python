# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for ModeWorkspace model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-mode-app emits today
(``{connectionQN}/workspaces/{token}``, FND-3838 census), so a creator change
that would re-key existing workspaces fails here.
"""

import pytest

from pyatlan_v9.model import ModeWorkspace
from tests_v9.unit.model.constants import (
    MODE_CONNECTION_QUALIFIED_NAME,
    MODE_CONNECTOR_TYPE,
    MODE_WORKSPACE_NAME,
    MODE_WORKSPACE_QUALIFIED_NAME,
    MODE_WORKSPACE_TOKEN,
)


def test_creator_matches_app_qualified_name():
    """Mirror atlan-mode-app's transform_workspace inputs and output."""
    sut = ModeWorkspace.creator(
        name="Acme Analytics",
        mode_token="a1b2c3d4e5f6",
        connection_qualified_name="default/mode/1712345678",
    )

    assert sut.qualified_name == "default/mode/1712345678/workspaces/a1b2c3d4e5f6"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, mode_token, connection_qualified_name, message",
    [
        (
            None,
            MODE_WORKSPACE_TOKEN,
            MODE_CONNECTION_QUALIFIED_NAME,
            "name is required",
        ),
        (
            " ",
            MODE_WORKSPACE_TOKEN,
            MODE_CONNECTION_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            MODE_WORKSPACE_NAME,
            None,
            MODE_CONNECTION_QUALIFIED_NAME,
            "mode_token is required",
        ),
        (
            MODE_WORKSPACE_NAME,
            " ",
            MODE_CONNECTION_QUALIFIED_NAME,
            "mode_token cannot be blank",
        ),
        (
            MODE_WORKSPACE_NAME,
            MODE_WORKSPACE_TOKEN,
            None,
            "connection_qualified_name is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, mode_token: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ModeWorkspace.creator(
            name=name,
            mode_token=mode_token,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the token, connection and connector name."""
    sut = ModeWorkspace.creator(
        name=MODE_WORKSPACE_NAME,
        mode_token=MODE_WORKSPACE_TOKEN,
        connection_qualified_name=MODE_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == MODE_WORKSPACE_NAME
    assert sut.mode_token == MODE_WORKSPACE_TOKEN
    assert sut.qualified_name == MODE_WORKSPACE_QUALIFIED_NAME
    assert sut.connection_qualified_name == MODE_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == MODE_CONNECTOR_TYPE
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, MODE_WORKSPACE_NAME, "qualified_name is required"),
        (MODE_WORKSPACE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ModeWorkspace.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a ModeWorkspace for modification."""
    sut = ModeWorkspace.updater(
        qualified_name=MODE_WORKSPACE_QUALIFIED_NAME, name=MODE_WORKSPACE_NAME
    )

    assert sut.qualified_name == MODE_WORKSPACE_QUALIFIED_NAME
    assert sut.name == MODE_WORKSPACE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = ModeWorkspace.updater(
        qualified_name=MODE_WORKSPACE_QUALIFIED_NAME, name=MODE_WORKSPACE_NAME
    ).trim_to_required()

    assert sut.qualified_name == MODE_WORKSPACE_QUALIFIED_NAME
    assert sut.name == MODE_WORKSPACE_NAME
