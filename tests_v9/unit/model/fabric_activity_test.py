# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for FabricActivity.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-fabric-app emits today (FND-3838 census), so a
creator change that would re-key existing Fabric assets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import FabricActivity

CONNECTION_QN = "default/fabric/1712345678"
WORKSPACE_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
DATA_PIPELINE_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f/d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a"
NAME = "Copy Orders"
EXPECTED_QN = (
    "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
    "/d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a/Copy Orders"
)


def _kwargs():
    return dict(
        data_pipeline_qualified_name=DATA_PIPELINE_QN,
    )


def _creator(**overrides):
    args = dict(name=NAME, **_kwargs())
    args.update(overrides)
    return FabricActivity.creator(**args)


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
    assert FabricActivity.create(name=NAME, **_kwargs()).qualified_name == EXPECTED_QN


@pytest.mark.parametrize("key", ["name", "data_pipeline_qualified_name"])
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    with pytest.raises(ValueError, match=key):
        _creator(**{key: blank})


def test_creator_rejects_wrong_parent_depth():
    with pytest.raises(ValueError, match="Invalid data_pipeline_qualified_name"):
        _creator(data_pipeline_qualified_name=WORKSPACE_QN)


def test_creator_sets_parent():
    sut = _creator()

    # atlan-fabric-app never sets the denormalised pipeline qualifiedName.
    assert sut.fabric_data_pipeline_qualified_name is UNSET
    assert sut.fabric_data_pipeline.unique_attributes == {
        "qualifiedName": DATA_PIPELINE_QN
    }


def test_updater():
    sut = FabricActivity.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.fabric_data_pipeline is UNSET
