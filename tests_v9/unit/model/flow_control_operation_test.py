# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for FlowControlOperation.creator in pyatlan_v9."""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import FlowControlOperation

FABRIC_CONNECTION_QN = "default/fabric/1700000000"
SAGEMAKER_CONNECTION_QN = "default/sagemaker/1700000000"
WORKSPACE_ID = "11111111-2222-3333-4444-555555555555"
NOTEBOOK_ID = "66666666-7777-8888-9999-000000000000"
NOTEBOOK_QN = f"{FABRIC_CONNECTION_QN}/{WORKSPACE_ID}/{NOTEBOOK_ID}"


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"name": None}, "name is required"),
        ({"connection_qualified_name": None}, "connection_qualified_name is required"),
        ({"source_id": " "}, "source_id cannot be blank"),
        ({"scope": None}, "Exactly one of scope or parent_qualified_name"),
        ({"parent_qualified_name": NOTEBOOK_QN}, "Exactly one of scope"),
        ({"scope": ""}, "scope cannot be blank"),
        ({"connection_qualified_name": "default/fabric"}, "Invalid connection"),
    ],
)
def test_creator_with_invalid_parameters_raises_value_error(kwargs, message):
    params = {
        "name": "nb",
        "connection_qualified_name": FABRIC_CONNECTION_QN,
        "source_id": NOTEBOOK_ID,
        "scope": WORKSPACE_ID,
        **kwargs,
    }
    with pytest.raises(ValueError, match=message):
        FlowControlOperation.creator(**params)


def test_creator_child_requires_parent_in_same_connection():
    with pytest.raises(ValueError, match="must belong to connection_qualified_name"):
        FlowControlOperation.creator(
            name="job",
            connection_qualified_name=FABRIC_CONNECTION_QN,
            source_id="abc",
            parent_qualified_name=f"{SAGEMAKER_CONNECTION_QN}/x/y",
        )


def test_parity_fabric_notebook():
    """atlan-fabric-app: {conn}/{workspace_id}/{notebook_id}."""
    sut = FlowControlOperation.creator(
        name="My notebook",
        connection_qualified_name=FABRIC_CONNECTION_QN,
        scope=WORKSPACE_ID,
        source_id=NOTEBOOK_ID,
        flow_id=NOTEBOOK_ID,
    )
    assert sut.qualified_name == NOTEBOOK_QN
    assert sut.name == "My notebook"
    assert sut.connection_qualified_name == FABRIC_CONNECTION_QN
    assert sut.connector_name == "fabric"
    assert sut.flow_id == NOTEBOOK_ID
    assert sut.flow_controlled_by is UNSET
    sut.validate(for_creation=True)


def test_parity_fabric_spark_job():
    """atlan-fabric-app: {notebook_qn}/jobs/{sha256(namespace\\0jobName)}."""
    key = "a" * 64
    sut = FlowControlOperation.creator(
        name="job",
        connection_qualified_name=FABRIC_CONNECTION_QN,
        parent_qualified_name=NOTEBOOK_QN,
        source_id=key,
        flow_id=key,
    )
    assert sut.qualified_name == f"{NOTEBOOK_QN}/jobs/{key}"
    assert sut.flow_controlled_by.qualified_name == NOTEBOOK_QN
    assert sut.flow_id == key
    sut.validate(for_creation=True)


def test_parity_sagemaker_job():
    """atlan-sagemaker-app: {conn}/{region}/{job_name}; flowId is the job ARN."""
    arn = "arn:aws:sagemaker:us-east-1:000000000000:training-job/example-job"
    sut = FlowControlOperation.creator(
        name="example-job",
        connection_qualified_name=SAGEMAKER_CONNECTION_QN,
        scope="us-east-1",
        source_id="example-job",
        flow_id=arn,
    )
    assert sut.qualified_name == f"{SAGEMAKER_CONNECTION_QN}/us-east-1/example-job"
    assert sut.connector_name == "sagemaker"
    assert sut.flow_id == arn
    sut.validate(for_creation=True)


def test_flow_id_optional():
    sut = FlowControlOperation.creator(
        name="j",
        connection_qualified_name=SAGEMAKER_CONNECTION_QN,
        scope="us-east-1",
        source_id="j",
    )
    assert sut.flow_id is UNSET
