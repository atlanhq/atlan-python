# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Callable, Generator, Optional

import pytest
from pydantic import StrictStr

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.group import AtlanGroup, CreateGroupResponse
from pyatlan.model.user import AtlanUser

MODULE_NAME = "Admin"
EMAIL_DOMAIN = "@example.com"

_default_group_count: int = 0


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
def group1(
    client: AtlanClient, make_unique: Callable[[str], str]
) -> Generator[CreateGroupResponse, None, None]:
    group_name = make_unique(f"{MODULE_NAME}1")
    g = create_group(client, group_name)
    yield g
    delete_group(client, g.group)


def test_create_group1(
    client: AtlanClient, make_unique: Callable[[str], str], group1: CreateGroupResponse
):
    assert group1
    group_name = make_unique(f"{MODULE_NAME}1")
    r = client.get_group_by_name(group_name)
    assert r
    assert len(r) == 1
    group1_full = r[0]
    assert group1_full
    assert group1_full.path
    assert group1_full.name
    assert group1_full.id == group1.group
    assert group1_full.attributes
    assert not group1_full.attributes.description


def test_retrieve_all_groups(
    client: AtlanClient, make_unique: Callable[[str], str], group1: CreateGroupResponse
):
    global _default_group_count
    groups = client.get_all_groups()
    assert groups
    assert len(groups) >= 1
    for group in groups:
        if group.is_default():
            _default_group_count += 1


@pytest.mark.order(after="test_create_group1")
def test_update_groups(
    client: AtlanClient, make_unique: Callable[[str], str], group1: CreateGroupResponse
):
    group_name = make_unique(f"{MODULE_NAME}1")
    groups = client.get_group_by_name(alias=group_name)
    assert groups
    assert len(groups) == 1
    group = groups[0]
    group.attributes = AtlanGroup.Attributes(description=["Now with a description!"])
    client.update_group(group)


def _get_user1_from_list(
    users: list[AtlanUser], make_unique: Callable[[str], str]
) -> Optional[AtlanUser]:
    username = make_unique(f"{MODULE_NAME}1")
    user_email = f"{username}{EMAIL_DOMAIN}".lower()
    return next((user for user in users if user.email == user_email), None)


def _get_user2_from_list(
    users: list[AtlanUser], make_unique: Callable[[str], str]
) -> Optional[AtlanUser]:
    username = make_unique(f"{MODULE_NAME}2")
    user_email = f"{username}{EMAIL_DOMAIN}".lower()
    return next((user for user in users if user.email == user_email), None)


def _get_user3_from_list(
    users: list[AtlanUser], make_unique: Callable[[str], str]
) -> Optional[AtlanUser]:
    username = make_unique(f"{MODULE_NAME}3")
    user_email = f"{username}{EMAIL_DOMAIN}".lower()
    return next((user for user in users if user.email == user_email), None)


@pytest.fixture(scope="module")
def users(
    client: AtlanClient, make_unique: Callable[[str], str]
) -> Generator[list[AtlanUser], None, None]:
    username1 = make_unique(f"{MODULE_NAME}1")
    username2 = make_unique(f"{MODULE_NAME}2")
    username3 = make_unique(f"{MODULE_NAME}3")
    user_email1 = f"{username1}{EMAIL_DOMAIN}"
    user_email2 = f"{username2}{EMAIL_DOMAIN}"
    user_email3 = f"{username3}{EMAIL_DOMAIN}"
    users: list[AtlanUser] = [
        AtlanUser.create(email=user_email1, role_name="$guest"),
        AtlanUser.create(email=user_email2, role_name="$guest"),
        AtlanUser.create(email=user_email3, role_name="$guest"),
    ]
    client.create_users(users=users)
    created = client.get_users_by_email(email=EMAIL_DOMAIN)
    assert created  # must be here for mypy
    yield created
    for user in created:
        client.purge_user(str(user.id))


@pytest.mark.order(after="test_retrieve_all_groups")
def test_retrieve_users(
    client: AtlanClient, make_unique: Callable[[str], str], users: list[AtlanUser]
):
    global _default_group_count
    all_users = client.get_all_users()
    assert all_users
    assert len(all_users) >= 3
    username = make_unique(f"{MODULE_NAME}1")
    user_email1 = f"{username}{EMAIL_DOMAIN}"
    users_list = client.get_users_by_email(user_email1)
    assert users_list
    assert len(users_list) == 1
    user1 = users_list[0]
    assert user1
    assert user1.id
    assert user1.attributes
    assert not user1.attributes.designation
    assert user1.group_count == _default_group_count
    users_list = client.get_users_by_email(EMAIL_DOMAIN)
    assert users_list
    assert len(users_list) == 3
    assert _get_user1_from_list(users, make_unique)
    assert _get_user2_from_list(users, make_unique)
    assert _get_user3_from_list(users, make_unique)


