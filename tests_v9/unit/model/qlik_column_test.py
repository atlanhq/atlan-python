# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for QlikColumn.creator in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-qlik-sense-app emits today:
`{connection}/{id}`, where `id` comes from generate_field_id in
app/processors/qlik_lineage.py, i.e. `{parent path}/column/{md5}` with the md5
taken over `"{parent path}/column/{field name}"`. A creator change that would
re-key existing Qlik columns fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import QlikColumn

CONNECTION_QN = "default/qlik-sense/1712345678"
SPACE_QN = "default/qlik-sense/1712345678/space/sp01"
APP_QN = "default/qlik-sense/1712345678/app/a1b2"
SHEET_QN = "default/qlik-sense/1712345678/app/a1b2/sheet/sh01"
CHART_QN = "default/qlik-sense/1712345678/app/a1b2/chart/ch01"
DATASET_QN = "default/qlik-sense/1712345678/dataset/ds01"
NAME = "Region"
PARENTS = ["qlik_sheet", "qlik_chart", "qlik_dataset"]


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
def test_creator_matches_app_qualified_name(parent_qn, relationship, expected_qn):
    sut = QlikColumn.creator(
        name=NAME, parent_qualified_name=parent_qn, space_qualified_name=SPACE_QN
    )

    assert sut.qualified_name == expected_qn
    assert sut.name == NAME
    assert sut.qlik_column_name == NAME
    assert sut.qlik_parent_qualified_name == parent_qn
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    assert sut.qlik_space_id == "sp01"
    assert sut.qlik_space_qualified_name == SPACE_QN
    assert getattr(sut, relationship).unique_attributes == {"qualifiedName": parent_qn}
    for other in set(PARENTS) - {relationship}:
        assert getattr(sut, other) is UNSET
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    # Any one of the three parents satisfies creation validation; a dataset
    # column has no app, so the app qualifiedName must not be required.
    sut.validate(for_creation=True)


def test_create_alias():
    sut = QlikColumn.create(name=NAME, parent_qualified_name=DATASET_QN)

    assert sut.qualified_name.startswith(f"{DATASET_QN}/column/")


def test_space_is_optional():
    sut = QlikColumn.creator(name=NAME, parent_qualified_name=DATASET_QN)

    assert sut.qlik_space_id is UNSET
    assert sut.qlik_space_qualified_name is UNSET


def test_same_field_under_different_parents_gets_different_hashes():
    sheet_col = QlikColumn.creator(name=NAME, parent_qualified_name=SHEET_QN)
    chart_col = QlikColumn.creator(name=NAME, parent_qualified_name=CHART_QN)

    assert (
        sheet_col.qualified_name.rsplit("/", 1)[1]
        != (chart_col.qualified_name.rsplit("/", 1)[1])
    )


def test_column_without_parent_fails_creation_validation():
    sut = QlikColumn(
        name=NAME,
        qualified_name=f"{DATASET_QN}/column/abc",
        connection_qualified_name=CONNECTION_QN,
        qlik_space_qualified_name=SPACE_QN,
    )

    with pytest.raises(ValueError, match="one of qlik_sheet, qlik_chart, qlik_dataset"):
        sut.validate(for_creation=True)


@pytest.mark.parametrize("key", ["name", "parent_qualified_name"])
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    args = dict(name=NAME, parent_qualified_name=SHEET_QN)
    args[key] = blank

    with pytest.raises(ValueError, match=key):
        QlikColumn.creator(**args)


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"parent_qualified_name": APP_QN}, "parent_qualified_name must end in"),
        ({"parent_qualified_name": SPACE_QN}, "parent_qualified_name must end in"),
        ({"parent_qualified_name": CONNECTION_QN}, "parent_qualified_name must end in"),
        ({"space_qualified_name": DATASET_QN}, "space_qualified_name must end in"),
    ],
)
def test_creator_rejects_wrong_parent(overrides, message):
    args = dict(name=NAME, parent_qualified_name=SHEET_QN)
    args.update(overrides)

    with pytest.raises(ValueError, match=message):
        QlikColumn.creator(**args)


def test_updater():
    qn = f"{DATASET_QN}/column/8899bf1ab296301e5c10c37600324580"
    sut = QlikColumn.updater(qualified_name=qn, name=NAME)

    assert sut.qualified_name == qn
    assert sut.name == NAME


def test_trim_to_required():
    sut = QlikColumn.creator(name=NAME, parent_qualified_name=DATASET_QN)
    trimmed = sut.trim_to_required()

    assert trimmed.qualified_name == sut.qualified_name
    assert trimmed.name == NAME
    assert trimmed.qlik_dataset is UNSET
