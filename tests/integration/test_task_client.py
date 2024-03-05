import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Column
from pyatlan.model.enums import (
    AtlanConnectorType,
    AtlanTagColor,
    AtlanTaskType,
    SortOrder,
)
from pyatlan.model.fluent_tasks import FluentTasks
from pyatlan.model.search import SortItem
from pyatlan.model.task import AtlanTask, TaskSearchRequest
from pyatlan.model.typedef import AtlanTagDef
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("TaskClient")
TAG_NAME = MODULE_NAME

DB_NAME = "RAW"
TABLE_NAME = "PACKAGETYPES"
COLUMN_NAME = "PACKAGETYPENAME"
SCHEMA_NAME = "WIDEWORLDIMPORTERS_WAREHOUSE"


@pytest.fixture(scope="module")
def snowflake_conn(client: AtlanClient):
    return client.asset.find_connections_by_name(
        "development", AtlanConnectorType.SNOWFLAKE
    )[0]


@pytest.fixture(scope="module")
def snowflake_column_qn(snowflake_conn):
    return f"{snowflake_conn.qualified_name}/{DB_NAME}/{SCHEMA_NAME}/{TABLE_NAME}/{COLUMN_NAME}"


@pytest.fixture()
def snowflake_column(client: AtlanClient, snowflake_column_qn) -> Column:
    client.asset.add_atlan_tags(
        asset_type=Column,
        qualified_name=snowflake_column_qn,
        atlan_tag_names=[TAG_NAME],
        propagate=True,
        remove_propagation_on_delete=True,
        restrict_lineage_propagation=True,
    )
    snowflake_column = client.asset.get_by_qualified_name(
        snowflake_column_qn, asset_type=Column
    )
    return snowflake_column


@pytest.fixture()
def task_search_request(snowflake_column: Column) -> TaskSearchRequest:
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


@pytest.fixture(scope="module")
def atlan_tag_def(
    client: AtlanClient,
    snowflake_column_qn,
) -> Generator[AtlanTagDef, None, None]:
    atlan_tag_def = AtlanTagDef.create(name=TAG_NAME, color=AtlanTagColor.GREEN)
    typedef = client.typedef.create(atlan_tag_def)
    yield typedef.atlan_tag_defs[0]
    client.asset.remove_atlan_tag(
        asset_type=Column,
        qualified_name=snowflake_column_qn,
        atlan_tag_name=TAG_NAME,
    )
    client.typedef.purge(TAG_NAME, typedef_type=AtlanTagDef)


def test_task_search(
    client: AtlanClient, atlan_tag_def, task_search_request, snowflake_column
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
        tasks = client.tasks.search(request=task_search_request)
        assert tasks
        if tasks.count >= 1:
            task = next(iter(tasks))
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
