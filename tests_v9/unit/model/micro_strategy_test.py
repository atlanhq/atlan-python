# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the MicroStrategy creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-microstrategy-app emits
today (FND-3838 census), so a creator change that would re-key existing
MicroStrategy assets fails here.
"""

import pytest

from pyatlan_v9.model import (
    MicroStrategyAttribute,
    MicroStrategyColumn,
    MicroStrategyCube,
    MicroStrategyDocument,
    MicroStrategyDossier,
    MicroStrategyFact,
    MicroStrategyMetric,
    MicroStrategyProject,
    MicroStrategyReport,
    MicroStrategyVisualization,
)

CONNECTION_QN = "default/microstrategy/1712345678"
PROJECT_ID = "B7CA92F04B9FAE8D941C3E9B7E0CD754"
PROJECT_QN = f"{CONNECTION_QN}/projects/{PROJECT_ID}"
PROJECT_NAME = "MicroStrategy Tutorial"
MSTR_ID = "8D679D3711D3E4981000E787EC6DE8A4"
NAME = "Quarterly Revenue"

PROJECT_CHILDREN = [
    (MicroStrategyAttribute, f"{PROJECT_QN}/attributes/{MSTR_ID}"),
    (MicroStrategyMetric, f"{PROJECT_QN}/metrics/{MSTR_ID}"),
    (MicroStrategyFact, f"{PROJECT_QN}/facts/{MSTR_ID}"),
    (MicroStrategyCube, f"{PROJECT_QN}/cubes/{MSTR_ID}"),
    (MicroStrategyReport, f"{PROJECT_QN}/reports/{MSTR_ID}"),
    (MicroStrategyDocument, f"{PROJECT_QN}/documents/{MSTR_ID}"),
    (MicroStrategyDossier, f"{PROJECT_QN}/dossiers/{MSTR_ID}"),
]

DOSSIER_QN = f"{PROJECT_QN}/dossiers/{MSTR_ID}"
DOSSIER_NAME = "Sales Overview"
CHAPTER_KEY = "K53"
PAGE_KEY = "K66"
VISUALIZATION_KEY = "W71"

COLUMN_ID = "attr_45C11FA478E745FEA08D781CEA190FE5"
COLUMN_PARENTS = [
    ("attributes", "micro_strategy_attribute"),
    ("facts", "micro_strategy_fact"),
    ("metrics", "micro_strategy_metric"),
    ("cubes", "micro_strategy_cube"),
    ("reports", "micro_strategy_report"),
    ("documents", "micro_strategy_document"),
    ("dossiers", "micro_strategy_dossier"),
]


def test_project_creator_matches_app_qualified_name():
    sut = MicroStrategyProject.creator(
        name=PROJECT_NAME,
        connection_qualified_name=CONNECTION_QN,
        micro_strategy_id=PROJECT_ID,
    )

    assert sut.qualified_name == PROJECT_QN
    assert sut.name == PROJECT_NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "microstrategy"
    sut.validate()
    sut.validate(for_creation=True)


@pytest.mark.parametrize("asset_type, expected_qn", PROJECT_CHILDREN)
def test_project_child_creator_matches_app_qualified_name(asset_type, expected_qn):
    sut = asset_type.creator(
        name=NAME,
        micro_strategy_project_qualified_name=PROJECT_QN,
        micro_strategy_project_name=PROJECT_NAME,
        micro_strategy_id=MSTR_ID,
    )

    assert sut.qualified_name == expected_qn
    assert sut.name == NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "microstrategy"
    assert sut.micro_strategy_project_qualified_name == PROJECT_QN
    assert sut.micro_strategy_project_name == PROJECT_NAME
    assert sut.micro_strategy_project.qualified_name == PROJECT_QN
    sut.validate()
    sut.validate(for_creation=True)


@pytest.mark.parametrize("asset_type, _", PROJECT_CHILDREN)
def test_project_child_creator_honours_explicit_connection(asset_type, _):
    other_connection = "default/microstrategy/999"
    sut = asset_type.creator(
        name=NAME,
        micro_strategy_project_qualified_name=PROJECT_QN,
        micro_strategy_project_name=PROJECT_NAME,
        micro_strategy_id=MSTR_ID,
        connection_qualified_name=other_connection,
    )

    assert sut.connection_qualified_name == other_connection


def test_visualization_creator_matches_app_qualified_name():
    sut = MicroStrategyVisualization.creator(
        name=NAME,
        micro_strategy_dossier_qualified_name=DOSSIER_QN,
        micro_strategy_dossier_name=DOSSIER_NAME,
        chapter_key=CHAPTER_KEY,
        page_key=PAGE_KEY,
        visualization_key=VISUALIZATION_KEY,
    )

    assert sut.qualified_name == (
        f"{CONNECTION_QN}/projects/{PROJECT_ID}/dossiers/{MSTR_ID}"
        f"/chapters/{CHAPTER_KEY}/pages/{PAGE_KEY}/visualizations/{VISUALIZATION_KEY}"
    )
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "microstrategy"
    assert sut.micro_strategy_dossier_qualified_name == DOSSIER_QN
    assert sut.micro_strategy_dossier_name == DOSSIER_NAME
    assert sut.micro_strategy_dossier.qualified_name == DOSSIER_QN
    sut.validate()


@pytest.mark.parametrize("segment, parent_field", COLUMN_PARENTS)
def test_column_creator_matches_app_qualified_name(segment, parent_field):
    parent_qn = f"{PROJECT_QN}/{segment}/{MSTR_ID}"
    sut = MicroStrategyColumn.creator(
        name=NAME, parent_qualified_name=parent_qn, micro_strategy_id=COLUMN_ID
    )

    assert sut.qualified_name == f"{PROJECT_QN}/columns/{COLUMN_ID}"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "microstrategy"
    assert sut.micro_strategy_project_qualified_name == PROJECT_QN
    assert getattr(sut, parent_field).qualified_name == parent_qn
    typed_parent_qn_field = parent_field.replace(
        "micro_strategy_", "micro_strategy_column_"
    )
    assert getattr(sut, f"{typed_parent_qn_field}_qualified_name") == parent_qn
    for _, other_field in COLUMN_PARENTS:
        if other_field != parent_field:
            assert not getattr(sut, other_field)
    sut.validate()


def test_column_creator_sets_project_name_when_given():
    sut = MicroStrategyColumn.creator(
        name=NAME,
        parent_qualified_name=f"{PROJECT_QN}/attributes/{MSTR_ID}",
        micro_strategy_id=COLUMN_ID,
        micro_strategy_project_name=PROJECT_NAME,
    )

    assert sut.micro_strategy_project_name == PROJECT_NAME


@pytest.mark.parametrize(
    "parent_qn",
    [
        PROJECT_QN,
        f"{PROJECT_QN}/columns/{COLUMN_ID}",
        f"{PROJECT_QN}/folders/{MSTR_ID}",
        f"{CONNECTION_QN}/attributes/{MSTR_ID}",
    ],
)
def test_column_creator_rejects_unknown_parent(parent_qn):
    with pytest.raises(ValueError, match="parent_qualified_name"):
        MicroStrategyColumn.creator(
            name=NAME, parent_qualified_name=parent_qn, micro_strategy_id=COLUMN_ID
        )


@pytest.mark.parametrize(
    "name, connection_qualified_name, micro_strategy_id, message",
    [
        (None, CONNECTION_QN, PROJECT_ID, "name is required"),
        (PROJECT_NAME, None, PROJECT_ID, "connection_qualified_name is required"),
        (PROJECT_NAME, CONNECTION_QN, None, "micro_strategy_id is required"),
        (PROJECT_NAME, CONNECTION_QN, "  ", "micro_strategy_id"),
        (PROJECT_NAME, "", PROJECT_ID, "connection_qualified_name"),
    ],
)
def test_project_creator_rejects_missing_or_blank_inputs(
    name, connection_qualified_name, micro_strategy_id, message
):
    with pytest.raises(ValueError, match=message):
        MicroStrategyProject.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            micro_strategy_id=micro_strategy_id,
        )


@pytest.mark.parametrize("asset_type, _", PROJECT_CHILDREN)
@pytest.mark.parametrize(
    "name, project_qn, project_name, micro_strategy_id, message",
    [
        (None, PROJECT_QN, PROJECT_NAME, MSTR_ID, "name is required"),
        (
            NAME,
            None,
            PROJECT_NAME,
            MSTR_ID,
            "micro_strategy_project_qualified_name is required",
        ),
        (NAME, PROJECT_QN, None, MSTR_ID, "micro_strategy_project_name is required"),
        (NAME, PROJECT_QN, PROJECT_NAME, None, "micro_strategy_id is required"),
        (NAME, PROJECT_QN, PROJECT_NAME, "  ", "micro_strategy_id"),
        (NAME, "", PROJECT_NAME, MSTR_ID, "micro_strategy_project_qualified_name"),
    ],
)
def test_project_child_creator_rejects_missing_or_blank_inputs(
    asset_type, _, name, project_qn, project_name, micro_strategy_id, message
):
    with pytest.raises(ValueError, match=message):
        asset_type.creator(
            name=name,
            micro_strategy_project_qualified_name=project_qn,
            micro_strategy_project_name=project_name,
            micro_strategy_id=micro_strategy_id,
        )


@pytest.mark.parametrize(
    "missing",
    [
        "name",
        "micro_strategy_dossier_qualified_name",
        "micro_strategy_dossier_name",
        "chapter_key",
        "page_key",
        "visualization_key",
    ],
)
def test_visualization_creator_rejects_missing_inputs(missing):
    kwargs = dict(
        name=NAME,
        micro_strategy_dossier_qualified_name=DOSSIER_QN,
        micro_strategy_dossier_name=DOSSIER_NAME,
        chapter_key=CHAPTER_KEY,
        page_key=PAGE_KEY,
        visualization_key=VISUALIZATION_KEY,
    )
    kwargs[missing] = None
    with pytest.raises(ValueError, match=f"{missing} is required"):
        MicroStrategyVisualization.creator(**kwargs)


@pytest.mark.parametrize(
    "missing", ["name", "parent_qualified_name", "micro_strategy_id"]
)
def test_column_creator_rejects_missing_inputs(missing):
    kwargs = dict(
        name=NAME,
        parent_qualified_name=f"{PROJECT_QN}/attributes/{MSTR_ID}",
        micro_strategy_id=COLUMN_ID,
    )
    kwargs[missing] = None
    with pytest.raises(ValueError, match=f"{missing} is required"):
        MicroStrategyColumn.creator(**kwargs)


@pytest.mark.parametrize("asset_type, expected_qn", PROJECT_CHILDREN)
def test_create_alias(asset_type, expected_qn):
    sut = asset_type.create(
        name=NAME,
        micro_strategy_project_qualified_name=PROJECT_QN,
        micro_strategy_project_name=PROJECT_NAME,
        micro_strategy_id=MSTR_ID,
    )

    assert sut.qualified_name == expected_qn
