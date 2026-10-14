# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for QuickSightAnalysisField model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-quicksight-app emits today
(``{visualQN}/{fieldId}``, FND-3838 census), so a creator change that would
re-key existing analysis fields fails here.
"""

import pytest

from pyatlan_v9.model import QuickSightAnalysisField
from tests_v9.unit.model.constants import (
    QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME,
    QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
    QUICK_SIGHT_CONNECTOR_TYPE,
    QUICK_SIGHT_NAME,
    QUICK_SIGHT_QUALIFIED_NAME,
)

FIELD_ID = "dset1-total"
FIELD_QUALIFIED_NAME = f"{QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME}/{FIELD_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-quicksight-app's analysis_field mapper inputs and output."""
    sut = QuickSightAnalysisField.creator(
        name="total",
        quick_sight_id="dset1-total",
        quick_sight_analysis_visual_qualified_name="default/quicksight/123/an1/sh1/vis1",
        quick_sight_analysis_qualified_name="default/quicksight/123/an1",
        quick_sight_analysis_field_expression="abs({amount}+5000)",
        quick_sight_analysis_field_data_set_identifier="ds",
        connection_qualified_name="default/quicksight/123",
    )

    assert sut.qualified_name == "default/quicksight/123/an1/sh1/vis1/dset1-total"
    assert sut.quick_sight_analysis_field_expression == "abs({amount}+5000)"
    assert sut.quick_sight_analysis_field_data_set_identifier == "ds"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, quick_sight_id, visual_qualified_name, message",
    [
        (
            None,
            FIELD_ID,
            QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME,
            "name is required",
        ),
        (
            " ",
            FIELD_ID,
            QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            QUICK_SIGHT_NAME,
            None,
            QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME,
            "quick_sight_id is required",
        ),
        (
            QUICK_SIGHT_NAME,
            FIELD_ID,
            None,
            "quick_sight_analysis_visual_qualified_name is required",
        ),
        (
            QUICK_SIGHT_NAME,
            FIELD_ID,
            QUICK_SIGHT_QUALIFIED_NAME,
            "quick_sight_analysis_visual_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, quick_sight_id: str, visual_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        QuickSightAnalysisField.creator(
            name=name,
            quick_sight_id=quick_sight_id,
            quick_sight_analysis_visual_qualified_name=visual_qualified_name,
        )


def test_creator():
    """Test creator derives the analysis and connection from the visual."""
    sut = QuickSightAnalysisField.creator(
        name=QUICK_SIGHT_NAME,
        quick_sight_id=FIELD_ID,
        quick_sight_analysis_visual_qualified_name=QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME,
    )

    assert sut.name == QUICK_SIGHT_NAME
    assert sut.quick_sight_id == FIELD_ID
    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert (
        sut.quick_sight_analysis_visual_qualified_name
        == QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME
    )
    assert sut.quick_sight_analysis_qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.connection_qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE
    assert sut.quick_sight_analysis_visual.unique_attributes == {
        "qualifiedName": QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts explicit analysis and connection qualified names."""
    sut = QuickSightAnalysisField.creator(
        name=QUICK_SIGHT_NAME,
        quick_sight_id=FIELD_ID,
        quick_sight_analysis_visual_qualified_name=QUICK_SIGHT_ANALYSIS_VISUAL_QUALIFIED_NAME,
        quick_sight_analysis_qualified_name=QUICK_SIGHT_QUALIFIED_NAME,
        connection_qualified_name=QUICK_SIGHT_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.quick_sight_analysis_qualified_name == QUICK_SIGHT_QUALIFIED_NAME
    assert sut.connection_qualified_name == QUICK_SIGHT_CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == QUICK_SIGHT_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, QUICK_SIGHT_NAME, "qualified_name is required"),
        (FIELD_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        QuickSightAnalysisField.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a QuickSightAnalysisField for modification."""
    sut = QuickSightAnalysisField.updater(
        qualified_name=FIELD_QUALIFIED_NAME, name=QUICK_SIGHT_NAME
    )

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.name == QUICK_SIGHT_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = QuickSightAnalysisField.updater(
        qualified_name=FIELD_QUALIFIED_NAME, name=QUICK_SIGHT_NAME
    ).trim_to_required()

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.name == QUICK_SIGHT_NAME
