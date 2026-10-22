# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for Flow model in pyatlan_v9.

atlan-powercenter-app never creates a Flow; its ``etl.jobRef`` resolves an
existing one, by qualifiedName ``{pcConnectionQN}/{folder}/{workflow}/{session}``
when the repository has a PowerCenter connection, else by name
``{folder}/{workflow}/{session}`` (qi_record.py). The parity tests pin both keys.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import Flow

CONNECTION_QUALIFIED_NAME = "default/informatica-powercenter/123456789"
CONNECTOR_NAME = "informatica-powercenter"
FOLDER_NAME = "SALES"
WORKFLOW_NAME = "wf_load_orders"
SESSION_NAME = "s_m_load_orders"
FLOW_NAME = f"{FOLDER_NAME}/{WORKFLOW_NAME}/{SESSION_NAME}"
FLOW_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/{FOLDER_NAME}/{WORKFLOW_NAME}/{SESSION_NAME}"
)


def test_creator_matches_app_job_ref():
    """Mirror atlan-powercenter-app's build_record etl.jobRef, both modes."""
    sut = Flow.creator(
        connection_qualified_name="default/informatica-powercenter/1700000000",
        folder_name="SALES",
        workflow_name="wf_load_orders",
        session_name="s_m_load_orders",
    )

    # repo override set: nameField = qualifiedName
    assert (
        sut.qualified_name
        == "default/informatica-powercenter/1700000000/SALES/wf_load_orders/s_m_load_orders"
    )
    # no repo override: nameField = name
    assert sut.name == "SALES/wf_load_orders/s_m_load_orders"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "connection_qualified_name, folder_name, workflow_name, session_name, message",
    [
        (
            None,
            FOLDER_NAME,
            WORKFLOW_NAME,
            SESSION_NAME,
            "connection_qualified_name is required",
        ),
        (
            " ",
            FOLDER_NAME,
            WORKFLOW_NAME,
            SESSION_NAME,
            "connection_qualified_name cannot be blank",
        ),
        (
            CONNECTION_QUALIFIED_NAME,
            None,
            WORKFLOW_NAME,
            SESSION_NAME,
            "folder_name is required",
        ),
        (
            CONNECTION_QUALIFIED_NAME,
            " ",
            WORKFLOW_NAME,
            SESSION_NAME,
            "folder_name cannot be blank",
        ),
        (
            CONNECTION_QUALIFIED_NAME,
            FOLDER_NAME,
            None,
            SESSION_NAME,
            "workflow_name is required",
        ),
        (
            CONNECTION_QUALIFIED_NAME,
            FOLDER_NAME,
            " ",
            SESSION_NAME,
            "workflow_name cannot be blank",
        ),
        (
            CONNECTION_QUALIFIED_NAME,
            FOLDER_NAME,
            WORKFLOW_NAME,
            None,
            "session_name is required",
        ),
        (
            CONNECTION_QUALIFIED_NAME,
            FOLDER_NAME,
            WORKFLOW_NAME,
            " ",
            "session_name cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    connection_qualified_name: str,
    folder_name: str,
    workflow_name: str,
    session_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        Flow.creator(
            connection_qualified_name=connection_qualified_name,
            folder_name=folder_name,
            workflow_name=workflow_name,
            session_name=session_name,
        )


@pytest.mark.parametrize(
    "connection_qualified_name",
    [
        "default/informatica-powercenter",
        "default/informatica-powercenter/1/x",
        "/informatica-powercenter/1",
    ],
)
def test_creator_with_invalid_connection_qualified_name_raises_value_error(
    connection_qualified_name: str,
):
    """Test creator rejects a malformed connection qualified name."""
    with pytest.raises(ValueError, match="Invalid connection_qualified_name"):
        Flow.creator(
            connection_qualified_name=connection_qualified_name,
            folder_name=FOLDER_NAME,
            workflow_name=WORKFLOW_NAME,
            session_name=SESSION_NAME,
        )


def test_creator_with_blank_name_raises_value_error():
    """Test an explicit blank name is rejected rather than defaulted."""
    with pytest.raises(ValueError, match="name cannot be blank"):
        Flow.creator(
            connection_qualified_name=CONNECTION_QUALIFIED_NAME,
            folder_name=FOLDER_NAME,
            workflow_name=WORKFLOW_NAME,
            session_name=SESSION_NAME,
            name=" ",
        )


def test_creator():
    """Test creator sets the denormalised connection and folder attributes."""
    sut = Flow.creator(
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        folder_name=FOLDER_NAME,
        workflow_name=WORKFLOW_NAME,
        session_name=SESSION_NAME,
    )

    assert sut.type_name == "Flow"
    assert sut.name == FLOW_NAME
    assert sut.qualified_name == FLOW_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.flow_folder_name == FOLDER_NAME
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_with_explicit_name():
    """Test an explicit name overrides the default but not the qualified name."""
    sut = Flow.creator(
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        folder_name=FOLDER_NAME,
        workflow_name=WORKFLOW_NAME,
        session_name=SESSION_NAME,
        name=SESSION_NAME,
    )

    assert sut.name == SESSION_NAME
    assert sut.qualified_name == FLOW_QUALIFIED_NAME


def test_validate_rejects_qualified_name_with_too_few_segments():
    """Test validate enforces the qualified name pattern."""
    sut = Flow(name=FLOW_NAME, qualified_name=f"default/{FOLDER_NAME}/{WORKFLOW_NAME}")

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FLOW_NAME, "qualified_name is required"),
        (FLOW_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        Flow.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a Flow for modification."""
    sut = Flow.updater(qualified_name=FLOW_QUALIFIED_NAME, name=FLOW_NAME)

    assert sut.type_name == "Flow"
    assert sut.qualified_name == FLOW_QUALIFIED_NAME
    assert sut.name == FLOW_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = Flow.creator(
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        folder_name=FOLDER_NAME,
        workflow_name=WORKFLOW_NAME,
        session_name=SESSION_NAME,
    ).trim_to_required()

    assert sut.qualified_name == FLOW_QUALIFIED_NAME
    assert sut.name == FLOW_NAME
    assert sut.flow_folder_name is UNSET
