# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import time
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.client.common.sso import (
    GROUP_MAPPER_ATTRIBUTE,
    GROUP_MAPPER_SYNC_MODE,
    IDP_GROUP_MAPPER,
)
from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import AtlanSSO
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper
from tests.integration.client import TestId

FIXED_USER = "aryaman"
MODULE_NAME = TestId.make_unique("AsyncSSOClient")

GROUP_NAME = MODULE_NAME
SSO_GROUP_NAME = "test-sso-group"
SSO_GROUP_NAME_UPDATED = "test-sso-group-updated"


async def delete_group_async(client: AsyncAtlanClient, guid: str) -> None:
    await client.group.purge(guid)


async def delete_sso_mapping_async(client: AsyncAtlanClient, group_map_id: str) -> None:
    response = await client.sso.delete_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD, group_map_id=group_map_id
    )
    assert response is None


@pytest_asyncio.fixture(scope="module")
async def group(client: AsyncAtlanClient) -> AsyncGenerator[AtlanGroup, None]:
    to_create = AtlanGroup.create(GROUP_NAME)
    fixed_user = await client.user.get_by_username(FIXED_USER)
    assert fixed_user
    g = await client.group.create(group=to_create, user_ids=[str(fixed_user.id)])
    groups = await client.group.get_by_name(alias=GROUP_NAME)
    assert groups
    assert groups.records is not None
    assert len(groups.records) == 1
    yield groups.records[0]
    assert g.group
    await delete_group_async(client, g.group)


@pytest_asyncio.fixture(scope="module")
async def sso_mapping(
    client: AsyncAtlanClient, group: AtlanGroup
) -> AsyncGenerator[SSOMapper, None]:
    assert group
    assert group.id
    response = await client.sso.create_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD, atlan_group=group, sso_group_name=SSO_GROUP_NAME
    )
    assert response

    azure_group_mapping = None
    sso_mappings = await client.sso.get_all_group_mappings(sso_alias=AtlanSSO.JUMPCLOUD)
    for mapping in sso_mappings:
        if (
            group.id
            and group.id in str(mapping.name)
            and mapping.identity_provider_mapper == IDP_GROUP_MAPPER
        ):
            azure_group_mapping = mapping
            break
    assert azure_group_mapping and azure_group_mapping.id
    yield azure_group_mapping
    await delete_sso_mapping_async(client, azure_group_mapping.id)


def _assert_sso_group_mapping(
    group: AtlanGroup, sso_mapping: SSOMapper, is_updated: bool = False
):
    assert sso_mapping
    assert sso_mapping.id
    assert sso_mapping.identity_provider_alias == AtlanSSO.JUMPCLOUD
    assert sso_mapping.identity_provider_mapper == IDP_GROUP_MAPPER
    assert sso_mapping.config.attributes == "[]"
    assert sso_mapping.config.group_name == group.name
    assert sso_mapping.config.attribute_values_regex is None
    assert sso_mapping.config.attribute_friendly_name is None

    assert sso_mapping.config.sync_mode == GROUP_MAPPER_SYNC_MODE
    assert sso_mapping.config.attribute_name == GROUP_MAPPER_ATTRIBUTE
    if is_updated:
        assert sso_mapping.name is None
        assert sso_mapping.config.attribute_value == SSO_GROUP_NAME_UPDATED
    else:
        assert group.id and (group.id in str(sso_mapping.name))
        assert sso_mapping.config.attribute_value == SSO_GROUP_NAME


async def test_sso_create_group_mapping(
    client: AsyncAtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping
    _assert_sso_group_mapping(group, sso_mapping)


@pytest.mark.order(after="test_sso_create_group_mapping")
async def test_sso_create_group_mapping_again_raises_invalid_request_error(
    client: AsyncAtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping

    with pytest.raises(InvalidRequestError) as err:
        await client.sso.create_group_mapping(
            sso_alias=AtlanSSO.JUMPCLOUD,
            atlan_group=group,
            sso_group_name=SSO_GROUP_NAME,
        )
    assert (
        f"ATLAN-PYTHON-400-058 SSO group mapping already exists between "
        f"{group.alias} (Atlan group) <-> {SSO_GROUP_NAME} (SSO group)"
    ) in str(err.value)


@pytest.mark.order(
    after="test_sso_create_group_mapping_again_raises_invalid_request_error"
)
async def test_sso_retrieve_group_mapping(
    client: AsyncAtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping
    assert sso_mapping.id
    time.sleep(5)

    retrieved_sso_mapping = await client.sso.get_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD, group_map_id=sso_mapping.id
    )
    _assert_sso_group_mapping(group, retrieved_sso_mapping)


@pytest.mark.order(after="test_sso_retrieve_group_mapping")
async def test_sso_retrieve_all_group_mappings(
    client: AsyncAtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert group.id
    assert sso_mapping
    time.sleep(5)

    retrieved_mappings = await client.sso.get_all_group_mappings(
        sso_alias=AtlanSSO.JUMPCLOUD
    )
    assert len(retrieved_mappings) >= 1
    mapping_found = False
    for mapping in retrieved_mappings:
        if (
            group.id in str(mapping.name)
            and mapping.identity_provider_mapper == IDP_GROUP_MAPPER
        ):
            mapping_found = True
            _assert_sso_group_mapping(group, mapping)
            break
    if not mapping_found:
        pytest.fail(
            f"{group.alias} (Atlan Group) <-> ({sso_mapping.config.attribute_value}) "
            f"{AtlanSSO.JUMPCLOUD} SSO group mapping not found."
        )


@pytest.mark.order(after="test_sso_retrieve_all_group_mappings")
async def test_update_group_mapping(
    client: AsyncAtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping
    assert sso_mapping.id

    updated_mapping = await client.sso.update_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD,
        atlan_group=group,
        group_map_id=sso_mapping.id,
        sso_group_name=SSO_GROUP_NAME_UPDATED,
    )
    _assert_sso_group_mapping(group, updated_mapping, True)
