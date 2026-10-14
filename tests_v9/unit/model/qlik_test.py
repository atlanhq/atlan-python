# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Qlik Sense creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-qlik-sense-app emits today
(app/transformers/qlik_sense_cloud.py and the generate_field_id column ids in
app/processors/qlik_lineage.py), so a creator change that would re-key existing
Qlik assets fails here.
"""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.model import (
    QlikApp,
    QlikChart,
    QlikColumn,
    QlikDataset,
    QlikSheet,
    QlikSpace,
    QlikStream,
)

CONNECTION_QN = "default/qlik-sense/1712345678"
SPACE_QN = "default/qlik-sense/1712345678/space/sp01"
STREAM_QN = "default/qlik-sense/1712345678/stream/st01"
APP_QN = "default/qlik-sense/1712345678/app/a1b2"
SHEET_QN = "default/qlik-sense/1712345678/app/a1b2/sheet/sh01"
CHART_QN = "default/qlik-sense/1712345678/app/a1b2/chart/ch01"
DATASET_QN = "default/qlik-sense/1712345678/dataset/ds01"
NAME = "Quarterly Sales"
FIELD = "Region"


@pytest.mark.parametrize(
    "asset_type, seg", [(QlikSpace, "space"), (QlikStream, "stream")]
)
def test_space_and_stream_creator_matches_app_qualified_name(asset_type, seg):
    sut = asset_type.creator(
        name=NAME, connection_qualified_name=CONNECTION_QN, qlik_id="sp01"
    )

    assert sut.qualified_name == f"default/qlik-sense/1712345678/{seg}/sp01"
    assert sut.name == NAME
    assert sut.qlik_id == "sp01"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    sut.validate()


@pytest.mark.parametrize(
    "asset_type, expected_qn",
    [
        (QlikApp, "default/qlik-sense/1712345678/app/a1b2"),
        (QlikDataset, "default/qlik-sense/1712345678/dataset/a1b2"),
    ],
)
@pytest.mark.parametrize(
    "space_qn, space_type, space_id",
    [(SPACE_QN, "QlikSpace", "sp01"), (STREAM_QN, "QlikStream", "st01")],
)
def test_app_and_dataset_creator_matches_app_qualified_name(
    asset_type, expected_qn, space_qn, space_type, space_id
):
    sut = asset_type.creator(name=NAME, qlik_id="a1b2", space_qualified_name=space_qn)

    assert sut.qualified_name == expected_qn
    assert sut.qlik_id == "a1b2"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    assert sut.qlik_space_id == space_id
    assert sut.qlik_space_qualified_name == space_qn
    assert sut.qlik_space.type_name == space_type
    assert sut.qlik_space.unique_attributes == {"qualifiedName": space_qn}
    sut.validate(for_creation=True)


def test_app_in_stream_serializes_stream_relationship(serde):
    sut = QlikApp.creator(name=NAME, qlik_id="a1b2", space_qualified_name=STREAM_QN)

    data = json.loads(sut.to_json(nested=True, serde=serde))

    space = data["relationshipAttributes"]["qlikSpace"]
    assert space["typeName"] == "QlikStream"
    assert space["uniqueAttributes"] == {"qualifiedName": STREAM_QN}


def test_sheet_creator_matches_app_qualified_name():
    sut = QlikSheet.creator(
        name=NAME,
        qlik_id="sh01",
        app_qualified_name=APP_QN,
        space_qualified_name=SPACE_QN,
    )

    assert sut.qualified_name == "default/qlik-sense/1712345678/app/a1b2/sheet/sh01"
    assert sut.qlik_id == "sh01"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    assert sut.qlik_app_id == "a1b2"
    assert sut.qlik_app_qualified_name == APP_QN
    assert sut.qlik_app.unique_attributes == {"qualifiedName": APP_QN}
    assert sut.qlik_space_id == "sp01"
    assert sut.qlik_space_qualified_name == SPACE_QN
    sut.validate(for_creation=True)


def test_chart_creator_matches_app_qualified_name():
    sut = QlikChart.creator(
        name=NAME,
        qlik_id="ch01",
        sheet_qualified_name=SHEET_QN,
        space_qualified_name=STREAM_QN,
    )

    # The chart hangs off the app, not the sheet.
    assert sut.qualified_name == "default/qlik-sense/1712345678/app/a1b2/chart/ch01"
    assert sut.qlik_id == "ch01"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.qlik_app_id == "a1b2"
    assert sut.qlik_app_qualified_name == APP_QN
    assert sut.qlik_sheet.unique_attributes == {"qualifiedName": SHEET_QN}
    assert sut.qlik_space_id == "st01"
    assert sut.qlik_space_qualified_name == STREAM_QN
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "asset_type, parent",
    [
        (QlikSheet, {"app_qualified_name": APP_QN}),
        (QlikChart, {"sheet_qualified_name": SHEET_QN}),
    ],
)
def test_sheet_and_chart_space_is_optional(asset_type, parent):
    sut = asset_type.creator(name=NAME, qlik_id="x1", **parent)

    assert sut.qlik_space_id is UNSET
    assert sut.qlik_space_qualified_name is UNSET


@pytest.mark.parametrize(
    "parent_qn, relationship, expected_qn",
    [
        (
            SHEET_QN,
            "qlik_sheet",
            "default/qlik-sense/1712345678/app/a1b2/sheet/sh01"
            "/column/72e9c09388e68cdceee575c42e2ee669",
        ),
        (
            CHART_QN,
            "qlik_chart",
            "default/qlik-sense/1712345678/app/a1b2/chart/ch01"
            "/column/9361398dc447eebbec36cb448d7cc064",
        ),
        (
            DATASET_QN,
            "qlik_dataset",
            "default/qlik-sense/1712345678/dataset/ds01"
            "/column/8899bf1ab296301e5c10c37600324580",
        ),
    ],
)
def test_column_creator_matches_app_qualified_name(
    parent_qn, relationship, expected_qn
):
    sut = QlikColumn.creator(name=FIELD, parent_qualified_name=parent_qn)

    assert sut.qualified_name == expected_qn
    assert sut.name == FIELD
    assert sut.qlik_column_name == FIELD
    assert sut.qlik_parent_qualified_name == parent_qn
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    assert getattr(sut, relationship).unique_attributes == {"qualifiedName": parent_qn}
    for other in {"qlik_sheet", "qlik_chart", "qlik_dataset"} - {relationship}:
        assert not getattr(sut, other)
    sut.validate()


@pytest.mark.parametrize(
    "creator, kwargs, message",
    [
        (
            QlikSpace.creator,
            {"name": "", "connection_qualified_name": CONNECTION_QN, "qlik_id": "x"},
            "name",
        ),
        (
            QlikStream.creator,
            {"name": NAME, "connection_qualified_name": CONNECTION_QN, "qlik_id": ""},
            "qlik_id",
        ),
        (
            QlikApp.creator,
            {"name": NAME, "qlik_id": "x", "space_qualified_name": None},
            "space_qualified_name",
        ),
        (
            QlikDataset.creator,
            {"name": NAME, "qlik_id": " ", "space_qualified_name": SPACE_QN},
            "qlik_id",
        ),
        (
            QlikSheet.creator,
            {"name": NAME, "qlik_id": "x", "app_qualified_name": ""},
            "app_qualified_name",
        ),
        (
            QlikChart.creator,
            {"name": NAME, "qlik_id": "x", "sheet_qualified_name": None},
            "sheet_qualified_name",
        ),
        (
            QlikColumn.creator,
            {"name": "", "parent_qualified_name": SHEET_QN},
            "name",
        ),
    ],
)
def test_creator_with_blank_input_raises(creator, kwargs, message):
    with pytest.raises(ValueError, match=message):
        creator(**kwargs)


@pytest.mark.parametrize(
    "creator, kwargs",
    [
        (
            QlikApp.creator,
            {"name": NAME, "qlik_id": "x", "space_qualified_name": APP_QN},
        ),
        (
            QlikDataset.creator,
            {"name": NAME, "qlik_id": "x", "space_qualified_name": CONNECTION_QN},
        ),
        (
            QlikSheet.creator,
            {"name": NAME, "qlik_id": "x", "app_qualified_name": SPACE_QN},
        ),
        (
            QlikSheet.creator,
            {
                "name": NAME,
                "qlik_id": "x",
                "app_qualified_name": APP_QN,
                "space_qualified_name": DATASET_QN,
            },
        ),
        (
            QlikChart.creator,
            {"name": NAME, "qlik_id": "x", "sheet_qualified_name": CHART_QN},
        ),
        (QlikColumn.creator, {"name": FIELD, "parent_qualified_name": APP_QN}),
        (QlikColumn.creator, {"name": FIELD, "parent_qualified_name": SPACE_QN}),
    ],
)
def test_creator_with_wrong_parent_qualified_name_raises(creator, kwargs):
    with pytest.raises(ValueError, match="must end in"):
        creator(**kwargs)
