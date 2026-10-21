# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for RedashQuery model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-redash-app emits today
(``{conn}/queries/{id}``, ``app/transformers/redashquery.yaml``), so a creator
change that would re-key existing queries fails here.
"""

import pytest

from pyatlan_v9.model import RedashQuery

CONNECTION_QUALIFIED_NAME = "default/redash/123456789"
QUERY_ID = "42"
QUERY_NAME = "weekly_revenue"
QUERY_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/queries/{QUERY_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-redash-app's redashquery.yaml inputs and output."""
    sut = RedashQuery.creator(
        name="weekly_revenue",
        query_id=42,
        connection_qualified_name="default/redash/123456789",
    )

    assert sut.qualified_name == "default/redash/123456789/queries/42"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, query_id, connection_qualified_name, message",
    [
        (None, QUERY_ID, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", QUERY_ID, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (QUERY_NAME, None, CONNECTION_QUALIFIED_NAME, "query_id is required"),
        (QUERY_NAME, " ", CONNECTION_QUALIFIED_NAME, "query_id cannot be blank"),
        (QUERY_NAME, QUERY_ID, None, "connection_qualified_name is required"),
        (QUERY_NAME, QUERY_ID, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, query_id: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        RedashQuery.creator(
            name=name,
            query_id=query_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the connection attributes."""
    sut = RedashQuery.creator(
        name=QUERY_NAME,
        query_id=QUERY_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == QUERY_NAME
    assert sut.qualified_name == QUERY_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "redash"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, QUERY_NAME, "qualified_name is required"),
        (QUERY_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        RedashQuery.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a RedashQuery for modification."""
    sut = RedashQuery.updater(qualified_name=QUERY_QUALIFIED_NAME, name=QUERY_NAME)

    assert sut.qualified_name == QUERY_QUALIFIED_NAME
    assert sut.name == QUERY_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = RedashQuery.updater(
        qualified_name=QUERY_QUALIFIED_NAME, name=QUERY_NAME
    ).trim_to_required()

    assert sut.qualified_name == QUERY_QUALIFIED_NAME
    assert sut.name == QUERY_NAME
