# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AuthPolicy, Purpose
from pyatlan.model.enums import (
    AssetSidebarTab,
    AtlanTagColor,
    AuthPolicyType,
    DataAction,
    DataMaskingType,
    PurposeMetadataAction,
)
from pyatlan.model.typedef import AtlanTagDef
from tests.integration.client import TestId, delete_asset

MODULE_NAME = TestId.make_unique("Purpose")


@pytest.fixture(scope="module")
def atlan_tag(
    client: AtlanClient,
) -> Generator[AtlanTagDef, None, None]:
    atlan_tag_def = AtlanTagDef.create(name=MODULE_NAME, color=AtlanTagColor.GREEN)
    typedef = client.create_typedef(atlan_tag_def)
    yield typedef.atlan_tag_defs[0]
    client.purge_typedef(MODULE_NAME, typedef_type=AtlanTagDef)


@pytest.fixture(scope="module")
def purpose(
    client: AtlanClient,
    atlan_tag: AtlanTagDef,
) -> Generator[Purpose, None, None]:
    to_create = Purpose.create(name=MODULE_NAME, atlan_tags=[atlan_tag.display_name])
    response = client.save(to_create)
    p = response.assets_created(asset_type=Purpose)[0]
    yield p
    delete_asset(client, guid=p.guid, asset_type=Purpose)


def test_purpose(
    client: AtlanClient,
    purpose: Purpose,
):
    assert purpose
    assert purpose.guid
    assert purpose.qualified_name
    assert purpose.name == MODULE_NAME
    assert purpose.display_name == MODULE_NAME
    assert purpose.qualified_name != MODULE_NAME


@pytest.mark.order(after="test_purpose")
def test_update_purpose(
    client: AtlanClient,
    purpose: Purpose,
):
    assert purpose.qualified_name
    assert purpose.name
    to_update = Purpose.create_for_modification(
        purpose.qualified_name, purpose.name, True
    )
    to_update.description = "Now with a description!"
    to_update.deny_asset_tabs = {
        AssetSidebarTab.LINEAGE.value,
        AssetSidebarTab.RELATIONS.value,
        AssetSidebarTab.QUERIES.value,
    }
    response = client.save(to_update)
    assert response
    updated = response.assets_updated(asset_type=Purpose)
    assert updated
    assert len(updated) == 1
    assert updated[0]
    assert updated[0].guid == purpose.guid
    assert updated[0].description == "Now with a description!"
    assert updated[0].deny_asset_tabs
    assert len(updated[0].deny_asset_tabs) == 3


@pytest.mark.order(after="test_update_purpose")
def test_find_purpose_by_name(
    client: AtlanClient,
    purpose: Purpose,
):
    result = client.find_purposes_by_name(MODULE_NAME)
    count = 0
    # TODO: replace with exponential back-off and jitter
    while not result and count < 10:
        time.sleep(2)
        result = client.find_purposes_by_name(MODULE_NAME)
        count += 1
    assert result
    assert len(result) == 1
    assert result[0].guid == purpose.guid


@pytest.mark.order(after="test_find_purpose_by_name")
def test_add_policies_to_purpose(
    client: AtlanClient,
    purpose: Purpose,
):
    metadata = Purpose.create_metadata_policy(
        name="Simple read access",
        purpose_id=purpose.guid,
        policy_type=AuthPolicyType.ALLOW,
        actions={PurposeMetadataAction.READ},
        all_users=True,
    )
    data = Purpose.create_data_policy(
        name="Mask the data",
        purpose_id=purpose.guid,
        policy_type=AuthPolicyType.DATA_MASK,
        all_users=True,
    )
    data.policy_mask_type = DataMaskingType.HASH
    response = client.save([metadata, data])
    assert response
    purposes = response.assets_updated(asset_type=Purpose)
    assert purposes
    assert len(purposes) == 1
    assert purposes[0].guid == purpose.guid
    policies = response.assets_created(asset_type=AuthPolicy)
    assert policies
    assert len(policies) == 2


@pytest.mark.order(after="test_add_policies_to_purpose")
def test_retrieve_purpose(
    client: AtlanClient,
    purpose: Purpose,
):
    assert purpose.qualified_name
    one = client.get_asset_by_qualified_name(
        qualified_name=purpose.qualified_name, asset_type=Purpose
    )
    assert one
    assert one.guid == purpose.guid
    assert one.description == "Now with a description!"
    denied = one.deny_asset_tabs
    assert denied
    assert len(denied) == 3
    assert AssetSidebarTab.LINEAGE.value in denied
    assert AssetSidebarTab.RELATIONS.value in denied
    assert AssetSidebarTab.QUERIES.value in denied
    policies = one.policies
    assert policies
    assert len(policies) == 2
    for policy in policies:
        # Need to retrieve the full policy if we want to see any info about it
        # (what comes back on the Persona itself are just policy references)
        full = client.get_asset_by_guid(guid=policy.guid, asset_type=AuthPolicy)
        assert full
        sub_cat = full.policy_sub_category
        assert sub_cat
        assert sub_cat in ["metadata", "data"]
        if sub_cat == "metadata":
            assert full.policy_actions
            assert len(full.policy_actions) == 1
            assert PurposeMetadataAction.READ in full.policy_actions
            assert full.policy_type == AuthPolicyType.ALLOW
        elif sub_cat == "data":
            assert full.policy_actions
            assert len(full.policy_actions) == 1
            assert DataAction.SELECT in full.policy_actions
            assert full.policy_type == AuthPolicyType.DATA_MASK
            assert full.policy_mask_type
            assert full.policy_mask_type == DataMaskingType.HASH
