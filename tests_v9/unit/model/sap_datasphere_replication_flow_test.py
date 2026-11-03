# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SapDatasphereReplicationFlow model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-sapdatasphere-app emits today
(``{connQN}/flow/{norm(space)}/{norm(name)}``, FND-3838 census), so a creator
change that would re-key existing replication flows fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SapDatasphereReplicationFlow

CONNECTION_QUALIFIED_NAME = "default/sapdatasphere/1700000000"
CONNECTOR_NAME = "sapdatasphere"
SPACE_NAME = "SALES"
FLOW_NAME = "RF_ORDERS"
SCHEMA_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/DEFAULT/{SPACE_NAME}"
FLOW_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/flow/{SPACE_NAME}/{FLOW_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-sapdatasphere-app's build_replication_flow_asset inputs and output.

    norm() replaces every char outside [A-Za-z0-9_] with one "_" in the qn
    segments only; name and space name keep their raw values.
    """
    sut = SapDatasphereReplicationFlow.creator(
        name="RF Orders.v2",
        space_name="SALES-EU",
        connection_qualified_name="default/sapdatasphere/1700000000",
    )

    assert (
        sut.qualified_name
        == "default/sapdatasphere/1700000000/flow/SALES_EU/RF_Orders_v2"
    )
    assert sut.name == "RF Orders.v2"
    assert sut.sap_datasphere_replication_flow_space_name == "SALES-EU"
    assert (
        sut.sap_datasphere_replication_flow_space_qualified_name
        == "default/sapdatasphere/1700000000/DEFAULT/SALES_EU"
    )
    assert sut.sap_datasphere_schema.unique_attributes == {
        "qualifiedName": "default/sapdatasphere/1700000000/DEFAULT/SALES_EU"
    }
    assert sut.connector_name == "sapdatasphere"
    sut.validate(for_creation=True)


def test_creator_does_not_collapse_unsafe_characters():
    """norm() maps each unsafe char to its own "_" (no de-duplication)."""
    sut = SapDatasphereReplicationFlow.creator(
        name="a  b//c",
        space_name="x.-y",
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == f"{CONNECTION_QUALIFIED_NAME}/flow/x__y/a__b__c"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, space_name, connection_qualified_name, message",
    [
        (None, SPACE_NAME, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", SPACE_NAME, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (FLOW_NAME, None, CONNECTION_QUALIFIED_NAME, "space_name is required"),
        (FLOW_NAME, " ", CONNECTION_QUALIFIED_NAME, "space_name cannot be blank"),
        (FLOW_NAME, SPACE_NAME, None, "connection_qualified_name is required"),
        (FLOW_NAME, SPACE_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, space_name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapDatasphereReplicationFlow.creator(
            name=name,
            space_name=space_name,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator derives the space schema from the connection."""
    sut = SapDatasphereReplicationFlow.creator(
        name=FLOW_NAME,
        space_name=SPACE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == FLOW_NAME
    assert sut.qualified_name == FLOW_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.sap_datasphere_replication_flow_space_name == SPACE_NAME
    assert (
        sut.sap_datasphere_replication_flow_space_qualified_name
        == SCHEMA_QUALIFIED_NAME
    )
    assert sut.sap_datasphere_schema.unique_attributes == {
        "qualifiedName": SCHEMA_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit space schema qualified name."""
    explicit_schema_qn = f"{CONNECTION_QUALIFIED_NAME}/OTHER_DB/{SPACE_NAME}"
    sut = SapDatasphereReplicationFlow.creator(
        name=FLOW_NAME,
        space_name=SPACE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        space_qualified_name=explicit_schema_qn,
    )

    assert sut.qualified_name == FLOW_QUALIFIED_NAME
    assert (
        sut.sap_datasphere_replication_flow_space_qualified_name == explicit_schema_qn
    )
    assert sut.sap_datasphere_schema.unique_attributes == {
        "qualifiedName": explicit_schema_qn
    }


def test_validate_rejects_non_flow_qualified_name():
    """The connector's connection/ qns belong to a different type."""
    sut = SapDatasphereReplicationFlow.updater(
        qualified_name=f"{CONNECTION_QUALIFIED_NAME}/connection/{SPACE_NAME}/{FLOW_NAME}",
        name=FLOW_NAME,
    )

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
        SapDatasphereReplicationFlow.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a SapDatasphereReplicationFlow for modification."""
    sut = SapDatasphereReplicationFlow.updater(
        qualified_name=FLOW_QUALIFIED_NAME, name=FLOW_NAME
    )

    assert sut.qualified_name == FLOW_QUALIFIED_NAME
    assert sut.name == FLOW_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SapDatasphereReplicationFlow.creator(
        name=FLOW_NAME,
        space_name=SPACE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == FLOW_QUALIFIED_NAME
    assert sut.name == FLOW_NAME
    assert sut.sap_datasphere_schema is UNSET
