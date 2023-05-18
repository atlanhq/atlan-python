# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
from typing import Type

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.response import A

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="module", autouse=True)
def client() -> AtlanClient:
    return AtlanClient()


def delete_asset(client: AtlanClient, asset_type: Type[A], guid: str) -> None:
    # These assertions check the cleanup actually worked
    r = client.purge_entity_by_guid(guid)
    s = r is not None
    s = s and len(r.assets_deleted(asset_type)) == 1
    s = s and r.assets_deleted(asset_type)[0].guid == guid
    if not s:
        LOGGER.error(f"Failed to remove {asset_type} with GUID {guid}.")
