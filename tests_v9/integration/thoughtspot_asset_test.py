# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    ThoughtspotAnswer,
    ThoughtspotDashlet,
    ThoughtspotLiveboard,
    ThoughtspotTable,
    ThoughtspotView,
    ThoughtspotWorksheet,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("THOUGHTSPOT")

FLAT_TYPES = [
    (ThoughtspotTable, ThoughtspotTable.creator, "tables"),
    (ThoughtspotView, ThoughtspotView.creator, "views"),
    (ThoughtspotWorksheet, ThoughtspotWorksheet.creator, "worksheets"),
    (ThoughtspotAnswer, ThoughtspotAnswer.creator, "answers"),
]


def _thoughtspot_id(slug: str) -> str:
    return f"i{slug}{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.THOUGHTSPOT
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def flat_assets(
    client: AtlanClient, connection: Connection
) -> Generator[dict, None, None]:
    created = {}
    for asset_type, creator, slug in FLAT_TYPES:
        to_create = creator(
            name=f"{slug}_{MODULE_NAME}",
            thoughtspot_id=_thoughtspot_id(slug),
            connection_qualified_name=connection.qualified_name,
        )
        created[asset_type] = client.asset.save(to_create).assets_created(
            asset_type=asset_type
        )[0]
    yield created
    for asset_type, asset in created.items():
        delete_asset(client, guid=asset.guid, asset_type=asset_type)


@pytest.fixture(scope="module")
def liveboard(
    client: AtlanClient, connection: Connection
) -> Generator[ThoughtspotLiveboard, None, None]:
    to_create = ThoughtspotLiveboard.creator(
        name=f"liveboards_{MODULE_NAME}",
        thoughtspot_id=_thoughtspot_id("liveboards"),
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=ThoughtspotLiveboard
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ThoughtspotLiveboard)


@pytest.fixture(scope="module")
def dashlet(
    client: AtlanClient, liveboard: ThoughtspotLiveboard
) -> Generator[ThoughtspotDashlet, None, None]:
    to_create = ThoughtspotDashlet.creator(
        name=f"dashlets_{MODULE_NAME}",
        thoughtspot_id=_thoughtspot_id("dashlets"),
        thoughtspot_liveboard_qualified_name=liveboard.qualified_name,
        thoughtspot_liveboard_name=liveboard.name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=ThoughtspotDashlet)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ThoughtspotDashlet)


def _assert_retrieved(client, asset, asset_type, connection, slug):
    assert asset.guid
    retrieved = client.asset.get_by_qualified_name(
        f"{connection.qualified_name}/{slug}/{_thoughtspot_id(slug)}",
        asset_type=asset_type,
        ignore_relationships=False,
    )
    assert retrieved.guid == asset.guid
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.THOUGHTSPOT
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_flat_assets(client: AtlanClient, connection: Connection, flat_assets: dict):
    for asset_type, _, slug in FLAT_TYPES:
        _assert_retrieved(client, flat_assets[asset_type], asset_type, connection, slug)


def test_liveboard(
    client: AtlanClient, connection: Connection, liveboard: ThoughtspotLiveboard
):
    _assert_retrieved(client, liveboard, ThoughtspotLiveboard, connection, "liveboards")


def test_dashlet(
    client: AtlanClient,
    connection: Connection,
    liveboard: ThoughtspotLiveboard,
    dashlet: ThoughtspotDashlet,
):
    retrieved = _assert_retrieved(
        client, dashlet, ThoughtspotDashlet, connection, "dashlets"
    )
    assert retrieved.thoughtspot_liveboard.guid == liveboard.guid
    assert retrieved.thoughtspot_liveboard_name == liveboard.name
    assert retrieved.thoughtspot_liveboard_qualified_name == liveboard.qualified_name
