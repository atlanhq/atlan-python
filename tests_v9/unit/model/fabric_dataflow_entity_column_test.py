# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for FabricDataflowEntityColumn.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-fabric-app emits today (FND-3838 census), so a
creator change that would re-key existing Fabric assets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import FabricDataflowEntityColumn

CONNECTION_QN = "default/fabric/1712345678"
WORKSPACE_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
DATAFLOW_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f/c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f"
NAME = "order_id"
EXPECTED_QN = (
    "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
    "/c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f/Orders/order_id"
)


def _kwargs():
    return dict(
        dataflow_qualified_name=DATAFLOW_QN,
        dataflow_name="Load Orders",
        entity_name="Orders",
    )


def _creator(**overrides):
    args = dict(name=NAME, **_kwargs())
    args.update(overrides)
    return FabricDataflowEntityColumn.creator(**args)


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "fabric"
    assert sut.asset_space_qualified_name == WORKSPACE_QN
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    assert (
        FabricDataflowEntityColumn.create(name=NAME, **_kwargs()).qualified_name
        == EXPECTED_QN
    )


@pytest.mark.parametrize(
    "key", ["name", "dataflow_qualified_name", "dataflow_name", "entity_name"]
)
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    with pytest.raises(ValueError, match=key):
        _creator(**{key: blank})


def test_creator_sets_parent():
    sut = _creator()

    assert sut.fabric_dataflow_qualified_name == DATAFLOW_QN
    assert sut.fabric_dataflow_name == "Load Orders"
    assert sut.fabric_dataflow.unique_attributes == {"qualifiedName": DATAFLOW_QN}


def test_updater():
    sut = FabricDataflowEntityColumn.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.fabric_dataflow is UNSET
