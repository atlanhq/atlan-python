# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
from typing import Callable, Type

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.response import A

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def make_unique() -> Callable[[str], str]:
    from nanoid import generate as generate_nanoid

    session_id = generate_nanoid(
        alphabet="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        size=5,
    )

    def _get_unique_name(input: str) -> str:
        return f"psdk_{input}_{session_id}"

    return _get_unique_name


@pytest.fixture(scope="module")
def client() -> AtlanClient:
    client = AtlanClient()
    client.register_client(client)

    yield client

    AtlanClient.reset_default_client()


def delete_asset(client: AtlanClient, asset_type: Type[A], guid: str) -> None:
    # These assertions check the cleanup actually worked
    r = client.purge_entity_by_guid(guid)
    s = r is not None
    s = s and len(r.assets_deleted(asset_type)) == 1
    s = s and r.assets_deleted(asset_type)[0].guid == guid
    if not s:
        LOGGER.error(f"Failed to remove {asset_type} with GUID {guid}.")
