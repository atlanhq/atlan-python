# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for FabricPage.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-fabric-app emits today (FND-3838 census), so a
creator change that would re-key existing Fabric assets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import FabricPage

CONNECTION_QN = "default/fabric/1712345678"
WORKSPACE_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
REPORT_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f/b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e"
PAGE_QN = "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f/b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e/ReportSection1a2b3c"
NAME = "Overview"
EXPECTED_QN = (
    "default/fabric/1712345678/6f1c2d3e-4a5b-4c6d-8e7f-9a0b1c2d3e4f"
    "/b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e/ReportSection1a2b3c"
)


def _kwargs():
    return dict(
        report_qualified_name=REPORT_QN,
        page_id="ReportSection1a2b3c",
    )


def _creator(**overrides):
    args = dict(name=NAME, **_kwargs())
    args.update(overrides)
    return FabricPage.creator(**args)


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
    assert FabricPage.create(name=NAME, **_kwargs()).qualified_name == EXPECTED_QN


@pytest.mark.parametrize("key", ["name", "report_qualified_name", "page_id"])
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    with pytest.raises(ValueError, match=key):
        _creator(**{key: blank})


def test_creator_rejects_wrong_parent_depth():
    with pytest.raises(ValueError, match="Invalid report_qualified_name"):
        _creator(report_qualified_name=PAGE_QN)


def test_creator_sets_parent():
    sut = _creator()

    assert sut.fabric_report_qualified_name == REPORT_QN
    assert sut.fabric_report.unique_attributes == {"qualifiedName": REPORT_QN}


def test_updater():
    sut = FabricPage.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.fabric_report is UNSET
