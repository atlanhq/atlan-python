# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for QlikChart.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-qlik-sense-app emits today
(app/transformers/qlik_sense_cloud.py, _transform_chart). A chart's qualifiedName
hangs off its app, not its sheet, so a creator change that would re-key existing
Qlik assets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import QlikChart

CONNECTION_QN = "default/qlik-sense/1712345678"
STREAM_QN = "default/qlik-sense/1712345678/stream/st01"
APP_QN = "default/qlik-sense/1712345678/app/a1b2"
SHEET_QN = "default/qlik-sense/1712345678/app/a1b2/sheet/sh01"
NAME = "Revenue by region"
EXPECTED_QN = "default/qlik-sense/1712345678/app/a1b2/chart/ch01"


def _creator(**overrides):
    args = dict(
        name=NAME,
        qlik_id="ch01",
        sheet_qualified_name=SHEET_QN,
        space_qualified_name=STREAM_QN,
    )
    args.update(overrides)
    return QlikChart.creator(**args)


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.qlik_id == "ch01"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    assert sut.qlik_app_id == "a1b2"
    assert sut.qlik_app_qualified_name == APP_QN
    assert sut.qlik_space_id == "st01"
    assert sut.qlik_space_qualified_name == STREAM_QN
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = QlikChart.create(name=NAME, qlik_id="ch01", sheet_qualified_name=SHEET_QN)

    assert sut.qualified_name == EXPECTED_QN


def test_creator_sets_parent():
    assert _creator().qlik_sheet.unique_attributes == {"qualifiedName": SHEET_QN}


def test_space_is_optional():
    sut = _creator(space_qualified_name=None)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.qlik_space_id is UNSET
    assert sut.qlik_space_qualified_name is UNSET


@pytest.mark.parametrize("key", ["name", "qlik_id", "sheet_qualified_name"])
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    with pytest.raises(ValueError, match=key):
        _creator(**{key: blank})


@pytest.mark.parametrize(
    "sheet_qn", [APP_QN, EXPECTED_QN, f"{CONNECTION_QN}/dataset/ds01"]
)
def test_creator_rejects_wrong_parent(sheet_qn):
    with pytest.raises(ValueError, match="sheet_qualified_name must end in"):
        _creator(sheet_qualified_name=sheet_qn)


def test_updater():
    sut = QlikChart.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.qlik_sheet is UNSET
