# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import logging
from typing import Generator, Type

import pytest

from pyatlan.client.atlan import DEFAULT_RETRY, AtlanClient
from pyatlan.model.enums import AtlanDeleteType
from pyatlan.model.response import A

LOGGER = logging.getLogger(__name__)


class TestId:
    # Mirrors :class:`pyatlan.test_utils.TestId` — kept in sync so a
    # value passed to ``AtlanConnectorType.CREATE_CUSTOM`` matches the
    # platform's ``^[a-z0-9-]+$`` connectorType slug rule (BLDX-1294 /
    # ATLAN-PYTHON-400-079). Lowercase alphanumeric session_id + hyphen
    # separators + lowercased+hyphenated input.
    from nanoid import generate as generate_nanoid  # type: ignore

    session_id = generate_nanoid(
        alphabet="1234567890abcdefghijklmnopqrstuvwxyz",
        size=5,
    )

    @classmethod
    def make_unique(cls, input: str):
        """See :meth:`pyatlan.test_utils.TestId.make_unique`."""
        slug = input.lower().replace("_", "-")
        return f"psdk-{slug}-{cls.session_id}"


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
