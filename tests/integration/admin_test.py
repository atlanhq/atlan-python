# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from datetime import datetime, timedelta
from typing import Generator

import pytest
from pydantic.v1 import StrictStr

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.group import AtlanGroup, CreateGroupResponse, GroupRequest
from pyatlan.model.keycloak_events import AdminEventRequest, KeycloakEventRequest
from pyatlan.model.user import UserRequest
from tests.integration.client import TestId

FIXED_USER = "aryaman.bhushan"
TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
MODULE_NAME = TestId.make_unique("Admin")
GROUP_NAME = f"{MODULE_NAME}"

EMAIL_DOMAIN = "@atlan.com"

_default_group_count: int = 0


def create_group(client: AtlanClient, name: str) -> CreateGroupResponse:
    g = AtlanGroup.create(alias=StrictStr(name))
    r = client.group.create(g)
    return r


def delete_group(client: AtlanClient, guid: str) -> None:
    client.group.purge(guid)


def test_retrieve_roles(client: AtlanClient):
    admin_role_guid = RoleCache.get_id_for_name("$admin")
    assert admin_role_guid


@pytest.fixture(scope="module")
def group(client: AtlanClient) -> Generator[CreateGroupResponse, None, None]:
    to_create = AtlanGroup.create(GROUP_NAME)
    fixed_user = client.user.get_by_username(FIXED_USER)
    assert fixed_user
    g = client.group.create(group=to_create, user_ids=[str(fixed_user.id)])
    yield g
    delete_group(client, g.group)


def test_create_group(client: AtlanClient, group: CreateGroupResponse):
    assert group
    r = client.group.get_by_name(GROUP_NAME)
    assert r
    assert len(r) == 1
    group1_full = r[0]
    assert group1_full
    assert group1_full.path
    assert group1_full.name
    assert group1_full.id == group.group
    assert group1_full.attributes
    assert not group1_full.attributes.description
    mapped_users = group.users
    assert mapped_users
    fixed_user = client.user.get_by_username(FIXED_USER)
    assert fixed_user
    assert fixed_user.id in mapped_users.keys()
    user_status = mapped_users.get(str(fixed_user.id))
    assert user_status
    assert user_status.was_successful()


def test_retrieve_all_groups(client: AtlanClient, group: CreateGroupResponse):
    global _default_group_count
    groups = client.group.get_all()
    assert groups
    assert len(groups) >= 1
    for group1 in groups:
        if group1.is_default():
            _default_group_count += 1


def test_group_get_pagination(client: AtlanClient, group: CreateGroupResponse):
    response = client.group.get(limit=1)

    assert response
    assert response.total_record is not None
    assert response.total_record >= 1
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 1
    for test_group in response:
        assert test_group.id
        assert test_group.name
        assert test_group.path
        assert test_group.attributes
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 0


def test_group_get_members_pagination(client: AtlanClient, group: CreateGroupResponse):
    groups = client.group.get_by_name(alias=GROUP_NAME)
    assert groups
    assert len(groups) == 1
    group1 = groups[0]
    assert group1.id
    response = client.group.get_members(guid=group1.id, request=UserRequest(limit=1))

    assert response
    assert response.total_record is not None
    assert response.total_record >= 1
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 1
    for test_user in response:
        assert test_user.username
        assert test_user.email
        assert test_user.attributes
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 0


def test_user_list_pagination(client: AtlanClient, group: CreateGroupResponse):
    response = client.user.get(limit=1)

    assert response
    assert response.total_record is not None
    assert response.total_record > 1
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 1
    for test_user in response:
        assert test_user.username
        assert test_user.email
        assert test_user.attributes
        assert test_user.login_events is not None
        assert len(test_user.login_events) >= 0
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 0


def test_user_groups_pagination(client: AtlanClient, group: CreateGroupResponse):
    fixed_user = client.user.get_by_username(FIXED_USER)
    assert fixed_user
    assert fixed_user.id
    response = client.user.get_groups(guid=fixed_user.id, request=GroupRequest(limit=1))

    assert response
    assert response.total_record is not None
    assert response.total_record >= 1
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 1
    for test_group in response:
        assert test_group.id
        assert test_group.name
        assert test_group.path
        assert test_group.attributes
    current_page = response.current_page()
    assert current_page is not None
    assert len(current_page) == 0


