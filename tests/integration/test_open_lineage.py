import time

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset, Connection, Process, SparkJob
from pyatlan.model.audit import AuditSearchRequest
from pyatlan.model.enums import OpenLineageEventType
from pyatlan.model.open_lineage.event import OpenLineageEvent
from pyatlan.model.open_lineage.job import OpenLineageJob
from pyatlan.model.open_lineage.run import OpenLineageRun
from tests.integration.client import TestId, delete_asset

MODULE_NAME = TestId.make_unique("OL")


@pytest.fixture(scope="module")
def connection(client: AtlanClient):
    admin_role_guid = client.role_cache.get_id_for_name("$admin")
    assert admin_role_guid
    response = client.open_lineage.create_connection(
        name=MODULE_NAME, admin_roles=[admin_role_guid]
    )
    result = response.assets_created(asset_type=Connection)[0]
    yield client.asset.get_by_guid(
        result.guid, asset_type=Connection, ignore_relationships=False
    )
    delete_asset(client, asset_type=Connection, guid=result.guid)


def test_open_lineage_integration(connection: Connection, client: AtlanClient):
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
    start.emit()

    complete = OpenLineageEvent.creator(
        run=run, event_type=OpenLineageEventType.COMPLETE
    )
    complete.emit()

    assert job
    assert start.event_type == OpenLineageEventType.START
    assert complete.event_type == OpenLineageEventType.COMPLETE

    # Awaiting the creation and storage of the Job asset in the backend
    time.sleep(30)

    job_qualified_name = f"{connection.qualified_name}/{job.name}"

    # Use the audit search, similar to UI calls,
    # to retrieve complete information (process, inputs, outputs) about Spark jobs
    results = client.audit.search(
        AuditSearchRequest.by_qualified_name(
            type_name=SparkJob.__name__,
            qualified_name=job_qualified_name,
        )
    )
    assert results and results.current_page() and len(results.current_page()) > 0
    job_asset = results.current_page()[0]
    assert (
        job_asset
        and job_asset.detail
        and isinstance(job_asset.detail, Asset)
        and job_asset.detail.relationship_attributes
    )
    assert job_asset.detail.name == job.name
    assert job_asset.detail.qualified_name == job_qualified_name

    inputs = job_asset.detail.relationship_attributes.get("inputs")
    outputs = job_asset.detail.relationship_attributes.get("outputs")
    process = job_asset.detail.relationship_attributes.get("process")

    assert inputs
    assert outputs
    assert process

    input_qns = {
        input.get("uniqueAttributes", {}).get("qualifiedName") for input in inputs
    }
    assert f"{connection.qualified_name}/OPS/DEFAULT/RUN_STATS" in input_qns
    assert f"{connection.qualified_name}/SOME/OTHER/TBL" in input_qns
    assert f"{connection.qualified_name}/AN/OTHER/TBL" in input_qns

    outputs_qns = {
        output.get("uniqueAttributes", {}).get("qualifiedName") for output in outputs
    }
    assert f"{connection.qualified_name}/OPS/DEFAULT/FULL_STATS" in outputs_qns
    assert f"{connection.qualified_name}/AN/OTHER/VIEW" in outputs_qns
    assert (
        process.get("uniqueAttributes", {}).get("qualifiedName")
        == f"{connection.qualified_name}/dag_123/process"
    )
    delete_asset(client, asset_type=Process, guid=process.get("guid"))
    delete_asset(client, asset_type=SparkJob, guid=job_asset.detail.guid)
