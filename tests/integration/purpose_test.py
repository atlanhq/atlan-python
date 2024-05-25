# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.token import SERVICE_ACCOUNT_
from pyatlan.model.api_tokens import ApiToken
from pyatlan.model.assets import AuthPolicy, Column, Purpose
from pyatlan.model.core import AtlanTagName
from pyatlan.model.enums import (
    AssetSidebarTab,
    AtlanConnectorType,
    AtlanTagColor,
    AuthPolicyType,
    DataAction,
    DataMaskingType,
    HekaFlow,
    PurposeMetadataAction,
    QueryStatus,
)
from pyatlan.model.query import QueryRequest
from pyatlan.model.typedef import AtlanTagDef
from tests.integration.client import TestId, delete_asset
from tests.integration.requests_test import delete_token

MODULE_NAME = TestId.make_unique("Purpose")
PERSONA_NAME = "Data Assets"
DB_NAME = "RAW"
TABLE_NAME = "PACKAGETYPES"
COLUMN_NAME = "PACKAGETYPENAME"
SCHEMA_NAME = "WIDEWORLDIMPORTERS_WAREHOUSE"
API_TOKEN_NAME = MODULE_NAME


@pytest.fixture(scope="module")
def snowflake_conn(client: AtlanClient):
    return client.asset.find_connections_by_name(
        "development", AtlanConnectorType.SNOWFLAKE
    )[0]


@pytest.fixture(scope="module")
def snowflake_column_qn(snowflake_conn):
    return f"{snowflake_conn.qualified_name}/{DB_NAME}/{SCHEMA_NAME}/{TABLE_NAME}/{COLUMN_NAME}"


@pytest.fixture(scope="module")
def atlan_tag_def(
    client: AtlanClient,
    snowflake_column_qn,
) -> Generator[AtlanTagDef, None, None]:
    atlan_tag_def = AtlanTagDef.create(name=MODULE_NAME, color=AtlanTagColor.GREEN)
    typedef = client.typedef.create(atlan_tag_def)
    yield typedef.atlan_tag_defs[0]
    # The client can be re-instantiated inside test cases, e.g `test_run_query_with_policy`.
    # Therefore, here we need to explicitly create the client
    client = AtlanClient()
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=snowflake_column_qn,
        atlan_tag_name=MODULE_NAME,
    )
    client.typedef.purge(MODULE_NAME, typedef_type=AtlanTagDef)


@pytest.fixture(scope="module")
def token(client: AtlanClient) -> Generator[ApiToken, None, None]:
    token = None
    try:
        token = client.token.create(API_TOKEN_NAME)
        assert token
        assert token.guid
        assert token.display_name
        # After creating the token, assign it to the
        # "Data Assets" persona to grant it query access
        persona = client.asset.find_personas_by_name(PERSONA_NAME)[0]
        assert persona.qualified_name
        client.token.update(
            guid=token.guid,
            display_name=token.display_name,
            personas={persona.qualified_name},
        )
        # Note: need to read the token back again to see
        # its associated personas -- will leave that to later...
        yield token
    finally:
        delete_token(client, token)


@pytest.fixture(scope="module")
def query(snowflake_conn) -> QueryRequest:
    # NOTE: This requires pre-existing assets:
    # - Snowflake connection called "development"
    #   with a specific pre-existing table
    # - Persona called "Data Assets" with a data policy
    #   granting query access to the Snowflake table
    return QueryRequest(
        sql=f'SELECT * FROM "{TABLE_NAME}" LIMIT 50',
        data_source_name=snowflake_conn.qualified_name,
        default_schema=f"{DB_NAME}.{SCHEMA_NAME}",
    )


@pytest.fixture(scope="module")
def atlan_tag_name(atlan_tag_def):
    return AtlanTagName(atlan_tag_def.display_name)


@pytest.fixture(scope="module")
def purpose(
    client: AtlanClient,
    atlan_tag_name,
) -> Generator[Purpose, None, None]:
    to_create = Purpose.create(name=MODULE_NAME, atlan_tags=[atlan_tag_name])
    response = client.asset.save(to_create)
    p = response.assets_created(asset_type=Purpose)[0]
    yield p
    delete_asset(client, guid=p.guid, asset_type=Purpose)


