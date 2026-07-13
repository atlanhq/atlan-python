# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
"""Unit tests for AtlanTagRetranslator tag name → ID resolution (BLDX-1530).

On a write/serialization path, a user-supplied tag name that does not resolve in
the tag cache must raise a clear client-side NotFoundError naming the tag —
rather than substituting the ``(DELETED)`` sentinel, which Atlas rejects with an
opaque ``Given classification (DELETED) was invalid``. The sentinel itself is
preserved so an asset read with an already-deleted tag round-trips losslessly.
"""

from unittest.mock import MagicMock

import pytest

from pyatlan.errors import NotFoundError
from pyatlan.model.constants import DELETED_
from pyatlan.model.retranslators import AtlanTagRetranslator


def _retranslator(name_to_id):
    client = MagicMock()
    client.atlan_tag_cache.get_id_for_name.side_effect = lambda name: name_to_id.get(
        name
    )
    client.atlan_tag_cache.get_source_tags_attr_id.return_value = None
    return AtlanTagRetranslator(client)


def test_resolves_existing_tag_name_to_id():
    retranslator = _retranslator({"PII": "abc123"})
    out = retranslator.retranslate({"classifications": [{"typeName": "PII"}]})
    assert out["classifications"][0]["typeName"] == "abc123"


def test_missing_tag_raises_named_not_found():
    # The reported bug: add_atlan_tags(["Alert: DQ"]) on a tenant without that tag
    # used to ship (DELETED) and get an opaque Atlas error. Now it fails fast with
    # a clear, named client-side error and never leaks the sentinel.
    retranslator = _retranslator({})
    with pytest.raises(NotFoundError) as exc:
        retranslator.retranslate(
            {"addOrUpdateClassifications": [{"typeName": "Alert: DQ"}]}
        )
    message = str(exc.value)
    assert "Alert: DQ" in message
    assert "ATLAN-PYTHON-404-006" in message
    assert DELETED_ not in message


def test_remove_missing_tag_also_raises():
    retranslator = _retranslator({})
    with pytest.raises(NotFoundError):
        retranslator.retranslate({"removeClassifications": [{"typeName": "GhostTag"}]})


def test_deleted_sentinel_round_trip_is_preserved():
    # An asset READ with an already-deleted tag surfaces (DELETED); re-serializing
    # it must stay lossless (no raise, sentinel preserved).
    retranslator = _retranslator({})
    out = retranslator.retranslate({"classifications": [{"typeName": DELETED_}]})
    assert out["classifications"][0]["typeName"] == DELETED_


def test_names_path_policy_serde_stays_tolerant():
    # purpose/persona *policy* names intentionally tolerate unresolvable tags
    # (they round-trip through the sentinel), so this path does not raise.
    retranslator = _retranslator({})
    out = retranslator.retranslate({"purposeClassifications": ["ghost-policy-tag"]})
    assert out["purposeClassifications"] == [DELETED_]
