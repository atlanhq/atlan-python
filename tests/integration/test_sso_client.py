# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.sso import SSOClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import AtlanSSO
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper
from tests.integration.client import TestId

FIXED_USER = "aryaman.bhushan"
MODULE_NAME = TestId.make_unique("SSOClient")

GROUP_NAME = MODULE_NAME
SSO_GROUP_NAME = "test-sso-group"
SSO_GROUP_NAME_UPDATED = "test-sso-group-updated"


def delete_group(client: AtlanClient, guid: str) -> None:
    client.group.purge(guid)


def delete_sso_mapping(client: AtlanClient, group_map_id: str) -> None:
    response = client.sso.delete_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD, group_map_id=group_map_id
    )
    assert response is None


@pytest.fixture(scope="module")
def group(client: AtlanClient) -> Generator[AtlanGroup, None, None]:
    to_create = AtlanGroup.create(GROUP_NAME)
    fixed_user = client.user.get_by_username(FIXED_USER)
    assert fixed_user
    g = client.group.create(group=to_create, user_ids=[str(fixed_user.id)])
    groups = client.group.get_by_name(alias=GROUP_NAME)
    assert groups
    assert len(groups) == 1
    yield groups[0]
    assert g.group
    delete_group(client, g.group)


@pytest.fixture(scope="module")
def sso_mapping(
    client: AtlanClient, group: AtlanGroup
) -> Generator[SSOMapper, None, None]:
    assert group
    assert group.id
    response = client.sso.create_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD, atlan_group=group, sso_group_name=SSO_GROUP_NAME
    )
    assert response

    azure_group_mapping = None
    sso_mappings = client.sso.get_all_group_mappings(sso_alias=AtlanSSO.JUMPCLOUD)
    for mapping in sso_mappings:
        if (
            group.id
            and group.id in str(mapping.name)
            and mapping.identity_provider_mapper == SSOClient.IDP_GROUP_MAPPER
        ):
            azure_group_mapping = mapping
            break
    assert azure_group_mapping and azure_group_mapping.id
    yield azure_group_mapping
    delete_sso_mapping(client, azure_group_mapping.id)


def _assert_sso_group_mapping(
    group: AtlanGroup, sso_mapping: SSOMapper, is_updated: bool = False
):
    assert sso_mapping
    assert sso_mapping.id
    assert sso_mapping.identity_provider_alias == AtlanSSO.JUMPCLOUD
    assert sso_mapping.identity_provider_mapper == SSOClient.IDP_GROUP_MAPPER
    assert sso_mapping.config.attributes == "[]"
    assert sso_mapping.config.group_name == group.name
    assert sso_mapping.config.attribute_values_regex is None
    assert sso_mapping.config.attribute_friendly_name is None

    assert sso_mapping.config.sync_mode == SSOClient.GROUP_MAPPER_SYNC_MODE
    assert sso_mapping.config.attribute_name == SSOClient.GROUP_MAPPER_ATTRIBUTE
    if is_updated:
        assert sso_mapping.name is None
        assert sso_mapping.config.attribute_value == SSO_GROUP_NAME_UPDATED
    else:
        assert group.id and (group.id in str(sso_mapping.name))
        assert sso_mapping.config.attribute_value == SSO_GROUP_NAME


def test_sso_create_group_mapping(
    client: AtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping
    _assert_sso_group_mapping(group, sso_mapping)


@pytest.mark.order(after="test_sso_create_group_mapping")
def test_sso_create_group_mapping_again_raises_invalid_request_error(
    client: AtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping

    with pytest.raises(InvalidRequestError) as err:
        client.sso.create_group_mapping(
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
def test_sso_retrieve_group_mapping(
    client: AtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping
    assert sso_mapping.id
    time.sleep(5)

    retrieved_sso_mapping = client.sso.get_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD, group_map_id=sso_mapping.id
    )
    _assert_sso_group_mapping(group, retrieved_sso_mapping)


@pytest.mark.order(after="test_sso_retrieve_group_mapping")
def test_sso_retrieve_all_group_mappings(
    client: AtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert group.id
    assert sso_mapping
    time.sleep(5)

    retrieved_mappings = client.sso.get_all_group_mappings(sso_alias=AtlanSSO.JUMPCLOUD)
    assert len(retrieved_mappings) >= 1
    mapping_found = False
    for mapping in retrieved_mappings:
        if (
            group.id in str(mapping.name)
            and mapping.identity_provider_mapper == SSOClient.IDP_GROUP_MAPPER
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
def test_update_group_mapping(
    client: AtlanClient,
    group: AtlanGroup,
    sso_mapping: SSOMapper,
):
    assert group
    assert sso_mapping
    assert sso_mapping.id

    updated_mapping = client.sso.update_group_mapping(
        sso_alias=AtlanSSO.JUMPCLOUD,
        atlan_group=group,
        group_map_id=sso_mapping.id,
        sso_group_name=SSO_GROUP_NAME_UPDATED,
    )
    _assert_sso_group_mapping(group, updated_mapping, True)
