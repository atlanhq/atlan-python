# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for KafkaCluster model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-kafka-app emits today
(``{connectionQN}/cluster/{clusterName}``, ``kafka_cluster.yaml``), so a creator
change that would re-key existing clusters fails here.
"""

import pytest

from pyatlan_v9.model import KafkaCluster

CONNECTION_QUALIFIED_NAME = "default/apache-kafka/1770801720"
CLUSTER_NAME = "kafka-prod"
CLUSTER_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/cluster/{CLUSTER_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-kafka-app's kafka_cluster transform inputs and output."""
    sut = KafkaCluster.creator(
        name="kafka-prod",
        connection_qualified_name="default/apache-kafka/1770801720",
    )

    assert sut.qualified_name == "default/apache-kafka/1770801720/cluster/kafka-prod"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (CLUSTER_NAME, None, "connection_qualified_name is required"),
        (CLUSTER_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        KafkaCluster.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator sets the connection attributes."""
    sut = KafkaCluster.creator(
        name=CLUSTER_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == CLUSTER_NAME
    assert sut.qualified_name == CLUSTER_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "apache-kafka"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CLUSTER_NAME, "qualified_name is required"),
        (CLUSTER_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        KafkaCluster.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a KafkaCluster for modification."""
    sut = KafkaCluster.updater(qualified_name=CLUSTER_QUALIFIED_NAME, name=CLUSTER_NAME)

    assert sut.qualified_name == CLUSTER_QUALIFIED_NAME
    assert sut.name == CLUSTER_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = KafkaCluster.updater(
        qualified_name=CLUSTER_QUALIFIED_NAME, name=CLUSTER_NAME
    ).trim_to_required()

    assert sut.qualified_name == CLUSTER_QUALIFIED_NAME
    assert sut.name == CLUSTER_NAME
