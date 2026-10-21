# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for RedashVisualization model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-redash-app emits today
(``{conn}/visualizations/{id}``, ``app/transformers/redashvisualization.yaml``),
which is flat under the connection rather than nested under the query, so a
creator change that would re-key existing visualizations fails here.
"""

import pytest

from pyatlan_v9.model import RedashVisualization

CONNECTION_QUALIFIED_NAME = "default/redash/123456789"
QUERY_NAME = "weekly_revenue"
QUERY_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/queries/42"
VIZ_ID = "7"
VIZ_NAME = "Revenue by week"
VIZ_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/visualizations/{VIZ_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-redash-app's extract_visualizations + redashvisualization.yaml."""
    sut = RedashVisualization.creator(
        name="Revenue by week",
        visualization_id=7,
        redash_query_qualified_name="default/redash/123456789/queries/42",
        redash_query_name="weekly_revenue",
    )

    assert sut.qualified_name == "default/redash/123456789/visualizations/7"
    assert sut.redash_query.unique_attributes == {
        "qualifiedName": "default/redash/123456789/queries/42"
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, visualization_id, query_qualified_name, query_name, message",
    [
        (None, VIZ_ID, QUERY_QUALIFIED_NAME, QUERY_NAME, "name is required"),
        (" ", VIZ_ID, QUERY_QUALIFIED_NAME, QUERY_NAME, "name cannot be blank"),
        (
            VIZ_NAME,
            None,
            QUERY_QUALIFIED_NAME,
            QUERY_NAME,
            "visualization_id is required",
        ),
        (
            VIZ_NAME,
            " ",
            QUERY_QUALIFIED_NAME,
            QUERY_NAME,
            "visualization_id cannot be blank",
        ),
        (
            VIZ_NAME,
            VIZ_ID,
            None,
            QUERY_NAME,
            "redash_query_qualified_name is required",
        ),
        (
            VIZ_NAME,
            VIZ_ID,
            QUERY_QUALIFIED_NAME,
            None,
            "redash_query_name is required",
        ),
        (
            VIZ_NAME,
            VIZ_ID,
            CONNECTION_QUALIFIED_NAME,
            QUERY_NAME,
            "redash_query_qualified_name is invalid",
        ),
        (
            VIZ_NAME,
            VIZ_ID,
            f"{CONNECTION_QUALIFIED_NAME}/dashboards/42",
            QUERY_NAME,
            "redash_query_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    visualization_id: str,
    query_qualified_name: str,
    query_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        RedashVisualization.creator(
            name=name,
            visualization_id=visualization_id,
            redash_query_qualified_name=query_qualified_name,
            redash_query_name=query_name,
        )


def test_creator():
    """Test creator derives the connection from the query."""
    sut = RedashVisualization.creator(
        name=VIZ_NAME,
        visualization_id=VIZ_ID,
        redash_query_qualified_name=QUERY_QUALIFIED_NAME,
        redash_query_name=QUERY_NAME,
    )

    assert sut.name == VIZ_NAME
    assert sut.qualified_name == VIZ_QUALIFIED_NAME
    assert sut.redash_query_qualified_name == QUERY_QUALIFIED_NAME
    assert sut.redash_query_name == QUERY_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "redash"
    assert sut.redash_query.unique_attributes == {"qualifiedName": QUERY_QUALIFIED_NAME}
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = RedashVisualization.creator(
        name=VIZ_NAME,
        visualization_id=VIZ_ID,
        redash_query_qualified_name=QUERY_QUALIFIED_NAME,
        redash_query_name=QUERY_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == VIZ_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "redash"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, VIZ_NAME, "qualified_name is required"),
        (VIZ_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        RedashVisualization.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a RedashVisualization for modification."""
    sut = RedashVisualization.updater(qualified_name=VIZ_QUALIFIED_NAME, name=VIZ_NAME)

    assert sut.qualified_name == VIZ_QUALIFIED_NAME
    assert sut.name == VIZ_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = RedashVisualization.updater(
        qualified_name=VIZ_QUALIFIED_NAME, name=VIZ_NAME
    ).trim_to_required()

    assert sut.qualified_name == VIZ_QUALIFIED_NAME
    assert sut.name == VIZ_NAME
