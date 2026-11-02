# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for MatillionComponent model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-matillion-app emits today
(``{connectionQN}/component/{componentId}``, FND-3838 census), so a creator
change that would re-key existing components fails here.
"""

import pytest

from pyatlan_v9.model import MatillionComponent

CONNECTION_QUALIFIED_NAME = "default/matillion/1700000000"
CONNECTOR_NAME = "matillion"
JOB_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/job/j1"
JOB_NAME = "load_orders"
COMPONENT_ID = "c1"
COMPONENT_NAME = "Table Input"
COMPONENT_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/component/{COMPONENT_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-matillion-app's map_component inputs and output."""
    sut = MatillionComponent.creator(
        name="Table Input",
        matillion_component_id="5f3c9a1e-77b2-4d0e-9c1a-2b8e6f0d4a11",
        matillion_job_qualified_name="default/matillion/1700000000/job/42",
        matillion_job_name="load_orders",
        connection_qualified_name="default/matillion/1700000000",
    )

    assert (
        sut.qualified_name == "default/matillion/1700000000/component/"
        "5f3c9a1e-77b2-4d0e-9c1a-2b8e6f0d4a11"
    )
    assert sut.matillion_job_qualified_name == "default/matillion/1700000000/job/42"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, component_id, job_qualified_name, job_name, message",
    [
        (None, COMPONENT_ID, JOB_QUALIFIED_NAME, JOB_NAME, "name is required"),
        (" ", COMPONENT_ID, JOB_QUALIFIED_NAME, JOB_NAME, "name cannot be blank"),
        (
            COMPONENT_NAME,
            None,
            JOB_QUALIFIED_NAME,
            JOB_NAME,
            "matillion_component_id is required",
        ),
        (
            COMPONENT_NAME,
            " ",
            JOB_QUALIFIED_NAME,
            JOB_NAME,
            "matillion_component_id cannot be blank",
        ),
        (
            COMPONENT_NAME,
            COMPONENT_ID,
            None,
            JOB_NAME,
            "matillion_job_qualified_name is required",
        ),
        (
            COMPONENT_NAME,
            COMPONENT_ID,
            JOB_QUALIFIED_NAME,
            None,
            "matillion_job_name is required",
        ),
        (
            COMPONENT_NAME,
            COMPONENT_ID,
            JOB_QUALIFIED_NAME,
            " ",
            "matillion_job_name cannot be blank",
        ),
        (
            COMPONENT_NAME,
            COMPONENT_ID,
            CONNECTION_QUALIFIED_NAME,
            JOB_NAME,
            "matillion_job_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    component_id: str,
    job_qualified_name: str,
    job_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        MatillionComponent.creator(
            name=name,
            matillion_component_id=component_id,
            matillion_job_qualified_name=job_qualified_name,
            matillion_job_name=job_name,
        )


def test_creator():
    """Test creator derives the connection from the job."""
    sut = MatillionComponent.creator(
        name=COMPONENT_NAME,
        matillion_component_id=COMPONENT_ID,
        matillion_job_qualified_name=JOB_QUALIFIED_NAME,
        matillion_job_name=JOB_NAME,
    )

    assert sut.name == COMPONENT_NAME
    assert sut.matillion_component_id == COMPONENT_ID
    assert sut.qualified_name == COMPONENT_QUALIFIED_NAME
    assert sut.matillion_job_qualified_name == JOB_QUALIFIED_NAME
    assert sut.matillion_job_name == JOB_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.matillion_job.unique_attributes == {"qualifiedName": JOB_QUALIFIED_NAME}
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = MatillionComponent.creator(
        name=COMPONENT_NAME,
        matillion_component_id=COMPONENT_ID,
        matillion_job_qualified_name=JOB_QUALIFIED_NAME,
        matillion_job_name=JOB_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == COMPONENT_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, COMPONENT_NAME, "qualified_name is required"),
        (COMPONENT_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        MatillionComponent.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a MatillionComponent for modification."""
    sut = MatillionComponent.updater(
        qualified_name=COMPONENT_QUALIFIED_NAME, name=COMPONENT_NAME
    )

    assert sut.qualified_name == COMPONENT_QUALIFIED_NAME
    assert sut.name == COMPONENT_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = MatillionComponent.updater(
        qualified_name=COMPONENT_QUALIFIED_NAME, name=COMPONENT_NAME
    ).trim_to_required()

    assert sut.qualified_name == COMPONENT_QUALIFIED_NAME
    assert sut.name == COMPONENT_NAME
