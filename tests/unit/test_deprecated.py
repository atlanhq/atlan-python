# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.group import GroupClient
from pyatlan.client.role import RoleClient
from pyatlan.client.token import TokenClient
from pyatlan.client.typedef import TypeDefClient
from pyatlan.client.user import UserClient
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory, AtlasGlossaryTerm
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import TypeDef
from pyatlan.model.user import AtlanUser
from tests.unit.model.constants import (
    GLOSSARY_CATEGORY_NAME,
    GLOSSARY_NAME,
    GLOSSARY_TERM_NAME,
)

GLOSSARY = AtlasGlossary.create(name=GLOSSARY_NAME)
GLOSSARY_CATEGORY = AtlasGlossaryCategory.create(
    name=GLOSSARY_CATEGORY_NAME, anchor=GLOSSARY
)
GLOSSARY_TERM = AtlasGlossaryTerm.create(name=GLOSSARY_TERM_NAME, anchor=GLOSSARY)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")


@pytest.fixture()
def client():
    return AtlanClient()


@patch.object(GroupClient, "get")
def test_get_groups(mock_group_client, client: AtlanClient):
    limit = 1
    post_filter = "post"
    sort = "sort"
    count = False
    offset = 3
    client.get_groups(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )

    mock_group_client.assert_called_once_with(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )


@patch.object(GroupClient, "get_all")
def test_get_all_groupss(mock_group_client, client: AtlanClient):
    limit = 1
    client.get_all_groups(limit=limit)

    mock_group_client.assert_called_once_with(limit=limit)


@patch.object(GroupClient, "get_by_name")
def test_get_group_by_name(mock_group_client, client: AtlanClient):
    alias = "bob"
    limit = 3
    client.get_group_by_name(alias=alias, limit=limit)

    mock_group_client.assert_called_once_with(alias=alias, limit=limit)


@patch.object(GroupClient, "get_members")
def test_get_get_group_members(mock_group_client, client: AtlanClient):
    guid = "123"
    client.get_group_members(guid=guid)

    mock_group_client.assert_called_once_with(guid=guid)


@patch.object(GroupClient, "remove_users")
def test_remove_users_from_group(mock_group_client, client: AtlanClient):
    guid = "123"
    user_ids = ["456", "789"]
    client.remove_users_from_group(guid=guid, user_ids=user_ids)

    mock_group_client.assert_called_once_with(guid=guid, user_ids=user_ids)


@patch.object(RoleClient, "get")
def test_get_roles(mock_role_client, client: AtlanClient):
    limit = 1
    post_filter = "post"
    sort = "sort"
    count = False
    offset = 3

    client.get_roles(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )

    mock_role_client.assert_called_once_with(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )


@patch.object(RoleClient, "get_all")
def test_get_all_roles(mock_role_client, client: AtlanClient):
    client.get_all_roles()

    mock_role_client.assert_called_once()


@patch.object(TokenClient, "get")
def test_get_api_tokens(mock_token_client, client: AtlanClient):
    limit = 1
    post_filter = "post"
    sort = "sort"
    count = False
    offset = 3

    client.get_api_tokens(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )

    mock_token_client.assert_called_once_with(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )


@patch.object(TokenClient, "get_by_name")
def test_get_api_token_by_name(mock_token_client, client: AtlanClient):
    display_name = "123"

    client.get_api_token_by_name(display_name=display_name)

    mock_token_client.assert_called_once_with(display_name=display_name)


@patch.object(TokenClient, "get_by_id")
def test_get_api_token_by_id(mock_token_client, client: AtlanClient):
    client_id = "123"

    client.get_api_token_by_id(client_id=client_id)

    mock_token_client.assert_called_once_with(client_id=client_id)


@patch.object(TokenClient, "create")
def test_create_api_token(mock_token_client, client: AtlanClient):
    display_name = "name"
    description = "something"
    personas = {"something"}
    validity_seconds = 23

    client.create_api_token(
        display_name=display_name,
        description=description,
        personas=personas,
        validity_seconds=validity_seconds,
    )

    mock_token_client.assert_called_once_with(
        display_name=display_name,
        description=description,
        personas=personas,
        validity_seconds=validity_seconds,
    )


@patch.object(TokenClient, "update")
def test_update_api_token(mock_token_client, client: AtlanClient):
    guid = "123"
    display_name = "name"
    description = "something"
    personas = {"something"}

    client.update_api_token(
        guid=guid, display_name=display_name, description=description, personas=personas
    )

    mock_token_client.assert_called_once_with(
        guid=guid, display_name=display_name, description=description, personas=personas
    )


