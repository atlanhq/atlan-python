# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Cognos creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-cognos-app emits today
(FND-3838 census), so a creator change that would re-key existing Cognos assets fails here.
"""

import pytest

from pyatlan_v9.model import (
    CognosColumn,
    CognosDashboard,
    CognosDataset,
    CognosDatasource,
    CognosExploration,
    CognosFile,
    CognosFolder,
    CognosModule,
    CognosPackage,
    CognosReport,
)

CONNECTION_QN = "default/cognos/1712345678"
COGNOS_ID = "i1A2B3C4D5E6F"
NAME = "Quarterly Sales"

ALL_TYPES = [
    (CognosReport, "default/cognos/1712345678/report/i1A2B3C4D5E6F"),
    (CognosDashboard, "default/cognos/1712345678/dashboard/i1A2B3C4D5E6F"),
    (CognosExploration, "default/cognos/1712345678/exploration/i1A2B3C4D5E6F"),
    (CognosFile, "default/cognos/1712345678/file/i1A2B3C4D5E6F"),
    (CognosModule, "default/cognos/1712345678/module/i1A2B3C4D5E6F"),
    (CognosPackage, "default/cognos/1712345678/package/i1A2B3C4D5E6F"),
    (CognosDataset, "default/cognos/1712345678/dataSet2/i1A2B3C4D5E6F"),
    (CognosFolder, "default/cognos/1712345678/folder/i1A2B3C4D5E6F"),
    (CognosDatasource, "default/cognos/1712345678/datasource/i1A2B3C4D5E6F"),
    (CognosColumn, "default/cognos/1712345678/column/i1A2B3C4D5E6F"),
]


@pytest.mark.parametrize("asset_type, expected_qn", ALL_TYPES)
def test_creator_matches_app_qualified_name(asset_type, expected_qn):
    sut = asset_type.creator(
        name=NAME, connection_qualified_name=CONNECTION_QN, cognos_id=COGNOS_ID
    )

    assert sut.qualified_name == expected_qn
    assert sut.name == NAME
    assert sut.cognos_id == COGNOS_ID
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "cognos"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate()


@pytest.mark.parametrize("asset_type, _", ALL_TYPES)
@pytest.mark.parametrize(
    "name, connection_qualified_name, cognos_id, message",
    [
        (None, CONNECTION_QN, COGNOS_ID, "name is required"),
        (NAME, None, COGNOS_ID, "connection_qualified_name is required"),
        (NAME, CONNECTION_QN, None, "cognos_id is required"),
        (NAME, CONNECTION_QN, "  ", "cognos_id"),
        (NAME, "", COGNOS_ID, "connection_qualified_name"),
    ],
)
def test_creator_rejects_missing_or_blank_inputs(
    asset_type, _, name, connection_qualified_name, cognos_id, message
):
    with pytest.raises(ValueError, match=message):
        asset_type.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            cognos_id=cognos_id,
        )


@pytest.mark.parametrize("asset_type, expected_qn", ALL_TYPES)
def test_create_alias(asset_type, expected_qn):
    sut = asset_type.create(
        name=NAME, connection_qualified_name=CONNECTION_QN, cognos_id=COGNOS_ID
    )

    assert sut.qualified_name == expected_qn
