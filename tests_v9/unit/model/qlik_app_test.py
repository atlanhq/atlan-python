# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for QlikApp.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-qlik-sense-app emits today
(app/transformers/qlik_sense_cloud.py, _transform_app), so a creator change that
would re-key existing Qlik assets fails here.
"""

import json

import pytest

from pyatlan_v9.model import QlikApp

CONNECTION_QN = "default/qlik-sense/1712345678"
SPACE_QN = "default/qlik-sense/1712345678/space/sp01"
STREAM_QN = "default/qlik-sense/1712345678/stream/st01"
NAME = "Sales"
EXPECTED_QN = "default/qlik-sense/1712345678/app/a1b2"


def _creator(**overrides):
    args = dict(name=NAME, qlik_id="a1b2", space_qualified_name=SPACE_QN)
    args.update(overrides)
    return QlikApp.creator(**args)


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.qlik_id == "a1b2"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    assert sut.qlik_space_id == "sp01"
    assert sut.qlik_space_qualified_name == SPACE_QN
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = QlikApp.create(name=NAME, qlik_id="a1b2", space_qualified_name=SPACE_QN)

    assert sut.qualified_name == EXPECTED_QN


@pytest.mark.parametrize(
    "space_qn, space_type, space_id",
    [(SPACE_QN, "QlikSpace", "sp01"), (STREAM_QN, "QlikStream", "st01")],
)
def test_creator_sets_space_or_stream_parent(space_qn, space_type, space_id):
    sut = _creator(space_qualified_name=space_qn)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.qlik_space_id == space_id
    assert sut.qlik_space_qualified_name == space_qn
    assert sut.qlik_space.type_name == space_type
    assert sut.qlik_space.unique_attributes == {"qualifiedName": space_qn}


def test_app_in_stream_serializes_stream_relationship(serde):
    data = json.loads(
        _creator(space_qualified_name=STREAM_QN).to_json(nested=True, serde=serde)
    )

    space = data["relationshipAttributes"]["qlikSpace"]
    assert space["typeName"] == "QlikStream"
    assert space["uniqueAttributes"] == {"qualifiedName": STREAM_QN}


@pytest.mark.parametrize("key", ["name", "qlik_id", "space_qualified_name"])
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    with pytest.raises(ValueError, match=key):
        _creator(**{key: blank})


@pytest.mark.parametrize("space_qn", [CONNECTION_QN, EXPECTED_QN])
def test_creator_rejects_wrong_parent(space_qn):
    with pytest.raises(ValueError, match="space_qualified_name must end in"):
        _creator(space_qualified_name=space_qn)


def test_updater():
    sut = QlikApp.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
