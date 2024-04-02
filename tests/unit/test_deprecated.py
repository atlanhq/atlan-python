# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import Mock, patch

import pytest

from pyatlan.client.asset import AssetClient
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.group import GroupClient
from pyatlan.client.role import RoleClient
from pyatlan.client.token import TokenClient
from pyatlan.client.typedef import TypeDefClient
from pyatlan.client.user import UserClient
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryCategory, AtlasGlossaryTerm
from pyatlan.model.core import Announcement
from pyatlan.model.custom_metadata import CustomMetadataDict
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    AtlanTypeCategory,
    CertificateStatus,
)
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


@pytest.mark.parametrize(
    "deprecated_name, current_name, values",
    [
        (
            "get_asset_by_qualified_name",
            "get_by_qualified_name",
            {
                "qualified_name": "qname",
                "asset_type": AtlasGlossary,
                "min_ext_info": False,
                "ignore_relationships": True,
            },
        ),
        (
            "get_asset_by_guid",
            "get_by_guid",
            {
                "guid": "123",
                "asset_type": AtlasGlossary,
                "min_ext_info": False,
                "ignore_relationships": True,
            },
        ),
        (
            "retrieve_minimal",
            "retrieve_minimal",
            {
                "guid": "123",
                "asset_type": AtlasGlossary,
            },
        ),
        (
            "upsert",
            "save",
            {
                "entity": [],
                "replace_atlan_tags": True,
                "replace_custom_metadata": True,
                "overwrite_custom_metadata": True,
            },
        ),
        (
            "save",
            "save",
            {
                "entity": [],
                "replace_atlan_tags": True,
                "replace_custom_metadata": True,
                "overwrite_custom_metadata": True,
            },
        ),
        (
            "upsert_merging_cm",
            "save_merging_cm",
            {
                "entity": [],
                "replace_atlan_tags": True,
            },
        ),
        (
            "save_merging_cm",
            "save_merging_cm",
            {
                "entity": [],
                "replace_atlan_tags": True,
            },
        ),
        (
            "upsert_replacing_cm",
            "save_replacing_cm",
            {
                "entity": [],
                "replace_atlan_tagss": True,
            },
        ),
        (
            "save_replacing_cm",
            "save_replacing_cm",
            {
                "entity": [],
                "replace_atlan_tags": True,
            },
        ),
        (
            "update_replacing_cm",
            "update_replacing_cm",
            {
                "entity": [],
                "replace_atlan_tags": True,
            },
        ),
        (
            "purge_entity_by_guid",
            "purge_by_guid",
            {
                "guid": "123",
            },
        ),
        (
            "delete_entity_by_guid",
            "delete_by_guid",
            {
                "guid": "123",
            },
        ),
        (
            "restore",
            "restore",
            {
                "asset_type": AtlasGlossary,
                "qualified_name": "qname",
            },
        ),
        (
            "search",
            "search",
            {
                "criteria": None,
            },
        ),
        (
            "add_atlan_tags",
            "add_atlan_tags",
            {
                "asset_type": AtlasGlossary,
                "qualified_name": "qname",
                "atlan_tag_names": ["Something"],
                "propagate": False,
                "remove_propagation_on_delete": False,
                "restrict_lineage_propagation": False,
                "restrict_propagation_through_hierarchy": False,
            },
        ),
        (
            "remove_atlan_tag",
            "remove_atlan_tag",
            {
                "asset_type": AtlasGlossary,
                "qualified_name": "qname",
                "atlan_tag_name": "Something",
            },
        ),
        (
            "update_certificate",
            "update_certificate",
            {
                "asset_type": AtlasGlossary,
                "qualified_name": "qname",
                "name": "Something",
                "certificate_status": CertificateStatus.DRAFT,
                "message": "dah",
            },
        ),
        (
            "remove_certificate",
            "remove_certificate",
            {
                "asset_type": AtlasGlossary,
                "qualified_name": "qname",
                "name": "Something",
            },
        ),
        (
            "update_announcement",
            "update_announcement",
            {
                "asset_type": AtlasGlossary,
                "qualified_name": "qname",
                "name": "Something",
                "announcement": Announcement(
                    announcement_title="blah",
                    announcement_message="bah",
                    announcement_type=AnnouncementType.ISSUE,
                ),
            },
        ),
        (
            "remove_announcement",
            "remove_announcement",
            {
                "asset_type": AtlasGlossary,
                "qualified_name": "qname",
                "name": "Something",
            },
        ),
        (
            "replace_custom_metadata",
            "replace_custom_metadata",
            {
                "guid": "123",
                "custom_metadata": Mock(CustomMetadataDict),
            },
        ),
        (
            "remove_custom_metadata",
            "remove_custom_metadata",
            {
                "guid": "123",
                "cm_name": "something",
            },
        ),
        (
            "append_terms",
            "append_terms",
            {
                "asset_type": AtlasGlossary,
                "terms": [],
                "guid": "123",
                "qualified_name": "qname",
            },
        ),
        (
            "replace_terms",
            "replace_terms",
            {
                "asset_type": AtlasGlossary,
                "terms": [],
                "guid": "123",
                "qualified_name": "qname",
            },
        ),
        (
            "remove_terms",
            "remove_terms",
            {
                "asset_type": AtlasGlossary,
                "terms": [],
                "guid": "123",
                "qualified_name": "qname",
            },
        ),
        (
            "find_connections_by_name",
            "find_connections_by_name",
            {
                "name": "Bob",
                "connector_type": AtlanConnectorType.SNOWFLAKE,
                "attributes": ["something"],
            },
        ),
        (
            "find_personas_by_name",
            "find_personas_by_name",
            {
                "name": "Bob",
                "attributes": ["something"],
            },
        ),
        (
            "find_purposes_by_name",
            "find_purposes_by_name",
            {
                "name": "Bob",
                "attributes": ["something"],
            },
        ),
        (
            "find_glossary_by_name",
            "find_glossary_by_name",
            {
                "name": "Bob",
                "attributes": ["something"],
            },
        ),
        (
            "find_category_fast_by_name",
            "find_category_fast_by_name",
            {
                "name": "Bob",
                "glossary_qualified_name": "abc",
                "attributes": ["something"],
            },
        ),
        (
            "find_category_by_name",
            "find_category_by_name",
            {
                "name": "Bob",
                "glossary_name": "abc",
                "attributes": ["something"],
            },
        ),
        (
            "find_term_fast_by_name",
            "find_term_fast_by_name",
            {
                "name": "Bob",
                "glossary_qualified_name": "abc",
                "attributes": ["something"],
            },
        ),
        (
            "find_term_by_name",
            "find_term_by_name",
            {
                "name": "Bob",
                "glossary_name": "abc",
                "attributes": ["something"],
            },
        ),
    ],
)
def test_asset_deprecated_methods(
    deprecated_name: str, current_name: str, values, client: AtlanClient
):
    with patch.object(AssetClient, current_name) as mock:
        func = getattr(client, deprecated_name)
        func(**values)

    if deprecated_name == "upsert_replacing_cm":
        values["replace_atlan_tags"] = values["replace_atlan_tagss"]
        del values["replace_atlan_tagss"]

    mock.assert_called_once_with(**values)