@pytest.fixture(scope="module")
def group2(
    client: AtlanClient, make_unique: Callable[[str], str], users: list[AtlanUser]
) -> Generator[CreateGroupResponse, None, None]:
    group_name = make_unique(f"{MODULE_NAME}2")
    to_create = AtlanGroup.create(group_name)
    user2 = _get_user2_from_list(users, make_unique)
    assert user2  # must be here for mypy
    user3 = _get_user3_from_list(users, make_unique)
    assert user3  # must be here for mypy
    g = client.create_group(group=to_create, user_ids=[str(user2.id), str(user3.id)])
    yield g
    delete_group(client, g.group)


def test_create_group2(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    users: list[AtlanUser],
    group2: CreateGroupResponse,
):
    assert group2
    assert group2.group
    mapped_users = group2.users
    assert mapped_users
    user2 = _get_user2_from_list(users, make_unique)
    assert user2
    assert user2.id in mapped_users.keys()
    user_status = mapped_users.get(str(user2.id))
    assert user_status
    assert user_status.was_successful()
    user3 = _get_user3_from_list(users, make_unique)
    assert user3
    assert user3.id in mapped_users.keys()
    user_status = mapped_users.get(str(user3.id))
    assert user_status
    assert user_status.was_successful()
    group_name = make_unique(f"{MODULE_NAME}2")
    r = client.get_group_by_name(group_name)
    assert r
    assert len(r) == 1
    group2_full = r[0]
    assert group2_full
    assert group2_full.path
    assert group2_full.name
    assert group2_full.id == group2.group
    assert group2_full.attributes
    assert not group2_full.attributes.description


@pytest.mark.order(after="test_retrieve_all_groups")
def test_update_users(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    users: list[AtlanUser],
    group1: CreateGroupResponse,
    group2: CreateGroupResponse,
):
    global _default_group_count
    user1 = _get_user1_from_list(users, make_unique)
    assert user1
    assert user1.id
    client.add_user_to_groups(guid=user1.id, group_ids=[group1.group])
    client.change_user_role(
        guid=user1.id, role_id=str(RoleCache.get_id_for_name("$member"))
    )
    response = client.get_groups_for_user(guid=user1.id)
    assert response
    assert response.records
    assert len(response.records) == 1 + _default_group_count


@pytest.mark.order(after="test_update_users")
def test_updated_users(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    users: list[AtlanUser],
    group1: CreateGroupResponse,
    group2: CreateGroupResponse,
):
    global _default_group_count
    username = make_unique(f"{MODULE_NAME}1")
    user_email = f"{username}{EMAIL_DOMAIN}"
    candidates = client.get_users_by_email(user_email)
    assert candidates
    assert len(candidates) == 1
    one = candidates[0]
    assert one
    user1 = _get_user1_from_list(users, make_unique)
    assert user1
    assert one.id == user1.id
    assert one.group_count == 1 + _default_group_count
    group_name = make_unique(f"{MODULE_NAME}1")
    guest = client.get_user_by_username(group_name.lower())
    assert guest
    assert guest == one


@pytest.mark.order(after=["test_update_groups", "test_update_users"])
def test_updated_groups(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    users: list[AtlanUser],
    group1: CreateGroupResponse,
    group2: CreateGroupResponse,
):
    group_name = make_unique(f"{MODULE_NAME}1")
    groups = client.get_group_by_name(alias=group_name)
    assert groups
    assert len(groups) == 1
    group = groups[0]
    assert group
    assert group.id == group1.group
    assert group.attributes
    assert group.attributes.description == ["Now with a description!"]
    assert group.user_count == 1


@pytest.mark.order(after="test_updated_groups")
def test_remove_user_from_group(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    users: list[AtlanUser],
    group1: CreateGroupResponse,
    group2: CreateGroupResponse,
):
    group_name = make_unique(f"{MODULE_NAME}1")
    groups = client.get_group_by_name(alias=group_name)
    assert groups
    assert len(groups) == 1
    group = groups[0]
    assert group.id
    user1 = _get_user1_from_list(users, make_unique)
    assert user1
    assert user1.id
    client.remove_users_from_group(guid=group.id, user_ids=[user1.id])
    response = client.get_group_members(guid=group.id)
    assert response
    assert not response.records


@pytest.mark.order(after="test_remove_user_from_group")
def test_final_user_state(
    client: AtlanClient,
    make_unique: Callable[[str], str],
    users: list[AtlanUser],
    group1: CreateGroupResponse,
    group2: CreateGroupResponse,
):
    global _default_group_count
    user1 = _get_user1_from_list(users, make_unique)
    assert user1
    assert user1.id
    response = client.get_groups_for_user(user1.id)
    assert (
        response.records is None
        or len(response.records) == 0
        or len(response.records) == _default_group_count
    )
