# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Generator, Optional

import pytest
from pydantic import StrictStr

from pyatlan.cache.role_cache import RoleCache

import logging

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.group import AtlanGroup, CreateGroupResponse

LOGGER = logging.getLogger(__name__)

PREFIX = "psdk-Admin"
GROUP_NAME1 = f"{PREFIX}1"
GROUP_NAME2 = f"{PREFIX}2"

_default_group_count = 0
_group1_full: Optional[AtlanGroup] = None


def create_group(client: AtlanClient, name: str) -> CreateGroupResponse:
    g = AtlanGroup.create(alias=StrictStr(name))
    r = client.create_group(g)
    return r


def delete_group(client: AtlanClient, guid: str) -> None:
    client.purge_group(guid)


def test_retrieve_roles():
    admin_role_guid = RoleCache.get_id_for_name("$admin")
    assert admin_role_guid


@pytest.fixture(scope="module")
def group1(client: AtlanClient) -> Generator[CreateGroupResponse, None, None]:
    g = create_group(client, GROUP_NAME1)
    LOGGER.info(f"Created: {g}")
    yield g
    delete_group(client, g.group)


def test_create_group1(client: AtlanClient, group1: CreateGroupResponse):
    global _group1_full
    assert group1
    r = client.get_group_by_name(GROUP_NAME1)
    assert r
    assert len(r) == 1
    _group1_full = r[0]
    assert _group1_full
    assert _group1_full.path
    assert _group1_full.name
    assert _group1_full.id == group1.group
    assert _group1_full.attributes
    assert not _group1_full.attributes.description


def test_retrieve_all_groups(client: AtlanClient, group1: CreateGroupResponse):
    global _default_group_count
    groups = client.get_all_groups()
    assert groups
    assert len(groups) >= 1
    for group in groups:
        if group.is_default():
            _default_group_count += 1


@pytest.mark.order(after="test_create_group1")
def test_update_groups(client: AtlanClient, group1: CreateGroupResponse):
    groups = client.get_group_by_name(alias=GROUP_NAME1)
    assert groups
    assert len(groups) == 1
    group = groups[0]
    group.attributes = AtlanGroup.Attributes(description=["Now with a description!"])
    client.update_group(group)


# TODO: users and then group membership


@pytest.mark.order(after="test_update_groups")
def test_updated_groups(client: AtlanClient, group1: CreateGroupResponse):
    groups = client.get_group_by_name(alias=GROUP_NAME1)
    assert groups
    assert len(groups) == 1
    group = groups[0]
    assert group
    assert group.id == group1.group
    assert group.attributes
    assert group.attributes.description == ["Now with a description!"]
    # TODO: add user count check, once users are added
