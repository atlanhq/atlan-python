# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for QlikStream.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-qlik-sense-app emits today for a Qlik Sense
Enterprise on Windows stream (_transform_space with isStream), so a creator change
that would re-key existing Qlik assets fails here.
"""

import pytest

from pyatlan_v9.model import QlikStream

CONNECTION_QN = "default/qlik-sense/1712345678"
NAME = "Everyone"
EXPECTED_QN = "default/qlik-sense/1712345678/stream/st01"


def _creator(**overrides):
    args = dict(name=NAME, connection_qualified_name=CONNECTION_QN, qlik_id="st01")
    args.update(overrides)
    return QlikStream.creator(**args)


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.qlik_id == "st01"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "qlik-sense"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_create_alias():
    sut = QlikStream.create(
        name=NAME, connection_qualified_name=CONNECTION_QN, qlik_id="st01"
    )

    assert sut.qualified_name == EXPECTED_QN


@pytest.mark.parametrize("key", ["name", "connection_qualified_name", "qlik_id"])
@pytest.mark.parametrize("blank", [None, "", "  "])
def test_creator_rejects_blank_inputs(key, blank):
    with pytest.raises(ValueError, match=key):
        _creator(**{key: blank})


def test_updater():
    sut = QlikStream.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
