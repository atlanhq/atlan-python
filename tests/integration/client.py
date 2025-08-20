# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
from typing import Generator, Type

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import AtlanDeleteType
from pyatlan.model.response import A
from pyatlan.client.atlan import DEFAULT_RETRY

LOGGER = logging.getLogger(__name__)


class TestId:
    from nanoid import generate as generate_nanoid  # type: ignore

    session_id = generate_nanoid(
        alphabet="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        size=5,
    )

    @classmethod
    def make_unique(cls, input: str):
        return f"psdk_{input}_{cls.session_id}"


@pytest.fixture(scope="module")
def client() -> Generator[AtlanClient, None, None]:
    client = AtlanClient()

    yield client


@pytest.fixture(scope="module")
def token_client() -> Generator[AtlanClient, None, None]:
    DEFAULT_RETRY.total = 0
    client = AtlanClient(retry=DEFAULT_RETRY)
    yield client


def delete_asset(
    client: AtlanClient,
    asset_type: Type[A],
    guid: str,
    delete_type: AtlanDeleteType = AtlanDeleteType.PURGE,
) -> None:
    # These assertions check the cleanup actually worked
    r = client.asset.purge_by_guid(guid, delete_type)
    s = r is not None
    s = s and len(r.assets_deleted(asset_type)) == 1
    s = s and r.assets_deleted(asset_type)[0].guid == guid
    if not s:
        LOGGER.error(f"Failed to remove {asset_type} with GUID {guid}.")
