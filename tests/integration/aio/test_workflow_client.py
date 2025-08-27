# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import time
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from pyatlan import utils
from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.assets import Connection
from pyatlan.model.credential import Credential, CredentialResponse
from pyatlan.model.enums import AtlanConnectorType, AtlanWorkflowPhase, WorkflowPackage
from pyatlan.model.packages.snowflake_miner import SnowflakeMiner
from pyatlan.model.workflow import WorkflowResponse, WorkflowSchedule
from tests.integration.aio.utils import delete_asset_async
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AsyncWorkflowClient")


async def delete_workflow_async(client: AsyncAtlanClient, workflow_name: str) -> None:
    await client.workflow.delete(workflow_name=workflow_name)


WORKFLOW_TEMPLATE_REF = "workflowTemplateRef"
WORKFLOW_SCHEDULE_SCHEDULE = "45 4 * * *"
WORKFLOW_SCHEDULE_TIMEZONE = "Asia/Kolkata"
WORKFLOW_SCHEDULE_UPDATED_1 = "45 5 * * *"
WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_1 = "Europe/Paris"
WORKFLOW_SCHEDULE_UPDATED_2 = "45 6 * * *"
WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_2 = "Europe/London"
WORKFLOW_SCHEDULE_UPDATED_3 = "45 7 * * *"
WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_3 = "Europe/Dublin"

ASSET_TYPE_CONNECTION = "Connection"
ASSET_TYPE_CONNECTION_QN = "default/snowflake/" + str(utils.get_epoch_timestamp())


@pytest_asyncio.fixture(scope="module")
async def connection(client: AsyncAtlanClient) -> AsyncGenerator[Connection, None]:
    admin_role_guid = str(await client.role_cache.get_id_for_name("$admin"))
    to_create = await Connection.creator_async(
        client=client,
        name=MODULE_NAME,
        connector_type=AtlanConnectorType.SNOWFLAKE,
        admin_roles=[admin_role_guid],
    )
    response = await client.asset.save(to_create)
    connection_created = response.assets_created(asset_type=Connection)
    assert connection_created
    c = connection_created[0]
    yield c
    await delete_asset_async(client=client, guid=c.guid, asset_type=Connection)


@pytest_asyncio.fixture(scope="module")
async def workflow(
    client: AsyncAtlanClient, connection: Connection
) -> AsyncGenerator[WorkflowResponse, None]:
    assert connection and connection.qualified_name
    miner = (
        SnowflakeMiner(connection_qualified_name=connection.qualified_name)
        .s3(
            s3_bucket="test-s3-bucket",
            s3_prefix="test-s3-prefix",
            s3_bucket_region="test-s3-bucket-region",
            sql_query_key="TEST_QUERY",
            default_database_key="TEST_SNOWFLAKE",
            default_schema_key="TEST_SCHEMA",
            session_id_key="TEST_SESSION_ID",
        )
        .popularity_window(days=15)
        .native_lineage(enabled=True)
        .custom_config(config={"test": True, "feature": 1234})
        .to_workflow()
    )
    schedule = WorkflowSchedule(
        cron_schedule=WORKFLOW_SCHEDULE_SCHEDULE, timezone=WORKFLOW_SCHEDULE_TIMEZONE
    )
    workflow = await client.workflow.run(miner, workflow_schedule=schedule)
    assert workflow
    # Adding some delay to make sure
    # the workflow run is indexed in ES.
    time.sleep(30)
    yield workflow
    assert workflow.metadata and workflow.metadata.name
    await delete_workflow_async(client, workflow.metadata.name)


@pytest_asyncio.fixture(scope="module")
async def create_credentials(
    client: AsyncAtlanClient,
) -> AsyncGenerator[CredentialResponse, None]:
    credentials_name = f"default-spark-{int(utils.get_epoch_timestamp())}-0"

    credentials = Credential(
        name=credentials_name,
        auth_type="atlan_api_key",
        connector_config_name="atlan-connectors-spark",
        connector="spark",
        username="test-username",
        password="12345",
        connector_type="event",
        host="test-host",
        port=123,
    )

    create_credentials = await client.credentials.creator(credentials)
    guid = create_credentials.id
    if guid is None:
        raise ValueError("Failed to retrieve GUID from created credentials.")

    yield create_credentials

    response = await delete_credentials_async(client, guid=guid)
    assert response is None


async def delete_credentials_async(client: AsyncAtlanClient, guid: str):
    response = await client.credentials.purge_by_guid(guid=guid)
    return response