@pytest.mark.order(after="test_retrieve_all_groups")
def test_retrieve_existing_user(client: AtlanClient, group: CreateGroupResponse):
    global _default_group_count
    all_users = client.user.get_all()
    assert all_users
    assert len(all_users) >= 1
    user1 = client.user.get_by_username(FIXED_USER)
    assert user1
    assert user1.id
    assert user1.attributes
    assert user1.group_count == 1 + _default_group_count
    response = client.user.get_by_usernames(usernames=[FIXED_USER])
    assert response
    assert len(response) == 1
    fixed_user = response[0]
    assert fixed_user
    assert fixed_user.id
    users_list = client.user.get_by_usernames(usernames=[])
    assert users_list == []
    users_list = client.user.get_by_email(EMAIL_DOMAIN)
    assert users_list
    assert len(users_list) >= 1
    email = user1.email
    assert email
    users_list = client.user.get_by_email(email)
    assert users_list
    assert len(users_list) == 1
    assert user1.email == users_list[0].email
    assert user1.username == users_list[0].username
    assert user1.attributes == users_list[0].attributes
    users_list = client.user.get_by_emails(emails=[email])
    assert users_list
    assert len(users_list) == 1
    assert user1.email == users_list[0].email
    assert user1.username == users_list[0].username
    assert user1.attributes == users_list[0].attributes
    users_list = client.user.get_by_emails(emails=[])
    assert users_list == []


@pytest.mark.order(after="test_create_group")
def test_update_groups(client: AtlanClient, group: CreateGroupResponse):
    groups = client.group.get_by_name(alias=GROUP_NAME)
    assert groups
    assert len(groups) == 1
    group1 = groups[0]
    group1.attributes = AtlanGroup.Attributes(description=["Now with a description!"])
    client.group.update(group1)


@pytest.mark.order(after=["test_update_groups", "test_update_users"])
def test_updated_groups(
    client: AtlanClient,
    group: CreateGroupResponse,
):
    groups = client.group.get_by_name(alias=GROUP_NAME)
    assert groups
    assert len(groups) == 1
    group1 = groups[0]
    assert group1
    assert group1.id == group.group
    assert group1.attributes
    assert group1.attributes.description == ["Now with a description!"]
    assert group1.user_count == 1


@pytest.mark.order(after="test_updated_groups")
def test_remove_user_from_group(
    client: AtlanClient,
    group: CreateGroupResponse,
):
    groups = client.group.get_by_name(alias=GROUP_NAME)
    assert groups
    assert len(groups) == 1
    group1 = groups[0]
    assert group1.id
    fixed_user = client.user.get_by_username(FIXED_USER)
    assert fixed_user
    assert fixed_user.id
    client.group.remove_users(guid=group1.id, user_ids=[fixed_user.id])
    response = client.group.get_members(guid=group1.id)
    assert response
    assert not response.records


@pytest.mark.order(after="test_remove_user_from_group")
def test_final_user_state(
    client: AtlanClient,
    group: CreateGroupResponse,
):
    global _default_group_count
    fixed_user = client.user.get_by_username(FIXED_USER)
    assert fixed_user
    assert fixed_user.id
    response = client.user.get_groups(fixed_user.id)
    assert (
        response.records is None
        or len(response.records) == 0
        or len(response.records) == _default_group_count
    )


@pytest.mark.order(after="test_final_user_state")
def test_retrieve_logs(
    client: AtlanClient,
):
    request = KeycloakEventRequest(date_from=YESTERDAY, date_to=TODAY)
    events = client.admin.get_keycloak_events(request)
    assert events
    count = 0
    for _ in events:
        count += 1
        if count >= 1000:
            break
    assert count > 0


@pytest.mark.order(after="test_final_user_state")
def test_retrieve_admin_logs(
    client: AtlanClient,
):
    request = AdminEventRequest(date_from=YESTERDAY, date_to=TODAY)
    events = client.admin.get_admin_events(request)
    assert events
    count = 0
    for _ in events:
        count += 1
        if count >= 1000:
            break
    assert count > 0
