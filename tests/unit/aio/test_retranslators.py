# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
"""Async unit tests for AsyncAtlanTagRetranslator tag name → ID resolution (BLDX-1530).

Mirrors tests/unit/test_retranslators.py for the async retranslator.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from pyatlan.errors import NotFoundError
from pyatlan.model.aio.retranslators import AsyncAtlanTagRetranslator
from pyatlan.model.constants import DELETED_


def _retranslator(name_to_id):
    client = MagicMock()
    client.atlan_tag_cache.get_id_for_name = AsyncMock(
        side_effect=lambda name: name_to_id.get(name)
    )
    client.atlan_tag_cache.get_source_tags_attr_id = AsyncMock(return_value=None)
    return AsyncAtlanTagRetranslator(client)


async def test_resolves_existing_tag_name_to_id():
    retranslator = _retranslator({"PII": "abc123"})
    out = await retranslator.retranslate({"classifications": [{"typeName": "PII"}]})
    assert out["classifications"][0]["typeName"] == "abc123"


async def test_missing_tag_raises_named_not_found():
    retranslator = _retranslator({})
    with pytest.raises(NotFoundError) as exc:
        await retranslator.retranslate(
            {"addOrUpdateClassifications": [{"typeName": "Alert: DQ"}]}
        )
    message = str(exc.value)
    assert "Alert: DQ" in message
    assert "ATLAN-PYTHON-404-006" in message
    assert DELETED_ not in message


async def test_deleted_sentinel_round_trip_is_preserved():
    retranslator = _retranslator({})
    out = await retranslator.retranslate({"classifications": [{"typeName": DELETED_}]})
    assert out["classifications"][0]["typeName"] == DELETED_