async def test_workflow_find_by_methods(client: AsyncAtlanClient):
    results = await client.workflow.find_by_type(
        prefix=WorkflowPackage.SNOWFLAKE, max_results=10
    )
    assert results
    assert len(results) >= 1

    workflow_id = results[0].id
    assert workflow_id
    workflow = await client.workflow.find_by_id(id=workflow_id)
    assert workflow
    assert workflow.id and workflow.id == workflow_id

    workflow = await client.workflow.find_by_id(id="invalid-id")
    assert workflow is None


async def test_workflow_get_runs_and_stop(
    client: AsyncAtlanClient, workflow: WorkflowResponse
):
    # Retrieve the latest workflow run
    assert workflow and workflow.metadata and workflow.metadata.name
    runs = await client.workflow.get_runs(
        workflow_name=workflow.metadata.name, workflow_phase=AtlanWorkflowPhase.RUNNING
    )
    assert runs and runs.count == 1
    current_page = runs.current_page()
    assert current_page is not None and len(current_page) == 1
    run = current_page[0]
    assert run and run.id
    assert workflow.metadata.name and (workflow.metadata.name in run.id)

    # Stop the running workflow
    run_response = await client.workflow.stop(workflow_run_id=run.id)
    assert run_response
    assert (
        run_response.status and run_response.status.phase == AtlanWorkflowPhase.RUNNING
    )
    assert (
        run_response.status.stored_workflow_template_spec
        and run_response.status.stored_workflow_template_spec.get(
            WORKFLOW_TEMPLATE_REF
        ).get("name")
        == workflow.metadata.name
    )

    # Test workflow monitoring
    workflow_status = await client.workflow.monitor(workflow_response=workflow)
    assert workflow_status == AtlanWorkflowPhase.FAILED

    # Test workflow monitoring by providing workflow name directly
    workflow_name = workflow.metadata.name
    workflow_status = await client.workflow.monitor(workflow_name=workflow_name)
    assert workflow_status == AtlanWorkflowPhase.FAILED

    # Test find run by id
    workflow_run = await client.workflow.find_run_by_id(id=run.id)
    assert (
        workflow_run
        and workflow_run.source
        and workflow_run.source.status
        and workflow_run.source.status.phase == AtlanWorkflowPhase.FAILED
    )

    # Test find run by status and time range
    runs_status = await client.workflow.find_runs_by_status_and_time_range(
        [AtlanWorkflowPhase.FAILED], started_at="now-1h"
    )
    assert runs_status
    async for _ in runs_status:
        pass


async def test_workflow_get_all_scheduled_runs(
    client: AsyncAtlanClient, workflow: WorkflowResponse
):
    runs = await client.workflow.get_all_scheduled_runs()

    assert workflow and workflow.metadata and workflow.metadata.name
    scheduled_workflow_name = f"{workflow.metadata.name}-cron"
    assert runs and len(runs) >= 1

    found = any(
        run.metadata and run.metadata.name == scheduled_workflow_name for run in runs
    )

    if not found:
        pytest.fail(
            f"Unable to find scheduled run for workflow: {workflow.metadata.name}"
        )


async def _assert_scheduled_run_async(
    client: AsyncAtlanClient, workflow: WorkflowResponse
):
    assert workflow and workflow.metadata and workflow.metadata.name
    scheduled_workflow = await client.workflow.get_scheduled_run(
        workflow_name=workflow.metadata.name
    )
    scheduled_workflow_name = f"{workflow.metadata.name}-cron"
    assert (
        scheduled_workflow
        and scheduled_workflow.metadata
        and scheduled_workflow.metadata.name == scheduled_workflow_name
    )


def _assert_add_schedule_async(workflow, scheduled_workflow, schedule, timezone):
    assert scheduled_workflow
    assert scheduled_workflow.metadata
    assert scheduled_workflow.metadata.name == workflow.metadata.name
    assert scheduled_workflow.metadata.annotations
    assert (
        scheduled_workflow.metadata.annotations.get("orchestration.atlan.com/schedule")
        == schedule
    )
    assert (
        scheduled_workflow.metadata.annotations.get("orchestration.atlan.com/timezone")
        == timezone
    )


def _assert_remove_schedule_async(response, workflow: WorkflowResponse):
    assert response
    assert workflow and workflow.metadata and workflow.metadata.name


async def test_workflow_get_scheduled_run(
    client: AsyncAtlanClient, workflow: WorkflowResponse
):
    await _assert_scheduled_run_async(client, workflow)


