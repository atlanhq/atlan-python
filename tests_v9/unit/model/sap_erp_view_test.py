# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SapErpView model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-saperp-app emits today
(``{connectionQN}/view/{cleaned name}``, FND-3838 census), so a creator change
that would re-key existing views fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SapErpView

CONNECTION_QUALIFIED_NAME = "default/sap-ecc/123456789"
CONNECTOR_NAME = "sap-ecc"
VIEW_NAME = "V_T001"
VIEW_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/view/V_T001"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-saperp-app's get_sapview_sql: a namespaced name is cleaned."""
    sut = SapErpView.creator(
        name="/BIC/AZSALES-01",
        connection_qualified_name="default/sap-s4/1700000000",
    )

    assert sut.name == "/BIC/AZSALES-01"
    assert sut.qualified_name == "default/sap-s4/1700000000/view/_BIC_AZSALES_01"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (VIEW_NAME, None, "connection_qualified_name is required"),
        (VIEW_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapErpView.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator sets the denormalised connection attributes."""
    sut = SapErpView.creator(
        name=VIEW_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.type_name == "SapErpView"
    assert sut.name == VIEW_NAME
    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.guid
    sut.validate(for_creation=True)


def test_validate_rejects_qualified_name_without_view_segment():
    """Test the qualifiedName pattern requires the /view/ segment."""
    sut = SapErpView.creator(
        name=VIEW_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )
    sut.qualified_name = f"{CONNECTION_QUALIFIED_NAME}/V_T001"

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, VIEW_NAME, "qualified_name is required"),
        (VIEW_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapErpView.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a SapErpView for modification."""
    sut = SapErpView.updater(qualified_name=VIEW_QUALIFIED_NAME, name=VIEW_NAME)

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SapErpView.creator(
        name=VIEW_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.qualified_name == VIEW_QUALIFIED_NAME
    assert sut.name == VIEW_NAME
    assert sut.connection_qualified_name is UNSET
