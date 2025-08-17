import time
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.assets import Column
from pyatlan.model.enums import AtlanConnectorType, AtlanTaskType, SortOrder
from pyatlan.model.fluent_tasks import FluentTasks
from pyatlan.model.search import SortItem
from pyatlan.model.task import AtlanTask, TaskSearchRequest
from pyatlan.model.typedef import AtlanTagDef
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AsyncTaskClient")
TAG_NAME = MODULE_NAME

DB_NAME = "WIDE_WORLD_IMPORTERS"
TABLE_NAME = "PACKAGETYPES"
COLUMN_NAME = "PACKAGETYPENAME"
SCHEMA_NAME = "BRONZE_WAREHOUSE"


@pytest_asyncio.fixture(scope="module")
async def snowflake_conn(client: AsyncAtlanClient):
    return (
        await client.asset.find_connections_by_name(
            "production", AtlanConnectorType.SNOWFLAKE
        )
    )[0]


@pytest_asyncio.fixture(scope="module")
async def snowflake_column_qn(snowflake_conn):
    return f"{snowflake_conn.qualified_name}/{DB_NAME}/{SCHEMA_NAME}/{TABLE_NAME}/{COLUMN_NAME}"


@pytest_asyncio.fixture()
async def snowflake_column(
    client: AsyncAtlanClient, snowflake_column_qn
) -> AsyncGenerator[Column, None]:
    await client.asset.add_atlan_tags(
        asset_type=Column,
        qualified_name=snowflake_column_qn,
        atlan_tag_names=[TAG_NAME],
        propagate=True,
        remove_propagation_on_delete=True,
        restrict_lineage_propagation=True,
    )
    snowflake_column = await client.asset.get_by_qualified_name(
        snowflake_column_qn, asset_type=Column, ignore_relationships=False
    )
    yield snowflake_column
    await client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=snowflake_column_qn,
        atlan_tag_name=TAG_NAME,
    )


@pytest_asyncio.fixture(scope="module")
async def atlan_tag_def(make_atlan_tag_async) -> AtlanTagDef:
    return await make_atlan_tag_async(TAG_NAME)


@pytest_asyncio.fixture()
async def task_search_request(snowflake_column: Column) -> TaskSearchRequest:
    return (
        FluentTasks()
        .page_size(1)
        .sort(
            by=SortItem(
                field=AtlanTask.START_TIME.numeric_field_name,
                order=SortOrder.DESCENDING,
            )
        )
        .where(AtlanTask.ENTITY_GUID.eq(snowflake_column.guid))
        .where(AtlanTask.TYPE.eq(AtlanTaskType.CLASSIFICATION_PROPAGATION_ADD.value))
        .to_request()
    )


async def test_task_search(
    client: AsyncAtlanClient, atlan_tag_def, task_search_request, snowflake_column
):
    assert snowflake_column
    assert snowflake_column.atlan_tags

    for tag in snowflake_column.atlan_tags:
        if str(tag.type_name) == TAG_NAME:
            break
        pytest.fail(f"Tag '{TAG_NAME}' missing in {snowflake_column}")

    count = 0
    # TODO: replace with exponential back-off and jitter
    while count < 10:
        tasks = await client.tasks.search(request=task_search_request)
        assert tasks
        if tasks.count >= 1:
            async for task in tasks:
                break
        count += 1
        time.sleep(5)

    assert task.guid
    assert task.status
    assert task.created_by
    assert task.updated_time
    assert task.parameters
    assert task.classification_id
    assert task.attempt_count is not None and task.attempt_count >= 0
    assert task.entity_guid == snowflake_column.guid
    assert task.type == AtlanTaskType.CLASSIFICATION_PROPAGATION_ADD