async def test_workflow_add_remove_schedule(
    client: AsyncAtlanClient, workflow: WorkflowResponse
):
    schedule = WorkflowSchedule(
        cron_schedule=WORKFLOW_SCHEDULE_UPDATED_1,
        timezone=WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_1,
    )

    # NOTE: This method will overwrite existing workflow run schedule
    # Try to update schedule again, with `Workflow` object
    scheduled_workflow = await client.workflow.add_schedule(
        workflow=workflow, workflow_schedule=schedule
    )

    _assert_add_schedule_async(
        workflow,
        scheduled_workflow,
        WORKFLOW_SCHEDULE_UPDATED_1,
        WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_1,
    )
    # Make sure scheduled run exists
    await _assert_scheduled_run_async(client, workflow)
    # Now remove the scheduled run
    response = await client.workflow.remove_schedule(workflow)
    _assert_remove_schedule_async(response, workflow)

    # Try to update schedule again, with `WorkflowSearchResult` object
    existing_workflow = (
        await client.workflow.find_by_type(prefix=WorkflowPackage.SNOWFLAKE_MINER)
    )[0]
    assert existing_workflow

    schedule = WorkflowSchedule(
        cron_schedule=WORKFLOW_SCHEDULE_UPDATED_2,
        timezone=WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_2,
    )
    scheduled_workflow = await client.workflow.add_schedule(
        workflow=existing_workflow, workflow_schedule=schedule
    )

    _assert_add_schedule_async(
        workflow,
        scheduled_workflow,
        WORKFLOW_SCHEDULE_UPDATED_2,
        WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_2,
    )
    # Make sure scheduled run exists
    await _assert_scheduled_run_async(client, workflow)
    # Now remove the scheduled run
    response = await client.workflow.remove_schedule(workflow)
    _assert_remove_schedule_async(response, workflow)

    schedule = WorkflowSchedule(
        cron_schedule=WORKFLOW_SCHEDULE_UPDATED_3,
        timezone=WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_3,
    )
    scheduled_workflow = await client.workflow.add_schedule(
        workflow=WorkflowPackage.SNOWFLAKE_MINER, workflow_schedule=schedule
    )

    _assert_add_schedule_async(
        workflow,
        scheduled_workflow,
        WORKFLOW_SCHEDULE_UPDATED_3,
        WORKFLOW_SCHEDULE_TIMEZONE_UPDATED_3,
    )
    # Make sure scheduled run exists
    await _assert_scheduled_run_async(client, workflow)
    # Now remove the scheduled run
    response = await client.workflow.remove_schedule(workflow)
    _assert_remove_schedule_async(response, workflow)


async def test_credentials(client: AsyncAtlanClient, create_credentials: Credential):
    credentials = create_credentials
    assert credentials
    assert credentials.id
    retrieved_creds = await client.credentials.get(guid=credentials.id)
    assert retrieved_creds.auth_type == "atlan_api_key"
    assert retrieved_creds.connector_config_name == "atlan-connectors-spark"


async def test_get_all_credentials(client: AsyncAtlanClient):
    credentials = await client.credentials.get_all()
    assert credentials, "Expected credentials but found None"
    assert credentials.records is not None, "Expected records but found None"


async def test_get_all_credentials_with_filter_limit_offset(client: AsyncAtlanClient):
    filter_criteria = {"connectorType": "snowflake", "isActive": True}
    limit = 1
    offset = 1
    credentials = await client.credentials.get_all(
        filter=filter_criteria, limit=limit, offset=offset
    )
    assert credentials, "Expected credentials but found None"
    assert credentials.records is not None, "Expected records but found None"


async def test_get_all_credentials_with_multiple_filters(client: AsyncAtlanClient):
    filter_criteria = {"connectorType": "jdbc", "isActive": True}

    credentials = await client.credentials.get_all(filter=filter_criteria)
    assert credentials, "Expected credentials but found None"
    assert credentials.records is not None, "Expected records but found None"


async def test_get_all_credentials_with_invalid_filter_key(client: AsyncAtlanClient):
    filter_criteria = {"invalidKey": "someValue"}
    try:
        await client.credentials.get_all(filter=filter_criteria)
        pytest.fail("Expected an error due to invalid filter key, but none occurred.")
    except Exception as e:
        assert e is not None


async def test_get_all_credentials_with_invalid_filter_value(client: AsyncAtlanClient):
    filter_criteria = {"connector_type": 123}

    try:
        await client.credentials.get_all(filter=filter_criteria)
        pytest.fail("Expected an error due to invalid filter value, but none occurred.")
    except Exception as e:
        assert "400" in str(e), f"Expected a 400 error, but got: {e}"