@pytest.fixture(scope="module")
def assign_tag_to_asset(client, snowflake_column_qn):
    result = client.asset.add_atlan_tags(
        asset_type=Column,
        qualified_name=snowflake_column_qn,
        atlan_tag_names=[MODULE_NAME],
        propagate=False,
        remove_propagation_on_delete=False,
        restrict_lineage_propagation=False,
    )
    return result


def test_query(query):
    assert query.sql
    assert query.data_source_name
    assert query.default_schema


def test_purpose(client: AtlanClient, purpose: Purpose, atlan_tag_name: AtlanTagName):
    assert purpose
    assert purpose.guid
    assert purpose.qualified_name
    assert purpose.name == MODULE_NAME
    assert purpose.display_name == MODULE_NAME
    assert purpose.qualified_name != MODULE_NAME
    purpose = client.asset.get_by_guid(guid=purpose.guid, asset_type=Purpose)
    assert purpose.purpose_atlan_tags
    assert [atlan_tag_name] == purpose.purpose_atlan_tags


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
    response = client.asset.save(to_update)
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
    result = client.asset.find_purposes_by_name(
        MODULE_NAME, attributes=["purposeClassifications"]
    )
    count = 0
    # TODO: replace with exponential back-off and jitter
    while not result and count < 10:
        time.sleep(2)
        result = client.asset.find_purposes_by_name(MODULE_NAME)
        count += 1
    assert result
    assert len(result) == 1
    assert result[0].guid == purpose.guid


@pytest.mark.order(after="test_find_purpose_by_name")
def test_add_policies_to_purpose(
    client: AtlanClient,
    purpose: Purpose,
    token: ApiToken,
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
        policy_users={f"{SERVICE_ACCOUNT_}{token.client_id}"},
        all_users=False,
    )
    data.policy_mask_type = DataMaskingType.REDACT
    response = client.asset.save([metadata, data])
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
    one = client.asset.get_by_qualified_name(
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
        full = client.asset.get_by_guid(guid=policy.guid, asset_type=AuthPolicy)
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
            assert full.policy_mask_type == DataMaskingType.REDACT


@pytest.mark.order(after="test_retrieve_purpose")
def test_run_query_without_policy(client: AtlanClient, assign_tag_to_asset, query):
    response = client.queries.stream(request=query)
    assert response
    assert response.rows
    assert len(response.rows) > 1
    row = response.rows[0]
    assert row
    assert len(row) == 7
    assert row[2]
    # Ensure it is NOT redacted
    assert row[2].startswith("Xx") is False


def test_token_permissions(client: AtlanClient, token):
    persona = client.asset.find_personas_by_name(PERSONA_NAME)[0]
    result = client.token.get_by_name(display_name=API_TOKEN_NAME)
    assert result
    assert result.attributes
    assert result.attributes.persona_qualified_name
    assert len(result.attributes.persona_qualified_name) == 1
    assert (
        next(iter(result.attributes.persona_qualified_name)).persona_qualified_name
        == persona.qualified_name
    )


@pytest.mark.order(after="test_token_permissions")
def test_run_query_with_policy(client: AtlanClient, assign_tag_to_asset, token, query):
    redacted = AtlanClient(
        base_url=client.base_url, api_key=token.attributes.access_token
    )
    # The policy will take some time to go into effect
    # start by waiting a reasonable set amount of time
    # (limit the same query re-running multiple times on data store)
    time.sleep(30)
    count = 0
    response = None
    found = HekaFlow.BYPASS

    # TODO: replace with exponential back-off and jitter
    while found == HekaFlow.BYPASS and count < 30:
        time.sleep(2)
        response = redacted.queries.stream(query)
        assert response
        assert response.details
        assert response.details.status
        assert response.details.heka_flow
        status = response.details.status
        if status != QueryStatus.ERROR:
            found = response.details.heka_flow
        count += 1

    assert response
    assert response.rows
    assert len(response.rows) > 1
    row = response.rows[0]
    assert row
    assert len(row) == 7
    assert row[2]
    # Ensure it IS redacted
    assert row[2].startswith("Xx")