@patch.object(TokenClient, "purge")
def test_purgeapi_token(mock_token_client, client: AtlanClient):
    guid = "123"

    client.purge_api_token(guid=guid)

    mock_token_client.assert_called_once_with(guid=guid)


@patch.object(TypeDefClient, "get_all")
def test_get_all_typedefs(mock_type_def_client, client: AtlanClient):
    client.get_all_typedefs()

    mock_type_def_client.assert_called_once()


@patch.object(TypeDefClient, "get")
def test_get_typedefs(mock_type_def_client, client: AtlanClient):
    client.get_typedefs(type_category=AtlanTypeCategory.ENUM)

    mock_type_def_client.assert_called_once_with(type_category=AtlanTypeCategory.ENUM)


@patch.object(TypeDefClient, "create")
def test_create_typedef(mock_type_def_client, client: AtlanClient):
    type_def = TypeDef(category=AtlanTypeCategory.ENUM, name="dummy")

    client.create_typedef(typedef=type_def)

    mock_type_def_client.assert_called_once_with(typedef=type_def)


@patch.object(TypeDefClient, "update")
def test_update_typedef(mock_type_def_client, client: AtlanClient):
    type_def = TypeDef(category=AtlanTypeCategory.ENUM, name="dummy")

    client.update_typedef(typedef=type_def)

    mock_type_def_client.assert_called_once_with(typedef=type_def)


@patch.object(TypeDefClient, "purge")
def test_purge_typedef(mock_type_def_client, client: AtlanClient):
    name = "bob"

    client.purge_typedef(name=name, typedef_type=TypeDef)

    mock_type_def_client.assert_called_once_with(name=name, typedef_type=TypeDef)


@patch.object(UserClient, "create")
def test_create_users(mock_type_def_client, client: AtlanClient):
    user = AtlanUser()

    client.create_users(users=[user])

    mock_type_def_client.assert_called_once_with(users=[user])


@patch.object(UserClient, "update")
def test_update_users(mock_type_def_client, client: AtlanClient):
    user = AtlanUser()
    guid = "123"

    client.update_user(guid=guid, user=user)

    mock_type_def_client.assert_called_once_with(guid=guid, user=user)


@patch.object(UserClient, "get_groups")
def test_get_groups_for_user(mock_type_def_client, client: AtlanClient):
    guid = "123"

    client.get_groups_for_user(guid=guid)

    mock_type_def_client.assert_called_once_with(guid=guid)


@patch.object(UserClient, "add_to_groups")
def test_add_user_to_groups(mock_type_def_client, client: AtlanClient):
    guid = "123"
    group_ids = ["456", "789"]

    client.add_user_to_groups(guid=guid, group_ids=group_ids)

    mock_type_def_client.assert_called_once_with(guid=guid, group_ids=group_ids)


@patch.object(UserClient, "change_role")
def test_change_user_role(mock_type_def_client, client: AtlanClient):
    guid = "123"
    role_id = "456"

    client.change_user_role(guid=guid, role_id=role_id)

    mock_type_def_client.assert_called_once_with(guid=guid, role_id=role_id)


@patch.object(UserClient, "get_current")
def test_get_current_user(mock_type_def_client, client: AtlanClient):
    client.get_current_user()

    mock_type_def_client.assert_called_once()


@patch.object(UserClient, "get")
def test_get_users(mock_type_def_client, client: AtlanClient):
    limit = 1
    post_filter = "post"
    sort = "sort"
    count = False
    offset = 6

    client.get_users(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )

    mock_type_def_client.assert_called_once_with(
        limit=limit, post_filter=post_filter, sort=sort, count=count, offset=offset
    )


@patch.object(UserClient, "get_all")
def test_get_all_users(mock_type_def_client, client: AtlanClient):
    limit = 1

    client.get_all_users(limit=limit)

    mock_type_def_client.assert_called_once_with(limit=limit)


@patch.object(UserClient, "get_by_email")
def test_get_users_by_email(mock_type_def_client, client: AtlanClient):
    limit = 1
    email = "who@somewhere.com"

    client.get_users_by_email(email=email, limit=limit)

    mock_type_def_client.assert_called_once_with(email=email, limit=limit)


@patch.object(UserClient, "get_by_username")
def test_get_user_by_username(mock_type_def_client, client: AtlanClient):
    username = "bob"

    client.get_user_by_username(username=username)

    mock_type_def_client.assert_called_once_with(username=username)
