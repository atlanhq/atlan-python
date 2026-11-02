# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for AdfActivity model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-adf-app emits today
(``{pipelineQN}/activities/{name}``, FND-3838 census), so a creator change
that would re-key existing activities fails here.
"""

import pytest

from pyatlan_v9.model import AdfActivity

CONNECTION_QUALIFIED_NAME = "default/azure-data-factory/1700000000"
CONNECTOR_NAME = "azure-data-factory"
FACTORY_NAME = "adf-factory"
PIPELINE_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/factory/{FACTORY_NAME}/pipeline/CopyPipeline"
)
ACTIVITY_NAME = "Copy data1"
ACTIVITY_QUALIFIED_NAME = f"{PIPELINE_QUALIFIED_NAME}/activities/{ACTIVITY_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-adf-app's process_activities inputs and output."""
    sut = AdfActivity.creator(
        name="Copy data1",
        adf_pipeline_qualified_name=(
            "default/azure-data-factory/1700000000"
            "/factory/adf-factory/pipeline/CopyPipeline"
        ),
    )

    assert sut.qualified_name == (
        "default/azure-data-factory/1700000000"
        "/factory/adf-factory/pipeline/CopyPipeline/activities/Copy data1"
    )
    assert sut.adf_factory_name == "adf-factory"
    assert sut.connection_qualified_name == "default/azure-data-factory/1700000000"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, pipeline_qualified_name, message",
    [
        (None, PIPELINE_QUALIFIED_NAME, "name is required"),
        (" ", PIPELINE_QUALIFIED_NAME, "name cannot be blank"),
        (ACTIVITY_NAME, None, "adf_pipeline_qualified_name is required"),
        (ACTIVITY_NAME, " ", "adf_pipeline_qualified_name cannot be blank"),
        (
            ACTIVITY_NAME,
            f"{CONNECTION_QUALIFIED_NAME}/CopyPipeline",
            "adf_pipeline_qualified_name is invalid",
        ),
        (
            ACTIVITY_NAME,
            f"{CONNECTION_QUALIFIED_NAME}/factory/{FACTORY_NAME}/dataflows/df1",
            "adf_pipeline_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, pipeline_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AdfActivity.creator(
            name=name, adf_pipeline_qualified_name=pipeline_qualified_name
        )


def test_creator():
    """Test creator derives the factory and connection from the pipeline."""
    sut = AdfActivity.creator(
        name=ACTIVITY_NAME, adf_pipeline_qualified_name=PIPELINE_QUALIFIED_NAME
    )

    assert sut.name == ACTIVITY_NAME
    assert sut.qualified_name == ACTIVITY_QUALIFIED_NAME
    assert sut.adf_pipeline_qualified_name == PIPELINE_QUALIFIED_NAME
    assert sut.adf_factory_name == FACTORY_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.adf_pipeline.unique_attributes == {
        "qualifiedName": PIPELINE_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts explicit factory and connection qualified names."""
    sut = AdfActivity.creator(
        name=ACTIVITY_NAME,
        adf_pipeline_qualified_name=PIPELINE_QUALIFIED_NAME,
        adf_factory_name=FACTORY_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == ACTIVITY_QUALIFIED_NAME
    assert sut.adf_factory_name == FACTORY_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME


def test_validate_rejects_other_qualified_name_shapes():
    """The generated pattern only accepts the app's activity shape."""
    sut = AdfActivity.updater(
        qualified_name=f"{PIPELINE_QUALIFIED_NAME}/{ACTIVITY_NAME}",
        name=ACTIVITY_NAME,
    )

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ACTIVITY_NAME, "qualified_name is required"),
        (ACTIVITY_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AdfActivity.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an AdfActivity for modification."""
    sut = AdfActivity.updater(
        qualified_name=ACTIVITY_QUALIFIED_NAME, name=ACTIVITY_NAME
    )

    assert sut.qualified_name == ACTIVITY_QUALIFIED_NAME
    assert sut.name == ACTIVITY_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = AdfActivity.updater(
        qualified_name=ACTIVITY_QUALIFIED_NAME, name=ACTIVITY_NAME
    ).trim_to_required()

    assert sut.qualified_name == ACTIVITY_QUALIFIED_NAME
    assert sut.name == ACTIVITY_NAME
