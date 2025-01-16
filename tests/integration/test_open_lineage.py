import time

import pytest

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import SparkJob
from pyatlan.model.enums import OpenLineageEventType
from pyatlan.model.open_lineage.event import OpenLineageEvent
from pyatlan.model.open_lineage.job import OpenLineageJob
from pyatlan.model.open_lineage.run import OpenLineageRun

client = AtlanClient()
@pytest.fixture(scope="module")
def connection():
    admin_role_guid = RoleCache.get_id_for_name("$admin")
    connection = client.open_lineage.create_connection(
        name="my-test", admin_roles=[admin_role_guid]
    )
    yield connection
    client.asset.purge_by_guid(guid=connection.guid)


def test_open_lineage_integration(connection: Connection):
    connection = setup_connection

    assert connection is not None
    assert connection.name == "my-test"

    namespace = "snowflake://abc123.snowflakecomputing.com"
    producer = "https://your.orchestrator/unique/id/123"
    time.sleep(5)
    job = OpenLineageJob.creator(
        connection_name="my-test", job_name="dag_123", producer=producer
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

    start.emit()

    complete = OpenLineageEvent.creator(
        run=run, event_type=OpenLineageEventType.COMPLETE
    )
    complete.emit()

    assert start.event_type == OpenLineageEventType.START
    assert complete.event_type == OpenLineageEventType.COMPLETE
    time.sleep(15)
   job_qualified_name = f"{connection.qualified_name}/{job.name}"
    job_asset = client.asset.get_by_qualified_name(
        qualified_name=qualified_name_jobs, asset_type=SparkJob
    )
    assert job_asset
    assert job_asset.name == job.name
    client.asset.purge_by_guid(guid=job_asset.guid)
