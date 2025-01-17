from pyatlan.client.atlan import AtlanClient
from pyatlan.model.enums import OpenLineageEventType
from pyatlan.model.open_lineage.event import OpenLineageEvent
from pyatlan.model.open_lineage.job import OpenLineageJob
from pyatlan.model.open_lineage.run import OpenLineageRun

client = AtlanClient()
namespace = "snowflake://abc123.snowflakecomputing.com"
producer = "https://your.orchestrator/unique/id/123"

job = OpenLineageJob.creator(
    connection_name="psdk_OpenLineage_75vVY", job_name="dag_123", producer=producer
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

complete = OpenLineageEvent.creator(run=run, event_type=OpenLineageEventType.COMPLETE)
complete.emit()
