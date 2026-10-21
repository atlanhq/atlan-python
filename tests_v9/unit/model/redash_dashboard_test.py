# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for RedashDashboard model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-redash-app emits today
(``{conn}/dashboards/{slug}``, ``app/transformers/redashdashboard.yaml``), so a
creator change that would re-key existing dashboards fails here.
"""

import pytest

from pyatlan_v9.model import RedashDashboard

CONNECTION_QUALIFIED_NAME = "default/redash/123456789"
DASHBOARD_SLUG = "sales-overview"
DASHBOARD_NAME = "Sales Overview"
DASHBOARD_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/dashboards/{DASHBOARD_SLUG}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-redash-app's redashdashboard.yaml inputs and output."""
    sut = RedashDashboard.creator(
        name="Sales Overview",
        slug="sales-overview",
        connection_qualified_name="default/redash/123456789",
    )

    assert sut.qualified_name == "default/redash/123456789/dashboards/sales-overview"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, slug, connection_qualified_name, message",
    [
        (None, DASHBOARD_SLUG, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", DASHBOARD_SLUG, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (DASHBOARD_NAME, None, CONNECTION_QUALIFIED_NAME, "slug is required"),
        (DASHBOARD_NAME, " ", CONNECTION_QUALIFIED_NAME, "slug cannot be blank"),
        (DASHBOARD_NAME, DASHBOARD_SLUG, None, "connection_qualified_name is required"),
        (
            DASHBOARD_NAME,
            DASHBOARD_SLUG,
            " ",
            "connection_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, slug: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        RedashDashboard.creator(
            name=name, slug=slug, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator sets the connection attributes."""
    sut = RedashDashboard.creator(
        name=DASHBOARD_NAME,
        slug=DASHBOARD_SLUG,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == DASHBOARD_NAME
    assert sut.qualified_name == DASHBOARD_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "redash"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DASHBOARD_NAME, "qualified_name is required"),
        (DASHBOARD_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        RedashDashboard.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a RedashDashboard for modification."""
    sut = RedashDashboard.updater(
        qualified_name=DASHBOARD_QUALIFIED_NAME, name=DASHBOARD_NAME
    )

    assert sut.qualified_name == DASHBOARD_QUALIFIED_NAME
    assert sut.name == DASHBOARD_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = RedashDashboard.updater(
        qualified_name=DASHBOARD_QUALIFIED_NAME, name=DASHBOARD_NAME
    ).trim_to_required()

    assert sut.qualified_name == DASHBOARD_QUALIFIED_NAME
    assert sut.name == DASHBOARD_NAME
