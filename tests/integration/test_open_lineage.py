import time

import pytest

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, SparkJob
from pyatlan.model.enums import OpenLineageEventType
from pyatlan.model.open_lineage.event import OpenLineageEvent
from pyatlan.model.open_lineage.job import OpenLineageJob
from pyatlan.model.open_lineage.run import OpenLineageRun
from tests.integration.client import TestId, delete_asset

CONNECTION_NAME = TestId.make_unique("OpenLineage")


@pytest.fixture(scope="module")
def connection(client: AtlanClient):
    admin_role_guid = str(RoleCache.get_id_for_name("$admin"))

    c = client.open_lineage.create_connection(
        name=CONNECTION_NAME, admin_roles=[admin_role_guid]
    )
    guid = c.guid
    yield c
    delete_asset(client, asset_type=Connection, guid=guid)


def test_open_lineage_integration(connection: Connection, client: AtlanClient):

    assert connection is not None
    assert connection.name == CONNECTION_NAME
    namespace = "snowflake://abc123.snowflakecomputing.com"
    producer = "https://your.orchestrator/unique/id/123"

    job = OpenLineageJob.creator(
        connection_name=CONNECTION_NAME, job_name="dag_123", producer=producer
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
    assert job
    assert start.event_type == OpenLineageEventType.START
    assert complete.event_type == OpenLineageEventType.COMPLETE

    # Awaiting the creation and storage of the Job asset in the backend
    time.sleep(15)

    job_qualified_name = f"{connection.qualified_name}/{job.name}"
    job_asset = client.asset.get_by_qualified_name(
        qualified_name=job_qualified_name,
        asset_type=SparkJob,
        ignore_relationships=False,
    )

    assert job_asset
    assert job_asset.name == job.name

    inputs = job_asset.inputs
    outputs = job_asset.outputs
    process = job_asset.process

    assert inputs
    assert outputs
    assert process

    input_display_text = [inp.display_text for inp in inputs]
    assert input_display_text[0] == "RUN_STATS"
    assert input_display_text[1] == "TBL"
    assert input_display_text[2] == "TBL"

    assert process.display_text == "dag_123"

    client.asset.purge_by_guid(guid=job_asset.guid)
