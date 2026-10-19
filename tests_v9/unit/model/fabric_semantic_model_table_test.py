# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for FabricSemanticModelTable.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-fabric-app emits today (FND-3838 census), so a
creator change that would re-key existing Fabric assets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import FabricSemanticModelTable

CONNECTION_QN = "default/fabric/1712345678"
WORKSPACE_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
SEMANTIC_MODEL_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
NAME = "Sales"
EXPECTED_QN = (
    "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
    "/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/Sales"
)


def _kwargs():
    return dict(
        semantic_model_qualified_name=SEMANTIC_MODEL_QN,
    )


def _creator(**overrides):
    args = dict(name=NAME, **_kwargs())
    args.update(overrides)
    return FabricSemanticModelTable.creator(**args)


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
        FabricSemanticModelTable.create(name=NAME, **_kwargs()).qualified_name
        == EXPECTED_QN
    )


@pytest.mark.parametrize("key", ["name", "semantic_model_qualified_name"])
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    with pytest.raises(ValueError, match=key):
        _creator(**{key: blank})


def test_creator_rejects_wrong_parent_depth():
    with pytest.raises(ValueError, match="Invalid semantic_model_qualified_name"):
        _creator(semantic_model_qualified_name=WORKSPACE_QN)


def test_creator_sets_parent():
    sut = _creator()

    assert sut.fabric_semantic_model_qualified_name == SEMANTIC_MODEL_QN
    assert sut.fabric_semantic_model.unique_attributes == {
        "qualifiedName": SEMANTIC_MODEL_QN
    }


def test_updater():
    sut = FabricSemanticModelTable.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.fabric_semantic_model is UNSET
