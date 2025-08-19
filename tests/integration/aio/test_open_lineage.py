from typing import AsyncGenerator

import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient
from pyatlan.model.assets import Connection
from pyatlan.model.enums import OpenLineageEventType
from pyatlan.model.open_lineage.event import OpenLineageEvent
from pyatlan.model.open_lineage.job import OpenLineageJob
from pyatlan.model.open_lineage.run import OpenLineageRun
from tests.integration.aio.utils import delete_asset_async
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AsyncOpenLineage")


@pytest_asyncio.fixture(scope="module")
async def connection(client: AsyncAtlanClient) -> AsyncGenerator[Connection, None]:
    admin_role_guid = str(await client.role_cache.get_id_for_name("$admin"))
    assert admin_role_guid
    response = await client.open_lineage.create_connection(
        name=MODULE_NAME, admin_roles=[admin_role_guid]
    )
    result = response.assets_created(asset_type=Connection)[0]
    yield await client.asset.get_by_guid(
        result.guid, asset_type=Connection, ignore_relationships=False
    )
    await delete_asset_async(client=client, guid=result.guid, asset_type=Connection)


async def test_open_lineage_integration(
    connection: Connection, client: AsyncAtlanClient
):
    assert connection is not None
    assert connection.name == MODULE_NAME

    namespace = "snowflake://abc123.snowflakecomputing.com"
    producer = "https://your.orchestrator/unique/id/123"
    job = OpenLineageJob.creator(
        connection_name=MODULE_NAME, job_name="dag_123", producer=producer
    )
    run = OpenLineageRun.creator(job=job)
    id = job.create_input(namespace=namespace, asset_name="OPS.DEFAULT.RUN_STATS")
    od = job.create_output(namespace=namespace, asset_name="OPS.DEFAULT.FULL_STATS")
    od.to_fields = [
        {
            "COLUMN": [
                id.from_field(field_name="COLUMN"),
                id.from_field(field_name="ONE"),
                id.from_field(field_name="TWO"),
            ]
        },
        {
            "ANOTHER": [
                id.from_field(field_name="THREE"),
            ]
        },
    ]
    start = OpenLineageEvent.creator(run=run, event_type=OpenLineageEventType.START)
    start.inputs = [
        id,
        job.create_input(namespace=namespace, asset_name="SOME.OTHER.TBL"),
        job.create_input(namespace=namespace, asset_name="AN.OTHER.TBL"),
    ]
    start.outputs = [
        od,
        job.create_output(namespace=namespace, asset_name="AN.OTHER.VIEW"),
    ]
    await start.emit(client=client)  # type: ignore[func-returns-value]

    complete = OpenLineageEvent.creator(
        run=run, event_type=OpenLineageEventType.COMPLETE
    )
    complete.inputs = [
        id,
        job.create_input(namespace=namespace, asset_name="SOME.OTHER.TBL"),
        job.create_input(namespace=namespace, asset_name="AN.OTHER.TBL"),
    ]
    complete.outputs = [
        od,
        job.create_output(namespace=namespace, asset_name="AN.OTHER.VIEW"),
    ]
    await complete.emit(client=client)  # type: ignore[func-returns-value]
